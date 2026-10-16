"""Read-only audit of frozen v3 evidence; no model/network calls."""
from pathlib import Path
import json,hashlib,copy
from core import validate
from tasks import conforms
ROOT=Path(__file__).resolve().parents[1]
def exact(record,task):
    if 'candidate' in record:return conforms(record['candidate'],task)
    return task.get('reject_reason') is not None and record.get('rejected')==task['reject_reason']
def main():
    freeze=json.loads((ROOT/'data/fresh-v3-freeze.json').read_text())
    for file,digest in freeze['sha256'].items():
        historical=ROOT/'history/v3-model-frozen.py' if file=='src/model.py' else ROOT/file
        assert hashlib.sha256(historical.read_bytes()).hexdigest()==digest,file
    tasks=json.loads((ROOT/'data/fresh-requirements-v3.json').read_text())
    rows=[json.loads(x)for x in(ROOT/'results/v3-teaching/model-candidates.jsonl').read_text().splitlines()]
    assert len(rows)==len(tasks)==8
    assert [r['task_id']for r in rows]==[t['id']for t in tasks]
    for r,t in zip(rows,tasks):
        assert r['request']['messages'][-1]=={'role':'user','content':t['contract']}
        assert type(r['seconds']) in (float,int) and r['seconds']>0
        assert exact(r,t)==r['contract_exact']
        assert r['schema_valid']==('candidate'in r)
        if 'candidate'in r:validate(r['candidate']);assert json.loads(r['answer_text'])==r['candidate']
    # Known-bad scorer canaries: missing output or changed operation must not pass.
    assert not exact({'error':'missing output'},tasks[0])
    altered=copy.deepcopy(rows[0]);altered['candidate']['ops'][1]['op']='cancel';assert not exact(altered,tasks[0])
    blocked=[r for r in rows if 'validation_rejection'in r]
    assert blocked and all('candidate'not in r and 'rejected'not in r for r in blocked)
    summary=json.loads((ROOT/'results/v3-teaching/summary.json').read_text())
    calculated=dict(model_calls=len(rows),valid=sum('candidate'in r for r in rows),exact=sum(exact(r,t)for r,t in zip(rows,tasks)),model_refusals=sum('rejected'in r for r in rows),validator_blocks=len(blocked))
    assert all(summary[k]==v for k,v in calculated.items())
    assert calculated==dict(model_calls=8,valid=6,exact=6,model_refusals=1,validator_blocks=1)
    print(json.dumps(dict(verified=True,model_source_scope='archived pre-transport model; current wire adapter verified separately',frozen_hashes=len(freeze['sha256']),known_bad_scoring_guards=2,**calculated),indent=2))
if __name__=='__main__':main()
