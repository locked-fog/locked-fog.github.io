---
title: "可持久化线段树"
description: "可持久化线段树，又名主席树，是一种可以保存历史记录的线段树。 "
pubDate: 2022-04-14
updatedDate: 2022-04-14
draft: false
tags:
  - OI
  - OLD
classification: 2
---

# 可持久化线段树

#### 1、基本概念

可持久化线段树，又名主席树，是一种可以保存历史记录的线段树。

由于线段树的修改是基于递归的单线修改（一次只修改一条线），所以可以考虑在修改时新建版本来储存修改~~（好像git)~~，需要使用动态开点线段树

#### 2、实现

```cpp
#include<bits/stdc++.h>
using namespace std;
inline int fr(){//快读
    register int x=0,dis=1;
    register char ch=getchar();
    while(ch<'0'||ch>'9'){
        if(ch =='-')dis=-1;
        ch=getchar();
    }
    while(ch>='0'&&ch<='9'){
        x=(x<<1)+(x<<3)+(ch^48);
        ch = getchar();
    }
    return x*dis;
}
inline void fw(int num){//快写
    if(num<0){
        putchar('-');
        num=-num;
    }
    if(num>9)fw(num/10);
    putchar(num%10+'0');
}
const int maxn=1e7;
int lson[maxn<<2],rson[maxn<<2];//左右儿子
int t[maxn<<2];//树
int cnt=1,version,root[maxn];//cnt->当前动态下标，version->当前版本，root[ver]->第ver个版本的根节点下标
```

##### 2.1、Pushup

```cpp
//其实和线段树的Pushup没什么区别（
inline void Pushup(int k){t[k]=t[lson[k]]+t[rson[k]];}
```

##### 2.2、clone

```cpp
//就是建立新版本时，因为之前的映射关系并不会全部变化，因此需要一个函数来将原本的映射关系复制到新节点上
inline void clone(int &k){//k是旧版本的节点下标
    t[++cnt]=t[k];//++cnt就是新建节点
    lson[cnt]=lson[k];
    rson[cnt]=rson[k];
    k=cnt;//要对k进行更新
}
```

##### 2.3、update

```cpp
//注意每次update的节点都需要用clone
inline void update(int &k,int l,int r,int v,int x){
    clone(k);
    if(l==r){
        t[k]=x;return;
    }
    int mid=(l+r)>>1;
    if(v<=mid)update(lson[k],l,mid,v,x);
    else update(rson[k],mid+1,r,v,x);
    Pushup(k);
}
```

##### 2.4、query

```cpp
//和线段树几乎一模一样
inline int query(int k,int l,int r,int v){
    if(!k)return 0;
    if(l==r)return t[k];
    int mid=(l+r)>>1;
    return v<=mid?query(lson[k],l,mid,v):query(rson[k],mid+1,r,v);
}
```

##### 2.5、main  ~~mian~~

```cpp
//主要是看看root怎么用
int main(){
    for(int i=1;i<=n;i++){
        int ver=fr(),op=fr();//ver->版本,op->操作
        if(op==1){
            int v=fr(),x=fr();//v->位置,x->值
            int temp=root[ver];//找到目标根节点
            update(temp,1,n,v,x);
            root[++version]=temp;//更新
        }else{
            int v=fr();//v->位置
            int temp=root[ver];
            fw(query(temp,1,n,v));
            root[++version]=temp;
        }
    }
}
```

#### 3、例题 P3919 【模板】可持久化线段树 1（可持久化数组）

