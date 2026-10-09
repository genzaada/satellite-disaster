# GIS Dashboard UX Workflow and Interface Specification

**Project:** Satellite-Based Multi-Hazard Disaster Risk Prediction and Early Warning System Using AI/ML
**Phase:** Phase 2 — Requirements and UX Workflow
**Document Ownership:** Authoritative technical specification for the interactive GIS dashboard layout, map controls, raster visualization rules, UI state machine, and accessibility requirements.
**Cross-References:** Requirements in [requirements-and-user-stories.md](file:///Users/salman/Desktop/satellite-disaster/docs/requirements-and-user-stories.md), Alert Taxonomy in [alert-and-severity-taxonomy.md](file:///Users/salman/Desktop/satellite-disaster/docs/alert-and-severity-taxonomy.md), API Contracts in [api-contracts-spec.md](file:///Users/salman/Desktop/satellite-disaster/docs/api-contracts-spec.md).

---

## 1. Information Architecture & Layout Wireframe

The GIS dashboard provides a unified, responsive single-page web interface structured into three primary functional columns on desktop displays, collapsing to accessible drawer tabs on mobile devices:

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [Logo] Satellite Multi-Hazard Early Warning System   [API: Online]  [Region: Central India Pilot v]   │
├──────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ [ALERT BANNER: Experimental Academic Research System &bull; Does Not Replace Official National Warnings] │
├──────────────────────────────┬──────────────────────────────────────────┬────────────────────────────┤
│ 1. HAZARD CONTROLS (Col 1)   │ 2. INTERACTIVE GIS MAP CANVAS (Col 2)    │ 3. RISK INSPECTOR (Col 3)  │
│                              │                                          │                            │
│ IN-SCOPE HAZARDS (Single-Sel)│ ┌──────────────────────────────────────┐ │ [ILLUSTRATIVE EXAMPLE ONLY]│
│ (o) Wildfire (`wildfire`)    │ │ Coordinate Reference: EPSG:4326      │ │ Cell: Lat 22.45, Lon 80.12 │
│ ( ) Flood (`flood`)          │ │ Active Layer: Fire Danger Forecast   │ │ Hazard: Wildfire           │
│ ( ) Landslide (`landslide`)  │ │ Overpass: VIIRS 375m & ERA5-Land     │ │ Task: Fire Danger Forecast │
│ ( ) Drought (`drought`)      │ │ Freshness: 4.5h ago (Nominal)        │ │ Synthesized Tier: WATCH    │
│ ( ) Cyclone (`cyclone`)      │ │                                      │ │ Trigger: Wind 32 km/h,     │
│ ( ) Severe Storm (`...`)     │ │ [Raster Map Visualization Canvas]    │ │          RH 18%, FWI 34    │
│ ( ) Volcano (`...`)          │ │                                      │ │ Platform: VIIRS + ERA5     │
│ ( ) Avalanche (`...`)        │ │ Legend: [Low] [Mod] [High] [Extr]    │ │ Overpass: 2026-10-09 08:30 │
│                              │ └──────────────────────────────────────┘ │ Uncertainty: Class Prob    │
│ PILOT BOUNDING BOX           │ Timeline: [-24h] [Now] [+24h] [+48h]     │ P(High)=0.78 (Calibrated)  │
│ Bounding: 20.0N, 78.0E...    │ Opacity Slider: [ ───●────── 80% ]       │ Limitation: Stochastic     │
│                              │ Base Layer: [Dark Vector] [Satellite]    │ human ignitions unmodeled  │
├──────────────────────────────┴──────────────────────────────────────────┴────────────────────────────┤
│ 4. ACTIVE ALERTS LEDGER (Bottom Drawer / Collapsible)                                                │
│ [ILLUSTRATIVE EXAMPLE ONLY — NOT REAL ALERTS]                                                        │
│ [WATCH]   2026-10-09 08:30 UTC &bull; Wildfire: High Fire Danger Weather &bull; Central India Forest Belt        │
│ [ADVISORY] 2026-10-09 06:00 UTC &bull; Flood: Elevated Antecedent Catchment Moisture &bull; Brahmaputra Sub-Basin │
└──────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Interactive Map Controls and Visualization Specifications

### 2.1 Coordinate Reference System & Base Layers
* **Spatial Reference:** EPSG:4326 (WGS 84 geographic coordinates) for GeoJSON feature queries; EPSG:3857 (Web Mercator) for client-side raster tile display.
* **Base Map Providers:** Default high-contrast dark vector basemap (CartoDB Dark Matter / OpenStreetMap vector tiles) to prioritize colored hazard raster readability. High-resolution satellite basemap toggle (ESRI World Imagery / Sentinel-2 cloudless mosaic) for terrain orientation.

### 2.2 Map Controls
1. **Layer Opacity Controller:** Variable slider ($0\text{--}100\%$, default $80\%$) enabling simultaneous inspection of underlying transportation corridors, rivers, and topography.
2. **Timeline Slider:** Scrubbing temporal dimension:
   * Historical scenes (past 7 days in 24h increments for flood/wildfire).
   * Nowcast/Forecast steps ($0\text{h}$, $+24\text{h}$, $+48\text{h}$, $+72\text{h}$ for fire weather and storm nowcasting).
3. **Bounding Box Selector:** Preset regional dropdowns bounding pilot zones (e.g. *Central India Forest Pilot*, *Brahmaputra Floodplain Pilot*) alongside interactive polygon bounding box drawer.

### 2.3 Legends and Symbology Standards
* **Continuous Anomaly Indices (Drought VHI, Vegetation Anomaly):** ColorBrewer Viridis or RdYlBu color ramp with continuous gradient bar and labeled numerical break points.
* **Discrete Hazard Masks (Flood SAR Inundation):** Discrete solid fill: Dark Blue (`#1d4ed8`, Permanent Surface Water) vs. Vivid Cyan (`#06b6d4`, Transient Flood Inundation).
* **Severity Alerts:** Standardized CAP-aligned color tokens:
  * Warning: Vivid Red (`#ef4444`) with exclamation triangle symbol.
  * Watch: Amber/Orange (`#f97316`) with alert diamond symbol.
  * Advisory: Yellow (`#eab308`) with information circle symbol.

---

## 3. Sensor-Specific Quality and Cloud Obscuration Handling

### 3.1 Differentiated Cloud Obscuration Rules
The UI strictly isolates optical cloud limitations from Synthetic Aperture Radar (SAR) characteristics:

1. **Optical / Multispectral Products (Sentinel-2, Landsat-8, MODIS optical):**
   * Clouds directly obstruct optical reflectance.
   * Pixels flagged with cloud/shadow mask $> 20\%$ are rendered with a dynamic semi-transparent hatched pattern (`stroke: #94a3b8; stroke-dasharray: 4, 4; opacity: 0.5`).
   * Tooltip notice: `Data Quality: Degraded (Optical Cloud Obscuration) — Ground surface invisible.`
2. **Microwave SAR Products (Sentinel-1 C-band SAR):**
   * C-band microwave pulses penetrate meteorological clouds, fog, and rain. Optical cloud masks are **strictly suppressed** on SAR layers.
   * Radar-specific caveats are displayed in the Inspector:
     * `Urban Caveat: Radar double-bounce and radar shadow artifacts possible in urban built environments.`
     * `Canopy Caveat: C-band radar cannot detect standing water beneath dense closed forest canopies.`

---

## 4. Degraded Real-World UI States

The dashboard accommodates imperfect real-world Earth observation availability via dedicated state handlers:

| State Code | Trigger Condition | Visual UI Behavior | User-Facing Guidance |
| :--- | :--- | :--- | :--- |
| **`LOADING`** | Network request in flight. | Map canvas displays subtle glowing pulse; Inspector shows skeleton placeholders (`aria-busy="true"`). | "Fetching satellite raster granules..." |
| **`DATA_UNAVAILABLE`** | No satellite overpass or environmental data in requested temporal/spatial window (HTTP 404 / 503). | Map canvas clears active raster; renders center informational card with satellite icon. | "No valid satellite acquisitions found for the selected bounding box and date. Try selecting an earlier date or alternative pilot region." |
| **`DATA_STALE`** | Observation latency exceeds sensor revisit threshold ($> 24\text{h}$ for thermal fire, $> 12\text{d}$ for SAR flood). | Top-right status chip changes from Green to Amber; warning banner appears above map. | "Data Stale: Latest satellite overpass is 74 hours old. Displaying historical state." |
| **`COVERAGE_PARTIAL`** | Satellite orbital swath intersects only a subset of the selected bounding box. | Uncovered portion rendered with neutral diagonal hatching; clear legend boundary indicator. | "Partial Satellite Swath: Sensor acquisition covers 64% of the selected region." |
| **`REGION_UNSUPPORTED`** | User pans/zooms outside calibrated pilot boundaries (e.g. into open ocean). | Boundary fence overlay with button: `[Snap to Calibrated Pilot Zone]`. | "Analytical models are uncalibrated for this geographic area. Please select a designated pilot basin." |

---

## 5. Accessibility and Responsive Design Standards (WCAG 2.1 AA)

1. **Color-Blind Safe Palette:** Alert tiers and risk layers use dual encoding: every color hue is paired with a distinct geometric icon (Triangle for Warning, Diamond for Watch, Circle for Advisory).
2. **Contrast Ratio:** Text and icon elements maintain a minimum contrast ratio of $4.5:1$ against dark background surfaces (`bg-slate-950`, `bg-slate-900`).
3. **Keyboard Navigation:** All interactive layer toggles, opacity sliders, and alert list items support full keyboard traversal (`Tab`, `Enter`, `Space`, `Arrow Keys`) with visible focus rings (`ring-2 ring-sky-400`).
4. **Semantic HTML & ARIA:** All regions use landmark elements (`<header>`, `<main>`, `<aside>`, `<footer>`, `<section aria-labelledby="...">`) with live region notifications (`aria-live="polite"`) for incoming alerts.
