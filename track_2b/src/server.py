from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import json,os,urllib.parse,threading
from core import execute,bundle,FAMILIES
from model import generate
ROOT=Path(__file__).resolve().parents[1]
MODEL_LOCK=threading.Lock()
class Handler(BaseHTTPRequestHandler):
 def respond(self,status,body,kind='application/json'):
    raw=body if isinstance(body,bytes) else json.dumps(body,ensure_ascii=False).encode()
    self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(raw)
 def do_GET(self):
    if self.path=='/': return self.respond(200,(ROOT/'src/index.html').read_bytes(),'text/html; charset=utf-8')
    if self.path=='/api/state':
      rows=ROOT/'results/v3-teaching/model-candidates.jsonl'; summary=ROOT/'results/v3-teaching/summary.json'
      return self.respond(200,dict(candidates=[json.loads(x) for x in rows.read_text().splitlines()] if rows.exists() else [],summary=json.loads(summary.read_text()) if summary.exists() else None,targets=['correct',*FAMILIES],protocol=(ROOT/'data/protocol.md').read_text()))
    self.respond(404,{'error':'not found'})
 def do_POST(self):
    try:
      if self.headers.get('Origin') and urllib.parse.urlparse(self.headers['Origin']).netloc!=self.headers.get('Host'): raise ValueError('cross-origin request rejected')
      length=int(self.headers.get('Content-Length',0))
      if not 0<length<=20000: raise ValueError('request size')
      doc=json.loads(self.rfile.read(length))
      if self.path=='/api/generate':
        if not MODEL_LOCK.acquire(blocking=False): return self.respond(429,{'error':'Local generation already running'})
        try: return self.respond(200,generate(doc['contract']))
        finally: MODEL_LOCK.release()
      if self.path=='/api/replay':
        review=doc.get('review',{})
        if review.get('confirmed') is not True or review.get('contract')!=doc.get('contract') or review.get('candidate')!=doc.get('candidate') or not isinstance(doc.get('contract'),str) or not doc['contract'].strip(): raise ValueError('Explicit review of this exact contract and candidate is required')
        target=doc['target']
        if target not in ('correct',*FAMILIES): raise ValueError('unknown target')
        result=execute(doc['candidate'],target)
        provenance=dict(doc.get('provenance',{'source':'manual UI input, not model output'})); provenance['human_review']={'confirmed':True,'contract':doc['contract'],'candidate':doc['candidate'],'limitation':'User attestation; not an automatic semantic proof or authentication'}
        result['bundle']=bundle(doc['candidate'],target,provenance) if result['detected'] else None
        return self.respond(200,result)
      self.respond(404,{'error':'not found'})
    except Exception as e: self.respond(400,{'error':str(e)})
if __name__=='__main__':
    print('SafeRouter ReplayLab http://127.0.0.1:19564',flush=True)
    ThreadingHTTPServer((os.getenv('BIND','127.0.0.1'),int(os.getenv('PORT','19564'))),Handler).serve_forever()
