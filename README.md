# AIRIS Blog

这是一个已经接入 AIRIS 视觉语言的个人博客骨架，目标是让你只维护 Markdown 内容，并通过 GitHub Pages 自动发布。

## 这套方案为什么适合你

- 你只需要写 `Markdown + LaTeX`
- 页面由 Astro 在构建时转成静态 HTML
- 数学公式由 `remark-math + rehype-katex` 在构建时渲染，不需要你手动转图片
- 部署由 GitHub Actions 自动完成，适合长期写作

## 目录结构

```text
src/
  content/
    posts/
      _template.md
      getting-started.md
  layouts/
  pages/
  styles/
.github/
  workflows/
    deploy.yml
```

## 你以后如何写文章

1. 复制 `src/content/posts/_template.md`
2. 改文件名，例如 `my-first-post.md`
3. 修改 frontmatter
4. 写正文
5. 把 `draft: true` 改成 `draft: false`
6. 提交并推送到 GitHub

### frontmatter 示例

```yaml
---
title: "文章标题"
description: "一句话摘要"
pubDate: 2026-03-17
updatedDate: 2026-03-17
draft: false
tags:
  - math
  - notes
classification: 3
---
```

### LaTeX 写法

行内公式：

```md
$E = mc^2$
```

块级公式：

```md
$$
\int_0^1 x^2 \, dx = \frac{1}{3}
$$
```

## 从零开始，本地启动

### 1. 安装环境

- 安装 Node.js 20 LTS 或更高版本
- 打开当前项目目录

### 2. 安装依赖

```powershell
npm install
```

### 3. 启动预览

```powershell
npm run dev
```

启动后，终端会给你一个本地地址，通常是 `http://localhost:4321/`。

## 从零开始，发布到 GitHub Pages

最简单的做法：

- 你的 GitHub 用户名假设是 `yourname`
- 把仓库名直接建成 `yourname.github.io`

这样可以避免处理 `base` 路径问题。

### 1. 在 GitHub 创建仓库

1. 登录 GitHub
2. 点击右上角 `+` -> `New repository`
3. 仓库名填写：`<你的 GitHub 用户名>.github.io`
4. 选择 `Public`
5. 不要勾选自动生成 `README`、`.gitignore` 或 license
6. 点击 `Create repository`

### 2. 初始化 Git 并推送

在当前目录运行：

```powershell
git init
git add .
git commit -m "Initial AIRIS blog"
git branch -M main
git remote add origin https://github.com/<你的用户名>/<你的用户名>.github.io.git
git push -u origin main
```

### 3. 在 GitHub 打开 Pages

1. 进入刚创建的仓库
2. 打开 `Settings`
3. 左侧找到 `Pages`
4. 在 `Build and deployment` -> `Source` 里选择 `GitHub Actions`

完成后，每次你往 `main` 分支推送内容，`.github/workflows/deploy.yml` 就会自动构建和发布。

### 4. 等待第一次部署完成

1. 打开仓库顶部的 `Actions`
2. 查看 `Deploy to GitHub Pages` 工作流
3. 当 `build` 和 `deploy` 都通过后，访问：

```text
https://<你的用户名>.github.io/
```

## 如果你不想用 `<username>.github.io` 作为仓库名

如果仓库名是普通项目名，例如 `blog`，那么 GitHub Pages 地址会变成：

```text
https://<你的用户名>.github.io/blog/
```

这种情况下，你需要在 `astro.config.mjs` 中补一个 `base`：

```js
export default defineConfig({
  site: 'https://<你的用户名>.github.io',
  base: '/blog',
});
```

如果你是第一次搭站，建议先不要这么做，先用 `<username>.github.io` 跑通整条链路。

## 自定义域名

等 GitHub 地址跑通后，再做自定义域名最稳。

1. 在 `public/` 下新建 `CNAME`
2. 文件里只写一行你的域名，例如：

```text
blog.example.com
```

3. 去 GitHub 仓库 `Settings` -> `Pages` 里绑定这个域名
4. 到你的域名服务商配置 DNS

## 当前工作流总结

```text
写 Markdown
-> 本地预览
-> git commit
-> git push
-> GitHub Actions 自动构建
-> GitHub Pages 自动发布
```
