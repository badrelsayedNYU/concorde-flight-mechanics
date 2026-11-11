"""Drag polar and L/D vs C_L chart (slide 4). Run: python -m plots.polar"""
import math, pathlib, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from concorde import aircraft as ac
from concorde.atmosphere import atm
from concorde.mission import run

R = run()
CD0, Ks, Kp, S = ac.CD0, ac.K_SUB, ac.K_SUP, ac.S
Wtoc = R["W_top_of_climb"]
OUT = pathlib.Path(__file__).resolve().parents[1] / "figures" / "polar_chart.png"
NAVY="#0B1F3A"; BLUE="#2E5C8A"; ORG="#F26B1D"; GRID="#DDE3EA"; MUTED="#5B6B7F"
plt.rcParams.update({"font.family":"DejaVu Sans","mathtext.fontset":"dejavusans","font.size":10,
  "axes.edgecolor":MUTED,"axes.labelcolor":NAVY,"xtick.color":MUTED,"ytick.color":MUTED,
  "axes.spines.top":False,"axes.spines.right":False})
def cl_range(h,M,fuel):
    rho,a=atm(h); q=0.5*rho*(M*a)**2
    return Wtoc/(q*S),(Wtoc-fuel)/(q*S)
sub_cl=cl_range(30000,0.95,R["phases"][3]["fuel"]); sup_cl=cl_range(55000,2.0,R["supersonic_cruise"]["fuel"])
CL=np.linspace(0.0,0.6,400)
fig,(a1,a2)=plt.subplots(1,2,figsize=(7.4,3.6),dpi=300,gridspec_kw={"wspace":0.32})
for K,c,lab in [(Ks,BLUE,"Subsonic (M 0.94)"),(Kp,ORG,"Supersonic (M 2.0)")]:
    CD=CD0+K*CL**2; a1.plot(CD,CL,color=c,lw=2.2,label=lab)
    cls=math.sqrt(CD0/K); cds=2*CD0; Em=cls/cds
    a1.plot([0,cds*2.2],[0,cls*2.2],color=c,lw=1.3,ls=(0,(4,3)),alpha=0.9)
    a1.plot(cds,cls,"o",color=c,ms=6,zorder=5)
    E=CL/(CD0+K*CL**2); a2.plot(CL,E,color=c,lw=2.2,label=lab)
    a2.plot(cls,Em,"o",color=c,ms=6,zorder=5)
    a2.annotate(f"$E_m$ = {Em:.2f}\n$C_L^*$ = {cls:.3f}",(cls,Em),xytext=(cls+0.07,Em+(0.3 if K==Ks else 1.0)),
                fontsize=9,color=c,arrowprops=dict(arrowstyle="-",color=c,lw=0.8))
# cruise operating ranges
for (c0,c1),K,c in [(sub_cl,Ks,BLUE),(sup_cl,Kp,ORG)]:
    xs=np.linspace(c1,c0,30); a2.plot(xs,xs/(CD0+K*xs**2),color=c,lw=7,alpha=0.28,solid_capstyle="round")
a2.text(sub_cl[1]-0.01,sub_cl[1]/(CD0+Ks*sub_cl[1]**2)+0.35,"cruise",fontsize=8.5,color=BLUE,va="bottom",ha="right")
a2.text(sup_cl[1]-0.01,sup_cl[1]/(CD0+Kp*sup_cl[1]**2)+0.35,"cruise",fontsize=8.5,color=ORG,va="bottom",ha="right")
a1.set_xlabel("Drag coefficient $C_D$"); a1.set_ylabel("Lift coefficient $C_L$")
a1.set_title("Drag polar  $C_D = C_{D_0} + K\\,C_L^{\\,2}$",fontsize=10.5,color=NAVY,loc="left")
a1.set_xlim(0,0.08); a1.set_ylim(0,0.6)
a1.text(0.079,0.02,"dashed line from origin is tangent\nat the maximum-$L/D$ point",fontsize=8,color=MUTED,va="bottom",ha="right")
a2.set_xlabel("Lift coefficient $C_L$"); a2.set_ylabel("Lift-to-drag ratio $E = C_L/C_D$")
a2.set_title("Lift-to-drag ratio vs. $C_L$",fontsize=10.5,color=NAVY,loc="left")
a2.set_xlim(0,0.6); a2.set_ylim(0,13.5)
for ax in (a1,a2): ax.grid(True,color=GRID,lw=0.6); ax.set_axisbelow(True)
a2.legend(frameon=False,fontsize=9,loc="lower right")
fig.savefig(OUT,dpi=300,bbox_inches="tight",facecolor="white")
print("wrote", OUT)
