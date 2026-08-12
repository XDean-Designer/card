# 挂单列表

| 字段 | 值 |
|------|-----|
| flow | `bill-hold` |
| 原型深链 | [`demo.html?flow=bill-hold&capture=1`](../demo.html?flow=bill-hold&capture=1) |
| 对照截图 | [`captures/bill-hold.png`](../captures/bill-hold.png) |
| DOM/Screen | `screen-holds` |
| 说明 | 取挂单；删除挂单 |

## 实现注意

1. 画布逻辑宽 **390pt**；`?capture=1` 时高度可随内容延伸。  
2. **不要**绘制原型假状态栏。  
3. Token：只用本包 `tokens/` → Android `values/*` / iOS `DesignTokens.swift`。  
4. 行为与文案：以 `demo.html?flow=bill-hold` 为准（尚无独立开单 PRD）。  
5. 图标：`ICONS.md`。

## Cursor 提示（可复制）

```
实现开单记账「挂单列表」（flow=bill-hold）。
平台：Android XML + iOS SwiftUI。
只使用 native-handoff-billing/tokens 与 COMPONENTS.md。
对照 captures/bill-hold.png，禁止臆造间距/颜色/图标。
不要实现假 iOS 状态栏。
Toast 须相对画布居中。
```
