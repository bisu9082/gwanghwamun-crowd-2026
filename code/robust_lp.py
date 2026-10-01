"""Living population robustness: March-only baseline, rest-of-Seoul control (DiD on log ratio),
suppressed-cell counts for the three core dongs."""
import pandas as pd, numpy as np
core = ['11110530','11110615','11140520']
def load(prefix):
    fr = []
    for m in ['202603','202604']:
        x = pd.read_csv(f'{prefix}_{m}.csv', encoding='utf-8-sig', index_col=False,
                        dtype={'기준일ID':str,'시간대구분':str,'행정동코드':str})
        x = x.iloc[:, :4]; x.columns = ['date','hour','dong','tot']; fr.append(x)
    d = pd.concat(fr); d['hour'] = d.hour.astype(int)
    d['supp'] = d.tot.astype(str).str.strip().eq('*')
    d['tot'] = pd.to_numeric(d.tot, errors='coerce').fillna(0)
    d = d[pd.to_datetime(d.date).dt.weekday == 5]
    return d
L, T, G = load('LOCAL_PEOPLE_DONG'), load('TEMP_FOREIGNER_DONG'), load('LONG_FOREIGNER_DONG')
A = pd.concat([L.assign(s='dom'), T.assign(s='temp'), G.assign(s='long')], ignore_index=True)
A['grp'] = np.where(A.dong.isin(core), 'core', np.where(A.dong.str[:5].isin(['11110','11140']), 'jj', 'ctrl'))
P = A.groupby(['grp','date','hour']).tot.sum().unstack('date')
EV = '20260321'; MAR = ['20260307','20260314','20260328']
out = []
for h in range(8, 24):
    c = P.loc[('core', h)]; k = P.loc[('ctrl', h)]
    ob = c.drop(EV); kb = k.drop(EV)
    out.append(dict(hour=h, event=c[EV], med_all=ob.median(), diff_all=c[EV]-ob.median(),
        med_mar=c[MAR].median(), diff_mar=c[EV]-c[MAR].median(),
        did_all=np.exp(np.log(c[EV]/ob.median()) - np.log(k[EV]/kb.median())),
        did_mar=np.exp(np.log(c[EV]/c[MAR].median()) - np.log(k[EV]/k[MAR].median())),
        ctrl_ratio=k[EV]/kb.median()))
O = pd.DataFrame(out); print(O.round(3).to_string())
# implied counts from DiD ratio
O['did_diff_all'] = O.event - O.event/O.did_all
O['did_diff_mar'] = O.event - O.event/O.did_mar
print(O[['hour','did_diff_all','did_diff_mar']].round(0).to_string())
C = A[A.dong.isin(core)]
print("suppressed cells, core dongs, by series and date (of 72 cells = 3 dongs x 24 h):")
print(C.groupby(['s','date']).supp.sum().unstack(0))
O.to_csv('living_pop_robustness.csv', index=False)
