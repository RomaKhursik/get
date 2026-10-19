#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
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
    vector<int> sizes={500,1000,1500,2000,2500,3000,3500,4000,4500,5000};
    // каждый алгоритм в отдельный файл с 3 кривыми
    vector<string> names={"bubble","insertion","selection","heap","quick","merge"};
    for(int ai=0; ai<6; ai++){
        ofstream f("lab_sort/Data/task5_"+names[ai]+".csv", ios::out);
        f<<"N,sorted,random,reversed\n";
        for(int N:sizes){
            double t_best=0,t_avg=0,t_worst=0;
            int reps=3;
            for(int r=0;r<reps;r++){
                vector<int> sorted(N), rev(N), rnd(N);
                for(int i=0;i<N;i++) sorted[i]=i;
                for(int i=0;i<N;i++) rev[i]=N-i;
                for(int i=0;i<N;i++) rnd[i]=rand_uns(0,100000);

                vector<int> a=sorted;
                double s=get_time();
                if(ai==0) bubble_sort(a); else if(ai==1) insertion_sort(a); else if(ai==2) selection_sort(a); else if(ai==3) heap_sort(a); else if(ai==4) quick_sort(a); else merge_sort(a);
                double e=get_time(); t_best+=(e-s); volatile long long sum=0; for(int x:a) sum+=x;

                a=rnd;
                s=get_time();
                if(ai==0) bubble_sort(a); else if(ai==1) insertion_sort(a); else if(ai==2) selection_sort(a); else if(ai==3) heap_sort(a); else if(ai==4) quick_sort(a); else merge_sort(a);
                e=get_time(); t_avg+=(e-s); sum=0; for(int x:a) sum+=x;

                a=rev;
                s=get_time();
                if(ai==0) bubble_sort(a); else if(ai==1) insertion_sort(a); else if(ai==2) selection_sort(a); else if(ai==3) heap_sort(a); else if(ai==4) quick_sort(a); else merge_sort(a);
                e=get_time(); t_worst+=(e-s); sum=0; for(int x:a) sum+=x;
            }
            t_best/=reps; t_avg/=reps; t_worst/=reps;
            f<<N<<","<<t_best<<","<<t_avg<<","<<t_worst<<"\n";
            cout<<names[ai]<<" "<<N<<" "<<t_best<<" "<<t_avg<<" "<<t_worst<<endl;
        }
    }
    return 0;
}
