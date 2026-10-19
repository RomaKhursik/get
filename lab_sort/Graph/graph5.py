import csv, os, matplotlib.pyplot as plt
base="lab_sort/Data/task5"
if not os.path.exists(base+"_bubble.csv") and os.path.exists("../Data/task5_bubble.csv"):
    base="../Data/task5"
    out="lab_sort/Graph/" if os.path.exists("lab_sort/Graph") else ""
else:
    base="lab_sort/Data/task5"
    out="lab_sort/Graph/"

algos=['bubble','insertion','selection','heap','quick','merge']
# каждый файл имеет N,sorted,random,reversed
for algo in algos:
    p=f"{base}_{algo}.csv"
    if not os.path.exists(p):
        # пробуем без lab_sort
        p=p.replace("lab_sort/","")
        if not os.path.exists(p): 
            print("missing",p); continue
    N=[]; sorted_t=[]; rnd=[]; rev=[]
    with open(p) as f:
        r=csv.DictReader(f)
        for row in r:
            N.append(int(row['N'])); sorted_t.append(float(row['sorted'])); rnd.append(float(row['random'])); rev.append(float(row['reversed']))
    plt.figure()
    plt.plot(N,sorted_t,label='sorted (best)',marker='o')
    plt.plot(N,rnd,label='random (avg)',marker='s')
    plt.plot(N,rev,label='reversed (worst)',marker='^')
    plt.xlabel('N'); plt.ylabel('time, s'); plt.title(f'Task5: {algo} - dependence on input'); plt.legend(); plt.grid(True)
    plt.savefig(f"{out}task5_{algo}.png", dpi=150)
    try: plt.savefig(f"lab_sort/Graph/task5_{algo}.png", dpi=150)
    except: pass
    plt.close()
    print(f"saved {algo}")

# дополнительный общий график для random случая всех алгоритмов
plt.figure()
for algo in algos:
    p=f"{base}_{algo}.csv"
    if not os.path.exists(p):
        p=p.replace("lab_sort/","")
        if not os.path.exists(p): continue
    N=[]; rnd=[]
    with open(p) as f:
        r=csv.DictReader(f)
        for row in r:
            N.append(int(row['N'])); rnd.append(float(row['random']))
    plt.plot(N,rnd,label=algo,marker='o')
plt.xlabel('N'); plt.ylabel('time, s'); plt.title('Task5: All algos random case'); plt.legend(); plt.grid(True)
plt.savefig(f"{out}task5_all_random.png", dpi=150)
try: plt.savefig("lab_sort/Graph/task5_all_random.png", dpi=150)
except: pass
print("saved all_random")
