"""Unit tests for Phase 3 feasibility check logic and security hardening."""

import os
import sys
from pathlib import Path

import pytest

# Add project root to sys.path so we can import from scripts
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.phase3_feasibility_check import (
    EXPECTED_VIIRS_COLUMNS,
    PILOT_BBOX,
    parse_firms_csv,
    sanitize_url,
)


def test_sanitize_url_masks_secret_key():
    """Verify that sensitive authentication keys are never leaked in URLs or logs."""
    fake_key = "1234567890abcdef1234567890abcdef"
    raw_url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{fake_key}/VIIRS_SNPP_SP/79,21,81,23/5/2023-03-15"
    sanitized = sanitize_url(raw_url, fake_key)

    assert fake_key not in sanitized
    assert "[MAP_KEY_REDACTED]" in sanitized
    assert "VIIRS_SNPP_SP" in sanitized


def test_sanitize_url_handles_none_or_empty():
    """Verify safe behavior when key is empty or None."""
    raw_url = "https://example.com/api/test"
    assert sanitize_url(raw_url, "") == raw_url
    assert sanitize_url(raw_url, None) == raw_url


def test_parse_firms_csv_valid_content():
    """Verify parsing of valid NASA FIRMS CSV payload."""
    sample_csv = (
        "latitude,longitude,bright_ti4,scan,track,acq_date,acq_time,satellite,confidence,version,bright_ti5,frp,daynight,type\n"
        "21.84,80.12,335.8,0.42,0.38,2023-03-20,0742,N,nominal,1.0,298.2,12.4,D,0\n"
        "22.15,79.85,340.1,0.40,0.37,2023-03-20,0742,N,high,1.0,301.5,18.7,D,0\n"
    )
    headers, rows, errors = parse_firms_csv(sample_csv)

    assert len(errors) == 0
    assert headers == EXPECTED_VIIRS_COLUMNS
    assert len(rows) == 2
    assert rows[0]["confidence"] == "nominal"
    assert rows[0]["type"] == "0"
    assert rows[1]["confidence"] == "high"


def test_parse_firms_csv_empty_or_header_only():
    """Verify parsing of valid empty CSV dataset (header with no rows)."""
    header_only_csv = "latitude,longitude,bright_ti4,scan,track,acq_date,acq_time,satellite,confidence,version,bright_ti5,frp,daynight,type\n"
    headers, rows, errors = parse_firms_csv(header_only_csv)

    assert len(errors) == 0
    assert headers == EXPECTED_VIIRS_COLUMNS
    assert len(rows) == 0


def test_parse_firms_csv_column_mismatch():
    """Verify detection of malformed rows with missing columns."""
    malformed_csv = (
        "latitude,longitude,bright_ti4\n"
        "21.84,80.12\n"
    )
    headers, rows, errors = parse_firms_csv(malformed_csv)

    assert len(headers) == 3
    assert len(errors) == 1
    assert "Column count mismatch" in errors[0]


def test_map_lat_lon_to_cell_boundaries_and_edges():
    """Verify coordinate mapping to discrete 0.05-degree grid cells and boundary edge handling."""
    from scripts.phase3_feasibility_check import map_lat_lon_to_cell
    import pytest

    # Exact bounding box corners
    assert map_lat_lon_to_cell(21.0, 79.0) == (0, 0)
    assert map_lat_lon_to_cell(23.0, 81.0) == (39, 39)
    assert map_lat_lon_to_cell(21.0, 81.0) == (0, 39)
    assert map_lat_lon_to_cell(23.0, 79.0) == (39, 0)

    # Quadrant central divider intersections
    # lat 22.0 is the exact dividing line: row 20
    # lon 80.0 is the exact dividing line: col 20
    assert map_lat_lon_to_cell(22.0, 80.0) == (20, 20)
    # Just south/west of the dividing line: row 19, col 19
    assert map_lat_lon_to_cell(21.9999, 79.9999) == (19, 19)

    # Out of bounds coordinates must raise ValueError
    with pytest.raises(ValueError):
        map_lat_lon_to_cell(20.99, 80.0)
    with pytest.raises(ValueError):
        map_lat_lon_to_cell(23.01, 80.0)
    with pytest.raises(ValueError):
        map_lat_lon_to_cell(22.0, 78.99)
    with pytest.raises(ValueError):
        map_lat_lon_to_cell(22.0, 81.01)


