import sys
def solve():
    data=[l.strip() for l in sys.stdin.readlines()]
    data=[l for l in data if l!='']
    if not data:
        return
    n=int(data[0])
    pmap={}
    idx=0
    es=set()
    for L in data[1:1+n]:
        t=L.split()
        if len(t)!=4:
            continue
        x1,y1,x2,y2=map(int,t)
        if x1==x2 and y1==y2:
            continue
        a=(x1,y1); b=(x2,y2)
        if a not in pmap:
            pmap[a]=idx; idx+=1
        if b not in pmap:
            pmap[b]=idx; idx+=1
        u=pmap[a]; v=pmap[b]
        if u==v:
            continue
        e=(u,v) if u<v else (v,u)
        es.add(e)
    V=len(pmap)
    E=len(es)
    if V==0:
        print(0); return
    g=[[] for _ in range(V)]
    for u,v in es:
        g[u].append(v); g[v].append(u)
    vis=[False]*V
    c=0
    for s in range(V):
        if not vis[s]:
            c+=1
            st=[s]; vis[s]=True
            while st:
                cur=st.pop()
                for nb in g[cur]:
                    if not vis[nb]:
                        vis[nb]=True; st.append(nb)
    print(E - V + c)

if __name__=="__main__":
    solve()
