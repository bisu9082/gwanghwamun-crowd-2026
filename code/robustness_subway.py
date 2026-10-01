"""Robustness checks for subway alightings: per-day group totals, March-only baseline,
outer ring of stations, far control stations (difference-in-differences on log ratio)."""
import pandas as pd, numpy as np
a = pd.read_csv("subway_daily.csv"); b = pd.read_csv("subway_daily_ext.csv")
d = pd.concat([a, b]); d = d[d.weekday == "Sat"]; d["key"] = d.line + " " + d.station
G = {"nostop": ["5호선 광화문(세종문화회관)","3호선 경복궁(정부서울청사)","1호선 시청","2호선 시청"],
     "nearby": ["1호선 종각","2호선 을지로입구","5호선 서대문","3호선 안국"],
     "ring2": ["1호선 종로3가","3호선 종로3가","5호선 종로3가","1호선 서울역","4호선 서울역","4호선 명동","4호선 회현(남대문시장)"],
     "control": ["2호선 강남","2호선 홍대입구","2호선 잠실(송파구청)","2호선 건대입구","5호선 여의도"]}
EV = "2026-03-21"; MAR = ["2026-03-07","2026-03-14","2026-03-28"]
rows = []
tot = {g: d[d.key.isin(k)].groupby("date").alightings.sum() for g, k in G.items()}
tot["core8"] = tot["nostop"] + tot["nearby"]
tot["core8_ring2"] = tot["core8"] + tot["ring2"]
for g, s in tot.items():
    base = s.drop(EV); mar = s[MAR]
    rows.append(dict(group=g, event=s[EV], median_all=base.median(), min_all=base.min(), max_all=base.max(),
                     diff_all=s[EV]-base.median(), median_mar=mar.median(), diff_mar=s[EV]-mar.median(),
                     rank_from_top=int((s >= s[EV]).sum()), n=len(s)))
R = pd.DataFrame(rows); print(R.round(0).to_string())
# DiD on log ratio vs far control
for g in ["nostop","nearby","core8","core8_ring2"]:
    for lab, bd in [("all", [x for x in tot[g].index if x != EV]), ("march", MAR)]:
        eff = np.log(tot[g][EV]/tot[g][bd].median()) - np.log(tot["control"][EV]/tot["control"][bd].median())
        print(f"DiD {g:12s} base={lab:6s} ratio_vs_control={np.exp(eff):.3f}")
print("control event/median:", round(tot["control"][EV]/tot["control"].drop(EV).median(),3))
pd.DataFrame(tot).to_csv("subway_group_totals_by_date.csv", encoding="utf-8-sig")
R.to_csv("subway_robustness.csv", index=False, encoding="utf-8-sig")
