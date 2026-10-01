"""Daily card-based alightings (Seoul Open Data Plaza OA-12914 monthly files, CARD_SUBWAY_MONTH_YYYYMM.csv), Saturdays Mar-May 2025 and 2026.
Groups as in the article; pools as in lp_design2.py (ordinary Saturdays exclude rally, parade and holiday Saturdays)."""
import glob, pandas as pd, numpy as np
fr=[pd.read_csv(f, encoding="utf-8-sig", index_col=False, dtype=str) for f in sorted(glob.glob("m_*.csv"))]
d=pd.concat(fr); d.columns=["date","line","station","board","alight","reg"]
d["board"]=d.board.astype(int); d["alight"]=d.alight.astype(int)
d["dt"]=pd.to_datetime(d.date); d=d[d.dt.dt.dayofweek==5]
G={"nostop":[("5호선","광화문(세종문화회관)"),("3호선","경복궁(정부서울청사)"),("1호선","시청"),("2호선","시청")],
   "nearby":[("1호선","종각"),("2호선","을지로입구"),("3호선","안국"),("5호선","서대문")],
   "outer":[("1호선","종로3가"),("3호선","종로3가"),("5호선","종로3가"),("1호선","서울역"),("4호선","서울역"),("4호선","명동"),("4호선","회현(남대문시장)")],
   "control":[("2호선","강남"),("2호선","홍대입구"),("2호선","잠실(송파구청)"),("2호선","건대입구"),("5호선","여의도")]}
key=set(k for v in G.values() for k in v)
d["k"]=list(zip(d.line,d.station)); s=d[d.k.isin(key)]
miss=[k for k in key if k not in set(s.k)]; print("missing station keys:", miss)
s[["date","line","station","board","alight"]].sort_values(["date","line","station"]).to_csv("subway_saturdays_2025_2026.csv", index=False, encoding="utf-8-sig")
T=pd.DataFrame({g: s[s.k.isin(v)].groupby("date").alight.sum() for g,v in G.items()}); T["all8"]=T.nostop+T.nearby
T.to_csv("subway_group_totals_2025_2026.csv")
EV="20260321"; GATHER=["20250301","20250308","20250315","20250322","20250329","20250405","20250426","20260516"]
others=[x for x in T.index if x!=EV]
P={"all_26":others,"ordinary":[x for x in others if x not in GATHER],"2026_all":[x for x in others if x.startswith("2026")],"2026_ordinary":[x for x in others if x.startswith("2026") and x not in GATHER]}
rows=[]
for g in ["nostop","nearby","all8","outer","control"]:
    for pn,pool in P.items():
        med=T.loc[pool,g].median(); rc=T.loc[EV,g]/med; rk=T.loc[EV,"control"]/T.loc[pool,"control"].median()
        rank=int((T.loc[pool,g]>T.loc[EV,g]).sum())+1
        rows.append(dict(group=g,pool=pn,n=len(pool),event=T.loc[EV,g],median=med,diff=T.loc[EV,g]-med,pmin=T.loc[pool,g].min(),pmax=T.loc[pool,g].max(),rank=f"{rank}/{len(pool)+1}",ratio_vs_control=rc/rk))
R=pd.DataFrame(rows); R.to_csv("subway_design2_results.csv",index=False)
pd.set_option("display.width",200); print(R.round(3).to_string())
# placebo on all8 and outer (ratio to control)
for g in ["all8","outer","nearby"]:
    for pn in ["ordinary","all_26"]:
        pool=P[pn]
        def st(day):
            b=[x for x in pool if x!=day]; return np.log(T.loc[day,g]/T.loc[b,g].median())-np.log(T.loc[day,"control"]/T.loc[b,"control"].median())
        ev=st(EV); pl=np.array([st(x) for x in pool])
        print(g,pn,"event",round(np.exp(ev),3),"placebo",round(np.exp(pl.min()),3),round(np.exp(pl.max()),3),"as low",int((pl<=ev).sum()),"as high",int((pl>=ev).sum()),"of",len(pl))
