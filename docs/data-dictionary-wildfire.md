# Data Dictionary: Retrospective Next-Day Wildfire Occurrence Classification

**Hazard Identifier:** `wildfire`
**Analytical Task:** Retrospective Next-Day Fire-Occurrence Classification
**Target Variable:** $Y_{s,t} \in \{0, 1\}$ (Binary indicator of satellite-detectable active vegetation fire occurrence)
**Governance State:** `Researching` / `Candidate Source, not fully verified` (Feasibility experiment pending)
**Academic Review State:** `PENDING_SUPERVISOR_REVIEW` (Evaluation partitioning and bounding box)

---

## 1. Task Definition & Analytical Framing

The wildfire module addresses **retrospective next-day fire-occurrence classification**. Given observable meteorological, topographic, and prior fire activity in a spatial grid cell $s$ up to calendar date $t-1$, the system predicts the probability that at least one satellite-detectable active vegetation fire will be detected in cell $s$ on calendar date $t$.

This task is strictly distinct from:
1. **Static Wildfire Susceptibility Mapping:** Static susceptibility models describe multi-year topographic and fuel vulnerability without dynamic meteorological inputs or specific forecast horizons.
2. **Real-Time Active Fire Detection / Mapping:** Active fire detection reports thermal anomalies occurring at sensor acquisition time ($t$), whereas this task performs a 24-hour prospective/next-day classification using historical antecedent conditions ($t-1$ to $t-7$).
3. **Operational Numerical Fire Weather Forecasting:** This model does not run coupled atmospheric-fire spread physics, but trains statistical and machine learning classifiers on historical reanalysis and earth observation records.

---

## 2. Target Variable Specification ($Y_{s,t}$)

### 2.1 Formal Definition
$$
Y_{s,t} = \begin{cases}
1, & \text{if } \ge 1 \text{ valid active vegetation fire hotspot is detected in cell } s \text{ on date } t \\
0, & \text{otherwise (unconfirmed negative)}
\end{cases}
$$

### 2.2 Ground-Truth Source & Extraction Pipeline
* **Source Product:** NASA FIRMS VIIRS 375m NRT / Archive Active Fire Products (`VNP14IMGTDL` from Suomi NPP and `VJ114IMGTDL` from NOAA-20).
* **Observation Instrument:** Visible Infrared Imaging Radiometer Suite (VIIRS), I-Bands (375 m nominal resolution at nadir).
* **Mandatory Label Filtering:**
  - `type == 0`: Presumed vegetation fire. Explicitly excludes `1` (active volcano), `2` (other static land source / industrial flare), and `3` (offshore detection).
  - `confidence IN ('nominal', 'high', 'n', 'h')`: Rejects `'low'` (`'l'`) confidence detections to minimize false-positive contamination from solar glint, sensor noise, or marginal heat signatures.
  - **Categorical Confidence Field:** NASA VIIRS products report confidence as categorical strings (`'low'`, `'nominal'`, `'high'` or single-character abbreviations `'l'`, `'n'`, `'h'` in Area API CSV responses). Numeric percentages ($0\text{--}100\%$) exist only in legacy MODIS (`MOD14`/`MYD14`) data and must not be queried or assumed for VIIRS records.

### 2.3 Label Uncertainty & Unconfirmed Negative Label Semantics
In earth observation-based fire modeling, $Y_{s,t} = 0$ indicates **the absence of satellite detection**, which is an **unconfirmed negative**, not definitive proof that no combustion occurred:
1. **Temporal / Diurnal Sampling Gaps:** VIIRS operates aboard polar-orbiting satellites with approximately two overpasses per satellite per 24-hour cycle (~13:30 local solar time ascending, ~01:30 descending). Fires that ignite, burn, and self-extinguish between orbital passes are unobserved.
2. **Cloud and Smoke Obscuration:** Dense cloud decks, convective storms, or heavy smoke plumes attenuate middle- and thermal-infrared radiation ($3.75\,\mu\text{m}$ / $11.45\,\mu\text{m}$), causing missed detections during active burning.
3. **Sub-Canopy Masking:** Low-intensity smoldering or surface fires beneath dense forest canopies may produce insufficient thermal contrast at the top of the atmosphere to trigger detection thresholds.
4. **Modeling Implication:** The target represents *satellite-detectable active vegetation fire occurrence*. Downstream evaluation must acknowledge label asymmetry (positive detections are high-confidence evidence of fire, but zero detections combine genuine non-burning with unobserved fire events).

