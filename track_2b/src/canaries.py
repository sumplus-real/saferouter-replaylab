"""Fail the experiment when the detector cannot distinguish fixed positive/clean controls."""
import json
from pathlib import Path
from core import execute,FAMILIES
TASKS=json.loads((Path(__file__).resolve().parents[1]/'data/tasks.json').read_text())
def validate_detector(detector=execute):
    checked=[]
    for family in FAMILIES:
        # Fixed pre-model cases, selected only with frozen reference/injected implementation.
        cases=[t['expected'] for t in TASKS if t['expected'] and execute(t['expected'],family)['detected']]
        if not cases: raise RuntimeError('No known-positive canary for '+family)
        doc=cases[0]
        if not detector(doc,family)['detected']: raise RuntimeError('Broken detector: missed known fault '+family)
        if detector(doc,'correct')['detected']: raise RuntimeError('Broken detector: false accusation')
        checked.append(family)
    return checked
if __name__=='__main__':print(json.dumps({'canaries':validate_detector(),'passed':True},indent=2))
