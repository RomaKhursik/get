import csv, os, matplotlib.pyplot as plt, time, random

base="lab_sort/Data/task7.csv"
if not os.path.exists(base): base="../Data/task7.csv"
out_prefix="lab_sort/Graph/" if os.path.exists("lab_sort/Graph") else ""

N=[]; d={'bubble':[],'insertion':[],'selection':[],'heap':[],'quick':[],'merge':[]}
with open(base) as f:
    r=csv.DictReader(f)
    for row in r:
        N.append(int(row['N']))
        for k in d: d[k].append(float(row[k]))

plt.figure()
for k,m in [('bubble','o'),('insertion','s'),('selection','^'),('heap','v'),('quick','D'),('merge','p')]:
    plt.plot(N,d[k],label=k,marker=m,markersize=3)
plt.xlabel('N (small 3-100)'); plt.ylabel('time per sort, s'); plt.title('Task7: Hulk vs Loki small N (O2)'); plt.legend(); plt.grid(True)
plt.savefig(out_prefix+"task7.png", dpi=150)
try: plt.savefig("lab_sort/Graph/task7.png", dpi=150)
except: pass
print("saved task7")
plt.close()

# теперь питон на малых N
def bubble(a):
    n=len(a)
    for i in range(n-1):
        for j in range(n-i-1):
            if a[j]>a[j+1]: a[j],a[j+1]=a[j+1],a[j]
def insertion(a):
    for i in range(1,len(a)):
        k=a[i]; j=i-1
        while j>=0 and a[j]>k: a[j+1]=a[j]; j-=1
        a[j+1]=k
def selection(a):
    n=len(a)
    for i in range(n-1):
        mn=i
        for j in range(i+1,n):
            if a[j]<a[mn]: mn=j
        a[i],a[mn]=a[mn],a[i]
def heap_sort(a):
    import heapq
    # используем встроенный heap не честно, сделаем ручной простой через sort? но для малых N покажем heap через heapq
    # сделаем быстрое heap через heapq
    heapq.heapify(a)
    for i in range(len(a)): a[i]=heapq.heappop(a)
    # но это криво, лучше просто использовать встроенный sort как приближение
def quick(a):
    if len(a)<=1: return a
    p=a[len(a)//2]
    l=[x for x in a if x<p]; m=[x for x in a if x==p]; r=[x for x in a if x>p]
    return quick(l)+m+quick(r)

sizes=list(range(3,101,5))
py_b=[]; py_i=[]; py_s=[]
for N_ in sizes:
    pool=[[random.randint(0,1000) for _ in range(N_)] for __ in range(20)]
    reps=1000
    import time as tm
    # bubble
    s=tm.perf_counter()
    for k in range(reps):
        a=pool[k%len(pool)].copy(); bubble(a)
    e=tm.perf_counter(); py_b.append((e-s)/reps)
    s=tm.perf_counter()
    for k in range(reps):
        a=pool[k%len(pool)].copy(); insertion(a)
    e=tm.perf_counter(); py_i.append((e-s)/reps)
    s=tm.perf_counter()
    for k in range(reps):
        a=pool[k%len(pool)].copy(); selection(a)
    e=tm.perf_counter(); py_s.append((e-s)/reps)

# сохраняем питон данные
with open("lab_sort/Data/task7_py.csv","w",newline="") as f:
    import csv
    w=csv.writer(f); w.writerow(["N","bubble","insertion","selection"])
    for n,b,i,s in zip(sizes,py_b,py_i,py_s): w.writerow([n,b,i,s])

plt.figure()
# C++ bubble small N
plt.plot(N,d['bubble'],label='C++ bubble',marker='o',markersize=3)
plt.plot(sizes,py_b,label='Python bubble',marker='s',markersize=3)
plt.xlabel('N'); plt.ylabel('time'); plt.title('Task7: C++ vs Python small N bubble'); plt.legend(); plt.grid(True)
plt.savefig(out_prefix+"task7_py_vs_cpp.png", dpi=150)
try: plt.savefig("lab_sort/Graph/task7_py_vs_cpp.png", dpi=150)
except: pass
print("saved py vs cpp")

# общий small N сравнение всех 6 vs python bubble
plt.figure()
for k,m in [('bubble','o'),('insertion','s'),('selection','^'),('heap','v'),('quick','D'),('merge','p')]:
    plt.plot(N,d[k],label='C++ '+k,marker=m,markersize=3)
plt.plot(sizes,py_b,label='Python bubble',marker='x',linestyle='--')
plt.xlabel('N'); plt.ylabel('time'); plt.title('Task7: All C++ vs Python'); plt.legend(fontsize='small'); plt.grid(True)
plt.savefig(out_prefix+"task7_all_vs_py.png", dpi=150)
try: plt.savefig("lab_sort/Graph/task7_all_vs_py.png", dpi=150)
except: pass
