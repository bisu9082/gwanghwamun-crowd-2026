"""Living population, Saturdays Mar-May 2025 and Mar-May 2026. Groups: core (3 corridor dongs), ring (8 adjacent dongs),
hubs (5 distant commercial/tourist dongs), rest (all other Seoul dongs). Baselines: other 2026 Saturdays, 2025 Saturdays,
both. Comparison with hubs on the log ratio, and a placebo distribution treating each baseline Saturday as a pseudo-event."""
import glob, pandas as pd, numpy as np
d = pd.concat([pd.read_csv(f, dtype={"date": str, "dong": str}) for f in glob.glob("sat_*_20*.csv")])
CORE = ["11110530", "11110615", "11140520"]
RING = ["11140550", "11140540", "11140605", "11110515", "11110540", "11110600", "11110580", "11110630"]
HUBS = ["11440660", "11410585", "11170650", "11560540", "11680640"]
def grp(x):
    return "core" if x in CORE else "ring" if x in RING else "hubs" if x in HUBS else "rest"
d["grp"] = d.dong.map(grp)
print("suppressed cells in core/ring/hubs:", d[d.grp != "rest"].supp.sum())
T = d.groupby(["grp", "date", "hour"]).tot.sum()
EV = "20260321"
dates = sorted(d.date.unique()); b26 = [x for x in dates if x.startswith("2026") and x != EV]; b25 = [x for x in dates if x.startswith("2025")]
print("n 2026 baseline", len(b26), "n 2025 baseline", len(b25))
W = T.unstack("hour")
def series(g, h): return W.loc[g][h]
rows = []
for h in range(8, 24):
    c = series("core", h); r = series("ring", h); k = series("hubs", h)
    for lab, base in [("2026", b26), ("2025", b25), ("both", b26 + b25)]:
        ratio_c = c[EV] / c[base].median(); ratio_k = k[EV] / k[base].median(); ratio_r = r[EV] / r[base].median()
        rows.append(dict(hour=h, base=lab, core_event=c[EV], core_med=c[base].median(), core_diff=c[EV] - c[base].median(),
                         core_min=c[base].min(), core_max=c[base].max(), hubs_ratio=ratio_k, ring_ratio=ratio_r,
                         core_vs_hubs=ratio_c / ratio_k, adj_diff=c[EV] - c[EV] / (ratio_c / ratio_k)))
R = pd.DataFrame(rows); R.to_csv("lp_design_results.csv", index=False)
print(R[R.hour.isin([12, 14, 16, 19, 20, 21])].round(3).to_string())
# placebo: statistic = log(core/core_med) - log(hubs/hubs_med), baseline = all other Saturdays (both years)
allb = b26 + b25
def stat(day, h, pool):
    c = series("core", h); k = series("hubs", h); base = [x for x in pool if x != day]
    return np.log(c[day] / c[base].median()) - np.log(k[day] / k[base].median())
out = []
for h in (14, 20):
    ev = stat(EV, h, allb); pl = np.array([stat(x, h, allb + [EV]) if False else stat(x, h, allb) for x in allb])
    rank = (pl <= ev).mean() if h == 14 else (pl >= ev).mean()
    out.append(dict(hour=h, event_stat=np.exp(ev), placebo_min=np.exp(pl.min()), placebo_max=np.exp(pl.max()), n_placebo=len(pl), share_as_extreme=rank))
    print(h, "event ratio", round(np.exp(ev), 3), "placebo range", round(np.exp(pl.min()), 3), round(np.exp(pl.max()), 3), "share of placebo days at least as extreme", round(rank, 3))
pd.DataFrame(out).to_csv("lp_placebo.csv", index=False)
pd.DataFrame({g: W.loc[g][14] for g in ["core","ring","hubs","rest"]}).to_csv("lp_14h_by_date.csv")
pd.DataFrame({g: W.loc[g][20] for g in ["core","ring","hubs","rest"]}).to_csv("lp_20h_by_date.csv")
