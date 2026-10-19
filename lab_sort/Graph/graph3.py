import csv, os, matplotlib.pyplot as plt, math
base="lab_sort/Data/task3"
if not os.path.exists(base+"_0.csv") and os.path.exists("../Data/task3_0.csv"):
    base="../Data/task3"
    outdir=""
else:
    outdir="lab_sort/Graph/"

levels=[0,1,2,3]
# соберем ускорения
# для каждого уровня читаем файл
datas={}
for lv in levels:
    p=f"{base}_{lv}.csv"
    if not os.path.exists(p):
        p=f"lab_sort/Data/task3_{lv}.csv"
    if not os.path.exists(p):
        print("missing",p)
        continue
    N=[]; d={}
    with open(p) as f:
        r=csv.DictReader(f)
        for row in r:
            N.append(int(row['N']))
            for k in ['bubble','insertion','selection','heap','quick','merge']:
                d.setdefault(k, []).append(float(row[k]))
    datas[lv]=(N,d)

# также пробуем noflag
p=f"lab_sort/Data/task3.csv"
if not os.path.exists(p):
    p="../Data/task3.csv"
if os.path.exists(p):
    try:
        N=[]; d={}
        with open(p) as f:
            r=csv.DictReader(f)
            if 'bubble' in r.fieldnames:
                for row in r:
                    N.append(int(row['N']))
                    for k in ['bubble','insertion','selection','heap','quick','merge']:
                        d.setdefault(k, []).append(float(row[k]))
                datas['noflag']=(N,d)
    except: pass

# строим 4 графика + табличка ускорения
# ускорение считаем как среднее отношение t_noopt / t_Olevel
# если noflag нет, то берем O0 как базу

for lv in levels:
    if lv not in datas: continue
    N,d=datas[lv]
    plt.figure()
    for k,marker in [('bubble','o'),('insertion','s'),('selection','^'),('heap','v'),('quick','D'),('merge','p')]:
        plt.plot(N,d[k],label=k,marker=marker)
    plt.xlabel('N'); plt.ylabel('time, s'); plt.title(f'Task3: All 6 sorts with -O{lv}'); plt.legend(); plt.grid(True)
    plt.savefig(f"{outdir}task3_O{lv}.png" if outdir else f"task3_O{lv}.png", dpi=150)
    try: plt.savefig(f"lab_sort/Graph/task3_O{lv}.png", dpi=150)
    except: pass
    print(f"saved O{lv}")
    plt.close()

# табличка ускорений: 6 алгоритмов *4 оптимизации, относительно O0
if 0 in datas:
    N0,d0=datas[0]
    table=[]
    for algo in ['bubble','insertion','selection','heap','quick','merge']:
        row=[]
        for lv in levels:
            if lv==0:
                row.append(1.0)
            else:
                if lv in datas:
                    _,d=datas[lv]
                    # среднее ускорение = среднее по N t0/t
                    vals=[a/b if b!=0 else 0 for a,b in zip(d0[algo], d[algo])]
                    avg=sum(vals)/len(vals) if vals else 0
                    row.append(avg)
                else:
                    row.append(0)
        table.append((algo,row))
    # сохраняем csv таблицу
    with open("lab_sort/Graph/task3_speedup.csv","w",newline="") as f:
        import csv
        w=csv.writer(f)
        w.writerow(["algo","O0","O1","O2","O3"])
        for algo,row in table:
            w.writerow([algo]+[f"{x:.2f}" for x in row])
    print("saved speedup csv")
    # также график таблички
    plt.figure(figsize=(8,4))
    plt.axis('off')
    plt.table(cellText=[[f"{x:.2f}" for x in r] for _,r in table],
              rowLabels=[a for a,_ in table], colLabels=['O0','O1','O2','O3'], loc='center')
    plt.title('Speedup vs O0')
    plt.savefig(f"{outdir}task3_speedup.png" if outdir else "task3_speedup.png", dpi=150, bbox_inches='tight')
    try: plt.savefig("lab_sort/Graph/task3_speedup.png", dpi=150, bbox_inches='tight')
    except: pass

# если нет O0 данных, но есть общий task3.csv - делаем один график
if not datas and os.path.exists("lab_sort/Data/task3.csv"):
    import csv
    N=[]; d={'bubble':[],'insertion':[],'selection':[],'heap':[],'quick':[],'merge':[]}
    with open("lab_sort/Data/task3.csv") as f:
        r=csv.DictReader(f)
        for row in r:
            N.append(int(row['N']))
            for k in d: d[k].append(float(row[k]))
    plt.figure()
    for k,m in [('bubble','o'),('insertion','s'),('selection','^'),('heap','v'),('quick','D'),('merge','p')]:
        plt.plot(N,d[k],label=k,marker=m)
    plt.xlabel('N'); plt.ylabel('time'); plt.title('Task3: Hulk vs Loki'); plt.legend(); plt.grid(True)
    plt.savefig("lab_sort/Graph/task3.png", dpi=150)