### 2.4 Aggregation: Raw Hotspot Detections vs. Binary Grid-Cell Labels
A critical scientific distinction exists between raw satellite hotspot detection records and analytical unit labels ($Y_{s,t}$):
- Multiple VIIRS 375m pixels can detect the same contiguous fire front inside a single $0.05^\circ \times 0.05^\circ$ (~5.5 km) grid cell on the same day.
- **Empirical Mapping:** In the March 15–28, 2023 pilot audit, 225 qualifying vegetation fire records mapped to exactly **173 unique positive cell-days** ($Y_{s,t} = 1$) across **137 unique grid cells** (clustering ratio: 1.30 detections per positive cell-day).
- Across the $1,600 \times 14 = 22,400$ total space-time cells in the pilot window, the empirical positive prevalence is $\frac{173}{22,400} \approx \mathbf{0.77\%}$, demonstrating acute class imbalance even during peak fire season.
- Therefore, raw detection counts must **never be conflated with independent positive training samples**.

---

## 3. Spatial and Temporal Discretization

### 3.1 Common Analysis Grid ($0.05^\circ \times 0.05^\circ$)
* **Coordinate Reference System (CRS):** EPSG:4326 (WGS 84 latitude/longitude).
* **Grid Spacing:** $0.05^\circ \times 0.05^\circ$ (approximately $5.5\,\text{km} \times 5.5\,\text{km}$ at the equator; ~5.2 km in Central India).
* **Bounding Box (Pilot Extent):**
  - Minimum Latitude: $21.0^\circ\text{N}$
  - Maximum Latitude: $23.0^\circ\text{N}$
  - Minimum Longitude: $79.0^\circ\text{E}$
  - Maximum Longitude: $81.0^\circ\text{E}$
  - Total Spatial Cells: $40 \times 40 = 1,600$ cells.
  - Footprint: Spans portions of Madhya Pradesh, Maharashtra, and Chhattisgarh, encompassing dry deciduous forest, agricultural tracts, and protected forest reserves.

### 3.2 Resolution Alignment and Downscaling Justification
The spatial inputs possess heterogeneous native resolutions that are harmonized onto the $0.05^\circ$ analysis grid:
1. **VIIRS Hotspots (~375 m):** Point coordinates are spatially aggregated into $0.05^\circ$ cell boundaries. Each $0.05^\circ$ cell contains approximately 150 to 200 potential VIIRS pixel footprints.
2. **Copernicus DEM GLO-30 (~30 m):** Elevation rasters are spatially aggregated over each $0.05^\circ$ cell to compute summary zonal statistics (mean elevation, mean slope, roughness standard deviation).
3. **ERA5-Land Atmospheric Reanalysis ($0.1^\circ \times 0.1^\circ$):** Native reanalysis cells (~9 km) are sampled to $0.05^\circ$ cell centroids using 2D bilinear interpolation.
4. **Resolution Mismatch Scientific Caveat:**
   - Bilinear interpolation from $0.1^\circ$ to $0.05^\circ$ is **strictly a geometric resampling convenience** to match the common analytical grid.
   - **Interpolation does not increase native atmospheric resolution.** It does not resolve microclimatic wind channeling, valley cold pools, localized convective downdrafts, or fine topographic temperature gradients.
   - The effective meteorological information content remains at the ~9–10 km mesoscale. The $0.05^\circ$ grid is selected because it balances fire ignition localization with regional weather coherence while maintaining a manageable tabular dataset volume.

