import json, re, difflib, sys
ws=json.load(open('/home/claude/ep01work/words.json'))
SCRIPT=open('/home/claude/spicesoftheworld/spicesOftheWorld/scripts/episode-01-read-aloud.md').read()
def toks(t): return re.findall(r"[A-Za-z0-9'’\-]+[,.;:!?—]*|—", t)
def norm(w): return re.sub(r"[^a-z0-9]","",w.lower())
def align(script_text, t0, t1):
    sw=[w for w in toks(script_text) if norm(w)]
    rw=[w for w in ws if t0<=w['s']<t1]
    n,m=len(sw),len(rw)
    S=[[0]*(m+1) for _ in range(n+1)]; B=[[0]*(m+1) for _ in range(n+1)]
    for i in range(1,n+1):
        for j in range(1,m+1):
            a,b=norm(sw[i-1]),norm(rw[j-1]['w']); r=difflib.SequenceMatcher(None,a,b).ratio()
            sc=(r-0.45)*2 if r>0.45 else -0.6
            best=(S[i-1][j-1]+sc,0)
            if S[i-1][j]-0.15>best[0]: best=(S[i-1][j]-0.15,1)
            if S[i][j-1]-0.15>best[0]: best=(S[i][j-1]-0.15,2)
            S[i][j],B[i][j]=best
    i,j=n,m; anch={}
    while i>0 and j>0:
        if B[i][j]==0:
            a,b=norm(sw[i-1]),norm(rw[j-1]['w'])
            if difflib.SequenceMatcher(None,a,b).ratio()>0.45: anch[i-1]=(rw[j-1]['s'],rw[j-1]['e'])
            i-=1;j-=1
        elif B[i][j]==1: i-=1
        else: j-=1
    # interpolate
    times=[None]*n
    keys=sorted(anch)
    first,last=rw[0]['s'],rw[-1]['e']
    pts=[(-1,first,first)]+[(k,anch[k][0],anch[k][1]) for k in keys]+[(n,last,last)]
    for (k0,_,e0),(k1,s1,_) in zip(pts,pts[1:]):
        gap=list(range(k0+1,k1))
        if not gap: continue
        tot=sum(len(norm(sw[g]))+2 for g in gap); t=e0
        for g in gap:
            d=(s1-e0)*(len(norm(sw[g]))+2)/tot; times[g]=(t,t+d); t+=d
    for k in keys: times[k]=anch[k]
    res=[[sw[i],times[i][0],times[i][1]] for i in range(n)]
    i=0
    while i<n:   # spread runs of words that collapsed onto one timestamp
        j=i
        while j+1<n and abs(res[j+1][1]-res[i][1])<1e-6: j+=1
        if j>i:
            nxt=res[j+1][1] if j+1<n else res[j][2]+0.5
            span=max(nxt-res[i][1],0.15*(j-i+1)); 
            tot=sum(len(norm(res[k][0]))+2 for k in range(i,j+1)); t=res[i][1]
            for k in range(i,j+1):
                d=span*(len(norm(res[k][0]))+2)/tot; res[k][1]=t; res[k][2]=t+d; t+=d
        i=j+1
    return [tuple(r) for r in res], len(keys)/n
if __name__=="__main__":
    t0,t1=float(sys.argv[1]),float(sys.argv[2]); para=sys.argv[3]
    out,frac=align(para,t0,t1); print("anchor frac",round(frac,2))
    for w,s,e in out: print(f"{s:6.2f} {w}")
