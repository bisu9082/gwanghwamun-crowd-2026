"""Fig 3. Planning figures versus the crowd that came.
(a) Crowd figures on one scale (planning, caps, observed, organiser claim).
(b) Daily card-based subway alightings per station: event day vs 12 other Saturdays (median, range).
(c) Event-day minus baseline-median alightings, summed for no-stop core stations and nearby stations.
(d) Hourly living population (domestic + foreign) in three core administrative dongs: event day vs seven other Saturdays, Mar-Apr 2026.
Data: data/subway_daily.csv (Seoul Open Data Plaza, CardSubwayStatsNew); data/living_pop_core3_saturdays.csv (Seoul Open Data Plaza, OA-14991/14992/14993)."""
import json, datetime as dt
import pandas as pd, numpy as np
import matplotlib.pyplot as plt, matplotlib as mpl
from matplotlib.ticker import FuncFormatter

D = "/mnt/user-data/uploads/claude_research/soft_target/JCCM_resubmission/data/"
OUT = "/mnt/user-data/outputs/jccm/figs/fig3_plan_vs_crowd"
mpl.rcParams.update({"font.family": "Liberation Sans", "font.size": 12.5, "axes.labelsize": 13,
                     "xtick.labelsize": 12, "ytick.labelsize": 12.5, "legend.fontsize": 12})
C = {"off": "#3A6EA8", "fan": "#C94F4A", "org": "#8A8A8A", "base": "#BDBDBD", "ink": "#222222", "grid": "#DDDDDD"}
kfmt = FuncFormatter(lambda v, _: f"{v/1000:,.0f}k" if v else "0")

def panel_label(ax, letter, fs=16, dy=6):
    ax.annotate(f"({letter})", xy=(0.0, 1.0), xycoords="axes fraction", xytext=(-4, dy), textcoords="offset points",
                fontsize=fs, fontweight="bold", va="bottom", ha="right", annotation_clip=False)
def clean(ax, grid_axis="x"):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.grid(axis=grid_axis, color=C["grid"], ls="--", lw=0.8); ax.set_axisbelow(True)

fig = plt.figure(figsize=(12, 10.2), dpi=200); fig.patch.set_facecolor("white")
gs = fig.add_gridspec(2, 2, left=0.2, right=0.985, top=0.95, bottom=0.07, wspace=0.62, hspace=0.36,
                      width_ratios=[1, 1])
axA, axB, axC, axD = (fig.add_subplot(gs[i, j]) for i in (0, 1) for j in (0, 1))

# ---------------- (a) crowd figures ----------------
items = [  # label, low, high, kind
    ("Seats", 22000, 22000, "org"),
    ("Tickets (police report)", 35000, 35000, "org"),
    ("20:00 (city data)", 40000, 42000, "fan"),
    ("Show time (MOIS)", 62000, 62000, "fan"),
    ("Hot-zone entry cap", 100000, 100000, "off"),
    ("Cumulative visitors", 104000, 104000, "org"),
    ("Police figure, to Daehanmun", 230000, 230000, "off"),
    ("Police figure, to Sungnyemun", 260000, 260000, "off"),
]
y = np.arange(len(items))[::-1]
for yi, (lab, lo, hi, k) in zip(y, items):
    axA.plot([0, hi], [yi, yi], color=C[k], lw=2.2, alpha=0.35, solid_capstyle="round")
    if hi > lo: axA.plot([lo, hi], [yi, yi], color=C[k], lw=6, solid_capstyle="round")
    axA.plot([hi], [yi], "o", ms=8, mfc=C[k], mec="white", mew=1.2)
    txt = f"{lo:,}–{hi:,}" if hi > lo else f"{hi:,}"
    axA.text(hi + 7000, yi, txt, va="center", ha="left", fontsize=12, color=C["ink"])
