import React, { useEffect, useState } from 'react';
import { 
  ShieldAlert, 
  Activity, 
  Satellite, 
  Flame, 
  Droplets, 
  Mountain, 
  Sun, 
  Wind, 
  CloudLightning, 
  MountainSnow, 
  AlertTriangle,
  CheckCircle2,
  XCircle,
  Clock
} from 'lucide-react';
import { checkBackendHealth } from './services/api';
import { HealthResponse } from './types/health';

interface HazardInfo {
  id: string;
  name: string;
  icon: React.ReactNode;
  category: 'Tier 1 (Pilot)' | 'Tier 2 (Secondary)' | 'Tier 3 (Stretch)';
  taskType: string;
  status: string;
}

const IN_SCOPE_HAZARDS: HazardInfo[] = [
  { id: 'flood', name: 'Flood', icon: <Droplets className="w-5 h-5 text-blue-400" />, category: 'Tier 1 (Pilot)', taskType: 'Susceptibility & SAR Inundation', status: 'Planned (Phase 4 Ingestion)' },
  { id: 'wildfire', name: 'Wildfire', icon: <Flame className="w-5 h-5 text-orange-400" />, category: 'Tier 1 (Pilot)', taskType: 'Danger Rating & Burn Severity', status: 'Planned (Phase 4 Ingestion)' },
  { id: 'landslide', name: 'Landslide', icon: <Mountain className="w-5 h-5 text-amber-400" />, category: 'Tier 2 (Secondary)', taskType: 'Susceptibility & Rainfall Triggers', status: 'Planned (Secondary)' },
  { id: 'drought', name: 'Drought', icon: <Sun className="w-5 h-5 text-yellow-400" />, category: 'Tier 2 (Secondary)', taskType: 'Multi-Index Anomaly Monitoring', status: 'Planned (Secondary)' },
  { id: 'cyclone', name: 'Cyclone', icon: <Wind className="w-5 h-5 text-teal-400" />, category: 'Tier 3 (Stretch)', taskType: 'Intensity & Track Displacement', status: 'Research Required' },
  { id: 'severe_storm', name: 'Severe Storm', icon: <CloudLightning className="w-5 h-5 text-purple-400" />, category: 'Tier 3 (Stretch)', taskType: 'Convective Initiation Nowcasting', status: 'Research Required' },
  { id: 'volcanic_activity', name: 'Volcanic Activity', icon: <AlertTriangle className="w-5 h-5 text-red-400" />, category: 'Tier 3 (Stretch)', taskType: 'Thermal & SO2 Monitoring', status: 'Research Required' },
  { id: 'avalanche', name: 'Avalanche', icon: <MountainSnow className="w-5 h-5 text-cyan-400" />, category: 'Tier 3 (Stretch)', taskType: 'Terrain Exposure Assessment', status: 'Deferred Pending Data' },
];

const EXCLUDED_DISASTERS = [
  { name: 'Earthquakes', reason: 'Solid-earth tectonic slip is unpredictable in lead-times via satellite imaging' },
  { name: 'Tsunamis', reason: 'Deep-ocean hydrodynamics require DART sensor buoys, outside Earth observation' },
  { name: 'Chemical / Industrial Disasters', reason: 'Point-source technological incidents require facility SCADA telemetry' },
  { name: 'Terrorist Attacks & Conflict', reason: 'Anthropogenic security events fall outside physical Earth observation' },
];

