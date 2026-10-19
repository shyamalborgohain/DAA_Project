import random
from Q10 import optimal_transmitters as f

def cd(a,b,L):
    d=abs(a-b)%L; return min(d,L-d)
def brute(posts,L,c,r):
    n=len(posts)
    if n==0: return 0
    best=None
    for mask in range(1,1<<len(c)):
        cnt=[sum(1 for j in range(len(c)) if mask>>j&1 and cd(p,c[j],L)<=r) for p in posts]
        if min(cnt)>=1:
            v=sum(1 for x in cnt if x>=2); best=v if best is None else min(best,v)
    return best

random.seed(5); bad=0
for _ in range(8000):
    L=random.randint(5,60); r=random.randint(1,15)
    posts=random.sample(range(L),random.randint(1,min(L,10)))
    c=random.sample(range(L),min(random.randint(1,11),L))
    out=f(posts,L,c,r); b=brute(posts,L,c,r)
    if out is None:
        ok = b is None
    else:
        v,locs=out
        cnt=[sum(1 for x in locs if cd(p,x,L)<=r) for p in posts]
        ok = b==v and set(locs)<=set(c) and len(set(locs))==len(locs) and min(cnt)>=1 and sum(1 for x in cnt if x>=2)==v
    if not ok: bad+=1; print(L,r,posts,c,out,b)
print("mismatches",bad)