axA.set_yticks(y); axA.set_yticklabels([i[0] for i in items]); axA.tick_params(axis="y", length=0)
axA.set_xlim(0, 330000); axA.xaxis.set_major_formatter(kfmt); axA.set_xticks(range(0, 300001, 100000)); axA.spines["bottom"].set_bounds(0, 300000)
axA.set_xlabel("People"); axA.set_ylim(-0.6, len(items) + 1.6); axA.spines["left"].set_bounds(-0.5, len(items) - 0.5); clean(axA, "x")
from matplotlib.lines import Line2D
axA.legend(handles=[Line2D([], [], marker="o", ls="", ms=8, mfc=C[k], mec="white", label=l) for k, l in
                    [("off", "Police planning figure or cap"), ("fan", "Count, people present"), ("org", "Organiser figure or tickets")]],
           loc="upper right", frameon=True, facecolor='white', edgecolor='none', framealpha=1, handletextpad=0.3)

# ---------------- (b) station alightings ----------------
GATHER_S = ["20250301","20250308","20250315","20250322","20250329","20250405","20250426","20260516"]
d = pd.read_csv(D + "subway_saturdays_2025_2026.csv", dtype={"date": str}).rename(columns={"alight": "alightings"})
d["key"] = d.line + " " + d.station
sat = d; base = sat[(sat.date != "20260321") & (~sat.date.isin(GATHER_S))]; ev = sat[sat.date == "20260321"].set_index("key")
NAMES = {"5호선 광화문(세종문화회관)": "Gwanghwamun (L5)", "3호선 경복궁(정부서울청사)": "Gyeongbokgung (L3)",
         "1호선 시청": "City Hall (L1)", "2호선 시청": "City Hall (L2)", "1호선 종각": "Jonggak (L1)",
         "2호선 을지로입구": "Euljiro 1-ga (L2)", "5호선 서대문": "Seodaemun (L5)", "3호선 안국": "Anguk (L3)"}
core = list(NAMES)[:4]; peri = list(NAMES)[4:]
order = core + peri
ypos = {k: (len(order) - i + (0.6 if k in core else 0)) for i, k in enumerate(order)}
for k in order:
    g = base[base.key == k].alightings; yy = ypos[k]
    axB.plot([g.min(), g.max()], [yy, yy], color=C["base"], lw=6, solid_capstyle="round", zorder=1)
    axB.plot([g.median()], [yy], marker="|", ms=13, mew=2, color="#555555", zorder=2)
    axB.plot([ev.loc[k, "alightings"]], [yy], "o", ms=8.5, mfc=C["fan"], mec="white", mew=1.2, zorder=3)
axB.set_yticks([ypos[k] for k in order]); axB.set_yticklabels([NAMES[k] for k in order]); axB.tick_params(axis="y", length=0)
axB.set_xlim(0, 60000); axB.xaxis.set_major_formatter(kfmt); axB.set_xticks(range(0, 60001, 20000)); axB.set_xlabel("Daily alightings (card taps)")
top = max(ypos.values())
axB.set_ylim(0.3, top + 3.9); clean(axB, "x")
axB.spines["left"].set_bounds(0.5, top + 0.5)
for ks, lab in ((core, "No-stop stations"), (peri, "Nearby stations")):
    yl = max(ypos[k] for k in ks) + 0.62
    axB.text(59000, yl, lab, ha="right", va="center", fontsize=12, fontstyle="italic", color="#555555", bbox=dict(fc="white", ec="none", pad=1.5))
axB.legend(handles=[Line2D([], [], marker="o", ls="", ms=8, mfc=C["fan"], mec="white", label="21 Mar (event day)"),
                    Line2D([], [], marker="|", ls="", ms=12, mew=2, color="#555555", label="Ordinary Saturdays, median"),
                    Line2D([], [], lw=6, color=C["base"], label="Ordinary Saturdays, range (n = 18)")],
           loc="upper left", bbox_to_anchor=(0.0, 1.03), ncol=1, frameon=True, facecolor='white', edgecolor='none', framealpha=1, handlelength=1.8, handletextpad=0.9, labelspacing=0.35)

# ---------------- (c) aggregate difference (median of per-day group totals) ----------------
allst = sat[sat.date.isin(base.date.unique()) | (sat.date == "20260321")]
RING = ["1호선 종로3가","3호선 종로3가","5호선 종로3가","1호선 서울역","4호선 서울역","4호선 명동","4호선 회현(남대문시장)"]
def gdiff(keys):
    t = allst[allst.key.isin(keys)].groupby("date").alightings.sum()
    return t["20260321"] - t.drop("20260321").median()
