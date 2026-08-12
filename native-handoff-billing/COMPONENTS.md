# COMPONENTS · 开单记账

原型 class → Android → SwiftUI。测量以 `tokens/design-tokens.json` 与 `captures/` 为准。

| 原型 class / 模式 | 说明 | Android | SwiftUI |
|-------------------|------|---------|---------|
| `.status-bar` | **勿实现** | system | system |
| `.page-title-bar` / `.title` | 导航 44 | Toolbar | NavigationStack |
| `.customer-card` / 顾客条 | 选客/点单顶区 | item_customer | `CustomerHeader` |
| `.pick-holds-entry` | 取挂单 | TextButton | `HoldsEntryButton` |
| `.bill-action` | 选卡/快消文件夹卡 | custom Constraint | `BillActionCard` |
| `.bill-action__tab` | 文件夹 Tab；斜切 18pt | ClipPath / Shape | `FolderTabShape` |
| `.bill-card-rail` | 横向持卡轨 | RecyclerView horizontal | `ScrollView(.horizontal)` |
| `.bill-held-card` | 卡面 48×32 + 名 | item_held_card | `HeldCardTile` |
| `.bill-held-card--add` | 虚线办卡 | dashed border | `AddCardTile` |
| `.bill-quick-row` | 快消金额+添加 | LinearLayout | `QuickConsumeRow` |
| `.bill-slip` / stack | 记账单 | item_bill_slip | `BillSlipView` |
| `.bill-slip__no-card` | 未选卡灰字 | TextView | Text |
| `.bill-slip__del` | 红色垃圾桶 | ImageButton tint trash | Button |
| `.bill-continue-add` | 莫兰迪绿继续添加 | `@style/Bill.ContinueAdd` | `ContinueAddButton` |
| `.catalog-list` / 价目 | 项目产品列表 | RecyclerView | `CatalogList` |
| `.page-tabs` | 项目｜产品 | TabLayout | segmented |
| `.bottom-bar` + 应付 | 底栏 | fixed bottom | safeAreaInset |
| `.picker-sheet` / mask | Sheet | BottomSheet | `.sheet` |
| `.checkout-action` | 结账三入口 | Image+label | `CheckoutAction` |
| `.pay-channels` | 支付渠道 | Radio list | `PayChannelList` |
| `.benefit-none-btn` / offer icons | 不使用权益(红)/人工打折(蓝) | tint offer_none/manual | Image+tint |
| `.toast` / `.toast-msg` | **画布居中** Toast | custom center | overlay center |
| `.staff-card` morph | 服务员工展开 | custom | `StaffPickerRow` |

## 点单台关键尺寸（390）

| 区域 | 值 |
|------|-----|
| 页左右边距 | 16pt |
| 文件夹 Tab 高 | 36pt |
| Tab 斜切宽 | 18pt（左右对称负边距咬合） |
| 持卡轨 gap | 30pt（约露出第 4 张 1/4） |
| 记账单删除图标 | brand 红 |
| Toast | 相对 phone 画布水平+垂直居中 |

## 冲突

1. `captures/*.png`  
2. `design-tokens.json`  
3. `demo.html?flow=bill-*`  
