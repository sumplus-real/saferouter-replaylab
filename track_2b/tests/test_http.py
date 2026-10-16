import sys,json,threading,unittest,urllib.request,urllib.error,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from server import Handler,ThreadingHTTPServer
from core import verify_bundle
from model import endpoint
class HTTPTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler);cls.url='http://127.0.0.1:'+str(cls.server.server_port);cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
 @classmethod
 def tearDownClass(cls): cls.server.shutdown();cls.server.server_close()
 def request(self,data,headers=None,reviewed=True):
  if reviewed:
   data=dict(data);data['contract']='Explicit test path';data['review']={'confirmed':True,'contract':data['contract'],'candidate':data['candidate']}
  req=urllib.request.Request(self.url+'/api/replay',data=json.dumps(data).encode(),headers={'Content-Type':'application/json',**(headers or {})})
  with urllib.request.urlopen(req) as response:return json.load(response)
 def test_replay_chain_and_negative_paths(self):
  doc={'candidate':{'ops':[{'op':'cancel','key':'missing'}]},'target':'unknown_cancel'}
  result=self.request(doc);self.assertTrue(result['detected']);self.assertTrue(verify_bundle(result['bundle']))
  doc['target']='correct';clean=self.request(doc);self.assertFalse(clean['detected']);self.assertIsNone(clean['bundle'])
  doc['candidate']['ops'][0]['op']='exec'
  with self.assertRaises(urllib.error.HTTPError) as e:self.request(doc)
  self.assertEqual(e.exception.code,400)
 def test_missing_and_stale_review_blocked(self):
  doc={'candidate':{'ops':[{'op':'cancel','key':'missing'}]},'target':'unknown_cancel','contract':'Cancel missing key'}
  with self.assertRaises(urllib.error.HTTPError) as e:self.request(doc,reviewed=False)
  self.assertEqual(e.exception.code,400)
  doc['review']={'confirmed':True,'contract':'different original','candidate':doc['candidate']}
  with self.assertRaises(urllib.error.HTTPError) as e:self.request(doc,reviewed=False)
  self.assertEqual(e.exception.code,400)
  doc['review']['contract']=doc['contract'];doc['review']['candidate']={'ops':[{'op':'retry','key':'missing'}]}
  with self.assertRaises(urllib.error.HTTPError) as e:self.request(doc,reviewed=False)
  self.assertEqual(e.exception.code,400)
 def test_reviewed_overflow_still_blocked(self):
  doc={'candidate':{'ops':[{'op':'cancel','key':k}for k in 'abcde']},'target':'correct'}
  with self.assertRaises(urllib.error.HTTPError) as e:self.request(doc)
  self.assertEqual(e.exception.code,400)
 def test_cross_origin_refused(self):
  with self.assertRaises(urllib.error.HTTPError) as e:self.request({'candidate':{'ops':[{'op':'cancel','key':'a'}]},'target':'correct'},{'Origin':'https://external.example'})
  self.assertEqual(e.exception.code,400)
 def test_external_model_endpoint_rejected_before_network(self):
  previous=os.environ.get('LLM_BASE_URL');os.environ['LLM_BASE_URL']='https://external.example/v1'
  try:
   with self.assertRaises(ValueError):endpoint()
  finally:
   if previous is None:os.environ.pop('LLM_BASE_URL',None)
   else:os.environ['LLM_BASE_URL']=previous
if __name__=='__main__':unittest.main()
