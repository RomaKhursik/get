#include <iostream>
#include <fstream>
#include <chrono>
#include <random>
#include <string>
#include <filesystem>
using namespace std;
double get_time(){return chrono::duration_cast<chrono::microseconds>(chrono::steady_clock::now().time_since_epoch()).count()/1e6;}
int rand_uns(int min,int max){unsigned seed=chrono::steady_clock::now().time_since_epoch().count(); static default_random_engine e(seed); uniform_int_distribution<int> d(min,max); return d(e);}
void merge_rec(int *a,int l,int r,int *tmp){ if(r-l<=1) return; int m=(l+r)/2; merge_rec(a,l,m,tmp); merge_rec(a,m,r,tmp); int i=l,j=m,k=l; while(i<m&&j<r) tmp[k++]=a[i]<a[j]?a[i++]:a[j++]; while(i<m) tmp[k++]=a[i++]; while(j<r) tmp[k++]=a[j++]; for(int k=l;k<r;k++) a[k]=tmp[k]; }
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
    string out=data_path("task2.csv");
    ofstream f(out); f<<"N,heap,quick,merge\n";
    int sizes[]={1000,5000,10000,20000,50000,100000,200000};
    int sn=sizeof(sizes)/sizeof(sizes[0]);
    for(int si=0;si<sn;si++){int N=sizes[si];
        double t1=0,t2=0,t3=0; int reps=5; if(N>50000) reps=3;
        for(int r=0;r<reps;r++){
            int *a=new int[N]; for(int i=0;i<N;i++) a[i]=rand_uns(0,1000000);
            int *b=new int[N]; int *c=new int[N]; for(int i=0;i<N;i++){b[i]=a[i]; c[i]=a[i];}
            double s=get_time(); heap_sort(b,N); double e=get_time(); t1+=(e-s); volatile long long sum=0; for(int i=0;i<N;i++) sum+=b[i];
            s=get_time(); quick_sort(c,N); e=get_time(); t2+=(e-s); sum=0; for(int i=0;i<N;i++) sum+=c[i];
            s=get_time(); merge_sort(a,N); e=get_time(); t3+=(e-s); sum=0; for(int i=0;i<N;i++) sum+=a[i];
            delete[] a; delete[] b; delete[] c;
        }
        t1/=reps; t2/=reps; t3/=reps;
        f<<N<<","<<t1<<","<<t2<<","<<t3<<"\n"; cout<<N<<" "<<t1<<" "<<t2<<" "<<t3<<endl;
    }
    cout<<"saved to "<<out<<endl;
    return 0;
}
