import json,time
from pathlib import Path
from model import generate
from tasks import conforms
root=Path(__file__).resolve().parents[1]
tasks=json.loads((root/'data/tasks.json').read_text()); out=root/'results/model-candidates.jsonl'
if out.exists(): raise SystemExit('Refusing to overwrite model evidence')
for task in tasks:
    r=generate(task['contract']); r['task_id']=task['id']; r['schema_valid']='candidate' in r
    r['contract_exact']=conforms(r['candidate'],task) if 'candidate' in r else (task['reject_reason'] is not None and r.get('rejected')==task['reject_reason'])
    # llama.cpp local model path is private machine metadata; only basename is shareable.
    if 'raw' in r and isinstance(r['raw'].get('model'),str): r['raw']['model']=Path(r['raw']['model']).name
    with out.open('a') as f: f.write(json.dumps(r,ensure_ascii=False)+'\n'); f.flush()
    print(task['id'],r['schema_valid'],r['contract_exact'],round(r['seconds'],3),r.get('error',''),flush=True)
