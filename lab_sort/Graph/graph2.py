import csv, matplotlib.pyplot as plt, math, os
base="lab_sort/Data/task2.csv"
if not os.path.exists(base): base="../Data/task2.csv"
out="lab_sort/Graph/task2.png" if os.path.exists("lab_sort/Graph") else "task2.png"

N=[]; heap=[]; quick=[]; merge=[]
with open(base) as f:
    r=csv.DictReader(f)
    for row in r:
        N.append(int(row['N'])); heap.append(float(row['heap'])); quick.append(float(row['quick'])); merge.append(float(row['merge']))

plt.figure()
plt.plot(N,heap,label='heap O(N log N)',marker='o')
plt.plot(N,quick,label='quick O(N log N)',marker='s')
plt.plot(N,merge,label='merge O(N log N)',marker='^')
plt.xlabel('N'); plt.ylabel('time, s'); plt.title('Task2: Fast O(N log N) sorts'); plt.legend(); plt.grid(True)
plt.savefig(out, dpi=150)
try: plt.savefig("lab_sort/Graph/task2.png", dpi=150)
except: pass
print("saved task2")

# нормализованный график t / (N log N) должен быть константа
plt.figure()
for arr,label,marker in [(heap,'heap','o'),(quick,'quick','s'),(merge,'merge','^')]:
    norm=[t/(n*math.log2(n)) if n>1 else 0 for n,t in zip(N,arr)]
    plt.plot(N,norm,label=label,marker=marker)
plt.xlabel('N'); plt.ylabel('t / (N log N)'); plt.title('Task2: Normalized t/(N log N) ~ const => O(N log N)'); plt.legend(); plt.grid(True)
plt.savefig(out.replace('task2.png','task2_norm.png'), dpi=150)
try: plt.savefig("lab_sort/Graph/task2_norm.png", dpi=150)
except: pass
print("saved task2_norm")
