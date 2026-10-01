"""Word-list coding of the BigKinds census (articles 9 Feb-26 Mar 2026 matching (BTS OR 방탄소년단) AND 광화문 AND 26만).
Same word lists as corpus/frame_coding.py; expectation and conditional wording are coded on the headline and sentences
that mention 26만, the other codes on the headline and full text."""
import json, re, pandas as pd, sys
sys.path.insert(0, ".")
PAT = {
 "forecast_strict": r"예상|전망|예측|몰릴 것|모일 것|운집할 것|찾을 것|될 것으로|내다|점쳐|관측",
 "forecast_any": r"예상|전망|예측|몰릴 것|모일 것|운집할 것|찾을 것|될 것으로|추정|추산|내다|점쳐|관측",
 "capacity":  r"경우|가정|수용|꽉 들어서|모이면|확산될|늘어설|이어질 경우|㎡당|제곱미터|1㎡|밀집도|면적",
 "maximum":   r"최대\s?26만|26만\s?명?까지",
 "basis":     r"(?:㎡|제곱미터|m²)[^.]{0,40}(?:26만|추산|산출|계산|예측치)|(?:26만|추산|산출|예측치)[^.]{0,60}(?:㎡|제곱미터|m²)",
 "ticketed":  r"3만\s?5000|3만\s?5천|35,000|3만\s?4000|3만\s?4천|2만\s?2000|2만\s?2천|티켓|좌석|예매",
 "caveat":    r"모르|장담|불확실|확실하지|미지수|안 올|못 미칠|오지 않",
 "error":     r"빗나|실패|오차|부정확|못 미|절반에도|과대|한참|엉터리|틀린|헛|뻥튀기|예상했는데|예상과 달리|예상보다 적|에 그쳐|에 그쳤",
 "overreact": r"과잉|과다|과도|낭비|혈세|세금|동원 논란|공백|피로",
 "prudence":  r"무사고|사고 없이|무사히|안전하게 마무리|이태원|과한 게|부족한 것보다|부족한 것보단|최악|선방|성숙|교훈",
 "counttype": r"누적|순간|실시간|동시간|체류|기준 시각|오후 8시",
 "g_staff":   r"공무원|차출|초과근무|특별휴가|노조|인력 동원|직원 동원",
 "g_cost":    r"세금|혈세|예산|비용",
 "g_merchant":r"상인|매출|자영업|장사|손님|상권",
 "a_police":  r"경찰",
 "a_city":    r"서울시",
}
d = pd.DataFrame(json.load(open("bk.json", encoding="utf-8"))["data"])
d["content"] = d.content.fillna("").str.replace(r"<br\s*/?>", " ", regex=True)
d["text"] = d.title + ". " + d.content
d = d[d.text.str.contains(r"26만(?!원|원대|건|회|장|개|표|가구|대)")]
n_raw = len(d)
d["tnorm"] = d.title.str.replace(r"\W", "", regex=True)
d = d.drop_duplicates(["provider", "tnorm"])
DIGEST = r"미리보는|주요뉴스|주요 뉴스|헤드라인|조간|오늘의 뉴스|뉴스 브리핑|\[브리핑\]"
n_digest = int(d.title.str.contains(DIGEST).sum()); d = d[~d.title.str.contains(DIGEST)]
print("digest items removed:", n_digest)
d["cnorm"] = d.content.str.replace(r"\W", "", regex=True).str[:300]
d = d[~((d.cnorm.str.len() > 100) & d.duplicated("cnorm"))]
def sents(t): return re.split(r"(?<=[.!?다])\s+", t)
POST = r"4만|10만\s?4|6만\s?2|7만\s?6|그쳤|밑돌|못 미|끝난|마무리|열린 |열렸|성료|무사히"
rows = []
for _, r in d.iterrows():
    fig = " ".join([r.title] + [s for s in sents(r.content) if re.search(r"26만|23만", s)])
    out = dict(news_id=r.news_id, date=str(r.date), provider=r.provider, title=r.title, url=r.url,
               postmark=int(bool(re.search(POST, r.text))))
    for k, p in PAT.items():
        src = fig if k in ("forecast_strict", "forecast_any", "capacity", "a_police", "a_city") else r.text
        out[k] = int(bool(re.search(p, src)))
    rows.append(out)
C = pd.DataFrame(rows)
C["period"] = C.date.map(lambda x: "pre" if x <= "20260320" else ("event day" if x == "20260321" else "after"))
# items indexed after the event whose title announces the event and whose text has no sign of it having taken place
late = (C.period == "after") & (C.postmark == 0) & C.title.str.contains(r"예고|D-\d|온다|준비하는|발령|앞두고|대책")
print("after-period items without post-event markers (reassigned to pre):", int(late.sum()), C[late].title.tolist()[:8])
C.loc[late, "period"] = "pre"
# manual check: a pre-event planning article indexed on 26 March (its text describes the measures in the future tense)
C.loc[C.title.str.startswith("26만 운집 ‘BTS 공연’ 대책"), "period"] = "pre"
C["error_or_over"] = ((C.error == 1) | (C.overreact == 1)).astype(int)
BROAD = {"YTN", "KBS", "MBC", "SBS", "OBS"}; C["broadcast"] = C.provider.isin(BROAD).astype(int)
C.to_csv("bigkinds_coded.csv", index=False, encoding="utf-8-sig")
print("raw relevant", n_raw, "after dedup", len(C), "outlets", C.provider.nunique(), "broadcast", C.broadcast.sum())
print(C.period.value_counts().to_dict())
for per in ["pre", "event day", "after"]:
    g = C[C.period == per]; n = len(g)
    cols = ["forecast_any","forecast_strict","maximum","capacity","basis","ticketed","caveat"] if per == "pre" else ["forecast_strict","basis","error","overreact","error_or_over","prudence","counttype","g_staff","g_cost","g_merchant"]
    print(per, n, {c: f"{int(g[c].sum())} ({g[c].mean()*100:.0f}%)" for c in cols})
pre = C[C.period == "pre"]
print("pre, forecast strict w/o capacity:", int(((pre.forecast_strict==1)&(pre.capacity==0)).sum()), "| with capacity:", int(((pre.forecast_strict==1)&(pre.capacity==1)).sum()))
aft = C[C.period == "after"]; cr = aft[aft.error_or_over == 1]
print("after critical", len(cr), "error", int(cr.error.sum()), "over without error", int(((cr.error==0)&(cr.overreact==1)).sum()), "staff", int(cr.g_staff.sum()), "cost", int(cr.g_cost.sum()), "merchant", int(cr.g_merchant.sum()))
print("broadcast pre forecast:", C[(C.broadcast==1)&(C.period=="pre")].forecast_strict.mean().round(2), "n", len(C[(C.broadcast==1)&(C.period=="pre")]))

print("pre base rates: overreact", int(pre.overreact.sum()), f"({pre.overreact.mean()*100:.0f}%)", "error", int(pre.error.sum()))
print("pre expectation without 'up to' and without conditional:", int(((pre.forecast_strict==1)&(pre.maximum==0)&(pre.capacity==0)).sum()))
for per in ["pre","event day","after"]:
    g=C[C.period==per]; print(per, "attributed police", f"{g.a_police.mean()*100:.0f}%", "city", f"{g.a_city.mean()*100:.0f}%")
