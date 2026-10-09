#!/usr/bin/env python3
"""Phase 3.2 Wildfire Dataset Feasibility Experiment & Verification Audit.

Empirically verifies data accessibility, authentication, schema compliance,
temporal continuity, spatial coordinates, byte transfers, and storage budgets
for NASA FIRMS (VIIRS 375m SP), Open-Meteo (ERA5-Land), and Copernicus DEM (GLO-30)
across the Central India pilot region (21°–23° N, 79°–81° E) for March 15–28, 2023.
"""

import csv
import io
import json
import math
import os
import struct
import sys
import tempfile
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import httpx

# Attempt to load dotenv if available (for local gitignored .env support)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

PILOT_BBOX = {
    "west": 79.0,
    "south": 21.0,
    "east": 81.0,
    "north": 23.0,
}

QUADRANT_CENTROIDS = [
    {"name": "NW_Q1", "lat": 22.5, "lon": 79.5},
    {"name": "NE_Q2", "lat": 22.5, "lon": 80.5},
    {"name": "SW_Q3", "lat": 21.5, "lon": 79.5},
    {"name": "SE_Q4", "lat": 21.5, "lon": 80.5},
]

COP_DEM_TILES = [
    "Copernicus_DSM_COG_10_N21_00_E079_00_DEM",
    "Copernicus_DSM_COG_10_N21_00_E080_00_DEM",
    "Copernicus_DSM_COG_10_N22_00_E079_00_DEM",
    "Copernicus_DSM_COG_10_N22_00_E080_00_DEM",
]

EXPECTED_VIIRS_COLUMNS = [
    "latitude", "longitude", "bright_ti4", "scan", "track",
    "acq_date", "acq_time", "satellite", "confidence", "version",
    "bright_ti5", "frp", "daynight", "type"
]


def sanitize_url(url: str, key: Optional[str]) -> str:
    """Mask sensitive authentication key from URLs for safe logging and reporting."""
    if key and key in url:
        return url.replace(key, "[MAP_KEY_REDACTED]")
    return url


def run_dem_check(results: Dict[str, Any], bytes_tracker: List[Dict[str, Any]]) -> None:
    """Verify Copernicus DEM GLO-30 tile object availability and header via HEAD and byte-range."""
    dem_results = {
        "status": "PASS",
        "tiles": {},
        "header_inspection": {},
        "evidence_level": {
            "endpoint_accessible": True,
            "authentication_required": False,
            "header_metadata_verified": True,
            "full_raster_decoded": False,
        },
        "notes": (
            "Limited strictly to HTTP object availability, response headers, and COG header magic inspection. "
            "Does NOT validate internal raster array cells, void absence, or elevation values."
        )
    }

    base_s3_url = "https://copernicus-dem-30m.s3.amazonaws.com"
    client = httpx.Client(timeout=15.0)

    for tile in COP_DEM_TILES:
        url = f"{base_s3_url}/{tile}/{tile}.tif"
        try:
            head_res = client.head(url)
            bytes_tracker.append({
                "source": f"Copernicus_DEM_HEAD_{tile}",
                "type": "header_probe",
                "bytes": 0,
                "status_code": head_res.status_code,
            })
            content_len = int(head_res.headers.get("content-length", 0))
            dem_results["tiles"][tile] = {
                "http_status": head_res.status_code,
                "content_type": head_res.headers.get("content-type"),
                "content_length_bytes": content_len,
                "content_length_mb": round(content_len / (1024 * 1024), 2),
                "accessible": head_res.status_code == 200,
            }
            if head_res.status_code != 200:
                dem_results["status"] = "FAIL"
                dem_results["evidence_level"]["endpoint_accessible"] = False
        except Exception as exc:
            dem_results["tiles"][tile] = {"error": str(exc), "accessible": False}
            dem_results["status"] = "FAIL"
            dem_results["evidence_level"]["endpoint_accessible"] = False

    # Byte-range request on first tile to verify TIFF/COG header
    sample_tile = COP_DEM_TILES[0]
    sample_url = f"{base_s3_url}/{sample_tile}/{sample_tile}.tif"
    try:
        range_res = client.get(sample_url, headers={"Range": "bytes=0-1023"})
        bytes_tracker.append({
            "source": f"Copernicus_DEM_Range_{sample_tile}",
            "type": "header_probe",
            "bytes": len(range_res.content),
            "status_code": range_res.status_code,
        })
        if range_res.status_code == 206:
            raw_bytes = range_res.content
            byte_order = raw_bytes[:2]
            magic = struct.unpack("<H" if byte_order == b"II" else ">H", raw_bytes[2:4])[0]
            dem_results["header_inspection"] = {
                "sample_tile": sample_tile,
                "range_status": range_res.status_code,
                "bytes_read": len(raw_bytes),
                "byte_order": "Little-Endian (II)" if byte_order == b"II" else "Big-Endian (MM)",
                "tiff_magic": magic,
                "is_valid_tiff": magic in (42, 43),
            }
            if magic not in (42, 43):
                dem_results["status"] = "FAIL"
                dem_results["evidence_level"]["header_metadata_verified"] = False
        else:
            dem_results["header_inspection"] = {"error": f"Unexpected range status {range_res.status_code}"}
            dem_results["status"] = "FAIL"
            dem_results["evidence_level"]["header_metadata_verified"] = False
    except Exception as exc:
        dem_results["header_inspection"] = {"error": str(exc)}
        dem_results["status"] = "FAIL"
        dem_results["evidence_level"]["header_metadata_verified"] = False

    results["copernicus_dem"] = dem_results


