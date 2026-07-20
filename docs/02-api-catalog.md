# 02 · 接口目录草案（本期 P0）

> 路径、分页风格可按中台规范改；**字段语义**对齐 `01-data-model.md`。  
> 鉴权、租户/门店 ID 按现有网关约定追加，本文从略。  
> 状态码建议：`0` 成功；业务错误用明确 `code`（见文末）。

Base（示例）：`/api/v1/member-cards`

---

## 1. 模板

### `GET /templates`

列表。Query：`shelf=active|shelved`、`keyword`、`page`。

**Response item（摘要）**

```json
{
  "id": "tpl_xxx",
  "name": "尊享组合卡",
  "purchaseAmount": 3980,
  "shelved": false,
  "benefits": { "balance": true, "timesOrValidity": true, "projectDiscount": true },
  "usagePolicy": { "refundRule": "alloc_pool", "performanceRule": "alloc_pool" },
  "validCardCount": 12,
  "editable": false
}
```

`editable = (validCardCount === 0)`。

### `GET /templates/{id}`

详情：完整 `projectItems`（含 `qtyScope` / `sharedGroupId`）、`memberPrices`、`cardValidity`、`stats`。

### `POST /templates`

创建。Body = Template 可写字段（见数据模型）。校验：至少一类权益；策略必填。

### `PUT /templates/{id}`

更新。若 `validCardCount > 0` → **403** `TEMPLATE_LOCKED`。

### `POST /templates/{id}/clone`

克隆。返回新模板；`duplicatedFrom` = 源 id；不强制下架源模板。

### `POST /templates/{id}/shelf`

Body：`{ "shelved": true|false }`。下架后不可新办；已持卡仍可退/延。

---

## 2. 项目挂牌价（只读依赖）

### `GET /catalog/projects`（或中台既有）

本期**不实现**价目管理；办卡/选项目/退卡权重需要：

```json
{ "name": "洗剪吹", "price": 68, "onSale": true }
```

---

## 3. 会员（既有）

### `GET /members?keyword=`

选人列表。返回 `id, name, phoneMasked` 即可。

---

## 4. 办卡

### `POST /templates/{id}/issue`

```json
{
  "memberId": "m1",
  "paidAmount": 3980,
  "paymentChannel": "wechat",
  "paymentPayload": {}
}
```

**行为要点**

1. 模板未下架  
2. 拉挂牌价写入 `catalogPriceSnapshot`  
3. 写入 `usagePolicySnapshot`、`benefitSnapshot`  
4. 初始化 `ledger`  
5. 计算 `cardExpireAt`（非永久）  
6. `validCardCount++`  

**Response**：`CardInstance` 摘要 + 支付结果。

---

## 5. 持卡查询

### `GET /templates/{id}/holders`

在售办卡弹层「退卡/延期」Tab。返回会员、`status`、`cardExpireAt`、剩余摘要。

### `GET /instances/{instanceId}`

详情 + ledger（供退卡 Sheet）。

---

## 6. 延期

### `POST /instances/{instanceId}/extend`

```json
{
  "unit": "month",
  "value": 3,
  "feeAmount": 0
}
```

`unit`: `day|month|year|permanent`。  

规则摘要：仅改 `cardExpireAt`；含折扣权益时 `feeAmount` 可改（默认可按规则预填）；**独立流水，不计入办卡统计**；失效可复活。  
永久卡：原型「退卡/延期」Tab **仍展示「延期」入口**，点击 toast「该卡永久有效，无需延期」；接口应 **400** `EXTEND_NOT_ALLOWED`。纯面值永久口径同理。

---

## 7. 退卡

### `POST /instances/{instanceId}/refund/preview`

试算（只读，不落库）。

**Response（对齐 Sheet）**

```json
{
  "refundRule": "alloc_pool",
  "paidAmount": 500,
  "consumedTotal": 100,
  "suggestedRefund": 400,
  "remainingDisplayTotal": 400,
  "lines": [
    {
      "kind": "project",
      "label": "洗剪吹",
      "consumed": 100,
      "remaining": 400,
      "note": "均值 · 单次摊销 50 × 已用 2"
    }
  ]
}
```

说明：`suggestedRefund = max(0, paidAmount - consumedTotal)`；**不要用 remainingDisplayTotal 封顶**。

### `POST /instances/{instanceId}/refund/confirm`

```json
{
  "actualRefund": 400,
  "previewToken": "可选：与 preview 绑定防串改"
}
```

**行为**：打款；实例 → `refunded`；权益清零；`validCardCount--`；若 `actualRefund !== suggested` 写 **AuditLog**。

本期：**不支持部分退**；无审批字段。

---

## 8. 错误码（建议）

| code | 含义 |
|------|------|
| TEMPLATE_LOCKED | 有有效持卡，禁止改规则 |
| TEMPLATE_SHELVED | 已下架不可办卡 |
| EXTEND_NOT_ALLOWED | 永久卡等不可延期（UI 可展示入口，接口拒绝） |
| REFUND_NOT_ALLOWED | 已退 / 状态非法 |
| LEDGER_INCOMPLETE | 缺消耗数据（可配置拦截） |
| CATALOG_PRICE_MISSING | 缺挂牌价无法建池/减值 |

---

## 9. Mock 建议

1. 先实现 `preview` 与算例 A 对齐（见 `03-rules-cases.md`）  
2. 办卡支付可用 sandbox  
3. ledger 可用配置覆盖（对齐原型 `DEMO_HOLDER_LEDGER`）
