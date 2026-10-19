#include <iostream>
#include <fstream>
#include <chrono>
#include <random>
#include <string>
#include <filesystem>
using namespace std;
double get_time(){return chrono::duration_cast<chrono::microseconds>(chrono::steady_clock::now().time_since_epoch()).count()/1e6;}
int rand_uns(int min,int max){unsigned seed=chrono::steady_clock::now().time_since_epoch().count(); static default_random_engine e(seed); uniform_int_distribution<int> d(min,max); return d(e);}
void bubble_sort(int *a,int n){for(int i=0;i<n-1;i++) for(int j=0;j<n-i-1;j++) if(a[j]>a[j+1]) swap(a[j],a[j+1]);}
void insertion_sort(int *a,int n){for(int i=1;i<n;i++){int k=a[i],j=i-1; while(j>=0&&a[j]>k){a[j+1]=a[j]; j--;} a[j+1]=k;}}
void selection_sort(int *a,int n){for(int i=0;i<n-1;i++){int mn=i; for(int j=i+1;j<n;j++) if(a[j]<a[mn]) mn=j; swap(a[i],a[mn]);}}
string data_path(string name){
    string cand[5]={"lab_sort/Data/"+name,"../Data/"+name,"Data/"+name,name,"../lab_sort/Data/"+name};
    for(int i=0;i<5;i++) if(!filesystem::path(cand[i]).parent_path().empty()) filesystem::create_directories(filesystem::path(cand[i]).parent_path());
    for(int i=0;i<5;i++){ ofstream t(cand[i], ios::app); if(t){ t.close(); return cand[i]; } }
    return cand[0];
}
int main(){
    string out=data_path("task0.csv");
    ofstream f(out); f<<"N,bubble,insertion,selection\n";
    int sizes[]={500,1000,1500,2000,2500,3000,3500,4000,4500,5000};
    int sn=sizeof(sizes)/sizeof(sizes[0]);
    for(int si=0;si<sn;si++){int N=sizes[si];
        double t1=0,t2=0,t3=0; int reps=3;
        for(int r=0;r<reps;r++){
            int *a=new int[N]; int *b=new int[N]; int *c=new int[N];
            for(int i=0;i<N;i++){int v=rand_uns(0,100000); a[i]=v; b[i]=v; c[i]=v;}
            double s=get_time(); bubble_sort(a,N); double e=get_time(); t1+=(e-s); volatile long long sum=0; for(int i=0;i<N;i++) sum+=a[i];
            s=get_time(); insertion_sort(b,N); e=get_time(); t2+=(e-s); sum=0; for(int i=0;i<N;i++) sum+=b[i];
            s=get_time(); selection_sort(c,N); e=get_time(); t3+=(e-s); sum=0; for(int i=0;i<N;i++) sum+=c[i];
            delete[] a; delete[] b; delete[] c;
        }
        t1/=reps; t2/=reps; t3/=reps;
        f<<N<<","<<t1<<","<<t2<<","<<t3<<"\n"; cout<<N<<" "<<t1<<" "<<t2<<" "<<t3<<endl;
    }
    cout<<"saved to "<<out<<endl;
    return 0;
}
