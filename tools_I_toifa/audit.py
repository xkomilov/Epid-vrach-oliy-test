import sys,re,glob,difflib
sys.path.insert(0,'.')
import build
tot=short=clause=sim=hint=0; clause_qs=[]; sim_qs=[]
CL=re.compile(r"(, (chunki|bunda|ular|u |bu |ya'ni|shuning|natijada)|\bchunki\b)",re.I)
for p in sorted(glob.glob('q/*.txt')):
    n=p[2:-4].split('/')[-1]
    t,qs,_,_=build.parse(p)
    for i,q in enumerate(qs,1):
        tot+=1; ok=q['ok']; w=q['bad']
        if len(ok)<min(map(len,w)): short+=1
        cw=sum(bool(CL.search(x)) for x in w)
        if cw>=3 and not CL.search(ok): clause+=1; clause_qs.append((n,i))
        for a in range(5):
            o=[ok]+w
        for a in range(5):
            for b in range(a+1,5):
                if difflib.SequenceMatcher(None,o[a],o[b]).ratio()>0.9: sim+=1; sim_qs.append((n,i)); break
            else: continue
            break
        if re.search(r"boshqa variant|to'g'ri javob:",q['note'],re.I): hint+=1
print('total',tot,'correct strictly shortest',short,'3+ wrong w/ clause tell, correct none',clause,'near-duplicate options',sim,'hint notes',hint)
print(clause_qs[:40]); print(sim_qs[:40])
