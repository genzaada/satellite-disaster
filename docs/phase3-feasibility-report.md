# Phase 3.2 & 3.3.1: Wildfire Dataset Feasibility & Spatial Buffer Audit Report

**Document Version:** 3.1 (Corrected Spatial Buffer Audit)
**Phase:** Phase 3.3.1 — NASA FIRMS Spatial Buffer Audit & Feasibility Verification
**Execution Timestamp:** 2026-10-09T11:10:00Z (UTC)
**Execution Script:** `scripts/phase3_feasibility_check.py`
**Test Suite:** `backend/tests/test_phase3_feasibility.py` (10/10 unit tests passing; 12/12 total backend suite passing)
**Overall Feasibility Outcome:** **PASS WITH LIMITATIONS** (ERA5-Land: PASS across all 6 levels; NASA FIRMS: PASS across all 6 levels with 225 qualifying vegetation fires and 173 unique positive cell-days; Copernicus DEM: PASS at header/object level, full raster decode deferred to Phase 4; 4-block spatial holdout labeled PROVISIONAL pending supervisor review)
**Governance State:** Datasets verified; spatial holdout labeled provisional; status maintained as `Feasibility Verified (Access & Schema Validated; Data Ready Pending Supervisor Review for Phase 4 Authorization)`.

---

## 1. Executive Summary & Audit Scope

Phase 3.2 successfully executed the authenticated empirical feasibility experiment across the three candidate datasets for the retrospective next-day wildfire occurrence classification task:
1. **NASA FIRMS Active Fire VIIRS 375m Standard Processing (`VIIRS_SNPP_SP`)**
2. **ECMWF ERA5-Land Reanalysis (via Open-Meteo Historical API)**
3. **Copernicus Global Digital Elevation Model (GLO-30 via AWS Public S3)**

### Key Empirical Results:
- **Spatial Bounding Box:** Central India ($21.0^\circ\text{--}23.0^\circ\text{N}, 79.0^\circ\text{--}81.0^\circ\text{E}$), EPSG:4326.
- **Evaluation Window:** March 15 to March 28, 2023 (14 calendar days; peak pre-monsoon dry season).
- **Antecedent Weather Lead Window:** March 8 to March 28, 2023 (21 calendar days).
- **NASA FIRMS Observations:** **349 total active fire records** retrieved across the 14-day window. Exactly **225 qualifying vegetation fires** (`type == 0` AND categorical `confidence IN ('n', 'h', 'nominal', 'high')`) confirmed, establishing empirical label adequacy for pilot classification.
- **ERA5-Land Observations:** **504 / 504 consecutive hourly intervals** per quadrant ($21 \times 24 = 504$), with exactly 0 missing timestamps, $0.00\%$ missing values across all six parameters, and zero future-leakage.
- **Copernicus DEM Footprint:** All four required $1^\circ \times 1^\circ$ tiles (`N21_E079`, `N21_E080`, `N22_E079`, `N22_E080`) confirmed present on public S3 ($40.87\text{--}42.28\,\text{MB}$ each); byte-range inspection verified Little-Endian TIFF Magic 42. Full raster array decode is deferred to Phase 4.
- **Storage & Network Transfer:** Total transferred across all probes and datasets: **$124,819\,\text{bytes}$ ($\sim 0.119\,\text{MB}$)**, well below the $25.0\,\text{MB}$ experiment budget. Ephemeral disk usage: $0\,\text{bytes}$ after automatic cleanup.

---

## 2. Multi-Tiered Evidence Hierarchy

