---
title: Hexo 博客双分支管理完全指南
date: 2025-10-01 15:45:00
tags:
  - Hexo
  - Git
  - 双分支管理
  - GitHub Pages
  - 教程
categories:
  - 教程
---

## 📖 前言

本文是 Hexo 博客双分支管理的完全指南，从概念到实战，从理论到操作，帮你彻底掌握 source 和 main 分支的管理策略。

**适合人群**：
- 🆕 刚接触 Hexo 博客的新手
- 🤔 对双分支管理感到困惑的用户
- 💻 需要在多台电脑上同步博客的作者

<!-- more -->

---

## 第一部分：概念理解

### 🤔 为什么需要两个分支？

#### 问题背景

当你使用 Hexo 写博客时，会产生两类文件：

1. **源文件**（你写的）：
   - Markdown 文章（`*.md`）
   - 配置文件（`_config.yml`）
   - 主题文件
   - 插件配置
   
2. **生成文件**（Hexo 自动生成的）：
   - HTML 页面
   - CSS 样式
   - JavaScript 脚本
   - 图片等静态资源

**问题来了**：
- GitHub Pages 需要的是生成的 HTML 文件才能展示网站
- 但你想保存的是 Markdown 源文件，以便修改和同步

**如果只用一个分支**：
- 放源文件？→ 网站无法显示
- 放生成文件？→ 源文件丢失，无法编辑

**解决方案**：用两个分支！

---

### 📊 双分支结构图解

```
你的 GitHub 仓库: SeaLeee.github.io
│
├─── source 分支 (博客源码) 👈 你主要工作的地方
│    │
│    ├── README.md
│    ├── .gitignore
│    └── new-blog/
│         ├── _config.yml          ← 博客配置
│         ├── _config.fluid.yml    ← 主题配置
│         ├── package.json         ← 依赖管理
│         ├── source/
│         │   └── _posts/          ← 📝 你的 Markdown 文章
│         │       ├── 文章1.md
│         │       ├── 文章2.md
│         │       └── 文章3.md
│         └── themes/              ← 主题文件
│
└─── main 分支 (静态网站) 👈 hexo deploy 自动管理
     │
     ├── index.html                ← 网站首页
     ├── 2025/10/01/文章1/
     │   └── index.html            ← 文章1 的 HTML
     ├── css/                      ← 样式文件
     ├── js/                       ← 脚本文件
     └── img/                      ← 图片资源
```

---

### 🎯 两个分支的职责

#### 📂 source 分支（源码分支）

**作用**：保存你的原始工作内容

**包含的内容**：
- ✅ Markdown 文章原文
- ✅ 博客配置文件
- ✅ 主题配置
- ✅ 插件列表
- ✅ 自定义页面

**谁使用**：
- 👨‍💻 **你** - 用来编辑文章
- 💻 **多台电脑** - 用来同步工作
- 📖 **查看历史** - 追溯文章修改记录

**特点**：
- 文件小（只有文本和配置）
- 可读性强（Markdown 格式）
- 方便版本控制

#### 🌐 main 分支（部署分支）

**作用**：让 GitHub Pages 展示你的网站

**包含的内容**：
- ✅ 生成的 HTML 页面
- ✅ 编译后的 CSS 样式
- ✅ JavaScript 文件
- ✅ 优化后的图片

**谁使用**：
- 🌍 **GitHub Pages** - 读取这些文件展示网站
- 👀 **访客** - 访问你的博客时看到的就是这些文件

**特点**：
- 文件多（每篇文章生成多个文件）
- 都是编译后的代码
- 完全自动化管理（你不需要手动编辑）

---

### 💡 类比：理解双分支

#### 类比1：写书和出版

想象你在写一本书：

| 阶段 | 对应分支 | 内容 |
|------|---------|------|
| 📝 **手稿阶段** | source 分支 | 你的 Word 文档、草稿、笔记 |
| 📚 **出版阶段** | main 分支 | 印刷成书的 PDF，读者看的版本 |

- **source 分支** = 你的工作台，随时修改
- **main 分支** = 书店的成品，给读者看

#### 类比2：开餐厅

- **source 分支** = 厨房（你的工作区）
  - 📝 菜谱（Markdown 文章）
  - 🥗 食材（配置文件）
  - 👨‍🍳 你可以随时调整菜谱

- **main 分支** = 餐桌（展示区）
  - 🍽️ 成品菜肴（HTML 网站）
  - 🎨 摆盘装饰（CSS 样式）
  - 👥 顾客直接享用（访客访问）

- **hexo deploy** = 服务员
  - 🚶‍♂️ 自动从厨房端到餐桌
  - ⚡ 你不需要自己端菜

---

## 第二部分：实战操作

