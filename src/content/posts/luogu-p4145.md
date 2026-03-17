---
title: 'Luogu P4145 上帝造题的七分钟 2 花神游历各国 题解'
description: '**不可能用区间修改**……'
pubDate: 2022-04-14
updatedDate: 2022-04-14
draft: false
tags:
  - OI
  - OLD
classification: 2
---

# P4145 题解

[P4145 上帝造题的七分钟 2 / 花神游历各国](https://www.luogu.com.cn/problem/P4145)

#### 解题思路

**不可能用区间修改**

证明：

```
西江月·证明

即得易见平凡，仿照上例显然。留作习题答案略，读者自证不难。
反之亦然同理，推论自然成立。略去过程Q. E. D，由上可知证毕。
```
~~(被打)~~


$$
\text{用反证法证明}
\\\because\text{已知的量有且仅有区间长度}len\text{和区间和}t
\\\text{假设仅凭这两个量可以推出区间中每一个值开方后的和}
\\\therefore{当这两个量确定时，区间开方后的和的值为一确定}
\\\text{假设两个数列}\{a_n\}=1,2,3,4,5
\\\{b_n\}=1,2,4,4,4
\\\therefore\{a_n\}开方后的和的值为7
\\\{b_n\}开方后的和的值为8
\\又\because\{a_n\}与\{b_n\}的长度及和都一样
\\\therefore这与题设相矛盾
\\\therefore题设不成立，故原命题成立
\\\tiny Q.E.D
$$


~~所以直接暴力就好了~~

用线段树

#### 实现

这里有一个很重要的东西：
$$
\lfloor\sqrt{1}\rfloor=1
\\\lfloor\sqrt{0}\rfloor=0
$$
而
$$
\lfloor\sqrt{\lfloor\sqrt{\lfloor\sqrt{\lfloor\sqrt{\lfloor\sqrt{\lfloor\sqrt{1000000000000}\rfloor}\rfloor}\rfloor}\rfloor}\rfloor}\rfloor=1
$$
也就是说我们最多修改一个节点 $6$ 次就好了

考虑维护两个线段树：一个维护区间和，一个维护区间最大值，区间最大值小于等于 $1$ 时直接跳过修改

#### 完整代码

```cpp
#include <bits/stdc++.h>
using namespace std;
#define GO(__start,__end,__var) for(int __var = __start ; __var<=__end ; __var++)
#define GON(__start,__end,__var,_comp,_ope,_type) for(_type __var = __start ; __var _comp __end ; __var _ope)
#define GOGRA(__edge,__head,__start,__var) for(int __var = __head[__start];__var;__var=__edge[__var].next)
#define COMP(__type,__member,__comp) [=](__type a1,__type a2)->bool{ return a1.__member __comp a2.__member;}
const int maxn=1e5+12,maxm=2000;
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
//模板
#define lson k<<1
#define rson k<<1|1
#define mi int mid = (l+r)>>1
using namespace io;
lld t[maxn<<2],maxt[maxn<<2];//maxt是最大值，t是和
inline void Pushup(int k){
    t[k]=t[lson]+t[rson];
    maxt[k]=max(maxt[lson],maxt[rson]);
    return;
}
lld a[maxn];
inline void build(int k,int l,int r){
    if(l==r){
        maxt[k]=t[k]=a[l];
        return;
    }
    mi;
    build(lson,l,mid);
    build(rson,mid+1,r);
    Pushup(k);
}
inline void update(int k,int l,int r,int L,int R){
    if(l==r){
        maxt[k]=t[k]=sqrt(t[k]);
        return;
    }
    mi;
    if(maxt[k]<=1)return;
    if(L<=mid)update(lson,l,mid,L,R);
    if(R>mid)update(rson,mid+1,r,L,R);
    Pushup(k);
}
inline lld query(int k,int l,int r,int L,int R){
    if(L<=l&&R>=r)return t[k];
    mi;
    lld ans=0;
    if(L<=mid)ans+=query(lson,l,mid,L,R);
    if(R>mid)ans+=query(rson,mid+1,r,L,R);
    return ans;
}
int n,m;
inline void Read(){
    n=fr();
    GO(1,n,i)a[i]=fr_lld();
    m=fr();
    build(1,1,n);
    return;
}
inline void Solve(){
    GO(1,m,i){
        int q=fr(),l=fr(),r=fr();
        if(l>r){
            int swap = l;
            l = r;
            r = swap;
        }
        if(q==0){
            update(1,1,n,l,r);
        }
        else{
            fw_lld(query(1,1,n,l,r));putchar('\n');
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


#### 总结

~~有时候暴力未必不是最优解~~

$$
\huge\color{red}\text{十年OI一场空，不开long long见祖宗}
$$