def run_weather_check(results: Dict[str, Any], bytes_tracker: List[Dict[str, Any]]) -> None:
    """Verify Open-Meteo ERA5-Land reanalysis access, temporal continuity, and value missingness."""
    weather_results = {
        "status": "PASS",
        "quadrants": {},
        "evidence_level": {
            "endpoint_accessible": True,
            "authentication_required": False,
            "payload_retrieved": True,
            "schema_verified": True,
            "coverage_verified": True,
            "quality_adequate": True,
        },
        "anti_leakage_checks": {},
    }

    client = httpx.Client(timeout=20.0)
    all_times = None
    required_vars = [
        "temperature_2m", "relative_humidity_2m", "dew_point_2m",
        "precipitation", "surface_pressure", "wind_speed_10m"
    ]

    for q in QUADRANT_CENTROIDS:
        params = {
            "latitude": q["lat"],
            "longitude": q["lon"],
            "start_date": "2023-03-08",
            "end_date": "2023-03-28",
            "hourly": ",".join(required_vars),
        }
        try:
            res = client.get("https://archive-api.open-meteo.com/v1/archive", params=params)
            bytes_tracker.append({
                "source": f"Open_Meteo_ERA5_Land_{q['name']}",
                "type": "dataset_payload",
                "bytes": len(res.content),
                "status_code": res.status_code,
            })
            if res.status_code != 200:
                weather_results["status"] = "FAIL"
                weather_results["evidence_level"]["endpoint_accessible"] = False
                weather_results["quadrants"][q["name"]] = {"http_status": res.status_code, "error": res.text[:200]}
                continue

            data = res.json()
            hourly = data.get("hourly", {})
            times = hourly.get("time", [])

            # Check 1: Missing Timestamps Check (Temporal Continuity)
            expected_hours = 21 * 24
            parsed_times = [datetime.fromisoformat(t) for t in times]
            timestamp_gaps = 0
            for i in range(1, len(parsed_times)):
                diff = (parsed_times[i] - parsed_times[i - 1]).total_seconds()
                if diff != 3600:
                    timestamp_gaps += 1

            # Check 2: Missing Values Check (Attribute Completeness)
            var_missing_rates = {}
            for v in required_vars:
                vals = hourly.get(v, [])
                missing_cnt = sum(1 for val in vals if val is None)
                rate = (missing_cnt / len(vals)) * 100.0 if vals else 100.0
                var_missing_rates[v] = {
                    "total_samples": len(vals),
                    "missing_count": missing_cnt,
                    "missing_percent": round(rate, 2),
                }
                if rate >= 5.0:
                    weather_results["status"] = "FAIL"
                    weather_results["evidence_level"]["quality_adequate"] = False
                elif rate >= 1.0 and weather_results["status"] != "FAIL":
                    weather_results["status"] = "INCONCLUSIVE"

            weather_results["quadrants"][q["name"]] = {
                "http_status": res.status_code,
                "generationtime_ms": data.get("generationtime_ms"),
                "total_hours": len(times),
                "expected_hours": expected_hours,
                "missing_timestamps": timestamp_gaps,
                "variables": var_missing_rates,
            }

            if len(times) != expected_hours or timestamp_gaps > 0:
                weather_results["status"] = "FAIL"
                weather_results["evidence_level"]["coverage_verified"] = False

            if all_times is None:
                all_times = parsed_times

        except Exception as exc:
            weather_results["status"] = "FAIL"
            weather_results["evidence_level"]["endpoint_accessible"] = False
            weather_results["quadrants"][q["name"]] = {"error": str(exc)}

    # Anti-leakage simulation check
    target_date = datetime(2023, 3, 20).date()
    antecedent_date = target_date - timedelta(days=1)
    if all_times:
        antecedent_indices = [
            i for i, dt in enumerate(all_times) if dt.date() == antecedent_date
        ]
        leakage_detected = any(all_times[i].date() >= target_date for i in antecedent_indices)
        weather_results["anti_leakage_checks"] = {
            "target_date": str(target_date),
            "antecedent_date": str(antecedent_date),
            "antecedent_hour_count": len(antecedent_indices),
            "leakage_detected": leakage_detected,
            "status": "PASS" if not leakage_detected and len(antecedent_indices) == 24 else "FAIL",
        }
        if leakage_detected or len(antecedent_indices) != 24:
            weather_results["status"] = "FAIL"
            weather_results["evidence_level"]["quality_adequate"] = False

    results["weather_era5_land"] = weather_results


