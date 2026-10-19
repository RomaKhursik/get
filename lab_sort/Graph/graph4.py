import csv, os, matplotlib.pyplot as plt, time, random, pathlib
def find_data(name):
    for p in [f"lab_sort/Data/{name}", f"../Data/{name}", f"Data/{name}", name]:
        if os.path.exists(p): return p
    return f"lab_sort/Data/{name}"
def find_out(name):
    for d in ["lab_sort/Graph","../Graph","Graph","."]:
        if os.path.exists(d): return f"{d}/{name}"
    os.makedirs("lab_sort/Graph", exist_ok=True); return f"lab_sort/Graph/{name}"
def find_data_out(name):
    for d in ["lab_sort/Data","../Data","Data","."]:
        if os.path.exists(d): return f"{d}/{name}"
    os.makedirs("lab_sort/Data", exist_ok=True); return f"lab_sort/Data/{name}"
def bubble(a): n=len(a); [ (a.__setitem__(j, a[j+1]) or a.__setitem__(j+1, a[j]) if False else None) for i in range(n-1) for j in range(n-i-1) if a[j]>a[j+1] ]  # placeholder
# правильные реализации
def bubble_sort(a):
    n=len(a)
    for i in range(n-1):
        for j in range(n-i-1):
            if a[j]>a[j+1]: a[j],a[j+1]=a[j+1],a[j]
def insertion_sort(a):
    for i in range(1,len(a)):
        k=a[i]; j=i-1
        while j>=0 and a[j]>k: a[j+1]=a[j]; j-=1
        a[j+1]=k
def selection_sort(a):
    n=len(a)
    for i in range(n-1):
        mn=i
        for j in range(i+1,n):
            if a[j]<a[mn]: mn=j
        a[i],a[mn]=a[mn],a[i]
sizes=[100,300,500,800,1000,1500,2000]
py_b=[]; py_i=[]; py_s=[]
for N in sizes:
    reps=3
    if N>1000: reps=2
    t1=t2=t3=0
    for _ in range(reps):
        base=[random.randint(0,100000) for _ in range(N)]
        a=base.copy(); s=time.perf_counter(); bubble_sort(a); e=time.perf_counter(); t1+=e-s
        a=base.copy(); s=time.perf_counter(); insertion_sort(a); e=time.perf_counter(); t2+=e-s
        a=base.copy(); s=time.perf_counter(); selection_sort(a); e=time.perf_counter(); t3+=e-s
    py_b.append(t1/reps); py_i.append(t2/reps); py_s.append(t3/reps)
    print(N, t1/reps, t2/reps, t3/reps)
out_data=find_data_out("task4_py.csv")
os.makedirs(os.path.dirname(out_data) or ".", exist_ok=True)
with open(out_data,"w",newline="") as f:
    import csv
    w=csv.writer(f); w.writerow(["N","bubble","insertion","selection"])
    for n,b,i,s in zip(sizes,py_b,py_i,py_s): w.writerow([n,b,i,s])
print("saved", out_data)
cpp_path=find_data("task4_cpp.csv")
cpp_N=[]; cpp_b=[]; cpp_i=[]; cpp_s=[]
if os.path.exists(cpp_path):
    with open(cpp_path) as f:
        r=csv.DictReader(f)
        for row in r: cpp_N.append(int(row['N'])); cpp_b.append(float(row['bubble'])); cpp_i.append(float(row['insertion'])); cpp_s.append(float(row['selection']))
else:
    print("no cpp data, run Tasks/task4.cpp first"); cpp_N=sizes; cpp_b=[0]*len(sizes); cpp_i=[0]*len(sizes); cpp_s=[0]*len(sizes)
for name,py_arr,cpp_arr in [('bubble',py_b,cpp_b),('insertion',py_i,cpp_i),('selection',py_s,cpp_s)]:
    plt.figure()
    plt.plot(sizes,py_arr,label='Python',marker='o')
    plt.plot(cpp_N,cpp_arr,label='C++',marker='s')
    plt.xlabel('N'); plt.ylabel('time, s'); plt.title(f'Task4: C++ vs Python - {name}'); plt.legend(); plt.grid(True)
    plt.savefig(find_out(f"task4_{name}.png"), dpi=150); plt.close(); print(f"saved {name}")
