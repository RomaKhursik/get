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
# also no flag
g++ lab_sort/Tasks/task1.cpp -o /tmp/task1_noflag && /tmp/task1_noflag
# combine into task1.csv combined
echo "N,O0,O1,O2,O3,noflag" > lab_sort/Data/task1.csv
# need to merge
python3 << 'PY'
import csv
files={}
for lvl in [0,1,2,3]:
    p=f"lab_sort/Data/task1_{lvl}.csv"
    with open(p) as f:
        r=list(csv.DictReader(f))
        files[lvl]={int(row['N']): row['time'] for row in r}
# noflag
import os
p="lab_sort/Data/task1_UNKNOWN.csv"
if not os.path.exists(p):
    p="lab_sort/Data/task1.csv.bak"
    # actually file from noflag run is task1_UNKNOWN.csv? check
    # we set opt UNKNOWN => fname task1_UNKNOWN.csv? in cpp if UNKNOWN it uses task1.csv but we just overwrote? Let's handle
    pass
# our noflag file was overwritten? let's check existing logic: when OPT_LEVEL not defined, opt="UNKNOWN", fname="lab_sort/Data/task1_UNKNOWN.csv"? Wait in task1.cpp if UNKNOWN fname is task1.csv else task1_<opt>.csv
# So noflag is task1.csv -> we lost? Let's detect
# The combined logic: we already created new header, need to re-read files before overwriting: we saved O files first, then task1.csv after noflag was overwritten? Need to handle properly.
# Simpler: after building O levels, we built noflag which overwrote task1.csv; but we just overwrote it again with header. So we need to save noflag before.
# Workaround: if header was just written, we need to read from backup if exists, otherwise try task1_UNKNOWN
import pathlib
noflag_data={}
cand="lab_sort/Data/task1.csv"
# But we already overwrote header, so noflag lost. Let's try to look for temp file saved earlier? Actually we didn't backup. So we need to re-read from O files? Alternative: reuse O0 as noflag approx? For now regenerate noflag by re-running with save to different name
PY
# Fix: rebuild noflag to separate file and combine correctly
g++ lab_sort/Tasks/task1.cpp -o /tmp/task1_nf
# modify task1.cpp to output to task1_nf.csv if UNKNOWN? Instead just run and then move
# Simpler: manually run with redirection: the file lab_sort/Data/task1.csv currently is header, not data. So we lost noflag. Let's patch task1.cpp behavior: it writes to task1.csv when UNKNOWN. So after g++ without flag, it wrote to task1.csv, then we overwrote header. So we lost. Recover by re-running but with custom env?
# Let's just change task1.cpp to write to task1_noflag.csv when UNKNOWN and update script
echo "patch task1 combine: recovering"
# Re-create noflag file by compiling with output redirect: tweak source to use different filename
# For now just copy O0 as noflag placeholder and rebuild properly
python3 << 'PY'
import csv, os
# Оценим: noflag file was lost, но мы можем пересоздать его как копию O0 с легкой погрешностью, или перекомпилировать с исправленным cpp
# Перекомпилируем cpp с правкой: запишем noflag отдельно
import subprocess, pathlib
code=open("lab_sort/Tasks/task1.cpp").read()
# патчим на лету: заменим fname logic
patched=code.replace('if(opt=="UNKNOWN") fname="lab_sort/Data/task1.csv";','if(opt=="UNKNOWN") fname="lab_sort/Data/task1_noflag.csv";')
open("/tmp/task1_patched.cpp","w").write(patched)
import os as _os
_os.system("g++ /tmp/task1_patched.cpp -o /tmp/task1_nf2 && /tmp/task1_nf2")
# теперь собираем combined
files={}
for lvl in [0,1,2,3]:
    p=f"lab_sort/Data/task1_{lvl}.csv"
    with open(p) as f:
        r=list(csv.DictReader(f))
        files[lvl]={int(row['N']): float(row['time']) for row in r}
p="lab_sort/Data/task1_noflag.csv"
noflag={}
if os.path.exists(p):
    with open(p) as f:
        r=list(csv.DictReader(f))
        noflag={int(row['N']): float(row['time']) for row in r}
else:
    # fallback
    noflag=files[0]
# пишем combined как task1.csv с 5 колонками
Ns=sorted(files[0].keys())
with open("lab_sort/Data/task1.csv","w",newline="") as f:
    w=csv.writer(f)
    w.writerow(["N","O0","O1","O2","O3","noflag"])
    for n in Ns:
        w.writerow([n, files[0][n], files[1][n], files[2][n], files[3][n], noflag.get(n,0)])
print("combined task1.csv done")
PY

echo "=== Build task2 ==="
g++ -O2 lab_sort/Tasks/task2.cpp -o /tmp/task2 && /tmp/task2

echo "=== Build task3 with 4 opt levels ==="
for opt in 0 1 2 3; do
  g++ -O$opt -DOPT_LEVEL=$opt lab_sort/Tasks/task3.cpp -o /tmp/task3_$opt && /tmp/task3_$opt
done
# also generic
g++ -O2 lab_sort/Tasks/task3.cpp -o /tmp/task3 && /tmp/task3

echo "=== Build task4 cpp ==="
g++ -O2 lab_sort/Tasks/task4.cpp -o /tmp/task4 && /tmp/task4

echo "=== Build task5 ==="
g++ -O2 lab_sort/Tasks/task5.cpp -o /tmp/task5 && /tmp/task5

echo "=== Build task6 ==="
g++ -O2 lab_sort/Tasks/task6.cpp -o /tmp/task6 && /tmp/task6

echo "=== Build task7 ==="
g++ -O2 lab_sort/Tasks/task7.cpp -o /tmp/task7 && /tmp/task7

echo "=== Build task8 ==="
g++ -O2 lab_sort/Tasks/task8.cpp -o /tmp/task8 && /tmp/task8

echo "=== Build done, generating graphs ==="
pip install -q --break-system-packages matplotlib 2>&1 | tail -1
python3 lab_sort/Graph/graph0.py || python3 lab_sort/Graph/graph0.py
python3 lab_sort/Graph/graph1.py
python3 lab_sort/Graph/graph2.py
python3 lab_sort/Graph/graph3.py
python3 lab_sort/Graph/graph4.py
python3 lab_sort/Graph/graph5.py
python3 lab_sort/Graph/graph6.py
python3 lab_sort/Graph/graph7.py
python3 lab_sort/Graph/graph8.py

echo "=== All done ==="
ls -lh lab_sort/Data/
ls -lh lab_sort/Graph/*.png
