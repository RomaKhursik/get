import csv, matplotlib.pyplot as plt, math, os
path_data="lab_sort/Data/task0.csv"
# если запуск из Graph папки - поправить путь
if not os.path.exists(path_data):
    path_data="../Data/task0.csv"
    out_prefix=""
else:
    out_prefix="lab_sort/Graph/"
    path_data="lab_sort/Data/task0.csv"
    if not os.path.exists(path_data):
        path_data="Data/task0.csv"
        out_prefix="Graph/"

# читаем
N=[]; bubble=[]; insertion=[]; selection=[]
try:
    with open(path_data) as f:
        r=csv.DictReader(f)
        for row in r:
            N.append(int(row['N'])); bubble.append(float(row['bubble'])); insertion.append(float(row['insertion'])); selection.append(float(row['selection']))
except: 
    print("no data", path_data)
    exit()

plt.figure()
plt.plot(N,bubble,label='bubble O(N^2)',marker='o')
plt.plot(N,insertion,label='insertion O(N^2)',marker='s')
plt.plot(N,selection,label='selection O(N^2)',marker='^')
plt.xlabel('N'); plt.ylabel('time, s'); plt.title('Task0: Simple O(N^2) sorts'); plt.legend(); plt.grid(True)
plt.savefig(out_prefix+'task0.png' if out_prefix else 'task0.png', dpi=150)
plt.savefig('lab_sort/Graph/task0.png', dpi=150) if out_prefix else None
print("saved task0.png")
plt.close()

# log log
plt.figure()
logN=[math.log10(x) for x in N]
logB=[math.log10(x) if x>0 else 0 for x in bubble]
logI=[math.log10(x) if x>0 else 0 for x in insertion]
logS=[math.log10(x) if x>0 else 0 for x in selection]
plt.plot(logN,logB,label='bubble',marker='o')
plt.plot(logN,logI,label='insertion',marker='s')
plt.plot(logN,logS,label='selection',marker='^')
# теоретическая прямая с наклоном 2: log(t)=2*logN + C, покажем пример
plt.xlabel('log10(N)'); plt.ylabel('log10(time)'); plt.title('Task0: Log-Log (slope ~2 => O(N^2))'); plt.legend(); plt.grid(True)
plt.savefig(out_prefix+'task0_loglog.png' if out_prefix else 'task0_loglog.png', dpi=150)
try: plt.savefig('lab_sort/Graph/task0_loglog.png', dpi=150)
except: pass
print("saved task0_loglog.png")
