---
title: "初始化记录：Markdown、LaTeX 与 AIRIS 主题"
description: "这是一篇示例文章，用来验证 Markdown 排版、代码块和数学公式可以在博客中正常显示。"
pubDate: 2026-03-17
updatedDate: 2026-03-17
draft: false
tags:
  - setup
  - markdown
  - latex
classification: 3
---

这篇文章的目的很直接：确认你以后只写 Markdown，也能得到一篇样式完整、可部署的博客文章。

## Markdown 正文

Astro 原生支持 Markdown 内容，适合写日志、教程、读书笔记和研究记录。你只需要维护 frontmatter 和正文，站点会在构建时把它变成静态 HTML 页面。

### 列表

- 项目结构清晰
- 版本管理方便
- 发布只需要 `git push`

### 代码块

```ts
type Signal = {
  title: string;
  status: 'draft' | 'published';
};

const signal: Signal = {
  title: 'AIRIS',
  status: 'published',
};

console.log(signal);
```

## LaTeX 公式

行内公式示例：$e^{i\pi} + 1 = 0$。

块级公式示例：

$$
f(x) = \sum_{n=0}^{\infty}\frac{x^n}{n!}
$$

也可以写矩阵：

$$
A =
\begin{bmatrix}
1 & 2 \\
3 & 4
\end{bmatrix}
$$

## 写作建议

如果你之后主要写技术内容，我建议保持这个工作流不变：

1. 每篇文章一个 `.md` 文件。
2. 在 frontmatter 中写标题、简介、日期、标签。
3. 正文里直接写 Markdown 和 LaTeX。
4. 提交到 GitHub 后，让 Actions 自动发布。

这样维护成本最低，也最稳定。
