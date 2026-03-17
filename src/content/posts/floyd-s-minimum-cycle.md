---
title: 'Floyd求最小环'
description: '在一张有环的图中，通过 $O(n^3)$ 的时间效率求出边长最小的环'
pubDate: 2022-04-13
updatedDate: 2022-04-13
draft: false
tags:
  - OI
  - OLD
classification: 2
---

# Floyd求最小环

#### 一、算法描述

在一张有环的图中，通过 $O(n^3)$ 的时间效率求出边长最小的环

 

#### 二、原理与正确性推导

前置知识：

####  $\text{Floyd}$ 正确性推导：

Floyd的递推公式如下

$$
\\dp[i][j]=\min_{1 \le k \le n}(d[i][k]+d[k][j])
$$

所以，当 $dp[i][k]$ 和 $dp[k][j]$ 都取最小值时，由公式珂知 $dp[i][j]$ 会取到最小值


证明：设 $i$ 和 $j$ 之间的最短路径上的节点集中(不包含 $i$ 、 $j$ ),编号最大为 $x$ 

$$
\therefore 当k=x时，d[i][j]一定能得到最小值
$$

$$
用强归纳法证明
$$

$$
设i到x中间编号最大的是x_1，x到j中间编号最大的是x_2
$$

$$
\because x是i到j中间编号最大的
$$

$$
\therefore x_1\lt x,x_2\lt x
$$

$$
\therefore 根据结论，k=x_1时，d[i][k]已取得最小值
$$

$$
k=x_2时d[x][j]已取得最小值
$$

$$
\therefore 当k=x时，d[i][k]和d[k][j]都已取得最小值
$$

$$
\therefore 当k=x时，d[i][j]能取得最小值
$$

$$
\tiny Q.E.D
$$

既然已经证明了上面的公式是正确的，那么根据公式写出的 $Floyd$ 算法也应是正确的

我们首先写出 $Floyd$ 的核心代码

```cpp
for(int k=1;k<=n;k++)//以k为中转点
	for(int i=1;i<=n;i++)//i为起点
		for(int j=1;j<=n;j++)//j为终点
			d[i][j]=min(d[i][j],d[i][k]+d[k][j]);
```

对这个算法进行分析珂知



在 $Floyd$ 算法枚举第 $k$ 个中转点时，已经得到了前 $k-1$ 个中转点的最短路径

这 $k-1$ 个点不包括点 $k$ ，并且他们的最短路径也不经过点 $k$ （排除起点、终点）



那么我们从前 $k-1$ 个点中选取两个点 $i,j$ 

由上珂知：由 $i$ 到 $j$ 的最短路径已经求出

如果 $j$ 能到 $k$ ，且 $k$ 能到 $i$ 

那么连接 $i-j-k-i$ ，我们就得到了包含 $\{i,j,k\}$ 三个点的最小环

最后枚举所有用这个方法算出的最小环，求最小即珂

#### 三、例题及代码

[P6175 无向图的最小环问题](https://www.luogu.com.cn/problem/solution/P6175)

由于题目中的 $1\le n\le 100$ ，我们珂以用时间效率为 $O(n^3)$ 的 $Floyd$ 来求最小环

核心代码：

```cpp
for(int k=1;k<=n;k++){
    for(int i=1;i<k;i++){
        for(int j=i+1;j<k;j++){
            ans=min(ans,dis[i][j]+a[j][k]+a[k][i]);
        }
    }
    for(int i=1;i<=n;i++){
        for(int j=1;j<=n;j++){
            dis[i][j]=min(dis[i][j],dis[i][k]+dis[k][j]);
            dis[j][i]=dis[i][j];
        }
    }
}
```

AC代码：[云剪贴板](https://www.luogu.com.cn/paste/u07nvbw4)

#### 四、优缺点

##### 优点

代码简单，珂以直接当作模板背下来

##### 缺点

 $O(n^3)$ ，大部分题都没戏

同时因为使用邻接表存图，所以内存也堪忧
