---
title: 如何创建一个基于Hexo和Fluid主题的GitHub博客
date: 2025-10-01 15:04:56
tags:
  - Hexo
  - GitHub Pages
  - Fluid
  - 博客搭建
categories:
  - 教程
---

## 前言

本文将详细介绍如何从零开始搭建一个基于 Hexo 框架和 Fluid 主题的 GitHub Pages 博客。整个过程包括环境准备、博客初始化、主题配置和部署到 GitHub。

<!-- more -->

## 一、环境准备

### 1.1 安装 Node.js

Hexo 基于 Node.js 运行，首先需要安装 Node.js。

**Windows 用户推荐使用 winget 安装：**

```powershell
winget install OpenJS.NodeJS
```

安装完成后，重启终端或手动添加 Node.js 到环境变量：

```powershell
$env:PATH += ";C:\Program Files\nodejs"
```

验证安装：

```powershell
node --version
npm --version
```

### 1.2 安装 Hexo CLI

使用 npm 全局安装 Hexo 命令行工具：

```powershell
npm install -g hexo-cli
```

添加 npm 全局安装路径到环境变量：

```powershell
$npmPath = npm config get prefix
$env:PATH += ";$npmPath"
```

验证 Hexo 安装：

```powershell
hexo version
```

## 二、创建 Hexo 博客

### 2.1 初始化博客项目

在你想要创建博客的目录下执行：

```powershell
hexo init new-blog
cd new-blog
npm install
```

### 2.2 博客目录结构

初始化完成后，博客目录结构如下：

```
new-blog/
├── _config.yml          # 博客配置文件
├── package.json         # 依赖包配置
├── scaffolds/           # 文章模板
├── source/              # 源文件目录
│   └── _posts/         # 文章目录
└── themes/              # 主题目录
```

### 2.3 本地预览

启动本地开发服务器：

```powershell
hexo server
```

访问 `http://localhost:4000` 即可预览博客。

## 三、安装 Fluid 主题

### 3.1 安装主题包

Fluid 是一个优雅的 Material Design 风格 Hexo 主题。

```powershell
npm install --save hexo-theme-fluid
```

### 3.2 配置主题

编辑博客根目录下的 `_config.yml`，修改主题配置：

```yaml
theme: fluid
```

同时建议修改以下基本配置：

```yaml
# 网站信息
title: 你的博客标题
subtitle: 副标题
description: 博客描述
author: 你的名字
language: zh-CN
timezone: Asia/Shanghai

# URL
url: https://你的用户名.github.io
```

### 3.3 创建主题配置文件

复制主题配置文件到博客根目录：

```powershell
Copy-Item node_modules\hexo-theme-fluid\_config.yml _config.fluid.yml
```

这样可以在 `_config.fluid.yml` 中自定义主题配置，而不影响主题源文件。

### 3.4 重新生成博客

```powershell
hexo clean
hexo generate
hexo server
```

现在访问 `http://localhost:4000`，你会看到全新的 Fluid 主题界面！

## 四、部署到 GitHub Pages

### 4.1 安装部署插件

```powershell
npm install hexo-deployer-git --save
```

### 4.2 配置部署参数

编辑 `_config.yml`，在文件末尾配置部署信息：

```yaml
deploy:
  type: git
  repo: https://github.com/你的用户名/你的用户名.github.io.git
  branch: main
```

### 4.3 配置 Git

确保已配置 Git 用户信息：

```powershell
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱"
```

### 4.4 部署博客

执行以下命令部署到 GitHub：

```powershell
hexo clean
hexo generate
hexo deploy
```

或使用简写命令：

```powershell
hexo clean && hexo g -d
```

### 4.5 配置 GitHub Pages

1. 访问你的 GitHub 仓库设置页面
2. 进入 `Settings` > `Pages`
3. 在 **Source** 下选择：
   - Branch: `main`
   - Folder: `/ (root)`
4. 点击 Save 保存

等待几分钟后，访问 `https://你的用户名.github.io` 即可看到部署好的博客！

## 五、日常使用

### 5.1 创建新文章

```powershell
hexo new "文章标题"
```

文章将在 `source/_posts/` 目录下生成。

### 5.2 编写文章

使用 Markdown 格式编写文章，基本格式：

```markdown
---
title: 文章标题
date: 2025-10-01 15:00:00
tags:
  - 标签1
  - 标签2
categories:
  - 分类
---

文章摘要

<!-- more -->

文章正文...
```

### 5.3 预览和部署

```powershell
# 本地预览
hexo server

# 生成静态文件
hexo generate

# 部署到 GitHub
hexo deploy

# 一键生成并部署
hexo g -d
```

## 六、Fluid 主题配置

### 6.1 自定义 Banner

编辑 `_config.fluid.yml`：

```yaml
index:
  banner_img: /img/bg/banner.jpg
  banner_img_height: 100
```

### 6.2 启用评论系统

Fluid 支持多种评论系统（Gitalk、Valine、Disqus 等），在 `_config.fluid.yml` 中配置。

### 6.3 开启本地搜索

```powershell
npm install hexo-generator-search --save
```

在 `_config.fluid.yml` 中启用：

```yaml
search:
  enable: true
```

## 七、常见问题

### 7.1 命令找不到

如果提示 `hexo` 或 `npm` 命令找不到，检查环境变量配置。

### 7.2 部署失败

- 确认 GitHub 仓库地址正确
- 确认 Git 已正确配置用户信息
- 检查网络连接

### 7.3 主题样式不显示

运行 `hexo clean` 清理缓存后重新生成。

## 八、总结

通过以上步骤，我们成功搭建了一个基于 Hexo 和 Fluid 主题的 GitHub Pages 博客。这是一个完全免费、功能强大且美观的博客解决方案。

### 优势

- ✅ **免费托管**：GitHub Pages 免费托管
- ✅ **高度可定制**：丰富的主题和插件
- ✅ **Markdown 写作**：专注内容创作
- ✅ **版本控制**：Git 管理文章版本
- ✅ **性能优秀**：静态网站加载快速

### 参考资源

- [Hexo 官方文档](https://hexo.io/zh-cn/docs/)
- [Fluid 主题文档](https://hexo.fluid-dev.com/docs/)
- [GitHub Pages 文档](https://docs.github.com/cn/pages)

祝你写作愉快！🎉
