# -*- coding: utf-8 -*-
"""Generate native handoff package for 开单记账 (Android XML + iOS SwiftUI)."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "native-handoff-billing"
ASSETS = ROOT / "assets" / "billing"

TOKENS = {
    "meta": {
        "scope": "billing-only",
        "canvas": {"width": 390, "height": 844, "unit": "pt"},
        "source": "card/demo.html FLOW_MAP「开单记账」(extracted, no Figma)",
        "platforms": ["Android XML", "iOS SwiftUI"],
        "conflictRule": [
            "Visual: capture PNG at ?flow=&capture=1 (390 logical width)",
            "Behavior/copy/state: demo.html?flow=bill-* (no dedicated billing PRD yet)",
            "Do NOT clone prototype fake iOS status bar; use system safe areas",
        ],
    },
    "color": {
        "brand": "#F32F41",
        "brandSoft": "#FFF2F2",
        "brandBorder": "#FFD5D9",
        "success": "#2BA471",
        "successSoft": "#E8F8F2",
        "successText": "#008858",
        "bgPage": "#F7F7F7",
        "surface": "#FFFFFF",
        "textPrimary": "#333333",
        "textSecondary": "#929292",
        "textMid": "#666666",
        "textStrong": "#1A1A1A",
        "border": "#D7D7D5",
        "borderLight": "#E8E8E8",
        "disabled": "#EDEDED",
        "accentOrange": "#FF7043",
        "folderTabIdle": "#EFEFEF",
        "folderTabIdleText": "#8A8A8A",
        "continueAdd": "#5FA890",
        "continueAddActive": "#4F9A82",
        "offerNone": "#C47B7B",
        "offerManual": "#7A9BB8",
        "toastBg": "rgba(26,26,26,0.88)",
        "slipNoCard": "#5C5C5C",
        "trash": "#F32F41",
        "shellChrome": "#E8EAED",
    },
    "typography": {
        "fontText": {
            "ios": "PingFang SC",
            "android": "sans-serif",
            "note": "Prefer PingFang on iOS, system sans on Android",
        },
        "fontData": {
            "family": "TCloudNumber",
            "fallback": ["DIN Alternate", "Helvetica Neue", "monospace"],
            "files": "card/assets/fonts/TCloudNumber/*.ttf",
        },
        "sizesPt": {
            "caption2": 10,
            "caption": 11,
            "footnote": 12,
            "subhead": 13,
            "body": 14,
            "callout": 15,
            "headline": 16,
            "title3": 17,
            "title2": 18,
            "title1": 20,
            "largeTitle": 22,
            "display": 28,
            "amountXL": 32,
        },
        "weights": {"regular": 400, "medium": 500, "semibold": 600, "bold": 700},
    },
    "spacing": {
        "scalePt": [0, 2, 4, 6, 8, 10, 12, 14, 16, 20, 24, 30, 32, 40, 48],
        "common": {
            "pageH": 16,
            "sectionGap": 12,
            "rowV": 14,
            "rowH": 16,
            "chipHPad": 12,
            "bottomBarPad": 16,
            "sheetTopPad": 20,
            "billActionGap": 30,
            "folderSlant": 18,
        },
    },
    "radius": {
        "xs": 4,
        "sm": 6,
        "md": 8,
        "lg": 10,
        "xl": 12,
        "xxl": 16,
        "pill": 999,
        "sheetTop": [16, 16, 0, 0],
    },
    "elevation": {
        "bottomBarShadow": "0 -0.5 4 rgba(0,0,0,0.08)",
        "actionCardShadow": "0 2 10 rgba(0,0,0,0.04)",
    },
    "touch": {
        "minHeightPt": 44,
        "navBarHeightPt": 44,
        "bottomPrimaryButtonHeightPt": 44,
        "folderTabHeightPt": 36,
        "heldCardFace": {"w": 48, "h": 32},
        "safeBottomHintPt": 34,
    },
}

SCREENS = [
    ("bill-pick", "① 选择顾客", "screen-pick", "会员/散客列表；取挂单入口；进点单台"),
    ("bill-bill", "② 点单台", "screen-bill", "文件夹 Tab 选卡/快消；价目；记账单；底栏应付"),
    ("bill-detail", "③ 结算确认", "screen-detail", "明细滑票；权益/优惠；去结账"),
    ("bill-cart", "已选", "cartSheetMask", "已选抽屉 Sheet"),
    ("bill-checkout", "结账方式", "checkoutMask", "客户扫我/我扫客户/开单"),
    ("bill-pay", "开单分账", "payMask", "支付渠道 + 确认支付"),
    ("bill-pay-price-changed", "价目变更拦截", "payAmountChangedMask", "居中 Dialog"),
    ("bill-success", "成功", "screen-success", "开单/办卡等成功页复用"),
    ("bill-scan-me", "客户扫我", "screen-scan-me", "收款码展码"),
    ("bill-scan-cust", "我扫客户", "screen-scan-cust", "扫码枪/摄像头"),
    ("bill-expand", "展卡", "screen-bill", "点单台展卡态"),
    ("bill-add-card", "添加卡", "screen-add-card", "开单侧办新卡/补录确认"),
    ("bill-add-card-group", "添加卡 · 选卡", "screen-add-card-pick", "选在售模板"),
    ("bill-card-asset", "充卡/续卡", "screen-bill-card-asset", "持卡资产操作"),
    ("bill-benefit", "选择权益", "screen-pick-benefit", "不使用权益/人工打折/卡权益"),
    ("bill-discount", "人工打折", "screen-discount", "整单人工折扣"),
    ("bill-hold", "挂单列表", "screen-holds", "取挂单；删除挂单"),
]


def ensure_dirs() -> None:
    for p in [
        OUT / "tokens",
        OUT / "android" / "values",
        OUT / "android" / "drawable-readme",
        OUT / "ios",
        OUT / "icons",
        OUT / "screens",
        OUT / "captures",
        OUT / "samples" / "android",
        OUT / "samples" / "ios",
    ]:
        p.mkdir(parents=True, exist_ok=True)


def write_tokens() -> None:
    (OUT / "tokens" / "design-tokens.json").write_text(
        json.dumps(TOKENS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def write_android_colors() -> None:
    c = TOKENS["color"]
    lines = ['<?xml version="1.0" encoding="utf-8"?>', "<resources>"]
    mapping = [
        ("brand", "brand"),
        ("brand_soft", "brandSoft"),
        ("brand_border", "brandBorder"),
        ("success", "success"),
        ("success_soft", "successSoft"),
        ("success_text", "successText"),
        ("bg_page", "bgPage"),
        ("surface", "surface"),
        ("text_primary", "textPrimary"),
        ("text_secondary", "textSecondary"),
        ("text_mid", "textMid"),
        ("text_strong", "textStrong"),
        ("border", "border"),
        ("border_light", "borderLight"),
        ("disabled", "disabled"),
        ("accent_orange", "accentOrange"),
        ("folder_tab_idle", "folderTabIdle"),
        ("folder_tab_idle_text", "folderTabIdleText"),
        ("continue_add", "continueAdd"),
        ("continue_add_active", "continueAddActive"),
        ("offer_none", "offerNone"),
        ("offer_manual", "offerManual"),
        ("slip_no_card", "slipNoCard"),
        ("trash", "trash"),
    ]
    for an, key in mapping:
        lines.append(f'    <color name="{an}">{c[key]}</color>')
    lines.append("</resources>")
    (OUT / "android" / "values" / "colors.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_android_dimens() -> None:
    lines = ['<?xml version="1.0" encoding="utf-8"?>', "<resources>"]
    lines.append("    <!-- Logical design width = 390dp -->")
    for v in TOKENS["spacing"]["scalePt"]:
        lines.append(f'    <dimen name="space_{v}">{v}dp</dimen>')
    for k, v in TOKENS["spacing"]["common"].items():
        lines.append(f'    <dimen name="space_{k}">{v}dp</dimen>')
    for k, v in TOKENS["radius"].items():
        if isinstance(v, list):
            continue
        name = "radius_pill" if k == "pill" else f"radius_{k}"
        lines.append(f'    <dimen name="{name}">{v if k != "pill" else 999}dp</dimen>')
    for k, v in TOKENS["typography"]["sizesPt"].items():
        lines.append(f'    <dimen name="text_{k}">{v}sp</dimen>')
    t = TOKENS["touch"]
    lines.append(f'    <dimen name="touch_min">{t["minHeightPt"]}dp</dimen>')
    lines.append(f'    <dimen name="nav_bar">{t["navBarHeightPt"]}dp</dimen>')
    lines.append(f'    <dimen name="btn_primary_h">{t["bottomPrimaryButtonHeightPt"]}dp</dimen>')
    lines.append(f'    <dimen name="folder_tab_h">{t["folderTabHeightPt"]}dp</dimen>')
    lines.append(f'    <dimen name="held_card_face_w">{t["heldCardFace"]["w"]}dp</dimen>')
    lines.append(f'    <dimen name="held_card_face_h">{t["heldCardFace"]["h"]}dp</dimen>')
    lines.append("    <dimen name=\"design_width\">390dp</dimen>")
    lines.append("</resources>")
    (OUT / "android" / "values" / "dimens.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_android_styles() -> None:
    content = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Text.Body">
        <item name="android:textSize">@dimen/text_body</item>
        <item name="android:textColor">@color/text_primary</item>
    </style>
    <style name="Text.Secondary">
        <item name="android:textSize">@dimen/text_subhead</item>
        <item name="android:textColor">@color/text_secondary</item>
    </style>
    <style name="Text.NavTitle">
        <item name="android:textSize">@dimen/text_title3</item>
        <item name="android:textStyle">bold</item>
        <item name="android:textColor">@color/text_strong</item>
    </style>
    <style name="Text.Amount">
        <item name="android:textSize">@dimen/text_title1</item>
        <item name="android:textColor">@color/text_strong</item>
    </style>
    <style name="Btn.Main">
        <item name="android:layout_height">@dimen/btn_primary_h</item>
        <item name="android:background">@color/brand</item>
        <item name="android:textColor">@android:color/white</item>
        <item name="android:textSize">@dimen/text_body</item>
        <item name="android:gravity">center</item>
        <item name="android:minHeight">@dimen/touch_min</item>
    </style>
    <style name="Btn.Secondary">
        <item name="android:layout_height">@dimen/btn_primary_h</item>
        <item name="android:background">@android:color/transparent</item>
        <item name="android:textColor">@color/brand</item>
        <item name="android:textSize">@dimen/text_body</item>
        <item name="android:minHeight">@dimen/touch_min</item>
    </style>
    <style name="Bill.FolderTab">
        <item name="android:layout_height">@dimen/folder_tab_h</item>
        <item name="android:textSize">@dimen/text_subhead</item>
        <item name="android:gravity">center</item>
    </style>
    <style name="Bill.ContinueAdd">
        <item name="android:textColor">@color/continue_add</item>
        <item name="android:textSize">@dimen/text_body</item>
        <item name="android:textStyle">bold</item>
    </style>
</resources>
"""
    (OUT / "android" / "values" / "styles.xml").write_text(content, encoding="utf-8")