### 🔄 完整工作流程（超详细）

#### 场景：你要写一篇新文章

##### 步骤 1：创建文章（在本地）

```powershell
# 在 new-blog 目录
hexo new "我的第一篇技术博客"
```

**发生了什么**：
- Hexo 在 `source/_posts/` 创建了 `我的第一篇技术博客.md`
- 这个文件只在你电脑上，还没上传

##### 步骤 2：编写文章（在本地）

用 VS Code 打开 `我的第一篇技术博客.md`，写内容：

```markdown
---
title: 我的第一篇技术博客
date: 2025-10-01
tags: [技术, 学习]
---

今天学习了 Hexo...
```

**此时状态**：
```
你的电脑 💻
  └── source/_posts/我的第一篇技术博客.md ✅ 新建

GitHub source 分支 ☁️
  └── (还没有这个文件) ❌

GitHub main 分支 ☁️
  └── (还没有这个文章的网页) ❌
```

##### 步骤 3：本地预览（在本地）

```powershell
hexo server
```

访问 `http://localhost:4000` 看效果

**发生了什么**：
- Hexo 临时生成 HTML，只在你电脑上预览
- 此时还没有任何东西上传到 GitHub

##### 步骤 4：部署到网站（推送到 main 分支）

```powershell
hexo clean && hexo generate && hexo deploy
```

**详细过程**：

1. `hexo clean` - 清理旧文件
2. `hexo generate` - 把 Markdown 转成 HTML
   ```
   我的第一篇技术博客.md 
   ↓ (Hexo 处理)
   2025/10/01/我的第一篇技术博客/index.html
   ```
3. `hexo deploy` - 自动推送到 GitHub 的 **main 分支**

**此时状态**：
```
你的电脑 💻
  ├── source/_posts/我的第一篇技术博客.md ✅ 源文件
  └── public/2025/10/01/.../index.html ✅ 生成的网页

GitHub source 分支 ☁️
  └── (还没有源文件) ❌

GitHub main 分支 ☁️
  └── 2025/10/01/.../index.html ✅ 已部署！
```

**现在访客可以看到你的文章了**！🎉
访问：`https://SeaLeee.github.io`

##### 步骤 5：保存源文件（推送到 source 分支）

```powershell
# 回到仓库根目录（不是 new-blog）
cd ..

# 查看修改
git status

# 添加文件
git add .

# 提交
git commit -m "📝 新增文章：我的第一篇技术博客"

# 推送到 source 分支
git push origin source
```

**此时状态**：
```
你的电脑 💻
  ├── source/_posts/我的第一篇技术博客.md ✅
  └── public/2025/10/01/.../index.html ✅

GitHub source 分支 ☁️
  └── source/_posts/我的第一篇技术博客.md ✅ 源文件已保存！

GitHub main 分支 ☁️
  └── 2025/10/01/.../index.html ✅ 网站已部署！
```

**完美！** 两个分支都更新了！✨

---

### 🎯 一张图看懂工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                      你的工作流程                             │
└─────────────────────────────────────────────────────────────┘

1️⃣ 写文章                    2️⃣ 部署网站                 3️⃣ 保存源码
   ↓                            ↓                           ↓
hexo new "文章"             hexo clean                  git add .
   ↓                       hexo generate                git commit
编辑 .md 文件               hexo deploy                 git push origin source
   ↓                            ↓                           ↓
hexo server (预览)          推送到 main 分支             推送到 source 分支


┌─────────────────────────────────────────────────────────────┐
│                     关键区别对比                              │
└─────────────────────────────────────────────────────────────┘

特性          │  source 分支          │  main 分支
─────────────┼──────────────────────┼───────────────────
文件类型      │  Markdown、YAML、JSON │  HTML、CSS、JS
文件大小      │  小（几十 KB）        │  大（几百 KB）
可读性        │  ★★★★★（人类可读）   │  ★★☆☆☆（机器代码）
谁使用        │  你（编辑文章）       │  GitHub Pages（展示网站）
更新方式      │  手动 git push        │  hexo deploy 自动
需要克隆吗    │  ✅ 需要（写作必备）  │  ❌ 不需要（自动生成）
```

---

### 📝 文章格式模板

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
\```

## 三、图片插入

![图片描述](/img/example.jpg)
```

---

### 💻 在多台电脑上工作

#### 电脑 A（第一台）- 首次设置

```powershell
# 1. 克隆 source 分支
git clone -b source https://github.com/SeaLeee/SeaLeee.github.io.git
cd SeaLeee.github.io/new-blog

# 2. 安装依赖
npm install

# 3. 写文章
hexo new "文章1"
# 编辑、部署
hexo clean && hexo g -d

# 4. 提交源码
cd ..
git add .
git commit -m "新增文章1"
git push origin source
```

