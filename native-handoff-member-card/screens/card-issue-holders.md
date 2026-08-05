# 选择会员 · 退卡/延期

| 字段 | 值 |
|------|-----|
| flow | `card-issue-holders` |
| 原型深链 | [`demo.html?flow=card-issue-holders&capture=1`](../demo.html?flow=card-issue-holders&capture=1) |
| 对照截图 | [`captures/card-issue-holders.png`](../captures/card-issue-holders.png)（若缺失则先跑 capture 脚本） |
| DOM/Screen | `overlay` |
| 说明 | 持卡管理 |

## 实现注意

1. 画布逻辑宽 **390pt**；高度随内容，底栏/Sheet 贴安全区。  
2. **不要**绘制原型假状态栏。  
3. Token：只用 `tokens/design-tokens.json` → Android `values/*` / iOS `DesignTokens.swift`。  
4. 行为与文案：`PRD-会员卡管理.md` 对应章节。  
5. 图标：`ICONS.md`。

## 布局树（摘要）

见 COMPONENTS 与截图自上而下还原；关键屏以截图像素为准微调 ±1pt。

## Cursor 提示（可复制）

```
实现会员卡「选择会员 · 退卡/延期」（flow=card-issue-holders）。
平台：Android XML + iOS SwiftUI。
只使用 native-handoff-member-card/tokens 与 COMPONENTS.md。
对照 captures/card-issue-holders.png，禁止臆造间距/颜色/图标。
不要实现假 iOS 状态栏。
```