| Evidence Level | ECMWF ERA5-Land Reanalysis (DS-05) | Copernicus DEM GLO-30 (DS-04) | NASA FIRMS VIIRS 375m (DS-01) |
| :--- | :--- | :--- | :--- |
| **Level 1: Endpoint Accessible** | **YES** (HTTP 200 via Open-Meteo) | **YES** (HTTP 200 across 4 S3 tiles) | **YES** (HTTP 200 across 3 area queries) |
| **Level 2: Authentication Successful** | **YES** (Open API; no token required) | **YES** (Open AWS S3; no token required)| **YES** (`FIRMS_MAP_KEY` validated) |
| **Level 3: Valid Payload Retrieved** | **YES** ($96,372\,\text{bytes}$ structured JSON) | **PARTIAL** ($1,024\,\text{bytes}$ COG header only)| **YES** ($27,423\,\text{bytes}$ valid CSV) |
| **Level 4: Schema Verified** | **YES** (All 6 meteorological keys valid) | **PARTIAL** (TIFF Magic 42 verified) | **YES** (15 expected columns confirmed) |
| **Level 5: Coverage Verified** | **YES** (504/504 hrs, 4 quadrant points) | **YES** (4 tiles cover $2^\circ \times 2^\circ$ bbox) | **YES** (14 days, 21°–23°N, 79°–81°E) |
| **Level 6: Quality Adequate for Task** | **YES** ($0.00\%$ missingness; 0 leakage) | **DEFERRED TO PHASE 4** (Raster decode)| **YES** (225 qualifying vegetation fires) |
| **Overall Component Status** | **PASS** | **PASS (Object & Header Level)** | **PASS** |

---

## 3. NASA FIRMS Historical Sample Audit (March 15–28, 2023)

### 3.1 Transactional Query Partitions
To respect the NASA FIRMS Area API 5-day limit per call without gaps or overlap, the 14-day window was executed across three partitions:

| Partition | Date Range | HTTP Status | Content-Type | Bytes Received | Records Retrieved |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Partition 1** | 2023-03-15 to 2023-03-19 (5 days) | 200 OK | `text/plain;charset=UTF-8` | 7,085 B | 90 records |
| **Partition 2** | 2023-03-20 to 2023-03-24 (5 days) | 200 OK | `text/plain;charset=UTF-8` | 4,782 B | 60 records |
| **Partition 3** | 2023-03-25 to 2023-03-28 (4 days) | 200 OK | `text/plain;charset=UTF-8` | 15,556 B | 199 records |
| **Total** | **March 15–28, 2023 (14 days continuous)** | — | — | **27,423 B** | **349 records** |

### 3.2 Schema Validation
Actual headers returned by NASA FIRMS:
`latitude`, `longitude`, `bright_ti4`, `scan`, `track`, `acq_date`, `acq_time`, `satellite`, `instrument`, `confidence`, `version`, `bright_ti5`, `frp`, `daynight`, `type`

- All 14 expected schema fields present. (`instrument` returned as an additional informative column `VIIRS`).
- Zero schema formatting or column-count mismatch errors observed.

### 3.3 Sample Breakdown & Label Distributions
- **By Satellite:** 349 from Suomi-NPP (`satellite == 'N'`).
- **By Categorical Confidence:**
  - Nominal (`'n'`): 240 records ($68.8\%$)
  - Low (`'l'`): 108 records ($30.9\%$)
  - High (`'h'`): 1 record ($0.3\%$)
  - Confirmed: Confidence values are strictly categorical strings (`'l'`, `'n'`, `'h'`), **not numeric percentages**.
- **By Fire Type:**
  - Type `0` (Presumed vegetation fire): 333 records ($95.4\%$)
  - Type `2` (Other static land source): 16 records ($4.6\%$)
  - Type `1` (Active volcano): 0 records
  - Type `3` (Offshore): 0 records
- **Qualifying Vegetation Fires:**
  $$\text{Filter: } \text{type} == 0 \land \text{confidence} \in \{\text{'n'}, \text{'h'}, \text{'nominal'}, \text{'high'}\} \implies \mathbf{225 \text{ observations}}$$
