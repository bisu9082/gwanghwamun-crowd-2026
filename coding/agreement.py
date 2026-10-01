"""Agreement between the manual coding (manual_coding.csv) and an independent coder (coding_sheet.csv).
Reports per-category percent agreement, pooled Cohen's kappa and Krippendorff's alpha (nominal)."""
import json, pandas as pd, numpy as np
key = json.load(open("coder2_unit_key.json", encoding="utf-8"))
A = pd.read_csv("manual_coding.csv", index_col=0, encoding="utf-8-sig")
B = pd.read_csv("coder2_coding_sheet.csv", encoding="utf-8-sig").set_index("message")
B.index = [key[m] for m in B.index]; B = B[[f"C{i}" for i in range(1, 9)]].astype(int)
A = A.loc[B.index]; A.columns = B.columns
a, b = A.values.ravel(), B.values.ravel()
po = (a == b).mean(); pe = a.mean()*b.mean() + (1-a.mean())*(1-b.mean()); kappa = (po-pe)/(1-pe)
# Krippendorff alpha, nominal, 2 coders, binary
n = np.array([[((a==i)&(b==j)).sum() + ((a==j)&(b==i)).sum() for j in (0,1)] for i in (0,1)])
nc = n.sum(1); N = nc.sum(); Do = n[0,1]+n[1,0]; De = (2*nc[0]*nc[1])/(N-1)
alpha = 1 - Do/De if De else float("nan")
print(pd.DataFrame({"agree_units": (A==B).sum(), "manual_n": A.sum(), "coder2_n": B.sum()}))
print(f"decisions={a.size} agreement={po:.3f} kappa={kappa:.3f} alpha={alpha:.3f}")
print("disagreements:", [(u, c, int(A.loc[u,c]), int(B.loc[u,c])) for u in A.index for c in A.columns if A.loc[u,c]!=B.loc[u,c]])
