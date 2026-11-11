# Concorde flight mechanics: San Francisco (KSFO) to Winnipeg (CYWG)

AE 4653 Aircraft Flight Mechanics final project, NYU Tandon, Fall 2026.

We fly the Concorde from San Francisco to Winnipeg two ways: by hand with the course's
flight-phase equations, and in the FlightGear simulator, then compare the two.
This repo holds the calculation model and the scripts that make the presentation's graphs.

## Run

```bash
pip install -r requirements.txt
python -m concorde.mission   # phase-by-phase results -> results/baseline.json
python -m plots.polar        # drag polar chart -> figures/polar_chart.png
```

## What's in it

| Path | Contents |
|---|---|
| `concorde/atmosphere.py` | 1976 standard atmosphere (density, speed of sound) |
| `concorde/aircraft.py` | Concorde data with sources, and the fitted drag polar |
| `concorde/route.py` | Great-circle distance and initial course |
| `concorde/mission.py` | Lift-off, turn, fastest climb, cruise, best-range glide |
| `plots/polar.py` | Drag polar and L/D vs. C_L chart |

## Current baseline (preliminary)

| Item | Value |
|---|---|
| Great-circle distance | 1,306 nmi, initial course 048° |
| Takeoff weight | 295,504 lb (100,000 lb fuel, 22,000 lb payload) |
| Flight time | 2.4 h (Mach 0.95 cruise at 30,000 ft) |
| Fuel burned | 68,670 lb |

The baseline cruise is subsonic. The plan is to fly the mission at Mach 2, as Concorde was
designed to: the next version adds a transonic acceleration phase with reheat and a Mach 2
cruise at about 55,000 ft.

## Assumptions

- Parabolic drag polar, C_D = C_D0 + K C_L², with one C_D0 = 0.0104. K is chosen in each
  regime so the maximum L/D matches Concorde's published values (11.47 at Mach 0.94,
  7.14 at Mach 2.04), giving K = 0.183 subsonic and 0.472 at Mach 2.
- Constant TSFC of 1.195 lb/(lbf·h) in every phase.
- Lift-off neglects drag and rolling friction; V_LO = 1.2 V_stall with C_L,max = 0.90.
- Climb thrust scales with density, T = σ T_SL. This model can't supply Mach 2 thrust,
  so the supersonic version will use engine data instead.

## Sources

- Concorde specifications: https://en.wikipedia.org/wiki/Concorde
- FlightGear Concorde (JSBSim flight model): https://wiki.flightgear.org/Concorde