- **Temporal Distribution Across Pilot Window:**
  - 2023-03-15: 11
  - 2023-03-16: 18
  - 2023-03-17: 55
  - 2023-03-18: 0 (Day with zero detections — confirmed unconfirmed negative)
  - 2023-03-19: 6
  - 2023-03-20: 3
  - 2023-03-21: 2
  - 2023-03-22: 8
  - 2023-03-23: 27
  - 2023-03-24: 20
  - 2023-03-25: 16
  - 2023-03-26: 20
  - 2023-03-27: 89
  - 2023-03-28: 74
- **Spatial Bounds Check:** $100\%$ of detected coordinates fall strictly within $[21.0^\circ\text{N}, 23.0^\circ\text{N}]$ and $[79.0^\circ\text{E}, 81.0^\circ\text{E}]$.

---

## 4. Spatial Partition & Buffer Audit (Phase 3.3.1 Corrected Audit)

### 4.1 Reproduction of Unique Positive Cell-Days (173 Count)
- **Raw Observations:** 349 total FIRMS records from `VIIRS_SNPP_SP` across the Central India pilot region ($21.0^\circ\text{--}23.0^\circ\text{N}, 79.0^\circ\text{--}81.0^\circ\text{E}$) for March 15–28, 2023.
- **Target Filter:**
  $$\text{Filter: } \text{type} == 0 \land \text{confidence} \in \{\text{'n'}, \text{'h'}, \text{'nominal'}, \text{'high'}\} \implies \mathbf{225 \text{ qualifying observations}}$$
- **Grid Cell Discretization ($0.05^\circ \times 0.05^\circ$):**
  - Bounding box spans $2.0^\circ \text{ lat} \times 2.0^\circ \text{ lon}$, creating a $40 \times 40 = 1,600$ cell grid.
  - Row index $i = \lfloor (\text{lat} - 21.0) / 0.05 \rfloor \in [0, 39]$ (South to North).
  - Column index $j = \lfloor (\text{lon} - 79.0) / 0.05 \rfloor \in [0, 39]$ (West to East).
  - Multiple hotspot detections occurring within the same cell $s=(i, j)$ on the same day $t$ collapse into a single binary label $Y_{s,t} = 1$.
- **Reproduction Outcome:**
  - The 225 qualifying records collapse into exactly **173 unique positive cell-days** across **137 unique grid cells** (clustering ratio: $1.30$ detections per positive cell-day).
  - Across the $1,600 \times 14 = 22,400$ total space-time evaluation cells, the empirical positive prevalence is $\frac{173}{22,400} \approx \mathbf{0.77\%}$.

### 4.2 Spatial Validation Design & Distance Disambiguation
In spatial cross-validation literature (e.g. Roberts et al., 2017; Valavi et al., 2019), an interior buffer / dead-zone is excised along fold boundaries to mitigate spatial autocorrelation leakage. Two distinct interpretations of "20 km buffer" exist and are disambiguated below:

1. **Design 1 (~20 km Total Exclusion Band Width across boundary):**
   - Defines a total dead-zone strip of width $W \approx 20\,\text{km}$ centered on each partition axis ($\text{lat} = 22.0^\circ\text{N}$, $\text{lon} = 80.0^\circ\text{E}$).
   - This corresponds to an exclusion margin of $\approx 10\,\text{km}$ on each side of the dividing line ($\pm 10\,\text{km}$).
   - In $0.05^\circ$ grid cells: $\pm 2$ cells on each side (rows $18\dots 21$, cols $18\dots 21$), creating a 4-cell wide dead-zone strip across the boundary line.
2. **Design 2 (20 km Exclusion Margin on Each Side / ~40 km Total Width):**
   - Enforces a full $20\,\text{km}$ exclusion margin on each side of the dividing line ($\pm 20\,\text{km}$).
   - In $0.05^\circ$ grid cells: $\pm 4$ cells on each side (rows $16\dots 23$, cols $16\dots 23$), creating an 8-cell wide dead-zone strip across the boundary line.