vals = [gdiff(core), gdiff(peri), gdiff(core + peri), gdiff(RING)]
labs = ["No-stop (4)", "Nearby (4)", "All eight", "Outer ring (7)"]
yc = np.array([3, 2, 1, 0])
cols = [C["fan"], C["fan"], "#555555", "#8A8A8A"]
axC.barh(yc, vals, height=0.5, color=cols, edgecolor="white", linewidth=1.5)
axC.axvline(0, color=C["ink"], lw=1.2)
for yi, v in zip(yc, vals):
    axC.text(v + (1500 if v > 0 else -1500), yi, f"{v:+,.0f}".replace("-", "\u2212"), va="center", ha="left" if v > 0 else "right",
             fontsize=12.5, color=C["ink"])
axC.set_yticks(yc); axC.set_yticklabels(labs); axC.tick_params(axis="y", length=0)
axC.set_xlim(-62000, 50000); axC.set_xticks([-40000, -20000, 0, 20000, 40000]); axC.xaxis.set_major_formatter(FuncFormatter(lambda v, _: (f"{v/1000:+,.0f}k" if v else "0").replace("-", "\u2212")))
axC.set_xlabel("Event day minus ordinary-Saturday median"); axC.set_ylim(-0.6, 3.6); clean(axC, "x")

# ---------------- (d) hourly living population, 26 spring Saturdays 2025-2026 ----------------
lp = pd.read_csv(D + "core_hourly_saturdays_2025_2026.csv", index_col=0); lp.index = lp.index.astype(int); lp = lp.loc[8:23]
GATHER = ["20250301","20250308","20250315","20250322","20250329","20250405","20250426","20260516"]
evl = lp["20260321"]; oth = lp.drop(columns=["20260321"] + GATHER); gat = lp[GATHER]
hrs = lp.index.values
axD.fill_between([20, 21.5], 0, 350000, color="#BBBBBB", alpha=0.3, lw=0, zorder=0)
axD.text(20.75, 356000, "Show", ha="center", va="bottom", fontsize=12, color="#666666")
axD.fill_between(hrs, oth.min(axis=1), oth.max(axis=1), color=C["base"], alpha=0.35, lw=0, zorder=1)
axD.fill_between(hrs, oth.quantile(0.25, axis=1), oth.quantile(0.75, axis=1), color=C["base"], alpha=0.9, lw=0, zorder=1)
for c in gat.columns: axD.plot(hrs, gat[c], color="#7A7A7A", lw=0.9, ls=":", zorder=2)
axD.plot(hrs, oth.median(axis=1), color="#555555", lw=1.6, ls="--", zorder=2)
axD.plot(hrs, evl, color=C["fan"], lw=2.2, marker="o", ms=5.5, mfc=C["fan"], mec="white", zorder=3)
axD.set_xlim(7.6, 23.4); axD.set_xticks(range(8, 24, 4)); axD.set_xticklabels([f"{h:02d}:00" for h in range(8, 24, 4)])
axD.set_ylim(0, 560000); axD.set_yticks(range(0, 350001, 50000)); axD.yaxis.set_major_formatter(kfmt); axD.spines["left"].set_bounds(0, 350000)
axD.set_ylabel("People present, three core dongs"); axD.set_xlabel("Hour (local time)")
axD.legend(handles=[Line2D([], [], color=C["fan"], lw=2.2, marker="o", ms=5.5, mfc=C["fan"], mec="white", label="21 Mar 2026 (event day)"),
                    Line2D([], [], color="#555555", lw=1.6, ls="--", label="Ordinary Saturdays, median"),
                    Line2D([], [], lw=6, color=C["base"], alpha=0.9, label="Interquartile range"),
                    Line2D([], [], lw=6, color=C["base"], alpha=0.35, label="Range (n = 18)"),
                    Line2D([], [], color="#7A7A7A", lw=0.9, ls=":", label="Rally or parade Saturdays (n = 8)")],
           loc="upper left", bbox_to_anchor=(0.0, 1.03), frameon=True, facecolor='white', edgecolor='none', framealpha=1, handlelength=2.2, labelspacing=0.3)
clean(axD, "y")

for ax, l in zip((axA, axB, axC, axD), "abcd"): panel_label(ax, l)
fig.savefig(OUT + ".png", facecolor="white"); fig.savefig(OUT + ".pdf", facecolor="white")
print("saved", vals)
