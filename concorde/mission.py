"""Phase-by-phase mission calculation using AE 4653 course methods.

Baseline mission (subsonic): lift-off, turn, fastest climb to 30,000 ft,
constant-altitude/constant-speed cruise at Mach 0.95, best-range glide.
Also computes a Mach 2 / 55,000 ft cruise over the same cruise leg for comparison.

Run:  python -m concorde.mission   (writes results/baseline.json)
"""
import json, math, pathlib
from . import aircraft as ac
from .atmosphere import atm, RHO_SL, G
from .route import great_circle, KSFO, CYWG

C = ac.TSFC / 3600.0  # 1/s


def drag(W, rho, V, K, n=1.0):
    q = 0.5 * rho * V * V
    CL = n * W / (q * ac.S)
    return q * ac.S * (ac.CD0 + K * CL * CL)


def liftoff(W):
    """V_LO = 1.2 V_stall, full reheat; drag and rolling friction neglected."""
    V = math.sqrt(2.88 * (W / ac.S) / (RHO_SL * ac.CLMAX_TO))
    TW = ac.T_REHEAT / W
    t = V / (G * TW)
    d = V**2 / (2 * G * TW)
    return dict(phase="Lift-off", t=t, fuel=C * ac.T_REHEAT * t, V0=0.0, V1=V, dist_nm=d / 6076.1,
                note=f"ground roll {d:,.0f} ft")


def turn(W, V, heading_from, heading_to, bank_deg=25):
    """Level coordinated turn at constant speed; thrust = drag."""
    dpsi = (heading_to - heading_from) % 360
    dpsi = 360 - dpsi if dpsi > 180 else dpsi
    n = 1 / math.cos(math.radians(bank_deg))
    omega = G * math.tan(math.radians(bank_deg)) / V
    t = math.radians(dpsi) / omega
    D = drag(W, RHO_SL, V, ac.K_SUB, n)
    return dict(phase="Turn", t=t, fuel=C * D * t, V0=V, V1=V, dist_nm=V * t / 6076.1,
                note=f"{dpsi:.0f} deg turn at {bank_deg} deg bank, n = {n:.2f}")


def fastest_climb(W, h_top, M_cap=0.95, dh=100):
    """Course fastest-climb speed at each altitude, dry thrust T = sigma*T_SL, capped at M_cap."""
    h = t = fuel = x = 0.0
    Vs = []
    while h < h_top:
        rho, a = atm(h + dh / 2)
        T = ac.T_DRY * rho / RHO_SL
        TW = T / W
        gam = 1 + math.sqrt(1 + 3 / (ac.EM_SUB * TW) ** 2)
        V = min(math.sqrt((T / ac.S) * gam / (3 * rho * ac.CD0)), M_cap * a)
        RC = V * (T - drag(W, rho, V, ac.K_SUB)) / W
        dt = dh / RC
        t += dt; f = C * T * dt; fuel += f; W -= f; x += V * dt; h += dh; Vs.append(V)
    return dict(phase="Climb", t=t, fuel=fuel, V0=Vs[0], V1=Vs[-1], dist_nm=x / 6076.1,
                note=f"0 to {h_top:,} ft, avg {h_top / t * 60:,.0f} ft/min")


def cruise(W, X_nm, h, M, K, dx=1000):
    """Constant altitude, constant Mach; integrate dW/dx = -c D / V."""
    rho, a = atm(h)
    V = M * a
    x = fuel = 0.0
    E = []
    while x < X_nm * 6076.1:
        D = drag(W, rho, V, K)
        E.append(W / D)
        f = C * D * dx / V; fuel += f; W -= f; x += dx
    return dict(phase="Cruise", t=X_nm * 6076.1 / V, fuel=fuel, V0=V, V1=V, dist_nm=X_nm,
                E_start=E[0], E_end=E[-1], note=f"{h:,} ft, Mach {M}")


def glide(W, h_top, dh=100):
    """Best-range glide at idle: gamma = -1/E_m, V_br from the course formula."""
    h = h_top; t = 0.0; Vs = []
    while h > 0:
        rho, a = atm(h - dh / 2)
        V = min(math.sqrt(2 * W / ac.S / rho) * (ac.K_SUB / ac.CD0) ** 0.25, 0.95 * a)
        Vs.append(V); t += dh / (V / ac.EM_SUB); h -= dh
    return dict(phase="Descent", t=t, fuel=0.0, V0=Vs[0], V1=Vs[-1],
                dist_nm=h_top * ac.EM_SUB / 6076.1, note="best-range glide at idle")


def run():
    D_nm, course = great_circle(KSFO, CYWG)
    W = ac.W0
    phases = []
    p = liftoff(W); phases.append(p); W -= p["fuel"]
    p = turn(W, 1.1 * phases[0]["V1"], 284, course); phases.append(p); W -= p["fuel"]
    p = fastest_climb(W, 30000); phases.append(p); W -= p["fuel"]
    W_toc = W
    desc = glide(W, 30000)
    X_cruise = D_nm - sum(q["dist_nm"] for q in phases) - desc["dist_nm"]
    cr = cruise(W_toc, X_cruise, 30000, 0.95, ac.K_SUB)
    phases += [cr, desc]
    sup = cruise(W_toc, X_cruise, 55000, 2.0, ac.K_SUP)
    rho55, a55 = atm(55000)
    out = dict(route=dict(distance_nm=D_nm, initial_course_deg=course),
               W0=ac.W0, W_top_of_climb=W_toc, phases=phases, supersonic_cruise=sup,
               mach2_check=dict(drag_lb=drag(W_toc, rho55, 2 * a55, ac.K_SUP),
                                course_thrust_lb=ac.T_DRY * rho55 / RHO_SL),
               totals=dict(t_s=sum(q["t"] for q in phases), fuel_lb=sum(q["fuel"] for q in phases)))
    return out


if __name__ == "__main__":
    res = run()
    path = pathlib.Path(__file__).resolve().parents[1] / "results" / "baseline.json"
    path.write_text(json.dumps(res, indent=1))
    W = res["W0"]
    print(f"Route {res['route']['distance_nm']:.0f} nmi, course {res['route']['initial_course_deg']:.0f} deg")
    for p in res["phases"]:
        W -= p["fuel"]
        print(f"{p['phase']:9s} {p['t']/60:7.1f} min {p['fuel']:9,.0f} lb fuel  end W {W:9,.0f} lb  | {p['note']}")
    print(f"Total {res['totals']['t_s']/3600:.2f} h, {res['totals']['fuel_lb']:,.0f} lb fuel")