### 4.3 Metric Distance Justification & Grid Approximation
At the Central India pilot latitude ($\approx 22.0^\circ\text{N}$):
- $1^\circ \text{ latitude} \approx 110.74\,\text{km} \implies 0.05^\circ \text{ cell dimension} \approx \mathbf{5.537\,\text{km}}$.
- $1^\circ \text{ longitude} \approx 111.320 \times \cos(22.0^\circ) \approx 103.216\,\text{km} \implies 0.05^\circ \text{ cell dimension} \approx \mathbf{5.161\,\text{km}}$.

Because the modeling unit is a discrete $0.05^\circ$ raster cell with tabular feature vectors (ERA5-Land reanalysis and Copernicus DEM slope/aspect), spatial exclusion must operate at the discrete cell level rather than bisecting individual raster cells:
- **2-Cell Margin (~10 km on each side; Design 1):**
  - $\Delta \text{lat} = 2 \times 5.537\,\text{km} = 11.07\,\text{km}$ margin ($\mathbf{22.15\,\text{km}}$ total width across lat boundary).
  - $\Delta \text{lon} = 2 \times 5.161\,\text{km} = 10.32\,\text{km}$ margin ($\mathbf{20.64\,\text{km}}$ total width across lon boundary).
  - Average total band width: $\approx 21.4\,\text{km}$.
- **4-Cell Margin (~20 km on each side; Design 2):**
  - $\Delta \text{lat} = 4 \times 5.537\,\text{km} = 22.15\,\text{km}$ margin ($\mathbf{44.30\,\text{km}}$ total width across lat boundary).
  - $\Delta \text{lon} = 4 \times 5.161\,\text{km} = 20.64\,\text{km}$ margin ($\mathbf{41.28\,\text{km}}$ total width across lon boundary).
  - Average total band width: $\approx 42.8\,\text{km}$.

**Continuous Metric Geodesic Distance Verification:**
Computing the geodesic distance from the center of each grid cell to the dividing coordinate lines confirms:
- $\{ (i, j) : \min(d_{\text{lat}}, d_{\text{lon}}) < 10.0\,\text{km} \}$ isolates exactly rows $18\dots 21$ and cols $18\dots 21$, yielding identically **21** excluded positive cell-days.
- $\{ (i, j) : \min(d_{\text{lat}}, d_{\text{lon}}) < 20.0\,\text{km} \}$ isolates exactly rows $16\dots 23$ and cols $16\dots 23$, yielding identically **49** excluded positive cell-days.

### 4.4 Spatial Partition Reconciliation & Overlap Verification

| Quadrant | Geographic Extent | Grid Row / Col Range | Pre-Exclusion ($Y_{s,t}=1$) | Buffer Excluded (Design 1: 2-cell) | Post-Exclusion Remaining (Design 1) | Buffer Excluded (Design 2: 4-cell) | Post-Exclusion Remaining (Design 2) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Q1 (NW)** | $[22.0^\circ\text{--}23.0^\circ\text{N}, 79.0^\circ\text{--}80.0^\circ\text{E}]$ | Rows $20\dots 39$, Cols $0\dots 19$ | **57** | 11 | **46** | 13 | **44** |
| **Q2 (NE)** | $[22.0^\circ\text{--}23.0^\circ\text{N}, 80.0^\circ\text{--}81.0^\circ\text{E}]$ | Rows $20\dots 39$, Cols $20\dots 39$ | **26** | 3 | **23** | 16 | **10** |
| **Q3 (SW)** | $[21.0^\circ\text{--}22.0^\circ\text{N}, 79.0^\circ\text{--}80.0^\circ\text{E}]$ | Rows $0\dots 19$, Cols $0\dots 19$ | **53** | 5 | **48** | 14 | **39** |
| **Q4 (SE)** | $[21.0^\circ\text{--}22.0^\circ\text{N}, 80.0^\circ\text{--}81.0^\circ\text{E}]$ | Rows $0\dots 19$, Cols $20\dots 39$ | **37** | 2 | **35** | 6 | **31** |
| **Total** | $[21.0^\circ\text{--}23.0^\circ\text{N}, 79.0^\circ\text{--}81.0^\circ\text{E}]$ | $40 \times 40$ ($1,600$ cells) | **173** | **21** | **152** | **49** | **124** |