---

## 4. Input Feature Dictionary

All dynamic predictors use strictly antecedent observation windows ($t-1$ or trailing multi-day windows) to guarantee temporal causality.

| Feature Identifier | Description | Source Dataset | Native Resolution | Aggregation Method | Physical Units | Valid Range | Missing Data Policy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `t2m_max_d1` | Daily maximum 2m air temperature on day $t-1$ | ERA5-Land (DS-05) | $0.1^\circ$, hourly | Bilinear interpolation to centroid; $\max_{h \in [0,23]}(T)$ | $^\circ\text{C}$ | $[-10, 55]$ | Linear interpolation if gap $\le 3\text{h}$; cell dropped if missing $>5\%$ |
| `t2m_mean_d1` | Daily mean 2m air temperature on day $t-1$ | ERA5-Land (DS-05) | $0.1^\circ$, hourly | Bilinear interpolation to centroid; $\text{mean}_{h}(T)$ | $^\circ\text{C}$ | $[-10, 50]$ | Same as above |
| `rh2m_min_d1` | Daily minimum 2m relative humidity on day $t-1$ | ERA5-Land (DS-05) | $0.1^\circ$, hourly | Derived from $T$ and $T_{\text{dew}}$; $\min_{h}(\text{RH})$ | $\%$ | $[0, 100]$ | Derived from valid temperature/dewpoint pairs |
| `rh2m_mean_d1` | Daily mean 2m relative humidity on day $t-1$ | ERA5-Land (DS-05) | $0.1^\circ$, hourly | Derived from $T$ and $T_{\text{dew}}$; $\text{mean}_{h}(\text{RH})$ | $\%$ | $[0, 100]$ | Derived from valid temperature/dewpoint pairs |
| `wind_speed_10m_max_d1` | Daily maximum 10m wind speed on day $t-1$ | ERA5-Land (DS-05) | $0.1^\circ$, hourly | $\max_{h} \sqrt{u_{10}^2 + v_{10}^2}$ | $\text{m/s}$ | $[0, 50]$ | Linear interpolation if gap $\le 3\text{h}$ |
| `wind_speed_10m_mean_d1`| Daily mean 10m wind speed on day $t-1$ | ERA5-Land (DS-05) | $0.1^\circ$, hourly | $\text{mean}_{h} \sqrt{u_{10}^2 + v_{10}^2}$ | $\text{m/s}$ | $[0, 40]$ | Linear interpolation if gap $\le 3\text{h}$ |
| `precip_sum_d1` | Total precipitation accumulation on day $t-1$ | ERA5-Land (DS-05) | $0.1^\circ$, hourly | $\sum_{h=0}^{23} P_h$ | $\text{mm}$ | $[0, 500]$ | Sum of hourly increments; zero-fill if null flag absent |
| `precip_sum_7d` | Cumulative precipitation accumulation across days $t-7$ to $t-1$ | ERA5-Land (DS-05) | $0.1^\circ$, daily | $\sum_{d=1}^{7} \text{precip\_sum\_d}d$ | $\text{mm}$ | $[0, 1500]$ | Requires $\ge 6$ valid antecedent days |
| `surface_pressure_mean_d1` | Daily mean surface atmospheric pressure on day $t-1$ | ERA5-Land (DS-05) | $0.1^\circ$, hourly | $\text{mean}_{h}(P_{\text{sfc}})$ | $\text{hPa}$ | $[800, 1050]$ | Linear interpolation if gap $\le 3\text{h}$ |
| `elevation_mean` | Zonal mean ground surface elevation | Copernicus DEM (DS-04) | 30 m raster | Zonal mean within $0.05^\circ$ cell polygon | $\text{m}$ (EGM2008) | $[-100, 8848]$ | Nearest-neighbor raster interpolation across NoData voids |
| `slope_mean` | Zonal mean surface terrain slope angle | Copernicus DEM (DS-04) | 30 m raster | Horn's algorithm on 30m grid, then zonal mean | Degrees | $[0, 90]$ | Derived from valid elevation cells |
| `roughness_std` | Terrain ruggedness / elevation standard deviation | Copernicus DEM (DS-04) | 30 m raster | Zonal standard deviation $\sigma_z$ within cell | $\text{m}$ | $[0, 2000]$ | Requires $\ge 80\%$ valid raster pixels in cell |
| `fire_count_lag1` | Count of detected active fires in cell $s$ on day $t-1$ | NASA FIRMS (DS-01) | Point vector | Spatial point-in-polygon count with label filters | Integer count | $[0, \infty)$ | Zero-filled if no FIRMS record matches cell and date |
| `fire_count_7d` | Total detected active fires in cell $s$ over days $t-7$ to $t-1$ | NASA FIRMS (DS-01) | Point vector | Cumulative sum of filtered fire counts | Integer count | $[0, \infty)$ | Zero-filled if no FIRMS records match |

