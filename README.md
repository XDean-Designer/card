# card · 剑琅联盟会员卡演示

静态 HTML 演示，通过 GitHub Pages 发布。

## 在线访问

**https://xdean-designer.github.io/card/**

- 入口：`index.html`
- 交互原型：`demo.html`
- 开发 PRD：`PRD-会员卡管理.md`（预览：`PRD-会员卡管理.html`）

推送 `main` 后，GitHub Actions（`Deploy GitHub Pages`）会自动发布。仓库 Pages 源需为 **GitHub Actions**（首次若 404，在 Settings → Pages 确认即可）。

## 本地预览

```bash
python -m http.server 8080
```

浏览器打开 `http://localhost:8080/`。

## 文件说明

| 文件 | 说明 |
|------|------|
| `index.html` | 演示入口 |
| `demo.html` | 交互原型（权益组合版）；已内嵌开单结账全量链路，资源在 `assets/billing/` |
| `PRD-会员卡管理.md` | 会员卡管理开发/测试 PRD 源文件（与原型配套） |
| `PRD-会员卡管理.html` | 上述 PRD 的阅读预览（表格/标题排版） |
| `assets/billing/` | 开单模块静态资源（从 `billing/assets` 拷贝，供 Pages 单包发布） |
| `剑琅联盟-会员卡-权益组合版.html` | 与 `demo.html` 同内容（中文文件名备份） |