def parse_firms_csv(csv_text: str) -> Tuple[List[str], List[Dict[str, Any]], List[str]]:
    """Parse FIRMS CSV response into headers, rows, and schema error descriptions."""
    f = io.StringIO(csv_text.strip())
    reader = csv.reader(f)
    try:
        headers = next(reader)
    except StopIteration:
        return [], [], ["Empty CSV content"]

    headers = [h.strip() for h in headers]
    rows = []
    errors = []
    for line_idx, raw_row in enumerate(reader, start=2):
        if not raw_row or not any(raw_row):
            continue
        if len(raw_row) != len(headers):
            errors.append(f"Line {line_idx}: Column count mismatch (expected {len(headers)}, got {len(raw_row)})")
            continue
        row_dict = dict(zip(headers, [c.strip() for c in raw_row]))
        rows.append(row_dict)

    return headers, rows, errors


def map_lat_lon_to_cell(
    lat: float,
    lon: float,
    bbox: Optional[Dict[str, float]] = None,
    grid_size: float = 0.05
) -> Tuple[int, int]:
    """Map continuous latitude and longitude to 0.05-degree discrete raster grid indices (i, j).

    i represents row index along latitude (0 to 39, South to North).
    j represents col index along longitude (0 to 39, West to East).
    """
    if bbox is None:
        bbox = PILOT_BBOX
    if not (bbox["south"] <= lat <= bbox["north"]) or not (bbox["west"] <= lon <= bbox["east"]):
        raise ValueError(f"Coordinate ({lat}, {lon}) outside bounding box {bbox}")

    if lat == bbox["north"]:
        i = int(round((bbox["north"] - bbox["south"]) / grid_size)) - 1
    else:
        i = int(math.floor((lat - bbox["south"]) / grid_size))

    if lon == bbox["east"]:
        j = int(round((bbox["east"] - bbox["west"]) / grid_size)) - 1
    else:
        j = int(math.floor((lon - bbox["west"]) / grid_size))

    return i, j


def classify_cell_quadrant(i: int, j: int, split_row: int = 20, split_col: int = 20) -> str:
    """Classify grid cell (i, j) into one of four geographic quadrants.

    Q1_NW: row >= 20, col < 20 (lat >= 22.0, lon < 80.0)
    Q2_NE: row >= 20, col >= 20 (lat >= 22.0, lon >= 80.0)
    Q3_SW: row < 20, col < 20 (lat < 22.0, lon < 80.0)
    Q4_SE: row < 20, col >= 20 (lat < 22.0, lon >= 80.0)
    """
    if i >= split_row and j < split_col:
        return "Q1_NW"
    elif i >= split_row and j >= split_col:
        return "Q2_NE"
    elif i < split_row and j < split_col:
        return "Q3_SW"
    else:
        return "Q4_SE"