def test_classify_cell_quadrant_partition():
    """Verify unambiguous partition of 40x40 cells into four disjoint quadrants."""
    from scripts.phase3_feasibility_check import classify_cell_quadrant

    assert classify_cell_quadrant(20, 0) == "Q1_NW"
    assert classify_cell_quadrant(39, 19) == "Q1_NW"
    assert classify_cell_quadrant(20, 20) == "Q2_NE"
    assert classify_cell_quadrant(39, 39) == "Q2_NE"
    assert classify_cell_quadrant(0, 0) == "Q3_SW"
    assert classify_cell_quadrant(19, 19) == "Q3_SW"
    assert classify_cell_quadrant(0, 20) == "Q4_SE"
    assert classify_cell_quadrant(19, 39) == "Q4_SE"


def test_is_cell_in_buffer_margins():
    """Verify buffer inclusion for 2-cell (~20 km total) and 4-cell (~40 km total) margins."""
    from scripts.phase3_feasibility_check import is_cell_in_buffer

    # Design 1: margin_cells=2 -> rows in [18, 21], cols in [18, 21]
    # Center cross:
    assert is_cell_in_buffer(19, 19, margin_cells=2) is True
    assert is_cell_in_buffer(20, 20, margin_cells=2) is True
    assert is_cell_in_buffer(18, 5, margin_cells=2) is True    # row inside lat buffer
    assert is_cell_in_buffer(5, 21, margin_cells=2) is True    # col inside lon buffer
    assert is_cell_in_buffer(10, 10, margin_cells=2) is False  # deep interior SW
    assert is_cell_in_buffer(30, 30, margin_cells=2) is False  # deep interior NE

    # Design 2: margin_cells=4 -> rows in [16, 23], cols in [16, 23]
    assert is_cell_in_buffer(16, 5, margin_cells=4) is True
    assert is_cell_in_buffer(23, 35, margin_cells=4) is True
    assert is_cell_in_buffer(15, 15, margin_cells=4) is False
    assert is_cell_in_buffer(24, 24, margin_cells=4) is False


@pytest.fixture
def synthetic_firms_rows():
    """Deterministic multi-quadrant synthetic observations with known cell mapping and buffer memberships.

    Engineered for Central India [21.0-23.0 N, 79.0-81.0 E] at 0.05-deg resolution:
    - Q1 deep: lat 22.52, lon 79.27 -> row 30, col 5
    - Q1 in 2-cell buffer: lat 22.07, lon 79.27 -> row 21, col 5
    - Q1 in 4-cell buffer: lat 22.17, lon 79.27 -> row 23, col 5
    - Q2 deep: lat 22.52, lon 80.52 -> row 30, col 30
    - Q2 in 2-cell buffer: lat 22.52, lon 80.02 -> row 30, col 20
    - Q2 in 4-cell buffer: lat 22.52, lon 80.17 -> row 30, col 23
    - Q3 deep: lat 21.27, lon 79.27 -> row 5, col 5
    - Q3 in 2-cell buffer: lat 21.97, lon 79.27 -> row 19, col 5
    - Q3 in 4-cell buffer: lat 21.82, lon 79.27 -> row 16, col 5
    - Q4 deep: lat 21.27, lon 80.52 -> row 5, col 30
    - Q4 in 2-cell buffer: lat 21.27, lon 79.97 -> row 5, col 19
    - Q4 in 4-cell buffer: lat 21.27, lon 79.82 -> row 5, col 16
    """
    return [
        # Q1 deep: 2 detections on same date (tests deduplication to 1 positive cell-day)
        {"latitude": "22.52", "longitude": "79.27", "acq_date": "2023-03-15", "type": "0", "confidence": "nominal"},
        {"latitude": "22.53", "longitude": "79.28", "acq_date": "2023-03-15", "type": "0", "confidence": "high"},
        # Q1 deep: 1 detection on different date (tests distinct positive cell-day in same cell)
        {"latitude": "22.52", "longitude": "79.27", "acq_date": "2023-03-16", "type": "0", "confidence": "nominal"},
        # Q1 in 2-cell buffer (row 21)
        {"latitude": "22.07", "longitude": "79.27", "acq_date": "2023-03-15", "type": "0", "confidence": "nominal"},
        # Q1 in 4-cell buffer (row 23)
        {"latitude": "22.17", "longitude": "79.27", "acq_date": "2023-03-15", "type": "0", "confidence": "nominal"},

        # Q2 deep
        {"latitude": "22.52", "longitude": "80.52", "acq_date": "2023-03-15", "type": "0", "confidence": "high"},
        # Q2 in 2-cell buffer (col 20)
        {"latitude": "22.52", "longitude": "80.02", "acq_date": "2023-03-15", "type": "0", "confidence": "nominal"},
        # Q2 in 4-cell buffer (col 23)
        {"latitude": "22.52", "longitude": "80.17", "acq_date": "2023-03-15", "type": "0", "confidence": "nominal"},

        # Q3 deep
        {"latitude": "21.27", "longitude": "79.27", "acq_date": "2023-03-16", "type": "0", "confidence": "nominal"},
        # Q3 in 2-cell buffer (row 19)
        {"latitude": "21.97", "longitude": "79.27", "acq_date": "2023-03-16", "type": "0", "confidence": "nominal"},
        # Q3 in 4-cell buffer (row 16)
        {"latitude": "21.82", "longitude": "79.27", "acq_date": "2023-03-16", "type": "0", "confidence": "nominal"},

        # Q4 deep
        {"latitude": "21.27", "longitude": "80.52", "acq_date": "2023-03-17", "type": "0", "confidence": "nominal"},
        # Q4 in 2-cell buffer (col 20)
        {"latitude": "21.27", "longitude": "80.02", "acq_date": "2023-03-17", "type": "0", "confidence": "nominal"},
        # Q4 in 4-cell buffer (col 23)
        {"latitude": "21.27", "longitude": "80.17", "acq_date": "2023-03-17", "type": "0", "confidence": "nominal"},
    ]


