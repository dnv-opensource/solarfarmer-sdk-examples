Notebooks for the DNV Digital bankability: Bankable yield modelling in your Python workflows — June 3rd 2026.

## Contents

| Notebook | Title | What it covers |
|----------|-------|----------------|
| [`01_multisite_SF_workflow2.ipynb`](01_multisite_SF_workflow2.ipynb) | Multi-site yield assessment — Workflow 2 | Load a portfolio of 5 US sites from CSV, fetch Solcast TMY in parallel, build `PVSystem` objects using SolarFarmer SDK Workflow 2, run energy calculations in parallel, and compare performance metrics |

## Environment Setup

Requires **Python 3.11+**. A `pyproject.toml` with all dependencies is included.

```bash
cd "WebinarJune2026"
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install .
```

Then select the `.venv` kernel in VS Code before running the notebook.

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
