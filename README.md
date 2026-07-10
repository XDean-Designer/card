# card · 剑琅联盟会员卡演示

静态 HTML 演示，通过 GitHub Pages 发布。

## 在线访问

**https://xdean-designer.github.io/card/**

- 入口：`index.html`
- 交互原型：`demo.html`
- 逻辑梳理：`logic.html`

推送 `main` 后，GitHub Actions 会自动部署到 `gh-pages` 分支。若首次访问 404，请在仓库 **Settings → Pages → Build and deployment → Source** 选择 **Deploy from a branch**，Branch 选 **gh-pages** / **/(root)**。

## 本地预览

```bash
python -m http.server 8080
```

浏览器打开 `http://localhost:8080/`。

## 文件说明

| 文件 | 说明 |
|------|------|
| `index.html` | 演示入口 |
| `demo.html` | 交互原型（权益组合版） |
| `logic.html` | 逻辑与算例文档 |
| `剑琅联盟-会员卡-权益组合版.html` | 与 `demo.html` 同内容（中文文件名备份） |
| `剑琅联盟-会员卡逻辑梳理.html` | 与 `logic.html` 同内容（中文文件名备份） |
