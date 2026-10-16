import json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from model import decode_chat,request_for,SCHEMA,PROTOCOL
class ChatProtocolTests(unittest.TestCase):
 def response(self,x,finish='stop'):
  return {'choices':[{'finish_reason':finish,'message':{'content':json.dumps(x)}}]}
 def test_non_thinking_json_does_not_require_thinking_tokens(self):
  text,accepted=decode_chat(self.response({'ops':[{'op':'cancel','key':'unknown'}]}))
  self.assertEqual(accepted['candidate']['ops'][0]['op'],'cancel')
 def test_refusal_is_data_not_a_dsl_operation(self):
  for reason in ['ambiguous','out_of_scope','resource_limit']:
   self.assertEqual(decode_chat(self.response({'reject':reason}))[1],{'rejected':reason})
  with self.assertRaises(ValueError):decode_chat(self.response({'ops':[{'op':'reject','key':'ambiguous'}]}))
 def test_incomplete_and_extra_fields_fail_independently(self):
  valid={'ops':[{'op':'cancel','key':'a'}]}
  with self.assertRaises(ValueError):decode_chat(self.response(valid,'length'))
  with self.assertRaises(ValueError):decode_chat(self.response({'ops':[{'op':'cancel','key':'a','stream':False}]}))
  with self.assertRaises(ValueError):decode_chat(self.response({'ops':[{'op':'cancel','key':x} for x in 'abcde']}))
 def test_schema_and_teaching_are_fixed_across_contracts(self):
  a=request_for('Cancel an unknown key.');b=request_for('Send two independent streaming requests.')
  self.assertEqual(a['response_format'],b['response_format']);self.assertEqual(a['messages'][:-1],b['messages'][:-1]);self.assertFalse(a['chat_template_kwargs']['enable_thinking']);self.assertEqual(a['response_format']['json_schema']['schema'],SCHEMA)
if __name__=='__main__':unittest.main()
