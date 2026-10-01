import sys, pandas as pd, io, subprocess
def compact(src, out, from_zip=False):
    if from_zip:
        data = subprocess.run(["unzip", "-p", src], capture_output=True).stdout
        x = pd.read_csv(io.BytesIO(data), encoding="utf-8-sig", index_col=False, dtype=str)
    else:
        x = pd.read_csv(src, encoding="utf-8-sig", index_col=False, dtype=str)
    x = x.iloc[:, :4]; x.columns = ["date", "hour", "dong", "tot"]
    x = x[pd.to_datetime(x.date).dt.weekday == 5]
    x["supp"] = x.tot.str.strip().eq("*").astype(int)
    x["tot"] = pd.to_numeric(x.tot, errors="coerce").fillna(0)
    x.to_csv(out, index=False)
    print(out, len(x), x.date.nunique())
compact(sys.argv[1], sys.argv[2], len(sys.argv) > 3)
