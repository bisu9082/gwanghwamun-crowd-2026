"""Living population, Saturdays Mar-May 2025 and 2026, with a pre-specified pool of ordinary Saturdays.
Gathering Saturdays (excluded from the ordinary pool): public holiday or a documented gathering of 15,000 or more
(police unofficial estimate) in the Sejong-daero corridor, or a city parade/festival there:
2025-03-01 (holiday; rallies), 03-08, 03-15, 03-22, 03-29, 04-05 (impeachment rallies), 2025-04-26 and 2026-05-16 (Lotus Lantern parade).
Statistics: hourly core-dong totals and two pre-specified windows (11-17h sum, 19-21h sum); adjustment by five distant
comparison dongs (ratio of ratios); placebo distribution treating each pool Saturday as a pseudo-event."""
import glob, pandas as pd, numpy as np
d = pd.concat([pd.read_csv(f, dtype={"date": str, "dong": str}) for f in glob.glob("sat_*_20*.csv")])
CORE = ["11110530", "11110615", "11140520"]
RING = ["11140550", "11140540", "11140605", "11110515", "11110540", "11110600", "11110580", "11110630"]
HUBS = ["11440660", "11410585", "11170650", "11560540", "11680640"]
grp = lambda x: "core" if x in CORE else "ring" if x in RING else "hubs" if x in HUBS else "rest"
d["grp"] = d.dong.map(grp)
T = d.groupby(["grp", "date", "hour"]).tot.sum(); W = T.unstack("hour")
EV = "20260321"
GATHER = ["20250301","20250308","20250315","20250322","20250329","20250405","20250426","20260516"]
dates = sorted(d.date.unique()); others = [x for x in dates if x != EV]
POOLS = {"all_26": others, "ordinary": [x for x in others if x not in GATHER],
         "2026_all": [x for x in others if x.startswith("2026")],
         "2026_ordinary": [x for x in others if x.startswith("2026") and x not in GATHER]}
def S(g, key):
    if key == "w11_17": return W.loc[g][list(range(11, 18))].sum(axis=1)
    if key == "w19_21": return W.loc[g][[19, 20, 21]].sum(axis=1)
    return W.loc[g][key]
rows = []; plac = []
for key in list(range(8, 24)) + ["w11_17", "w19_21"]:
    c, k, r = S("core", key), S("hubs", key), S("ring", key)
    for pn, pool in POOLS.items():
        med = c[pool].median(); rc = c[EV]/med; rk = k[EV]/k[pool].median(); rr = r[EV]/r[pool].median()
        rank = int((c[pool] > c[EV]).sum()) + 1
        rows.append(dict(stat=key, pool=pn, n=len(pool), core_event=c[EV], core_med=med, diff=c[EV]-med,
                         q1=c[pool].quantile(.25), q3=c[pool].quantile(.75), pmin=c[pool].min(), pmax=c[pool].max(),
                         rank_of=f"{rank}/{len(pool)+1}", hubs_ratio=rk, ring_ratio=rr, adj_diff=c[EV]-c[EV]/(rc/rk)))
        if key in (14, 20, "w11_17", "w19_21"):
            def st(day):
                b = [x for x in pool if x != day]
                return np.log(c[day]/c[b].median()) - np.log(k[day]/k[b].median())
            ev = st(EV); pl = np.array([st(x) for x in pool])
            plac.append(dict(stat=key, pool=pn, n_placebo=len(pl), event_ratio=np.exp(ev), pl_min=np.exp(pl.min()), pl_max=np.exp(pl.max()),
                             n_as_low=int((pl <= ev).sum()), n_as_high=int((pl >= ev).sum())))
R = pd.DataFrame(rows); P = pd.DataFrame(plac)
R.to_csv("lp_design2_results.csv", index=False); P.to_csv("lp_placebo2.csv", index=False)
pd.set_option("display.width", 250)
print(R[R.stat.isin([12,14,16,17,19,20,21,22,23,"w11_17","w19_21"])].round(3).to_string())
print(P.round(3).to_string())
hh = W.loc["core"][list(range(8,24))].T; hh.to_csv("core_hourly_saturdays_2025_2026.csv")
