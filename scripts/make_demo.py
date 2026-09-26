"""Generate deterministic SYNTHETIC inputs, never a market snapshot."""
import json
import math
from datetime import date, timedelta
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
reg=json.loads((ROOT/'registry.json').read_text(encoding='utf-8'))
weekly={i['series_id'] for i in reg['indicators'] if i['frequency']=='weekly'}
bases={'SOFR':4.4,'EFFR':4.35,'IORB':4.4,'BAMLC0A4CBBB':1.3,'BAMLH0A0HYM2':3.8,
       'BAMLH0A1HYBB':2.4,'BAMLH0A2HYB':4.1,'BAMLH0A3HYC':8.5,'WLCFLPCL':3500,
       'WRESBAL':3200000,'DPSACBW027SBOG':18000,'TOTBKCR':18500,'VIXCLS':19,
       'NFCI':-.3,'STLFSI4':-.2,'T10Y2Y':.2,'T10Y3M':-.1,'DFII10':1.7}
series={s:[] for s in bases}
start,end=date(2019,1,1),date(2026,9,22)
for sid,base in bases.items():
    for n in range((end-start).days+1):
        d=start+timedelta(days=n)
        if d.weekday()>4 or (sid in weekly and d.weekday()!=2):
            continue
        wave=math.sin(n/59)+.3*math.cos(n/17)
        scale=max(abs(base)*.05,.04)
        value=base+scale*wave
        if sid in ('WRESBAL','DPSACBW027SBOG','TOTBKCR'):
            value+=base*.00003*n
        if sid in ('BAMLH0A3HYC','BAMLH0A0HYM2','BAMLH0A2HYB'):
            value+=max(0,n-((end-start).days-50))*base*.004
        series[sid].append({'date':str(d),'value':str(round(value,6))})
# Emulate current ICE history availability; source limitation is not bypassed.
for sid in series:
    if sid.startswith('BAML'):
        series[sid]=[r for r in series[sid] if r['date']>='2023-09-23']
out=ROOT/'examples/synthetic-input.json'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps({'synthetic':True,'description':'DEMO ONLY. Deterministic artificial values, not actual observations.',
                           'as_of':'2026-09-23','series':series},ensure_ascii=False,indent=2),encoding='utf-8')
print(out)
