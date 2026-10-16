"""Bounded synthetic protocol. Model candidates are data, never executable code."""
import copy, hashlib, json, re
VERSION='router-spec-v1'
FAMILIES=('retry_double_charge','late_completion','cross_key','unknown_cancel','stream_residue','reject_legal')
def validate(doc):
    if type(doc) is not dict or set(doc)!={'ops'}: raise ValueError('object must contain only ops')
    ops=doc['ops']
    if type(ops) is not list or not 1<=len(ops)<=12: raise ValueError('1..12 operations required')
    keys=set()
    for o in ops:
        if type(o) is not dict or o.get('op') not in ('request','retry','cancel'): raise ValueError('operation not allowed')
        if type(o.get('key')) is not str or not re.fullmatch(r'[a-z][a-z0-9_]{0,15}',o['key']): raise ValueError('key invalid')
        keys.add(o['key'])
        expected={'op','key','stream','break_at'} if o['op']=='request' else {'op','key'}
        if set(o)!=expected: raise ValueError('unexpected or missing fields')
        if o['op']=='request':
            if type(o['stream']) is not bool or o['break_at'] not in ('none','before_headers','after_first_chunk'): raise ValueError('invalid request')
            if not o['stream'] and o['break_at']=='after_first_chunk': raise ValueError('chunk break requires stream')
    if len(keys)>4: raise ValueError('at most four logical keys')
    return ops

def reference_step(state,o):
    """Declarative reference: completed work bills once; cancelled work stays cancelled."""
    st=copy.deepcopy(state); k=o['key']; op=o['op']; old=st.get(k)
    if op=='request':
        if old is not None: return st,'duplicate'
        done=o['break_at']=='none'
        st[k]={'status':'done' if done else 'interrupted','charge':int(done),'pending':False,'stream':o['stream']}
        return st,'ok'
    if old is None: return st,'unknown'
    if op=='cancel':
        if old['status']!='done': old.update(status='cancelled',pending=False)
        return st,'ok'
    if old['status']=='cancelled': return st,'cancelled'
    old.update(status='done',charge=1,pending=False)
    return st,'ok'

class Router:
    """Separate imperative target plus six deliberately injected defects."""
    def __init__(self, mutant='correct'): self.state={}; self.mutant=mutant
    def step(self,o):
        k=o['key']; op=o['op']; m=self.mutant
        if op=='request':
            if k in self.state: return 'duplicate'
            if m=='reject_legal' and o['stream'] and o['break_at']=='none': return 'rejected'
            finished=o['break_at']=='none'
            self.state[k]=dict(status='done' if finished else 'interrupted',charge=1 if finished else 0,pending=(m=='stream_residue' and o['break_at']=='after_first_chunk'),stream=o['stream'])
            return 'ok'
        if k not in self.state:
            if m=='unknown_cancel' and op=='cancel':
                self.state[k]=dict(status='cancelled',charge=0,pending=False,stream=False)
            return 'unknown'
        item=self.state[k]
        if op=='cancel':
            if item['status']!='done': item['status']='cancelled'; item['pending']=False
            return 'ok'
        if item['status']=='cancelled' and m!='late_completion': return 'cancelled'
        if m=='cross_key' and len(self.state)>1:
            item=self.state[next(x for x in self.state if x!=k)]
        item['status']='done'; item['pending']=False
        item['charge']=item['charge']+1 if m=='retry_double_charge' else 1
        return 'ok'

def execute(doc,mutant='correct',bad_oracle=False):
    ops=validate(doc); target=Router(mutant); ref={}; trace=[]; found=False
    for i,o in enumerate(ops):
        ref,expected=reference_step(ref,o); actual=target.step(o)
        mismatch=ref!=target.state or expected!=actual
        if bad_oracle: mismatch=False
        found|=mismatch
        trace.append(dict(index=i,operation=o,reference=copy.deepcopy(ref),target=copy.deepcopy(target.state),expected_status=expected,actual_status=actual,mismatch=mismatch))
    return dict(spec=VERSION,mutant=mutant,detected=found,trace=trace)

def minimize(doc,mutant):
    ops=list(validate(doc)); calls=0; changed=True
    while changed and len(ops)>1:
        changed=False
        for i in range(len(ops)):
            candidate=ops[:i]+ops[i+1:]; calls+=1
            if execute({'ops':candidate},mutant)['detected']:
                ops=candidate; changed=True; break
    return {'ops':ops},calls

def digest(doc): return hashlib.sha256(json.dumps(doc,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def bundle(doc,mutant,provenance):
    result=execute(doc,mutant)
    if not result['detected']: raise ValueError('no counterexample')
    small,calls=minimize(doc,mutant)
    b=dict(format='replaylab-1',spec=VERSION,original=doc,minimized=small,mutant=mutant,provenance=provenance,original_trace=result['trace'],replay=execute(small,mutant),minimizer_calls=calls)
    return dict(payload=b,sha256=digest(b))
def verify_bundle(b):
    p=b['payload']
    if digest(p)!=b['sha256'] or p['spec']!=VERSION: raise ValueError('bundle integrity/spec mismatch')
    if execute(p['minimized'],p['mutant'])!=p['replay'] or not p['replay']['detected']: raise ValueError('replay mismatch')
    return True
