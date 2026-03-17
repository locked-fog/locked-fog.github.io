---
title: '差分约束'
description: '有形如 $x_i-x_j\le k_i$ 的一系列不等式，求满足这些不等式的一组解'
pubDate: 2022-04-14
updatedDate: 2022-04-14
draft: false
tags:
  - OI
  - OLD
classification: 2
---

# 差分约束

#### 原理

> 有形如 $x_i-x_j\le k_i$ 的一系列不等式，求满足这些不等式的一组解

例：

$$
\begin{cases}
x_1-x_2\le 3
\\x_2-x_3\le -2
\\x_1-x_3\le 1
\end{cases}
$$

可以比较轻松口算出几组解 

$\begin{cases}x_1=5\\x_2=3\\x_3=5\end{cases}$       $\begin{cases}x_1=0\\x_2=-2\\x_3=0\end{cases}$      $\begin{cases}x_1=0\\x_2=0\\x_3=2\end{cases}$ 

##### 问题转化

对于 $x_i-x_j\le k$ ，我们可以发现它等价于 $x_i \le x_j +k$ 。设想一个图，其中有一个超级源点，其到每个点的距离为 $0$ ，那么上面的式子可以转化为 $d_i \le d_j + w_{<j,i>}$ ，其中图的起点是超级源点。

这其实就是最短路网络中的三角不等式，所以我们可以考虑用图论-最短路来解决差分约束。

#### 实现

##### 连边

如何将约束条件转化为边，这是差分约束中最主要的问题。

在上文中，我们是将 $x_i-x_j\le k$ 中连接了边 $w_{<j,i>}=k$ 。在其他问题中需要根据题目要求分析。

##### 最短路

都行，注意判断负环回路（即无解的情况）

注意：~~`已死去的`~~`SPFA`中，判断负环回路时每个点最多入队是 `n+1` 次而非 `n` 次，因为有超级源点

#### 例题

[P5960 【模板】差分约束算法](https://www.luogu.com.cn/problem/P5960)

如上文，将每一个约束条件 $x_i -x_j \le k$ 转化为边 $w_{<j,i>}=k$ ，再加入超级源点，使其到每个点的距离为 $0$ ，跑一遍最短路，得到的最短路 $d_i$ 就对应一个解 $x_i$ 。

##### 代码

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
    inline void fw(int num){
        if(num<0){
            putchar('-');
            num=-num;
        }
        if(num>9)fw(num/10);
        putchar(num%10+'0');
    }
    inline void fw(int num,char backch){
        fw(num);
        putchar(backch);
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
int len,head[maxn];
struct Edge{
    int to,next,w;
}e[maxn];
inline void insert(int u,int v,int w){
    e[++len]={v,head[u],w};
    head[u]=len;
}
int n,m;
inline void Read(){
    n=fr();m=fr();
    GO(1,m,i){
        int u=fr(),v=fr(),w=fr();
        insert(v,u,w);
    }
    GO(1,n,i){
        insert(0,i,0);
    }
    return;
}
int dis[maxn];
int inqq[maxn];
bool inq[maxn];
queue<int>q;
inline void spfa(){
    memset(dis,0x3f,sizeof(dis));
    q.push(0);inqq[0]++;
    inq[0]=true;
    dis[0]=0;
    while(!q.empty()){
        int u=q.front();q.pop();inq[u]=false;
        GOGRA(e,head,u,i){
            int v=e[i].to,w=e[i].w;
            if(dis[v]>dis[u]+w){
                dis[v]=dis[u]+w;
                if(!inq[v]){
                    q.push(v);
                    inqq[v]++;
                    if(inqq[v]>=n+1){//注意是n+1
                        printf("NO");return;
                    }
                }
                inq[v]=true;
            }
        }
    }
    GO(1,n,i){
        fw(dis[i],' ');
    }
}
inline void Solve(){
    spfa();
    return;
}
signed main(){
    // freopen("Chorse.in","r",stdin);
    // freopen("Chores.out","w",stdout);
    Read();
    Solve();
    return 0;
}
```
