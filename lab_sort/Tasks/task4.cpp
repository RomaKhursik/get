#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <random>
#include <string>
#include <filesystem>
using namespace std;
double get_time(){return chrono::duration_cast<chrono::microseconds>(chrono::steady_clock::now().time_since_epoch()).count()/1e6;}
int rand_uns(int min,int max){unsigned seed=chrono::steady_clock::now().time_since_epoch().count(); static default_random_engine e(seed); uniform_int_distribution<int> d(min,max); return d(e);}
void bubble_sort(vector<int> &a){int n=a.size(); for(int i=0;i<n-1;i++) for(int j=0;j<n-i-1;j++) if(a[j]>a[j+1]) swap(a[j],a[j+1]);}
void insertion_sort(vector<int> &a){int n=a.size(); for(int i=1;i<n;i++){int k=a[i],j=i-1; while(j>=0&&a[j]>k){a[j+1]=a[j]; j--;} a[j+1]=k;}}
void selection_sort(vector<int> &a){int n=a.size(); for(int i=0;i<n-1;i++){int mn=i; for(int j=i+1;j<n;j++) if(a[j]<a[mn]) mn=j; swap(a[i],a[mn]);}}
string data_path(string name){
    vector<string> cand={"lab_sort/Data/"+name,"../Data/"+name,"Data/"+name,name,"../lab_sort/Data/"+name};
    for(auto &p:cand) if(!filesystem::path(p).parent_path().empty()) filesystem::create_directories(filesystem::path(p).parent_path());
    for(auto &p:cand){ ofstream t(p, ios::app); if(t){ t.close(); return p; } }
    return cand[0];
}
int main(){
    string out=data_path("task4_cpp.csv");
    ofstream f(out); f<<"N,bubble,insertion,selection\n";
    vector<int> sizes={100,300,500,800,1000,1500,2000};
    for(int N:sizes){
        double t1=0,t2=0,t3=0; int reps=5;
        for(int r=0;r<reps;r++){
            vector<int> a(N); for(int i=0;i<N;i++) a[i]=rand_uns(0,100000);
            vector<int> b=a,c=a;
            double s=get_time(); bubble_sort(a); double e=get_time(); t1+=(e-s); volatile long long sum=0; for(int x:a) sum+=x;
            s=get_time(); insertion_sort(b); e=get_time(); t2+=(e-s); sum=0; for(int x:b) sum+=x;
            s=get_time(); selection_sort(c); e=get_time(); t3+=(e-s); sum=0; for(int x:c) sum+=x;
        }
        t1/=reps; t2/=reps; t3/=reps;
        f<<N<<","<<t1<<","<<t2<<","<<t3<<"\n"; cout<<N<<" "<<t1<<" "<<t2<<" "<<t3<<endl;
    }
    cout<<"saved to "<<out<<endl;
    return 0;
}