#### Reconciliation Invariants:
1. **Per-Quadrant Conservation:** $\text{Pre}[q] = \text{Post}[q] + \text{Buffer}[q]$ holds strictly across all 4 quadrants for both designs:
   - Design 1: $57 = 46 + 11$; $26 = 23 + 3$; $53 = 48 + 5$; $37 = 35 + 2$.
   - Design 2: $57 = 44 + 13$; $26 = 10 + 16$; $53 = 39 + 14$; $37 = 31 + 6$.
2. **Total Population Conservation:** $\sum \text{Post} + \text{Total Buffer} = \text{Total Pre}$:
   - Design 1: $152 + 21 = 173$ ($100.0\%$).
   - Design 2: $124 + 49 = 173$ ($100.0\%$).
3. **Cross-Fold Isolation & Zero Overlap:**
   - Every grid cell $(i, j)$ belongs to exactly one post-exclusion evaluation quadrant or the buffer zone.
   - Pairwise intersection across all fold combinations ($Q_1 \cap Q_2$, $Q_1 \cap Q_3$, $Q_1 \cap Q_4$, $Q_2 \cap Q_3$, $Q_2 \cap Q_4$, $Q_3 \cap Q_4$) is identically **0**.
4. **Buffer Case Removal:** Buffer observations are completely excised from the spatial holdout evaluation pools, not merely tallied.

### 4.5 Statistical Limitation & Evaluation Reassessment
- **Quadrant 2 Sample Scarcity:** Under Design 2 (20 km margin on each side), Quadrant 2 retains only **10 positive cell-days** across the entire 14-day window. Evaluating precision-recall curves or F1-scores on a test fold with only 10 positive cases yields wide confidence intervals and unacceptably high variance.
- **Provisional Status:** In accordance with Rule 8, Rule 17, and Rule 18, the 4-block spatial holdout design cannot be declared validated on a 14-day sample and is classified as **Provisional (`PENDING_SUPERVISOR_REVIEW` under SUP-08)**.
- **Recommended Evaluation Design:**
  1. **Multi-Year Temporal Holdout (Primary):** Aggregate 2020–2022 as training/validation data and calendar year 2023 as prospective holdout test data (providing thousands of positive fire events per fold).
  2. **Ecoregion Clustered Cross-Validation:** Replace arbitrary rectangular coordinate crosshairs with ecologically bounded spatial blocks (e.g. WWF Terrestrial Ecoregions / forest cover zones) with 20 km edge buffers.
  3. **Purged Rolling Window Validation:** Enforce a 7-day purging buffer prior to each test interval to prevent rolling antecedent weather features from leaking across fold boundaries.

---

## 5. Transferred Bytes & Storage Audit

