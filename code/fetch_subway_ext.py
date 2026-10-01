"""Extra stations for catchment ring and control comparison (same API as fetch_subway.py)."""
import requests, urllib.parse, datetime as dt, csv, os
ST = [("1호선","종로3가"),("3호선","종로3가"),("5호선","종로3가"),("1호선","서울역"),("4호선","서울역"),
      ("4호선","명동"),("4호선","회현(남대문시장)"),
      ("2호선","강남"),("2호선","홍대입구"),("2호선","잠실(송파구청)"),("2호선","건대입구"),("5호선","여의도")]
days = [dt.date(2026,3,7)+dt.timedelta(7*i) for i in range(13)]
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "subway_daily_ext.csv")
with open(fn, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["date","weekday","line","station","boardings","alightings"])
    for d in days:
        for ln, st in ST:
            u = "http://openapi.seoul.go.kr:8088/sample/json/CardSubwayStatsNew/1/5/%s/%s/%s" % (
                d.strftime("%Y%m%d"), urllib.parse.quote(ln), urllib.parse.quote(st))
            try: r = requests.get(u, timeout=20).json()["CardSubwayStatsNew"]["row"][0]
            except Exception as e: print("miss", d, ln, st); continue
            w.writerow([d.isoformat(), d.strftime("%a"), ln, st, r["GTON_TNOPE"], r["GTOFF_TNOPE"]])
print("done")
