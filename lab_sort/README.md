# Лабораторная по сортировкам (0-6)

## Структура
```
lab_sort/
  Tasks/  - C++ код заданий (один файл на задание, задания 0-6)
  Data/   - csv с замерами (генерируются запуском)
  Graph/  - Python скрипты для графиков и png
```

## Запуски через Play в VS Code
Каждый файл запускается отдельно кнопкой Play:
- `Tasks/task0.cpp` → генерит `Data/task0.csv`
- `Tasks/task1.cpp` → демо `Data/task1.csv` с 5 колонками (для точных 5 сборок используй build.sh)
- `Tasks/task2.cpp` → `Data/task2.csv`
- `Tasks/task3.cpp` → демо `Data/task3.csv` + `Data/task3_0..3.csv`
- `Tasks/task4.cpp` → `Data/task4_cpp.csv`, затем `Graph/graph4.py` генерит `Data/task4_py.csv`
- `Tasks/task5.cpp` → `Data/task5_*.csv`
- `Tasks/task6.cpp` → `Data/task6.csv`
- `Graph/graphX.py` → читает `Data` и сохраняет `Graph/*.png`

Все пути в коде устойчивы к cwd (lab_sort, Tasks, Graph).

## Быстрый старт
```bash
bash lab_sort/build.sh
```
Собирает всё с флагами -O0..O3 и строит графики.

## Ручной запуск C++
```bash
g++ -std=c++17 -O2 lab_sort/Tasks/task0.cpp -o /tmp/task0 && /tmp/task0
python3 lab_sort/Graph/graph0.py
```
Для task1/task3 с флагами:
```bash
g++ -O0 -DOPT_LEVEL=0 lab_sort/Tasks/task1.cpp -o /tmp/task1_0 && /tmp/task1_0
g++ -O1 -DOPT_LEVEL=1 lab_sort/Tasks/task1.cpp -o /tmp/task1_1 && /tmp/task1_1
g++ -O2 -DOPT_LEVEL=2 lab_sort/Tasks/task1.cpp -o /tmp/task1_2 && /tmp/task1_2
g++ -O3 -DOPT_LEVEL=3 lab_sort/Tasks/task1.cpp -o /tmp/task1_3 && /tmp/task1_3
g++ lab_sort/Tasks/task1.cpp -o /tmp/task1_nf && /tmp/task1_nf
python3 lab_sort/Graph/graph1.py
```

## Методы сортировок
- O(N^2): bubble, insertion, selection
- O(N log N): heap, quick (Hoare), merge

## Графики
`lab_sort/Graph/`:
- task0.png, task0_loglog.png
- task1.png
- task2.png, task2_norm.png
- task3_O0..O3.png, task3_speedup.png
- task4_bubble/insertion/selection.png
- task5_*.png + task5_all_random.png
- task6.png, task6_loglog.png

## Защита
См. `lab_sort/защита.txt`
