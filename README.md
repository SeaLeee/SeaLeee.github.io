# SeaLeee's Blog

基于 Hexo 框架和 Fluid 主题构建的个人博客。

## 博客地址

🌐 https://SeaLeee.github.io

## 分支说明

本仓库采用双分支管理：

- **`source` 分支**：博客源码（Markdown 文章、配置文件、主题等）← 当前分支
- **`main` 分支**：生成的静态网站文件（由 `hexo deploy` 自动推送）

> 💡 **提示**：克隆仓库时请使用 `source` 分支

## 技术栈

- **框架**: [Hexo](https://hexo.io/)
- **主题**: [Fluid](https://github.com/fluid-dev/hexo-theme-fluid)
- **部署**: GitHub Pages

## 本地运行

### 克隆仓库

```bash
# 克隆 source 分支（博客源码）
git clone -b source https://github.com/SeaLeee/SeaLeee.github.io.git
cd SeaLeee.github.io
```

### 环境要求

- Node.js >= 12.0
- Git

### 安装依赖

```bash
cd new-blog
npm install
```

### 本地预览

```bash
hexo server
```

访问 http://localhost:4000

### 新建文章

```bash
hexo new "文章标题"
```

文章会生成在 `source/_posts/` 目录下。

### 发布流程

1. **编写文章**：在 `source/_posts/` 目录编写 Markdown 文章
2. **本地预览**：`hexo server` 预览效果
3. **生成静态文件**：`hexo generate` 或 `hexo g`
4. **部署到 GitHub Pages**：`hexo deploy` 或 `hexo d`
5. **提交源码到 source 分支**：
   ```bash
   git add .
   git commit -m "📝 添加新文章：文章标题"
   git push origin source
   ```

### 快捷命令

```bash
# 清理缓存
hexo clean

# 生成静态文件
hexo generate  # 或 hexo g

# 部署到 GitHub Pages（推送到 main 分支）
hexo deploy    # 或 hexo d

# 一键生成并部署
hexo clean && hexo g -d
```

## 目录结构

```
new-blog/
├── _config.yml          # 博客配置文件
├── _config.fluid.yml    # Fluid 主题配置文件
├── package.json         # 项目依赖
├── scaffolds/           # 文章模板
├── source/              # 源文件
│   ├── _posts/         # 文章目录
│   └── about/          # 关于页面
└── themes/              # 主题目录
```

## License

MIT
