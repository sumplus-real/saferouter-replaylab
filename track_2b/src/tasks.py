def canonical(doc):
    mapping={}; result=[]
    for op in doc['ops']:
        v=dict(op); k=v['key']; mapping.setdefault(k,str(len(mapping))); v['key']=mapping[k]; result.append(v)
    return result
def conforms(doc,task):
    return task['expected'] is not None and canonical(doc)==canonical(task['expected'])
