# GitHub Pages 设置指南

## 问题诊断
当前访问 https://mengliang555.github.io/finance 返回404错误："Site not found"

## 解决方案步骤

### 步骤1：访问GitHub仓库设置
1. 打开浏览器，访问：https://github.com/mengliang555/finance
2. 点击右上角的 **"Settings"**（设置）
3. 在左侧菜单中选择 **"Pages"**（页面）

### 步骤2：配置GitHub Pages
在Pages设置页面中，配置以下选项：

#### 分支设置
```
Source: Deploy from a branch
Branch: main
Folder: /docs
```

#### 保存设置
点击 **"Save"**（保存）按钮

### 步骤3：等待构建
GitHub Pages构建通常需要：
- 首次构建：1-5分钟
- 后续更新：1-2分钟

### 步骤4：检查构建状态
1. 在Pages设置页面查看构建状态
2. 如果有错误，查看错误日志
3. 等待状态变为 **"Your site is published at..."**

## 验证步骤

### 验证1：检查仓库名称
确保仓库名称为：`finance`
- 正确：https://github.com/mengliang555/finance
- 错误：https://github.com/mengliang555/Finance (大小写敏感)

### 验证2：检查文件结构
确保 `docs/` 目录包含：
```
docs/
├── index.html
├── css/style.css
├── js/main.js
├── _config.yml
└── .nojekyll
```

### 验证3：检查分支
确保代码在 `main` 分支：
```bash
git branch
# 应该显示: * main
```

## 常见问题解决

### 问题1：404错误
**症状**: 访问返回 "Site not found"
**解决方案**:
1. 确认Pages已启用
2. 检查分支和目录设置
3. 等待构建完成

### 问题2：构建失败
**症状**: Pages设置显示构建失败
**解决方案**:
1. 查看构建日志
2. 检查文件语法错误
3. 确保 `.nojekyll` 文件存在

### 问题3：样式丢失
**症状**: 页面显示但样式异常
**解决方案**:
1. 检查CSS文件路径
2. 确保相对路径正确
3. 清除浏览器缓存

## 手动设置命令

如果需要通过命令行检查：

```bash
# 检查当前分支
git branch

# 检查文件结构
ls -la docs/

# 检查最近提交
git log --oneline -3

# 推送到GitHub
git push origin main
```

## 备用访问方案

### 方案A：本地访问
```bash
cd /Users/mengliang.yang/github/finance/docs
python3 -m http.server 8000
# 访问 http://localhost:8000
```

### 方案B：直接查看文件
```bash
open /Users/mengliang.yang/github/finance/docs/index.html
```

### 方案C：使用其他端口
```bash
cd /Users/mengliang.yang/github/finance/docs
python3 -m http.server 8080
# 访问 http://localhost:8080
```

## 预期结果

成功配置后，应该能够访问：
- **GitHub Pages**: https://mengliang555.github.io/finance
- **本地服务器**: http://localhost:8000

## 联系支持

如果问题仍然存在：
1. 查看GitHub Pages文档：https://docs.github.com/en/pages
2. 检查GitHub状态：https://www.githubstatus.com/
3. 在GitHub仓库创建Issue

---

**最后更新**: 2026年3月11日 14:04  
**问题状态**: GitHub Pages返回404错误  
**解决方案**: 需要手动配置GitHub Pages设置