"""Hourly living population, three core dongs, Saturdays Mar-Apr 2026 (Seoul Open Data Plaza OA-14991/14992/14993).
Input: monthly CSVs LOCAL_PEOPLE_DONG_2026MM.csv, TEMP_FOREIGNER_DONG_2026MM.csv, LONG_FOREIGNER_DONG_2026MM.csv."""
import pandas as pd
core = ['11110530', '11110615', '11140520']  # Sajik-dong, Jongno 1-4ga-dong, Sogong-dong
def load(prefix):
    fr = []
    for m in ['202603', '202604']:
        x = pd.read_csv(f'{prefix}_{m}.csv', encoding='utf-8-sig', index_col=False,
                        dtype={'기준일ID': str, '시간대구분': str, '행정동코드': str}, na_values=['*'])
        x = x.iloc[:, :4]; x.columns = ['date', 'hour', 'dong', 'tot']; fr.append(x)
    d = pd.concat(fr); d['hour'] = d.hour.astype(int); d['tot'] = pd.to_numeric(d.tot, errors='coerce').fillna(0)
    d = d[d.dong.isin(core)]; d = d[pd.to_datetime(d.date).dt.weekday == 5]
    return d.groupby(['date', 'hour']).tot.sum().unstack(0)
L, T, G = load('LOCAL_PEOPLE_DONG'), load('TEMP_FOREIGNER_DONG'), load('LONG_FOREIGNER_DONG')
tot = L.add(T, fill_value=0).add(G, fill_value=0)
pd.concat({'domestic': L, 'temp_foreign': T, 'long_foreign': G, 'total': tot}, axis=1).to_csv('living_pop_core3_saturdays.csv')
