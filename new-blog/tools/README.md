# 🚀 沪深300与M2数据更新完全指南

## 📊 数据更新保证方案总览

### 🎯 多层次数据保证体系

我们建立了完整的数据更新保证体系，从手动到全自动，确保数据的及时性、准确性和可靠性。

## 🛠️ 工具清单

### 核心工具
- `manual_update.py` - 手动数据输入工具
- `update_market_data.py` - 自动数据获取脚本  
- `data_manager.py` - 数据验证与备份系统
- `scheduler.py` - 自动化任务调度器
- `health_check.py` - 数据完整性检查工具

### 辅助脚本
- `daily_update.bat` - 一键更新部署脚本
- `create_task.bat` - Windows计划任务创建脚本
- `config.ini` - 系统配置文件

## 📋 使用方法

### 方法1: 手动更新（推荐日常使用）

```bash
# 1. 进入工具目录
cd tools

# 2. 运行手动更新脚本
python manual_update.py

# 3. 按提示输入数据
沪深300收盘点位: 3850.23
沪深300涨跌幅(%): 1.25
M2同比增速(%): 7.8

# 4. 确认更新
确认更新博客? (y/N): y

# 5. 一键发布
../daily_update.bat
```

### 方法2: 一键式更新

```bash
# 直接运行批处理脚本（如果数据已准备好）
./daily_update.bat
```

### 方法3: Windows定时任务

```bash
# 1. 以管理员身份运行
./create_task.bat

# 2. 系统将自动创建每日9:00的更新任务
```

### 方法4: Python调度器

```bash
# 启动Python调度器（支持更多自定义）
python scheduler.py
```

## 🔍 数据质量保证

### 数据验证规则

- **沪深300点位**: 1000-10000范围
- **涨跌幅**: ±20%以内
- **M2增速**: 0-20%范围
- **数据格式**: 严格类型检查

### 自动备份机制

```
data_backup/
├── market_data_20251029_090000.json
├── market_data_20251028_090000.json
└── ...（保留30天）
```

### 完整性检查

```bash
# 运行健康检查
python health_check.py

# 输出示例：
# ✓ 博客文件正常
# ✓ 网站已发布  
# ✓ 数据最新 (今日数据)
# ✓ 数据一致
```

## ⚙️ 配置选项

### config.ini 配置文件

```ini
[data_sources]
hs300_source = "manual"     # 数据源类型
m2_source = "manual"        # 数据源类型

[update_schedule]  
auto_update = false         # 是否启用自动更新
update_time = "09:00"       # 每日更新时间
weekend_skip = true         # 是否跳过周末

[backup]
backup_enabled = true       # 启用备份
backup_days = 30           # 保留天数
```

## 🚨 故障排除

### 常见问题

1. **数据验证失败**
   ```bash
   # 检查数据范围是否合理
   # 沪深300: 1000-10000
   # M2增速: 0-20%
   ```

2. **博客生成失败**
   ```bash
   # 检查Hexo环境
   hexo version
   
   # 重新安装依赖
   npm install
   ```

3. **Git推送失败**
   ```bash
   # 检查Git配置
   git status
   git remote -v
   ```

### 数据恢复

```bash
# 从备份恢复数据
python data_manager.py

# 查看备份历史
ls data_backup/
```

## 📈 监控与通知

### 邮件通知设置

1. 修改 `config.ini`:
```ini
[notification]
email_notify = true
email_address = "your@email.com"
```

2. 配置SMTP服务器（在scheduler.py中）

### 日志监控

```bash
# 查看更新日志
tail -f update_log.txt

# 查看错误日志  
grep ERROR update_log.txt
```

## 🎯 最佳实践

### 日常维护流程

1. **每日上午9点前**
   - 获取最新市场数据
   - 运行 `python manual_update.py`
   - 执行 `./daily_update.bat`

2. **每周检查**
   - 运行 `python health_check.py`
   - 检查备份文件完整性
   - 清理过期日志

3. **每月维护**
   - 更新API密钥（如使用）
   - 检查系统配置
   - 优化性能设置

### 数据质量提升

1. **多源验证**: 对比不同数据源
2. **趋势检查**: 识别异常波动
3. **手动复核**: 重要数据人工确认

## 🔐 安全考虑

1. **API密钥管理**: 使用环境变量存储
2. **访问权限**: 限制脚本执行权限  
3. **数据加密**: 敏感配置信息加密存储

## 📞 技术支持

如遇问题，请检查：
1. Python环境是否正确配置
2. 必需包是否已安装
3. 网络连接是否正常
4. Git权限是否配置正确

---

*更新时间: 2025-10-29*  
*版本: v1.0*