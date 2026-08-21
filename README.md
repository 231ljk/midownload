# MiDownload - 官方下载页面

一个采用小米设计风格的现代化官方软件下载页面，支持 Windows、Linux、Android、鸿蒙全平台。

## 设计风格

- **小米橙** (#FF6700) 为主色调
- 简洁轻盈的 MIUI / HyperOS 设计语言
- 白色卡片 + 柔和阴影 + 大圆角
- 大量留白，清晰的信息层级

## 支持平台

| 平台 | 直接下载 | 命令下载 |
|------|---------|---------|
| Windows | .exe / .zip | winget / choco |
| Linux | AppImage / .deb | curl 一键脚本 / apt |
| Android | APK / Google Play | - |
| HarmonyOS 鸿蒙 | HAP / 应用市场 | - |

## 页面结构

1. **导航栏** - 毛玻璃效果，固定顶部
2. **Hero 区域** - 产品标语、下载 CTA、版本信息
3. **下载中心** - 四大平台下载卡片
   - Windows / Linux：标签切换「直接下载」和「命令下载」
   - Android / 鸿蒙：简洁下载卡片
4. **特性展示** - 安全签名、极速下载、自动更新、简洁易用
5. **更新日志** - 版本历史记录
6. **常见问题** - FAQ 折叠面板
7. **页脚** - 品牌信息、链接、版权

## 功能特性

- 完全响应式，适配桌面/平板/手机
- 命令行一键复制功能
- 下载方式标签切换
- FAQ 手风琴折叠
- 纯静态单文件，无外部依赖
- 部署简单，直接上传即可使用

## 快速开始

### 本地预览

直接用浏览器打开 `index.html` 即可。

### 部署到静态托管

将 `index.html` 上传到任意静态文件服务：
- GitHub Pages
- Vercel / Netlify
- 阿里云 OSS / 腾讯云 COS
- Nginx / Apache 等 Web 服务器

## 自定义修改

1. **产品名称** - 搜索 `MiDownload` 替换为你的产品名
2. **下载链接** - 在 `handleDownload()` 函数中替换为真实下载地址
3. **命令行** - 修改各平台命令框中的安装命令
4. **版本信息** - 更新 Hero 区域和下载卡片中的版本号
5. **更新日志** - 在 changelog 区域添加版本记录
6. **配色** - 修改 `:root` 中的 CSS 变量

## 技术栈

- HTML5
- CSS3（CSS 变量、Grid、Flexbox、动画）
- 原生 JavaScript（无框架依赖）

## 浏览器兼容

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 许可证

MIT License
