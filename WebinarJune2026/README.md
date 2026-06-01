Notebooks for the **DNV Webinar: Bankable yield modelling in your Python workflows** — June 3rd 2026.

## Contents

| Notebook | Title | What it covers |
|----------|-------|----------------|
| [`demo_solarfarmer.ipynb`](demo_solarfarmer.ipynb) | SolarFarmer SDK in 90 seconds | Design a 10 MW tracker plant from high-level intent, run a bankable energy calculation, visualise monthly energy & PR, sweep GCR for LCOE optimisation |
| [`demo_multiyear_resource.ipynb`](demo_multiyear_resource.ipynb) | Multi-year resource & energy variability | Fetch Solcast TMY + 19 years of historic satellite weather, run all years through SolarFarmer in parallel, derive P50/P75/P90 exceedance and inter-annual variability |
| [`demo_operational.ipynb`](demo_operational.ipynb) | From pro forma to operations | Reuse the same SolarFarmer 3D model for TMY baseline and satellite-actual simulations; compute weekly PII/PIE/WA-PIE; apply pvlib Kimber soiling from precipitation; quantify cleaning ROI |
| [`demo_multisite_portfolio.ipynb`](demo_multisite_portfolio.ipynb) | Multi-site portfolio assessment | Load a 5-site US West Coast portfolio from CSV, fetch Solcast TMY in parallel, instantiate `PVSystem` objects, run energy calculations in parallel, compare PR / specific yield / monthly profiles |

## Environment Setup

Requires **Python 3.11+**. All dependencies are listed in `pyproject.toml` and `environment.yml`.

### Option A — conda

```bash
cd WebinarJune2026
conda env create -f environment.yml
conda activate webinar-june-2026-dnv-apis
jupyter lab
```

### Option B — pip / venv

```bash
cd WebinarJune2026
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install .
```

Then select the `.venv` (or conda) kernel in VS Code before running the notebooks.

## API Keys

| Variable | Where to get it |
|----------|-----------------|
| `SOLCAST_API_KEY` | [toolkit.solcast.com.au/register](https://toolkit.solcast.com.au/register) |
| `SF_API_KEY` | Retrieved from [solarfarmer.dnv.com](https://solarfarmer.dnv.com/) after being requested |

```powershell
# Windows (PowerShell)
$env:SOLCAST_API_KEY = "your-key"
$env:SF_API_KEY      = "your-key"
```

## Equipment Files

The notebook reuses the PAN and OND equipment files from `../PVPMC2026/equipment/`.
No separate equipment folder is required.

## Contact

For questions or to request access to API tokens, contact the DNV team at [solarfarmer@dnv.com](mailto:solarfarmer@dnv.com).
