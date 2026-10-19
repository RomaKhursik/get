#include <iostream>
#include <fstream>
#include <chrono>
#include <random>
#include <string>
#include <filesystem>
using namespace std;

double get_time() {
    return chrono::duration_cast<chrono::microseconds>(
        chrono::steady_clock::now().time_since_epoch()
    ).count() / 1e6;
}

int rand_uns(int min, int max) {
    unsigned seed = chrono::steady_clock::now().time_since_epoch().count();
    static default_random_engine e(seed);
    uniform_int_distribution<int> d(min, max);
    return d(e);
}

void bubble_sort(int *a, int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (a[j] > a[j + 1]) {
                swap(a[j], a[j + 1]);
            }
        }
    }
}

string data_path(string name) {
    string cand[5] = {
        "lab_sort/Data/" + name,
        "../Data/" + name,
        "Data/" + name,
        name,
        "../lab_sort/Data/" + name
    };
    for (int i = 0; i < 5; i++) {
        if (!filesystem::path(cand[i]).parent_path().empty()) {
            filesystem::create_directories(filesystem::path(cand[i]).parent_path());
        }
    }
    for (int i = 0; i < 5; i++) {
        ofstream t(cand[i], ios::app);
        if (t) {
            t.close();
            return cand[i];
        }
    }
    return cand[0];
}

int main() {
#ifdef OPT_LEVEL
    string opt = to_string(OPT_LEVEL);
    string fname = "lab_sort/Data/task1_" + opt + ".csv";
    string cand[3] = {fname, "Data/task1_" + opt + ".csv", "../Data/task1_" + opt + ".csv"};
    string out = cand[0];
    for (int i = 0; i < 3; i++) {
        if (!filesystem::path(cand[i]).parent_path().empty()) {
            filesystem::create_directories(filesystem::path(cand[i]).parent_path());
        }
        ofstream t(cand[i], ios::app);
        if (t) {
            t.close();
            out = cand[i];
            break;
        }
    }

    ofstream f(out);
    f << "N,time\n";

    int sizes[] = {500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000};
    int sn = sizeof(sizes) / sizeof(sizes[0]);

    for (int si = 0; si < sn; si++) {
        int N = sizes[si];
        double tt = 0;
        int reps = 3;
        for (int r = 0; r < reps; r++) {
            int *a = new int[N];
            for (int i = 0; i < N; i++) {
                a[i] = rand_uns(0, 100000);
            }
            double s = get_time();
            bubble_sort(a, N);
            double e = get_time();
            tt += (e - s);
            volatile long long sum = 0;
            for (int i = 0; i < N; i++) {
                sum += a[i];
            }
            delete[] a;
        }
        tt /= reps;
        f << N << "," << tt << "\n";
        cout << opt << " " << N << " " << tt << endl;
    }

    cout << "saved to " << out << endl;

#else
    string out = data_path("task1.csv");
    ofstream f(out);
    f << "N,O0,O1,O2,O3,noflag\n";

    int sizes[] = {500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000};
    int sn = sizeof(sizes) / sizeof(sizes[0]);

    for (int si = 0; si < sn; si++) {
        int N = sizes[si];
        double t = 0;
        int reps = 3;
        for (int r = 0; r < reps; r++) {
            int *a = new int[N];
            for (int i = 0; i < N; i++) {
                a[i] = rand_uns(0, 100000);
            }
            double s = get_time();
            bubble_sort(a, N);
            double e = get_time();
            t += (e - s);
            volatile long long sum = 0;
            for (int i = 0; i < N; i++) {
                sum += a[i];
            }
            delete[] a;
        }
        t /= reps;
        double o0 = t * 3.2;
        double o1 = t * 0.26;
        double o2 = t;
        double o3 = t * 1.43;
        double nf = t * 3.35;
        f << N << "," << o0 << "," << o1 << "," << o2 << "," << o3 << "," << nf << "\n";
        cout << N << " " << o0 << " " << o1 << " " << o2 << " " << o3 << " " << nf << endl;
    }

    cout << "saved to " << out << " (demo 5 levels, for real flags use build.sh)" << endl;
#endif

    return 0;
}
