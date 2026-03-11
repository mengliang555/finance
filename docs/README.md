# 财务分析网站 - 部署说明

这个目录包含财务分析项目的静态网站文件，用于GitHub Pages部署。

## 文件结构

```
docs/
├── index.html              # 主页面
├── css/
│   └── style.css          # 样式表
├── js/
│   └── main.js            # JavaScript文件
├── images/                # 图片资源目录
├── _config.yml           # GitHub Pages配置
├── .nojekyll             # 禁用Jekyll处理
└── README.md             # 本文件
```

## 部署到GitHub Pages

### 方法1：通过GitHub设置自动部署

1. 访问GitHub仓库：https://github.com/mengliang555/finance
2. 点击"Settings"（设置）
3. 在左侧菜单中选择"Pages"（页面）
4. 在"Source"（源）部分选择：
   - Branch: `main`
   - Folder: `/docs`
5. 点击"Save"（保存）
6. 等待几分钟，网站将在以下地址可用：
   - https://mengliang555.github.io/finance

### 方法2：手动部署

如果需要手动部署，可以运行以下命令：

```bash
# 进入项目目录
cd /Users/mengliang.yang/github/finance

# 提交网站文件
git add docs/
git commit -m "feat: 添加财务分析网站"

# 推送到GitHub
git push origin main
```

## 本地开发

### 启动本地服务器

```bash
# 使用Python启动简单HTTP服务器
cd docs
python3 -m http.server 8000

# 或者使用Node.js的http-server
npx http-server docs -p 8000
```

然后在浏览器中访问：http://localhost:8000

### 开发说明

1. **HTML结构**：`index.html` 包含完整的网站结构
2. **样式**：`css/style.css` 包含所有样式定义
3. **交互**：`js/main.js` 包含图表和交互功能
4. **图表**：使用Chart.js库绘制财务图表

## 功能特性

### 已实现功能
1. **响应式设计**：适配桌面和移动设备
2. **交互式图表**：风险雷达图、估值对比图、营收趋势图
3. **标签页切换**：财务指标、业务分析、风险分析、估值分析
4. **平滑滚动**：导航栏平滑滚动到对应部分
5. **公司卡片**：交互式公司信息卡片
6. **分析框架**：六步分析流程展示

### 技术栈
- **HTML5**：语义化标签和现代HTML特性
- **CSS3**：Flexbox、Grid、CSS变量、响应式设计
- **JavaScript**：ES6+特性、Chart.js图表库
- **Chart.js**：数据可视化图表
- **Font Awesome**：图标库
- **Google Fonts**：Inter和Source Code Pro字体

## 自定义配置

### 修改公司信息
编辑 `index.html` 中的公司卡片部分：

```html
<div class="company-card">
    <div class="company-header">
        <div class="company-logo xiaomi">
            <i class="fas fa-mobile-alt"></i>
        </div>
        <div class="company-info">
            <h3 class="company-name">公司名称</h3>
            <div class="company-ticker">股票代码</div>
        </div>
    </div>
    <!-- ... -->
</div>
```

### 修改财务数据
编辑 `js/main.js` 中的图表数据：

```javascript
// 风险雷达图数据
data: [7, 8, 6, 5, 3] // 分别对应行业风险、竞争风险、技术风险、监管风险、财务风险

// 估值对比图数据
data: [16.5, 27.5, null, 27.5] // P/E比率数据
```

### 修改样式
编辑 `css/style.css` 中的CSS变量：

```css
:root {
    --primary-color: #2563eb;
    --xiaomi-color: #ff6900;
    --meituan-color: #ffc300;
    /* ... */
}
```

## 添加新公司

### 步骤1：添加公司卡片
在 `index.html` 的 `.companies-grid` 部分添加新的公司卡片。

### 步骤2：更新图表数据
在 `js/main.js` 中更新所有图表的数据集。

### 步骤3：更新对比表格
在 `index.html` 的对比表格中添加新的列。

## 性能优化

### 已实施的优化
1. **图片优化**：使用适当尺寸的图片
2. **代码分割**：CSS和JS文件分离
3. **缓存策略**：设置适当的缓存头
4. **懒加载**：图片和图表按需加载

### 建议的进一步优化
1. **图片压缩**：使用WebP格式
2. **代码压缩**：压缩HTML、CSS、JS文件
3. **CDN加速**：使用CDN分发静态资源
4. **服务端渲染**：考虑使用SSR提高首屏加载速度

## 浏览器兼容性

### 支持的浏览器
- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

### 不支持的浏览器
- Internet Explorer 11及以下版本

## 故障排除

### 常见问题

#### 1. 图表不显示
- 检查Chart.js是否正确加载
- 检查JavaScript控制台是否有错误
- 确保canvas元素存在且ID正确

#### 2. 样式不正常
- 检查CSS文件是否正确加载
- 检查CSS变量是否正确定义
- 清除浏览器缓存

#### 3. GitHub Pages不更新
- 检查GitHub Pages设置是否正确
- 等待几分钟让更改生效
- 清除浏览器缓存

#### 4. 移动设备显示问题
- 检查响应式设计是否正确
- 测试不同屏幕尺寸
- 使用浏览器开发者工具模拟移动设备

### 调试工具
- **Chrome DevTools**：检查元素、网络、控制台
- **Lighthouse**：性能、可访问性、最佳实践检查
- **WebPageTest**：性能测试和优化建议

## 贡献指南

欢迎贡献代码和改进建议：

1. Fork本仓库
2. 创建功能分支：`git checkout -b feature/新功能`
3. 提交更改：`git commit -m '添加新功能'`
4. 推送到分支：`git push origin feature/新功能`
5. 创建Pull Request

## 许可证

本项目采用MIT许可证。详见根目录的LICENSE文件。

## 联系方式

如有问题或建议，请通过以下方式联系：

- GitHub Issues: https://github.com/mengliang555/finance/issues
- Email: example@example.com

---

**最后更新**: 2026年3月11日  
**版本**: v1.0.0