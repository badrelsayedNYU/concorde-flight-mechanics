"""Concorde data used in the calculations.

Published values: Concorde specifications (https://en.wikipedia.org/wiki/Concorde).
Estimated values are marked as such.
"""

S = 3856.2            # wing area, ft^2 (published)
SPAN = 84.0           # ft (published)
AR = SPAN**2 / S      # aspect ratio (computed, ~1.83)

OEW = 173_504         # empty weight, lb (published)
MTOW = 408_010        # max takeoff weight, lb (published)
PAYLOAD = 22_000      # lb (team assumption)
FUEL = 100_000        # lb loaded (team assumption, ~half of 210,940 lb capacity)
W0 = OEW + PAYLOAD + FUEL

T_DRY = 4 * 31_000    # lbf, 4 x Olympus 593 Mk 610 dry (published)
T_REHEAT = 4 * 38_050 # lbf, with reheat (published)
TSFC = 1.195          # lb/(lbf*h), Mach 2 cruise value used in every phase (assumption)

# Published maximum L/D used to fit the parabolic drag polar
EM_SUB = 11.47        # Mach 0.94
EM_SUP = 7.14         # Mach 2.04

CD0 = 0.0104          # estimated, same in both regimes
K_SUB = 1 / (4 * CD0 * EM_SUB**2)   # ~0.183, from Em = 1/(2 sqrt(K CD0))
K_SUP = 1 / (4 * CD0 * EM_SUP**2)   # ~0.472 (linear theory sqrt(M^2-1)/4 = 0.43 at M2)

CLMAX_TO = 0.90       # effective C_L,max at lift-off (estimated)
