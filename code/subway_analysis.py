"""Event-day (2026-03-21, Sat) alightings vs. baseline Saturdays (median, IQR range).
Baseline: all Saturdays 2026-03-07..05-30 except event day. Output: subway_event_vs_baseline.csv"""
import pandas as pd
d = pd.read_csv("../data/raw/subway_daily.csv"); d["key"] = d.line + " " + d.station
sat = d[d.weekday == "Sat"]
base = sat[sat.date != "2026-03-21"]
ev = sat[sat.date == "2026-03-21"].set_index("key")
rows = []
for k, g in base.groupby("key"):
    for col in ("alightings", "boardings"):
        med, lo, hi = g[col].median(), g[col].min(), g[col].max()
        rows.append(dict(station=k, measure=col, event=int(ev.loc[k, col]), base_median=int(med),
                         base_min=int(lo), base_max=int(hi), diff=int(ev.loc[k, col] - med),
                         ratio=round(ev.loc[k, col] / med, 2), n_base=len(g)))
r = pd.DataFrame(rows)
core = ["5호선 광화문(세종문화회관)", "3호선 경복궁(정부서울청사)", "1호선 시청", "2호선 시청"]
r["group"] = r.station.map(lambda s: "core (no-stop 14/15-22h)" if s in core else "peripheral")
r.to_csv("../data/processed/subway_event_vs_baseline.csv", index=False, encoding="utf-8-sig")
a = r[r.measure == "alightings"]
print(a.to_string(index=False))
print(a.groupby("group")[["event", "base_median", "diff"]].sum())
