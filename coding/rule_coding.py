"""Rule-based (dictionary) coding of artist messages, applied mechanically to the Korean text,
compared with the manual coding. Categories as in Supplementary Table S2."""
import json, re, itertools
import pandas as pd

CATS = ["Follow staff and officials", "Do not push; look after each other", "Stay back; use the screens",
        "General request to stay safe", "Health and comfort", "Thanks to authorities and staff",
        "Safe precedent; trust in fans", "Stay home or watch remotely"]
# Dictionary fixed from the category definitions (Korean stems / short patterns)
DICT = {
 0: [r"안내를?\s*(꼭\s*)?따라", r"통제에\s*(잘\s*)?따라", r"안전요원\S*\s*(에게|께)\s*(반드시\s*)?알려", r"지시에?\s*따라"],
 1: [r"밀(거나|지)", r"서로\S{0,3}\s*(배려|지켜)", r"배려", r"천천히"],
 2: [r"스크린", r"무대\s*앞으로\s*모이지", r"각자\s*자리"],
 3: [r"안전하", r"안전에\s*(꼭\s*)?유의", r"안전이\s*(제일|최우선)", r"다치는\s*(일|사람)", r"사고\s*없이", r"무리하지"],
 4: [r"따[뜻듯]하게", r"컨디션", r"쌀쌀", r"건강", r"감기"],
 5: [r"(경찰|소방|스태프|관계자|안전요원|정부|지자체|도움\s*주신|고생해)[^.!?]{0,40}감사"],
 6: [r"좋은\s*사례", r"믿어", r"믿는다", r"믿습니다"],
 7: [r"집에서", r"넷플릭스", r"생중계", r"온라인", r"중계", r"오지\s*말", r"방문\S{0,3}\s*자제", r"시청", r"화면으로\s*보"],
}
MANUAL = {  # manual coding after checking the original Weverse text
 "RM, 19 Mar":        [1,1,0,1,0,1,0,0],
 "Jin, 19 Mar":       [0,0,0,1,0,1,0,0],
 "V, 20 Mar":         [0,1,0,1,0,0,0,0],
 "Jimin, 20 Mar":     [1,1,0,1,1,0,0,0],
 "Group live, 20 Mar":[1,0,1,1,0,0,1,0],
 "Suga, 21 Mar":      [0,0,0,1,1,1,0,0],
 "J-Hope, 21 Mar":    [0,1,1,1,0,0,0,0],
 "Jungkook, 21 Mar":  [0,0,0,1,0,1,0,0],
}
msgs = json.load(open("messages.json", encoding="utf-8"))
rows, hits = [], []
for m in msgs:
    r = []
    for c in range(8):
        found = [p for p in DICT[c] if re.search(p, m["ko"])]
        r.append(int(bool(found)))
        if found: hits.append((m["unit"], CATS[c], "; ".join(found)))
    rows.append(r)
R = pd.DataFrame(rows, index=[m["unit"] for m in msgs], columns=CATS)
M = pd.DataFrame([MANUAL[m["unit"]] for m in msgs], index=R.index, columns=CATS)
man, rul = M.values.ravel(), R.values.ravel()
agree = (man == rul).mean()
po = agree; pe_k = man.mean()*rul.mean() + (1-man.mean())*(1-rul.mean())
kappa = (po - pe_k) / (1 - pe_k)  # Cohen's kappa
# Gwet's AC1 (robust to skewed prevalence)
pa = agree; pi = (man.mean() + rul.mean()) / 2; pe = 2 * pi * (1 - pi); ac1 = (pa - pe) / (1 - pe)
per = pd.DataFrame({"manual_n": M.sum(), "rule_n": R.sum(), "agree_units": (M == R).sum()})
dis = [(u, c, int(M.loc[u, c]), int(R.loc[u, c])) for u in R.index for c in CATS if M.loc[u, c] != R.loc[u, c]]
print(per.to_string()); print(f"decisions={man.size} agreement={agree:.3f} kappa={kappa:.3f} AC1={ac1:.3f}")
print("disagreements:", dis)
M.to_csv("manual_coding.csv", encoding="utf-8-sig"); R.to_csv("rule_coding.csv", encoding="utf-8-sig")
pd.DataFrame(hits, columns=["unit", "category", "matched_pattern"]).to_csv("rule_hits.csv", index=False, encoding="utf-8-sig")
json.dump({"decisions": int(man.size), "agreement": agree, "kappa": kappa, "ac1": ac1, "disagreements": dis},
          open("reliability.json", "w"), indent=1, ensure_ascii=False)
