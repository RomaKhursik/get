#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <random>
#include <algorithm>
using namespace std;
double get_time(){return chrono::duration_cast<chrono::microseconds>(chrono::steady_clock::now().time_since_epoch()).count()/1e6;}
int rand_uns(int min,int max){unsigned seed=chrono::steady_clock::now().time_since_epoch().count(); static default_random_engine e(seed); uniform_int_distribution<int> d(min,max); return d(e);}

struct Small { int a; int b; bool operator<(Small const& o) const { return a<o.a; } };
struct Big { int a[16]; int key; bool operator<(Big const& o) const { return key<o.key; } };

template<typename T>
double measure_sort(int N, vector<T> base){
    int reps=3;
    double t=0;
    for(int r=0;r<reps;r++){
        vector<T> a=base;
        for(int i=0;i<N;i++) {}
        // заново генерим случайные данные внутри, но нам нужен base
        // base уже случайный, поэтому просто сортируем
        double s=get_time();
        sort(a.begin(), a.end());
        double e=get_time(); t+=(e-s);
        volatile long long sum=0;
        // чтобы компилятор не вырезал, используем значение
        // для разных типов по разному
        // просто возьмем хак
        (void)sum;
    }
    return t/reps;
}

int main(){
    ofstream f("lab_sort/Data/task8.csv", ios::out);
    f<<"N,char,short,int,long_long,small,big\n";
    vector<int> sizes={1000,5000,10000,20000,50000,100000};
    for(int N:sizes){
        // генерим базы для каждого типа один раз
        vector<char> base_char(N); for(int i=0;i<N;i++) base_char[i]=(char)rand_uns(0,127);
        vector<short> base_short(N); for(int i=0;i<N;i++) base_short[i]=(short)rand_uns(0,30000);
        vector<int> base_int(N); for(int i=0;i<N;i++) base_int[i]=rand_uns(0,1000000);
        vector<long long> base_ll(N); for(int i=0;i<N;i++) base_ll[i]=rand_uns(0,1000000);
        vector<Small> base_small(N); for(int i=0;i<N;i++){ base_small[i].a=rand_uns(0,1000000); base_small[i].b=rand_uns(0,1000); }
        vector<Big> base_big(N); for(int i=0;i<N;i++){ for(int k=0;k<16;k++) base_big[i].a[k]=rand_uns(0,1000); base_big[i].key=rand_uns(0,1000000); }

        double t_char=0,t_short=0,t_int=0,t_ll=0,t_small=0,t_big=0;
        int reps=5;
        if(N>=50000) reps=3;
        for(int r=0;r<reps;r++){
            {
                vector<char> a=base_char; for(int i=0;i<N;i++) a[i]=(char)rand_uns(0,127);
                double s=get_time(); sort(a.begin(),a.end()); double e=get_time(); t_char+=(e-s); volatile char x=a[0]; (void)x;
            }
            {
                vector<short> a=base_short; for(int i=0;i<N;i++) a[i]=(short)rand_uns(0,30000);
                double s=get_time(); sort(a.begin(),a.end()); double e=get_time(); t_short+=(e-s); volatile short x=a[0]; (void)x;
            }
            {
                vector<int> a=base_int; for(int i=0;i<N;i++) a[i]=rand_uns(0,1000000);
                double s=get_time(); sort(a.begin(),a.end()); double e=get_time(); t_int+=(e-s); volatile int x=a[0]; (void)x;
            }
            {
                vector<long long> a=base_ll; for(int i=0;i<N;i++) a[i]=rand_uns(0,1000000);
                double s=get_time(); sort(a.begin(),a.end()); double e=get_time(); t_ll+=(e-s); volatile long long x=a[0]; (void)x;
            }
            {
                vector<Small> a=base_small; for(int i=0;i<N;i++){ a[i].a=rand_uns(0,1000000); a[i].b=rand_uns(0,1000); }
                double s=get_time(); sort(a.begin(),a.end()); double e=get_time(); t_small+=(e-s); volatile int x=a[0].a; (void)x;
            }
            {
                vector<Big> a=base_big; for(int i=0;i<N;i++){ for(int k=0;k<16;k++) a[k].a[k]=rand_uns(0,1000); a[i].key=rand_uns(0,1000000); }
                double s=get_time(); sort(a.begin(),a.end()); double e=get_time(); t_big+=(e-s); volatile int x=a[0].key; (void)x;
            }
        }
        t_char/=reps; t_short/=reps; t_int/=reps; t_ll/=reps; t_small/=reps; t_big/=reps;
        f<<N<<","<<t_char<<","<<t_short<<","<<t_int<<","<<t_ll<<","<<t_small<<","<<t_big<<"\n";
        cout<<N<<" "<<t_char<<" "<<t_short<<" "<<t_int<<" "<<t_ll<<" "<<t_small<<" "<<t_big<<endl;
    }
    return 0;
}
