"""Recompute headline metrics from complete rows; refuses missing/duplicate trials."""
import json
from pathlib import Path
from core import FAMILIES,execute,verify_bundle
p=Path(__file__).resolve().parents[1]; plan=json.loads((p/'data/experiment-plan.json').read_text())
rows=[json.loads(x) for x in (p/'results/comparison.jsonl').read_text().splitlines()]
expected={(mode,n,t,a) for mode in ('calls','time') for n in plan['seeds'] for t in plan['targets'] for a in ('A','B')}
actual=[(x['mode'],x['seed'],x['target'],x['arm']) for x in rows]
assert len(rows)==len(expected)==len(set(actual)) and set(actual)==expected
replays=0
for row in rows:
 assert type(row['detected']) is bool and type(row['calls']) is int
 if row['mode']=='calls': assert row['calls']<=plan['call_budget_per_target']
 if row['detected']:
  assert row['target'] in FAMILIES
  assert execute(row['original'],row['target'])['detected']
  assert execute(row['minimized'],row['target'])['detected'];replays+=1
assert all(not x['detected'] for x in rows if x['target'] not in FAMILIES)
s=json.loads((p/'results/summary.json').read_text())
for g in s['groups']:
 rr=[x for x in rows if x['mode']==g['mode'] and x['arm']==g['arm']]
 assert g['defect_hits']==sum(x['detected'] for x in rr)
print(json.dumps(dict(trial_rows=len(rows),all_expected_trials_present=True,independent_replays=replays,false_positives=0),indent=2))
