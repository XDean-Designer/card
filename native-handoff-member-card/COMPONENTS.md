# COMPONENTS · 会员卡管理

原型 class → Android style/layout → SwiftUI View。测量以 `tokens/design-tokens.json` 与 `captures/` 为准。

| 原型 class / 模式 | 说明 | Android | SwiftUI |
|-------------------|------|---------|---------|
| `.status-bar` | **勿实现**；用系统状态栏 | system | system |
| 导航栏 `.nav` / title | 高 44；左返回 右操作 | Toolbar / custom 44dp | `.navigationTitle` + toolbar |
| `#listShelfSeg` | 在售｜已下架 | `TabLayout` / 自定义 Segment | `Picker(.segmented)` 或自定义 |
| `.catalog-group-bar` | 分组筛选轨 + 齿轮 | HorizontalScroll + ImageButton | `ScrollView(.horizontal)` |
| `.member-card-item` | 列表卡 | `item_member_card.xml` | `MemberCardRow` |
| `.member-card-compact` | 渐变头+VIP+名+金额 | include header | `MemberCardCompactHeader` |
| `.member-card-item__panel` | 权益摘要区 | LinearLayout sections | `MemberCardFacePanel` |
| `.card-face-act--clone-text` | 复制建卡 | `@style/Btn.CardFace.Outline` + icon | `CardFaceCloneButton` |
| `.card-face-act--outline` | 快速分组 | Outline button | `CardFaceOutlineButton` |
| `.card-face-act--solid` | 办卡/退卡 | `@style/Btn.CardFace.Solid` | `CardFaceSolidButton` |
| `.btn-main` | 主按钮红底白字 高44 | `@style/Btn.Main` | `PrimaryButton` |
| `.form-row` | 表单行 | `@style/Form.Row` | `FormRow` |
| `.benefit-block` + Switch | Step2 权益块 | Switch + expand | `BenefitToggleSection` |
| `.picker-sheet.tall` | 底部 Sheet | `BottomSheetDialog` | `.sheet` / custom detent |
| `.picker-mask` 居中 | Dialog | `AlertDialog` / Dialog | `.alert` / overlay |
| `.toast` | 底部黑半透提示 | Snackbar/custom | toast overlay |
| `.list-empty-state` | 空态 | empty layout | `ListEmptyState` |
| `.bottom-bar` | 底栏主按钮区 | 固定底 + elevation | safeAreaInset bottom |
| 颜色色板 `.color-chip` | Step1 五色 | Radio + gradient drawable | `CardColorSwatch` |

## 列表卡关键尺寸（390 宽）

| 区域 | 值 |
|------|-----|
| 页左右边距 | 16pt |
| 卡间距 | 12pt |
| 卡圆角 | 12pt（面板/卡片常见） |
| Compact 头内边距 | 对照 `captures/list-active.png` |
| Footer 按钮高 | ≥44pt |
| 权益网格折叠阈值 | 超过 4 项显示「展开 N 项」 |

## 冲突

- 间距/色：`design-tokens.json` > 臆造  
- 交互：`PRD-会员卡管理.md` + `demo.html?flow=`  