#### 电脑 B（第二台）- 首次使用

```powershell
# 1. 克隆 source 分支（源码）
git clone -b source https://github.com/SeaLeee/SeaLeee.github.io.git
cd SeaLeee.github.io/new-blog

# 2. 安装依赖
npm install

# 3. 继续写作
hexo new "文章2"
# 编辑、部署
hexo clean && hexo g -d

# 4. 提交源码
cd ..
git add .
git commit -m "新增文章2"
git push origin source
```

#### 电脑 A - 第二天继续

```powershell
# 同步最新源码
git pull origin source

# 现在你有文章2了！
hexo new "文章3"
```

**关键**：
- 📥 每次开始前：`git pull origin source`（拉取最新）
- 📤 每次写完后：`git push origin source`（保存到云端）

---

## 第三部分：常用命令

### 📋 命令速查表

#### 日常发布流程

```powershell
# === 在 new-blog 目录 ===

# 1. 创建文章
hexo new "文章标题"

# 2. 编辑文章
# (用 VS Code 编辑 source/_posts/文章标题.md)

# 3. 本地预览
hexo server

# 4. 部署到网站（自动推送到 main 分支）
hexo clean && hexo g -d

# === 切换到仓库根目录 ===
cd ..

# 5. 保存源码到 source 分支
git add .
git commit -m "📝 新增文章：文章标题"
git push origin source
```

#### 常用 Hexo 命令

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

#### 分支管理命令

```powershell
# 查看当前分支
git branch

# 查看所有分支
git branch -a

# 查看分支历史
git log --oneline --all --graph

# 同步最新代码
git pull origin source

# 提交并推送
git add .
git commit -m "提交说明"
git push origin source
```

---

## 第四部分：常见问题

### ❓ 疑问解答

#### Q1: 为什么不能把源文件和生成文件放一起？

**A**: 可以，但会很乱：
- ❌ GitHub Pages 会尝试读取 `.md` 文件（报错）
- ❌ 仓库体积大（源文件 + 生成文件重复）
- ❌ 版本混乱（哪些该提交？哪些该忽略？）

#### Q2: 我能只用一个分支吗？

**A**: 可以，有两种方案：

**方案 A**：用两个仓库
```
仓库1: blog-source (源文件)
仓库2: username.github.io (生成文件)
```
缺点：管理两个仓库麻烦

**方案 B**：只部署，不保存源文件
缺点：❌ 源文件丢失了，换电脑无法继续写作

**推荐**：还是用双分支，最方便！

#### Q3: 哪个是默认分支？

**A**: 
- GitHub Pages 读取 **main 分支**
- 你克隆时应该用 **source 分支**：
  ```powershell
  git clone -b source https://github.com/SeaLeee/SeaLeee.github.io.git
  ```

#### Q4: 如果我忘记推送 source 分支会怎样？

**A**: 
- ✅ 网站依然正常（main 分支已更新）
- ❌ 但源文件没保存到云端
- ❌ 换电脑或重装系统后，源文件丢失

**建议**：养成习惯，每次发布后都推送 source！

#### Q5: hexo deploy 做了什么？

**A**: `hexo-deployer-git` 插件内部执行了：

```javascript
1. 切换到 .deploy_git 文件夹
2. git add .
3. git commit -m "Site updated"
4. git push origin main
5. 切换回原来的分支
```

你看不到这个过程，但它确实发生了！

---

### 🔧 故障排查

#### 问题：网站没更新

**解决方案**：
- 检查 `hexo deploy` 有没有报错
- 访问 GitHub 查看 main 分支的提交时间
- 等待几分钟（GitHub Pages 需要构建时间）
- 清除浏览器缓存

#### 问题：换电脑后找不到文章源文件

**解决方案**：
- 检查有没有 push 到 source 分支
- `git clone -b source` 下载源码
- 如果忘记推送，源文件就丢失了

#### 问题：不知道当前在哪个分支

**解决方案**：
- 运行 `git branch` 查看
- 应该在 source 分支（`* source`）
- 如果在 main 分支，切换回来：`git checkout source`

#### 问题：命令找不到

**解决方案**：
- 如果提示 `hexo` 或 `npm` 命令找不到，检查环境变量配置
- Windows: 添加到 PATH
  ```powershell
  $env:PATH += ";C:\Program Files\nodejs"
  $env:PATH += ";C:\Users\$env:USERNAME\AppData\Roaming\npm"
  ```

#### 问题：主题样式不显示

**解决方案**：
- 运行 `hexo clean` 清理缓存后重新生成
- 检查 `_config.yml` 中的 `theme` 配置
- 确保主题文件夹存在

---