---

## 5. Evaluation Partitioning & Spatial Independence

### 5.1 Temporal Splitting Protocol
To respect the temporal arrow of time and evaluate generalization to future fire seasons:
* **Training & Validation Window:** Calendar years 2020 through 2022 (36 months).
* **Prospective Holdout Test Window:** Calendar year 2023 (12 months).
* **Purging / Guard Band:** A 7-day purging window is enforced immediately prior to January 1, 2023, preventing rolling 7-day antecedent weather aggregates from leaking information across the split boundary.

### 5.2 Spatial Block Holdout & Evaluation Reassessment (Phase 3.3.1 Corrected Audit)
* **Proposed Design:** The $2^\circ \times 2^\circ$ region ($40 \times 40$ cells) is divided into four geographic quadrants along the central axes ($\text{lat} = 22.0^\circ\text{N}$, $\text{lon} = 80.0^\circ\text{E}$):
  - Quadrant 1 (North-West): $[22.0^\circ\text{--}23.0^\circ\text{N}, 79.0^\circ\text{--}80.0^\circ\text{E}]$ ($20 \times 20 = 400$ cells; rows $20\dots 39$, cols $0\dots 19$)
  - Quadrant 2 (North-East): $[22.0^\circ\text{--}23.0^\circ\text{N}, 80.0^\circ\text{--}81.0^\circ\text{E}]$ ($400$ cells; rows $20\dots 39$, cols $20\dots 39$)
  - Quadrant 3 (South-West): $[21.0^\circ\text{--}22.0^\circ\text{N}, 79.0^\circ\text{--}80.0^\circ\text{E}]$ ($400$ cells; rows $0\dots 19$, cols $0\dots 19$)
  - Quadrant 4 (South-East): $[21.0^\circ\text{--}22.0^\circ\text{N}, 80.0^\circ\text{--}81.0^\circ\text{E}]$ ($400$ cells; rows $0\dots 19$, cols $20\dots 39$)
* **Distance Disambiguation & Metric Approximation:**
  - At $22.0^\circ\text{N}$, $1^\circ \text{ lat} \approx 110.74\,\text{km} \implies 0.05^\circ \approx 5.537\,\text{km}$; $1^\circ \text{ lon} \approx 103.22\,\text{km} \implies 0.05^\circ \approx 5.161\,\text{km}$.
  - **Design 1 (~20 km Total Buffer Width across boundary):** 2 grid cells on each side of the dividing axes ($\pm 2$ rows/cols; rows $18\dots 21$, cols $18\dots 21$). The exclusion band is 4 cells wide ($\approx 22.15\,\text{km}$ lat $\times 20.64\,\text{km}$ lon total width across the boundary).
  - **Design 2 (20 km Margin on Each Side / ~40 km Total Width):** 4 grid cells on each side of the dividing axes ($\pm 4$ rows/cols; rows $16\dots 23$, cols $16\dots 23$). The exclusion band is 8 cells wide ($\approx 44.30\,\text{km}$ lat $\times 41.28\,\text{km}$ lon total width across the boundary).
