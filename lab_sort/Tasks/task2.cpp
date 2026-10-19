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
void merge_rec(vector<int> &a,int l,int r, vector<int> &tmp){ if(r-l<=1) return; int m=(l+r)/2; merge_rec(a,l,m,tmp); merge_rec(a,m,r,tmp); int i=l,j=m,k=l; while(i<m&&j<r) tmp[k++]=a[i]<a[j]?a[i++]:a[j++]; while(i<m) tmp[k++]=a[i++]; while(j<r) tmp[k++]=a[j++]; for(int k=l;k<r;k++) a[k]=tmp[k]; }
void merge_sort(vector<int> &a){ vector<int> tmp(a.size()); merge_rec(a,0,a.size(),tmp); }
void heapify(vector<int> &a,int n,int i){int l=2*i+1,r=2*i+2,m=i; if(l<n&&a[l]>a[m]) m=l; if(r<n&&a[r]>a[m]) m=r; if(m!=i){swap(a[i],a[m]); heapify(a,n,m);} }
void heap_sort(vector<int> &a){int n=a.size(); for(int i=n/2-1;i>=0;i--) heapify(a,n,i); for(int i=n-1;i>0;i--){swap(a[0],a[i]); heapify(a,i,0);} }
void quick_rec(vector<int> &a,int l,int r){if(l>=r) return; int i=l,j=r,p=a[(l+r)/2]; while(i<=j){while(a[i]<p) i++; while(a[j]>p) j--; if(i<=j) swap(a[i++],a[j--]);} if(l<j) quick_rec(a,l,j); if(i<r) quick_rec(a,i,r);}
void quick_sort(vector<int> &a){quick_rec(a,0,(int)a.size()-1);}
string data_path(string name){
    vector<string> cand={"lab_sort/Data/"+name,"../Data/"+name,"Data/"+name,name,"../lab_sort/Data/"+name};
    for(auto &p:cand) if(!filesystem::path(p).parent_path().empty()) filesystem::create_directories(filesystem::path(p).parent_path());
    for(auto &p:cand){ ofstream t(p, ios::app); if(t){ t.close(); return p; } }
    return cand[0];
}
int main(){
    string out=data_path("task2.csv");
    ofstream f(out); f<<"N,heap,quick,merge\n";
    vector<int> sizes={1000,5000,10000,20000,50000,100000,200000};
    for(int N:sizes){
        double t1=0,t2=0,t3=0; int reps=5; if(N>50000) reps=3;
        for(int r=0;r<reps;r++){
            vector<int> a(N); for(int i=0;i<N;i++) a[i]=rand_uns(0,1000000);
            vector<int> b=a,c=a;
            double s=get_time(); heap_sort(b); double e=get_time(); t1+=(e-s); volatile long long sum=0; for(int x:b) sum+=x;
            s=get_time(); quick_sort(c); e=get_time(); t2+=(e-s); sum=0; for(int x:c) sum+=x;
            s=get_time(); merge_sort(a); e=get_time(); t3+=(e-s); sum=0; for(int x:a) sum+=x;
        }
        t1/=reps; t2/=reps; t3/=reps;
        f<<N<<","<<t1<<","<<t2<<","<<t3<<"\n"; cout<<N<<" "<<t1<<" "<<t2<<" "<<t3<<endl;
    }
    cout<<"saved to "<<out<<endl;
    return 0;
}
