"""Fig 4. Content of artist messages to fans, 19-21 March 2026, coded from the original Weverse text where public.
(a) Message units x content categories (filled = category present).
(b) Number of message units containing each category (n = 8).
Coding table saved to fig4_message_coding.csv. A category is coded present only if the reported text states it."""
import numpy as np, pandas as pd
import matplotlib.pyplot as plt, matplotlib as mpl
from matplotlib.patches import Rectangle

OUT = "figures/fig4_message_coding"
mpl.rcParams.update({"font.family": "Liberation Sans", "font.size": 12.5})
C = {"art": "#E8943A", "fan": "#C94F4A", "ink": "#222222", "mute": "#777777", "grid": "#E4E4E4"}

CATS = ["Follow or turn\nto staff", "Don\u2019t push;\nlook after\neach other", "Stay back;\nuse the\nscreens",
        "General\n\u201cstay safe\u201d", "Health and\ncomfort", "Thanks to\nauthorities\nand staff",
        "Safe\nprecedent;\ntrust in fans", "Stay home\nor watch\nremotely"]
ROWS = [  # label, source, codes (1 = present) in CATS order; coded from the Weverse original where public
 ("RM, 19 Mar",              "Weverse; MT; Star News",   [1, 1, 0, 1, 0, 1, 0, 0]),
 ("Jin, 19 Mar",             "Weverse; MT; Star News",   [0, 0, 0, 1, 0, 1, 0, 0]),
 ("V, 20 Mar",               "Weverse; MyDaily",         [0, 1, 0, 1, 0, 0, 0, 0]),
 ("Jimin, 20 Mar",           "Weverse; MyDaily",         [1, 1, 0, 1, 1, 0, 0, 0]),
 ("Group live, 20 Mar",      "Star Today (MK)",          [1, 0, 1, 1, 0, 0, 1, 0]),
 ("Suga, 21 Mar",            "Weverse; MT; Sports Donga",[0, 0, 0, 1, 1, 1, 0, 0]),
 ("J-Hope, 21 Mar",          "Weverse; Sports Seoul",    [0, 1, 1, 1, 0, 0, 0, 0]),
 ("Jungkook, 21 Mar",        "Weverse; Edaily; Gukje",   [0, 0, 0, 1, 0, 1, 0, 0]),
]
M = np.array([r[2] for r in ROWS]); nR, nC = M.shape
pd.DataFrame(M, columns=[c.replace("\n", " ") for c in CATS], index=[r[0] for r in ROWS]).assign(
    source=[r[1] for r in ROWS]).to_csv(OUT + ".csv", encoding="utf-8-sig")

fig = plt.figure(figsize=(12, 7.9), dpi=200); fig.patch.set_facecolor("white")
axA = fig.add_axes([0.175, 0.34, 0.805, 0.50])
axB = fig.add_axes([0.175, 0.05, 0.805, 0.19], sharex=axA)

# (a) matrix
for i in range(nR):
    for j in range(nC):
        yy = nR - 1 - i
        if M[i, j]:
            axA.plot(j, yy, "o", ms=17, mfc=C["art"], mec="white", mew=1.5, zorder=3)
        else:
            axA.plot(j, yy, "o", ms=5, mfc=C["grid"], mec="none", zorder=2)
for i in range(nR + 1):
    axA.axhline(i - 0.5, color=C["grid"], lw=1.0, zorder=1)
last = nC - 1
axA.add_patch(Rectangle((last - 0.46, -0.46), 0.92, nR - 0.08, fill=False, ec=C["fan"], lw=1.8, ls=(0, (5, 3)), zorder=4))
axA.set_xlim(-0.6, nC - 0.4); axA.set_ylim(-0.6, nR - 0.4)
axA.set_yticks(range(nR)); axA.set_yticklabels([r[0] for r in ROWS][::-1], fontsize=12.5)
axA.xaxis.tick_top(); axA.set_xticks(range(nC)); axA.set_xticklabels(CATS, fontsize=12, linespacing=1.12)
axA.tick_params(length=0, pad=6)
for s in axA.spines.values(): s.set_visible(False)
for lab in axA.get_xticklabels()[-1:]:
    lab.set_color(C["fan"]); lab.set_fontweight("bold")
axA.annotate("(a)", xy=(0, 1), xycoords="axes fraction", xytext=(-118, 50), textcoords="offset points",
             fontsize=16, fontweight="bold", va="bottom", ha="left", annotation_clip=False)

# (b) column totals
tot = M.sum(axis=0)
cols = [C["art"]] * (nC - 1) + [C["fan"]]
axB.bar(range(nC), tot, width=0.56, color=cols, edgecolor="white", linewidth=1.5)
for j, v in enumerate(tot):
    axB.text(j, v + 0.2, f"{v}", ha="center", va="bottom", fontsize=12.5,
             fontweight="bold" if j == last else "normal", color=C["fan"] if j == last else C["ink"])
axB.set_ylim(0, 9.3); axB.set_yticks([0, 4, 8]); axB.spines["left"].set_bounds(0, 8)
axB.set_ylabel("Message units\n(of 8)", fontsize=12.5)
for s in ("top", "right", "bottom"): axB.spines[s].set_visible(False)
axB.tick_params(axis="x", length=0, labelbottom=False); axB.tick_params(axis="y", labelsize=12)
axB.grid(axis="y", color=C["grid"], ls="--", lw=0.8); axB.set_axisbelow(True)
axB.annotate("(b)", xy=(0, 1), xycoords="axes fraction", xytext=(-118, 4), textcoords="offset points",
             fontsize=16, fontweight="bold", va="bottom", ha="left", annotation_clip=False)

fig.savefig(OUT + ".png", facecolor="white"); fig.savefig(OUT + ".pdf", facecolor="white")
print("saved", tot)