def write_ios_tokens() -> None:
    c = TOKENS["color"]
    sizes = TOKENS["typography"]["sizesPt"]
    swift = f"""// DesignTokens.swift — 开单记账 · 方案 B
// Source: tokens/design-tokens.json · Do not invent colors/spacing outside this file.

import SwiftUI

enum AppColor {{
    static let brand = Color(hex: "{c['brand']}")
    static let brandSoft = Color(hex: "{c['brandSoft']}")
    static let brandBorder = Color(hex: "{c['brandBorder']}")
    static let success = Color(hex: "{c['success']}")
    static let bgPage = Color(hex: "{c['bgPage']}")
    static let surface = Color(hex: "{c['surface']}")
    static let textPrimary = Color(hex: "{c['textPrimary']}")
    static let textSecondary = Color(hex: "{c['textSecondary']}")
    static let textMid = Color(hex: "{c['textMid']}")
    static let textStrong = Color(hex: "{c['textStrong']}")
    static let border = Color(hex: "{c['border']}")
    static let borderLight = Color(hex: "{c['borderLight']}")
    static let accentOrange = Color(hex: "{c['accentOrange']}")
    static let folderTabIdle = Color(hex: "{c['folderTabIdle']}")
    static let folderTabIdleText = Color(hex: "{c['folderTabIdleText']}")
    static let continueAdd = Color(hex: "{c['continueAdd']}")
    static let offerNone = Color(hex: "{c['offerNone']}")
    static let offerManual = Color(hex: "{c['offerManual']}")
    static let slipNoCard = Color(hex: "{c['slipNoCard']}")
    static let trash = Color(hex: "{c['trash']}")
}}

enum AppSpace {{
    static let pageH: CGFloat = 16
    static let s4: CGFloat = 4
    static let s6: CGFloat = 6
    static let s8: CGFloat = 8
    static let s12: CGFloat = 12
    static let s16: CGFloat = 16
    static let s24: CGFloat = 24
    static let billActionGap: CGFloat = 30
    static let folderSlant: CGFloat = 18
}}

enum AppRadius {{
    static let sm: CGFloat = 6
    static let md: CGFloat = 8
    static let lg: CGFloat = 10
    static let xl: CGFloat = 12
    static let pill: CGFloat = 999
}}

enum AppFont {{
    static let caption: CGFloat = {sizes['caption']}
    static let footnote: CGFloat = {sizes['footnote']}
    static let subhead: CGFloat = {sizes['subhead']}
    static let body: CGFloat = {sizes['body']}
    static let title3: CGFloat = {sizes['title3']}
    static let title1: CGFloat = {sizes['title1']}
    static func text(_ size: CGFloat, weight: Font.Weight = .regular) -> Font {{
        .system(size: size, weight: weight)
    }}
    static func data(_ size: CGFloat, weight: Font.Weight = .regular) -> Font {{
        // Bundle TCloudNumber if available
        .system(size: size, weight: weight).monospacedDigit()
    }}
}}

extension Color {{
    init(hex: String) {{
        let h = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: h).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch h.count {{
        case 6: (a, r, g, b) = (255, int >> 16, int >> 8 & 0xff, int & 0xff)
        case 8: (a, r, g, b) = (int >> 24, int >> 16 & 0xff, int >> 8 & 0xff, int & 0xff)
        default: (a, r, g, b) = (255, 0, 0, 0)
        }}
        self.init(.sRGB, red: Double(r)/255, green: Double(g)/255, blue: Double(b)/255, opacity: Double(a)/255)
    }}
}}
"""
    (OUT / "ios" / "DesignTokens.swift").write_text(swift, encoding="utf-8")


