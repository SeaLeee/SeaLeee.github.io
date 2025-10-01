# SeaLeee's Blog

基于 Hexo 框架和 Fluid 主题构建的个人博客。

## 博客地址

🌐 https://SeaLeee.github.io

## 技术栈

- **框架**: [Hexo](https://hexo.io/)
- **主题**: [Fluid](https://github.com/fluid-dev/hexo-theme-fluid)
- **部署**: GitHub Pages

## 本地运行

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

### 生成静态文件

```bash
hexo generate
```

### 部署到 GitHub Pages

```bash
hexo deploy
```

或者一键生成并部署：

```bash
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
