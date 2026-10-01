# gwanghwamun-crowd-2026

Data and code for the article
**"When precaution looks like failure: A capacity-based crowd ceiling, artist–fan channels and public judgement at the 2026 BTS concert in Seoul"**
(submitted to the *Journal of Contingencies and Crisis Management*).

All analyses use public data only. No data on individual people are used.

## Contents

| Folder | File | What it is |
|---|---|---|
| `data/raw/` | `subway_daily.csv` | Daily card-based alightings, 8 stations, Saturdays 7 Mar–30 May 2026 (Seoul Open Data Plaza, `CardSubwayStatsNew`) |
| | `subway_daily_ext.csv` | Outer-ring (7 station-lines) and distant control stations (5), same Saturdays |
| | `subway_saturdays_2025_2026.csv` | Alightings and boardings, 20 station–line pairs, all Saturdays of March–May 2025 and 2026, from the monthly files of OA-12914 (`CARD_SUBWAY_MONTH_YYYYMM.csv`); the API returns only recent dates |
| | `living_pop_saturdays/sat_*_YYYYMM.csv` | Saturday-only extracts of the living-population files (OA-14991/14992/14993), all dongs, Mar–May 2025 and 2026 |
| | `seoul_dongs.geojson`, `seoul_dong_names.json` | Administrative-dong boundaries for Seoul (admdongkor ver20250401), for Supplementary Figure S1 |
| | `weather_openmeteo_era5.json` | Hourly ERA5 reanalysis at 37.572°N, 126.977°E via the Open-Meteo archive API |
| | `era5_2025.json`, `era5_2026.json` | Hourly ERA5, March–May 2025 and 2026 (Open-Meteo archive) |
| `data/processed/` | `subway_event_vs_baseline.csv` | Event day vs median/range of 12 other Saturdays (Supplementary Table S3) |
| | `subway_group_totals_by_date.csv`, `subway_robustness.csv` | Daily group totals; March-only baseline and control comparison (Supplementary Table S3) |
| | `living_pop_robustness.csv` | Three dongs vs rest of Seoul, March-only baseline (Supplementary Table S5) |
| | `living_pop_core3_saturdays.csv` | Hourly living population, Sajik-dong (11110530), Jongno 1·2·3·4ga-dong (11110615), Sogong-dong (11140520), Saturdays Mar–Apr 2026; domestic, short-term foreign, long-term foreign and total (Supplementary Table S5) |
| | `core_hourly_saturdays_2025_2026.csv` | Hourly totals, three core dongs, 27 spring Saturdays 2025–26 (Figure 3d) |
| | `lp_design_results.csv`, `lp_placebo.csv`, `lp_14h_by_date.csv`, `lp_20h_by_date.csv` | Baseline comparisons, adjustment by distant comparison dongs, placebo pseudo-events, values by date (Supplementary Tables S5b, S5c) |
| | `lp_design2_results.csv`, `lp_placebo2.csv` | Pools of all 26, 18 ordinary, 12 (2026) and 11 ordinary (2026) Saturdays; hourly and window statistics; placebo by pool (Supplementary Tables S5–S5d) |
| | `weather_saturdays_2025_2026.csv` | ERA5 14:00–22:00 weather on all 27 Saturdays (Supplementary Table S4) |
| | `subway_group_totals_2025_2026.csv`, `subway_design2_results.csv`, `subway_placebo2.txt` | Station-group totals and comparisons by pool, with placebo (Supplementary Tables S3b, S3c) |
| `corpus/` | `pre_event.json`, `post_event.json` | News reports mentioning the figure of 260,000: 68 pre-event and 59 event-day/post-event articles (URL, outlet, date, headline, verbatim sentences) |
| | `*_queries.txt`, `pre_event_excluded.json` | Search queries and excluded items |
| | `frame_coding.py`, `pre_coded.csv`, `post_coded.csv` | Word-list framing coding and results (Supplementary Table S6) |
| | `framing_sheet_coded.csv`, `framing_sample_key.json`, `agreement_framing.py`, `agreement_framing_output.txt` | Second coder's sheet for 30 sampled articles, sample key, agreement (Cohen's κ and Gwet's AC1; run inside `corpus/`) |
| `official/` | `official_statements.json`, `summary.md` | 26 official statements on the crowd figure with verbatim Korean wording, translation, form and source (Supplementary Table S7) |
| `shadow/` | `shadow_cases.json`, `summary.md` | Eleven other planned gatherings in Korea since 2022 with a published crowd figure: figures, counts, post-event framing and sources (Supplementary Table S8) |
| `corpus/` | `bigkinds_merge.py` | Checks a BigKinds export against the corpus |
| | `bk_coding.py`, `bigkinds_coded.csv` | BigKinds census (1,198 articles after removing duplicates and news digests, 64 outlets): word-list codes per article with outlet, date, title and URL (Supplementary Table S6c). Full texts are not redistributed; `bk_coding.py` expects the archive export `bigkinds_26man_20260209_20260326.json`, retrievable from bigkinds.or.kr with the query in the SI |
| | `bigkinds_sample_second_coder.csv`, `bigkinds_sample_key.csv`, `agreement_sample.py`, `agreement_sample_output.csv` | Census validation: independent second coder on a random sample of 120 census articles (60 pre, 60 post; seed 20261001), sample key, and per-category agreement with the word list (Cohen's κ, Gwet's AC1, Krippendorff's α; Supplementary Table S6d). Run inside `corpus/` |
| `coding/` | `messages.json` | Full Korean text and English translation of the eight artist message units (19–21 Mar 2026), with sources |
| | `manual_coding.csv`, `rule_coding.csv`, `rule_hits.csv`, `reliability.json` | Manual coding, rule-based (dictionary) coding, matched patterns, agreement |
| | `coder2_coding_sheet.csv`, `coder2_unit_key.json`, `agreement.py`, `agreement_output.txt` | Independent second coder's sheet (units shuffled), key, and inter-coder agreement (63/64; κ = 0.97; α = 0.97) |
| | `rule_coding.py` | Word-list coding (transparency aid, not an independent reliability check) |
| `code/` | `fetch_subway.py`, `fetch_subway_ext.py`, `subway_analysis.py`, `robustness_subway.py` | Retrieve and summarise subway data; robustness checks |
| | `living_pop.py`, `robust_lp.py` | Build the living-population table; comparison with the rest of Seoul |
| | `compact.py`, `lp_design.py` | Saturday-only extracts; 26-Saturday baseline, comparison-dong adjustment, adjacent dongs and placebo (run in `data/raw/living_pop_saturdays/`) |
| | `lp_design2.py` | Ordinary-Saturday pool (rally, parade and holiday Saturdays excluded), windows and staff scenarios (run in `data/raw/living_pop_saturdays/`) |
| | `figS1_map.py` | Supplementary Figure S1 (map) |
| | `fig1_framework.py` … `fig4_message_coding.py` | Figures 1–4 |
| `figures/` | `fig1`–`fig4`, `figS1_map` (PDF, PNG) | Figures as in the article |

## Reproducing

```bash
pip install -r requirements.txt
# figure scripts, corpus coding and the map run from the repository root
python code/fig3_plan_vs_crowd.py      # -> figures/fig3_plan_vs_crowd.pdf/png
python code/fig4_message_coding.py     # -> figures/fig4_message_coding.pdf/png
python code/figS1_map.py               # -> figures/figS1_map.pdf/png
python corpus/frame_coding.py          # -> corpus/pre_coded.csv, corpus/post_coded.csv
# living-population design (Supplementary Tables S5b, S5c)
cd data/raw/living_pop_saturdays && python ../../../code/lp_design.py && python ../../../code/lp_design2.py && cd ../../..
# subway scripts and word-list message coding
cd code && python subway_analysis.py && cd ../data/raw && python ../../code/subway_design2.py && cd ../coding && python rule_coding.py
```

`living_pop.py` needs the monthly files `LOCAL_PEOPLE_DONG_2026MM.csv`, `TEMP_FOREIGNER_DONG_2026MM.csv` and
`LONG_FOREIGNER_DONG_2026MM.csv` (March and April 2026) from the Seoul Open Data Plaza
(datasets OA-14991, OA-14992, OA-14993). They are not redistributed here because of their size.
Cells suppressed for disclosure control (`*`) are treated as zero. The Saturday-only extracts in `data/raw/living_pop_saturdays/` are enough to reproduce the 2025–26 comparisons.

The subway API (`CardSubwayStatsNew`) returns only recent dates; the 2025 and 2026 values come from the dataset's monthly files, which match the API values for 2026.

## Sources

- Seoul Open Data Plaza, <https://data.seoul.go.kr> (subway ridership; living population OA-14991/14992/14993)
- Copernicus Climate Change Service (2018), ERA5 hourly data on single levels, doi:10.24381/cds.adbb2d47
- BTS artist posts, Weverse, <https://weverse.io/bts/artist> (quoted for research purposes)

## Licence

Code: MIT. Processed data and coding: CC BY 4.0. Source data remain under the terms of their providers.
