"""Figure S1. Spatial units: the three core administrative dongs, the eight adjacent (ring) dongs, the concert corridor
from the stage to Sungnyemun, and subway stations used in the analysis. Boundaries: admdongkor ver20250401 (CC BY 4.0,
based on Statistics Korea / MOIS administrative boundaries). Station and landmark positions are approximate."""
import json, numpy as np
import matplotlib.pyplot as plt, matplotlib as mpl
from shapely.geometry import shape
mpl.rcParams.update({"font.family": "Liberation Sans", "font.size": 11})
g = json.load(open("data/raw/seoul_dongs.geojson", encoding="utf-8"))
NAMES = json.load(open("data/raw/seoul_dong_names.json", encoding="utf-8"))
CORE = {"11110530": "Sajik", "11110615": "Jongno 1-4ga", "11140520": "Sogong"}
RING = {"11140550": "Myeong-dong", "11140540": "Hoehyeon", "11140605": "Euljiro", "11110515": "Cheongun-Hyoja",
        "11110540": "Samcheong", "11110600": "Gahoe", "11110580": "Gyonam", "11110630": "Jongno 5-6ga"}
C = {"core": "#C94F4A", "ring": "#E8943A", "other": "#EEEEEE", "ink": "#222222", "corr": "#3A6EA8"}
fig, ax = plt.subplots(figsize=(9, 9.6), dpi=200)
xmin, xmax, ymin, ymax = 126.955, 127.003, 37.553, 37.588
for f in g["features"]:
    cd = f["properties"]["adm_cd2"][:8]; geom = shape(f["geometry"])
    if not geom.intersects(shape({"type": "Polygon", "coordinates": [[(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax), (xmin, ymin)]]})): continue
    kind = "core" if cd in CORE else "ring" if cd in RING else "other"
    polys = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    for p in polys:
        x, y = p.exterior.xy
        ax.fill(x, y, fc=C[kind], alpha={"core": 0.35, "ring": 0.22, "other": 1.0}[kind], ec="white", lw=1.2, zorder=1)
    if kind != "other":
        c = geom.representative_point(); cx, cy = (126.9712, 37.5618) if cd == "11140520" else (c.x, c.y)
        ax.text(cx, cy, (CORE | RING)[cd], ha="center", va="center", fontsize=10.5 if kind == "core" else 9.5,
                fontweight="bold" if kind == "core" else "normal", color=C["ink"], zorder=4,
                bbox=dict(fc="white", ec="none", alpha=0.7, pad=1))
# corridor (approximate): stage -> City Hall/Daehanmun -> Sungnyemun
stage = (126.9768, 37.5745); daehan = (126.9760, 37.5657); sung = (126.9753, 37.5600)
ax.plot([stage[0], daehan[0], sung[0]], [stage[1], daehan[1], sung[1]], color=C["corr"], lw=5, solid_capstyle="round", zorder=3)
for (x, y), lab, dx, dy, ha in [(stage, "Stage", 0.0012, 0, "left"), (daehan, "Daehanmun\n(230,000 to here)", -0.0015, 0.0024, "right"), (sung, "Sungnyemun\n(260,000 to here)", 0.0012, 0, "left")]:
    ax.plot(x, y, "o", ms=9, mfc="white", mec=C["corr"], mew=2.5, zorder=5)
    ax.text(x + dx, y + dy, lab, ha=ha, va="center", fontsize=10.5, color=C["corr"], fontweight="bold", zorder=6,
            bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))
ST = {"Gwanghwamun": (126.9768, 37.5710, "n"), "Gyeongbokgung": (126.9735, 37.5758, "n"), "City Hall": (126.9772, 37.5653, "n"),
      "Jonggak": (126.9831, 37.5702, "n"), "Euljiro 1-ga": (126.9822, 37.5660, "n"), "Seodaemun": (126.9665, 37.5658, "n"),
      "Anguk": (126.9855, 37.5765, "n"), "Jongno 3-ga": (126.9919, 37.5714, "r"), "Seoul Station": (126.9707, 37.5547, "r"),
      "Myeong-dong": (126.9863, 37.5609, "r"), "Hoehyeon": (126.9786, 37.5588, "r")}
for n, (x, y, k) in ST.items():
    ax.plot(x, y, marker="s", ms=7, mfc="#222222" if k == "n" else "white", mec="#222222", mew=1.5, zorder=6)
    ax.text(x + 0.0007, y - 0.0009, n, fontsize=9, color="#333333", zorder=6)
ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax); ax.set_aspect(1 / np.cos(np.radians(37.57)))
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_visible(False)
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
ax.legend(handles=[Patch(fc=C["core"], alpha=0.35, label="Core dongs (3)"), Patch(fc=C["ring"], alpha=0.22, label="Adjacent dongs (8)"),
                   Line2D([], [], color=C["corr"], lw=5, label="Concert corridor (approximate)"),
                   Line2D([], [], marker="s", ls="", mfc="#222222", mec="#222222", label="Corridor stations"),
                   Line2D([], [], marker="s", ls="", mfc="white", mec="#222222", label="Outer-ring stations")],
          loc="lower right", frameon=True, facecolor="white", edgecolor="none", fontsize=10)
ax.plot([126.9575, 126.9575 + 0.0113], [37.5545, 37.5545], color="#222222", lw=2)
ax.text(126.9575 + 0.0056, 37.5550, "1 km", ha="center", fontsize=9.5)
fig.tight_layout()
for ext in ("pdf", "png"): fig.savefig(f"figures/figS1_map.{ext}", facecolor="white", bbox_inches="tight", pad_inches=0.05)
print("saved")
