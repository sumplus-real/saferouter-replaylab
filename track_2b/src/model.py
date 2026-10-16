"""Apertus non-thinking Chat Completions + fixed structured output; independent DSL gate."""
import json, os, time, urllib.request, urllib.parse
from core import validate
PROTOCOL='apertus-chat-json-schema-v3-teaching'
SYSTEM='Generate exactly the API operation sequence requested, with no extra operations. Return ops only. request requires op,key,stream,break_at; retry and cancel require only op,key. Use arbitrary logical keys. Reuse a key to refer to the same request, use different keys for independent requests. break_at none unless requested before_headers or after_first_chunk. A nonexistent key may be used for a requested negative test. Never add a prerequisite request for a negative retry/cancel test. No expected answers or executable code. If the requested operation sequence is not specified unambiguously, return {"reject":"ambiguous"}. If the contract requires any operation outside request/retry/cancel, return {"reject":"out_of_scope"}. The runtime permits at most12 operations and4 distinct keys; return {"reject":"resource_limit"} for requests exceeding these limits. Retrying/cancelling unknown keys and cancelled or completed requests are valid test inputs, not reasons to refuse.'
TEACHING=[{'role': 'user', 'content': 'Start a non-streaming request, retry that request once, then start a different non-streaming request.'}, {'role': 'assistant', 'content': '{"ops":[{"op":"request","key":"x","stream":false,"break_at":"none"},{"op":"retry","key":"x"},{"op":"request","key":"y","stream":false,"break_at":"none"}]}'}, {'role': 'user', 'content': 'Cancel a missing key three times total, then retry that same key once. Send no new request.'}, {'role': 'assistant', 'content': '{"ops":[{"op":"cancel","key":"z"},{"op":"cancel","key":"z"},{"op":"cancel","key":"z"},{"op":"retry","key":"z"}]}'}]
KEY={'type':'string','minLength':1,'maxLength':16,'pattern':'^[a-z][a-z0-9_]{0,15}$'}
ITEMS=[]
for op in ['request','retry','cancel']:
    props={'op':{'const':op},'key':KEY}
    if op=='request':props.update(stream={'type':'boolean'},break_at={'enum':['none','before_headers','after_first_chunk']})
    ITEMS.append({'type':'object','properties':props,'required':list(props),'additionalProperties':False})
OPS_SCHEMA={'type':'object','properties':{'ops':{'type':'array','minItems':1,'maxItems':12,'items':{'oneOf':ITEMS}}},'required':['ops'],'additionalProperties':False}
SCHEMA={'oneOf':[OPS_SCHEMA,{'type':'object','properties':{'reject':{'enum':['ambiguous','out_of_scope','resource_limit']}},'required':['reject'],'additionalProperties':False}]}
def endpoint():
    url=os.getenv('LLM_BASE_URL','http://127.0.0.1:19464').rstrip('/').removesuffix('/v1')
    parsed=urllib.parse.urlparse(url)
    if parsed.scheme!='http' or parsed.hostname not in ('127.0.0.1','localhost','host.docker.internal','apertus') or parsed.username is not None or parsed.password is not None or parsed.query or parsed.fragment:raise ValueError('Only configured local on-premise model host allowed')
    return url

class NoModelRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        raise ValueError('Model endpoint redirects are not allowed')

def model_name():
    name=os.getenv('LLM_NAME','Apertus-v1.5-8B-Q4_K_M')
    if not name or len(name)>200 or any(ord(c)<32 or ord(c)==127 for c in name):raise ValueError('Invalid LLM_NAME')
    return name

def post(path,data):
    headers={'Content-Type':'application/json'}
    key=os.getenv('LLM_API_KEY','')
    if key:
        if len(key)>8192 or any(not 33<=ord(c)<=126 for c in key):raise ValueError('LLM_API_KEY must contain printable non-space ASCII')
        headers['Authorization']='Bearer '+key
    req=urllib.request.Request(endpoint()+path,data=json.dumps(data).encode(),headers=headers)
    # Local-only traffic must neither follow redirects nor inherit an external HTTP proxy.
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoModelRedirect())
    with opener.open(req,timeout=120) as res:return json.load(res)

def extract(tokens,stop_limit=False):
    """Legacy native-thinking evidence helper; never applied to non-thinking chat content."""
    if stop_limit or tokens.count(32)!=1 or tokens.count(33)!=1 or tokens.index(32)>=tokens.index(33):raise ValueError('invalid/truncated Apertus thinking boundary')
    return [x for x in tokens[tokens.index(33)+1:] if x!=68]

def request_for(contract):
    if not isinstance(contract,str) or not 1<=len(contract)<=1200:raise ValueError('contract length')
    return {'model':model_name(),'messages':[{'role':'system','content':SYSTEM},*TEACHING,{'role':'user','content':contract}],'temperature':0,'seed':42,'max_tokens':450,'response_format':{'type':'json_schema','json_schema':{'name':'router_proposal','strict':True,'schema':SCHEMA}},'chat_template_kwargs':{'enable_thinking':False}}

def decode_chat(raw):
    choice=raw['choices'][0]
    if choice['finish_reason']!='stop':raise ValueError('truncated or incomplete chat response')
    text=choice['message']['content']
    if not isinstance(text,str):raise ValueError('chat content must be a string')
    answer=json.loads(text)
    if type(answer) is dict and set(answer)=={'reject'} and answer['reject'] in ('ambiguous','out_of_scope','resource_limit'):return text,{'rejected':answer['reject']}
    validate(answer)
    return text,{'candidate':answer}

def generate(contract):
    request=request_for(contract);start=time.monotonic();record={'protocol':PROTOCOL,'model':model_name(),'contract':contract,'request':request}
    try:
        raw=post('/v1/chat/completions',request);record['raw']=raw
        record['answer_text']=raw['choices'][0]['message'].get('content')
        text,accepted=decode_chat(raw);record.update(accepted);record['answer_text']=text
    except Exception as e:
        record['error']=str(e)
        if str(e)=='at most four logical keys' or (str(e)=='1..12 operations required' and isinstance(record.get('answer_text'),str)):
            try:
                untrusted=json.loads(record['answer_text'])
                if isinstance(untrusted,dict) and isinstance(untrusted.get('ops'),list) and (len(untrusted['ops'])>12 or str(e)=='at most four logical keys'):
                    record['untrusted_candidate']=untrusted;record['validation_rejection']={'kind':'resource_limit','source':'independent runtime validator','detail':str(e)}
            except (ValueError,TypeError):pass
    record['seconds']=time.monotonic()-start
    return record