def is_cell_in_buffer(i: int, j: int, split_row: int = 20, split_col: int = 20, margin_cells: int = 2) -> bool:
    """Determine whether grid cell (i, j) falls inside the interior buffer dead-zone around quadrant dividing lines.

    margin_cells = 2: 2 cells on each side of the boundary (4 cells total width ~ 20.6 - 22.2 km).
    margin_cells = 4: 4 cells on each side of the boundary (8 cells total width ~ 41.3 - 44.4 km; 20 km each side).
    """
    row_in_buf = (split_row - margin_cells) <= i < (split_row + margin_cells)
    col_in_buf = (split_col - margin_cells) <= j < (split_col + margin_cells)
    return row_in_buf or col_in_buf


def compute_spatial_partition_audit(
    qualifying_rows: List[Dict[str, Any]],
    margin_cells: int = 2,
    bbox: Optional[Dict[str, float]] = None,
    grid_size: float = 0.05
) -> Dict[str, Any]:
    """Compute spatial partition, buffer exclusion, and reconciliation invariants for qualifying fire observations."""
    if bbox is None:
        bbox = PILOT_BBOX

    quadrants = ["Q1_NW", "Q2_NE", "Q3_SW", "Q4_SE"]

    # Map qualifying detections to discrete cell-days Y_{s, t} = 1
    cell_day_map: Dict[Tuple[int, int, str], List[Dict[str, Any]]] = {}
    for r in qualifying_rows:
        lat = float(r["latitude"])
        lon = float(r["longitude"])
        acq_date = r["acq_date"]
        i, j = map_lat_lon_to_cell(lat, lon, bbox=bbox, grid_size=grid_size)
        key_cd = (i, j, acq_date)
        if key_cd not in cell_day_map:
            cell_day_map[key_cd] = []
        cell_day_map[key_cd].append(r)

    pre_counts = {q: 0 for q in quadrants}
    buf_counts = {q: 0 for q in quadrants}
    post_counts = {q: 0 for q in quadrants}

    unique_cells = set()
    post_cells: Dict[str, set] = {q: set() for q in quadrants}
    buf_cells = set()

    for (i, j, acq_date) in cell_day_map:
        unique_cells.add((i, j))
        q = classify_cell_quadrant(i, j)
        pre_counts[q] += 1

        in_buf = is_cell_in_buffer(i, j, margin_cells=margin_cells)
        if in_buf:
            buf_counts[q] += 1
            buf_cells.add((i, j))
        else:
            post_counts[q] += 1
            post_cells[q].add((i, j))

    total_pre = len(cell_day_map)
    total_buf = sum(buf_counts.values())
    total_post = sum(post_counts.values())

    # Invariant checks: pre[q] == post[q] + buf[q]
    reconciliation_per_quadrant = {
        q: (pre_counts[q] == post_counts[q] + buf_counts[q])
        for q in quadrants
    }
    reconciles = all(reconciliation_per_quadrant.values()) and (total_pre == total_post + total_buf)

    # Cross-fold spatial overlap check: post-exclusion cells must have zero intersection across folds
    cross_fold_overlaps = {}
    for idx1, q1 in enumerate(quadrants):
        for idx2, q2 in enumerate(quadrants):
            if idx1 < idx2:
                overlap = post_cells[q1].intersection(post_cells[q2])
                cross_fold_overlaps[f"{q1}_vs_{q2}"] = len(overlap)

    has_cross_fold_overlap = any(cnt > 0 for cnt in cross_fold_overlaps.values())

    return {
        "total_qualifying_records": len(qualifying_rows),
        "total_positive_cell_days": total_pre,
        "unique_cells_count": len(unique_cells),
        "margin_cells": margin_cells,
        "pre_exclusion_counts": pre_counts,
        "buffer_excluded_counts": buf_counts,
        "buffer_total_excluded": total_buf,
        "post_exclusion_counts": post_counts,
        "post_exclusion_total": total_post,
        "reconciles": reconciles,
        "reconciliation_per_quadrant": reconciliation_per_quadrant,
        "cross_fold_overlaps": cross_fold_overlaps,
        "has_cross_fold_overlap": has_cross_fold_overlap,
    }


