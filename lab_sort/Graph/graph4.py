import csv, os, matplotlib.pyplot as plt, time, random

# этот скрипт делает:
# 1. читает C++ данные task4_cpp.csv
# 2. сам меряет питон сортировки и сохраняет их в Data/task4_py.csv
# 3. строит 3 графика сравнения

def bubble(a):
    n=len(a)
    for i in range(n-1):
        for j in range(n-i-1):
            if a[j]>a[j+1]: a[j],a[j+1]=a[j+1],a[j]
def insertion(a):
    for i in range(1,len(a)):
        k=a[i]; j=i-1
        while j>=0 and a[j]>k:
            a[j+1]=a[j]; j-=1
        a[j+1]=k
def selection(a):
    n=len(a)
    for i in range(n-1):
        mn=i
        for j in range(i+1,n):
            if a[j]<a[mn]: mn=j
        a[i],a[mn]=a[mn],a[i]

sizes=[100,300,500,800,1000,1500,2000]
# меряем питон
py_b=[]; py_i=[]; py_s=[]
for N in sizes:
    reps=3
    if N>1000: reps=2
    t1=t2=t3=0
    for _ in range(reps):
        base=[random.randint(0,100000) for _ in range(N)]
        a=base.copy(); s=time.perf_counter(); bubble(a); e=time.perf_counter(); t1+=e-s
        a=base.copy(); s=time.perf_counter(); insertion(a); e=time.perf_counter(); t2+=e-s
        a=base.copy(); s=time.perf_counter(); selection(a); e=time.perf_counter(); t3+=e-s
    py_b.append(t1/reps); py_i.append(t2/reps); py_s.append(t3/reps)
    print(N, t1/reps, t2/reps, t3/reps)

# сохраняем
import os as os2
out_data="lab_sort/Data/task4_py.csv"
if not os2.path.exists("lab_sort/Data"): out_data="../Data/task4_py.csv"
os2.makedirs(os2.path.dirname(out_data) if os2.path.dirname(out_data) else ".", exist_ok=True)
with open(out_data,"w",newline="") as f:
    import csv
    w=csv.writer(f); w.writerow(["N","bubble","insertion","selection"])
    for n,b,i,s in zip(sizes,py_b,py_i,py_s): w.writerow([n,b,i,s])

# читаем C++ данные
cpp_path="lab_sort/Data/task4_cpp.csv"
if not os.path.exists(cpp_path): cpp_path="../Data/task4_cpp.csv"
cpp_N=[]; cpp_b=[]; cpp_i=[]; cpp_s=[]
if os.path.exists(cpp_path):
    with open(cpp_path) as f:
        r=csv.DictReader(f)
        for row in r:
            cpp_N.append(int(row['N'])); cpp_b.append(float(row['bubble'])); cpp_i.append(float(row['insertion'])); cpp_s.append(float(row['selection']))
else:
    print("no cpp data")
    cpp_N=sizes; cpp_b=[0]*len(sizes); cpp_i=[0]*len(sizes); cpp_s=[0]*len(sizes)

# 3 графика по каждой сортировке
out_prefix="lab_sort/Graph/"
if not os.path.exists(out_prefix): out_prefix=""
for name,py_arr,cpp_arr in [('bubble',py_b,cpp_b),('insertion',py_i,cpp_i),('selection',py_s,cpp_s)]:
    plt.figure()
    plt.plot(sizes,py_arr,label='Python',marker='o')
    # cpp_N может совпадать с sizes, но выровняем по sizes
    if cpp_N==sizes:
        plt.plot(cpp_N,cpp_arr,label='C++',marker='s')
    else:
        # интерполяция: просто построим оба если размеры совпали
        plt.plot(cpp_N,cpp_arr,label='C++',marker='s')
        plt.plot(sizes,py_arr,label='Python',marker='o')
    plt.xlabel('N'); plt.ylabel('time, s'); plt.title(f'Task4: C++ vs Python - {name}'); plt.legend(); plt.grid(True)
    plt.savefig(f"{out_prefix}task4_{name}.png", dpi=150)
    try: plt.savefig(f"lab_sort/Graph/task4_{name}.png", dpi=150)
    except: pass
    plt.close()
    print(f"saved {name}")

# общий график скорости ratio
# посчитаем среднее ускорение Python/C++
ratios=[]
for b,i in zip(py_b,cpp_b):
    if i!=0: ratios.append(b/i)
if ratios:
    print("avg speedup bubble python vs cpp", sum(ratios)/len(ratios))
