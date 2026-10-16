import copy,json,random,time,platform,multiprocessing
from pathlib import Path
import hypothesis
from hypothesis import settings,seed,Phase,strategies as st
from hypothesis.stateful import RuleBasedStateMachine,rule
from core import Router,reference_step,execute,minimize,bundle,verify_bundle,FAMILIES
ROOT=Path(__file__).resolve().parents[1]
class Exhausted(BaseException): pass

def _hypothesis_worker(connection,runseed,plan):
    """Only generates operations. Parent enforces target budgets by stopping its own worker."""
    class Machine(RuleBasedStateMachine):
        def __init__(self):
            super().__init__();connection.send(('reset',None))
        @rule(kind=st.sampled_from(['request','retry','cancel']),key=st.sampled_from(['a','b','c','d']),stream=st.booleans(),br=st.sampled_from(['none','before_headers','after_first_chunk']))
        def operation(self,kind,key,stream,br):
            op={'op':kind,'key':key}
            if kind=='request':op.update(stream=stream,break_at=br if stream or br!='after_first_chunk' else 'before_headers')
            connection.send(('op',op));connection.recv()
    try:
        factory=seed(runseed)(Machine)
        hypothesis.stateful.run_state_machine_as_test(factory,settings=settings(max_examples=plan['max_examples'],stateful_step_count=plan['stateful_step_count'],deadline=None,database=None,phases=[Phase.generate]))
        connection.send(('done',None))
    except (EOFError,BrokenPipeError):pass
    except BaseException as e:connection.send(('error',repr(e)))
    finally:connection.close()


def trial(mutant,arm,runseed,mode,records,plan,startup_seconds):
    begun=time.monotonic(); calls=0; found=None; first=None; sequences=0
    overhead=(sum(x['seconds'] for x in records)+startup_seconds+plan.get('repair_generation_seconds',0))/len(plan['targets']) if arm=='B' else 0
    limit=plan['call_budget_per_target']; seconds=plan['time_budget_seconds_per_target']
    def tick():
        nonlocal calls
        if (mode=='calls' and calls>=limit) or (mode=='time' and time.monotonic()-begun+overhead>=seconds): raise Exhausted()
        calls+=1
    def accept(doc):
        nonlocal found,first,sequences
        target=Router(mutant); ref={}; prefix=[]; sequences+=1
        for op in doc['ops']:
            tick(); prefix.append(op); ref,status=reference_step(ref,op); result=target.step(op)
            if ref!=target.state or status!=result:
                found={'ops':copy.deepcopy(prefix)}; first=time.monotonic()-begun+overhead
                return True
        return False
    try:
        if arm=='B':
            for record in records:
                if 'candidate' in record and accept(record['candidate']):break
        if found is None:
            if mode=='time' and time.monotonic()-begun+overhead>=seconds:raise Exhausted()
            context=multiprocessing.get_context('spawn');connection,child=context.Pipe()
            worker=context.Process(target=_hypothesis_worker,args=(child,runseed,plan));worker.start();child.close()
            target=None;ref={};prefix=[]
            try:
                while True:
                    if mode=='calls' and calls>=limit:break
                    remaining=seconds-(time.monotonic()-begun+overhead) if mode=='time' else 30
                    if remaining<=0:break
                    if not connection.poll(min(remaining,30)):
                        if not worker.is_alive():raise RuntimeError('Hypothesis worker exited without completion')
                        if mode=='calls':raise RuntimeError('Hypothesis worker stalled')
                        continue
                    kind,value=connection.recv()
                    if kind=='reset':target=Router(mutant);ref={};prefix=[];sequences+=1;continue
                    if kind=='done':break
                    if kind=='error':raise RuntimeError(value)
                    tick();prefix.append(value);ref,status=reference_step(ref,value);actual=target.step(value)
                    if ref!=target.state or status!=actual:
                        found={'ops':copy.deepcopy(prefix)};first=time.monotonic()-begun+overhead;break
                    connection.send(True)
            finally:
                connection.close()
                if worker.is_alive():worker.terminate()
                worker.join(timeout=1)
                if worker.is_alive():worker.kill();worker.join()
    except Exhausted:pass
    minimized=None; shrink_calls=0; shrink_complete=False
    # Shared deletion shrinker; all its target calls count against remaining budget.
    if found:
        ops=list(found['ops']); changed=True
        try:
            while changed and len(ops)>1:
                changed=False
                for i in range(len(ops)):
                    doc={'ops':ops[:i]+ops[i+1:]}
                    # Budget accounts each target operation, including replayed prefixes.
                    shrink_target=Router(mutant); shrink_ref={}; mismatch=False
                    for op in doc['ops']:
                        tick(); shrink_calls+=1
                        shrink_ref,status=reference_step(shrink_ref,op); actual=shrink_target.step(op)
                        mismatch|=shrink_ref!=shrink_target.state or status!=actual
                    if mismatch: ops=doc['ops']; changed=True; break
            shrink_complete=True
        except Exhausted: pass
        minimized={'ops':ops}
    return dict(target=mutant,arm=arm,seed=runseed,mode=mode,calls=calls,sequences=sequences,detected=found is not None,first_counterexample_seconds=first,elapsed_seconds=time.monotonic()-begun,model_overhead_seconds=overhead,end_to_end_seconds=time.monotonic()-begun+overhead,original=found,minimized=minimized,shrink_calls=shrink_calls,shrink_complete=shrink_complete)

def main():
    from canaries import validate_detector
    validate_detector()
    plan=json.loads((ROOT/'data/experiment-plan.json').read_text()); records=[json.loads(x) for x in (ROOT/'results/model-candidates.jsonl').read_text().splitlines()]
    startup=json.loads((ROOT/'results/startup.json').read_text())['seconds']
    repair=json.loads((ROOT/'results/repair-cost.json').read_text())
    plan['repair_generation_seconds']=repair['seconds']
    output=ROOT/'results/comparison.jsonl'
    if output.exists(): raise SystemExit('Refusing to overwrite comparison')
    for mode in ['calls','time']:
      for n in plan['seeds']:
       for target in plan['targets']:
        for arm in ['A','B']:
            row=trial('correct' if target=='clean_control' else target,arm,n,mode,records,plan,startup); row['target']=target
            with output.open('a') as f: f.write(json.dumps(row)+'\n')
            print(mode,n,target,arm,row['detected'],row['calls'],flush=True)
    rows=[json.loads(x) for x in output.read_text().splitlines()]
    summary=dict(hypothesis=hypothesis.__version__,python=platform.python_version(),model_calls=len(records),valid=sum('candidate' in x for x in records),exact=sum(x['contract_exact'] for x in records),model_generation_seconds=sum(x['seconds'] for x in records),startup_seconds=startup,repair_generation_seconds=repair['seconds'],total_model_attempts=repair['calls']+len(records),independent_heldout_claim=False,groups=[])
    for mode in ['calls','time']:
      for arm in ['A','B']:
       rs=[x for x in rows if x['mode']==mode and x['arm']==arm]
       summary['groups'].append(dict(mode=mode,arm=arm,defect_hits=sum(x['detected'] for x in rs if x['target'] in FAMILIES),defect_trials=len([x for x in rs if x['target'] in FAMILIES]),false_positives=sum(x['detected'] for x in rs if x['target'] not in FAMILIES),families={m:sum(x['detected'] for x in rs if x['target']==m) for m in FAMILIES}))
    (ROOT/'results/summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