def copy_icons() -> None:
    if not ASSETS.exists():
        return
    for src in ASSETS.rglob("*"):
        if src.suffix.lower() not in {".svg", ".png"}:
            continue
        # flatten with path hint in name
        rel = src.relative_to(ASSETS).as_posix().replace("/", "-")
        dst = OUT / "icons" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def write_icons_md() -> None:
    rows = [
        "# ICONS · 开单记账",
        "",
        "图标来自 `assets/billing/**`，已复制到本包 `icons/`（路径中的 `/` 换成 `-`）。",
        "",
        "| 文件 | 用途 | Android | SwiftUI Image |",
        "|------|------|---------|---------------|",
    ]
    for p in sorted((OUT / "icons").glob("*")):
        if p.suffix.lower() not in {".svg", ".png"}:
            continue
        stem = p.stem.replace("-", "_")
        rows.append(f"| {p.name} | 见文件名 | `ic_{stem}` | `{stem}` |")
    rows.extend(
        [
            "",
            "## 仍多为内联 SVG（需按截图导出补齐）",
            "",
            "导航返回、文件夹 Tab、垃圾桶、记账单折叠、金额键盘、Toast、权益/优惠面性图标等。",
            "对照 `captures/<flow>.png` 从 `demo.html` 导出后补入 `icons/`。",
            "",
            "## 字体",
            "",
            "金额：`card/assets/fonts/TCloudNumber/`",
            "",
        ]
    )
    (OUT / "ICONS.md").write_text("\n".join(rows), encoding="utf-8")
    (OUT / "android" / "drawable-readme" / "README.md").write_text(
        "将 `../../icons/*` 转为 VectorDrawable / bitmap 放入 `res/drawable/`，命名见 ICONS.md。\n",
        encoding="utf-8",
    )


