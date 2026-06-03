# solarfarmer-sdk-examples

Runnable Jupyter notebooks demonstrating end-to-end PV energy yield workflows using
the [SolarFarmer Python SDK](https://dnv-opensource.github.io/solarfarmer-python-sdk/),
the [Solcast Python SDK](https://solcast.github.io/solcast-api-python-sdk/), and the
[DNV Solar Resource Compass API](https://api.src.dnv.com/).

Each subfolder corresponds to a specific event or workshop. More are added over time.

---

## Contents

| Folder | Event | Date |
|--------|-------|------|
| [`PVPMC2026/`](PVPMC2026/) | PVPMC USA Workshop, Albuquerque NM | May 2026 |
| [`WebinarJune2026/`](WebinarJune2026/) | DNV Webinar — Bankable yield modelling in your Python workflows | June 2026 |

---

## Webinar June 2026

Four notebooks from the **DNV Webinar: Bankable yield modelling in your Python workflows** (June 3rd 2026).
Covers single-plant design, GCR optimisation, multi-year resource variability, operational monitoring, and multi-site portfolio assessment — all using the SolarFarmer SDK and Solcast satellite weather.

| Notebook | Title | What it covers |
|----------|-------|----------------|
| [`demo_solarfarmer.ipynb`](WebinarJune2026/demo_solarfarmer.ipynb) | SolarFarmer SDK in 90 seconds | Design a 10 MW tracker plant, run a bankable energy calculation, visualise monthly energy & PR, sweep GCR for LCOE optimisation |
| [`demo_multiyear_resource.ipynb`](WebinarJune2026/demo_multiyear_resource.ipynb) | Multi-year resource & energy variability | Solcast TMY + 19 years of historic data, parallel SolarFarmer runs, P50/P75/P90 exceedance, inter-annual variability |
| [`demo_operational.ipynb`](WebinarJune2026/demo_operational.ipynb) | From pro forma to operations | Reuse a SolarFarmer 3D model for TMY baseline and satellite-actual simulations; weekly PII/PIE/WA-PIE decomposition; pvlib Kimber soiling from precipitation; cleaning ROI |
| [`demo_multisite_portfolio.ipynb`](WebinarJune2026/demo_multisite_portfolio.ipynb) | Multi-site portfolio assessment | 5-site US West Coast portfolio from CSV; parallel Solcast TMY fetch; `PVSystem` (Workflow 2); parallel energy calculations; PR / specific yield / monthly profiles |

---

## PVPMC2026

Five notebooks presented at the **PVPMC USA 2026 Workshop** in Albuquerque, New Mexico.
They form a progression from raw resource data retrieval through to multi-year energy yield analysis.

| Notebook | Title | What it covers |
|----------|-------|----------------|
| [`01_solcast.ipynb`](PVPMC2026/01_solcast.ipynb) | Solcast API | TMY, historic, live and forecast irradiance & weather retrieval via the Solcast SDK |
| [`02_solar_resource_compass.ipynb`](PVPMC2026/02_solar_resource_compass.ipynb) | DNV Solar Resource Compass | Multi-source irradiance comparison, monthly soiling profiles, and ground albedo via the SRC API |
| [`03_solarfarmer.ipynb`](PVPMC2026/03_solarfarmer.ipynb) | SolarFarmer API — PVSystem builder | Build a 10 MW tracker plant from scratch, run an energy yield calculation, and sweep GCR for LCOE optimisation |
| [`04_operational_SF3d.ipynb`](PVPMC2026/04_operational_SF3d.ipynb) | Operational: Live + Forecast → SolarFarmer | Pull Solcast live observations and short-range forecasts, convert to a SolarFarmer weather file, and run a near-real-time energy calculation |
| [`05_solcast_solarfarmer_multiyear.ipynb`](PVPMC2026/05_solcast_solarfarmer_multiyear.ipynb) | Multi-year yield variability | Fetch 19 years of Solcast historic data, apply pvlib Kimber soiling, run each year through SolarFarmer in parallel, and analyse P50/P90 exceedance |

---

## Prerequisites

### API keys

All notebooks require at least one API key set as an environment variable before running.

| Variable | Where to get it |
|----------|-----------------|
| `SOLCAST_API_KEY` | [toolkit.solcast.com.au/register](https://toolkit.solcast.com.au/register) | 
| `SRC_API_KEY` | Issued by DNV on request |
| `SF_API_KEY` | Retrieved from [solarfarmer.dnv.com](https://solarfarmer.dnv.com/) after being requested |

Set them in your shell before launching Jupyter:

```bash
# Linux / macOS
export SOLCAST_API_KEY=your-key
export SRC_API_KEY=your-key
export SF_API_KEY=your-key

# Windows (Command Prompt)
set SOLCAST_API_KEY=your-key
set SRC_API_KEY=your-key
set SF_API_KEY=your-key

# Windows (PowerShell)
$env:SOLCAST_API_KEY = "your-key"
$env:SRC_API_KEY     = "your-key"
$env:SF_API_KEY      = "your-key"
```

---

## Setup

Requires **Python 3.11+**. Each event folder contains its own `pyproject.toml` (and, where available, an `environment.yml`) listing all dependencies. Install from whichever folder you want to run.

The examples below use `PVPMC2026/`; substitute `WebinarJune2026/` (or any other folder) to install for a different event.

### Option A — conda (recommended, where environment.yml is provided)

```bash
cd PVPMC2026
conda env create -f environment.yml
conda activate pvpmc-usa-2026-dnv-apis
jupyter lab
```

### Option B — uv

```bash
cd PVPMC2026
uv sync              # reads pyproject.toml and uv.lock
jupyter lab
```

### Option C — pip / venv

```bash
cd PVPMC2026          # or WebinarJune2026, etc.
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install .        # reads pyproject.toml
jupyter lab
```

---

## Repository structure

```
solarfarmer-sdk-examples/
├── README.md
├── PVPMC2026/
│   ├── environment.yml
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── solar_resource_compass.py     # SRC API helper
│   ├── 01_solcast.ipynb
│   ├── 02_solar_resource_compass.ipynb
│   ├── 03_solarfarmer.ipynb
│   ├── 04_operational_SF3d.ipynb
│   ├── 05_solcast_solarfarmer_multiyear.ipynb
│   ├── equipment/                    # PAN / OND files for notebooks 03–05
│   └── operational_usecase/          # SolarFarmer Workflow 1 API input files
└── WebinarJune2026/
    ├── pyproject.toml
    ├── environment.yml
    ├── sites.csv                     # 5-site portfolio definition
    ├── demo_solarfarmer.ipynb        # Single-plant design, GCR optimisation
    ├── demo_multiyear_resource.ipynb # Multi-year variability & P50/P90
    ├── demo_operational.ipynb        # Operational monitoring & soiling ROI
    ├── demo_multisite_portfolio.ipynb  # Multi-site portfolio
    ├── equipment/                    # PAN / OND files (symlinked from PVPMC2026)
    └── weather/                      # Cached Solcast TMY TSV files
```

---

## Key dependencies

| Package | Purpose |
|---------|---------|
| [`solcast`](https://solcast.github.io/solcast-api-python-sdk/) | Solcast TMY, historic, live and forecast endpoints |
| [`dnv-solarfarmer`](https://dnv-opensource.github.io/solarfarmer-python-sdk/) | SolarFarmer energy yield API |
| [`pvlib`](https://pvlib-python.readthedocs.io/) | Soiling model (Kimber) and irradiance utilities |
| `pandas`, `matplotlib` | Data manipulation and visualisation |

---

## Contact

For questions or to request access to API tokens, contact the DNV team at [solarfarmer@dnv.com](mailto:solarfarmer@dnv.com).

---

## License

See [LICENSE](LICENSE).
