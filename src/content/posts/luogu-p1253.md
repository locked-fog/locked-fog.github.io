---
title: 'Luogu P1253 扶苏的问题 题解'
description: '线段树+动态开点'
pubDate: 2022-04-14
updatedDate: 2022-04-14
draft: false
tags:
  - OI
  - OLD
classification: 2
---

# P1253 题解

[P1253 [yLOI2018] 扶苏的问题 - 洛谷](https://www.luogu.com.cn/problem/P1253)

$update: \text{你谷Markdown的表格显示有问题，题解中的一部分表格可能无法正确显示}$

$update：\text{我还是把这篇文章的源码贴一下吧}$

[源码](https://www.luogu.com.cn/paste/d3e6rd9q)

#### 算法

线段树+动态开点

注意区间赋值和加法的相互关系

#### 实现

```cpp
#include<bits/stdc++.h>
using namespace std;
const int maxn=1e6+12;
inline long long fr(){
    register long long x=0,dis=1;
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
long long t[maxn<<1],lson[maxn<<1],rson[maxn<<1],lazya[maxn<<1],lazyx[maxn<<1][2];//动态开点 lazya->加 lazyx->赋值
int cnt=1;
```

##### 1、Pushdown

需要我们思考一下区间赋值与区间加的关系：

我们假设有一个区间：

| a    | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| val  | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    |

我们首先修改区间 $ 2 $ ~ $ 5 $ 的值为 $12$ 

| a    | 1    | 2               | 3               | 4               | 5               | 6    | 7    | 8    |
| ---- | ---- | --------------- | --------------- | --------------- | --------------- | ---- | ---- | ---- |
| val  | 1    | $\color{gold}9$ | $\color{gold}9$ | $\color{gold}9$ | $\color{gold}9$ | 6    | 7    | 8    |

 然后将区间 $ 3 $ ~ $ 6 $ 的值增加 $12$ 

| a    | 1    | 2               | 3                       | 4                       | 5                       | 6                       | 7    | 8    |
| ---- | ---- | --------------- | ----------------------- | ----------------------- | ----------------------- | ----------------------- | ---- | ---- |
| val  | 1    | $\color{gold}9$ | $\color{blue}{21=9+12}$ | $\color{blue}{21=9+12}$ | $\color{blue}{21=9+12}$ | $\color{blue}{18=6+12}$ | 7    | 8    |

我们发现**如果先修改区间的值，再增加区间的值，不会相互影响**

~~那我们这道题的`Pushdown`就愉快的写完了~~

**且慢！**

我们试想一下**先增加区间的值，再修改的情况**

如果按照上面推出的逻辑，我们会先把某个区间修改为 $x$ ，再增加 $y$ ，即变成 $x+y$ 。但事实上，我们需要让其变成 $y$ 。

所以上面的逻辑实际上存在问题，需要修改。

怎么改呢？

我们珂以注意到：**当我们进行了区间赋值操作后，这个区间之前增加的值实际上就没有任何意义**。这就意味着，我们珂以在修改了区间赋值的`lazy_tag`后，清空区间加法的 `lazy_tag` 

```cpp
inline void Pushdown(long long k,long long l,long long r){
    if(lazyx[k][0]){
        if(!lson[k])lson[k]=++cnt;
        if(!rson[k])rson[k]=++cnt;
        mi;
        t[lson[k]]=lazyx[k][1];
        t[rson[k]]=lazyx[k][1];
        lazyx[lson[k]][0]=1;
        lazyx[rson[k]][0]=1;
        lazyx[lson[k]][1]=lazyx[k][1];
        lazyx[rson[k]][1]=lazyx[k][1];
        lazyx[k][0]=0;
        lazya[lson[k]]=0;//清空操作
        lazya[rson[k]]=0;
    }
    if(lazya[k]){
        if(!lson[k])lson[k]=++cnt;
        if(!rson[k])rson[k]=++cnt;
        mi;
        t[lson[k]]+=lazya[k];
        t[rson[k]]+=lazya[k];
        lazya[lson[k]]+=lazya[k];
        lazya[rson[k]]+=lazya[k];
        lazya[k]=0;
    }
}
```

##### 2、Build

建树的过程就比较简单了，依次访问所有区间就好

```cpp
long long a[maxn];
inline void build(long long &k,long long l,long long r){
    if(!k)k=++cnt;
    if(l==r){
        t[k]=a[l];
        return;
    }
    mi;
    build(lson[k],l,mid);
    build(rson[k],mid+1,r);
    Pushup(k);
}
```

##### 3、update

有两个 `update` ，区间加法和区间赋值

如上文所述，区间赋值时需要将对应区间的加法 `lazy_tag` 归零

```cpp
inline void updatex(long long &k,long long l,long long r,long long L,long long R,long long x){
    if(!k)k=++cnt;
    if(L<=l&&R>=r){
        lazyx[k][0]=1;
        lazyx[k][1]=x;lazya[k]=0;
        t[k]=x;
        return;
    }
    Pushdown(k,l,r);
    mi;
    if(L<=mid)updatex(lson[k],l,mid,L,R,x);
    if(R>mid)updatex(rson[k],mid+1,r,L,R,x);
    Pushup(k);
}
inline void updatea(long long &k,long long l,long long r,long long L,long long R,long long x){
    if(!k)k=++cnt;
    if(L<=l&&R>=r){
        lazya[k]+=x;
        t[k]+=x;
        return;
    }
    Pushdown(k,l,r);
    mi;
    if(L<=mid)updatea(lson[k],l,mid,L,R,x);
    if(R>mid)updatea(rson[k],mid+1,r,L,R,x);
    Pushup(k);
}
```


#### 总结

要分析区间加法与区间赋值的相互关系，找到对应的解决方法。
$$
\huge\color{red}\text{十年OI一场空，不开long long见祖宗}
$$