def write_components() -> None:
    content = """# COMPONENTS · 开单记账

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
"""
    (OUT / "COMPONENTS.md").write_text(content, encoding="utf-8")


def write_screens() -> None:
    index = [
        "# SCREEN-INDEX · 开单记账",
        "",
        "| flow id | 标题 | 对照截图 | 规格 |",
        "|---------|------|----------|------|",
    ]
    for fid, title, screen, note in SCREENS:
        md = f"""# {title}

| 字段 | 值 |
|------|-----|
| flow | `{fid}` |
| 原型深链 | [`demo.html?flow={fid}&capture=1`](../demo.html?flow={fid}&capture=1) |
| 对照截图 | [`captures/{fid}.png`](../captures/{fid}.png) |
| DOM/Screen | `{screen}` |
| 说明 | {note} |

## 实现注意

1. 画布逻辑宽 **390pt**；`?capture=1` 时高度可随内容延伸。  
2. **不要**绘制原型假状态栏。  
3. Token：只用本包 `tokens/` → Android `values/*` / iOS `DesignTokens.swift`。  
4. 行为与文案：以 `demo.html?flow={fid}` 为准（尚无独立开单 PRD）。  
5. 图标：`ICONS.md`。

## Cursor 提示（可复制）

```
实现开单记账「{title}」（flow={fid}）。
平台：Android XML + iOS SwiftUI。
只使用 native-handoff-billing/tokens 与 COMPONENTS.md。
对照 captures/{fid}.png，禁止臆造间距/颜色/图标。
不要实现假 iOS 状态栏。
Toast 须相对画布居中。
```
"""
        (OUT / "screens" / f"{fid}.md").write_text(md, encoding="utf-8")
        index.append(f"| `{fid}` | {title} | [png](captures/{fid}.png) | [spec](screens/{fid}.md) |")
    (OUT / "SCREEN-INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")


