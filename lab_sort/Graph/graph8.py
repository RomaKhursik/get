import csv, os, matplotlib.pyplot as plt
base="lab_sort/Data/task8.csv"
if not os.path.exists(base): base="../Data/task8.csv"
out="lab_sort/Graph/task8.png" if os.path.exists("lab_sort/Graph") else "task8.png"
N=[]; ch=[]; sh=[]; iv=[]; ll=[]; sm=[]; bg=[]
with open(base) as f:
    r=csv.DictReader(f)
    for row in r:
        N.append(int(row['N'])); ch.append(float(row['char'])); sh.append(float(row['short'])); iv.append(float(row['int'])); ll.append(float(row['long_long'])); sm.append(float(row['small'])); bg.append(float(row['big']))

plt.figure()
plt.plot(N,ch,label='char (1 byte)',marker='o')
plt.plot(N,sh,label='short (2)',marker='s')
plt.plot(N,iv,label='int (4)',marker='^')
plt.plot(N,ll,label='long long (8)',marker='D')
plt.plot(N,sm,label='struct Small',marker='v')
plt.plot(N,bg,label='struct Big (heavy)',marker='p')
plt.xlabel('N'); plt.ylabel('time, s (std::sort)'); plt.title('Task8: Sort different types'); plt.legend(); plt.grid(True)
plt.savefig(out, dpi=150)
try: plt.savefig("lab_sort/Graph/task8.png", dpi=150)
except: pass
print("saved task8")

# нормализуем к int
plt.figure()
for arr,label,marker in [(ch,'char','o'),(sh,'short','s'),(iv,'int','^'),(ll,'long long','D'),(sm,'small','v'),(bg,'big','p')]:
    ratio=[a/b if b!=0 else 0 for a,b in zip(arr,iv)]
    plt.plot(N,ratio,label=label,marker=marker)
plt.xlabel('N'); plt.ylabel('time / time(int)'); plt.title('Task8: Normalized to int'); plt.legend(); plt.grid(True)
plt.savefig(out.replace('task8.png','task8_norm.png'), dpi=150)
try: plt.savefig("lab_sort/Graph/task8_norm.png", dpi=150)
except: pass
print("saved norm")
