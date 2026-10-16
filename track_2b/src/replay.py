import argparse,json
from core import verify_bundle
p=argparse.ArgumentParser();p.add_argument('bundle');a=p.parse_args()
with open(a.bundle) as f: b=json.load(f)
verify_bundle(b)
print(json.dumps({'verified':True,'sha256':b['sha256'],'operations':len(b['payload']['minimized']['ops']),'target':b['payload']['mutant']},indent=2))
