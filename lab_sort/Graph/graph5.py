import csv, os, matplotlib.pyplot as plt
def find_data(name):
    for p in [f"lab_sort/Data/{name}", f"../Data/{name}", f"Data/{name}", name]:
        if os.path.exists(p): return p
    return f"lab_sort/Data/{name}"
def find_out(name):
    for d in ["lab_sort/Graph","../Graph","Graph","."]:
        if os.path.exists(d): return f"{d}/{name}"
    os.makedirs("lab_sort/Graph", exist_ok=True); return f"lab_sort/Graph/{name}"
algos=['bubble','insertion','selection','heap','quick','merge']
for algo in algos:
    p=find_data(f"task5_{algo}.csv")
    if not os.path.exists(p): print("missing",p); continue
    N=[]; sorted_t=[]; rnd=[]; rev=[]
    with open(p) as f:
        r=csv.DictReader(f)
        for row in r: N.append(int(row['N'])); sorted_t.append(float(row['sorted'])); rnd.append(float(row['random'])); rev.append(float(row['reversed']))
    plt.figure()
    plt.plot(N,sorted_t,label='sorted (best)',marker='o')
    plt.plot(N,rnd,label='random (avg)',marker='s')
    plt.plot(N,rev,label='reversed (worst)',marker='^')
    plt.xlabel('N'); plt.ylabel('time, s'); plt.title(f'Task5: {algo} - dependence on input'); plt.legend(); plt.grid(True)
    plt.savefig(find_out(f"task5_{algo}.png"), dpi=150); plt.close(); print(f"saved {algo}")
plt.figure()
for algo in algos:
    p=find_data(f"task5_{algo}.csv")
    if not os.path.exists(p): continue
    N=[]; rnd=[]
    with open(p) as f:
        r=csv.DictReader(f)
        for row in r: N.append(int(row['N'])); rnd.append(float(row['random']))
    plt.plot(N,rnd,label=algo,marker='o')
plt.xlabel('N'); plt.ylabel('time, s'); plt.title('Task5: All algos random case'); plt.legend(); plt.grid(True)
plt.savefig(find_out("task5_all_random.png"), dpi=150); print("saved all_random")
