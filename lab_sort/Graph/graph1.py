import csv, os, matplotlib.pyplot as plt
def find_data(name):
    for p in [f"lab_sort/Data/{name}", f"../Data/{name}", f"Data/{name}", name]:
        if os.path.exists(p): return p
    return f"lab_sort/Data/{name}"
def find_out(name):
    for d in ["lab_sort/Graph","../Graph","Graph","."]:
        if os.path.exists(d): return f"{d}/{name}"
    os.makedirs("lab_sort/Graph", exist_ok=True); return f"lab_sort/Graph/{name}"
# основной файл task1.csv с колонками N,O0,O1,O2,O3,noflag (создается Tasks/task1 при play)
# также поддержим отдельные файлы task1_*.csv для build.sh
combined=find_data("task1.csv")
if os.path.exists(combined):
    try:
        with open(combined) as f:
            r=csv.DictReader(f)
            if all(k in r.fieldnames for k in ["O0","O1","O2","O3","noflag"]):
                N=[]; o0=[]; o1=[]; o2=[]; o3=[]; nf=[]
                for row in r:
                    N.append(int(row['N'])); o0.append(float(row['O0'])); o1.append(float(row['O1'])); o2.append(float(row['O2'])); o3.append(float(row['O3'])); nf.append(float(row['noflag']))
                plt.figure()
                plt.plot(N,o0,label='-O0',marker='o'); plt.plot(N,o1,label='-O1',marker='s'); plt.plot(N,o2,label='-O2',marker='^'); plt.plot(N,o3,label='-O3',marker='D'); plt.plot(N,nf,label='no flag',marker='x',linestyle='--')
                plt.xlabel('N'); plt.ylabel('time, s'); plt.title('Task1: Optimization levels for bubble sort'); plt.legend(); plt.grid(True)
                plt.savefig(find_out("task1.png"), dpi=150); print("saved task1 combined"); plt.close()
                raise SystemExit
    except SystemExit:
        pass
    except: pass
# fallback: отдельные файлы
levels=[0,1,2,3]
data={}
for lv in levels:
    p=find_data(f"task1_{lv}.csv")
    if os.path.exists(p):
        N=[]; t=[]
        with open(p) as f:
            r=csv.DictReader(f)
            for row in r: N.append(int(row['N'])); t.append(float(row['time']))
        data[lv]=(N,t)
# noflag
for cand in [find_data("task1_noflag.csv"), find_data("task1.csv")]:
    if os.path.exists(cand):
        try:
            with open(cand) as f:
                r=csv.DictReader(f)
                if 'time' in r.fieldnames:
                    N=[]; t=[]
                    for row in r: N.append(int(row['N'])); t.append(float(row['time']))
                    data['nf']=(N,t)
                    break
        except: pass
plt.figure()
for k in levels:
    if k in data: N,t=data[k]; plt.plot(N,t,label=f'-O{k}',marker='o')
if 'nf' in data: N,t=data['nf']; plt.plot(N,t,label='no flag',marker='x',linestyle='--')
plt.xlabel('N'); plt.ylabel('time, s'); plt.title('Task1: Optimization levels for bubble sort'); plt.legend(); plt.grid(True)
plt.savefig(find_out("task1.png"), dpi=150); print("saved task1")
