def solve():
    M, N = map(int, input().split())
    g = [input().split() for _ in range(M)]

    dxy = [(-1,0),(0,1),(1,0),(0,-1)]  # up, right, down, left

    def reflect(ch, d):
        if ch == '/':
            return [1,0,3,2][d]
        if ch == '\\':
            return [3,2,1,0][d]
        return d

    seen_global = set()
    ans = 0

    for i in range(M):
        for j in range(N):
            for d in range(4):
                if (i,j,d) in seen_global:
                    continue
                visited = {}
                path = []
                x,y,dirc = i,j,d
                step = 0
                while True:
                    if not (0 <= x < M and 0 <= y < N):
                        break
                    state = (x,y,dirc)
                    if state in visited:
                        loop_start = visited[state]
                        loop_cells = {p[0:2] for p in path[loop_start:]}
                        ans = max(ans, len(loop_cells))
                        break
                    if state in seen_global:
                        break
                    visited[state] = step
                    path.append(state)
                    seen_global.add(state)
                    dirc = reflect(g[x][y], dirc)
                    dx,dy = dxy[dirc]
                    x,y = x+dx,y+dy
                    step += 1
    print(ans)