def write_samples() -> None:
    xml = '''<?xml version="1.0" encoding="utf-8"?>
<!-- SAMPLE · 点单台 bill-bill · Token 用法示范 -->
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/root_bill_desk"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/bg_page">

    <LinearLayout
        android:id="@+id/nav_bar"
        android:layout_width="0dp"
        android:layout_height="@dimen/nav_bar"
        android:background="@color/surface"
        android:gravity="center_vertical"
        android:orientation="horizontal"
        android:paddingStart="@dimen/space_pageH"
        android:paddingEnd="@dimen/space_pageH"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent">
        <ImageButton
            android:id="@+id/btn_back"
            android:layout_width="@dimen/touch_min"
            android:layout_height="@dimen/touch_min"
            android:background="@android:color/transparent"
            android:contentDescription="@string/back" />
        <TextView
            android:id="@+id/tv_title"
            style="@style/Text.NavTitle"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:gravity="center"
            android:text="开单记账" />
        <View android:layout_width="@dimen/touch_min" android:layout_height="@dimen/touch_min" />
    </LinearLayout>

    <!-- 顾客条 -->
    <FrameLayout
        android:id="@+id/customer_header"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:padding="@dimen/space_pageH"
        app:layout_constraintTop_toBottomOf="@id/nav_bar"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent" />

    <!-- 文件夹 Tab + 选卡轨 / 快消 -->
    <LinearLayout
        android:id="@+id/bill_action"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:layout_marginStart="@dimen/space_pageH"
        android:layout_marginEnd="@dimen/space_pageH"
        app:layout_constraintTop_toBottomOf="@id/customer_header"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent">
        <LinearLayout
            android:id="@+id/folder_tabs"
            android:layout_width="match_parent"
            android:layout_height="@dimen/folder_tab_h"
            android:orientation="horizontal">
            <TextView style="@style/Bill.FolderTab" android:layout_width="0dp" android:layout_weight="1" android:text="选择会员卡" android:background="@color/surface" />
            <TextView style="@style/Bill.FolderTab" android:layout_width="0dp" android:layout_weight="1" android:text="快速消费" android:background="@color/folder_tab_idle" android:textColor="@color/folder_tab_idle_text" />
        </LinearLayout>
        <androidx.recyclerview.widget.RecyclerView
            android:id="@+id/rv_held_cards"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:background="@color/surface"
            android:padding="@dimen/space_12"
            android:clipToPadding="false" />
    </LinearLayout>

    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/rv_catalog_or_slips"
        android:layout_width="0dp"
        android:layout_height="0dp"
        android:padding="@dimen/space_pageH"
        app:layout_constraintTop_toBottomOf="@id/bill_action"
        app:layout_constraintBottom_toTopOf="@id/bottom_bar"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent" />

    <LinearLayout
        android:id="@+id/bottom_bar"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:gravity="center_vertical"
        android:padding="@dimen/space_bottomBarPad"
        android:background="@color/surface"
        android:elevation="4dp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent">
        <TextView android:id="@+id/tv_due_label" style="@style/Text.Secondary" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="应付" />
        <TextView android:id="@+id/tv_due" style="@style/Text.Amount" android:layout_width="0dp" android:layout_weight="1" android:layout_height="wrap_content" android:paddingStart="@dimen/space_8" android:text="¥0" />
        <Button android:id="@+id/btn_next" style="@style/Btn.Main" android:layout_width="120dp" android:text="去结账" />
    </LinearLayout>
</androidx.constraintlayout.widget.ConstraintLayout>
'''
    (OUT / "samples" / "android" / "fragment_bill_desk.xml").write_text(xml, encoding="utf-8")

    item = '''<?xml version="1.0" encoding="utf-8"?>
<!-- SAMPLE · 记账单行 -->
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:background="@color/surface"
    android:padding="@dimen/space_12"
    android:layout_marginBottom="@dimen/space_8">
    <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:gravity="center_vertical">
        <TextView android:id="@+id/tv_card" style="@style/Text.Body" android:layout_width="0dp" android:layout_weight="1" android:textColor="@color/slip_no_card" android:text="未选卡" />
        <ImageButton android:id="@+id/btn_del" android:layout_width="32dp" android:layout_height="32dp" android:background="@android:color/transparent" android:tint="@color/trash" android:contentDescription="删除记账单" />
    </LinearLayout>
    <LinearLayout android:id="@+id/lines" android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" />
    <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:gravity="center_vertical">
        <TextView style="@style/Text.Secondary" android:layout_width="0dp" android:layout_weight="1" android:text="共 N 项" />
        <TextView android:id="@+id/tv_total" style="@style/Text.Amount" android:layout_width="wrap_content" android:layout_height="wrap_content" />
    </LinearLayout>
</LinearLayout>
'''
    (OUT / "samples" / "android" / "item_bill_slip.xml").write_text(item, encoding="utf-8")

    swift = '''// BillDeskView.swift — SAMPLE · 点单台（bill-bill）
// 对照：screens/bill-bill.md + captures/bill-bill.png

import SwiftUI

struct BillDeskView: View {
    enum ActionTab: String { case card = "选择会员卡"; case quick = "快速消费" }
    @State private var tab: ActionTab = .card
    var onBack: () -> Void = {}
    var onCheckout: () -> Void = {}

    var body: some View {
        VStack(spacing: 0) {
            HStack {
                Button(action: onBack) { Image(systemName: "chevron.left") }
                    .frame(width: 44, height: 44)
                Spacer()
                Text("开单记账")
                    .font(AppFont.text(AppFont.title3, weight: .semibold))
                    .foregroundStyle(AppColor.textStrong)
                Spacer()
                Color.clear.frame(width: 44, height: 44)
            }
            .padding(.horizontal, AppSpace.pageH)
            .background(AppColor.surface)

            // Customer header placeholder
            RoundedRectangle(cornerRadius: AppRadius.xl)
                .fill(AppColor.surface)
                .frame(height: 72)
                .padding(.horizontal, AppSpace.pageH)
                .padding(.top, AppSpace.s8)

            VStack(spacing: 0) {
                HStack(spacing: 0) {
                    folderTab(.card)
                    folderTab(.quick)
                }
                .frame(height: 36)
                if tab == .card {
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: AppSpace.billActionGap) {
                            ForEach(0..<4, id: \\.self) { _ in
                                VStack(spacing: 6) {
                                    RoundedRectangle(cornerRadius: 5)
                                        .stroke(AppColor.borderLight)
                                        .frame(width: 48, height: 32)
                                    Text("卡名")
                                        .font(AppFont.text(AppFont.caption, weight: .medium))
                                        .foregroundStyle(AppColor.textStrong)
                                        .frame(width: 68)
                                }
                            }
                        }
                        .padding(AppSpace.s12)
                    }
                } else {
                    HStack {
                        Text("输入消费金额")
                            .foregroundStyle(AppColor.textSecondary)
                        Spacer()
                        Text("添加").foregroundStyle(AppColor.brand)
                    }
                    .padding(AppSpace.s12)
                }
            }
            .background(AppColor.surface)
            .clipShape(RoundedRectangle(cornerRadius: AppRadius.xl))
            .padding(.horizontal, AppSpace.pageH)
            .padding(.top, AppSpace.s12)

            Spacer()

            HStack {
                Text("应付").font(AppFont.text(AppFont.subhead)).foregroundStyle(AppColor.textSecondary)
                Text("¥0").font(AppFont.data(AppFont.title1, weight: .semibold))
                Spacer()
                Button("去结账", action: onCheckout)
                    .frame(width: 120, height: 44)
                    .background(AppColor.brand)
                    .foregroundStyle(.white)
                    .clipShape(RoundedRectangle(cornerRadius: AppRadius.xl))
            }
            .padding(AppSpace.s16)
            .background(AppColor.surface)
        }
        .background(AppColor.bgPage)
    }

    private func folderTab(_ t: ActionTab) -> some View {
        Button {
            tab = t
        } label: {
            Text(t.rawValue)
                .font(AppFont.text(AppFont.subhead, weight: tab == t ? .semibold : .medium))
                .foregroundStyle(tab == t ? AppColor.textStrong : AppColor.folderTabIdleText)
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .background(tab == t ? AppColor.surface : AppColor.folderTabIdle)
        }
        .buttonStyle(.plain)
    }
}
'''
    (OUT / "samples" / "ios" / "BillDeskView.swift").write_text(swift, encoding="utf-8")


def write_readme() -> None:
    content = """# 开单记账 · Native Handoff（方案 B）

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
"""
    (OUT / "README.md").write_text(content, encoding="utf-8")


def main() -> int:
    ensure_dirs()
    write_tokens()
    write_android_colors()
    write_android_dimens()
    write_android_styles()
    write_ios_tokens()
    copy_icons()
    write_icons_md()
    write_components()
    write_screens()
    write_samples()
    write_readme()
    print(f"Wrote package -> {OUT}")
    print(f"Screens: {len(SCREENS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
