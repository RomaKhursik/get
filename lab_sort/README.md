# Лабораторная по сортировкам

## Структура
```
lab_sort/
  Tasks/  - C++ код заданий (один файл на задание)
  Data/   - csv с замерами (генерируются запуском)
  Graph/  - Python скрипты для графиков и png
```

## Быстрый старт
```bash
bash lab_sort/build.sh
```
Скрипт скомпилирует все задачи с нужными флагами, запустит замеры и построит графики.

## Ручной запуск
```bash
# Пример task0
g++ -O2 lab_sort/Tasks/task0.cpp -o /tmp/task0 && /tmp/task0
python3 lab_sort/Graph/graph0.py

# task1 с оптимизациями
g++ -O0 -DOPT_LEVEL=0 lab_sort/Tasks/task1.cpp -o /tmp/task1_0 && /tmp/task1_0
g++ -O1 -DOPT_LEVEL=1 lab_sort/Tasks/task1.cpp -o /tmp/task1_1 && /tmp/task1_1
g++ -O2 -DOPT_LEVEL=2 lab_sort/Tasks/task1.cpp -o /tmp/task1_2 && /tmp/task1_2
g++ -O3 -DOPT_LEVEL=3 lab_sort/Tasks/task1.cpp -o /tmp/task1_3 && /tmp/task1_3
g++ lab_sort/Tasks/task1.cpp -o /tmp/task1_nf && /tmp/task1_nf
python3 lab_sort/Graph/graph1.py

# task3 аналогично
# task4: C++ часть + Python часть внутри graph4.py
g++ -O2 lab_sort/Tasks/task4.cpp -o /tmp/task4 && /tmp/task4
python3 lab_sort/Graph/graph4.py
```

## Используемые методы сортировок
- O(N^2): bubble, insertion, selection
- O(N log N): heap, quick (Hoare), merge

## Графики
Все png в `lab_sort/Graph/`:
- task0.png, task0_loglog.png
- task1.png
- task2.png, task2_norm.png
- task3_O0..O3.png, task3_speedup.png
- task4_bubble/insertion/selection.png
- task5_*.png
- task6.png, task6_loglog.png
- task7.png, task7_py_vs_cpp.png
- task8.png, task8_norm.png

## Защита
См. `lab_sort/защита.txt` - краткое описание каждого задания простым языком.
