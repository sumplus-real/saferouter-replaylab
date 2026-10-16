import json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from evaluate import trial
class ExperimentTests(unittest.TestCase):
 def test_empty_model_arm_matches_baseline_for_fixed_seed(self):
  root=Path(__file__).resolve().parents[1];plan=json.loads((root/'data/experiment-plan.json').read_text());plan['call_budget_per_target']=100
  a=trial('unknown_cancel','A',17,'calls',[],plan,0);b=trial('unknown_cancel','B',17,'calls',[],plan,0)
  self.assertTrue(a['detected'])
  self.assertEqual(a['original'],b['original']);self.assertEqual(a['minimized'],b['minimized']);self.assertEqual(a['calls'],b['calls']);self.assertLessEqual(a['calls'],100)
 def test_clean_model_arm_exhausts_nonzero_seed_offset_budget(self):
  root=Path(__file__).resolve().parents[1];plan=json.loads((root/'data/experiment-plan.json').read_text())
  records=[{'seconds':1,'candidate':{'ops':[{'op':'cancel','key':'a'}]}}]
  result=trial('correct','B',17,'calls',records,plan,0)
  self.assertFalse(result['detected']);self.assertEqual(result['calls'],800)
 def test_time_exhausted_by_model_has_zero_target_calls(self):
  root=Path(__file__).resolve().parents[1];plan=json.loads((root/'data/experiment-plan.json').read_text())
  result=trial('unknown_cancel','B',17,'time',[{'seconds':1000}],plan,0)
  self.assertEqual(result['calls'],0);self.assertFalse(result['detected'])
if __name__=='__main__':unittest.main()
