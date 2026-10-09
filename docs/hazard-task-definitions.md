# Hazard Task Definitions and Scientific Scope

**Project:** Satellite-Based Multi-Hazard Disaster Risk Prediction and Early Warning System Using AI/ML  
**Document Ownership:** Authoritative specification for hazard task definitions, target variables, units of analysis, and scientific safeguards.  
**Cross-References:** Scope overview in [project-scope.md](file:///Users/salman/Desktop/satellite-disaster/docs/project-scope.md), Dataset mapping in [dataset-feasibility-matrix.md](file:///Users/salman/Desktop/satellite-disaster/docs/dataset-feasibility-matrix.md).

---

## 1. Scientific Safeguards & Operational Principles

To maintain scientific integrity and avoid overclaiming, the system enforces the following principles:

1. **Detection is Not Forecasting:** Satellite observation detects current or past physical states (e.g., surface reflectance, thermal radiance, microwave backscatter change). Active-fire hotspot detection (e.g., MODIS/VIIRS) indicates a fire actively burning at sensor overpass time; it is not a prediction of future fire occurrence.
2. **Susceptibility is Not Deterministic Timing:** Spatial susceptibility models (e.g., for landslides or floods) quantify static or quasi-static conditional probability of where a hazard is prone to occur given terrain and environmental conditioning factors. They do not predict the exact day or hour an event will occur without real-time dynamic triggering thresholds.
3. **Physical Anomalies are Not Guaranteed Eruptions:** Satellite-detected thermal hotspots or volcanic plume $\text{SO}_2$ column density indicate geothermal activity or magmatic degassing; they do not prove imminent explosive volcanic eruption without subsurface geophysical instrumentation (borehole tiltmeters, seismic tremor arrays).
4. **Proxy Indices are Not Calibrated Probabilities:** Empirical drought indices (e.g., VHI, NDRE, SPI, SPEI) measure observed vegetative or meteorological deviations from historical baselines; they are not calibrated Bayesian probabilities of future agricultural collapse.
5. **Atmospheric Hazards Require Multi-Modal Data:** Standalone polar-orbiting satellite snapshots cannot forecast cyclone tracks or convective storms. Operational atmospheric forecasting requires numerical weather prediction (NWP) model outputs, geostationary rapid-scan imagery, and vertical atmospheric profiles.
6. **Avalanche Prediction Requires Subsurface Snowpack Telemetry:** Avalanche slab release depends on internal snowpack stratigraphy (weak layer formation, buried faceted crystals, temperature gradients) and micro-topography, which cannot be measured by satellite imagery alone.

### 1.1 Strictly Out-of-Scope Disasters (Explicit Exclusions)
The following phenomena are strictly excluded from the project:
- **Earthquakes:** Solid-earth lithospheric fault rupture is not reliably predictable in operational lead-times via satellite surface imaging.
- **Tsunamis:** Hydrodynamic wave propagation requires deep-sea pressure sensors (DART buoys) and coastal seismic alarms, outside terrestrial Earth observation.
- **Chemical / Industrial Disasters:** Point-source toxic releases are anthropogenic technological failures requiring facility SCADA sensors.
- **Terrorist Attacks & Conflict Events:** Human conflict events fall under geopolitical/security domains outside physical Earth observation.


---

## 2. In-Scope Hazard Analysis (8 Hazards)

---

### Hazard 1: Flood
* **Internal Identifier:** `flood`
* **Real-World Problem:** Rapid and seasonal inundation of populated river basins, floodplains, and coastal regions leading to displacement, infrastructure damage, and loss of life.
* **Candidate Task Type:** Dual-track formulation:
  1. *Track A (Susceptibility Assessment):* High-resolution spatial mapping of baseline flood inundation susceptibility.
  2. *Track B (Near-Real-Time Inundation Extent Detection):* SAR-based surface water delineation post-event compared against permanent baseline water bodies.
* **Proposed Target Variable:**
  - *Track A:* Continuous susceptibility score $[0, 1]$ or categorical susceptibility tier (Low, Medium, High, Very High) per grid cell.
  - *Track B:* Binary flood inundation mask ($1 = \text{inundated}, 0 = \text{dry/normal}$).
* **Unit of Analysis:** Spatial raster cell ($30\text{ m} \times 30\text{ m}$ to $100\text{ m} \times 100\text{ m}$).
* **Geographic Coverage Under Consideration:** Selected river basin pilot areas (e.g., Brahmaputra / Ganges floodplains, Godavari basin, or European Copernicus pilot basins).
* **Temporal Resolution & Prediction Horizon:**
  - Track A: Static / seasonal baseline (annual/seasonal update).
  - Track B: Near-real-time detection dependent on SAR satellite revisit cycle (6–12 days for Sentinel-1).
* **Inputs Available at Inference Time:**
  - Static: Elevation/DEM (Copernicus DEM / SRTM), slope, Topographic Wetness Index (TWI), distance to stream network, soil hydraulic conductivity, land-use/land-cover (LULC).
  - Dynamic: Antecedent precipitation index (GPM IMERG, ERA5), soil moisture anomalies (Sentinel-1 backscatter / SMAP).
* **Candidate Satellite & Environmental Features:**
  - Sentinel-1 SAR (C-band VV/VH backscatter, coherence change).
  - Sentinel-2 / Landsat-8 (MNDWI, NDWI, optical water indices for cloud-free baselines).
  - GPM IMERG / ERA5 hourly/daily precipitation totals.
  - HydroSHEDS / Copernicus DEM hydro-derivatives.
* **Candidate Ground-Truth / Reference Labels:**
  - Historical flood extents from Dartmouth Flood Observatory (DFO) and Copernicus Emergency Management Service (EMS) Rapid Mapping activations.
  - Permanent water body masks (JRC Global Surface Water).
* **Evaluation Approach:**
  - Critical Success Index (CSI / Threat Score), Intersection over Union (IoU), Precision, Recall, and ROC-AUC.
* **Scientific Limitations & Failure Modes:**
  - Optical imagery is obscured by dense cloud cover during peak storm/flood events.
  - SAR backscatter over inundated urban areas suffers from double-bounce radar artifacts and shadow distortion.
  - Dense vegetation canopies obscure standing flood water beneath leaves in C-band SAR.
* **Feasibility Status:** **Feasible for Defined Initial Task (Candidate Pilot)**.

---

### Hazard 2: Wildfire / Forest Fire
* **Internal Identifier:** `wildfire`
* **Real-World Problem:** Uncontrolled vegetation fires threatening ecosystems, settlements, and atmospheric air quality.
* **Candidate Task Type:** Dual-track formulation:
  1. *Track A (Wildfire Danger Susceptibility Forecasting):* Short-term (24–72h) fire danger rating index predicting spatial susceptibility of vegetation to fire initiation and spread.
  2. *Track B (Thermal Anomaly & Burn Severity Mapping):* Rapid thermal hotspot detection and post-fire Normalized Burn Ratio (NBR / dNBR) severity estimation.
* **Proposed Target Variable:**
  - *Track A:* Fire ignition and spread susceptibility score ($[0, 1]$ probability) or Fire Weather Index (FWI) proxy class (Low, Moderate, High, Very High, Extreme).
  - *Track B:* Continuous burn severity index (dNBR) and active fire confidence ($0\text{--}100\%$).
* **Unit of Analysis:** Gridded spatial cells ($500\text{ m} \times 500\text{ m}$ to $1\text{ km} \times 1\text{ km}$ for danger; $20\text{ m} \times 20\text{ m}$ for burn scar assessment).
* **Geographic Coverage Under Consideration:** Wildfire-prone pilot regions (e.g., Central India deciduous forest belts, Western North America, or Mediterranean basin).
* **Temporal Resolution & Prediction Horizon:**
  - Danger forecast: 24 to 72 hours ahead.
  - Thermal detection: 3 to 12 hours (MODIS/VIIRS overpasses).
  - Burn severity: Post-event / bi-weekly composite.
* **Inputs Available at Inference Time:**
  - Dynamic Weather: 2m air temperature, 10m wind speed and direction, relative humidity, dry-spell duration (ERA5 / Open-Meteo).
  - Fuel Moisture / Vegetation State: Normalized Difference Vegetation Index (NDVI), Moisture Stress Index (MSI), Normalized Difference Water Index (NDWI).
  - Topography: Slope, aspect, elevation (SRTM / Copernicus DEM).
  - Anthropogenic: Distance to roads, distance to settlement edges.
* **Candidate Satellite & Environmental Features:**
  - Sentinel-2 / Landsat-8 (Bands B08, B11, B12 for NBR, NDVI).
  - VIIRS (375m) and MODIS (1km) Active Fire / Thermal Anomalies (FIRMS).
  - ECMWF / Global Fire Assimilation System (GFAS) / Open-Meteo fire weather variables.
* **Candidate Ground-Truth / Reference Labels:**
  - Historical active fire point clusters from NASA FIRMS VIIRS/MODIS with verified confidence $\ge 80\%$.
  - Mapped fire perimeters from GlobFire or national forest agency fire incidence reports.
* **Evaluation Approach:**
  - Precision, Recall, F1-score, Spatial Brier Score, and Area Under the Precision-Recall Curve (PR-AUC) given high class imbalance.
* **Scientific Limitations & Failure Modes:**
  - Active-fire hotspot detection records current combustion, not future ignition.
  - Cloud cover and heavy smoke plumes mask optical and shortwave infrared detectors.
  - Human ignition sources (arson, agricultural stubble burning, accidental campfires) are stochastic and lack direct physical predictors.
* **Feasibility Status:** **Feasible for Defined Initial Task (Candidate Pilot)**.

---

### Hazard 3: Landslide
* **Internal Identifier:** `landslide`
* **Real-World Problem:** Mass wasting and slope failure along mountainous terrain triggered by monsoon rainfall or prolonged moisture saturation.
* **Candidate Task Type:** Spatial Susceptibility Assessment conditionally modulated by dynamic rainfall triggering thresholds (Susceptibility-Trigger Matrix).
* **Proposed Target Variable:** Spatial susceptibility probability $[0, 1]$ categorized into susceptibility tiers (Low, Medium, High, Very High) paired with a binary dynamic warning trigger (Rainfall Threshold Exceeded).
* **Unit of Analysis:** High-resolution slope units or spatial grid cells ($30\text{ m} \times 30\text{ m}$).
* **Geographic Coverage Under Consideration:** Mountainous pilot sectors (e.g., Western Ghats of India, Himalayas / Uttarakhand, or Italian Alpine corridors).
* **Temporal Resolution & Prediction Horizon:**
  - Susceptibility: Static multi-year assessment.
  - Dynamic Trigger: 24 to 48 hours rainfall accumulation forecast.
* **Inputs Available at Inference Time:**
  - Static: Slope gradient, aspect, plan/profile curvature, lithology / soil texture, distance to faults, distance to drainage networks, distance to roads, historical deforestation.
  - Dynamic: Cumulative 3-day, 7-day, and 14-day antecedent precipitation, current 24h forecasted rainfall intensity.
* **Candidate Satellite & Environmental Features:**
  - ALOS PALSAR / Copernicus 30m DEM derivatives (Slope, Aspect, Curvature, Stream Power Index).
  - Sentinel-2 LULC and NDVI change (identifying devegetated slopes).
  - GPM IMERG / ERA5 rainfall accumulation series.
* **Candidate Ground-Truth / Reference Labels:**
  - NASA Global Landslide Catalog (GLC) and Geological Survey of India (GSI) National Landslide Susceptibility Mapping (NLSM) event inventories.
* **Evaluation Approach:**
  - ROC-AUC, Spatial Cross-Validation (block spatial k-fold to avoid spatial autocorrelation overfitting), Success Rate Curve (SRC), and Prediction Rate Curve (PRC).
* **Scientific Limitations & Failure Modes:**
  - Susceptibility maps do *not* predict exact failure time; they identify *where* failure is likely given a sufficient physical trigger.
  - Historical landslide inventories are heavily biased toward roads, settlements, and populated corridors, omitting backcountry slope failures.
  - Subsurface geotechnical parameters (pore-water pressure, shear strength, cohesion) cannot be directly sensed by orbital satellites.
* **Feasibility Status:** **Feasible with Unresolved Dependencies (Secondary Phase)**.

---

### Hazard 4: Drought
* **Internal Identifier:** `drought`
* **Real-World Problem:** Prolonged deficiency in precipitation and soil moisture resulting in agricultural stress, groundwater depletion, and vegetative die-off.
* **Candidate Task Type:** Multi-Index Agricultural & Meteorological Drought Monitoring and Multi-Week Trajectory Forecasting.
* **Proposed Target Variable:** Standardized Drought Severity Class based on continuous anomaly indices:
  - Vegetation Condition Index (VCI) / Vegetation Health Index (VHI) $[0\text{--}100]$.
  - Standardized Precipitation-Evapotranspiration Index (SPEI-1, SPEI-3).
  - Target classes: No Drought, Mild, Moderate, Severe, Extreme.
* **Unit of Analysis:** District / sub-basin aggregate or gridded regular cells ($1\text{ km} \times 1\text{ km}$ to $5\text{ km} \times 5\text{ km}$).
* **Geographic Coverage Under Consideration:** Arid / semi-arid agricultural belts (e.g., Marathwada/Vidarbha, India; Sahel; or US Great Plains).
* **Temporal Resolution & Prediction Horizon:**
  - Monitoring cadence: Weekly / 16-day compositing periods.
  - Forecast horizon: 2 to 6 weeks forward trend projection.
* **Inputs Available at Inference Time:**
  - Multi-temporal vegetation indices over 10-year baseline.
  - Land Surface Temperature (LST) anomalies.
  - Root-zone soil moisture estimates.
  - Cumulative precipitation deficits and potential evapotranspiration (PET).
* **Candidate Satellite & Environmental Features:**
  - MODIS / Sentinel-3 / Sentinel-2: NDVI, EVI, Land Surface Temperature (LST).
  - SMAP / Sentinel-1 surface soil moisture.
  - CHIRPS / ERA5-Land precipitation and PET time-series.
* **Candidate Ground-Truth / Reference Labels:**
  - US Drought Monitor (USDM) classifications, National Drought Management Authority records, or verified SPEI / SPI calculation baselines.
* **Evaluation Approach:**
  - Mean Absolute Error (MAE), Root Mean Square Error (RMSE) on continuous indices; Weighted Cohen’s Kappa and Ordinal F1-score across severity classes.
* **Scientific Limitations & Failure Modes:**
  - Drought indices represent observational deviations from historical normal; they are not calibrated probability densities of catastrophic famine or crop loss.
  - Irrigation and human groundwater extraction decouple surface vegetation greenness from meteorological precipitation deficits, creating false-normal signatures.
  - Cloud persistence can corrupt thermal and optical composites during crucial monsoon transition windows.
* **Feasibility Status:** **Feasible with Unresolved Dependencies (Secondary Phase)**.

---

### Hazard 5: Cyclone / Tropical Storm
* **Internal Identifier:** `cyclone`
* **Real-World Problem:** Violent rotating oceanic storm systems producing extreme destructive winds, storm surges, and torrential inland rainfall.
* **Candidate Task Type:** Cyclone Intensity Estimation and Track Deviation Monitoring.
* **Proposed Target Variable:**
  - Current Maximum Sustained Wind Speed (knots / km/h) and Central Pressure (hPa) (Dvorak technique proxy).
  - 12h-to-48h Storm Center Position Displacement ($\Delta\text{lat}, \Delta\text{lon}$).
* **Unit of Analysis:** Storm-centered bounding box / storm event frame ($10^\circ \times 10^\circ$ coordinate window).
* **Geographic Coverage Under Consideration:** North Indian Ocean (Bay of Bengal / Arabian Sea) or Atlantic / Western Pacific basins.
* **Temporal Resolution & Prediction Horizon:**
  - Cadence: 3 to 6 hours.
  - Horizon: 12 to 48 hours for trajectory displacement; immediate nowcast for intensity.
* **Inputs Available at Inference Time:**
  - Geostationary infrared and water vapor brightness temperatures (INSAT-3D/3DR, GOES, or Meteosat).
  - Sea Surface Temperature (SST) fields.
  - Deep-layer vertical wind shear, mid-tropospheric humidity, and 850hPa/200hPa geopotential height fields (ERA5 / GFS).
* **Candidate Satellite & Environmental Features:**
  - Infrared cloud-top brightness temperature profiles ($10.8\,\mu\text{m}$).
  - Scatterometer ocean surface wind vectors (ASCAT).
  - NOAA Optimum Interpolation SST (OISST).
  - GFS/ECMWF atmospheric dynamic variables.
* **Candidate Ground-Truth / Reference Labels:**
  - IBTrACS (International Best Track Archive for Climate Stewardship) records.
  - Official Regional Specialized Meteorological Centre (RSMC) / IMD / JTWC best-track advisories.
* **Evaluation Approach:**
  - Mean Absolute Error (MAE) in maximum wind speed (knots); Mean Along-Track and Cross-Track Position Error (kilometers).
* **Scientific Limitations & Failure Modes:**
  - Satellite optical/IR imagery alone cannot forecast trajectory without numerical weather prediction (NWP) steering flow fields.
  - Polar-orbiting satellites pass too infrequently (1–2 times/day) for operational storm tracking; geostationary data access and calibration pipelines are required.
  - Rapid Intensification (RI) events exhibit non-linear inner-core physics that remain a notorious frontier in atmospheric science.
* **Feasibility Status:** **Research Required (Stretch Goal)**.

---

### Hazard 6: Severe Storm / Extreme Convective Weather
* **Internal Identifier:** `severe_storm`
* **Real-World Problem:** Localized convective thunderstorms, intense hail, microbursts, and severe lightning causing sudden urban flash floods and damage.
* **Candidate Task Type:** Convective Initiation Detection and 0-to-2 Hour Radar/Satellite Nowcasting.
* **Proposed Target Variable:**
  - Binary Convective Storm Occurrence within grid cell in next 30–120 minutes.
  - Maximum Expected Radar Reflectivity ($dBZ \ge 40$).
* **Unit of Analysis:** Regional high-resolution grid ($2\text{ km} \times 2\text{ km}$ to $5\text{ km} \times 5\text{ km}$).
* **Geographic Coverage Under Consideration:** Doppler Weather Radar coverage areas (e.g., coastal and urban radar rings in India or NOAA NEXRAD zones).
* **Temporal Resolution & Prediction Horizon:**
  - Cadence: 10 to 15 minutes.
  - Horizon: 30 to 120 minutes (nowcasting horizon).
* **Inputs Available at Inference Time:**
  - Rapid-scan geostationary satellite IR channels (Cloud-top cooling rates).
  - Convective Available Potential Energy (CAPE), Lifted Index (LI), Convective Inhibition (CIN) from NWP analysis.
  - Ground-based Doppler weather radar reflectivity composites (where accessible).
* **Candidate Satellite & Environmental Features:**
  - INSAT-3D / GOES Rapid Scan Split-Window IR channels.
  - ERA5 / GFS thermodynamic instability indices.
  - Global Lightning Mapper (GLM) / ground lightning network pulses.
* **Candidate Ground-Truth / Reference Labels:**
  - Doppler Radar Reflectivity grids ($dBZ \ge 45$), ground station automated weather observations, and lightning flash records.
* **Evaluation Approach:**
  - Critical Success Index (CSI), False Alarm Rate (FAR), Probability of Detection (POD), and Fraction Skill Score (FSS) across spatial neighborhood radii.
* **Scientific Limitations & Failure Modes:**
  - Polar-orbiting satellites (Sentinel/Landsat) are completely useless for sub-hourly convective storm nowcasting due to 5–12 day revisit cycles.
  - High reliance on geostationary rapid-scan pipelines or ground-based Doppler radar networks, which have variable open data availability.
  - Convective initiation is highly sensitive to microscale boundary layer triggers that are unresolved by regional models.
* **Feasibility Status:** **Research Required (Stretch Goal)**.

---

### Hazard 7: Volcanic Activity
* **Internal Identifier:** `volcanic_activity`
* **Real-World Problem:** Volcanic degassing, thermal extrusion, pyroclastic flows, and ash dispersion disrupting aviation, settlements, and regional ecology.
* **Candidate Task Type:** Thermal Anomaly Detection and Sulfur Dioxide ($\text{SO}_2$) Column Density Monitoring.
* **Proposed Target Variable:**
  - Volcanic Radiative Power (VRP, in Megawatts) calculated from Shortwave/Middle Infrared radiation.
  - Total vertical column density of $\text{SO}_2$ (Dobson Units or $\text{mol/m}^2$) over the volcanic caldera.
* **Unit of Analysis:** Spatial bounding box ($50\text{ km} \times 50\text{ km}$) surrounding cataloged active volcanic centers.
* **Geographic Coverage Under Consideration:** Global active volcanoes (e.g., Barren Island, Stromboli, Mount Etna, Kilauea, Merapi).
* **Temporal Resolution & Prediction Horizon:**
  - Monitoring Cadence: Daily (Sentinel-5P, MODIS, VIIRS, Sentinel-2).
  - Horizon: Observational detection and anomaly tracking (NOT deterministic eruption prediction).
* **Inputs Available at Inference Time:**
  - Sentinel-5P TROPOMI UV/visible spectral bands.
  - Sentinel-2 MSI Bands B11, B12 (SWIR) and B8A (NIR).
  - MODIS / VIIRS thermal bands.
* **Candidate Satellite & Environmental Features:**
  - Sentinel-5P $\text{SO}_2$ total column product.
  - Normalized Hotspot Indices (NHI) and SWIR radiance ratios.
  - Baseline background thermal temperature of surrounding terrain.
* **Candidate Ground-Truth / Reference Labels:**
  - Smithsonian Institution Global Volcanism Program (GVP) activity reports.
  - MIROVA (Middle InfraRed Observation of Volcanic Activity) database.
* **Evaluation Approach:**
  - Anomaly detection Precision/Recall, Pearson correlation of estimated VRP against validated MIROVA records, Detection Lead-Time against Smithsonian event logs.
* **Scientific Limitations & Failure Modes:**
  - Thermal anomalies and $\text{SO}_2$ plumes do **not** prove imminent catastrophic explosive eruption; many volcanoes continuously degas and exhibit open magma lakes for decades without erupting.
  - Cloud cover, high-altitude meteorological moisture, and ice/snow cap reflections frequently generate false positives or obscure volcanic plumes.
  - Subsurface magmatic movement cannot be determined without borehole tiltmeters, GPS deformation arrays, and local seismometers.
* **Feasibility Status:** **Feasible for Detection / Deferred for Eruption Forecast (Stretch Goal)**.

---

### Hazard 8: Avalanche
* **Internal Identifier:** `avalanche`
* **Real-World Problem:** Rapid snow and ice detachment and downslope flow in alpine terrain, endangering transportation corridors, winter sports, and mountain settlements.
* **Candidate Task Type:** Static Avalanche Terrain Susceptibility Mapping and Snow Water Equivalent / Temperature Trigger Assessment.
* **Proposed Target Variable:**
  - Avalanche Terrain Exposure Scale (ATES) susceptibility category $[0\text{--}4]$ (Non-avalanche, Simple, Challenging, Complex).
  - Binary avalanche hazard bulletin advisory level (Low, Moderate, Considerable, High, Very High).
* **Unit of Analysis:** Alpine terrain slope unit or regular DEM grid cell ($10\text{ m} \times 10\text{ m}$ to $30\text{ m} \times 30\text{ m}$).
* **Geographic Coverage Under Consideration:** Selected high-altitude alpine corridors (e.g., Pir Panjal / Ladakh Himalayas, Swiss/French Alps, or Colorado Rockies).
* **Temporal Resolution & Prediction Horizon:**
  - Susceptibility: Static multi-year.
  - Trigger Monitoring: 24 to 72 hours based on snowfall, temperature, and wind drift.
* **Inputs Available at Inference Time:**
  - Terrain: Slope angle ($28^\circ\text{--}45^\circ$ primary release zone), aspect, curvature, terrain ruggedness, forest canopy density.
  - Snow/Meteo: Snow Depth, Snow Water Equivalent (SWE), 3-day snowfall accumulation, air temperature gradient, wind speed/direction.
* **Candidate Satellite & Environmental Features:**
  - High-resolution DEM (Copernicus DEM 30m / ALOS 30m / ArcticDEM).
  - Sentinel-1 SAR backscatter change (wet snow vs dry snow mapping).
  - Sentinel-2 NDSI (Normalized Difference Snow Index) and fractional snow cover.
  - ERA5-Land high-altitude precipitation and 2m temperature.
* **Candidate Ground-Truth / Reference Labels:**
  - European Avalanche Warning Services (EAWS) bulletins, Swiss SLF avalanche event inventories, or Defence Geoinformatics Research Establishment (DGRE / DRDO) records.
* **Evaluation Approach:**
  - Area Under ROC Curve (AUC) for terrain susceptibility; Ordinal accuracy and Heidke Skill Score (HSS) for regional danger tiers.
* **Scientific Limitations & Failure Modes:**
  - Operational avalanche forecasting depends heavily on internal snowpack stratigraphy (weak layer formation, buried hoar frost, faceted crystals), which cannot be measured by satellite imagery.
  - 30-meter DEM resolution is frequently too coarse to capture micro-couloirs, localized cornices, and terrain traps that release deadly slab avalanches.
  - Event ground-truth catalogs outside select Western European and North American test ranges are scarce and sparsely documented.
* **Feasibility Status:** **Deferred Pending Evidence (Stretch Goal)**.

---

## 3. Comparative Hazard Matrix

| Hazard | Task Type | Target | Unit | Geography | Horizon | Required Labels | Evaluation Approach | Key Limitations | Current Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Flood** (`flood`) | Susceptibility & Inundation Detection | Binary susceptibility $[0,1]$ & Inundation mask | $30\text{m}\times 30\text{m}$ raster cell | Selected river basin pilot areas | Static (Susceptibility) / 6–24h (SAR overpass) | Copernicus EMS, Dartmouth Flood Observatory, JRC Water | IoU, CSI, ROC-AUC | Radar double bounce in urban areas; cloud cover obscures optical; sub-canopy water invisible in C-band | **Feasible for Initial Task (Candidate Pilot)** |
| **Wildfire** (`wildfire`) | Danger Rating & Burn Severity Detection | Fire danger probability $[0,1]$ & dNBR score | $500\text{m}\times 500\text{m}$ grid (Danger) / $20\text{m}$ (Severity) | Forest & shrubland pilot belts | 24–72h forecast (Danger) / Post-event (Severity) | NASA FIRMS active fires, GlobFire perimeters | Precision, Recall, F1, PR-AUC, Spatial Brier Score | Active hotspot detects current burn not future ignition; stochastic human ignitions; cloud/smoke obscuration | **Feasible for Initial Task (Candidate Pilot)** |
| **Landslide** (`landslide`) | Susceptibility & Rainfall Trigger Monitoring | Susceptibility class & Threshold exceedance | $30\text{m}\times 30\text{m}$ slope unit | Mountainous pilot sectors (e.g. Western Ghats) | Static (Susceptibility) / 24–48h trigger | NASA GLC, Geological Survey of India NLSM | ROC-AUC, Spatial k-fold cross-val, Success Rate Curve | Susceptibility is not event timing; road reporting bias in inventories; subsurface pore pressure unmeasurable | **Feasible with Unresolved Dependencies** |
| **Drought** (`drought`) | Anomaly Index Monitoring & Trajectory Projection | Continuous VHI / SPEI anomaly & categorical tier | $1\text{km}\text{--}5\text{km}$ grid cell / District | Arid / semi-arid agricultural belts | Multi-week (2–6 weeks trend) | USDM records, verified SPEI/SPI calculations | MAE, RMSE, Weighted Cohen's Kappa, Ordinal F1 | Anomaly is not catastrophe probability; irrigation decouples greenness from meteorological drought | **Feasible with Unresolved Dependencies** |
| **Cyclone** (`cyclone`) | Intensity Estimation & Track Deviation Monitoring | Wind speed (knots) & center position displacement | $10^\circ \times 10^\circ$ storm frame | North Indian Ocean / Tropical basins | 12–48h track / Real-time intensity | IBTrACS, IMD/JTWC best-track advisories | MAE (knots), Along/Cross-track error (km) | Requires NWP steering flow; geostationary access needed; rapid intensification is non-linear | **Research Required** |
| **Severe Storm** (`severe_storm`) | Convective Initiation Nowcasting | Binary storm initiation & Reflectivity $\ge 40\text{dBZ}$ | $2\text{km}\times 2\text{km}$ grid cell | Doppler radar coverage zones | 30–120 minutes | Doppler Radar grids, lightning sensor pulses | CSI, FAR, POD, Fraction Skill Score (FSS) | Polar satellites too slow (5–12 day revisit); requires radar/geostationary feeds; microscale physics | **Research Required** |
| **Volcano** (`volcanic_activity`) | Thermal Anomaly & $\text{SO}_2$ Monitoring | Radiative power (MW) & $\text{SO}_2$ column density | $50\text{km}\times 50\text{km}$ caldera box | Cataloged global volcanic centers | Observational detection / Real-time | MIROVA database, Smithsonian GVP logs | Precision, Recall, Pearson $r$ with MIROVA | Anomaly does not prove imminent explosive eruption; persistent degassing volcanoes; cloud/snow artifacts | **Feasible for Detection / Deferred for Eruption Forecast** |
| **Avalanche** (`avalanche`) | Terrain Susceptibility & Danger Tier Assessment | ATES terrain class & regional danger tier | $10\text{m}\text{--}30\text{m}$ slope unit | Alpine mountain corridors | Static (Terrain) / 24–72h weather advisory | EAWS bulletins, SLF inventories, DGRE records | ROC-AUC, Heidke Skill Score (HSS) | Internal snowpack stratigraphy unmeasurable by satellite; 30m DEM misses micro-couloirs; sparse event labels | **Deferred Pending Evidence** |

---

## 4. Initial Pilot Selection Rationale (Provisional Hypothesis)

* **Candidate Options:** Wildfire (`wildfire`) and Flood (`flood`).
* **Feasibility Evidence:**
  1. *Open Ground-Truth Availability:* NASA FIRMS provides machine-readable active fire observations with confidence attributes; Copernicus EMS provides verified flood inundation polygons.
  2. *Accessible Feature Pipelines:* Both hazards utilize established multispectral indices (NBR, NDVI, MNDWI) and SAR backscatter accessible via Copernicus Open Access / CDSE and USGS EarthExplorer.
  3. *Scientific Clarity:* Clear division between susceptibility, real-time detection, and severity assessment without requiring complex non-linear atmospheric sounding or inaccessible subsurface telemetry.
* **Governance Status:** Provisional planning recommendation. Formally marked as **`PENDING_SUPERVISOR_REVIEW`** in [decision-log.md](file:///Users/salman/Desktop/satellite-disaster/docs/decision-log.md).
