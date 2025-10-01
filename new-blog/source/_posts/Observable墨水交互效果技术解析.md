---
title: Observable 墨水交互效果技术深度解析
date: 2025-10-01 16:00:00
updated: 2025-10-01 16:00:00
tags:
  - WebGL
  - 流体仿真
  - 计算机图形学
  - Shader
  - Observable
categories:
  - 技术解析
index_img: https://cdn.jsdelivr.net/gh/fluid-dev/static@master/hexo-theme-fluid/screenshots/index.png
excerpt: 深入解析 Observable 平台上惊艳的墨水交互效果的完整实现原理，从数学公式到 Shader 代码，带你理解流体仿真的核心算法。
---

## 📌 前言

在 [Observable 平台](https://observablehq.com/@tomlarkworthy/ink) 上有一个令人惊艳的墨水交互效果演示，当你用鼠标在画布上滑动时，会产生如同真实墨水在水中扩散的流动效果。这个效果背后是一套完整的 **流体仿真系统**，本文将深入剖析其实现原理。

## 🎯 效果演示

**原始链接**: [https://observablehq.com/@tomlarkworthy/ink](https://observablehq.com/@tomlarkworthy/ink)

**核心特性**:
- ✨ 真实的墨水流动效果
- 🌀 涡流旋转动画
- 🎨 彩色墨水混合
- 💨 速度与密度的耦合仿真
- 🖱️ 流畅的鼠标/触摸交互

---

## 一、整体流程概览

### 🔄 每帧执行流程（60 FPS）

```
┌─────────────────────────────────────────────────────────────┐
│                    每帧执行 (60 FPS)                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  1. 鼠标/触摸交互检测                  │
        │     - 获取位置和速度                   │
        │     - 计算移动方向                     │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  2. Splat (注入)                      │
        │     - velocity_splat (速度注入)        │
        │     - density_splat (密度注入)         │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  3. Curl (涡度计算)                   │
        │     - 计算速度场的旋度                 │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  4. Vorticity (涡度增强) ⭐           │
        │     - 施加涡度增强力                   │
        │     - 保持旋涡结构                     │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  5. Divergence (散度计算)             │
        │     - div = ∂u/∂x + ∂v/∂y            │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  6. Pressure (压力求解)               │
        │     - Jacobi迭代 (20-40次)            │
        │     - 解泊松方程                       │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  7. Gradient Subtract (梯度减法)      │
        │     - v = v - ∇p                      │
        │     - 保持不可压缩性                   │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  8. Advection (平流)                  │
        │     - velocity_advect (速度平流)       │
        │     - density_advect (密度平流)        │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │  9. Display (渲染)                    │
        │     - 显示密度场为颜色                 │
        └───────────────────────────────────────┘
                            ↓
                    循环回到步骤1
```

---

## 二、渲染目标 (RenderTarget) 架构

### 📊 RT 列表和用途

| RT名称 | 格式 | 用途 | 大小 (512x512) |
|--------|------|------|----------------|
| `velocity` + `velocity_temp` | RG16F/32F | 速度场 (u, v) | 512KB |
| `density` + `density_temp` | RGBA8/16F | 密度场 (颜色 RGBA) | 1MB |
| `divergence` | R16F/32F | 散度场 (标量) | 256KB |
| `curl` | R16F/32F | 涡度场 (标量) | 256KB |
| `pressure` + `pressure_temp` | R16F/32F | 压力场 (标量) | 512KB |

**总计**: 9个 RenderTarget，约 **2.5MB** 显存占用

### 🔄 RT 数据流转图

```
                        鼠标输入
                           ↓
        ┌──────────────────────────────────┐
        │  Splat (注入)                    │
        ├──────────────────┬───────────────┤
        │ velocity_temp ← │ ← velocity    │
        │ density_temp  ← │ ← density     │
        └──────────────────┴───────────────┘
                           ↓
        ┌──────────────────────────────────┐
        │  Curl (涡度计算)                 │
        ├──────────────────┬───────────────┤
        │ curl ←           │ ← velocity    │
        └──────────────────┴───────────────┘
                           ↓
        ┌──────────────────────────────────┐
        │  Vorticity (涡度增强)            │
        ├──────────────────┬───────────────┤
        │ velocity_temp ← │ ← velocity     │
        │                 │ ← curl         │
        └──────────────────┴───────────────┘
                           ↓
                    swap(velocity, velocity_temp)
                           ↓
        ┌──────────────────────────────────┐
        │  Divergence (散度计算)           │
        ├──────────────────┬───────────────┤
        │ divergence ←     │ ← velocity    │
        └──────────────────┴───────────────┘
                           ↓
        ┌──────────────────────────────────┐
        │  Pressure (压力求解) x N次       │
        ├──────────────────┬───────────────┤
        │ pressure_temp ← │ ← pressure     │
        │                 │ ← divergence   │
        │  循环迭代        │                │
        │  swap每次迭代    │                │
        └──────────────────┴───────────────┘
                           ↓
        ┌──────────────────────────────────┐
        │  Gradient Subtract (梯度减法)    │
        ├──────────────────┬───────────────┤
        │ velocity_temp ← │ ← velocity     │
        │                 │ ← pressure     │
        └──────────────────┴───────────────┘
                           ↓
                    swap(velocity, velocity_temp)
                           ↓
        ┌──────────────────────────────────┐
        │  Advection (平流)                │
        ├──────────────────┬───────────────┤
        │ velocity_temp ← │ ← velocity     │
        │ density_temp  ← │ ← density      │
        │                 │ ← velocity     │
        └──────────────────┴───────────────┘
                           ↓
            swap(velocity, velocity_temp)
            swap(density, density_temp)
                           ↓
        ┌──────────────────────────────────┐
        │  Display (显示)                  │
        ├──────────────────┬───────────────┤
        │ Screen ←         │ ← density     │
        └──────────────────┴───────────────┘
```

---

## 三、详细 Pass 分析

### Pass 1: Splat (注入)

**功能**: 在鼠标/触摸位置注入速度和密度

```glsl
// Splat Shader 片段
precision highp float;
varying vec2 vUv;
uniform sampler2D uTarget;
uniform float aspectRatio;
uniform vec3 color;
uniform vec2 point;
uniform float radius;

void main () {
  vec2 p = vUv - point.xy;
  p.x *= aspectRatio;
  
  // 高斯函数：距离越近影响越大
  vec3 splat = exp(-dot(p, p) / radius) * color;
  vec3 base = texture2D(uTarget, vUv).xyz;
  
  gl_FragColor = vec4(base + splat, 1.0);
}
```

**关键参数**:
- `splatRadius`: 0.0001 - 0.001 (屏幕空间)
- `splatForce`: 速度乘数
- `color`: 墨水颜色 (反色处理)

---

### Pass 2: Curl (涡度计算)

**功能**: 计算速度场的涡度（旋转程度）

```glsl
// Curl Shader
precision highp float;
varying vec2 vL, vR, vT, vB;
uniform sampler2D uVelocity;

void main () {
  float L = texture2D(uVelocity, vL).y;  // 左边的 v 分量
  float R = texture2D(uVelocity, vR).y;  // 右边的 v 分量
  float T = texture2D(uVelocity, vT).x;  // 上边的 u 分量
  float B = texture2D(uVelocity, vB).x;  // 下边的 u 分量
  
  // 涡度公式: ω = ∂v/∂x - ∂u/∂y
  float vorticity = R - L - T + B;
  
  gl_FragColor = vec4(vorticity, 0.0, 0.0, 1.0);
}
```

**数学公式**:

$$
\omega = \frac{\partial v}{\partial x} - \frac{\partial u}{\partial y}
$$

**离散化**:

$$
\omega \approx \frac{v_{i+1,j} - v_{i-1,j}}{2\Delta x} - \frac{u_{i,j+1} - u_{i,j-1}}{2\Delta y}
$$

---

### Pass 3: Vorticity Confinement (涡度增强) ⭐

**功能**: 增强涡度，这是保持旋涡美感的**核心算法**

```glsl
// Vorticity Confinement Shader
precision highp float;
varying vec2 vUv, vL, vR, vT, vB;
uniform sampler2D uVelocity;
uniform sampler2D uCurl;
uniform float curl;
uniform float dt;

void main () {
  // 1. 获取相邻位置的涡度绝对值
  float L = texture2D(uCurl, vL).x;
  float R = texture2D(uCurl, vR).x;
  float T = texture2D(uCurl, vT).x;
  float B = texture2D(uCurl, vB).x;
  float C = texture2D(uCurl, vUv).x;
  
  // 2. 计算涡度梯度方向
  vec2 force = vec2(abs(T) - abs(B), abs(R) - abs(L));
  force *= 1.0 / (length(force) + 0.00001);  // 归一化
  
  // 3. 施加增强力（垂直于梯度方向）
  force *= curl * C;
  
  // 4. 更新速度
  vec2 velocity = texture2D(uVelocity, vUv).xy;
  velocity += force * dt;
  
  gl_FragColor = vec4(velocity, 0.0, 1.0);
}
```

**关键参数**:
- `curl`: 10 - 40 (典型值: 30)
- `dt`: 0.016 (60fps)

**物理意义**: 在涡度高的地方施加垂直于梯度的力，保持和增强旋涡结构

---

### Pass 4: Divergence (散度计算)

**功能**: 计算速度场的散度

```glsl
// Divergence Shader
precision highp float;
varying vec2 vL, vR, vT, vB, vUv;
uniform sampler2D uVelocity;

vec2 sampleVelocity (in vec2 uv) {
  vec2 multiplier = vec2(1.0, 1.0);
  // 边界处理：反弹
  if (uv.x < 0.0) { uv.x = 0.0; multiplier.x = -1.0; }
  if (uv.x > 1.0) { uv.x = 1.0; multiplier.x = -1.0; }
  if (uv.y < 0.0) { uv.y = 0.0; multiplier.y = -1.0; }
  if (uv.y > 1.0) { uv.y = 1.0; multiplier.y = -1.0; }
  return multiplier * texture2D(uVelocity, uv).xy;
}

void main () {
  float L = sampleVelocity(vL).x;
  float R = sampleVelocity(vR).x;
  float T = sampleVelocity(vT).y;
  float B = sampleVelocity(vB).y;
  
  // 散度公式: div = ∂u/∂x + ∂v/∂y
  float div = 0.5 * (R - L + T - B);
  
  gl_FragColor = vec4(div, 0.0, 0.0, 1.0);
}
```

**数学公式**:

$$
\text{div} = \nabla \cdot \mathbf{v} = \frac{\partial u}{\partial x} + \frac{\partial v}{\partial y}
$$

**物理意义**:
- `> 0`: 流体发散（源）
- `< 0`: 流体汇聚（汇）
- `= 0`: 不可压缩

---

### Pass 5: Pressure (压力求解)

**功能**: 通过 Jacobi 迭代求解泊松方程

```glsl
// Pressure Jacobi Iteration Shader
precision highp float;
varying vec2 vUv, vL, vR, vT, vB;
uniform sampler2D uPressure;
uniform sampler2D uDivergence;

vec2 boundary (in vec2 uv) {
  return min(max(uv, 0.0), 1.0);
}

void main () {
  float L = texture2D(uPressure, boundary(vL)).x;
  float R = texture2D(uPressure, boundary(vR)).x;
  float T = texture2D(uPressure, boundary(vT)).x;
  float B = texture2D(uPressure, boundary(vB)).x;
  float divergence = texture2D(uDivergence, vUv).x;
  
  // Jacobi 迭代公式
  float pressure = (L + R + T + B - divergence) * 0.25;
  
  gl_FragColor = vec4(pressure, 0.0, 0.0, 1.0);
}
```

**泊松方程**:

$$
\nabla^2 p = \nabla \cdot \mathbf{v}
$$

**Jacobi 迭代**:

$$
p_{i,j}^{(n+1)} = \frac{p_{i-1,j} + p_{i+1,j} + p_{i,j-1} + p_{i,j+1} - \text{div}_{i,j}}{4}
$$

**迭代次数**: 20-40 次

---

### Pass 6: Gradient Subtract (梯度减法)

**功能**: 从速度场中减去压力梯度，保证不可压缩性

```glsl
// Gradient Subtract Shader
precision highp float;
varying vec2 vUv, vL, vR, vT, vB;
uniform sampler2D uPressure;
uniform sampler2D uVelocity;

vec2 boundary (in vec2 uv) {
  return min(max(uv, 0.0), 1.0);
}

void main () {
  float L = texture2D(uPressure, boundary(vL)).x;
  float R = texture2D(uPressure, boundary(vR)).x;
  float T = texture2D(uPressure, boundary(vT)).x;
  float B = texture2D(uPressure, boundary(vB)).x;
  
  vec2 velocity = texture2D(uVelocity, vUv).xy;
  
  // 减去压力梯度
  velocity.xy -= vec2(R - L, T - B);
  
  gl_FragColor = vec4(velocity, 0.0, 1.0);
}
```

**数学公式**:

$$
\mathbf{v}_{\text{new}} = \mathbf{v} - \nabla p
$$

**物理意义**: 移除速度场中的散度分量，保证 $\nabla \cdot \mathbf{v} = 0$

---

### Pass 7: Advection (平流)

**功能**: 沿速度场移动速度和密度（半拉格朗日法）

```glsl
// Advection Shader
precision highp float;
varying vec2 vUv;
uniform sampler2D uVelocity;
uniform sampler2D uSource;
uniform vec2 texelSize;
uniform float dt;
uniform float dissipation;

void main () {
  // 反向追踪粒子位置
  vec2 coord = vUv - dt * texture2D(uVelocity, vUv).xy * texelSize;
  
  // 双线性插值采样
  vec4 result = dissipation * texture2D(uSource, coord);
  
  gl_FragColor = result;
}
```

**关键参数**:
- `velocityDissipation`: 0.98 (速度衰减)
- `densityDissipation`: 0.97 (密度衰减)
- `dt`: 时间步长

---

### Pass 8: Display (显示)

**功能**: 将密度场渲染到屏幕

```glsl
// Display Shader
precision highp float;
varying vec2 vUv;
uniform sampler2D uTexture;

void main () {
  vec4 textureColor = texture2D(uTexture, vUv);
  
  // 反色处理（白色背景上的深色墨水）
  gl_FragColor = vec4(
    1.0 - textureColor.r,
    1.0 - textureColor.g,
    1.0 - textureColor.b,
    1.0
  );
}
```

---

## 四、完整管线结构图

```
═══════════════════════════════════════════════════════════════
                        墨水效果渲染管线
═══════════════════════════════════════════════════════════════

帧开始
  │
  ├─> [Input] 鼠标/触摸事件
  │      │
  │      ├─ position (x, y)
  │      ├─ velocity (dx, dy)
  │      └─ color (r, g, b)
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 1: SPLAT (注入阶段)                                   │
├─────────────────────────────────────────────────────────────┤
│ Pass 1.1: Velocity Splat                                    │
│   [velocity] ──────> [velocity_temp]                        │
│                                                             │
│ Pass 1.2: Density Splat                                     │
│   [density] ───────> [density_temp]                         │
│                                                             │
│ swap(velocity ↔ velocity_temp)                              │
│ swap(density ↔ density_temp)                                │
└─────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 2: VORTICITY (涡度增强阶段) ⭐                        │
├─────────────────────────────────────────────────────────────┤
│ Pass 2.1: Curl Calculation                                  │
│   [velocity] ──────> [curl]                                 │
│                                                             │
│ Pass 2.2: Vorticity Confinement                             │
│   [velocity] ─┐                                             │
│   [curl] ─────┴───> [velocity_temp]                         │
│                                                             │
│ swap(velocity ↔ velocity_temp)                              │
└─────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 3: PROJECTION (投影阶段 - 保持不可压缩)              │
├─────────────────────────────────────────────────────────────┤
│ Pass 3.1: Divergence Calculation                            │
│   [velocity] ──────> [divergence]                           │
│                                                             │
│ Pass 3.2: Pressure Solve (Jacobi迭代 x 20-40)              │
│   ┌─────────────────────────────┐                          │
│   │ for i = 0 to iterations:    │                          │
│   │   [pressure] ─┐              │                          │
│   │   [divergence]┴─> [pressure_temp]                      │
│   │   swap(pressure ↔ pressure_temp)                       │
│   └─────────────────────────────┘                          │
│                                                             │
│ Pass 3.3: Gradient Subtract                                 │
│   [velocity] ─┐                                             │
│   [pressure] ─┴───> [velocity_temp]                         │
│                                                             │
│ swap(velocity ↔ velocity_temp)                              │
└─────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 4: ADVECTION (平流阶段)                              │
├─────────────────────────────────────────────────────────────┤
│ Pass 4.1: Velocity Advection                                │
│   [velocity] ──────> [velocity_temp]                        │
│                                                             │
│ Pass 4.2: Density Advection                                 │
│   [velocity] ─┐                                             │
│   [density] ──┴───> [density_temp]                          │
│                                                             │
│ swap(velocity ↔ velocity_temp)                              │
│ swap(density ↔ density_temp)                                │
└─────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 5: DISPLAY (渲染阶段)                                │
├─────────────────────────────────────────────────────────────┤
│ Pass 5: Render to Screen                                    │
│   [density] ──────> [Screen]                                │
└─────────────────────────────────────────────────────────────┘
  │
  ▼
帧结束，返回Stage 1
```

---

## 五、Ping-Pong 缓冲机制

### 🔄 为什么需要双缓冲？

WebGL **不能同时读写同一个纹理**，所以使用 Ping-Pong 缓冲机制：

```javascript
// 创建双缓冲 FBO
function createDoubleFBO(texId, w, h, internalFormat, format, type, param) {
  let fbo1 = createFBO(texId, w, h, internalFormat, format, type, param);
  let fbo2 = createFBO(texId + 1, w, h, internalFormat, format, type, param);
  
  return {
    get first () { return fbo1; },
    get second () { return fbo2; },
    swap () {
      let temp = fbo1;
      fbo1 = fbo2;
      fbo2 = temp;
    }
  }
}
```

### 📊 Swap 操作示意图

```
初始状态:
  velocity [A] ──read──> Shader
  velocity_temp [B] <──write── Shader

swap() 后:
  velocity [B] ──read──> 下一Pass
  velocity_temp [A] 等待下次写入
```

---

## 六、关键参数配置

```javascript
// Observable 实现中的典型参数
const config = {
  // 分辨率
  simResolution: 128,              // 仿真分辨率 (128x128)
  dyeResolution: 512,              // 染料分辨率 (512x512)
  
  // 物理参数
  densityDissipation: 0.97,        // 密度消散 (0-1)
  velocityDissipation: 0.98,       // 速度消散 (0-1)
  pressure: 0.8,                   // 压力系数
  pressureIterations: 20,          // 压力迭代次数
  curl: 30,                        // 涡度增强强度 ⭐
  
  // 注入参数
  splatRadius: 0.0001,             // 注入半径
  splatForce: 6000,                // 注入力度
  
  // 渲染参数
  colorful: true,                  // 彩色模式
  paused: false,                   // 是否暂停
  
  // 性能参数
  bloom: false,                    // 辉光效果
  sunrays: false                   // 阳光效果
};
```

### 🎛️ 参数调优建议

| 参数 | 效果 | 推荐范围 |
|------|------|----------|
| `curl` | 涡流强度 | 10-40 |
| `velocityDissipation` | 速度保持时间 | 0.95-0.99 |
| `densityDissipation` | 墨水保持时间 | 0.90-0.98 |
| `splatRadius` | 注入范围 | 0.0001-0.001 |
| `pressureIterations` | 压力精度 | 15-40 |

---

## 七、性能分析

### 📊 每帧 Pass 统计

| Pass | 次数 | RT读写 |
|------|------|--------|
| Splat (velocity) | 1 | 1R + 1W |
| Splat (density) | 1 | 1R + 1W |
| Curl | 1 | 1R + 1W |
| Vorticity | 1 | 2R + 1W |
| Divergence | 1 | 1R + 1W |
| **Pressure (x20迭代)** | **20** | **2R + 1W x20** |
| Gradient Subtract | 1 | 2R + 1W |
| Advection (velocity) | 1 | 2R + 1W |
| Advection (density) | 1 | 2R + 1W |
| Display | 1 | 1R + 1W |
| **总计** | **29** | - |

### 💾 显存带宽 (512x512, RG16F)

- 每个 RT: `512 × 512 × 2 × 2 bytes = 1MB`
- 每帧总读写: 约 **60MB**
- 60fps: 约 **3.6GB/s** 带宽

---

## 八、核心算法总结

### 🌟 5大核心阶段

| 阶段 | 作用 | 核心算法 |
|------|------|----------|
| **1. Splat** | 注入速度和密度 | 高斯函数 |
| **2. Vorticity** | 增强涡度 ⭐ | 涡度约束法 |
| **3. Projection** | 保持不可压缩 | Jacobi迭代 + 投影法 |
| **4. Advection** | 传输物理量 | 半拉格朗日法 |
| **5. Display** | 渲染显示 | 反色映射 |

### 🔬 关键技术点

1. **涡度增强** - 保持旋涡的灵魂算法
2. **Ping-Pong 缓冲** - 解决 RT 读写冲突
3. **半拉格朗日平流** - 无条件稳定的平流方法
4. **Jacobi 迭代** - 快速压力求解
5. **边界处理** - 反弹边界条件

---

## 九、视觉效果链条

```
鼠标移动 → 速度注入 → 涡度增强 → 形成旋涡
                                    ↓
           密度扩散 ← 密度平流 ← 压力推动
                    ↓
              美丽的墨水卷曲效果 ✨
```

---

## 十、代码实现要点

### 🛠️ WebGL 设置

```javascript
// 检查浮点纹理支持
const ext = {
  formatRGBA: getSupportedFormat(gl, gl.RGBA16F, gl.RGBA, gl.HALF_FLOAT),
  formatRG: getSupportedFormat(gl, gl.RG16F, gl.RG, gl.HALF_FLOAT),
  formatR: getSupportedFormat(gl, gl.R16F, gl.RED, gl.HALF_FLOAT),
  halfFloatTexType: gl.HALF_FLOAT,
  supportLinearFloat: gl.getExtension('OES_texture_float_linear')
};

// 创建 FBO
function createFBO(texId, w, h, internalFormat, format, type, param) {
  gl.activeTexture(gl.TEXTURE0 + texId);
  let texture = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, texture);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, param);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, param);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  gl.texImage2D(gl.TEXTURE_2D, 0, internalFormat, w, h, 0, format, type, null);
  
  let fbo = gl.createFramebuffer();
  gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);
  gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, texture, 0);
  gl.viewport(0, 0, w, h);
  gl.clear(gl.COLOR_BUFFER_BIT);
  
  return [fbo, texture, texId];
}
```

### 🎨 鼠标交互

```javascript
function splat(x, y, dx, dy, color) {
  // 速度注入
  splatProgram.bind();
  gl.uniform1i(splatProgram.uniforms.uTarget, velocity.first[2]);
  gl.uniform2f(splatProgram.uniforms.point, 
    x / canvas.width, 
    1.0 - y / canvas.height
  );
  gl.uniform3f(splatProgram.uniforms.color, dx, -dy, 1.0);
  gl.uniform1f(splatProgram.uniforms.radius, 0.0001);
  blit(velocity.second[1]);
  velocity.swap();
  
  // 密度注入
  gl.uniform1i(splatProgram.uniforms.uTarget, density.first[2]);
  gl.uniform3f(splatProgram.uniforms.color, 
    0.3 * (256 - color[0]),
    0.3 * (256 - color[1]),
    0.3 * (256 - color[2])
  );
  blit(density.second[1]);
  density.swap();
}
```

---

## 十一、扩展阅读

### 📚 理论基础

- **Navier-Stokes 方程**: 流体力学的基础方程
- **Helmholtz-Hodge 分解**: 速度场分解为无散场和无旋场
- **涡度动力学**: 涡流的产生和演化

### 🔗 相关资源

- [原始演示](https://observablehq.com/@tomlarkworthy/ink) - Observable 平台
- [WebGL Fluid Simulation](https://paveldogreco.github.io/WebGL-Fluid-Simulation/) - 类似实现
- [GPU Gems: Real-Time Fluid Dynamics](https://developer.nvidia.com/gpugems/gpugems/part-vi-beyond-triangles/chapter-38-fast-fluid-dynamics-simulation-gpu) - NVIDIA 技术文档

---

## 📝 总结

Observable 墨水效果是一个精巧的流体仿真系统，核心亮点在于：

1. **涡度增强算法** - 保持墨水的旋涡美感
2. **投影法** - 保证物理正确的不可压缩流动
3. **高效的 GPU 实现** - 每帧仅需约 30 个 Pass

这套技术不仅可用于艺术效果，还可以扩展到：
- 🔥 火焰和烟雾模拟
- 🌊 水面波纹效果
- 🎨 交互式绘画工具
- 🎮 游戏特效系统

**关键启示**: 好的视觉效果 = 扎实的物理模型 + 巧妙的数值算法 + 精心的参数调优

---

> 💡 **提示**: 如果你对流体仿真感兴趣，可以从简单的 2D 烟雾模拟开始，逐步添加涡度增强、多种颜色混合等高级特性。

> 🎓 **学习建议**: 理解 Navier-Stokes 方程的物理意义，然后学习数值求解方法（投影法、半拉格朗日法），最后用 WebGL 实现。

---

**参考文献**:
1. Jos Stam, "Stable Fluids" (SIGGRAPH 1999)
2. Ronald Fedkiw et al., "Visual Simulation of Smoke" (SIGGRAPH 2001)
3. Mark Harris, "Fast Fluid Dynamics Simulation on the GPU" (GPU Gems)
