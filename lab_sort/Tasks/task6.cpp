#include <iostream>
#include <fstream>
#include <chrono>
#include <random>
#include <string>
#include <filesystem>
using namespace std;
double get_time(){return chrono::duration_cast<chrono::microseconds>(chrono::steady_clock::now().time_since_epoch()).count()/1e6;}
int rand_uns(int min,int max){unsigned seed=chrono::steady_clock::now().time_since_epoch().count(); static default_random_engine e(seed); uniform_int_distribution<int> d(min,max); return d(e);}
string data_path(string name){
    string cand[5]={"lab_sort/Data/"+name,"../Data/"+name,"Data/"+name,name,"../lab_sort/Data/"+name};
    for(int i=0;i<5;i++) if(!filesystem::path(cand[i]).parent_path().empty()) filesystem::create_directories(filesystem::path(cand[i]).parent_path());
    for(int i=0;i<5;i++){ ofstream t(cand[i], ios::app); if(t){ t.close(); return cand[i]; } }
    return cand[0];
}
int main(){
    string out=data_path("task6.csv");
    ofstream f(out); f<<"N,gen,forward,backward,output\n";
    int sizes[]={10000,50000,100000,200000,500000,1000000};
    int sn=sizeof(sizes)/sizeof(sizes[0]);
    for(int si=0;si<sn;si++){int N=sizes[si];
        int reps=5; if(N>=500000) reps=3;
        double t_gen=0,t_for=0,t_back=0,t_out=0;
        for(int r=0;r<reps;r++){
            { double s=get_time(); int *a=new int[N]; for(int i=0;i<N;i++) a[i]=rand_uns(0,1000000); double e=get_time(); t_gen+=(e-s); volatile long long sum=0; for(int i=0;i<N;i++) sum+=a[i]; delete[] a; }
            int *a=new int[N]; for(int i=0;i<N;i++) a[i]=rand_uns(0,1000000);
            { double s=get_time(); volatile long long sum=0; for(int i=0;i<N;i++) sum+=a[i]*2+1; double e=get_time(); t_for+=(e-s); }
            { double s=get_time(); volatile long long sum=0; for(int i=N-1;i>=0;i--) sum+=a[i]*2+1; double e=get_time(); t_back+=(e-s); }
            { double s=get_time(); ofstream tmp("/tmp/out_tmp.txt"); for(int i=0;i<N;i++) tmp<<a[i]<<" "; tmp.close(); double e=get_time(); t_out+=(e-s); }
            delete[] a;
        }
        t_gen/=reps; t_for/=reps; t_back/=reps; t_out/=reps;
        f<<N<<","<<t_gen<<","<<t_for<<","<<t_back<<","<<t_out<<"\n"; cout<<N<<" "<<t_gen<<" "<<t_for<<" "<<t_back<<" "<<t_out<<endl;
    }
    cout<<"saved to "<<out<<endl;
    return 0;
}
