#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <random>
using namespace std;
double get_time(){return chrono::duration_cast<chrono::microseconds>(chrono::steady_clock::now().time_since_epoch()).count()/1e6;}
int rand_uns(int min,int max){unsigned seed=chrono::steady_clock::now().time_since_epoch().count(); static default_random_engine e(seed); uniform_int_distribution<int> d(min,max); return d(e);}
void bubble_sort(vector<int> &a){int n=a.size(); for(int i=0;i<n-1;i++) for(int j=0;j<n-i-1;j++) if(a[j]>a[j+1]) swap(a[j],a[j+1]);}
void insertion_sort(vector<int> &a){int n=a.size(); for(int i=1;i<n;i++){int k=a[i],j=i-1; while(j>=0&&a[j]>k){a[j+1]=a[j]; j--;} a[j+1]=k;}}
void selection_sort(vector<int> &a){int n=a.size(); for(int i=0;i<n-1;i++){int mn=i; for(int j=i+1;j<n;j++) if(a[j]<a[mn]) mn=j; swap(a[i],a[mn]);}}
void merge_sort_rec(vector<int> &a,int l,int r, vector<int> &tmp){ if(r-l<=1) return; int m=(l+r)/2; merge_sort_rec(a,l,m,tmp); merge_sort_rec(a,m,r,tmp); int i=l,j=m,k=l; while(i<m&&j<r) tmp[k++]=a[i]<a[j]?a[i++]:a[j++]; while(i<m) tmp[k++]=a[i++]; while(j<r) tmp[k++]=a[j++]; for(int k=l;k<r;k++) a[k]=tmp[k];}
void merge_sort(vector<int> &a){ vector<int> tmp(a.size()); merge_sort_rec(a,0,a.size(),tmp); }
void heapify(vector<int> &a,int n,int i){int l=2*i+1,r=2*i+2,m=i; if(l<n&&a[l]>a[m]) m=l; if(r<n&&a[r]>a[m]) m=r; if(m!=i){swap(a[i],a[m]); heapify(a,n,m);} }
void heap_sort(vector<int> &a){int n=a.size(); for(int i=n/2-1;i>=0;i--) heapify(a,n,i); for(int i=n-1;i>0;i--){swap(a[0],a[i]); heapify(a,i,0);} }
void quick_rec(vector<int> &a,int l,int r){if(l>=r) return; int i=l,j=r,p=a[(l+r)/2]; while(i<=j){while(a[i]<p) i++; while(a[j]>p) j--; if(i<=j) swap(a[i++],a[j--]);} if(l<j) quick_rec(a,l,j); if(i<r) quick_rec(a,i,r);}
void quick_sort(vector<int> &a){quick_rec(a,0,(int)a.size()-1);}
int main(){
    string opt="UNKNOWN";
#ifdef OPT_LEVEL
    opt=to_string(OPT_LEVEL);
#endif
    string fname="lab_sort/Data/task3_"+opt+".csv";
    if(opt=="UNKNOWN") fname="lab_sort/Data/task3.csv";
    ofstream f(fname, ios::out);
    f<<"N,bubble,insertion,selection,heap,quick,merge\n";
    vector<int> sizes={500,1000,1500,2000,2500,3000,3500,4000,4500,5000};
    for(int N:sizes){
        double tb=0,ti=0,ts=0,th=0,tq=0,tm=0;
        int reps=3;
        for(int r=0;r<reps;r++){
            vector<int> base(N); for(int i=0;i<N;i++) base[i]=rand_uns(0,100000);
            vector<int> a=base; double s=get_time(); bubble_sort(a); double e=get_time(); tb+=(e-s); volatile long long sum=0; for(int x:a) sum+=x;
            a=base; s=get_time(); insertion_sort(a); e=get_time(); ti+=(e-s); sum=0; for(int x:a) sum+=x;
            a=base; s=get_time(); selection_sort(a); e=get_time(); ts+=(e-s); sum=0; for(int x:a) sum+=x;
            a=base; s=get_time(); heap_sort(a); e=get_time(); th+=(e-s); sum=0; for(int x:a) sum+=x;
            a=base; s=get_time(); quick_sort(a); e=get_time(); tq+=(e-s); sum=0; for(int x:a) sum+=x;
            a=base; s=get_time(); merge_sort(a); e=get_time(); tm+=(e-s); sum=0; for(int x:a) sum+=x;
        }
        tb/=reps; ti/=reps; ts/=reps; th/=reps; tq/=reps; tm/=reps;
        f<<N<<","<<tb<<","<<ti<<","<<ts<<","<<th<<","<<tq<<","<<tm<<"\n";
        cout<<opt<<" "<<N<<" "<<tb<<" "<<ti<<" "<<ts<<" "<<th<<" "<<tq<<" "<<tm<<endl;
    }
    return 0;
}
