"""Dictionary coding of how the 260,000 figure was framed in news reports (pre-event 9 Feb-20 Mar; post-event 21-26 Mar 2026).
Codes are applied to the headline and the verbatim sentences recorded for each article."""
import json, re, pandas as pd
PAT = {
 "forecast":  r"예상|전망|예측|몰릴 것|모일 것|운집할 것|찾을 것|될 것으로|추정|추산|내다|점쳐|관측",
 "capacity":  r"경우|가정|수용|꽉 들어서|모이면|확산될|늘어설|이어질 경우|㎡당|제곱미터|1㎡|밀집도|면적",
 "basis":     r"(?:㎡|제곱미터|m²)[^.]{0,40}(?:26만|추산|산출|계산|예측치)|(?:26만|추산|산출|예측치)[^.]{0,60}(?:㎡|제곱미터|m²)",
 "ticketed":  r"3만\s?5000|3만\s?5천|35,000|3만\s?4000|3만\s?4천|2만\s?2000|2만\s?2천|티켓|좌석|예매",
 "caveat":    r"모르|장담|불확실|확실하지|미지수|안 올|못 미칠|오지 않",
 "error":     r"빗나|실패|오차|부정확|못 미|절반에도|과대|한참|엉터리|틀린|헛|뻥튀기",
 "overreact": r"과잉|과다|과도|낭비|혈세|세금|동원 논란|공백|피로",
 "prudence":  r"무사고|사고 없이|무사히|안전하게 마무리|이태원|과한 게|부족한 것보다|부족한 것보단|최악|선방|성숙|교훈",
 "counttype": r"누적|순간|실시간|동시간|체류|기준 시각|오후 8시",
}
def code(rec, fields):
    fig = [s for s in rec["sentences"] if re.search(r"26만|23만|260,000", s)]
    head = rec["headline"]
    out = {"outlet": rec["outlet"], "date": rec["date"], "url": rec["url"], "headline": head}
    for k in fields:
        txt = " ".join([head] + (fig if k in ("forecast", "capacity") else rec["sentences"]))
        out[k] = int(bool(re.search(PAT[k], txt)))
    att = set(rec.get("attribution", []))
    out["attr_police"] = int(any(a.startswith("police") for a in att))
    out["attr_city"] = int(any("Seoul city" in a for a in att))
    out["attr_mcst"] = int(any("MCST" in a or "문체부" in a for a in att))
    out["attr_mois"] = int(any(a.startswith("MOIS") for a in att))
    out["attr_none"] = int(all(a.startswith("none") for a in att) if att else 1)
    return out
pre = [code(r, ["forecast","capacity","basis","ticketed","caveat"]) for r in json.load(open("corpus/pre_event.json", encoding="utf-8"))]
post = [code(r, ["forecast","capacity","basis","error","overreact","prudence","counttype"]) for r in json.load(open("corpus/post_event.json", encoding="utf-8"))]
P, Q = pd.DataFrame(pre), pd.DataFrame(post)
P["frame"] = P.apply(lambda r: "forecast only" if r.forecast and not r.capacity else "capacity/conditional only" if r.capacity and not r.forecast else "both" if r.forecast and r.capacity else "figure only", axis=1)
P.to_csv("corpus/pre_coded.csv", index=False, encoding="utf-8-sig"); Q.to_csv("corpus/post_coded.csv", index=False, encoding="utf-8-sig")
print("PRE n=",len(P)); print(P.frame.value_counts()); print(P[["basis","ticketed","caveat","attr_police","attr_city","attr_mcst","attr_none"]].sum())
print("pre Feb vs Mar basis:", P.groupby(P.date.str[:7]).basis.agg(['sum','count']).to_dict())
print("POST n=",len(Q)); print(Q[["forecast","capacity","basis","error","overreact","prudence","counttype","attr_police","attr_city","attr_mois","attr_none"]].sum())
print("both error&prudence:", int(((Q.error==1)&(Q.prudence==1)).sum()), " overreact&prudence:", int(((Q.overreact==1)&(Q.prudence==1)).sum()))
# --- Additional codes (v0.9): 'up to' wording, strict forecast wording, grounds of post-event criticism ---
X = {
 "maximum": r"최대\s?26만|26만\s?명?까지|최대\s?인원",
 "forecast_strict": r"예상|전망|예측|몰릴 것|모일 것|운집할 것|찾을 것|될 것으로|내다|점쳐|관측",
}
G = {
 "g_staff": r"공무원|차출|초과근무|특별휴가|노조|인력 동원|직원 동원",
 "g_merchant": r"상인|매출|자영업|장사|손님|상권",
 "g_inconv": r"불편|교통 통제|통제로|우회|무정차",
 "g_cost": r"세금|혈세|예산|비용",
}
def extra(rec, keys, all_sent):
    fig = [s for s in rec["sentences"] if re.search(r"26만|23만|260,000", s)]
    txt = " ".join([rec["headline"]] + (rec["sentences"] if all_sent else fig))
    return {k: int(bool(re.search(PAT2[k], txt))) for k in keys}
PAT2 = {**X, **G}
pre_raw = json.load(open("corpus/pre_event.json", encoding="utf-8")); post_raw = json.load(open("corpus/post_event.json", encoding="utf-8"))
for k in X: P[k] = [extra(r, [k], False)[k] for r in pre_raw]
for k in G: Q[k] = [extra(r, [k], True)[k] for r in post_raw]
Q["error_or_over"] = ((Q.error == 1) | (Q.overreact == 1)).astype(int)
print("maximum:", int(P.maximum.sum()), " forecast strict:", int(P.forecast_strict.sum()),
      " forecast via 추정/추산 only:", int(((P.forecast == 1) & (P.forecast_strict == 0)).sum()),
      " maximum among forecast:", int(((P.forecast == 1) & (P.maximum == 1)).sum()),
      " forecast_strict without maximum:", int(((P.forecast_strict == 1) & (P.maximum == 0)).sum()))
print(Q[list(G)].sum().to_dict())
crit = Q[Q.error_or_over == 1]
print("among critical (n=%d):" % len(crit), crit[list(G)].sum().to_dict(), " error only:", int((crit.error==1).sum()), " no other ground:", int((crit[list(G)].sum(axis=1)==0).sum()))
P.to_csv("corpus/pre_coded.csv", index=False, encoding="utf-8-sig"); Q.to_csv("corpus/post_coded.csv", index=False, encoding="utf-8-sig")
