# Technical Dataset Register

**Project:** Satellite-Based Multi-Hazard Disaster Risk Prediction and Early Warning System Using AI/ML  
**Document Ownership:** Technical data asset register documenting product specifications, access protocols, licensing terms, and ingestion constraints.  
**Phase 0 Evidence Notice:** Specifications in this register reflect authoritative documentation reviewed. Live API testing, credential validation, sample tile parsing, and definitive license reviews are explicitly scheduled for Phase 3. Unverified items are marked `Pending Verification in Phase 3`.  
**Cross-References:** Feasibility evaluation in [dataset-feasibility-matrix.md](file:///Users/salman/Desktop/satellite-disaster/docs/dataset-feasibility-matrix.md).

---

## 1. Candidate Dataset Specifications

---

### DS-01: NASA FIRMS Active Fire Data
* **Provider:** NASA Earth Science Data and Information System (ESDIS) / LANCE.
* **Canonical URL:** [https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms](https://earthdata.nasa.gov/earth-observation-data/near-real-time/firms)
* **Citation:** Schroeder, W., et al. (2014). The New VIIRS 375 m active fire detection product. *Remote Sensing of Environment*, 143, 85-96.
* **Product Identifier:** `VNP14IMGTDL` (Suomi-NPP VIIRS 375m) / `VJ114IMGTDL` (NOAA-20 VIIRS 375m) / `MCD14DL` (MODIS 1km).
* **Data Type & Format:** Tabular vector point data (CSV, GeoJSON, SHP).
* **Spatial & Temporal Resolution:**
  - Spatial: 375 m pixel footprint at nadir (VIIRS I-Band) / 1 km (MODIS).
  - Temporal: 3–6 hour latency (NRT); 2 overpasses/satellite/day.
* **Key Attributes / Schema:**
  - `latitude`, `longitude` (WGS 84 degrees)
  - `bright_ti4` (VIIRS I-4 brightness temp in Kelvin)
  - `confidence` (**Categorical string: `'low'`, `'nominal'`, `'high'`** for VIIRS; numeric $0\text{--}100\%$ applies only to MODIS)
  - `frp` (Fire Radiative Power in MW)
  - `acq_date` (`YYYY-MM-DD`), `acq_time` (`HHMM` UTC)
  - `type` (Integer: `0` = Presumed vegetation fire, `1` = Active volcano, `2` = Other static land source, `3` = Offshore detection)
* **Label Validity & Observability Protocol:**
  - Mandatory positive filter: `type == 0` (presumed vegetation fires) AND `confidence IN ('nominal', 'high')`.
  - Cells with zero observed hotspots are treated as **unconfirmed negatives** due to diurnal overpass gaps and smoke/cloud obscuration.
* **Access Method & Credentials:** RESTful HTTP API / Earthdata Download. Free `MAP_KEY` required for transactional API queries (up to 5,000 queries/day).
* **Licence & Redistribution:** NASA Open Data Policy (Free and open global distribution for research with citation).
* **Storage Footprint & Ingestion Impact:** Bounded pilot extract ($2^\circ \times 2^\circ$, 3 years) is ~5–15 MB CSV.
* **Sensor Lifecycle & Long-Term Continuity Notice:** NASA has announced that forward data delivery for Suomi-NPP VIIRS products will **cease on November 1, 2026**. While Suomi-NPP remains valid for historical retrospective training (2012–2024), operational forward deployments must migrate to NOAA-20 (`VJ114IMGTDL`) and NOAA-21 (`VJ214IMGTDL`) products.
* **Operational Verification State:** `Candidate Source, not fully verified (Feasibility Verified in Phase 3.2: 349 records retrieved, 225 qualifying vegetation fires, schema confirmed; Data Ready Pending Supervisor Review)`.

---

### DS-02: Copernicus Sentinel-2 Multi-Spectral Instrument (MSI)
* **Provider:** European Space Agency (ESA) / European Commission.
* **Canonical URL:** [https://dataspace.copernicus.eu/](https://dataspace.copernicus.eu/)
* **Citation:** Drusch, M., et al. (2012). Sentinel-2: ESA's Optical High-Resolution Mission for GMES Operational Services. *Remote Sensing of Environment*, 120, 25-36.
* **Product Identifier:** `S2MSI2A` (Level-2A Bottom-Of-Atmosphere reflectance).
* **Data Type & Format:** Raster imagery (JPEG2000 / Cloud-Optimized GeoTIFF).
* **Spatial & Temporal Resolution:**
  - Spatial: 10 m (B02, B03, B04, B08), 20 m (B05, B06, B07, B8A, B11, B12), 60 m atmospheric bands.
  - Temporal: 5-day revisit at equator with 2-satellite constellation.
* **Key Bands for Hazards:**
  - Wildfire (NBR / dNBR): Band 8 (NIR, 842 nm) & Band 12 (SWIR-2, 2190 nm).
  - Flood (MNDWI): Band 3 (Green, 560 nm) & Band 11 (SWIR-1, 1610 nm).
  - Vegetation/Drought (NDVI): Band 4 (Red, 665 nm) & Band 8 (NIR, 842 nm).
* **Access Method & Credentials:**
  - Method: Copernicus Data Space Ecosystem (CDSE) OData / S3 OpenSearch API.
  - Credentials: Free CDSE account required for programmatic OAuth2 download tokens.
  - Quotas: Standard concurrency caps (4 parallel downloads per standard account).
* **Licence & Redistribution:** Free, full, and open access under Copernicus Sentinels Data Policy.
* **Storage Footprint & Ingestion Impact:** Raw Level-2A granulate is ~500 MB–1 GB per $100\times 100\text{ km}$ tile. Indiscriminate multi-temporal downloads would exceed disk bounds. Must use spatial bounding boxes, cloud masking filters ($< 20\%$ cloud cover), and targeted band extraction in Phase 4.
* **Operational Verification State:** `Documentation Reviewed — Access Not Tested (Pending Verification in Phase 3)`.

---

### DS-03: Copernicus Sentinel-1 Synthetic Aperture Radar (SAR)
* **Provider:** European Space Agency (ESA) / European Commission.
* **Canonical URL:** [https://dataspace.copernicus.eu/](https://dataspace.copernicus.eu/)
* **Citation:** Torres, R., et al. (2012). GMES Sentinel-1 mission. *Remote Sensing of Environment*, 120, 9-24.
* **Product Identifier:** `S1_GRD` (Level-1 Ground Range Detected, C-band SAR).
* **Data Type & Format:** Raster SAR backscatter intensity (GeoTIFF / SAFE format).
* **Spatial & Temporal Resolution:**
  - Spatial: 10 m pixel spacing (High Resolution IW mode).
  - Temporal: 6–12 days repeat cycle depending on orbital pass.
* **Key Attributes / Schema:** C-band radar backscatter in dual polarization: VV (Vertical-Vertical) and VH (Vertical-Horizontal).
* **Access Method & Credentials:**
  - Method: CDSE OData API / S3 object store.
  - Credentials: Free CDSE user account.
  - Quotas: Same as Sentinel-2 (standard CDSE download queues).
* **Licence & Redistribution:** Open access under Copernicus Sentinels Data Policy.
* **Storage Footprint & Ingestion Impact:** Level-1 GRD products are ~1 GB per scene. Requires calibrated radiometric terrain correction and speckle filtering; ingestion must be strictly restricted to pilot flood event windows.
* **Operational Verification State:** `Documentation Reviewed — Access Not Tested (Pending Verification in Phase 3)`.

---

### DS-04: Copernicus Global Digital Elevation Model (GLO-30)
* **Provider:** European Space Agency (ESA) / Airbus Defence and Space.
* **Canonical URL:** [https://spacedata.copernicus.eu/collections/copernicus-digital-elevation-model](https://spacedata.copernicus.eu/collections/copernicus-digital-elevation-model)
* **Citation:** Copernicus DEM User Handbook (2020), ESA Document.
* **Product Identifier:** `COP-DEM-GLO-30-DGED`.
* **Data Type & Format:** 32-bit floating point elevation raster (Cloud-Optimized GeoTIFF via AWS Public Datasets / OpenTopography API).
* **Spatial & Temporal Resolution:**
  - Spatial: 1 arc-second (~30 m at equator).
  - Temporal: Static baseline (EGM2008 geoid).
* **Tile Distribution Footprint:** Distributed in $1^\circ \times 1^\circ$ geographic tiles. A $2^\circ \times 2^\circ$ pilot region requires **exactly four tiles** (e.g. `N21_E079`, `N21_E080`, `N22_E079`, `N22_E080`).
* **Key Attributes / Derived Features:** Orthometric elevation ($z$ in meters above geoid); used to derive Slope angle, Aspect, Curvature, and Terrain Ruggedness Index aggregated to common analysis grid.
* **Access Method & Credentials:** AWS S3 Public Bucket (`s3://copernicus-dem-30m/`) / OpenTopography API. Open access; no credentials required on AWS bucket.
* **Licence & Redistribution:** Free and open access for research under Copernicus terms.
* **Storage Footprint & Ingestion Impact:** 4 compressed GeoTIFF tiles total ~75–100 MB. Fits easily within workspace bounds.
* **Operational Verification State:** `Candidate Source, not fully verified (Object Availability & COG Header Verified on AWS S3; Full Raster Array Decode Deferred to Phase 4)`.

---

### DS-05: ECMWF ERA5-Land Atmospheric Reanalysis (via Open-Meteo)
* **Provider:** European Centre for Medium-Range Weather Forecasts (ECMWF) / Copernicus Climate Change Service (CDS), served via Open-Meteo Historical API.
* **Canonical URL:** [https://open-meteo.com/en/docs/historical-weather-api](https://open-meteo.com/en/docs/historical-weather-api) & [https://cds.climate.copernicus.eu/](https://cds.climate.copernicus.eu/)
* **Citation:** Hersbach, H., et al. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society*, 146(730), 1999-2049.
* **Product Identifier:** `era5_land` (0.1° atmospheric and land-surface reanalysis).
* **Data Type & Format:** Tabular JSON / CSV / NetCDF.
* **Spatial & Temporal Resolution:**
  - Spatial: Native $0.1^\circ \times 0.1^\circ$ (~9 km at equator).
  - Temporal: Hourly time-series, 1950 to present.
* **Analytical Resolution Alignment Notice:**
  - Reanalysis is sampled to cell centroids on the $0.05^\circ$ common analysis grid via bilinear interpolation.
  - **Important Limitation:** Bilinear interpolation is a geometric sampling convenience; it does **not** create sub-grid physical atmospheric detail or resolve microscale wind channeling.
* **Scientific Status:** This data is a **retrospective historical reanalysis**, not an operational weather forecast.
* **Key Variables:** `temperature_2m` ($^\circ\text{C}$), `relative_humidity_2m` ($\%$), `wind_speed_10m` ($\text{km/h}$), `precipitation` ($\text{mm}$), `surface_pressure` ($\text{hPa}$), `dew_point_2m` ($^\circ\text{C}$).
* **Access Method & Credentials:** RESTful HTTP JSON API. Non-commercial research allows up to 10,000 daily API calls without authentication keys.
* **Licence & Redistribution:** Creative Commons Attribution 4.0 International (CC-BY 4.0) matching ECMWF Copernicus licensing.
* **Storage Footprint & Ingestion Impact:** Hourly aggregates over 3 years for pilot centroid points total ~15–30 MB in JSON.
* **Operational Verification State:** `Candidate Source, not fully verified (Empirically Verified in Phase 3.2: 504/504 hrs continuous, 0 missing timestamps, 0.00% missing values; Full Pipeline Ingestion Deferred to Phase 4)`.

---

### DS-06: NASA Global Landslide Catalog (GLC)
* **Provider:** NASA Goddard Space Flight Center.
* **Canonical URL:** [https://data.nasa.gov/Earth-Science/Global-Landslide-Catalog-Export/dd9e-wu2v](https://data.nasa.gov/Earth-Science/Global-Landslide-Catalog-Export/dd9e-wu2v)
* **Citation:** Kirschbaum, D. B., et al. (2010). A global landslide catalog for hazard applications. *Natural Hazards*, 52(3), 561-575.
* **Product Identifier:** `NASA_GLC_Export`.
* **Data Type & Format:** Tabular / point vector (CSV / GeoJSON).
* **Spatial & Temporal Resolution:**
  - Spatial: Point coordinates with spatial accuracy radius estimate.
  - Temporal: Event records spanning 2007–2017 (discontinued for active updates; historical benchmark only).
* **Key Attributes / Schema:** `event_date`, `latitude`, `longitude`, `landslide_category`, `landslide_trigger` (e.g. `rain`, `downpour`), `location_accuracy`, `fatalities`.
* **Access Method & Credentials:** Direct open HTTP download from data.nasa.gov. No token required.
* **Licence & Redistribution:** NASA Public Domain / CC0.
* **Storage Footprint & Ingestion Impact:** Very small (~10 MB).
* **Operational Verification State:** `Documentation Reviewed — Access Not Tested (Pending Verification in Phase 3)`.

---

### DS-07: NOAA NCEI IBTrACS (Tropical Cyclone Best Track Archive)
* **Provider:** NOAA National Centers for Environmental Information (NCEI).
* **Canonical URL:** [https://www.ncei.noaa.gov/products/international-best-track-archive](https://www.ncei.noaa.gov/products/international-best-track-archive)
* **Citation:** Knapp, K. R., et al. (2010). The International Best Track Archive for Climate Stewardship (IBTrACS). *Bulletin of the American Meteorological Society*, 91(3), 363-376.
* **Product Identifier:** `IBTrACS.v04r00`.
* **Data Type & Format:** Tabular NetCDF / CSV / GeoJSON.
* **Spatial & Temporal Resolution:**
  - Spatial: Storm center coordinates ($0.1^\circ$ precision).
  - Temporal: 3-hourly / 6-hourly storm fixes (1851 to present).
* **Key Attributes / Schema:** `SID`, `NAME`, `ISO_TIME`, `LAT`, `LON`, `WMO_WIND`, `WMO_PRES`, `DIST2LAND`, `STORM_SPEED`, `STORM_DIR`.
* **Access Method & Credentials:** Direct open HTTP / FTP download. No authentication required.
* **Licence & Redistribution:** US Government Public Domain / Open Data.
* **Storage Footprint & Ingestion Impact:** ~150 MB for the entire global historical archive in CSV.
* **Operational Verification State:** `Documentation Reviewed — Access Not Tested (Pending Verification in Phase 3)`.

---

### DS-08: Copernicus Sentinel-5P TROPOMI $\text{SO}_2$ Product
* **Provider:** European Space Agency (ESA) / Royal Netherlands Meteorological Institute (KNMI).
* **Canonical URL:** [https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-5p](https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-5p)
* **Citation:** Theys, C., et al. (2017). Sulfur dioxide retrievals from TROPOMI onboard Sentinel-5 Precursor. *Atmospheric Measurement Techniques*, 10(1), 119-153.
* **Product Identifier:** `L2__SO2___`.
* **Data Type & Format:** Swath NetCDF-4 product.
* **Spatial & Temporal Resolution:**
  - Spatial: $3.5\text{ km} \times 5.5\text{ km}$ at nadir.
  - Temporal: Daily global overpass.
* **Key Attributes / Schema:** `sulfurdioxide_total_vertical_column` (mol/m$^2$ and Dobson Units), `qa_value` (quality assurance flag, recommended $> 0.5$).
* **Access Method & Credentials:** CDSE OData API / S3 store. Requires free CDSE account.
* **Licence & Redistribution:** Open access under Copernicus Sentinels Data Policy.
* **Storage Footprint & Ingestion Impact:** ~500 MB per orbit file. Ingestion requires bounding to volcanic calderas.
* **Operational Verification State:** `Documentation Reviewed — Access Not Tested (Pending Verification in Phase 3)`.

---

## 2. Ingestion Feasibility Assessment Summary

| Dataset ID | Candidate Hazard | Primary Data Provider | Licencing Status | Quota / Token Required | Storage Impact per Bounded Pilot | Ingestion Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DS-01** (FIRMS) | `wildfire` | NASA ESDIS | Open (NASA) | Free `MAP_KEY` | Minimal (<100 MB) | Low (Tabular CSV/JSON) |
| **DS-02** (Sentinel-2) | `wildfire`, `flood` | ESA / Copernicus | Open (Copernicus) | Free CDSE Account | Medium (1–5 GB clipped) | Medium (Raster GeoTIFF / Bounding) |
| **DS-03** (Sentinel-1) | `flood` | ESA / Copernicus | Open (Copernicus) | Free CDSE Account | Medium (1–5 GB clipped) | High (SAR calibration, speckle filter) |
| **DS-04** (GLO-30 DEM) | All Hazards | ESA / Airbus | Open (Copernicus) | Open AWS / Free Token | Low (<200 MB) | Low (Static GeoTIFF) |
| **DS-05** (ERA5 / Meteo) | All Hazards | ECMWF / CDS | Open (Copernicus) | Free CDS Key / Open-Meteo | Low (<500 MB) | Medium (NetCDF slicing / JSON) |
| **DS-06** (NASA GLC) | `landslide` | NASA GSFC | Open (NASA Public Domain) | None | Minimal (<20 MB) | Low (Tabular CSV) |
| **DS-07** (IBTrACS) | `cyclone` | NOAA NCEI | Open (US Public Domain) | None | Minimal (<150 MB) | Low (Tabular CSV/NetCDF) |
| **DS-08** (TROPOMI) | `volcanic_activity` | ESA / KNMI | Open (Copernicus) | Free CDSE Account | Medium (1–2 GB) | Medium (NetCDF swath raster) |
