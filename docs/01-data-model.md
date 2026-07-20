# 01 · 领域数据模型（草案）

> 字段名对齐原型 `demo.html` 状态结构，落库时可改名，但语义需一一映射。  
> `id` 建议 UUID；金额单位：**元**，保留 2 位小数。

```text
Template（卡模板）
  ├─ benefits flags + 面值字段
  ├─ projectItems[]          （项目权益）
  ├─ memberPrices{}          （折扣权益）
  └─ usagePolicy             （策略，办卡时快照到实例）

CardInstance（持卡实例）
  ├─ usagePolicySnapshot
  ├─ catalogPriceSnapshot{}  （相关项目挂牌价）
  ├─ cardExpireAt
  ├─ paidAmount
  └─ ledger                  （余额 / 次数 / 折扣已享）

Member（外部）──办卡──▶ CardInstance
Payment / Refund（外部）
Consumption（既存核销）──汇总──▶ ledger used 字段
```

---

## 1. Template（卡模板）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 模板 ID |
| name | string | 是 | 卡名称 |
| recharge / purchaseAmount | number | 是* | 购买金额（原型 `recharge`）；面值场景下亦为面值基准 |
| giftAmount | number | 否 | 赠送面值；仅 `benefits.balance` |
| cardColor | string | 否 | 卡面主题枚举，如 `brand_red` |
| shelved | bool | 是 | true = 已下架，不可新办 |
| createdAt | number/ISO | 是 | |
| duplicatedFrom | string | 否 | 复制建卡来源模板 ID |
| benefits.balance | bool | 是 | 是否含面值 |
| benefits.timesOrValidity | bool | 是 | 是否含项目次数 |
| benefits.projectDiscount | bool | 是 | 是否含折扣 |
| projectItems | ProjectItem[] | 条件 | `timesOrValidity` 时至少 1 项 |
| memberPrices | map | 条件 | key = 项目名或 `__ALL__`；`projectDiscount` 时必有 |
| usagePolicy | UsagePolicy | 是 | 见下 |
| cardValidity | Validity | 是 | 卡级有效期；仅约束项目/折扣；**默认永久** |
| stats.validCardCount | int | 算 | **锁定关键**：>0 不可编辑规则字段 |

\* 无面值的纯项目/折扣卡仍有「购买金额」作为办卡实付。

> **原型编辑态**：Step2 以 `projectBenefitCards[]` / `discountBenefitCards[]` 分组编辑（同次数或同折扣规则可绑多项目合成一张卡），保存时展开为 `projectItems` / `memberPrices`。落库以展开后字段为准。

### ProjectItem

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 可选 |
| name | string | 关联价目项目名 / ID（本期用既存挂牌价源） |
| purchaseQty | int | 权益次数（界面文案；字段名历史保留） |
| giftQty | int | 赠送次数 |
| unlimited | bool | 不限次；不参与退卡名义池项目权重 |
| qtyScope | `per_item` \| `shared` | 计次模式：每项 / 共计；不限次强制 `per_item` |
| sharedGroupId | string \| null | 共计时共享次数池 ID（同权益卡内多项目共用） |

### DiscountRule（memberPrices 的 value）

| 字段 | 类型 | 说明 |
|------|------|------|
| mode | `discount` \| `fixed` | 折扣档 / 固定会员价 |
| tickIndex | 0–20 | 仅 discount；`20` = 原价；折后价 = 原价 × tickIndex/20 |
| amount | number | 仅 fixed |

`__ALL__`：批量「全部项目」同一规则（原型 `MP_BATCH_KEY`）。

### UsagePolicy

| 字段 | 枚举 | 默认 | 说明 |
|------|------|------|------|
| refundRule | `alloc_pool` \| `retail` | `alloc_pool` | 退卡：界面「均值模式」/「减值模式」 |
| performanceRule | `alloc_pool` \| `retail` | `alloc_pool` | 业绩：界面「均值模式」/「原价模式」；**本期只存不运算** |

> 枚举值两端相同；界面文案按轨区分（退卡 retail≠业绩 retail 的中文名）。原型 Step3 各选项附一行公式提示。

### Validity（卡有效期）

| 形态 | 说明 |
|------|------|
| permanent | 项目/折扣亦视为不设到期；**含不限次项目时不可为永久**（前端弹窗拦截，见 `04`） |
| 日 / 月 / 年 | 办卡日写入 `cardExpireAt` |

---

## 2. CardInstance（持卡实例）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 实例 ID |
| templateId | string | 来源模板（可保留快照副本） |
| memberId | string | 外部会员 ID |
| paidAmount | number | 办卡实付 |
| issuedAt | ISO | 办卡时间 |
| cardExpireAt | date\|null | 项目/折扣到期；永久为空 |
| status | enum | `active` \| `expired` \| `refunded` |
| usagePolicySnapshot | UsagePolicy | 办卡冻结 |
| catalogPriceSnapshot | map name→price | 办卡时挂牌价；**改价不回溯** |
| benefitSnapshot | object | 办卡时权益结构副本（防模板后改） |
| ledger | Ledger | 见下 |

### Ledger

**balance**（可空）

| 字段 | 说明 |
|------|------|
| rechargeRemaining / giftRemaining | 剩余充值面值 / 赠送 |
| rechargeUsed / giftUsed | 已用（消费顺序：先充值后赠送） |

**projects[name]**（次数卡项）

| 字段 | 说明 |
|------|------|
| purchaseRemaining / giftRemaining | 剩余次数；**共计组**仅 primary 项目写入完整剩余，同组其余为 0 |
| purchaseUsed / giftUsed | 先购买次后赠送次；共计组各项目均可记 used |
| sharedGroupId | 可选；共计组 ID |
| sharedPoolPrimary | 可选 bool；共计组内是否为次数池主行 |

**discountUses[name]**  
可为次数或明细；退卡折扣消耗用 **累计已享优惠** `savedTotal`（Σ 原价−折后）。账本需能汇总到 `savedTotal`。

---

## 3. 流水与审计

| 实体 | 关键字段 | 说明 |
|------|----------|------|
| ExtensionOrder | instanceId, days/unit, feeAmount, fromExpire, toExpire | 延期；**不计入办卡总额/次数** |
| RefundOrder | instanceId, suggestedAmount, actualAmount, lines[] | 整卡退 |
| AuditLog | actor, action, before/after, at | 至少覆盖：改实际退款 |

---

## 4. 状态机（摘要）

**模板**

```text
在售(shelved=false) ⇄ 已下架(shelved=true)
编辑规则：仅当 validCardCount==0（及产品约定的无有效持卡）
复制建卡：始终可 → 新模板 duplicatedFrom
```

**实例**

```text
active --到期--> expired --延期--> active
active|expired --确认退卡--> refunded（权益清零）
```

---

## 5. 外部依赖（只读/调用）

| 系统 | 本期用法 |
|------|----------|
| 会员 | 搜索/选择 `memberId` |
| 支付/退款 | 办卡收款；退卡打款 |
| 价目/项目 | 名称 + 挂牌价（只读） |
| 核销 | 汇总写入 ledger used；无则允许 Mock 账本 |

字段级 DDL 可由后端按本表展开；评审时重点对齐：**快照、ledger、usagePolicy 枚举**。
