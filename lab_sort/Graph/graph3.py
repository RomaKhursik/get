import csv, os, matplotlib.pyplot as plt
def find_data(name):
    for p in [f"lab_sort/Data/{name}", f"../Data/{name}", f"Data/{name}", name]:
        if os.path.exists(p): return p
    return f"lab_sort/Data/{name}"
def find_out(name):
    for d in ["lab_sort/Graph","../Graph","Graph","."]:
        if os.path.exists(d): return f"{d}/{name}"
    os.makedirs("lab_sort/Graph", exist_ok=True); return f"lab_sort/Graph/{name}"
levels=[0,1,2,3]
datas={}
for lv in levels:
    p=find_data(f"task3_{lv}.csv")
    if os.path.exists(p):
        N=[]; d={}
        with open(p) as f:
            r=csv.DictReader(f)
            for row in r:
                N.append(int(row['N']))
                for k in ['bubble','insertion','selection','heap','quick','merge']:
                    d.setdefault(k, []).append(float(row[k]))
        datas[lv]=(N,d)
# если есть общий task3.csv как demo
if os.path.exists(find_data("task3.csv")):
    try:
        p=find_data("task3.csv")
        with open(p) as f:
            r=csv.DictReader(f)
            if 'bubble' in r.fieldnames:
                # если это уже общий файл с 6 колонками, используем как один из уровней
                if 2 not in datas:
                    N=[]; d={}
                    f.seek(0); r=csv.DictReader(f)
                    for row in r:
                        N.append(int(row['N']))
                        for k in ['bubble','insertion','selection','heap','quick','merge']:
                            d.setdefault(k, []).append(float(row[k]))
                    datas['demo']=(N,d)
    except: pass
# строим графики
for lv in levels:
    if lv not in datas: continue
    N,d=datas[lv]
    plt.figure()
    for k,m in [('bubble','o'),('insertion','s'),('selection','^'),('heap','v'),('quick','D'),('merge','p')]:
        plt.plot(N,d[k],label=k,marker=m)
    plt.xlabel('N'); plt.ylabel('time, s'); plt.title(f'Task3: All 6 sorts with -O{lv}'); plt.legend(); plt.grid(True)
    plt.savefig(find_out(f"task3_O{lv}.png"), dpi=150); print(f"saved O{lv}"); plt.close()
# demo файл если нет O файлов
if not any(lv in datas for lv in levels) and 'demo' in datas:
    N,d=datas['demo']
    plt.figure()
    for k,m in [('bubble','o'),('insertion','s'),('selection','^'),('heap','v'),('quick','D'),('merge','p')]:
        plt.plot(N,d[k],label=k,marker=m)
    plt.xlabel('N'); plt.ylabel('time, s'); plt.title('Task3: Hulk vs Loki (demo O2)'); plt.legend(); plt.grid(True)
    plt.savefig(find_out("task3.png"), dpi=150); print("saved demo")
# табличка ускорений относительно O0
if 0 in datas:
    N0,d0=datas[0]
    table=[]
    for algo in ['bubble','insertion','selection','heap','quick','merge']:
        row=[]
        for lv in levels:
            if lv==0: row.append(1.0)
            else:
                if lv in datas:
                    _,d=datas[lv]
                    vals=[a/b if b!=0 else 0 for a,b in zip(d0[algo], d[algo])]
                    avg=sum(vals)/len(vals) if vals else 0
                    row.append(avg)
                else: row.append(0)
        table.append((algo,row))
    with open(find_out("task3_speedup.csv").replace(".png",".csv") if False else find_data("task3_speedup.csv").replace("task3_speedup.csv","../Graph/task3_speedup.csv"),"w",newline="") as f:
        pass
    # пробуем сохранить в разные места
    for outp in [find_out("task3_speedup.csv"), "lab_sort/Graph/task3_speedup.csv"]:
        try:
            import csv as csvm
            os.makedirs(os.path.dirname(outp) or ".", exist_ok=True)
            with open(outp,"w",newline="") as f:
                w=csvm.writer(f); w.writerow(["algo","O0","O1","O2","O3"])
                for algo,row in table: w.writerow([algo]+[f"{x:.2f}" for x in row])
            print("saved speedup csv", outp); break
        except: pass
    # картинка таблички
    plt.figure(figsize=(8,4)); plt.axis('off')
    plt.table(cellText=[[f"{x:.2f}" for x in r] for _,r in table], rowLabels=[a for a,_ in table], colLabels=['O0','O1','O2','O3'], loc='center')
    plt.title('Speedup vs O0')
    plt.savefig(find_out("task3_speedup.png"), dpi=150, bbox_inches='tight'); print("saved speedup png")
