# RESTful API Contracts and Uncertainty Communication Specification

**Project:** Satellite-Based Multi-Hazard Disaster Risk Prediction and Early Warning System Using AI/ML
**Phase:** Phase 2 — Requirements and UX Workflow
**Document Ownership:** Authoritative technical specification for frontend-to-backend API endpoint contracts, Pydantic schemas, task-appropriate uncertainty representations, sensor-specific freshness policies, and error handling.
**Cross-References:** User stories in [requirements-and-user-stories.md](file:///Users/salman/Desktop/satellite-disaster/docs/requirements-and-user-stories.md), UI spec in [ux-workflow-and-dashboard-spec.md](file:///Users/salman/Desktop/satellite-disaster/docs/ux-workflow-and-dashboard-spec.md), Alert taxonomy in [alert-and-severity-taxonomy.md](file:///Users/salman/Desktop/satellite-disaster/docs/alert-and-severity-taxonomy.md).

---

## 1. General API Architectural Conventions

* **Base URL Prefix:** `/api/v1`
* **Data Interchange Format:** JSON (`application/json`) with standard GeoJSON RFC 7946 for geographic feature geometries.
* **Timestamp Standard:** Strict ISO 8601 UTC with explicit `Z` suffix (`YYYY-MM-DDTHH:MM:SSZ`).
* **Coordinate Ordering:** Standard GeoJSON longitude-first ordering (`[longitude, latitude]`).
* **Error Envelope:** All error responses follow standard structure with an explicit machine-readable `error_code`, human-readable `message`, and contextual `details`.

---

## 2. Sensor Freshness Policy by Product, Latency, and Task

Data freshness thresholds are defined by sensor orbital mechanics and processing latency. All thresholds listed below are **provisional proposals** subject to validation in Phase 3/4:

| Data Product | Sensor / Platform | Acquisition Schedule | Typical Processing Latency | Primary Hazard Task | Proposed Freshness Policy Limits |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **NRT Active Fire** | VIIRS 375m / MODIS 1km | 2–4 overpasses daily (global) | 3–6 hours (NASA LANCE/FIRMS) | `wildfire` (Hotspot Detection) | **Fresh:** $< 6\text{h}$ &bull; **Aging:** $6\text{--}24\text{h}$ &bull; **Stale:** $> 24\text{h}$ |
| **SAR GRD Backscatter**| Sentinel-1 C-SAR | 6–12 days repeat cycle | 6–24 hours (Copernicus CDSE) | `flood` (SAR Inundation Detection) | **Fresh:** $< 24\text{h}$ &bull; **Aging:** $24\text{h}\text{--}7\text{d}$ &bull; **Stale:** $> 12\text{d}$ |
| **Multispectral Optical**| Sentinel-2 Level-2A | 5 days repeat cycle | 12–36 hours (Copernicus CDSE) | `wildfire` (dNBR), `flood` (MNDWI) | **Fresh:** $< 48\text{h}$ &bull; **Aging:** $2\text{--}7\text{d}$ &bull; **Stale:** $> 14\text{d}$ |
| **Atmospheric Reanalysis**| ERA5-Land / Open-Meteo | Hourly time series | Real-time (Forecast/NWP proxy) | `wildfire` (FWI), `landslide` (Rainfall) | **Fresh:** $< 3\text{h}$ &bull; **Aging:** $3\text{--}24\text{h}$ &bull; **Stale:** $> 48\text{h}$ |
| **Vegetation Health Index**| MODIS 16-day Composite| 16-day compositing interval | 2–4 days after composite close | `drought` (Index Monitoring) | **Fresh:** $< 16\text{d}$ &bull; **Aging:** $16\text{--}32\text{d}$ &bull; **Stale:** $> 32\text{d}$ |

---

## 3. Task-Appropriate Uncertainty Communication

Uncertainty reporting is strictly conditioned on the physical nature of the analytical task:

1. **Discrete Classification & Susceptibility Tasks (`wildfire` danger tier, `landslide` susceptibility tier):**
   * Output calibrated class probabilities: $P(\text{Class} = c) \in [0, 1]$ where $\sum_c P(c) = 1.0$.
   * Where calibration cannot be proven, output non-probabilistic decision confidence scores tagged `uncalibrated_score`.
2. **Continuous Anomaly Regression Tasks (`drought` VHI/SPEI, burn severity dNBR):**
   * Output point estimate accompanied by empirical baseline deviation bounds or residual standard error ($[\hat{y} - 1.96\hat{\sigma}, \hat{y} + 1.96\hat{\sigma}]$).
3. **Observational Detection Tasks (VIIRS thermal hotspots, Sentinel-1 water masks):**
   * Output sensor detection confidence attribute (`low`, `nominal`, `high` from VIIRS) and explicit false-alarm caveat flags.
4. **Qualitative Data Quality Flags:**
   * Output metadata flags: `cloud_cover_percentage` (optical only), `sar_orbit_direction` (Ascending/Descending), and `missing_inputs_interpolated` (Boolean).

---

## 4. API Endpoint Specifications

---

### 4.1 Endpoint: `GET /api/v1/hazards`
* **Summary:** Enumerates all eight supported hazards, their metadata, task types, and lifecycle status.
* **Response (200 OK):**
```json
{
  "hazards": [
    {
      "id": "wildfire",
      "name": "Wildfire / Forest Fire",
      "task_type": "danger_forecasting_and_burn_severity",
      "status": "Planned",
      "primary_sensors": ["VIIRS 375m", "Sentinel-2 MSI", "ERA5-Land"],
      "unit_of_analysis": "500m_grid_cell",
      "scientific_safeguard": "Active hotspot detection identifies current combustion, not future ignition."
    },
    {
      "id": "flood",
      "name": "Flood",
      "task_type": "susceptibility_and_sar_inundation_detection",
      "status": "Planned",
      "primary_sensors": ["Sentinel-1 C-SAR", "Copernicus DEM", "ERA5"],
      "unit_of_analysis": "30m_raster_cell",
      "scientific_safeguard": "SAR inundation mapping detects observed surface water, not future cresting."
    }
  ]
}
```

---

### 4.2 Endpoint: `GET /api/v1/hazards/{hazard_id}/risk`
* **Query Parameters:**
  * `bbox` (string, required): Format `min_lon,min_lat,max_lon,max_lat` (e.g. `80.0,22.0,81.0,23.0`).
  * `date` (string, optional): ISO date `YYYY-MM-DD` (defaults to latest available observation).
* **Success Response (200 OK):**
```json
/* [ILLUSTRATIVE EXAMPLE ONLY — NOT REAL OBSERVATION OR PREDICTION] */
{
  "hazard_id": "wildfire",
  "bbox": [80.00, 22.00, 81.00, 23.00],
  "evaluated_at_utc": "2026-10-09T09:00:00Z",
  "data_provenance": {
    "sensor_platform": "VIIRS on Suomi-NPP / NOAA-20",
    "product_name": "VNP14IMGTDL Active Fire",
    "latest_acquisition_utc": "2026-10-09T04:15:00Z",
    "latency_hours": 4.75,
    "freshness_tier": "Fresh",
    "cloud_mask_applied": true,
    "cloud_cover_percent": 8.5
  },
  "task_classification": {
    "task_type": "fire_danger_susceptibility_forecast",
    "target_variable": "fire_danger_tier",
    "prediction_horizon_hours": 24
  },
  "assessment": {
    "synthesized_tier": "Watch",
    "uncertainty_representation": {
      "type": "calibrated_class_probabilities",
      "probabilities": {
        "Low": 0.05,
        "Moderate": 0.15,
        "High": 0.58,
        "Very_High": 0.22
      },
      "predicted_class": "High",
      "calibration_standard": "Platt Scaling evaluated on 2020-2022 holdout"
    },
    "physical_triggers": {
      "relative_humidity_percent": 18.2,
      "wind_speed_10m_kmh": 32.5,
      "fire_weather_index_proxy": 31.4
    }
  },
  "scientific_limitations": [
    "FWI proxy evaluated using gridded ERA5-Land reanalysis; microclimate wind gusts may differ.",
    "Stochastic human ignitions cannot be deterministically forecasted."
  ]
}
```

* **Degraded Error Response: Missing Data (HTTP 404):**
```json
{
  "error_code": "DATA_UNAVAILABLE",
  "message": "No valid satellite overpass or weather reanalysis found for the requested bounding box and date.",
  "hazard_id": "flood",
  "requested_bbox": [91.50, 26.00, 92.00, 26.50],
  "last_available_observation_utc": "2026-10-03T02:45:00Z",
  "suggested_action": "Select an earlier observation date or expand bounding box."
}
```

---

### 4.3 Endpoint: `GET /api/v1/alerts`
* **Query Parameters:**
  * `hazard_id` (string, optional): Filter by hazard identifier.
  * `tier` (string, optional): `Warning` | `Watch` | `Advisory`.
  * `lifecycle_state` (string, optional): `Active` | `Updated` | `Cleared` | `Expired` | `Cancelled`.
* **Success Response (200 OK):**
```json
/* [ILLUSTRATIVE EXAMPLE ONLY — NOT REAL OBSERVATION OR ALERT] */
{
  "total_alerts": 1,
  "alerts": [
    {
      "alert_id": "ALT-2026-WF-0089-SYNTHETIC",
      "hazard_id": "wildfire",
      "synthesized_tier": "Warning",
      "cap_v1_2_elements": {
        "severity": "Severe",
        "urgency": "Immediate",
        "certainty": "Observed"
      },
      "headline": "Active Wildfire Hotspot Cluster Detected by VIIRS (Illustrative Example)",
      "description": "Synthetic demonstration payload: High-confidence thermal hotspot cluster detected in Central India deciduous forest belt.",
      "triggering_variables": {
        "sensor": "VIIRS 375m",
        "fire_radiative_power_mw": 114.5,
        "detection_confidence": 92
      },
      "effective_utc": "2026-10-09T08:15:00Z",
      "expires_utc": "2026-10-09T20:15:00Z",
      "lifecycle_state": "Active",
      "geometry": {
        "type": "Point",
        "coordinates": [80.12, 22.45]
      },
      "disclaimer": "Academic capstone demonstration. This is not an official disaster warning."
    }
  ]
}
```
