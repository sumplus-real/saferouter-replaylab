"""Real HTTP stub and make-launch tests; no model/production/network service calls."""
import copy,importlib.util,json,os,subprocess,sys,tempfile,threading,unittest,shutil
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from model import generate,request_for
class Stub(BaseHTTPRequestHandler):
 seen=[];redirect=False;sink_hits=0
 def log_message(self,*args):pass
 def do_POST(self):
  body=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
  type(self).seen.append({'path':self.path,'authorization':self.headers.get('Authorization'),'body':body})
  if type(self).redirect:
   self.send_response(307);self.send_header('Location','http://127.0.0.1:'+str(self.server.server_port)+'/sink');self.end_headers();return
  status=200 if self.headers.get('Authorization')=='Bearer local-stub-test-key' and body.get('model')=='apertus-stub-selected' else 401 if self.headers.get('Authorization')!='Bearer local-stub-test-key' else 404
  self.send_response(status);self.send_header('Content-Type','application/json');self.end_headers()
  self.wfile.write(json.dumps({'choices':[{'finish_reason':'stop','message':{'content':'{"ops":[{"op":"cancel","key":"missing"}]}'}}]}).encode())
class ModelConfigTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.server=ThreadingHTTPServer(('127.0.0.1',0),Stub);cls.url='http://127.0.0.1:'+str(cls.server.server_port);cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
 @classmethod
 def tearDownClass(cls):cls.server.shutdown();cls.server.server_close()
 def setUp(self):Stub.seen=[];Stub.redirect=False
 def env(self,**changes):return patch.dict(os.environ,{'LLM_NAME':'apertus-stub-selected','LLM_BASE_URL':self.url+'/v1/','LLM_API_KEY':'local-stub-test-key',**changes})
 def test_selected_model_version_base_and_bearer_reach_stub(self):
  with self.env():r=generate('Cancel an unknown key.')
  self.assertIn('candidate',r);self.assertEqual(len(Stub.seen),1);wire=Stub.seen[0]
  self.assertEqual(wire['path'],'/v1/chat/completions');self.assertEqual(wire['body']['model'],'apertus-stub-selected');self.assertEqual(wire['authorization'],'Bearer local-stub-test-key');self.assertEqual(r['request'],wire['body']);self.assertEqual(r['model'],wire['body']['model'])
  self.assertNotIn('local-stub-test-key',json.dumps(r));self.assertNotIn('Authorization',json.dumps(r))
 def test_wrong_key_and_model_fail_without_fallback_or_secret_echo(self):
  for change,status in [({'LLM_API_KEY':'wrong-stub-key'},'401'),({'LLM_NAME':'wrong-model'},'404')]:
   with self.env(**change):r=generate('Cancel an unknown key.')
   self.assertNotIn('candidate',r);self.assertIn(status,r['error']);self.assertNotIn('wrong-stub-key',json.dumps(r))
 def test_empty_key_omits_authorization(self):
  with self.env(LLM_API_KEY=''):r=generate('Cancel an unknown key.')
  self.assertIsNone(Stub.seen[-1]['authorization']);self.assertNotIn('candidate',r)
 def test_invalid_key_rejected_before_network_without_echo(self):
  with self.env(LLM_API_KEY='stub\r\nsecret'):r=generate('Cancel an unknown key.')
  self.assertEqual(Stub.seen,[]);self.assertNotIn('secret',r['error']);self.assertNotIn('candidate',r)
 def test_local_redirect_cannot_forward_key(self):
  Stub.redirect=True
  with self.env():r=generate('Cancel an unknown key.')
  self.assertEqual(len(Stub.seen),1);self.assertEqual(r['error'],'Model endpoint redirects are not allowed');self.assertNotIn('candidate',r)
 def test_local_request_does_not_inherit_proxy(self):
  with self.env(http_proxy='http://127.0.0.1:1',HTTP_PROXY='http://127.0.0.1:1',all_proxy='http://127.0.0.1:1',ALL_PROXY='http://127.0.0.1:1',no_proxy='',NO_PROXY=''):r=generate('Cancel an unknown key.')
  self.assertIn('candidate',r)
 def test_external_or_url_embedded_credentials_fail_before_network(self):
  for url in ['https://external.example/v1',self.url.replace('://','://user:password@')+'/v1',self.url+'?key=hidden']:
   with self.env(LLM_BASE_URL=url):r=generate('Cancel an unknown key.')
   self.assertNotIn('candidate',r)
  self.assertEqual(Stub.seen,[])
 def test_only_model_selector_added_to_frozen_protocol(self):
  spec=importlib.util.spec_from_file_location('frozen_v3_model',ROOT/'history/v3-model-frozen.py');frozen=importlib.util.module_from_spec(spec);spec.loader.exec_module(frozen)
  for contract in ['Cancel one unknown key.','Start two independent non-streaming requests.']:
   with self.env():a=request_for(contract)
   a.pop('model');self.assertEqual(a,frozen.request_for(contract))
 @unittest.skipUnless(shutil.which('make') and (ROOT.parent/'Makefile').exists(),'Host make-launch check; application image contains neither host make nor Docker CLI')
 def test_make_forwards_environment_without_shell_interpolating_values(self):
  with tempfile.TemporaryDirectory() as tmp:
   d=Path(tmp);script=d/'fake-docker';record=d/'calls.jsonl'
   script.write_text('#!'+sys.executable+'\nimport os,sys,json\nwith open(os.environ["STUB_LOG"],"a")as f:f.write(json.dumps({"args":sys.argv[1:],"env":{k:os.environ.get(k)for k in ["LLM_NAME","LLM_BASE_URL","LLM_API_KEY"]}})+"\\n")\n');script.chmod(0o700)
   with self.env(LLM_NAME="apertus-stub'quoted",STUB_LOG=str(record)):
    r=subprocess.run(['make','run','DOCKER='+str(script)],cwd=ROOT.parent,capture_output=True,text=True,check=True)
   rows=[json.loads(x)for x in record.read_text().splitlines()];self.assertEqual(len(rows),2);args=rows[-1]['args']
   for name in ['LLM_NAME','LLM_BASE_URL','LLM_API_KEY']:self.assertIn(name,args)
   self.assertEqual(rows[-1]['env']['LLM_NAME'],"apertus-stub'quoted");self.assertEqual(rows[-1]['env']['LLM_API_KEY'],'local-stub-test-key');self.assertNotIn('local-stub-test-key',r.stdout);self.assertNotIn("apertus-stub'quoted",r.stdout)
if __name__=='__main__':unittest.main()
