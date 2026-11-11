"""Great-circle distance and initial course between two airports."""
import math

KSFO = (37.6189, -122.3750)   # San Francisco International
CYWG = (49.9100, -97.2399)    # Winnipeg James Armstrong Richardson International


def great_circle(a, b):
    """Return (distance [nmi], initial true course [deg]) from a to b (lat, lon in deg)."""
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dl = math.radians(b[1] - a[1])
    d = math.acos(math.sin(p1) * math.sin(p2) + math.cos(p1) * math.cos(p2) * math.cos(dl))
    brg = math.degrees(math.atan2(math.sin(dl) * math.cos(p2),
                                  math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl))) % 360
    return d * 3440.065, brg
