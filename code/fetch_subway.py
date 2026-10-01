"""Seoul Open Data Plaza API 'CardSubwayStatsNew' (daily card-based boardings/alightings
per station). Public sample key, filtered by line+station. Output: subway_daily.csv"""
import requests, urllib.parse, datetime as dt, csv, os, time
ST = [("5호선","광화문(세종문화회관)"),("3호선","경복궁(정부서울청사)"),("1호선","시청"),("2호선","시청"),
      ("1호선","종각"),("2호선","을지로입구"),("3호선","안국"),("5호선","서대문")]
start, end = dt.date(2026,1,3), dt.date(2026,5,30)
days = [start + dt.timedelta(d) for d in range((end-start).days+1)]
days = [d for d in days if d.weekday()==5] + [dt.date(2026,3,d) for d in (16,17,18,19,20,22)]
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw", "subway_daily.csv")
with open(fn, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["date","weekday","line","station","boardings","alightings"])
    for d in sorted(days):
        for ln, st in ST:
            u = "http://openapi.seoul.go.kr:8088/sample/json/CardSubwayStatsNew/1/5/%s/%s/%s" % (
                d.strftime("%Y%m%d"), urllib.parse.quote(ln), urllib.parse.quote(st))
            try: r = requests.get(u, timeout=20).json()["CardSubwayStatsNew"]["row"][0]
            except Exception: print("miss", d, ln, st); continue
            w.writerow([d.isoformat(), d.strftime("%a"), ln, st, r["GTON_TNOPE"], r["GTOFF_TNOPE"]])
print("done")
