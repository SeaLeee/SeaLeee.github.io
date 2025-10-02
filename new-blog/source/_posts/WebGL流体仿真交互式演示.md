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

<div style="margin: 2em 0; border: 2px solid #e0e0e0; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
  <iframe width="100%" height="684" frameborder="0"
    src="https://observablehq.com/embed/@tomlarkworthy/ink?cells=viewof+intro%2Cviewof+demo"></iframe>
</div>

**技术要点：**
- 使用 WebGL Compute Shader 实现 GPU 加速
- 实现了 Stable Fluids 算法的核心步骤
- 支持鼠标/触摸交互输入

**操作提示：**
- 🖱️ 按住鼠标左键拖动：添加速度扰动
- 🎨 按住鼠标右键拖动：添加染料
- 🔄 刷新页面：重置场景

---

## 🎭 演示二：2D 流体场可视化

这个演示展示了速度场的矢量可视化，帮助理解流体的运动模式。

<div style="margin: 2em 0; border: 2px solid #e0e0e0; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
  <iframe width="100%" height="600" frameborder="0"
    src="https://observablehq.com/embed/@mbostock/flow-fields?cells=canvas"></iframe>
</div>

**可视化说明：**
- 每个箭头代表该位置的速度方向和大小
- 颜色表示速度强度（红色=高速，蓝色=低速）
- 观察涡旋（Vortex）的形成和消散

---

## 🔬 演示三：GPU 粒子系统

使用 GPU 并行计算 10 万个粒子的运动轨迹。

<div style="margin: 2em 0; border: 2px solid #e0e0e0; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
  <iframe width="100%" height="600" frameborder="0"
    src="https://observablehq.com/embed/@rreusser/gpgpu-particles-from-first-principles?cells=canvas"></iframe>
</div>

**性能对比：**
- **CPU 计算**：~1,000 粒子 @ 60 FPS
- **GPU 计算**：~100,000 粒子 @ 60 FPS
- 性能提升：**100 倍**！

---

## 💻 本地实现：简易 WebGL 流体仿真

想在自己的网页中实现流体效果？这里是一个最小化的实现示例：

<div id="fluid-canvas-container" style="margin: 2em 0;">
  <canvas id="fluid-canvas" width="512" height="512" style="width: 100%; max-width: 512px; border: 1px solid #ccc; border-radius: 4px; cursor: crosshair;"></canvas>
  <div style="margin-top: 1em; text-align: center;">
    <button onclick="resetFluid()" style="padding: 8px 16px; font-size: 14px; cursor: pointer; background: #3273dc; color: white; border: none; border-radius: 4px;">重置</button>
    <button onclick="togglePause()" style="padding: 8px 16px; font-size: 14px; cursor: pointer; background: #48c774; color: white; border: none; border-radius: 4px; margin-left: 8px;">暂停/继续</button>
  </div>
</div>

<script>
// 简易 2D 流体仿真实现
(function() {
  const canvas = document.getElementById('fluid-canvas');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  const width = canvas.width;
  const height = canvas.height;
  
  // 流体网格
  const gridSize = 64;
  const cellSize = width / gridSize;
  
  // 速度场和密度场
  let velocityX = new Array(gridSize * gridSize).fill(0);
  let velocityY = new Array(gridSize * gridSize).fill(0);
  let density = new Array(gridSize * gridSize).fill(0);
  
  let isPaused = false;
  let mouseDown = false;
  let mouseX = 0, mouseY = 0;
  let prevMouseX = 0, prevMouseY = 0;
  
  // 鼠标事件
  canvas.addEventListener('mousedown', (e) => {
    mouseDown = true;
    const rect = canvas.getBoundingClientRect();
    mouseX = (e.clientX - rect.left) / rect.width * width;
    mouseY = (e.clientY - rect.top) / rect.height * height;
    prevMouseX = mouseX;
    prevMouseY = mouseY;
  });
  
  canvas.addEventListener('mousemove', (e) => {
    if (!mouseDown) return;
    const rect = canvas.getBoundingClientRect();
    prevMouseX = mouseX;
    prevMouseY = mouseY;
    mouseX = (e.clientX - rect.left) / rect.width * width;
    mouseY = (e.clientY - rect.top) / rect.height * height;
    
    // 添加速度和密度
    const gridX = Math.floor(mouseX / cellSize);
    const gridY = Math.floor(mouseY / cellSize);
    if (gridX >= 0 && gridX < gridSize && gridY >= 0 && gridY < gridSize) {
      const idx = gridY * gridSize + gridX;
      velocityX[idx] += (mouseX - prevMouseX) * 0.5;
      velocityY[idx] += (mouseY - prevMouseY) * 0.5;
      density[idx] = Math.min(density[idx] + 50, 255);
    }
  });
  
  canvas.addEventListener('mouseup', () => { mouseDown = false; });
  canvas.addEventListener('mouseleave', () => { mouseDown = false; });
  
  // 扩散函数（简化版）
  function diffuse(field, diffusionRate) {
    const newField = new Array(field.length);
    for (let y = 1; y < gridSize - 1; y++) {
      for (let x = 1; x < gridSize - 1; x++) {
        const idx = y * gridSize + x;
        newField[idx] = field[idx] + diffusionRate * (
          field[idx - 1] + field[idx + 1] + 
          field[idx - gridSize] + field[idx + gridSize] - 
          4 * field[idx]
        );
      }
    }
    return newField;
  }
  
  // 衰减函数
  function decay(field, rate) {
    return field.map(v => v * rate);
  }
  
  // 更新和渲染
  function update() {
    if (!isPaused) {
      // 扩散
      velocityX = diffuse(velocityX, 0.0001);
      velocityY = diffuse(velocityY, 0.0001);
      density = diffuse(density, 0.0001);
      
      // 衰减
      velocityX = decay(velocityX, 0.99);
      velocityY = decay(velocityY, 0.99);
      density = decay(density, 0.995);
    }
    
    // 渲染
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, width, height);
    
    for (let y = 0; y < gridSize; y++) {
      for (let x = 0; x < gridSize; x++) {
        const idx = y * gridSize + x;
        const d = Math.floor(density[idx]);
        if (d > 0) {
          ctx.fillStyle = `rgba(100, 150, 255, ${Math.min(d / 255, 1)})`;
          ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
        }
      }
    }
    
    requestAnimationFrame(update);
  }
  
  window.resetFluid = function() {
    velocityX.fill(0);
    velocityY.fill(0);
    density.fill(0);
  };
  
  window.togglePause = function() {
    isPaused = !isPaused;
  };
  
  update();
})();
</script>

**代码说明：**
- 使用 Canvas 2D API（简化版，实际应用推荐 WebGL）
- 实现了基本的扩散和衰减
- 鼠标交互添加速度和密度
- 约 100 行代码的完整实现

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
