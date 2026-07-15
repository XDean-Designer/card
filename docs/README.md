# 研发最小可开工包 · 会员卡权益组合版

> **在线 / 演示请打开 [`index.html`](./index.html)**（左侧切换各文档）。GitHub Pages 无法把 `.md` 渲染成可导航站点，`.md` 仅作源文件维护。

面向前后端联调与估点的**最小文档集**。业务范围以产品 PRD 为准；规则以实现说明书 + 算例为准；原型仅作交互参考。

| 文档 | 用途 | 主读者 | 浏览 |
|------|------|--------|------|
| [00-scope.md](./00-scope.md) | 本期做 / 不做 | 全员 | [在站点中打开](./index.html#00-scope) |
| [01-data-model.md](./01-data-model.md) | 实体、字段、状态、快照 | 后端为主 | [在站点中打开](./index.html#01-data-model) |
| [02-api-catalog.md](./02-api-catalog.md) | 接口目录与请求/响应草案 | 前后端 | [在站点中打开](./index.html#02-api-catalog) |
| [03-rules-cases.md](./03-rules-cases.md) | 延期/退卡公式与验收算例 | 后端 + QA | [在站点中打开](./index.html#03-rules-cases) |
| [04-page-map.md](./04-page-map.md) | 原型页面 ↔ 能力 ↔ 接口 | 前端为主 | [在站点中打开](./index.html#04-page-map) |
| [05-acceptance.md](./05-acceptance.md) | 本期 P0 验收清单 | QA + 产品 | [在站点中打开](./index.html#05-acceptance) |

## 权威源优先级

1. **范围**：`../PRD-会员卡-权益组合版.md`、`../prd-review.html`
2. **规则**：本目录 `03-rules-cases.md` + `../logic.html` 算例；实现应对齐 `demo.html` 中 `computeSuggestedRefund*`
3. **交互**：`../demo.html`（含价目等**非本期**演示，勿按原型扩 scope）

## 在线入口

- **开工包站点**：https://xdean-designer.github.io/card/docs/
- 演示：https://xdean-designer.github.io/card/
- 原型：https://xdean-designer.github.io/card/demo.html
- 逻辑：https://xdean-designer.github.io/card/logic.html

## 建议联调顺序

1. 定稿：模板创建/详情字段 + `usagePolicy` 枚举  
2. Mock：模板列表、办卡、退卡试算（先通 Sheet）  
3. 退卡算例 A 单测通过后再接支付/核销真数据  
4. 延期、上下架、锁定（`validCardCount`）  
