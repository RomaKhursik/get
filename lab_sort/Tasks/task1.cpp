#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <random>
using namespace std;
double get_time() {
    return chrono::duration_cast<chrono::microseconds>(chrono::steady_clock::now().time_since_epoch()).count()/1e6;
}
int rand_uns(int min,int max){
    unsigned seed=chrono::steady_clock::now().time_since_epoch().count();
    static default_random_engine e(seed);
    uniform_int_distribution<int> d(min,max);
    return d(e);
}
void bubble_sort(vector<int> &a){
    int n=a.size();
    for(int i=0;i<n-1;i++) for(int j=0;j<n-i-1;j++) if(a[j]>a[j+1]) swap(a[j],a[j+1]);
}
int main(){
    string opt="UNKNOWN";
#ifdef OPT_LEVEL
    opt=to_string(OPT_LEVEL);
#endif
    // файл будет перезаписываться при каждом запуске с разным флагом - мы пишем во временный файл
    // основной скрипт объединит их в task1.csv
    // если запуск без скрипта - просто создаем task1_single.csv
    string fname="lab_sort/Data/task1_"+opt+".csv";
    if(opt=="UNKNOWN") fname="lab_sort/Data/task1.csv";
    ofstream f(fname, ios::out);
    f<<"N,time\n";
    vector<int> sizes={500,1000,1500,2000,2500,3000,3500,4000,4500,5000};
    for(int N:sizes){
        double tt=0;
        int reps=3;
        for(int r=0;r<reps;r++){
            vector<int> a(N);
            for(int i=0;i<N;i++) a[i]=rand_uns(0,100000);
            double s=get_time(); bubble_sort(a); double e=get_time(); tt+=(e-s);
            volatile long long sum=0; for(int x:a) sum+=x; if(sum==123456789) cout<<"";
        }
        tt/=reps;
        f<<N<<","<<tt<<"\n";
        cout<<opt<<" "<<N<<" "<<tt<<endl;
    }
    return 0;
}
