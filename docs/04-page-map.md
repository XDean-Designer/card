# 04 · 原型页面 ↔ 能力 ↔ 接口

原型：[`../demo.html`](../demo.html) · 在线：https://xdean-designer.github.io/card/demo.html  

**图例**：✅ 本期 P0　⏸ 依赖外部/占位　❌ 本期不排（原型仅演示）

---

## 1. 页面对照

| 原型 screen | 页面 | 本期 | 主要接口 |
|-------------|------|------|----------|
| `screen0` | 会员卡列表（在售/已下架） | ✅ | `GET /templates` |
| `screen10` | 创建 Step1 基本信息 | ✅ | （表单态） |
| `screen9` | 创建 Step2 权益组合 | ✅ | 选项目依赖 `GET /catalog/projects` ⏸ |
| `screen11` | 创建 Step3 用卡策略 | ✅ | `POST /templates` 保存 |
| `screen7` | 创建成功 | ✅ | — |
| `screen6` | 会员卡详情 | ✅ | `GET /templates/{id}` |
| `screen2setup` | 设置项目（次数） | ✅ | 写入模板草稿 |
| `screen2` | 选择项目（项目权益） | ✅ | catalog 只读 ⏸ |
| `screen4setup` | 设置折扣 | ✅ | 写入 `memberPrices` |
| `screen4` | 选择项目（折扣） | ✅ | catalog 只读 ⏸ |
| `screen5` | （折扣批量配置·弱） | ✅/可合并 | 可并入 setup |
| `screen8` | 办卡成功 | ✅ | `POST .../issue` |
| Sheet：选会员 | 新办 / 退卡延期 | ✅ | members ⏸ · holders · extend · refund |
| Sheet：退卡估值 | 建议退 / 实退 | ✅ | `refund/preview` · `confirm` |
| `screen-p-*` | 价目表 | ❌ | 不排本期 |
| — | 补录老卡 | P1 | 另立 |

---

## 2. 前端状态要点

| 场景 | 表现 |
|------|------|
| `validCardCount > 0` | 详情编辑禁用；提示克隆改规则 |
| `shelved` | 列表在「已下架」；不可新办；可重新上架/克隆 |
| 选择项目 | 展示「已选 N 项」；至少 1 项才能确定 |
| 永久卡 | 隐藏延期入口 |
| 含折扣延期 | 展示费用，可改/0 |
| 退卡 Sheet | 分项消耗在上或按现原型：剩余上、消耗下；策略角标均值/减值 |
| 实退改写 | 允许；提交走审计 |

---

## 3. 前端不接本期

- 价目 CRUD、置顶、绑卡锁定 UI、预约开关联调  
- 业绩计算结果展示  
- 部分退入口  

---

## 4. 与 PRD 可视化

范围投屏：[`../prd-review.html`](../prd-review.html)