## 第五部分：最佳实践

### ✅ 推荐做法

1. **每天开始前**
   ```powershell
   git pull origin source  # 同步最新版本
   ```

2. **写完文章后**
   ```powershell
   # 部署到网站
   hexo clean && hexo g -d
   
   # 保存源码
   git add .
   git commit -m "📝 新增文章：文章标题"
   git push origin source
   ```

3. **定期备份**
   - 每周检查 source 分支是否最新
   - 重要文章写完立即推送

4. **使用有意义的提交信息**
   ```powershell
   # ✅ 好的提交信息
   git commit -m "📝 新增文章：双分支管理完全指南"
   git commit -m "🎨 更新主题配置"
   git commit -m "🐛 修复代码高亮问题"
   
   # ❌ 不好的提交信息
   git commit -m "update"
   git commit -m "fix"
   ```

### ❌ 不要做的事

1. **不要手动修改 main 分支**
   - main 分支会被 `hexo deploy` 覆盖
   - 所有修改都会丢失

2. **不要在 main 分支工作**
   - 始终在 source 分支工作
   - main 分支只是部署用

3. **不要忘记 push source 分支**
   - 网站部署了但源码没保存
   - 换电脑后无法继续写作

4. **不要克隆 main 分支**
   - main 分支只有 HTML，无法编辑
   - 应该克隆 source 分支

---

## 第六部分：实战练习

### 🎓 毕业测试

#### 请回答以下问题：

1. 你写的 Markdown 文章保存在哪个分支？
   - [ ] main
   - [x] source

2. 访客访问你的网站，GitHub Pages 读取哪个分支？
   - [x] main
   - [ ] source

3. `hexo deploy` 会更新哪个分支？
   - [x] main
   - [ ] source

4. 换电脑后，应该克隆哪个分支？
   - [ ] main
   - [x] source

5. 写完文章后，需要执行几次 push？
   - [ ] 1 次（hexo deploy 自动 push）
   - [x] 2 次（hexo deploy + git push source）

#### 答案解析：

1. ✅ source - Markdown 源文件
2. ✅ main - HTML 网站文件
3. ✅ main - hexo deploy 自动推送
4. ✅ source - 需要源文件才能继续写作
5. ✅ 2 次 - main 自动，source 手动

---

### 🚀 实战练习

#### 练习 1：完整流程一遍

```powershell
# === 写文章 ===
cd new-blog
hexo new "测试文章"
# 编辑 source/_posts/测试文章.md

# === 发布到网站 ===
hexo clean && hexo g -d
# 现在 main 分支已更新，网站可以看到了

# === 保存源文件 ===
cd ..
git add .
git commit -m "新增测试文章"
git push origin source
# 现在 source 分支也更新了

# === 验证 ===
# 访问 https://SeaLeee.github.io 看网站 ✅
# 访问 GitHub 查看 source 分支 ✅
```

---

## 总结

### 🎯 核心要点

#### 记住这 4 句话

1. **source 分支** = 你的草稿本（Markdown）
2. **main 分支** = 印刷厂的成品（HTML）
3. **hexo deploy** = 自动送去印刷（更新 main）
4. **git push source** = 草稿备份到云盘（更新 source）

#### 每天的工作流程

```
早上：
  git pull origin source         ← 同步最新版本

写作：
  hexo new "文章"                ← 创建
  (编辑 Markdown)                ← 写作
  hexo server                    ← 预览

发布：
  hexo clean && hexo g -d        ← 发布到网站（main 分支）
  git add . && git commit -m "..." && git push origin source
                                  ← 保存源文件（source 分支）
```

#### 记忆口诀

```
source 存源码，main 放网站
写完文章记得，两边都要传
hexo deploy 很智能，main 它自己管
git push source 别忘记，源码安全最重要
```

---

### 📚 参考资源

- [Hexo 官方文档](https://hexo.io/zh-cn/docs/)
- [Fluid 主题文档](https://hexo.fluid-dev.com/docs/)
- [GitHub Pages 文档](https://docs.github.com/cn/pages)
- [Git 官方文档](https://git-scm.com/doc)

---

### 🎉 结语

通过本文，你应该已经完全理解了 Hexo 博客的双分支管理策略。记住：

- ✅ **source 分支** = 你的工作台（编辑区）
- ✅ **main 分支** = 展示橱窗（发布区）
- ✅ 两者分工明确，互不干扰
- ✅ 养成良好习惯，每次都保存源码

现在你可以自信地管理你的 Hexo 博客了！

祝你写作愉快！🎊

> 💡 **提示**：如果你觉得这篇教程有帮助，欢迎 Star ⭐ 我的 [GitHub 仓库](https://github.com/SeaLeee/SeaLeee.github.io)！