def test_spatial_partition_audit_deterministic_fixture_reconciliation(synthetic_firms_rows):
    """Verify deduplication, buffer exclusion, and reconciliation invariants strictly using synthetic data."""
    from scripts.phase3_feasibility_check import compute_spatial_partition_audit

    # 1. Total input rows is 14; with 2 co-located detections on same date, unique cell-days must equal 13
    audit_margin2 = compute_spatial_partition_audit(synthetic_firms_rows, margin_cells=2)
    assert audit_margin2["total_qualifying_records"] == 14
    assert audit_margin2["total_positive_cell_days"] == 13
    assert audit_margin2["unique_cells_count"] == 12

    # Design 1 (margin_cells=2): rows/cols 18..21 in buffer
    # Q1: 4 cell-days (1 buffer [row 21], 3 post)
    # Q2: 3 cell-days (1 buffer [col 20], 2 post)
    # Q3: 3 cell-days (1 buffer [row 19], 2 post)
    # Q4: 3 cell-days (1 buffer [col 19], 2 post)
    assert audit_margin2["pre_exclusion_counts"] == {"Q1_NW": 4, "Q2_NE": 3, "Q3_SW": 3, "Q4_SE": 3}
    assert audit_margin2["buffer_excluded_counts"] == {"Q1_NW": 1, "Q2_NE": 1, "Q3_SW": 1, "Q4_SE": 1}
    assert audit_margin2["buffer_total_excluded"] == 4
    assert audit_margin2["post_exclusion_counts"] == {"Q1_NW": 3, "Q2_NE": 2, "Q3_SW": 2, "Q4_SE": 2}
    assert audit_margin2["post_exclusion_total"] == 9
    assert audit_margin2["reconciles"] is True
    assert audit_margin2["has_cross_fold_overlap"] is False

    # Design 2 (margin_cells=4): rows/cols 16..23 in buffer
    # Q1: 4 cell-days (2 buffer [rows 21, 23], 2 post)
    # Q2: 3 cell-days (2 buffer [cols 20, 23], 1 post)
    # Q3: 3 cell-days (2 buffer [rows 19, 16], 1 post)
    # Q4: 3 cell-days (2 buffer [cols 19, 16], 1 post)
    audit_margin4 = compute_spatial_partition_audit(synthetic_firms_rows, margin_cells=4)
    assert audit_margin4["total_positive_cell_days"] == 13
    assert audit_margin4["unique_cells_count"] == 12
    assert audit_margin4["pre_exclusion_counts"] == {"Q1_NW": 4, "Q2_NE": 3, "Q3_SW": 3, "Q4_SE": 3}
    assert audit_margin4["buffer_excluded_counts"] == {"Q1_NW": 2, "Q2_NE": 2, "Q3_SW": 2, "Q4_SE": 2}
    assert audit_margin4["buffer_total_excluded"] == 8
    assert audit_margin4["post_exclusion_counts"] == {"Q1_NW": 2, "Q2_NE": 1, "Q3_SW": 1, "Q4_SE": 1}
    assert audit_margin4["post_exclusion_total"] == 5
    assert audit_margin4["reconciles"] is True
    assert audit_margin4["has_cross_fold_overlap"] is False


