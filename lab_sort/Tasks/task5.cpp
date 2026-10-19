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
void merge_rec(int *a,int l,int r,int *tmp){ if(r-l<=1) return; int m=(l+r)/2; merge_rec(a,l,m,tmp); merge_rec(a,m,r,tmp); int i=l,j=m,k=l; while(i<m&&j<r) tmp[k++]=a[i]<a[j]?a[i++]:a[j++]; while(i<m) tmp[k++]=a[i++]; while(j<r) tmp[k++]=a[j++]; for(int k=l;k<r;k++) a[k]=tmp[k];}
void merge_sort(int *a,int n){ int *tmp=new int[n]; merge_rec(a,0,n,tmp); delete[] tmp; }
void heapify(int *a,int n,int i){int l=2*i+1,r=2*i+2,m=i; if(l<n&&a[l]>a[m]) m=l; if(r<n&&a[r]>a[m]) m=r; if(m!=i){swap(a[i],a[m]); heapify(a,n,m);} }
void heap_sort(int *a,int n){for(int i=n/2-1;i>=0;i--) heapify(a,n,i); for(int i=n-1;i>0;i--){swap(a[0],a[i]); heapify(a,i,0);} }
void quick_rec(int *a,int l,int r){if(l>=r) return; int i=l,j=r,p=a[(l+r)/2]; while(i<=j){while(a[i]<p) i++; while(a[j]>p) j--; if(i<=j) swap(a[i++],a[j--]);} if(l<j) quick_rec(a,l,j); if(i<r) quick_rec(a,i,r);}
void quick_sort(int *a,int n){quick_rec(a,0,n-1);}
string data_path(string name){
    string cand[5]={"lab_sort/Data/"+name,"../Data/"+name,"Data/"+name,name,"../lab_sort/Data/"+name};
    for(int i=0;i<5;i++) if(!filesystem::path(cand[i]).parent_path().empty()) filesystem::create_directories(filesystem::path(cand[i]).parent_path());
    for(int i=0;i<5;i++){ ofstream t(cand[i], ios::app); if(t){ t.close(); return cand[i]; } }
    return cand[0];
}
int main(){
    int sizes[]={500,1000,1500,2000,2500,3000,3500,4000,4500,5000};
    int sn=sizeof(sizes)/sizeof(sizes[0]);
    string names[6]={"bubble","insertion","selection","heap","quick","merge"};
    for(int ai=0; ai<6; ai++){
        string out=data_path("task5_"+names[ai]+".csv");
        ofstream f(out); f<<"N,sorted,random,reversed\n";
        for(int si=0;si<sn;si++){int N=sizes[si];
            double t_best=0,t_avg=0,t_worst=0; int reps=3;
            for(int r=0;r<reps;r++){
                int *sorted=new int[N]; int *rev=new int[N]; int *rnd=new int[N];
                for(int i=0;i<N;i++) sorted[i]=i;
                for(int i=0;i<N;i++) rev[i]=N-i;
                for(int i=0;i<N;i++) rnd[i]=rand_uns(0,100000);
                int *a=new int[N];
                for(int i=0;i<N;i++) a[i]=sorted[i];
                double s=get_time();
                if(ai==0) bubble_sort(a,N); else if(ai==1) insertion_sort(a,N); else if(ai==2) selection_sort(a,N); else if(ai==3) heap_sort(a,N); else if(ai==4) quick_sort(a,N); else merge_sort(a,N);
                double e=get_time(); t_best+=(e-s); volatile long long sum=0; for(int i=0;i<N;i++) sum+=a[i];
                for(int i=0;i<N;i++) a[i]=rnd[i]; s=get_time();
                if(ai==0) bubble_sort(a,N); else if(ai==1) insertion_sort(a,N); else if(ai==2) selection_sort(a,N); else if(ai==3) heap_sort(a,N); else if(ai==4) quick_sort(a,N); else merge_sort(a,N);
                e=get_time(); t_avg+=(e-s); sum=0; for(int i=0;i<N;i++) sum+=a[i];
                for(int i=0;i<N;i++) a[i]=rev[i]; s=get_time();
                if(ai==0) bubble_sort(a,N); else if(ai==1) insertion_sort(a,N); else if(ai==2) selection_sort(a,N); else if(ai==3) heap_sort(a,N); else if(ai==4) quick_sort(a,N); else merge_sort(a,N);
                e=get_time(); t_worst+=(e-s); sum=0; for(int i=0;i<N;i++) sum+=a[i];
                delete[] sorted; delete[] rev; delete[] rnd; delete[] a;
            }
            t_best/=reps; t_avg/=reps; t_worst/=reps;
            f<<N<<","<<t_best<<","<<t_avg<<","<<t_worst<<"\n"; cout<<names[ai]<<" "<<N<<" "<<t_best<<" "<<t_avg<<" "<<t_worst<<endl;
        }
        cout<<"saved "<<out<<endl;
    }
    return 0;
}