export const App: React.FC = () => {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthLoading, setHealthLoading] = useState<boolean>(true);
  const [healthError, setHealthError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    checkBackendHealth()
      .then((data) => {
        if (isMounted) {
          setHealth(data);
          setHealthLoading(false);
        }
      })
      .catch((err: Error) => {
        if (isMounted) {
          setHealthError(err.message);
          setHealthLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="flex flex-col min-h-screen bg-slate-950 text-slate-100">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex flex-wrap justify-between items-center gap-4">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-sky-500/10 border border-sky-500/20 rounded-lg">
              <Satellite className="w-6 h-6 text-sky-400" />
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight text-white sm:text-xl">
                Satellite Multi-Hazard Early Warning System
              </h1>
              <p className="text-xs text-slate-400">
                Phase 1 Engineering Baseline &bull; B.Tech CSE Major Project
              </p>
            </div>
          </div>

          {/* Backend Connection Indicator */}
          <div className="flex items-center space-x-2 text-xs">
            <span className="text-slate-400">Backend Status:</span>
            {healthLoading && (
              <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-amber-500/10 text-amber-300 border border-amber-500/30">
                <Clock className="w-3 h-3 mr-1 animate-spin" /> Checking...
              </span>
            )}
            {!healthLoading && health && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                <CheckCircle2 className="w-3 h-3 mr-1" /> API Online (v{health.version})
              </span>
            )}
            {!healthLoading && healthError && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-rose-500/10 text-rose-400 border border-rose-500/30" title={healthError}>
                <XCircle className="w-3 h-3 mr-1" /> API Disconnected
              </span>
            )}
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Academic Safety Banner */}
        <section aria-labelledby="safety-notice" className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-4 sm:p-5">
          <div className="flex items-start space-x-3">
            <ShieldAlert className="w-6 h-6 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <h2 id="safety-notice" className="text-sm font-semibold text-amber-200">
                Experimental Research System — Non-Operational Notice
              </h2>
              <p className="text-xs text-amber-300/90 mt-1 leading-relaxed">
                This software is developed strictly for research, academic evaluation, and demonstration purposes as part of a final-year B.Tech capstone project. 
                It is <strong>not</strong> an active disaster dispatch service and must never be used as a substitute for official warnings issued by national disaster authorities (NDMA, IMD, NOAA, ECMWF, USGS).
              </p>
            </div>
          </div>
        </section>

        {/* Dashboard Shell Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Map & GIS Viewport Placeholder */}
          <section aria-labelledby="map-viewport" className="lg:col-span-2 rounded-xl border border-slate-800 bg-slate-900/50 p-6 flex flex-col justify-between min-h-[420px]">
            <div>
              <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
                <div className="flex items-center space-x-2">
                  <Activity className="w-5 h-5 text-sky-400" />
                  <h2 id="map-viewport" className="font-semibold text-slate-200">Interactive GIS Map Viewport</h2>
                </div>
                <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">
                  Planned for Phase 8
                </span>
              </div>
              <p className="text-sm text-slate-400 leading-relaxed">
                The interactive map canvas (Leaflet / MapLibre) will be integrated in Phase 8 to visualize multi-hazard geospatial raster overlays, SAR flood inundation contours, active fire hotspots, and terrain slope hazard zones.
              </p>
            </div>

            {/* Scientific Safeguard Notice: No Fake Maps */}
            <div className="my-auto py-12 px-4 text-center rounded-lg border border-dashed border-slate-800 bg-slate-950/40">
              <Satellite className="w-12 h-12 text-slate-600 mx-auto mb-3" />
              <h3 className="text-sm font-medium text-slate-300">No Mock Geospatial Predictions Displayed</h3>
              <p className="text-xs text-slate-500 max-w-md mx-auto mt-1">
                Per project rule #9, placeholder or fabricated hazard predictions are strictly prohibited. Genuine satellite observations will be rendered upon Phase 4 data pipeline completion.
              </p>
            </div>

            <div className="border-t border-slate-800 pt-4 text-xs text-slate-500 flex justify-between items-center">
              <span>Coordinate Reference: EPSG:4326 (WGS 84)</span>
              <span>Layer Ingestion: Phase 4</span>
            </div>
          </section>

          {/* System Baseline & Backend Diagnostic Card */}
          <section aria-labelledby="system-diagnostic" className="rounded-xl border border-slate-800 bg-slate-900/50 p-6 flex flex-col justify-between">
            <div>
              <div className="flex items-center space-x-2 border-b border-slate-800 pb-4 mb-4">
                <Activity className="w-5 h-5 text-emerald-400" />
                <h2 id="system-diagnostic" className="font-semibold text-slate-200">System Diagnostic</h2>
              </div>

              <div className="space-y-4 text-xs">
                <div>
                  <span className="text-slate-400">Current Phase:</span>
                  <div className="font-mono text-slate-200 font-medium mt-0.5">
                    Phase 1.2 — Engineering Baseline
                  </div>
                </div>

                <div>
                  <span className="text-slate-400">FastAPI Health Service:</span>
                  <div className="font-mono text-slate-200 mt-0.5 p-2 rounded bg-slate-950/60 border border-slate-800">
                    {healthLoading && <span className="text-amber-400">Querying /health endpoint...</span>}
                    {!healthLoading && health && (
                      <div className="space-y-1">
                        <div><span className="text-slate-500">Status:</span> <span className="text-emerald-400">{health.status}</span></div>
                        <div><span className="text-slate-500">Version:</span> {health.version}</div>
                        <div><span className="text-slate-500">Env:</span> {health.environment}</div>
                        <div><span className="text-slate-500">Timestamp:</span> {health.timestamp}</div>
                      </div>
                    )}
                    {!healthLoading && healthError && (
                      <span className="text-rose-400">Error: {healthError}</span>
                    )}
                  </div>
                </div>

                <div>
                  <span className="text-slate-400">Phase 0 Governance Baseline:</span>
                  <div className="font-mono text-emerald-400 mt-0.5">
                    PASS WITH LIMITATIONS
                  </div>
                </div>

                <div>
                  <span className="text-slate-400">Supervisor Review State:</span>
                  <div className="font-mono text-amber-400 mt-0.5">
                    PENDING_SUPERVISOR_REVIEW
                  </div>
                </div>
              </div>
            </div>

            <div className="border-t border-slate-800 pt-4 mt-6 text-xs text-slate-500">
              API Contract: <code className="text-slate-400">GET /health</code> verified
            </div>
          </section>
        </div>

        {/* In-Scope Hazard Matrix Section */}
        <section aria-labelledby="hazard-scope">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 id="hazard-scope" className="text-lg font-bold text-white">In-Scope Hazard Architecture (8 Hazards)</h2>
              <p className="text-xs text-slate-400">Grounded task definitions established in Phase 0 governance charter</p>
            </div>
            <span className="text-xs text-slate-400 font-mono">docs/hazard-task-definitions.md</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {IN_SCOPE_HAZARDS.map((hazard) => (
              <div key={hazard.id} className="p-4 rounded-xl border border-slate-800 bg-slate-900/40 hover:border-slate-700 transition-colors">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    {hazard.icon}
                    <h3 className="font-medium text-sm text-slate-200">{hazard.name}</h3>
                  </div>
                  <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">
                    {hazard.id}
                  </span>
                </div>
                <p className="text-xs text-slate-400 mb-2">{hazard.taskType}</p>
                <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px]">
                  <span className="text-sky-400 font-mono text-[10px]">{hazard.category}</span>
                  <span className="text-slate-500 font-mono text-[10px]">{hazard.status}</span>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Exclusions Section */}
        <section aria-labelledby="excluded-scope" className="rounded-xl border border-slate-800/80 bg-slate-900/30 p-5">
          <h2 id="excluded-scope" className="text-sm font-semibold text-slate-300 mb-2">
            Explicit Disaster Exclusions (Out of Scope)
          </h2>
          <p className="text-xs text-slate-400 mb-3">
            In accordance with Phase 0 governance rules, the following categories are strictly excluded from all project phases:
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
            {EXCLUDED_DISASTERS.map((excl) => (
              <div key={excl.name} className="p-3 rounded-lg bg-slate-950/40 border border-slate-800/60">
                <span className="font-semibold text-rose-400 block mb-1">{excl.name}</span>
                <span className="text-slate-500 text-[11px] leading-tight block">{excl.reason}</span>
              </div>
            ))}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-slate-950 py-6 mt-12 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4">
          Satellite-Based Multi-Hazard Disaster Risk Prediction System &bull; Final-Year Major Project &bull; CSE
        </div>
      </footer>
    </div>
  );
};
