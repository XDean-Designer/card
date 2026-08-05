# 会员卡管理 · Native Handoff（方案 B）

面向：**Android XML** + **iOS SwiftUI**。  
范围：**仅会员卡管理**。无 Figma；视觉以 `captures/` + Token 为准，行为以 `PRD-会员卡管理.md` + `demo.html` 为准。

## 目录

| 路径 | 用途 |
|------|------|
| `tokens/design-tokens.json` | 唯一 Token 源 |
| `android/values/*.xml` | 直接拷入 Android `res/values/` |
| `ios/DesignTokens.swift` | 拷入 iOS 工程 |
| `ICONS.md` + `icons/` | 图标 |
| `COMPONENTS.md` | 组件映射 |
| `SCREEN-INDEX.md` + `screens/*.md` | 逐屏规格 |
| `captures/*.png` | `?flow=&capture=1` 对照图 |
| `samples/android/` | 列表页 XML 样板 |
| `samples/ios/CardListView.swift` | 列表页 SwiftUI 样板 |

## 给 Cursor 的标准提示词

```
你是 Android XML + iOS SwiftUI 工程师。
只实现「会员卡管理」中我指定的 flow（见 SCREEN-INDEX.md）。
硬性规则：
1. 颜色/间距/圆角/字号只能来自 native-handoff-member-card/tokens（及已生成的 colors.xml / dimens.xml / DesignTokens.swift）。
2. 布局对照 captures/<flow>.png，误差目标 ±1pt；禁止臆造。
3. 图标只用 ICONS.md；缺失则先标注 TODO，不要用占位几何凑合当最终稿。
4. 不要绘制原型里的假 iOS 状态栏；使用系统 SafeArea / WindowInsets。
5. 交互、文案、状态机以 ../PRD-会员卡管理.md 与 ../demo.html?flow= 为准。
6. 输出：Android XML（layout + 如需 item）+ SwiftUI View；命名对齐 samples/ 与 COMPONENTS.md。
先读：README、COMPONENTS、screens/<flow>.md、对应 capture。
```

## 本地预览原型

```
../demo.html?flow=list-active&device=1
../demo.html?flow=list-active&capture=1
```

## 重新截图

```powershell
python ../scripts/capture_member_handoff_shots.py
```

## 冲突优先级

1. `captures/*.png`（视觉）  
2. `design-tokens.json`  
3. PRD + 可点击原型（行为）  
