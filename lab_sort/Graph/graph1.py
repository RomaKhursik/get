import csv, os, matplotlib.pyplot as plt
# собираем 5 файлов: task1_0,1,2,3 и task1_None
levels=[0,1,2,3]
labels=['O0','O1','O2','O3','no flag']
files=[]
base="lab_sort/Data/task1"
if not os.path.exists(base+".csv"):
    base="../Data/task1"
    out="task1.png"
    out2="lab_sort/Graph/task1.png"
else:
    out="lab_sort/Graph/task1.png"
    out2=None

# данные: dict level -> (N,time)
data={}
for lv in levels:
    p=f"{base}_{lv}.csv"
    if not os.path.exists(p):
        p=f"lab_sort/Data/task1_{lv}.csv"
    if not os.path.exists(p):
        continue
    N=[]; t=[]
    with open(p) as f:
        r=csv.DictReader(f)
        for row in r:
            N.append(int(row['N'])); t.append(float(row['time']))
    data[lv]=(N,t)

# no flag
p_nf=f"{base}.csv"
alt="lab_sort/Data/task1.csv"
if os.path.exists(alt):
    p_nf=alt
if os.path.exists(p_nf):
    N=[]; t=[]
    with open(p_nf) as f:
        r=csv.DictReader(f)
        # проверяем колонки
        first=r.fieldnames
        for row in r:
            if 'N' in row and 'time' in row:
                N.append(int(row['N'])); t.append(float(row['time']))
            elif 'N' in row:
                # старый формат task0?
                pass
    if N:
        # если есть данные без уровня, считаем это no flag, но если уже есть 4 уровня, добавим как пятый
        data['noflag']=(N,t)

plt.figure()
for k in levels:
    if k in data:
        N,t=data[k]
        plt.plot(N,t,label=f'-O{k}',marker='o')
if 'noflag' in data:
    N,t=data['noflag']
    plt.plot(N,t,label='no flag',marker='x',linestyle='--')
plt.xlabel('N'); plt.ylabel('time, s'); plt.title('Task1: Optimization levels for bubble sort'); plt.legend(); plt.grid(True)
plt.savefig(out, dpi=150)
if os.path.exists("lab_sort/Graph"):
    plt.savefig("lab_sort/Graph/task1.png", dpi=150)
print("saved task1")

# также попробуем прочитать единый объединенный файл если есть
combined="lab_sort/Data/task1_combined.csv"
if os.path.exists(combined):
    import csv
    N=[]; d={0:[],1:[],2:[],3:[], 'nf':[]}
    with open(combined) as f:
        r=csv.DictReader(f)
        for row in r:
            N.append(int(row['N']))
            for k in [0,1,2,3]:
                d[k].append(float(row[f'O{k}']))
            d['nf'].append(float(row['noflag']))
    plt.figure()
    for k in [0,1,2,3]:
        plt.plot(N,d[k],label=f'-O{k}',marker='o')
    plt.plot(N,d['nf'],label='no flag',marker='x',linestyle='--')
    plt.xlabel('N'); plt.ylabel('time'); plt.title('Task1 combined'); plt.legend(); plt.grid(True)
    plt.savefig("lab_sort/Graph/task1.png", dpi=150)
