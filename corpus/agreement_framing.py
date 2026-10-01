"""Agreement between dictionary coding (pre_coded.csv, post_coded.csv) and the independent human coder (framing_sheet.csv)."""
import json, pandas as pd, numpy as np
key = json.load(open("framing_sample_key.json", encoding="utf-8"))
P = pd.read_csv("pre_coded.csv", encoding="utf-8-sig"); Q = pd.read_csv("post_coded.csv", encoding="utf-8-sig")
H = pd.read_csv("framing_sheet_coded.csv", encoding="utf-8-sig").set_index("item")
MAP = {"A": {"F1": "forecast", "F2": "capacity", "F3": "basis", "F4": "ticketed", "F5": "caveat"},
       "B": {"G1": "error", "G2": "overreact", "G3": "prudence", "G4": "basis", "G5": "counttype"}}
rows = []
for item, k in key.items():
    src = P if k["type"] == "A" else Q
    auto = src[src.url == k["url"]].iloc[0]
    for hc, ac in MAP[k["type"]].items():
        rows.append(dict(item=item, type=k["type"], cat=hc, human=int(H.loc[item, hc]), auto=int(auto[ac])))
R = pd.DataFrame(rows)
def kappa(a, b):
    po = (a == b).mean(); pe = a.mean()*b.mean() + (1-a.mean())*(1-b.mean())
    return (po - pe)/(1 - pe) if pe < 1 else float("nan")
def ac1(a, b):
    """Gwet's AC1 for two raters and a binary code (Gwet 2008)."""
    po = (a == b).mean(); pi = (a.mean() + b.mean()) / 2; pe = 2 * pi * (1 - pi)
    return (po - pe) / (1 - pe)
for c, g in R.groupby("cat"):
    print(c, f"agree {int((g.human==g.auto).sum())}/{len(g)}", f"kappa {kappa(g.human.values, g.auto.values):.2f}", f"AC1 {ac1(g.human.values, g.auto.values):.2f}", f"human n={g.human.sum()} auto n={g.auto.sum()}")
print("pooled agreement", round((R.human == R.auto).mean(), 3), "kappa", round(kappa(R.human.values, R.auto.values), 3), "AC1", round(ac1(R.human.values, R.auto.values), 3))
print("disagreements: coder present, word list absent =", int(((R.human==1)&(R.auto==0)).sum()), "; word list present, coder absent =", int(((R.human==0)&(R.auto==1)).sum()))
print(R[R.human != R.auto].to_string())
