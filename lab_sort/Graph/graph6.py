import csv, os, matplotlib.pyplot as plt
base="lab_sort/Data/task6.csv"
if not os.path.exists(base): base="../Data/task6.csv"
out="lab_sort/Graph/task6.png" if os.path.exists("lab_sort/Graph") else "task6.png"
N=[]; gen=[]; fwd=[]; back=[]; outp=[]
with open(base) as f:
    r=csv.DictReader(f)
    for row in r:
        N.append(int(row['N'])); gen.append(float(row['gen'])); fwd.append(float(row['forward'])); back.append(float(row['backward'])); outp.append(float(row['output']))

plt.figure()
plt.plot(N,gen,label='random generation',marker='o')
plt.plot(N,fwd,label='forward sum',marker='s')
plt.plot(N,back,label='backward sum',marker='^')
plt.plot(N,outp,label='output to file',marker='D')
plt.xlabel('N'); plt.ylabel('time, s'); plt.title('Task6: Royal battle - overheads'); plt.legend(); plt.grid(True)
plt.savefig(out, dpi=150)
try: plt.savefig("lab_sort/Graph/task6.png", dpi=150)
except: pass
print("saved task6")

# логлог
import math
plt.figure()
logN=[math.log10(x) for x in N]
for arr,label,marker in [(gen,'gen','o'),(fwd,'forward','s'),(back,'backward','^'),(outp,'output','D')]:
    logA=[math.log10(x) if x>0 else -6 for x in arr]
    plt.plot(logN,logA,label=label,marker=marker)
plt.xlabel('log10(N)'); plt.ylabel('log10(time)'); plt.title('Task6 log-log (slope 1 => O(N))'); plt.legend(); plt.grid(True)
plt.savefig(out.replace('task6.png','task6_loglog.png'), dpi=150)
try: plt.savefig("lab_sort/Graph/task6_loglog.png", dpi=150)
except: pass
print("saved loglog")
