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
* **Product Identifier:** `VNP14IMGTDL` (NRT VIIRS 375m) / `MCD14DL` (MODIS 1km).
* **Data Type & Format:** Tabular vector point data (CSV, GeoJSON, SHP).
* **Spatial & Temporal Resolution:**
  - Spatial: 375 m pixel footprint (VIIRS I-Band) / 1 km (MODIS).
  - Temporal: 3–12 hour latency; daily global coverage.
* **Key Attributes / Schema:** `latitude`, `longitude`, `bright_ti4` (brightness temperature I-4), `scan`, `track`, `acq_date`, `acq_time`, `satellite`, `confidence` (`low`, `nominal`, `high` or numeric $0\text{--}100$), `frp` (Fire Radiative Power, MW), `daynight`.
* **Access Method & Credentials:**
  - Method: RESTful HTTP API / Earthdata Download.
  - Credentials: Free NASA Earthdata account; `MAP_KEY` required for transactional API queries.
  - Rate Limits: Up to 5,000 transactions/day per key (Standard FIRMS API).
* **Licence & Redistribution:** NASA Open Data Policy (Free and open global distribution for research and operational use, with attribution).
* **Storage Footprint & Ingestion Impact:** Very lightweight (~50–100 MB per annual regional pilot extract in CSV). Safe for local disk bounds.
* **Operational Verification State:** `Documentation Reviewed — Access Not Tested (Pending Verification in Phase 3)`.

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
* **Provider:** European Space Agency (ESA) / Airbus.
* **Canonical URL:** [https://spacedata.copernicus.eu/collections/copernicus-digital-elevation-model](https://spacedata.copernicus.eu/collections/copernicus-digital-elevation-model)
* **Citation:** Copernicus DEM User Handbook (2020), ESA Document.
* **Product Identifier:** `COP-DEM-GLO-30-DGED`.
* **Data Type & Format:** 32-bit floating point elevation raster (GeoTIFF / Cloud-Optimized GeoTIFF via OpenTopography / AWS Public Datasets).
* **Spatial & Temporal Resolution:**
  - Spatial: 30 m (1 arc-second).
  - Temporal: Static baseline.
* **Key Attributes / Derived Features:** Orthometric elevation ($z$ in meters above EGM2008 geoid); used to compute Slope, Aspect, Topographic Wetness Index (TWI), and Curvature.
* **Access Method & Credentials:**
  - Method: AWS S3 Public Bucket (`s3://copernicus-dem-30m/`) / OpenTopography API.
  - Credentials: Open on AWS; API key for OpenTopography.
* **Licence & Redistribution:** Free and open access for research and commercial applications under Copernicus terms.
* **Storage Footprint & Ingestion Impact:** Static regional pilot tile is ~50–150 MB. Fits easily within workspace storage.
* **Operational Verification State:** `Documentation Reviewed — Access Not Tested (Pending Verification in Phase 3)`.

---

### DS-05: ECMWF ERA5 & ERA5-Land Atmospheric Reanalysis
* **Provider:** European Centre for Medium-Range Weather Forecasts (ECMWF) / Copernicus Climate Change Service (CDS).
* **Canonical URL:** [https://cds.climate.copernicus.eu/](https://cds.climate.copernicus.eu/)
* **Citation:** Hersbach, H., et al. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society*, 146(730), 1999-2049.
* **Product Identifier:** `reanalysis-era5-single-levels` / `reanalysis-era5-land`.
* **Data Type & Format:** Gridded multidimensional multidataset (NetCDF / GRIB).
* **Spatial & Temporal Resolution:**
  - Spatial: $0.25^\circ \times 0.25^\circ$ (~31 km, ERA5) / $0.1^\circ \times 0.1^\circ$ (~9 km, ERA5-Land).
  - Temporal: Hourly, 1950 to present (latency ~5 days).
* **Key Variables:** `2m_temperature`, `10m_u_component_of_wind`, `10m_v_component_of_wind`, `2m_dewpoint_temperature` (for Relative Humidity), `total_precipitation`, `volumetric_soil_water_layer_1`.
* **Access Method & Credentials:**
  - Method: CDS API (`cdsapi` Python package).
  - Credentials: Free CDS account; API UID and API key in `~/.cdsapirc`.
  - Quotas: Queued asynchronous processing. Processing queues can experience delays of minutes to hours during high load.
* **Licence & Redistribution:** Copernicus Climate Change Service Licence (Free open access for all uses with attribution).
* **Storage Footprint & Ingestion Impact:** NetCDF regional time-series extracts over 1–2 years are ~200–500 MB. Ingestion must use targeted bounding box subsets. Alternatively, Open-Meteo Historical Weather API (which mirrors ERA5) provides synchronous JSON REST queries for rapid pilot prototyping.
* **Operational Verification State:** `Documentation Reviewed — Access Not Tested (Pending Verification in Phase 3)`.

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