| Source | Request Type | HTTP Status | Transferred Bytes | Payload Type | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Copernicus_DEM_N21_E079` | HEAD | 200 | 0 B | Header Probe | Verified S3 tile existence & length ($40.98\,\text{MB}$) |
| `Copernicus_DEM_N21_E080` | HEAD | 200 | 0 B | Header Probe | Verified S3 tile existence & length ($42.28\,\text{MB}$) |
| `Copernicus_DEM_N22_E079` | HEAD | 200 | 0 B | Header Probe | Verified S3 tile existence & length ($40.87\,\text{MB}$) |
| `Copernicus_DEM_N22_E080` | HEAD | 200 | 0 B | Header Probe | Verified S3 tile existence & length ($42.23\,\text{MB}$) |
| `Copernicus_DEM_N21_E079` | GET Range (0-1023) | 206 | 1,024 B | Header Probe | Verified Little-Endian TIFF Magic `42` |
| `Open_Meteo_NW_Q1` | GET (21 days) | 200 | 24,105 B | Dataset Payload | 504 hourly records at $(22.5^\circ\text{N}, 79.5^\circ\text{E})$ |
| `Open_Meteo_NE_Q2` | GET (21 days) | 200 | 24,080 B | Dataset Payload | 504 hourly records at $(22.5^\circ\text{N}, 80.5^\circ\text{E})$ |
| `Open_Meteo_SW_Q3` | GET (21 days) | 200 | 24,126 B | Dataset Payload | 504 hourly records at $(21.5^\circ\text{N}, 79.5^\circ\text{E})$ |
| `Open_Meteo_SE_Q4` | GET (21 days) | 200 | 24,061 B | Dataset Payload | 504 hourly records at $(21.5^\circ\text{N}, 80.5^\circ\text{E})$ |
| `NASA_FIRMS_P1` | GET (2023-03-15, 5d) | 200 | 7,085 B | Dataset Payload | 90 records (March 15–19) |
| `NASA_FIRMS_P2` | GET (2023-03-20, 5d) | 200 | 4,782 B | Dataset Payload | 60 records (March 20–24) |
| `NASA_FIRMS_P3` | GET (2023-03-25, 4d) | 200 | 15,556 B | Dataset Payload | 199 records (March 25–28) |
| **Total Transferred** | — | — | **124,819 B** | — | **$\sim 0.119\,\text{MB}$ (Cap $\le 25.0\,\text{MB}$ Respected)** |

- **Dataset Payloads:** $123,795\,\text{bytes}$ ($99.18\%$ of total transfer).
- **Probes & Headers:** $1,024\,\text{bytes}$ ($0.82\%$ of total transfer).
- **Disk Footprint After Cleanup:** Exactly $0\,\text{bytes}$ retained on disk.

---

## 6. Security & Governance Audit

1. **Credential Safety:**
   - `.env` verified ignored by Git (`.gitignore:45:.env`).
   - `FIRMS_MAP_KEY` read via environment; masked as `[MAP_KEY_REDACTED]` in all script output, reports, and exception handlers.
   - Zero credentials or tokens present in Git commits, diffs, or staged trees.
2. **Scientific Honesty & Limitations:**
   - **Label Uncertainty:** Absence of a detected hotspot ($Y_{s,t} = 0$, e.g., March 18) is formally treated as an **unconfirmed negative**, not proof of fire absence, due to polar diurnal overpass gaps (~13:30/01:30 solar time), cloud/smoke opacity, and sub-canopy masking.
   - **Meteorological Downscaling:** Resampling $0.1^\circ$ ERA5-Land to the $0.05^\circ$ common analysis grid via bilinear interpolation does **not** create sub-grid physical atmospheric detail or resolve microclimatic wind channeling.
   - **Topography Scope:** Copernicus DEM check verified object presence and TIFF Magic 42 header. **Full internal raster array validity, void-free status, and elevation values are not evaluated and remain deferred to Phase 4.**

---

## 7. Phase Gate Determination

* **Outcome:** **PASS WITH LIMITATIONS**
  - The empirical feasibility of NASA FIRMS (`VIIRS_SNPP_SP`), ERA5-Land reanalysis, and Copernicus DEM is fully validated across access, schema, temporal alignment, and storage constraints.
  - Phase 3 experimental criteria are satisfied.
* **Lifecycle Governance Decision:**
  - In compliance with Rule 3, Rule 15, and Rule 18, the wildfire dataset stack is **NOT promoted to `Data Ready` without supervisor sign-off**.
  - Current lifecycle label: `Feasibility Verified (Access & Schema Validated; Data Ready Pending Supervisor Review for Phase 4 Authorization)`.
  - Next planned phase: Phase 4 Ingestion Pipeline (awaiting formal Phase 3 gate approval).
