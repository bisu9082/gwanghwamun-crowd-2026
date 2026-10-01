"""Fig 1. Analytical framework: three interfaces between the official safety system and the fan community,
laid out before / during / after the 21 March 2026 event. Vector output (PDF) + PNG preview."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib as mpl

mpl.rcParams.update({"font.family": "Liberation Sans", "font.size": 12.5})
C = {"off": "#3A6EA8", "art": "#E8943A", "fan": "#C94F4A", "ink": "#222222", "mute": "#666666"}
TINT = {"off": "#E6EDF6", "art": "#FCEEDD", "fan": "#F7E3E2"}

fig, ax = plt.subplots(figsize=(12, 7.6), dpi=200)
fig.patch.set_facecolor("white"); ax.set_xlim(0, 100); ax.set_ylim(2, 64); ax.axis("off")

# column geometry
X0, LANE_W = 20.5, 25.5          # first column x, column width
GAP = 1.2
cols = [("Before", "announcement to eve of event"), ("During", "event day to end of show"), ("After", "after the show")]
lanes = [("off", "Official safety\nsystem", 42.0),
         ("art", "Artist–fan\nchannel", 23.5),
         ("fan", "Fan community\nand crowd", 5.0)]
LANE_H = 14.0

cells = {
 "off": ["Planning figure and\nhow it was derived\nMeasures sized to it\nPublic warnings",
         "Access control\nand closures\nCrowd monitoring\nEmergency texts",
         "Reopening\nPublic account of the\nfigure and the response"],
 "art": ["Messages to fans\nbefore the event:\ncontent and fit with\nthe official plan",
         "Messages on the day:\nconduct, position,\nattend or stay home?",
         "Messages after\nthe event"],
 "fan": ["Decisions to attend\nor watch remotely\nSelf-organised plans",
         "Crowd present\nand its conduct",
         "Self-organised tasks\nafter the show"],
}

# column headers
for j, (h, sub) in enumerate(cols):
    cx = X0 + j * (LANE_W + GAP) + LANE_W / 2
    ax.text(cx, 62.2, h, ha="center", va="center", fontsize=15, fontweight="bold", color=C["ink"])
    ax.text(cx, 59.6, sub, ha="center", va="center", fontsize=12.5, color=C["mute"])

for key, name, y in lanes:
    # lane label
    ax.add_patch(FancyBboxPatch((0.6, y), 17.4, LANE_H, boxstyle="round,pad=0,rounding_size=1.2",
                                fc=C[key], ec="none"))
    ax.text(0.6 + 8.7, y + LANE_H / 2, name, ha="center", va="center", fontsize=14,
            fontweight="bold", color="white", linespacing=1.15)
    for j in range(3):
        x = X0 + j * (LANE_W + GAP)
        ax.add_patch(FancyBboxPatch((x, y), LANE_W, LANE_H, boxstyle="round,pad=0,rounding_size=1.0",
                                    fc=TINT[key], ec=C[key], lw=2.0))
        ax.text(x + LANE_W / 2, y + LANE_H / 2, cells[key][j], ha="center", va="center",
                fontsize=12.5, color=C["ink"], linespacing=1.25)

# interface arrows in the right gutter: lane centre -> lane centre
AX = X0 + 3 * (LANE_W + GAP) + 2.0
YC = {k: y + LANE_H / 2 for k, _, y in lanes}
def arrow(y1, y2, color, ls="-"):
    ax.add_patch(FancyArrowPatch((AX, y1), (AX, y2), arrowstyle="-|>", mutation_scale=18,
                 lw=2.0, color=color, linestyle=ls, shrinkA=0, shrinkB=0))
arrow(YC["off"], YC["art"] + 1.0, C["off"])
ax.text(AX + 1.2, (YC["off"] + YC["art"]) / 2, "Aligned with\nthe plan? (4.6)", ha="left", va="center",
        fontsize=12.5, color=C["ink"], linespacing=1.2)
arrow(YC["art"], YC["fan"] + 1.0, C["art"])
ax.text(AX + 1.2, (YC["art"] + YC["fan"]) / 2, "Heeded as a\ntrusted\nsource? (5.2)", ha="left", va="center",
        fontsize=12.5, color=C["ink"], linespacing=1.2)
RX = AX + 18.5
ax.add_patch(FancyArrowPatch((RX, YC["fan"]), (RX, YC["off"]), arrowstyle="-|>", mutation_scale=18,
             lw=2.0, color=C["fan"], linestyle=(0, (5, 3)), shrinkA=0, shrinkB=0))
ax.text(RX + 1.2, (YC["fan"] + YC["off"]) / 2, "Complement or substitute for official control?",
        ha="left", va="center", rotation=90, fontsize=12.5, color=C["ink"])
ax.set_xlim(0, RX + 4.0)
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
for ext in ("pdf", "png"):
    fig.savefig(f"figures/fig1_framework.{ext}", facecolor="white")
print("saved")