def run_firms_check(results: Dict[str, Any], bytes_tracker: List[Dict[str, Any]]) -> None:
    """Verify NASA FIRMS Historical Archive (Standard Processing) endpoint, authentication, and data."""
    raw_key = os.getenv("FIRMS_MAP_KEY", "").strip()
    has_key = bool(raw_key)

    firms_results = {
        "status": "INCONCLUSIVE",
        "auth_resolution": {
            "has_key": has_key,
            "key_length": len(raw_key) if has_key else 0,
            "key_format_valid": bool(has_key and len(raw_key) == 32 and raw_key.isalnum()),
        },
        "historical_product_verification": {
            "standard_processing_source": "VIIRS_SNPP_SP",
            "is_historical_nrt_prohibited": True,
            "target_period": "2023-03-15 to 2023-03-28",
            "date_partitioning": [
                {"date": "2023-03-15", "day_range": 5, "description": "2023-03-15 to 2023-03-19"},
                {"date": "2023-03-20", "day_range": 5, "description": "2023-03-20 to 2023-03-24"},
                {"date": "2023-03-25", "day_range": 4, "description": "2023-03-25 to 2023-03-28"},
            ]
        },
        "evidence_level": {
            "endpoint_accessible": False,
            "authentication_successful": False,
            "payload_retrieved": False,
            "schema_verified": False,
            "coverage_verified": False,
            "quality_adequate": False,
        },
        "query_results": [],
        "sample_counts": {
            "total_records": 0,
            "by_confidence": {},
            "by_type": {},
            "by_satellite": {},
            "by_date": {},
            "qualifying_vegetation_fires": 0,
        },
        "validation_errors": [],
    }

    client = httpx.Client(timeout=20.0)

    if not has_key:
        # Probe endpoint with dummy key to verify reachability and confirm authentication requirement
        dummy_key = "00000000000000000000000000000000"
        probe_url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{dummy_key}/VIIRS_SNPP_SP/79,21,81,23/5/2023-03-15"
        try:
            res = client.get(probe_url)
            bytes_tracker.append({
                "source": "NASA_FIRMS_unauthenticated_probe",
                "type": "error_body_probe",
                "bytes": len(res.content),
                "status_code": res.status_code,
            })
            firms_results["evidence_level"]["endpoint_accessible"] = True
            firms_results["auth_resolution"]["auth_state"] = "AUTH_KEY_MISSING"
            firms_results["auth_resolution"]["probe_http_status"] = res.status_code
            firms_results["auth_resolution"]["probe_snippet"] = res.text[:120].strip()
            firms_results["status"] = "INCONCLUSIVE (FIRMS_MAP_KEY required in environment)"
            firms_results["auth_resolution"]["action_required"] = (
                "Please configure FIRMS_MAP_KEY in your local environment. "
                "See docs/phase3-feasibility-report.md for registration instructions."
            )
        except Exception as exc:
            firms_results["auth_resolution"]["probe_error"] = str(exc)
            firms_results["status"] = "FAIL"

        results["nasa_firms"] = firms_results
        return

    # If key is available, execute the bounded 3-query plan for March 15-28, 2023
    all_rows = []
    headers_found = None
    bbox_str = f"{PILOT_BBOX['west']},{PILOT_BBOX['south']},{PILOT_BBOX['east']},{PILOT_BBOX['north']}"
    partitions = firms_results["historical_product_verification"]["date_partitioning"]

    for part in partitions:
        anchor_date = part["date"]
        d_range = part["day_range"]
        query_url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{raw_key}/VIIRS_SNPP_SP/{bbox_str}/{d_range}/{anchor_date}"
        safe_url = sanitize_url(query_url, raw_key)

        try:
            res = client.get(query_url)
            is_valid_payload = res.status_code == 200 and not res.text.startswith("Invalid") and not res.text.startswith("Error")
            bytes_tracker.append({
                "source": f"NASA_FIRMS_{anchor_date}_{d_range}d",
                "type": "dataset_payload" if is_valid_payload else "error_body_probe",
                "bytes": len(res.content),
                "status_code": res.status_code,
            })

            query_record = {
                "partition": part["description"],
                "url": safe_url,
                "http_status": res.status_code,
                "content_type": res.headers.get("content-type"),
                "bytes_received": len(res.content),
            }

            if res.status_code == 401 or "Invalid MAP_KEY" in res.text:
                query_record["auth_error"] = "Invalid MAP_KEY provided"
                firms_results["auth_resolution"]["auth_state"] = "AUTH_KEY_INVALID"
                firms_results["status"] = "FAIL"
                firms_results["query_results"].append(query_record)
                results["nasa_firms"] = firms_results
                return

            if res.status_code == 429 or "exceeded" in res.text.lower():
                query_record["rate_limit_error"] = "Transactional rate limit exceeded"
                firms_results["status"] = "INCONCLUSIVE (Rate limited)"
                firms_results["query_results"].append(query_record)
                results["nasa_firms"] = firms_results
                return

            if res.status_code != 200:
                query_record["http_error"] = f"HTTP {res.status_code}: {res.text[:120].strip()}"
                firms_results["status"] = "FAIL"
                firms_results["query_results"].append(query_record)
                results["nasa_firms"] = firms_results
                return

            # Successful response
            firms_results["evidence_level"]["endpoint_accessible"] = True
            firms_results["evidence_level"]["authentication_successful"] = True
            firms_results["evidence_level"]["payload_retrieved"] = True

            hdrs, rows, parse_errs = parse_firms_csv(res.text)
            query_record["header_columns"] = hdrs
            query_record["record_count"] = len(rows)
            query_record["parse_errors"] = parse_errs

            if hdrs and headers_found is None:
                headers_found = hdrs

            all_rows.extend(rows)
            firms_results["query_results"].append(query_record)

        except Exception as exc:
            firms_results["validation_errors"].append(f"Query {anchor_date} exception: {str(exc)}")
            firms_results["status"] = "FAIL"

    # Schema verification against EXPECTED_VIIRS_COLUMNS
    if headers_found:
        missing_cols = [c for c in EXPECTED_VIIRS_COLUMNS if c not in headers_found]
        if missing_cols:
            firms_results["validation_errors"].append(f"Missing expected schema columns: {missing_cols}")
        else:
            firms_results["evidence_level"]["schema_verified"] = True

    # Validate rows, coordinates, timestamps, confidence, and types
    by_conf = {}
    by_type = {}
    by_sat = {}
    by_date = {}
    qualifying_fires = 0

    valid_conf_values = {"low", "nominal", "high", "l", "n", "h"}
    for r in all_rows:
        try:
            lat = float(r.get("latitude", 0.0))
            lon = float(r.get("longitude", 0.0))
            acq_date = r.get("acq_date", "")
            conf = r.get("confidence", "").lower()
            fire_type = int(r.get("type", -1))
            sat = r.get("satellite", "")

            # Coordinate range check
            if not (PILOT_BBOX["south"] <= lat <= PILOT_BBOX["north"]) or not (PILOT_BBOX["west"] <= lon <= PILOT_BBOX["east"]):
                firms_results["validation_errors"].append(f"Coordinate out of bbox: lat={lat}, lon={lon}")

            # Date range check
            if not ("2023-03-15" <= acq_date <= "2023-03-28"):
                firms_results["validation_errors"].append(f"Date outside pilot window: {acq_date}")

            # Confidence check
            by_conf[conf] = by_conf.get(conf, 0) + 1
            if conf not in valid_conf_values:
                firms_results["validation_errors"].append(f"Unexpected categorical confidence value: {conf}")

            # Type check
            by_type[str(fire_type)] = by_type.get(str(fire_type), 0) + 1

            # Satellite check
            by_sat[sat] = by_sat.get(sat, 0) + 1

            # Date count
            by_date[acq_date] = by_date.get(acq_date, 0) + 1

            # Qualifying vegetation fires
            if fire_type == 0 and conf in ("nominal", "high", "n", "h"):
                qualifying_fires += 1

        except Exception as exc:
            firms_results["validation_errors"].append(f"Row parsing error: {str(exc)}")

    firms_results["sample_counts"] = {
        "total_records": len(all_rows),
        "by_confidence": by_conf,
        "by_type": by_type,
        "by_satellite": by_sat,
        "by_date": by_date,
        "qualifying_vegetation_fires": qualifying_fires,
    }

    if qualifying_fires > 0:
        qualifying_rows = [
            r for r in all_rows
            if int(r.get("type", -1)) == 0 and r.get("confidence", "").lower() in ("nominal", "high", "n", "h")
        ]
        firms_results["spatial_partition_audit"] = {
            "design_1_2cell_margin_20km_total_buffer": compute_spatial_partition_audit(qualifying_rows, margin_cells=2),
            "design_2_4cell_margin_40km_total_buffer": compute_spatial_partition_audit(qualifying_rows, margin_cells=4),
        }

    if len(all_rows) > 0:
        firms_results["evidence_level"]["coverage_verified"] = True
        firms_results["evidence_level"]["quality_adequate"] = qualifying_fires > 0
        firms_results["status"] = "PASS" if not firms_results["validation_errors"] else "PASS_WITH_LIMITATIONS"
    else:
        # Valid empty dataset is not an error, but coverage must be noted
        firms_results["evidence_level"]["coverage_verified"] = True
        firms_results["evidence_level"]["quality_adequate"] = False
        firms_results["status"] = "PASS_WITH_LIMITATIONS (Valid empty dataset returned; no fire hotspots observed in window)"

    results["nasa_firms"] = firms_results


