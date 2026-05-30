# Operational Demo — Presenter Narration Script

**Format:** ~2-minute screen recording, manual cell-by-cell execution, with live voice-over.  
**Audience:** PV simulation practitioners who already saw the first demo (design + GCR sweep). Now we show how the same physics engine extends into operations.  
**Goals:** Demonstrate that a single exported 3D model serves both financing and monitoring; show a concrete soiling-detection workflow driven by satellite precipitation.  
**Pacing:** API calls (3× ~50s each) should be cut to ~3–4s in post with a fast-forward indicator. Total narrated runtime ≈ 2:00.

---

## [0:00–0:08] Title cell visible, run imports cell

> In the first demo we designed a plant from scratch and optimised GCR. Now we take an existing bankable 3D model — already signed off for financing — and reuse it unchanged for operational monitoring. Same physics, different weather.

*[Run imports cell. Completes in ~2s.]*

---

## [0:08–0:18] 3D Model markdown + site setup cell

> This model was designed in SolarFarmer Desktop — trackers, slope-aware backtracking, string-level wiring — and exported as a single JSON file. That file is our reusable artifact.

*[Scroll past the layout image. Run site setup cell — prints location and folder.]*

---

## [0:18–0:30] Phase 1 — TMY fetch + energy calculation

> Phase one: establish the financing baseline. We pull TMY data from Solcast, convert it to SolarFarmer's weather format, and submit. This is the P50 number the project is built around.

*[Run TMY fetch cell, then TMY energy calc cell. Cut API wait to ~3s. Annual yield prints.]*

---

## [0:30–0:45] Phase 2 — Historic fetch + energy calculation

> Phase two: swap the weather. Same model, same equipment files — only the meteorological input changes. We pull hourly satellite actuals from January 2026 to today, and resubmit.

*[Run historic fetch cell, then historic energy calc cell. Cut API wait to ~3s.]*

> Now we have two energy timeseries from the same 3D model. One tells us what the plant *should* produce given typical weather; the other tells us what it *should* produce given the weather it actually received.

---

## [0:45–1:00] Performance Indices — compute + plot

> We decompose performance weekly. PII isolates weather — was irradiance above or below TMY? PIE captures total energy deviation. And WA-PIE factors out the weather, leaving only the plant's own behaviour.

*[Run PI computation cell, then root-cause chart cell. Pause ~3s on the 3-panel chart.]*

> Green bars above the line: the plant is outperforming. Red bars below: something is off — and WA-PIE tells you whether it's weather or the plant itself.

---

## [1:00–1:15] Phase 3 — Soiling from precipitation

> Phase three: we introduce soiling. Solcast gives us hourly precipitation rate. We feed that into pvlib's Kimber model — a simple ramp-and-reset soiling profile — and inject the result as a per-timestep loss column in the weather file. One more API call with the soiled weather.

*[Run soiling computation cell. Pause ~2s on precip/soiling chart. Run soiled energy calc cell — cut to ~3s.]*

---

## [1:15–1:35] Three-Signal Comparison

> Three signals from one model. TMY baseline in navy, clean actuals in blue, soiled actuals in green. The gap between expected and soiled is the actionable underperformance — the signal a monitoring system should flag.

*[Run three-signal chart cell. Pause ~4s on the chart.]*

> The bottom panel shows the ratio week by week. When it dips below the threshold, you know soiling is the cause — not weather, not equipment degradation.

---

## [1:35–1:55] Cumulative Revenue & Cleaning ROI

> Finally, we quantify the business case. Cumulative energy loss converts to revenue at the PPA rate. The orange line is the cleaning cost. When cumulative loss crosses it, cleaning pays for itself.

*[Run revenue/ROI cell. Pause ~4s on the chart.]*

> At this site — Fort Peck, Montana — there's enough rainfall that soiling losses stay small. The model correctly tells you: don't spend money cleaning when the physics don't justify it. That's a decision backed by the same engine your financing was built on.

---

## [1:55–2:00] Summary cell visible

> One 3D model. Three simulations. From bankable P50 to soiling ROI — by swapping only the weather file.

---

## Tips for Recording

- **Execution:** Run cells manually with `Shift+Enter`. Do not pre-run.
- **Pre-warm:** Run imports once before recording to cache dependencies, then restart and clear all outputs.
- **API calls:** Three energy calculations (~50s each). Cut each to 3–4s in post with a ⏩ badge.
- **Pause points:** ~3s on root-cause decomposition, ~4s on three-signal chart, ~4s on cumulative revenue chart.
- **Resolution:** 1920×1080+, 125% zoom, light Jupyter theme.
- **Continuity with first demo:** If presented back-to-back, the transition is: "In the first demo we designed from scratch. Now we take an existing model into operations."
