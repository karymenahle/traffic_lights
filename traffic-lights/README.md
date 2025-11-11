# Traffic Lights – 4 Intersections (Decision-Making Under Uncertainty)

A simple Python simulator for a 2x2 grid (4 intersections) traffic-light system with stochastic arrivals,
a rule-based controller, metrics logging, and a **live visualization** using Matplotlib animation.

## Features
- 4 intersections (2x2 grid), each with N/E/S/W approaches and stochastic (Poisson) arrivals
- Phases: NS-green vs EW-green, with `min_green`, `amber`, and `all_red` timers
- Rule-based controller with a tunable `threshold` for switching
- Metrics logging and a **Matplotlib animation** (`viz/animate.py`) that pops up a window

## Quick Start

### 1) Create a virtual environment & install dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Run the baseline experiment (prints stats, no GUI)
```bash
python -m experiments.run_baseline
```

### 3) Run the visualization (GUI popup)
```bash
python -m viz.animate
```
Press the window's close (x) button to stop.

## Repo Layout
```
src/
  sim/
    config.py         # configs (arrival rates, phase timings, sim horizon)
    intersection.py   # per-intersection queues + timers + service
    controller.py     # Base + RuleBasedController
    metrics.py        # metrics logger
    env_multi.py      # 4-intersection environment + stepping
experiments/
  run_baseline.py     # non-GUI run that logs & prints metrics
viz/
  animate.py          # Matplotlib animation of 4 intersections
tests/
  test_env_basic.py   # sanity tests for arrivals & service
requirements.txt
README.md
```

## Notes
- This is intentionally lightweight and easy to extend (e.g., add Q-learning or global coordination).
- For your report, save figures from `viz/animate.py` (you can export frames) and logs from experiments.
