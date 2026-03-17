---
title: "高级打字机"
description: "算法：主席树（柯持久化线段树）+单点修改+单点查询"
pubDate: 2022-04-14 
updatedDate: 2022-04-14 
draft: false
tags:
  - OI
  - OLD
classification: 2
---

# [P1383 高级打字机](https://www.luogu.com.cn/problem/P1383) 题解

算法：主席树（柯持久化线段树）+单点修改+单点查询

![](https://cdn.luogu.com.cn/upload/pic/37472.png)

#### 实现

##### 1、如何建树？

我们发现题目中没有提到树的长度，但是我们柯以发现这样一棵树最长就是 $ n $ .

所以我们柯以直接认为这棵树是 $ [1,n] $ 这个区间.

同时我们还发现，没有进行过修改的地点它的值是 $ 0 $ .

所以我们也不用写建树的代码，直接写修改的代码即柯

##### 2、撤销？

撤销操作的实质就是将某一个版本的内容原封不动地复制到新版本中。

我们假设 `root[version]`储存的是 `version` 版本的树根信息，那么在当前为 `k` 步时撤销 `x` 步的原理为：

```cpp
root[++k]=root[k-x-1];
```

注意是 `k-x-1` ，因为前面使用了 `k++` ， `k` 的值增加了 $1$ .

##### 3、修改？

看起来这道题已经基本结束了，但仔细一想就会发现还有些问题没解决。

**如何确定将要修改的值的位置？**

在标准的主席树中， $update$ 的写法是：

```cpp
inline void update(int &k,int l,int r,int v,int x)
```

 但显然，在这道题中，我们无法直接归纳出 `v` 的值。

所以我们柯以维护一个数组 `len[version]` 代表第 $version$ 个版本中将要修改的值的位置（ $\text{字符串的长度}$ ），随着版本的更新而更新。

所以上面的撤销需要更正为：

```cpp
root[++k]=root[k-x-1];
len[k]=len[k-x-1];
```

#### 代码

```cpp
#include <bits/stdc++.h>
using namespace std;
#define mi int mid = (l+r)>>1;
#define GO(__start,__end,__var) for(int __var = __start ; __var<=__end ; __var++)
const int maxn=1e6+12,maxm=3000;
typedef long long lld;
typedef double lf;
int t[maxn<<1],lson[maxn<<1],rson[maxn<<1];//柯持久化线段树
int cnt,root[maxn],version;//cnt->节点数量，root、version->如上文
int len[maxn],le;//如上文,le表示需要修改的位置
inline void clone(int &k){//clone操作
    t[++cnt]=t[k];
    lson[cnt]=lson[k];
    rson[cnt]=rson[k];
    k=cnt;
}
inline void update(int &k,int l,int r,char x){
    clone(k);
    if(l==r){
        t[k]=x;
        return;
    }
    mi;
    if(le<=mid)update(lson[k],l,mid,x);//le就是将要修改的值的位置
    else update(rson[k],mid+1,r,x);
    return;
}
inline char query(int k,int l,int r,int v){
    if(!k)return 0;
    if(l==r)return t[k];
    mi;
    return v<=mid?query(lson[k],l,mid,v):query(rson[k],mid+1,r,v);//三目运算，注意检查C++版本是否支持
}
int n;
inline void Read(){
    cin>>n;
    return;
}
inline void Solve(){
    GO(1,n,i){
        char op;
        cin>>op;
        if(op=='T'){
            char x;
            cin>>x;
            le++;
            int temp=root[version];
            update(temp,1,n,x);
            root[++version]=temp;len[version]=le;//版本更新
        }
        else if(op=='Q'){
            int x;
            cin>>x;
            cout<<query(root[version],1,n,x)<<endl;
        }
        else if(op=='U'){
            int x;
            cin>>x;
            le=len[version-x];len[++version]=le;
            root[version]=root[version-x-1];//如上文
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

$362ms/13.93MB$

**AC代码和实现中讲的内容略有区别，请注意分辨**