* **Empirical Reconciliation Audit (March 15–28, 2023):**
  - **Pre-Exclusion Positive Cell-Days ($Y_{s,t} = 1$):** Q1 (NW): 57, Q2 (NE): 26, Q3 (SW): 53, Q4 (SE): 37 (Total = **173** unique cell-days across 137 unique cells).
  - **Design 1 (2-cell margin / ~20 km total band):**
    - Inside buffer (excised): Q1: 11, Q2: 3, Q3: 5, Q4: 2 (Total = **21** positive cell-days excised).
    - Remaining post-exclusion evaluation counts: Q1: **46**, Q2: **23**, Q3: **48**, Q4: **35** (Total = **152** positive cell-days).
    - Strict reconciliation: $152 + 21 = 173$; zero cross-fold spatial overlap.
  - **Design 2 (4-cell margin / 20 km each side / ~40 km total band):**
    - Inside buffer (excised): Q1: 13, Q2: 16, Q3: 14, Q4: 6 (Total = **49** positive cell-days excised).
    - Remaining post-exclusion evaluation counts: Q1: **44**, Q2: **10**, Q3: **39**, Q4: **31** (Total = **124** positive cell-days).
    - Strict reconciliation: $124 + 49 = 173$; zero cross-fold spatial overlap.
* **Scientific Consequence & Evaluation Reassessment:**
  - Under Design 2, excising a 20 km margin on each side leaves **only 10 positive cell-days in Quadrant 2**, rendering holdout PR-AUC evaluation statistically unstable on this 14-day sample.
  - The 14-day window proves **data access and ingestion protocol feasibility**, but is **statistically insufficient for machine learning spatial cross-validation**.
  - **Provisional Status:** The 4-block spatial holdout with buffer exclusion remains strictly **provisional** (`PENDING_SUPERVISOR_REVIEW` under SUP-08).
  - **Recommended Design:** Multi-year temporal aggregation (2020–2022 train, 2023 prospective test) combined with ecoregion-based spatial clustering or purged temporal block cross-validation.

---

## 6. Pilot Engineering Quality Thresholds

The following numerical thresholds are **pilot engineering bounding criteria** designed to ensure reproducible, lightweight local execution on consumer hardware, and must not be cited as universal scientific or meteorological standards:
1. **Pilot Storage Cap ($\le 30\,\text{MB}$):** Governs the maximum uncompressed tabular feature matrix for the pilot region over the study period to ensure smooth local in-memory processing without specialized database infrastructure.
2. **Missing Weather Tolerance ($\le 5\%$ per cell):** Rejects spatial cells where missing reanalysis steps exceed 5% of total time steps, ensuring robust rolling window aggregations.
3. **Pilot Geographic Extent ($2^\circ \times 2^\circ$):** Selected to span four $1^\circ \times 1^\circ$ DEM tiles while bounding network transfer and memory footprint.

---

## 7. Long-Term Mission Continuity & Sensor Lifecycle

* **Suomi-NPP Data Delivery Cessation Notice:** NASA has announced that forward operational data product delivery for the Suomi-NPP satellite is scheduled to **cease on November 1, 2026** (end of mission lifecycle).
* **Cross-Mission Sensor Compatibility:** The follow-on Joint Polar Satellite System (JPSS) satellites carry identical VIIRS instruments:
  - **NOAA-20 (JPSS-1):** Active since 2017; product `VJ114IMGTDL` / `VIIRS_NOAA20_SP`.
  - **NOAA-21 (JPSS-2):** Active since 2022; product `VJ214IMGTDL` / `VIIRS_NOAA21_SP`.
* **Engineering Requirement for Operational Phase:** While historical retrospective training utilizes Suomi-NPP (2012–2024), any forward-looking operational early warning pipeline must verify cross-satellite radiometric alignment and switch to NOAA-20/21 prior to November 1, 2026.
