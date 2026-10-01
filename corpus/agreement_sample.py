"""Census validation: independent second coder (bigkinds_sample_second_coder.csv, 120 sampled census articles, full text)
against the word-list coding (bigkinds_coded.csv). Run inside corpus/. Reports human-coded proportions, per-category agreement, Cohen's kappa, Gwet's AC1 and Krippendorff's alpha."""
import json, pandas as pd, numpy as np
key = {r["item"]: dict(type=r["type"], news_id=str(r["news_id"])) for r in pd.read_csv("bigkinds_sample_key.csv", encoding="utf-8-sig", dtype={"news_id": str}).to_dict("records")}
BK = pd.read_csv("bigkinds_coded.csv", encoding="utf-8-sig", dtype={"news_id": str}).set_index("news_id")
H = pd.read_csv("bigkinds_sample_second_coder.csv", encoding="utf-8-sig").set_index("item")
MAP = {"A": {"F1": "forecast_strict", "F2": "capacity", "F3": "basis", "F4": "ticketed", "F5": "caveat", "F6": "maximum"},
       "B": {"G1": "error", "G2": "overreact", "G3": "prudence", "G4": "basis", "G5": "counttype", "G6": "g_staff", "G7": "g_cost", "G8": "g_merchant"}}
rows = []
for item, k in key.items():
    if k["news_id"] not in BK.index: continue  # excluded from the census after coding (e.g. news digest)
    auto = BK.loc[k["news_id"]]
    for hc, ac in MAP[k["type"]].items():
        v = H.loc[item, hc]
        if pd.isna(v): continue
        rows.append(dict(item=item, type=k["type"], cat=hc, human=int(v), auto=int(auto[ac]), full=1))
R = pd.DataFrame(rows)
def kappa(a, b):
    po = (a == b).mean(); pe = a.mean()*b.mean() + (1-a.mean())*(1-b.mean()); return (po-pe)/(1-pe) if pe < 1 else float("nan")
def ac1(a, b):
    po = (a == b).mean(); pi = (a.mean()+b.mean())/2; pe = 2*pi*(1-pi); return (po-pe)/(1-pe)
def kalpha(a, b):
    v = np.concatenate([a, b]); n = len(v); p = v.mean(); De = 2*p*(1-p)*n/(n-1); Do = (a != b).mean()
    return 1 - Do/De if De > 0 else float("nan")
out = []
for c, g in R.groupby("cat"):
    a, b = g.human.values, g.auto.values
    out.append(dict(cat=c, n=len(g), human_present=int(a.sum()), human_share=round(a.mean(), 3), wordlist_present=int(b.sum()),
                    agree=int((a == b).sum()), kappa=round(kappa(a, b), 2), ac1=round(ac1(a, b), 2), alpha=round(kalpha(a, b), 2)))
O = pd.DataFrame(out); print(O.to_string(index=False)); O.to_csv("agreement_sample_output.csv", index=False)
a, b = R.human.values, R.auto.values
print("pooled", int((a == b).sum()), "/", len(R), "kappa", round(kappa(a, b), 3), "AC1", round(ac1(a, b), 3))
B = R[R.type == "B"].pivot(index="item", columns="cat", values="human")
crit = B[(B.G1 == 1) | (B.G2 == 1)]
print("human: critical articles", len(crit), "| G1", int(crit.G1.sum()), "| G2 without G1", int(((crit.G1 == 0) & (crit.G2 == 1)).sum()), "| G6", int(crit.G6.sum()), "| G7", int(crit.G7.sum()), "| G8", int(crit.G8.sum()))
