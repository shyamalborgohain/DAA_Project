from bisect import bisect_left, bisect_right
from collections import deque
from math import inf

def optimal_transmitters(posts, L, candidates, r=500):
    P = sorted(q%L for q in posts)
    n = len(P)
    if n == 0:
        return 0, []
    if not candidates:
        return None
    if 2*r >= L:
        return 0, [candidates[0]]
    
    extP = [q-L for q in P] + P + [q+L for q in P]
    locs = {}
    for ca in candidates:
        c = ca % L
        lo = bisect_left(extP, c - r)
        hi = bisect_right(extP, c + r) - 1
        if lo > hi:
            continue
        lo, hi = lo - n, hi - n
        shift = (lo//n)*n
        lo, hi = lo -shift, hi - shift
        if hi - lo + 1 >= n:
            return 0, [ca]
        locs.setdefault((lo, hi), ca)
    
    arcs = sorted(locs)
    M = len(arcs)
    if M == 0:
        return None
    
    start = [arc[0] for arc in arcs]
    end = [arc[1] for arc in arcs]
    sg, eg = [0]*M, [0]*M
    for i in range(1, M):
        sg[i] = sg[i-1] if start[i] == start[i-1] else i
        eg[i] = eg[i-1] if end[i] == end[i-1] else i
        
    lo_idx = [bisect_left(end, start[i]-1) for i in range(M)]
    hi_idx = [min(sg[i], eg[i]) - 1 for i in range(M)]
    
    best, best_chain = inf, None
    for a in range(M):
        sa = start[a]
        dp = [inf]*M
        dp[a] = 0
        par = [-1]*M
        dq = deque()
        ptr = a
        for i in range(a+1, M):
            if start[i] == sa:
                continue
            while ptr <= hi_idx[i]:
                if dp[ptr] < inf:
                    val = dp[ptr] + end[ptr]
                    while dq and dq[-1][0] >= val:
                        dq.pop()
                    dq.append((val, ptr))
                ptr += 1
            
            lo = max(a, lo_idx[i])
            while dq and dq[0][1] < lo:
                dq.popleft()
            if dq:
                dp[i] = dq[0][0] - start[i] + 1
                par[i] = dq[0][1]
            
        for i in range(a, M):
            if dp[i] < inf and end[i] >= sa + n - 1:
                cost = dp[i] + max(0, end[i] - sa - n + 1)
                if cost < best:
                    best = cost
                    chain = []
                    k = i
                    while k != -1:
                        chain.append(k)
                        k = par[k]
                    best_chain =  chain[::-1]
    
    if best == inf:
        return None
    
    return best, [locs[arcs[k]] for k in best_chain]



if __name__ == "__main__":
    posts = [100, 400, 700, 900]
    L = 1000
    candidates = [50, 350, 650, 950]
    print(*optimal_transmitters(posts, L, candidates, r=250))