---
title: WebGL 流体仿真交互式演示
date: 2025-10-02 15:00:00
tags: 
  - WebGL
  - 流体仿真
  - 交互式演示
  - JavaScript
  - Shader
categories: 技术解析
excerpt: 在浏览器中体验实时流体仿真效果，了解 WebGL 如何实现高性能的 GPU 计算。
---

## 在线演示

本页面集合了多个优质的 WebGL 流体仿真演示，你可以直接在浏览器中交互体验。

<!-- more -->

---

## 🌊 演示一：墨水扩散效果

这是 Tom Larkworthy 实现的经典墨水扩散模拟，展示了流体的**扩散（Diffusion）**和**平流（Advection）**特性。

<div style="text-align: center; margin: 2em 0; padding: 2em; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; box-shadow: 0 8px 16px rgba(0,0,0,0.2);">
  <a href="https://observablehq.com/@tomlarkworthy/ink" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 15px 40px; background: white; color: #667eea; text-decoration: none; border-radius: 8px; font-size: 18px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.3); transition: all 0.3s;">
    🎨 打开 Observable 交互式笔记本
  </a>
  <p style="color: white; margin-top: 1em; font-size: 14px;">在新标签页中体验完整的墨水扩散效果</p>
</div>

**技术要点：**
- 使用 WebGL Compute Shader 实现 GPU 加速
- 实现了 Stable Fluids 算法的核心步骤
- 支持鼠标/触摸交互输入

**操作提示：**
- 🖱️ 按住鼠标左键拖动：添加速度扰动
- 🎨 按住鼠标右键拖动：添加染料
- 🔄 刷新页面：重置场景

> 💡 **提示**：Observable 笔记本提供了源码查看和实时编辑功能，你可以直接修改参数看效果！

---

## 💻 本地实现：完整流体仿真演示

我创建了一个完整的交互式流体仿真页面，使用 Canvas 2D API 实现。

### 🚀 [点击这里打开完整演示页面](/fluid-demo.html)

**演示特色：**
- ✅ 完整的 Stable Fluids 算法实现
- ✅ 支持鼠标和触摸交互
- ✅ 实时 FPS 显示
- ✅ 彩色渐变染料效果
- ✅ 扩散 + 衰减 + 边界处理
- ✅ 响应式设计，支持移动端

**快速预览：**

<div style="text-align: center; margin: 2em 0;">
  <a href="/fluid-demo.html" target="_blank" style="display: inline-block; padding: 15px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 8px; font-size: 18px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.3); transition: transform 0.3s;">
    🌊 打开完整演示
  </a>
</div>

![流体仿真演示预览](/img/fluid-demo-preview.jpg)

**核心功能：**
- ✅ **64x64 网格分辨率**，4096 个模拟单元
- ✅ **扩散算法**：4 次 Jacobi 迭代
- ✅ **彩色渐变**：基于密度的 HSL 色彩映射
- ✅ **实时统计**：FPS 计数器和帧数追踪
- ✅ **完整源码**：约 200 行注释清晰的 JavaScript

---

## 📚 进阶学习资源

### WebGL 流体仿真教程
1. **[WebGL Fluid Simulation](https://github.com/PavelDoGreat/WebGL-Fluid-Simulation)**  
   开源的高性能 WebGL 流体仿真库
   
2. **[GPU Gems Chapter 38](https://developer.nvidia.com/gpugems/gpugems/part-vi-beyond-triangles/chapter-38-fast-fluid-dynamics-simulation-gpu)**  
   NVIDIA 官方 GPU 流体仿真指南

3. **[Shader Toy 流体模拟合集](https://www.shadertoy.com/results?query=fluid)**  
   社区贡献的各种流体效果实现

### Observable 笔记本推荐
- [Tom Larkworthy's Notebooks](https://observablehq.com/@tomlarkworthy) - WebGL 大师的作品集
- [Ricky Reusser's Graphics](https://observablehq.com/@rreusser) - 物理模拟专家
- [Mike Bostock's Visualizations](https://observablehq.com/@mbostock) - D3.js 作者的可视化作品

---

## 🛠️ 技术栈

本页面使用的技术：
- **WebGL 2.0**：GPU 加速图形渲染
- **GLSL**：着色器编程语言
- **JavaScript ES6+**：交互逻辑控制
- **Observable Runtime**：嵌入交互式笔记本

---

## 💡 实现提示

如果你想在自己的项目中集成流体仿真：

1. **使用现成的库**（推荐新手）：
   - [WebGL-Fluid-Simulation](https://github.com/PavelDoGreat/WebGL-Fluid-Simulation)
   - [Three.js](https://threejs.org/) + Shader Material

2. **从零实现**（适合学习）：
   - 参考 [Jos Stam 的论文](https://www.researchgate.net/publication/2560062_Real-Time_Fluid_Dynamics_for_Games)
   - 学习 [WebGL Fundamentals](https://webglfundamentals.org/)
   - 实现 Compute Shader（需要 WebGL 2.0）

3. **嵌入 Observable**（最快方式）：
   ```html
   <iframe width="100%" height="600" frameborder="0"
     src="https://observablehq.com/embed/@用户名/笔记本名?cells=单元格名"></iframe>
   ```

---

## 🎯 性能优化建议

- **分辨率**：64x64 到 256x256 网格是移动端的最佳平衡
- **迭代次数**：Jacobi 求解器 20-30 次足够实时应用
- **纹理格式**：使用 `RGBA16F` 或 `RGBA32F` 提高精度
- **双缓冲**：Ping-Pong 两个 Framebuffer 避免读写冲突

---

*本页面所有演示均可在现代浏览器中运行，推荐使用 Chrome/Edge/Firefox 获得最佳体验。*
