A trcl example
c cli: --lattice 2,-2:2,-1:2,-2:2
c cells
2 0 -12 11 -14 13 -16 15 lat=1 fill=3 u=2 imp:n=1
3 1 -1.  -31 u=3 imp:n=1
31 2 -2.  31 u=3 imp:n=1
10 0  -2 1 3 -4 -6 5 IMP:N=1 FILL=2  *trcl=148
100 1 -1. -1000 #10 IMP:N=1
1000 0 1000 IMP:N=0

c surfaces
1 PX -5
2 PX 5
3 PY -5
4 PY 5
5 PZ -5
6 PZ 5
11 PX -1
12 PX 1
13 PY -2
14 PY 1
15 PZ -1
16 PZ 1
1000 SO 30
31 SO 0.5

m1 13027 1.
m2 13027 1.
*TR148 -10 2 1 25.34625 64.65375 90 115.34625 25.34625 90 90 90 0
