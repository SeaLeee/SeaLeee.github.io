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

## 五、Git 分支管理策略

### 5.1 双分支管理（推荐）

为了更好地管理博客源码和部署文件，建议采用双分支管理：

- **`source` 分支**：存放博客源码（Markdown 文章、配置文件、主题等）
- **`main` 分支**：存放生成的静态网站文件（由 `hexo deploy` 自动推送）

### 5.2 创建 source 分支

```powershell
# 在博客根目录（不是 new-blog 目录）
git init
git add .
git commit -m "🎉 初始化博客项目"

# 创建并切换到 source 分支
git checkout -b source

# 推送到远程仓库
git remote add origin https://github.com/你的用户名/你的用户名.github.io.git
git push -u origin source
```

### 5.3 分支结构说明

```
source 分支（博客源码）
  ├── .gitignore
  ├── README.md
  └── new-blog/
      ├── _config.yml          # 博客配置
      ├── _config.fluid.yml    # 主题配置
      ├── package.json         # 依赖配置
      ├── source/_posts/       # 文章目录 ⭐
      └── themes/              # 主题目录

main 分支（静态网站）
  └── public/                  # hexo deploy 自动推送
      ├── index.html
      ├── css/
      ├── js/
      └── ...
```

## 六、日常写作和发布流程

### 6.1 完整工作流程

```powershell
# 步骤 1：创建新文章
hexo new "文章标题"

# 步骤 2：编辑文章
# 在 source/_posts/ 目录下编写 Markdown 文章

# 步骤 3：本地预览
hexo server
# 访问 http://localhost:4000 预览效果

# 步骤 4：生成并部署到网站（推送到 main 分支）
hexo clean && hexo g -d

# 步骤 5：提交源码到 source 分支
git add .
git commit -m "📝 新增文章：文章标题"
git push origin source
```

### 6.2 文章格式模板

创建文章后，编辑 Markdown 文件：

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

这里是文章摘要，会显示在首页。

<!-- more -->

## 一、正文标题

这里是文章正文内容...

### 1.1 子标题

段落内容...

## 二、代码示例

```python
def hello():
    print("Hello, World!")
```

## 三、图片插入

![图片描述](/img/example.jpg)
```

### 6.3 常用命令速查

```powershell
# 创建新文章
hexo new "文章标题"

# 创建新页面
hexo new page "页面名称"

# 本地预览（热重载）
hexo server
# 或简写
hexo s

# 清理缓存
hexo clean

# 生成静态文件
hexo generate
# 或简写
hexo g

# 部署到 GitHub Pages
hexo deploy
# 或简写
hexo d

# 一键清理、生成、部署
hexo clean && hexo g -d

# 生成文章草稿
hexo new draft "草稿标题"

# 发布草稿
hexo publish "草稿标题"
```

### 6.4 在多台电脑上工作

**首次克隆仓库：**

```powershell
# 克隆 source 分支（博客源码）
git clone -b source https://github.com/你的用户名/你的用户名.github.io.git
cd 你的用户名.github.io/new-blog

# 安装依赖
npm install

# 现在可以开始写作了
hexo new "新文章"
```

**每次开始写作前：**

```powershell
# 拉取最新的源码
git pull origin source

# 然后开始写作
hexo new "文章标题"
```

**写作完成后：**

```powershell
# 部署到网站
hexo clean && hexo g -d

# 提交源码
git add .
git commit -m "📝 更新文章"
git push origin source
```

## 七、Fluid 主题配置

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

## 八、常见问题

### 7.1 命令找不到

如果提示 `hexo` 或 `npm` 命令找不到，检查环境变量配置。

### 7.2 部署失败

- 确认 GitHub 仓库地址正确
- 确认 Git 已正确配置用户信息
- 检查网络连接

### 8.3 主题样式不显示

运行 `hexo clean` 清理缓存后重新生成。

### 8.4 多台电脑同步问题

确保：
- 两台电脑都克隆了 `source` 分支
- 每次开始前先 `git pull origin source`
- 写作完成后记得 `git push origin source`

## 九、总结

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
