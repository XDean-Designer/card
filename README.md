# card · 剑琅联盟会员卡演示

静态 HTML 演示，通过 GitHub Pages 发布。

## 在线访问

**https://xdean-designer.github.io/card/**

- 入口：`index.html`
- 交互原型：`demo.html`
- 逻辑梳理：`logic.html`

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
| `demo.html` | 交互原型（权益组合版） |
| `logic.html` | 逻辑与算例文档 |
| `prd-review.html` | PRD 可视化评审页 |
| `PRD-会员卡-权益组合版.md` | 产品 PRD |
| **`docs/`** | **研发最小可开工包**（范围/模型/接口/规则/页面/验收） |
| `剑琅联盟-会员卡-权益组合版.html` | 与 `demo.html` 同内容（中文文件名备份） |
| `剑琅联盟-会员卡逻辑梳理.html` | 与 `logic.html` 同内容（中文文件名备份） |
