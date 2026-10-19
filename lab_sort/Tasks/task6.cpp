#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <random>
using namespace std;
double get_time(){return chrono::duration_cast<chrono::microseconds>(chrono::steady_clock::now().time_since_epoch()).count()/1e6;}
int rand_uns(int min,int max){unsigned seed=chrono::steady_clock::now().time_since_epoch().count(); static default_random_engine e(seed); uniform_int_distribution<int> d(min,max); return d(e);}
int main(){
    ofstream f("lab_sort/Data/task6.csv", ios::out);
    f<<"N,gen,forward,backward,output\n";
    vector<int> sizes={10000,50000,100000,200000,500000,1000000};
    for(int N:sizes){
        int reps=5;
        if(N>=500000) reps=3;
        double t_gen=0,t_for=0,t_back=0,t_out=0;
        // Для точности повторяем много раз и усредняем
        for(int r=0;r<reps;r++){
            // генерация
            {
                double s=get_time();
                vector<int> a(N);
                for(int i=0;i<N;i++) a[i]=rand_uns(0,1000000);
                double e=get_time(); t_gen+=(e-s);
                volatile long long sum=0; for(int x:a) sum+=x;
            }
            // подготовка массива для обработки
            vector<int> a(N);
            for(int i=0;i<N;i++) a[i]=rand_uns(0,1000000);
            // forward
            {
                double s=get_time();
                volatile long long sum=0;
                for(int i=0;i<N;i++) sum+=a[i]*2+1;
                double e=get_time(); t_for+=(e-s);
            }
            // backward
            {
                double s=get_time();
                volatile long long sum=0;
                for(int i=N-1;i>=0;i--) sum+=a[i]*2+1;
                double e=get_time(); t_back+=(e-s);
            }
            // вывод на экран (в файл, без флеша экрана)
            {
                // чтобы не спамить консоль, измеряем вывод в /dev/null через stringstream или файл
                // делаем вывод в файл temp
                double s=get_time();
                ofstream tmp("/tmp/out_tmp.txt");
                for(int i=0;i<N;i++) tmp<<a[i]<<" ";
                tmp.close();
                double e=get_time(); t_out+=(e-s);
            }
        }
        t_gen/=reps; t_for/=reps; t_back/=reps; t_out/=reps;
        f<<N<<","<<t_gen<<","<<t_for<<","<<t_back<<","<<t_out<<"\n";
        cout<<N<<" "<<t_gen<<" "<<t_for<<" "<<t_back<<" "<<t_out<<endl;
    }
    return 0;
}
