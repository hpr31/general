import numpy as np

def solve():
    n = int(input().strip())
    g = [list(input().strip()) for _ in range(n)]
    
    nodes = {}
    idx = 0
    for i in range(n):
        for j in range(n):
            if g[i][j] != ' ':
                nodes[(i,j)] = idx
                idx += 1
    
    edges = []
    for (i,j), u in nodes.items():
        c = g[i][j]
        for di,dj,allowed in [(1,0,"|+."),(-1,0,"|+."),(0,1,"-+."),(0,-1,"-+.")]:
            ni, nj = i+di, j+dj
            if (ni,nj) in nodes:
                v = nodes[(ni,nj)]
                nc = g[ni][nj]
                if (c in "|+." and nc in "|+." and di!=0) or (c in "-+." and nc in "-+." and dj!=0):
                    w = 1 if c in "|-" else 0
                    edges.append((u,v,w))
    
    # build conductance matrix
    N = len(nodes)
    G = np.zeros((N,N))
    for u,v,w in edges:
        g = 1/w if w>0 else 1e9  # junction ~ infinite conductance
        G[u,u]+=g
        G[v,v]+=g
        G[u,v]-=g
        G[v,u]-=g
    
    # find terminals
    terms = [nodes[p] for p in nodes if g[p[0]][p[1]]=='.']
    s,t = terms
    
    # apply unit current
    I = np.zeros(N)
    I[s]=1
    I[t]=-1
    
    # remove reference node (ground)
    mask = [i for i in range(N) if i!=t]
    Gm = G[np.ix_(mask,mask)]
    Im = I[mask]
    V = np.linalg.solve(Gm,Im)
    
    vs = V[mask.index(s)]
    vt = 0
    print(round(vs-vt))
