from fractions import Fraction
import sys

def read_ints():
    return list(map(int, sys.stdin.readline().split()))

def on_segment(px,py,x1,y1,x2,y2):
    # check collinear and within bounding box
    # cross product
    if (x2-x1)*(py-y1) - (y2-y1)*(px-x1) != 0:
        return False
    if not (min(x1,x2) <= px <= max(x1,x2) and min(y1,y2) <= py <= max(y1,y2)):
        return False
    return True

def seg_intersections(seg1, seg2):
    # return a set of intersection points (usually 0 or 1),
    # include shared endpoints even if lines are collinear
    (x1,y1,x2,y2) = seg1
    (x3,y3,x4,y4) = seg2
    pts = set()
    # check shared endpoints first
    for (a,b) in [(x1,y1),(x2,y2)]:
        for (c,d) in [(x3,y3),(x4,y4)]:
            if a==c and b==d:
                pts.add((a,b))
    # general line intersection via determinants
    denom = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if denom == 0:
        # parallel or collinear - we already captured shared endpoints above
        return pts
    numx = (x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4 - y3*x4)
    numy = (x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4 - y3*x4)
    px = Fraction(numx, denom)
    py = Fraction(numy, denom)
    # only consider integer-coord intersections (grid/corner intersections)
    if px.denominator != 1 or py.denominator != 1:
        return pts
    pxi = px.numerator
    pyi = py.numerator
    # check it lies on both segments
    if on_segment(pxi, pyi, x1,y1,x2,y2) and on_segment(pxi, pyi, x3,y3,x4,y4):
        pts.add((pxi, pyi))
    return pts

def cell_distance(px,py, x,y):
    return max(abs(px-x), abs(py-y))

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        print(0)
        return
    it = iter(data)
    N = int(next(it))
    segs = []
    for _ in range(N):
        x1 = int(next(it)); y1 = int(next(it)); x2 = int(next(it)); y2 = int(next(it))
        segs.append((x1,y1,x2,y2))
    K = int(next(it))

    # collect candidate intersection points
    pts = set()
    for i in range(N):
        for j in range(i+1, N):
            pts |= seg_intersections(segs[i], segs[j])

    total = 0
    for p in pts:
        px,py = p
        lines_here = []
        for i in range(N):
            if on_segment(px,py, *segs[i]):
                lines_here.append(i)
        if len(lines_here) != K:
            continue
        counts = []
        for idx in lines_here:
            x1,y1,x2,y2 = segs[idx]
            # if px,py equals an endpoint, it's one-sided
            is_end_a = (px==x1 and py==y1)
            is_end_b = (px==x2 and py==y2)
            if is_end_a and is_end_b:
                # degenerate zero-length (shouldn't happen per constraints), skip
                continue
            if is_end_a:
                counts.append(cell_distance(px,py, x2,y2))
            elif is_end_b:
                counts.append(cell_distance(px,py, x1,y1))
            else:
                counts.append(cell_distance(px,py, x1,y1))
                counts.append(cell_distance(px,py, x2,y2))
        if counts:
            intensity = min(counts)
            total += intensity

    print(total)

if __name__ == "__main__":
    main()
