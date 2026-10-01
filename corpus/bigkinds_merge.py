"""Compare a BigKinds export (Korea Press Foundation, https://www.bigkinds.or.kr) with the Exa-based corpus.
Usage: python bigkinds_merge.py NewsResult_*.xlsx
Keeps articles 9 Feb-26 Mar 2026 whose title or body excerpt mentions 26만 (or 260,000), collapses duplicates by
(outlet, title), and lists articles missing from corpus/pre_event.json and corpus/post_event.json."""
import sys, re, json, pandas as pd
bk = pd.concat([pd.read_excel(f) for f in sys.argv[1:]])
col = {c: c.strip() for c in bk.columns}; bk = bk.rename(columns=col)
txt = (bk["제목"].astype(str) + " " + bk.get("본문", "").astype(str))
bk = bk[txt.str.contains(r"26만|260,000|26만명|26만 명")]
bk["date"] = pd.to_datetime(bk["일자"].astype(str).str[:8], format="%Y%m%d")
bk = bk[(bk.date >= "2026-02-09") & (bk.date <= "2026-03-26")]
bk["tnorm"] = bk["제목"].astype(str).str.replace(r"\W", "", regex=True)
bk = bk.drop_duplicates(["언론사", "tnorm"])
corp = json.load(open("corpus/pre_event.json", encoding="utf-8")) + json.load(open("corpus/post_event.json", encoding="utf-8"))
ct = {re.sub(r"\W", "", c["headline"]) for c in corp}
bk["in_corpus"] = bk.tnorm.isin(ct)
print("BigKinds articles mentioning 26만:", len(bk), "| outlets:", bk["언론사"].nunique(), "| already in corpus:", int(bk.in_corpus.sum()))
print(bk.groupby(bk.date < "2026-03-21").size().rename({True: "pre-event", False: "event day and after"}))
bk[~bk.in_corpus][["일자", "언론사", "제목", "URL"]].to_csv("bigkinds_missing_from_corpus.csv", index=False, encoding="utf-8-sig")
bk.to_csv("bigkinds_26man.csv", index=False, encoding="utf-8-sig")
