"""Fig 2. Case timeline on three tracks (authorities & organiser / artist channel / fans & crowd).
(a) 3 Feb - 20 Mar 2026, one column per dated event (ordinal spacing).
(b) 21 Mar 2026, clock time. Times of member posts are upper bounds (first report timestamp).
Sources: evidence/evidence_dossier.pdf."""
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyBboxPatch

mpl.rcParams.update({"font.family": "Liberation Sans", "font.size": 12.5})
C = {"off": "#3A6EA8", "art": "#E8943A", "fan": "#C94F4A", "ink": "#222222", "mute": "#666666", "grid": "#DDDDDD"}
TINT = {"off": "#E6EDF6", "art": "#FCEEDD", "fan": "#F7E3E2"}
LANES = [("off", "Authorities\n& organiser"), ("art", "Artist\nchannel"), ("fan", "Fans &\ncrowd")]

def panel_label(ax, letter, fs=16, dy=6):
    ax.annotate(f"({letter})", xy=(0.0, 1.0), xycoords="axes fraction", xytext=(0, dy),
                textcoords="offset points", fontsize=fs, fontweight="bold", va="bottom", ha="left",
                annotation_clip=False)

fig = plt.figure(figsize=(12, 10.6), dpi=200)
fig.patch.set_facecolor("white")
axA = fig.add_axes([0.125, 0.575, 0.86, 0.35])
axB = fig.add_axes([0.125, 0.075, 0.86, 0.41])

# ---------------- (a) pre-event, ordinal date columns ----------------
dates = ["3 Feb", "9 Feb", "9 Mar", "10 Mar", "15 Mar", "18 Mar", "19 Mar", "20 Mar"]
A = {  # (lane, column index): text
 ("off", 0): "Date set;\nNetflix live\nstream\nannounced",
 ("off", 1): "Police: up\nto 260,000\n(ticketed\n\u224835,000)",
 ("off", 2): "City safety\nHQ; 3,400\nstaff; texts\nplanned",
 ("off", 3): "Seats 15,000\n\u2192 22,000;\nno-stop\ntrains planned",
 ("off", 4): "Police\nrestate\n260,000;\n\u22486,500 officers",
 ("off", 5): "Transport\nplan: road\nclosures, bus\ndiversions",
 ("off", 6): "Terror alert\nraised to\n\u2018caution\u2019",
 ("off", 7): "English\nemergency\ntext; road\nclosed 21:00",
 ("art", 6): "RM, Jin:\n\u201cfollow staff\u201d,\n\u201cstay safe\u201d",
 ("art", 7): "V, Jimin\nposts; 14:00\ngroup live",
 ("fan", 7): "\u2248400 clean-up\nvolunteers\n(incl. ticket-\nless fans)",
}
nC, laneH = len(dates), 1.0
axA.set_xlim(-0.5, nC - 0.5); axA.set_ylim(0, 3 * laneH); axA.axis("off")
for i, (k, name) in enumerate(LANES):
    y0 = (2 - i) * laneH
    axA.add_patch(FancyBboxPatch((-0.5, y0 + 0.04), nC, laneH - 0.08, boxstyle="round,pad=0,rounding_size=0.06",
                                 fc=TINT[k], ec="none", zorder=0))
    axA.text(-0.56, y0 + laneH / 2, name, ha="right", va="center", fontsize=13.5, fontweight="bold",
             color=C[k], linespacing=1.15)
for j, d in enumerate(dates):
    axA.plot([j, j], [0.02, 3 * laneH - 0.02], color=C["grid"], lw=1.0, ls="--", zorder=1)
    axA.text(j, 3 * laneH + 0.06, d, ha="center", va="bottom", fontsize=13, fontweight="bold", color=C["ink"])
for (k, j), txt in A.items():
    i = [l for l, _ in LANES].index(k); y0 = (2 - i) * laneH
    axA.text(j, y0 + laneH / 2, txt, ha="center", va="center", fontsize=12, color=C["ink"], linespacing=1.18,
             bbox=dict(fc="white", ec=C[k], lw=1.8, boxstyle="round,pad=0.3"), zorder=3)
panel_label(axA, "a", dy=24)

# ---------------- (b) event day, clock time ----------------
B = {
 "off": [(6.0, "06:00 screening\nat 31 gates"), (14.0, "14:00 no-stop:\nGwanghwamun"),
         (15.0, "15:00 no-stop:\n2 more stations"), (16.0, "16:00 Sajik-ro\nclosed"),
         (22.0, "22:00 stations\nreopen"), (23.0, "23:00 buses,\nroads reopen")],
 "art": [(15.75, "≤15:45 Suga:\n“dress warmly”"), (17.7, "≤17:42 J-Hope:\n“don’t push; use\nthe big screens”"),
         (18.85, "≤18:51 Jungkook:\n“meet safely”")],
 "fan": [(20.0, "20:00 ≈40,000–42,000\npresent (city data)"), (21.5, "≈21:30 volunteer\nclean-up begins")],
}
axB.set_xlim(5.0, 25.2); axB.set_ylim(0, 3 * laneH)
for s in ("top", "right", "left"): axB.spines[s].set_visible(False)
axB.set_yticks([]); axB.set_xticks(range(6, 25, 2)); axB.set_xticklabels([f"{h:02d}:00" for h in range(6, 25, 2)])
axB.tick_params(axis="x", labelsize=12.5); axB.set_xlabel("21 March 2026 (local time)", fontsize=13)
for i, (k, name) in enumerate(LANES):
    y0 = (2 - i) * laneH
    axB.add_patch(FancyBboxPatch((5.0, y0 + 0.04), 20.2, laneH - 0.08, boxstyle="round,pad=0,rounding_size=0.06",
                                 fc=TINT[k], ec="none", zorder=0))
    axB.text(4.85, y0 + laneH / 2, name, ha="right", va="center", fontsize=13.5, fontweight="bold",
             color=C[k], linespacing=1.15)
# show window
axB.axvspan(20.0, 21.5, color="#BBBBBB", alpha=0.35, zorder=0.5, lw=0)
axB.text(20.75, 3 * laneH + 0.03, "Show", ha="center", va="bottom", fontsize=12.5, color=C["mute"])

fig.canvas.draw(); R = fig.canvas.get_renderer()
LEVELS = [0.80, 0.47, 0.18]   # label heights inside a lane (fraction of lane)
for i, (k, _) in enumerate(LANES):
    y0 = (2 - i) * laneH; placed = []
    for x, txt in sorted(B[k]):
        for lv in LEVELS:
            right = x > 24.5
            t = axB.text(x - 0.15 if right else x + 0.15, y0 + lv * laneH, txt, ha="right" if right else "left", va="center", fontsize=12, color=C["ink"],
                         linespacing=1.15, bbox=dict(fc="white", ec="none", alpha=0.95, boxstyle="round,pad=0.15"), zorder=4)
            bb = t.get_window_extent(R).expanded(1.03, 1.08)
            if not any(bb.overlaps(p) for p in placed):
                placed.append(bb); break
            t.remove()
        axB.plot([x], [y0 + lv * laneH], marker="o", ms=7.5, mfc=C[k], mec="white", mew=1.2, zorder=5)
        axB.plot([x, x], [y0 + 0.06, y0 + lv * laneH], color=C[k], lw=1.4, zorder=2)
panel_label(axB, "b", dy=30)

for ext in ("pdf", "png"):
    fig.savefig(f"../figures/fig2_timeline.{ext}", facecolor="white")
print("saved")
