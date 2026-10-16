import copy,json,sys,unittest,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from core import *
from model import extract,endpoint
from canaries import validate_detector
from hypothesis import given,strategies as st
ROOT=Path(__file__).resolve().parents[1]
class CoreTests(unittest.TestCase):
 def test_family_positive_controls_and_broken_oracle(self):
    docs=json.loads((ROOT/'data/tasks.json').read_text()); result={}
    for family in FAMILIES:
        hits=[t for t in docs if t['expected'] and execute(t['expected'],family)['detected']]
        self.assertTrue(hits,family)
        doc=hits[0]['expected']; self.assertFalse(execute(doc,'correct')['detected'])
        self.assertFalse(execute(doc,family,bad_oracle=True)['detected'])
        b=bundle(doc,family,{'source':'human synthetic positive control'})
        self.assertTrue(verify_bundle(b)); b['payload']['spec']='tampered'
        with self.assertRaises(ValueError): verify_bundle(b)
        result[family]=dict(task=hits[0]['id'],known_bad_detected=True,correct_clean=True,broken_oracle_fails_canary=True)
    if os.access(ROOT/'results',os.W_OK): (ROOT/'results/controls.json').write_text(json.dumps(result,indent=2))
 def test_canary_harness_rejects_broken_oracle(self):
    self.assertEqual(set(validate_detector()),set(FAMILIES))
    with self.assertRaisesRegex(RuntimeError,'Broken detector'):
        validate_detector(lambda doc,target:execute(doc,target,bad_oracle=True))
 def test_schema_rejects_attack_and_resources(self):
    bad=[{'ops':[]},{'ops':[{'op':'exec','key':'a'}]},{'ops':[{'op':'cancel','key':'../../etc/passwd'}]},{'ops':[{'op':'retry','key':'a','expected':True}]},{'ops':[{'op':'request','key':'a','stream':0,'break_at':'none'}]},{'ops':[{'op':'request','key':'a','stream':False,'break_at':'after_first_chunk'}]},{'ops':[{'op':'cancel','key':x} for x in 'abcde']},{'ops':[{'op':'cancel','key':'a'}]*13}]
    for doc in bad:
      with self.assertRaises(ValueError): validate(doc)
 def test_adapter_fail_closed(self):
    self.assertEqual(extract([32,4,33,44,68]),[44])
    for tokens in [[],[33,32],[32,32,33],[32,33,33],[32,12]]:
      with self.assertRaises(ValueError): extract(tokens)
    with self.assertRaises(ValueError): extract([32,33],True)
 @given(st.lists(st.tuples(st.sampled_from(['request','retry','cancel']),st.sampled_from(['a','b','c','d']),st.booleans(),st.sampled_from(['none','before_headers'])),min_size=1,max_size=12))
 def test_correct_reference_equivalence(self,items):
    ops=[]
    for kind,key,stream,br in items:
      o=dict(op=kind,key=key)
      if kind=='request': o.update(stream=stream,break_at=br)
      ops.append(o)
    self.assertFalse(execute({'ops':ops},'correct')['detected'])
if __name__=='__main__': unittest.main()