[P3919 【模板】可持久化线段树 1（可持久化数组）](https://www.luogu.com.cn/problem/P3919)

```cpp
#include <bits/stdc++.h>
using namespace std;
#define GO(__start,__end,__var) for(int __var = __start ; __var<=__end ; __var++)
#define GON(__start,__end,__var,_comp,_ope,_type) for(_type __var = __start ; __var _comp __end ; __var _ope)
#define GOGRA(__edge,__head,__start,__var) for(int __var = __head[__start];__var;__var=__edge[__var].next)
#define COMP(__type,__member,__comp) [=](__type a1,__type a2)->bool{ return a1.__member __comp a2.__member;}
const int maxn=1e7,maxm=3000;
typedef long long lld;
typedef double lf;
namespace io{
    inline int fr(){
        register int x=0,dis=1;
        register char ch=getchar();
        while(ch<'0'||ch>'9'){
            if(ch =='-')dis=-1;
            ch=getchar();
        }
        while(ch>='0'&&ch<='9'){
            x=(x<<1)+(x<<3)+(ch^48);
            ch = getchar();
        }
        return x*dis;
    }
    inline lld fr_lld(){
        lld x=0,dis=1;
        char ch=getchar();
        while(ch<'0'||ch>'9'){
            if(ch=='-')dis=-1;
            ch=getchar();
        }
        while(ch>='0'&&ch<='9'){
            x=(x<<1)+(x<<3)+(ch^48);
            ch = getchar();
        }
        return x*dis;
    }
    inline lf fr_lf(){
        lf x=0;int dis =1;lf l=0.1;
        char ch=getchar();
        while(ch<'0'||ch>'9'){
            if(ch=='-')dis=-1;
            ch=getchar();
        }
        while(ch>='0'&&ch<='9'){
            x= 10*x+(ch^48);
            ch=getchar();
        }
        if(ch=='.'){
            ch=getchar();
            while(ch>='0'&&ch<='9'){
                x = x+l*(ch^48);
                l*=0.1;
            }
        }
        return x*dis;
    }
    struct highp{
        int a[maxm];int dis=1;int base;
        highp(){
            this->a[0]=1;
            this->base=10;
        }
        highp(char s[]){
            this->base=10;
            if(s[0]=='-'){
                this->dis=-1;
                GO(0,strlen(s),i)s[i]=s[i+1];
            }
            this->a[0]=strlen(s);
            GO(1,this->a[0],i)this->a[i]=s[this->a[0]-i]-'0';
        }
        highp(char s[],int Base){
            this->base=Base;
            if(s[0]=='-'){
                this->dis=-1;
                GO(0,strlen(s),i)s[i]=s[i+1];
            }
            this->a[0]=strlen(s);
            if(base>10){
                GO(1,this->a[0],i){
                    int pos = this->a[0]-i;
                    if(s[pos]>='0'&&s[pos]<='9')this->a[i]=s[pos]-'0';
                    if(s[pos]>='a'&&s[pos]<='z')this->a[i]=s[pos]-'a'+10;
                    if(s[pos]>='A'&&s[pos]<='Z')this->a[i]=s[pos]-'A'+10;
                }
            }else GO(1,this->a[0],i) this->a[i]=s[this->a[0]-i]-'0';
        }
    public:
        bool operator==(const highp& num){
            if(this->base==num.base){
                GO(0,this->a[0],i)if(this->a[i]!=num.a[i])return false;
                return true;
            }
        }
        bool operator!=(const highp& num){
            return !(*this==num);
        }
        bool operator>(const highp& num){
            if(this->base==num.base){
                if(*this==num)return false;
                if(this->dis==num.dis){
                    if(this->a[0]==num.a[0]){
                        GON(this->a[0],1,i,>=,--,int){
                            if(this->a[i]>num.a[i])return this->dis==-1?false:true;
                            if(this->a[i]<num.a[i])return this->dis==-1?true:false;
                        }
                    }else return this->dis==1?this->a[0]>num.a[0]:this->a[0]<num.a[0];
                }else return this->dis>num.dis;
            }
        }
        bool operator<(const highp& num){
            if(this->base==num.base){
                if(*this==num)return false;
                else return !(*this>num);
            }
        }
        bool operator>=(const highp& num){
            if(this->base==num.base){
                return !(*this<num);
            }
        }
        bool operator<=(const highp& num){
            if(this->base==num.base){
                return !(*this>num);
            }
        }
        highp operator=(const lld& num){
            char num1[maxm];
            sprintf(num1,"%lld",num);
            highp num2(num1);
            *this=num2;
        }
        highp operator+(const highp& num){
            if(this->base==num.base){
                highp ans;
                if(this->dis==-1&&num.dis==-1)ans.dis==-1;
                if(this->dis==-1&&num.dis==1){
                    this->dis=1;
                    highp temp = num;
                    ans = temp-*this;
                    this->dis=-1;
                    return ans;
                }
                if(this->dis==1&&num.dis==-1){
                    highp temp = num;
                    temp.dis=1;
                    ans = *this - temp;
                    return ans;
                }
                int len=max(this->a[0],num.a[0]);
                GO(1,len,i){
                    ans.a[i]+=this->a[i]+num.a[i];
                    ans.a[i+1]=ans.a[i]/base;
                    ans.a[i]%=base;
                }
                if(ans.a[len+1]>0)ans.a[0]=len+1;
                else ans.a[0]=len;
                return ans;
            }
        }
        highp operator+(const lld& num){
            highp num1;
            num1=num;
            return *this+num1;
        }
        highp operator-(const highp& num){
            if(this->base==num.base){
                highp ans;
                if(this->dis==-1&&num.dis==1){
                    highp temp = num;
                    temp.dis=-1;
                    return *this+temp;
                }
                if(this->dis==1&&num.dis==-1){
                    highp temp = num;
                    temp.dis=1;
                    return *this+temp;
                }
                if(this->dis==-1&&num.dis==-1){
                    highp temp=num;
                    return temp-*this;
                }
                if(*this<num){
                    highp temp=num;
                    ans=temp-*this;
                    ans.dis=-1;
                    return ans;
                }
                GO(1,this->a[0],i){
                    ans.a[i]+=this->a[i]-num.a[i];
                    if(ans.a[i]<0){
                        ans.a[i+1]--;
                        ans.a[i]+=base;
                    }
                }
                int len = this->a[0];
                while(ans.a[len]==0 && len>=2)len--;
                ans.a[0]=len;
                return ans;
            }
        }
        highp operator-(const lld& num){
            highp num1;
            num1=num;
            return *this-num;
        }
        highp operator*(const highp& num){
            if(this->base==num.base){
                highp ans,temp=num;
                highp ZERO,ONE;
                ZERO=0;ONE=1;
                if(*this==ZERO||temp==ZERO) return ZERO;
                if(*this==ONE)return num;
                if(temp==ONE)return *this;
                if(this->dis==-1 && num.dis==1 || this->dis==1 && num.dis==-1) ans.dis=-1;
                GO(1,this->a[0],i){
                    GO(1,num.a[0],j){
                        ans.a[i+j-1]+=this->a[i]*num.a[j];
                        ans.a[i+j]+=ans.a[i+j-1]/base;
                        ans.a[i+j-1]%=base;
                    }
                }
                if(ans.a[this->a[0]+num.a[0]])ans.a[0]=this->a[0]+num.a[0];
                else ans.a[0]=this->a[0]+num.a[0]-1;
                return ans;
            }
        }
        highp operator*(const lld& num){
            highp num1;
            num1=num;
            return *this*num1;
        }
        void print(){
            if(this->dis==-1)putchar('-');
            if(this->base>10){
                GON(this->a[0],1,i,>=,--,int){
                    if(this->a[i]<=9)putchar(this->a[i]+'0');
                    else if(10<=this->a[i])putchar(this->a[i]+'A'-10);
                }
            }else GON(this->a[0],1,i,>=,--,int) putchar(this->a[i]+'0');
        }
    };
    highp operator+(const lld& num1,const highp& num2){
        highp num;
        num=num1;
        return num+num2;
    }
    highp operator-(const lld& num1,const highp& num2){
        highp num;
        num=num1;
        return num-num2;
    }
    highp fr_hp(){
        char num[maxm];register int pos = 0;
        register char ch = getchar();
        while(ch<'0'|| ch>'9'&&ch<'A' || ch>'Z' && ch<'a' || ch>'z'){
            if(ch=='-')num[pos++]='-';
            ch=getchar();
        }
        while(ch>='0'&&ch<='9' || ch>='A'&& ch<='Z' || ch>='a'&& ch<='z'){
            num[pos++]=ch;
            ch=getchar();
        }
        highp b(num);
        return b;
    }
    inline void fw(int num){
        if(num<0){
            putchar('-');
            num=-num;
        }
        if(num>9)fw(num/10);
        putchar(num%10+'0');
    }
    inline void fw_lld(lld num){
        if(num<0){
            putchar('-');
            num=-num;
        }
        if(num>9)fw_lld(num/10);
        putchar(num%10+'0');
    }
}
using namespace io;
int lson[maxn<<2],rson[maxn<<2],t[maxn<<2];
int cnt=1;
int root[maxn];
int a[maxn<<1];
inline void Pushup(int k){t[k]=t[lson[k]]+t[rson[k]];}
inline void clone(int &k){//对应版本的树根信息
    lson[++cnt]=lson[k];
    rson[cnt]=rson[k];
    t[cnt]=t[k];
    k=cnt;
}
inline void build(int &k,int l,int r){
    if(!k)k=++cnt;
    if(l==r){
        t[k]=a[l];
        return;
    }
    int mid=(l+r)>>1;
    build(lson[k],l,mid);
    build(rson[k],mid+1,r);
    Pushup(k);
}
inline void update(int &k,int l,int r,int v,int x){
    clone(k);
    if(l==r){
        t[k]=x;
        return;
    }
    int mid=(l+r)>>1;
    if(v<=mid)update(lson[k],l,mid,v,x);
    else update(rson[k],mid+1,r,v,x);
    Pushup(k);
}
inline int query(int k,int l,int r,int v){
    if(!k)return 0;
    if(l==r)return t[k];
    int mid=(l+r)>>1;
    return v<=mid?query(lson[k],l,mid,v):query(rson[k],mid+1,r,v);
}
int n,m;
inline void Read(){
    n=fr(),m=fr();
    GO(1,n,i)a[i]=fr();
    int temp=1;
    build(temp,1,n);root[0]=1;
    return;
}
int version;
inline void Solve(){
    GO(1,m,i){
        int ver=fr(),op=fr();
        if(op==1){
            int v=fr(),x=fr(),temp=root[ver];
            update(temp,1,n,v,x);
            root[++version]=temp;
        }else{
            int v=fr(),temp=root[ver];
            fw(query(temp,1,n,v));putchar('\n');
            root[++version]=temp;
        }
    }
    return;
}
int main(){
    // freopen("Chorse.in","r",stdin);
    // freopen("Chores.out","w",stdout);
    Read();
    Solve();
    return 0;
}
```