def test_spatial_partition_audit_empty_qualifying_rows():
    """Verify safe behavior when qualifying records list is empty."""
    from scripts.phase3_feasibility_check import compute_spatial_partition_audit

    audit = compute_spatial_partition_audit([], margin_cells=2)
    assert audit["total_qualifying_records"] == 0
    assert audit["total_positive_cell_days"] == 0
    assert audit["unique_cells_count"] == 0
    assert audit["post_exclusion_total"] == 0
    assert audit["buffer_total_excluded"] == 0
    assert audit["reconciles"] is True
    assert audit["has_cross_fold_overlap"] is False


@pytest.mark.integration
def test_spatial_partition_audit_authenticated_reproduction():
    """Explicit live NASA FIRMS integration verification.

    Must never run implicitly during default unit tests.
    Requires explicit invocation with RUN_LIVE_FIRMS_TESTS=1 and a configured FIRMS_MAP_KEY.
    """
    import os
    if os.getenv("RUN_LIVE_FIRMS_TESTS") != "1":
        pytest.skip(
            "Live NASA FIRMS integration test deselected by default. "
            "To execute explicitly, run: RUN_LIVE_FIRMS_TESTS=1 pytest backend/tests -m integration"
        )

    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    key = os.getenv("FIRMS_MAP_KEY")
    if not key:
        pytest.skip("FIRMS_MAP_KEY not configured in environment")

    import httpx
    from scripts.phase3_feasibility_check import (
        PILOT_BBOX,
        compute_spatial_partition_audit,
        parse_firms_csv,
    )

    client = httpx.Client(timeout=25.0)
    bbox_str = f"{PILOT_BBOX['west']},{PILOT_BBOX['south']},{PILOT_BBOX['east']},{PILOT_BBOX['north']}"
    partitions = [
        ("2023-03-15", 5),
        ("2023-03-20", 5),
        ("2023-03-25", 4),
    ]
    all_rows = []
    for anchor, d_range in partitions:
        url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{key}/VIIRS_SNPP_SP/{bbox_str}/{d_range}/{anchor}"
        res = client.get(url)
        assert res.status_code == 200
        _, rows, _ = parse_firms_csv(res.text)
        all_rows.extend(rows)

    assert len(all_rows) == 349
    qualifying_rows = [
        r for r in all_rows
        if int(r.get("type", -1)) == 0 and r.get("confidence", "").lower() in ("nominal", "high", "n", "h")
    ]
    assert len(qualifying_rows) == 225

    # Design 1 (2-cell margin each side; ~20 km total buffer width across boundary)
    audit1 = compute_spatial_partition_audit(qualifying_rows, margin_cells=2)
    assert audit1["total_positive_cell_days"] == 173
    assert audit1["unique_cells_count"] == 137
    assert audit1["pre_exclusion_counts"] == {"Q1_NW": 57, "Q2_NE": 26, "Q3_SW": 53, "Q4_SE": 37}
    assert audit1["buffer_excluded_counts"] == {"Q1_NW": 11, "Q2_NE": 3, "Q3_SW": 5, "Q4_SE": 2}
    assert audit1["buffer_total_excluded"] == 21
    assert audit1["post_exclusion_counts"] == {"Q1_NW": 46, "Q2_NE": 23, "Q3_SW": 48, "Q4_SE": 35}
    assert audit1["post_exclusion_total"] == 152
    assert audit1["reconciles"] is True
    assert audit1["has_cross_fold_overlap"] is False

    # Design 2 (4-cell margin each side; ~40 km total buffer width; 20 km each side)
    audit2 = compute_spatial_partition_audit(qualifying_rows, margin_cells=4)
    assert audit2["total_positive_cell_days"] == 173
    assert audit2["unique_cells_count"] == 137
    assert audit2["pre_exclusion_counts"] == {"Q1_NW": 57, "Q2_NE": 26, "Q3_SW": 53, "Q4_SE": 37}
    assert audit2["buffer_excluded_counts"] == {"Q1_NW": 13, "Q2_NE": 16, "Q3_SW": 14, "Q4_SE": 6}
    assert audit2["buffer_total_excluded"] == 49
    assert audit2["post_exclusion_counts"] == {"Q1_NW": 44, "Q2_NE": 10, "Q3_SW": 39, "Q4_SE": 31}
    assert audit2["post_exclusion_total"] == 124
    assert audit2["reconciles"] is True
    assert audit2["has_cross_fold_overlap"] is False
