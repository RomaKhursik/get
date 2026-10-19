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
    ofstream f("lab_sort/Data/task7.csv", ios::out);
    f<<"N,bubble,insertion,selection,heap,quick,merge\n";
    vector<int> sizes;
    for(int i=3;i<=100;i+=2) sizes.push_back(i);
    // заранее генерим много случайных массивов для каждого N, чтобы не генерить внутри таймера
    for(int N:sizes){
        int repeats_inside=5000;
        if(N>50) repeats_inside=2000;
        // генерим пул массивов
        int pool=100;
        vector<vector<int>> pool_data;
        for(int p=0;p<pool;p++){ vector<int> a(N); for(int i=0;i<N;i++) a[i]=rand_uns(0,1000); pool_data.push_back(a); }
        double tb=0,ti=0,ts=0,th=0,tq=0,tm=0;
        // bubble
        {
            double s=get_time();
            for(int k=0;k<repeats_inside;k++){ vector<int> a=pool_data[k%pool]; bubble_sort(a); volatile long long sum=0; for(int x:a) sum+=x; }
            double e=get_time(); tb=(e-s)/repeats_inside;
        }
        {
            double s=get_time();
            for(int k=0;k<repeats_inside;k++){ vector<int> a=pool_data[k%pool]; insertion_sort(a); volatile long long sum=0; for(int x:a) sum+=x; }
            double e=get_time(); ti=(e-s)/repeats_inside;
        }
        {
            double s=get_time();
            for(int k=0;k<repeats_inside;k++){ vector<int> a=pool_data[k%pool]; selection_sort(a); volatile long long sum=0; for(int x:a) sum+=x; }
            double e=get_time(); ts=(e-s)/repeats_inside;
        }
        {
            double s=get_time();
            for(int k=0;k<repeats_inside;k++){ vector<int> a=pool_data[k%pool]; heap_sort(a); volatile long long sum=0; for(int x:a) sum+=x; }
            double e=get_time(); th=(e-s)/repeats_inside;
        }
        {
            double s=get_time();
            for(int k=0;k<repeats_inside;k++){ vector<int> a=pool_data[k%pool]; quick_sort(a); volatile long long sum=0; for(int x:a) sum+=x; }
            double e=get_time(); tq=(e-s)/repeats_inside;
        }
        {
            double s=get_time();
            for(int k=0;k<repeats_inside;k++){ vector<int> a=pool_data[k%pool]; merge_sort(a); volatile long long sum=0; for(int x:a) sum+=x; }
            double e=get_time(); tm=(e-s)/repeats_inside;
        }
        f<<N<<","<<tb<<","<<ti<<","<<ts<<","<<th<<","<<tq<<","<<tm<<"\n";
        cout<<N<<" "<<tb<<" "<<ti<<" "<<ts<<" "<<th<<" "<<tq<<" "<<tm<<endl;
    }
    return 0;
}
