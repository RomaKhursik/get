import csv, os, matplotlib.pyplot as plt, math
def find_data(name):
    for p in [f"lab_sort/Data/{name}", f"../Data/{name}", f"Data/{name}", name]:
        if os.path.exists(p): return p
    return f"lab_sort/Data/{name}"
def find_out(name):
    for d in ["lab_sort/Graph","../Graph","Graph","."]:
        if os.path.exists(d): return f"{d}/{name}"
    os.makedirs("lab_sort/Graph", exist_ok=True); return f"lab_sort/Graph/{name}"
data=find_data("task2.csv")
N=[]; heap=[]; quick=[]; merge=[]
with open(data) as f:
    r=csv.DictReader(f)
    for row in r: N.append(int(row['N'])); heap.append(float(row['heap'])); quick.append(float(row['quick'])); merge.append(float(row['merge']))
plt.figure()
plt.plot(N,heap,label='heap O(N log N)',marker='o')
plt.plot(N,quick,label='quick O(N log N)',marker='s')
plt.plot(N,merge,label='merge O(N log N)',marker='^')
plt.xlabel('N'); plt.ylabel('time, s'); plt.title('Task2: Fast O(N log N) sorts'); plt.legend(); plt.grid(True)
plt.savefig(find_out("task2.png"), dpi=150); print("saved task2")
plt.close()
plt.figure()
for arr,label,marker in [(heap,'heap','o'),(quick,'quick','s'),(merge,'merge','^')]:
    norm=[t/(n*math.log2(n)) if n>1 else 0 for n,t in zip(N,arr)]
    plt.plot(N,norm,label=label,marker=marker)
plt.xlabel('N'); plt.ylabel('t / (N log N)'); plt.title('Task2: Normalized t/(N log N) ~ const => O(N log N)'); plt.legend(); plt.grid(True)
plt.savefig(find_out("task2_norm.png"), dpi=150); print("saved norm")
