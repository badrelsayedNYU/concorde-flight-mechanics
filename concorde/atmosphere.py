"""1976 US Standard Atmosphere, English units (troposphere + lower stratosphere)."""
import math

RHO_SL = 0.0023769   # slug/ft^3
G = 32.174           # ft/s^2
R_AIR = 1716.49      # ft*lbf/(slug*R)


def atm(h_ft):
    """Return (density [slug/ft^3], speed of sound [ft/s]) at geometric altitude h_ft."""
    if h_ft <= 36089:
        T = 518.67 - 0.00356616 * h_ft
        p = 2116.22 * (T / 518.67) ** 5.2561
    else:
        T = 389.97
        p = 472.68 * math.exp(-(h_ft - 36089) / 20806.0)
    return p / (R_AIR * T), math.sqrt(1.4 * R_AIR * T)


def sigma(h_ft):
    """Density ratio rho/rho_SL."""
    return atm(h_ft)[0] / RHO_SL
