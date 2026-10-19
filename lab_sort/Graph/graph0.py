import csv, os, pathlib, matplotlib.pyplot as plt, math
def find_data(name):
    for p in [f"lab_sort/Data/{name}", f"../Data/{name}", f"Data/{name}", name, f"../../lab_sort/Data/{name}"]:
        if os.path.exists(p): return p
    return f"lab_sort/Data/{name}"
def find_out(name):
    for d in ["lab_sort/Graph", "../Graph", "Graph", ".", "../lab_sort/Graph"]:
        if os.path.exists(d): return f"{d}/{name}"
    os.makedirs("lab_sort/Graph", exist_ok=True); return f"lab_sort/Graph/{name}"
data=find_data("task0.csv")
N=[]; bubble=[]; ins=[]; sel=[]
with open(data) as f:
    r=csv.DictReader(f)
    for row in r:
        N.append(int(row['N'])); bubble.append(float(row['bubble'])); ins.append(float(row['insertion'])); sel.append(float(row['selection']))
plt.figure()
plt.plot(N,bubble,label='bubble O(N^2)',marker='o')
plt.plot(N,ins,label='insertion O(N^2)',marker='s')
plt.plot(N,sel,label='selection O(N^2)',marker='^')
plt.xlabel('N'); plt.ylabel('time, s'); plt.title('Task0: Simple O(N^2) sorts'); plt.legend(); plt.grid(True)
plt.savefig(find_out("task0.png"), dpi=150); print("saved task0.png")
plt.close()
plt.figure()
logN=[math.log10(x) for x in N]
logB=[math.log10(x) if x>0 else 0 for x in bubble]
logI=[math.log10(x) if x>0 else 0 for x in ins]
logS=[math.log10(x) if x>0 else 0 for x in sel]
plt.plot(logN,logB,label='bubble',marker='o')
plt.plot(logN,logI,label='insertion',marker='s')
plt.plot(logN,logS,label='selection',marker='^')
plt.xlabel('log10(N)'); plt.ylabel('log10(time)'); plt.title('Task0: Log-Log (slope ~2 => O(N^2))'); plt.legend(); plt.grid(True)
plt.savefig(find_out("task0_loglog.png"), dpi=150); print("saved loglog")
