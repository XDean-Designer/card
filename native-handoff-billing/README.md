# 开单记账 · Native Handoff（方案 B）

面向：**Android XML** + **iOS SwiftUI**。  
范围：**仅 FLOW_MAP「开单记账」**（17 个 flow）。无 Figma；视觉以 `captures/` + Token 为准，行为以 `demo.html?flow=bill-*` 为准。

## 冲突优先级

1. `captures/*.png`（视觉）  
2. `tokens/design-tokens.json`（及 Android `values/*` / iOS `DesignTokens.swift`）  
3. 交互原型 `demo.html`（行为 / 文案 / 状态）  
4. **禁止**照抄原型假状态栏；用系统 SafeArea / WindowInsets  

## 目录

| 路径 | 用途 |
|------|------|
| `tokens/design-tokens.json` | 唯一 Token 源 |
| `android/values/*.xml` | 拷入 Android `res/values/` |
| `ios/DesignTokens.swift` | 拷入 iOS 工程 |
| `ICONS.md` + `icons/` | 图标 |
| `COMPONENTS.md` | 组件映射 |
| `SCREEN-INDEX.md` + `screens/*.md` | 逐屏规格 |
| `captures/*.png` | `?flow=&capture=1` 对照图 |
| `samples/android/` | 点单台 XML 样板 |
| `samples/ios/BillDeskView.swift` | 点单台 SwiftUI 样板 |

## 给 Cursor 的标准提示词

```
你是 Android XML + iOS SwiftUI 工程师。
只实现「开单记账」中我指定的 flow（见 SCREEN-INDEX.md）。
硬性规则：
1. 颜色/间距/圆角/字号只能来自 native-handoff-billing/tokens（及已生成的 colors.xml / dimens.xml / DesignTokens.swift）。
2. 布局对照 captures/<flow>.png，误差目标 ±1pt；禁止臆造。
3. 图标只用 ICONS.md；缺失则先标注 TODO，不要用占位几何凑合当最终稿。
4. 不要绘制原型里的假 iOS 状态栏；使用系统 SafeArea / WindowInsets。
5. 交互、文案以 ../demo.html?flow= 为准（尚无独立开单 PRD）。
6. Toast 相对手机画布居中（非贴底）。
7. 输出：Android XML + SwiftUI；命名对齐 samples/ 与 COMPONENTS.md。
先读：README、COMPONENTS、screens/<flow>.md、对应 capture。
```

## 本地预览 / 重采截图

```
../demo.html?flow=bill-bill&device=1
../demo.html?flow=bill-bill&capture=1
python ../scripts/capture_billing_handoff_shots.py
python ../scripts/gen_billing_native_handoff.py
```

## 主链建议实现顺序

1. `bill-pick` → `bill-bill` → `bill-detail`  
2. `bill-checkout` → `bill-pay` → `bill-success`  
3. `bill-benefit` / `bill-discount` / `bill-hold`  
4. 扫码与添加卡 / 充卡续卡
