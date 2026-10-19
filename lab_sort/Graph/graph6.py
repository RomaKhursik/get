import csv, os, matplotlib.pyplot as plt, math
def find_data(name):
    for p in [f"lab_sort/Data/{name}", f"../Data/{name}", f"Data/{name}", name]:
        if os.path.exists(p): return p
    return f"lab_sort/Data/{name}"
def find_out(name):
    for d in ["lab_sort/Graph","../Graph","Graph","."]:
        if os.path.exists(d): return f"{d}/{name}"
    os.makedirs("lab_sort/Graph", exist_ok=True); return f"lab_sort/Graph/{name}"
data=find_data("task6.csv")
N=[]; gen=[]; fwd=[]; back=[]; outp=[]
with open(data) as f:
    r=csv.DictReader(f)
    for row in r: N.append(int(row['N'])); gen.append(float(row['gen'])); fwd.append(float(row['forward'])); back.append(float(row['backward'])); outp.append(float(row['output']))
plt.figure()
plt.plot(N,gen,label='random generation',marker='o')
plt.plot(N,fwd,label='forward sum',marker='s')
plt.plot(N,back,label='backward sum',marker='^')
plt.plot(N,outp,label='output to file',marker='D')
plt.xlabel('N'); plt.ylabel('time, s'); plt.title('Task6: Royal battle - overheads'); plt.legend(); plt.grid(True)
plt.savefig(find_out("task6.png"), dpi=150); print("saved task6"); plt.close()
plt.figure()
logN=[math.log10(x) for x in N]
for arr,label,marker in [(gen,'gen','o'),(fwd,'forward','s'),(back,'backward','^'),(outp,'output','D')]:
    logA=[math.log10(x) if x>0 else -6 for x in arr]
    plt.plot(logN,logA,label=label,marker=marker)
plt.xlabel('log10(N)'); plt.ylabel('log10(time)'); plt.title('Task6 log-log (slope 1 => O(N))'); plt.legend(); plt.grid(True)
plt.savefig(find_out("task6_loglog.png"), dpi=150); print("saved loglog")