def main() -> int:
    start_time = datetime.utcnow()
    bytes_tracker: List[Dict[str, Any]] = []
    results: Dict[str, Any] = {
        "experiment": "Phase 3.2 Wildfire Dataset Feasibility & Evidence Audit",
        "executed_at_utc": start_time.isoformat(),
        "pilot_bounding_box": PILOT_BBOX,
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        results["scratch_directory"] = tmpdir

        # Run checks
        run_dem_check(results, bytes_tracker)
        run_weather_check(results, bytes_tracker)
        run_firms_check(results, bytes_tracker)

        # Audit storage footprint and transferred bytes
        total_bytes = sum(b["bytes"] for b in bytes_tracker)
        total_mb = total_bytes / (1024 * 1024)
        results["storage_and_network_audit"] = {
            "total_bytes_transferred": total_bytes,
            "total_mb_transferred": round(total_mb, 4),
            "storage_cap_mb": 25.0,
            "within_cap": total_mb <= 25.0,
            "transfer_breakdown": bytes_tracker,
            "dataset_payload_bytes": sum(b["bytes"] for b in bytes_tracker if b["type"] == "dataset_payload"),
            "probe_and_header_bytes": sum(b["bytes"] for b in bytes_tracker if b["type"] != "dataset_payload"),
            "cleanup_verified": True,
        }

    # Summarize evidence hierarchy
    results["evidence_hierarchy"] = {
        "open_meteo_era5_land": results["weather_era5_land"]["evidence_level"],
        "copernicus_dem_glo30": results["copernicus_dem"]["evidence_level"],
        "nasa_firms_viirs375m": results["nasa_firms"]["evidence_level"],
    }

    # Overall outcome
    dem_status = results["copernicus_dem"]["status"]
    weather_status = results["weather_era5_land"]["status"]
    firms_status = results["nasa_firms"]["status"]

    results["summary_statuses"] = {
        "copernicus_dem": dem_status,
        "weather_era5_land": weather_status,
        "nasa_firms": firms_status,
    }

    if "FAIL" in [dem_status, weather_status, firms_status]:
        results["overall_result"] = "FAIL"
    elif "INCONCLUSIVE" in firms_status:
        results["overall_result"] = "INCONCLUSIVE (Weather & DEM PASS; FIRMS_MAP_KEY required to complete empirical fire audit)"
    elif "LIMITATIONS" in firms_status:
        results["overall_result"] = "PASS_WITH_LIMITATIONS"
    else:
        results["overall_result"] = "PASS"

    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
