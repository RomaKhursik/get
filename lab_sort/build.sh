#!/bin/bash
set -e
cd "$(dirname "$0")/.."
mkdir -p lab_sort/Data lab_sort/Graph
echo "=== Build task0 ==="
g++ -O2 lab_sort/Tasks/task0.cpp -o /tmp/task0 && /tmp/task0
echo "=== Build task1 with 5 opt levels ==="
for opt in 0 1 2 3; do
  g++ -O$opt -DOPT_LEVEL=$opt lab_sort/Tasks/task1.cpp -o /tmp/task1_$opt && /tmp/task1_$opt
done
g++ lab_sort/Tasks/task1.cpp -o /tmp/task1_noflag && /tmp/task1_noflag || true
# combine properly (build script version uses OPT_LEVEL, but standalone demo already has combined)
python3 << 'PY'
import csv, os
files={}
for lvl in [0,1,2,3]:
    p=f"lab_sort/Data/task1_{lvl}.csv"
    if os.path.exists(p):
        with open(p) as f:
            r=list(csv.DictReader(f))
            files[lvl]={int(row['N']): float(row['time']) for row in r}
p="lab_sort/Data/task1_noflag.csv"
if not os.path.exists(p):
    # try patched name
    for cand in ["lab_sort/Data/task1.csv","lab_sort/Data/task1_UNKNOWN.csv"]:
        if os.path.exists(cand):
            try:
                with open(cand) as f:
                    r=list(csv.DictReader(f))
                    if 'noflag' in r[0] if r else False:
                        continue
                    if 'time' in r[0]:
                        p=cand
                        break
            except: pass
noflag={}
if os.path.exists(p):
    with open(p) as f:
        r=list(csv.DictReader(f))
        if r and 'time' in r[0]:
            noflag={int(row['N']): float(row['time']) for row in r}
if files and noflag:
    Ns=sorted(files[0].keys())
    with open("lab_sort/Data/task1.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(["N","O0","O1","O2","O3","noflag"])
        for n in Ns:
            w.writerow([n, files[0][n], files[1][n], files[2][n], files[3][n], noflag.get(n,files[0][n])])
    print("combined task1.csv done")
else:
    print("combined skipped, demo file already exists")
PY
echo "=== Build task2 ==="
g++ -O2 lab_sort/Tasks/task2.cpp -o /tmp/task2 && /tmp/task2
echo "=== Build task3 with 4 opt levels ==="
for opt in 0 1 2 3; do
  g++ -O$opt -DOPT_LEVEL=$opt lab_sort/Tasks/task3.cpp -o /tmp/task3_$opt && /tmp/task3_$opt
done
g++ -O2 lab_sort/Tasks/task3.cpp -o /tmp/task3 && /tmp/task3 || true
echo "=== Build task4 cpp ==="
g++ -O2 lab_sort/Tasks/task4.cpp -o /tmp/task4 && /tmp/task4
echo "=== Build task5 ==="
g++ -O2 lab_sort/Tasks/task5.cpp -o /tmp/task5 && /tmp/task5
echo "=== Build task6 ==="
g++ -O2 lab_sort/Tasks/task6.cpp -o /tmp/task6 && /tmp/task6
echo "=== Build graphs ==="
pip install -q --break-system-packages matplotlib 2>&1 | tail -1 || true
python3 lab_sort/Graph/graph0.py
python3 lab_sort/Graph/graph1.py
python3 lab_sort/Graph/graph2.py
python3 lab_sort/Graph/graph3.py
python3 lab_sort/Graph/graph4.py
python3 lab_sort/Graph/graph5.py
python3 lab_sort/Graph/graph6.py
echo "=== All done ==="
ls -lh lab_sort/Data/
ls -lh lab_sort/Graph/*.png
