# -*- coding: utf-8 -*-
"""Generate native handoff package for membership-card (Android XML + iOS SwiftUI)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "native-handoff-member-card"

CARD_COLORS = {
    "peach": {
        "label": "蜜桃色",
        "gradient": ["#F4EAE5", "#EED1C3"],
        "accent": "#C4A394",
        "vipBg": "#E2D0C6",
        "vipText": "#694E42",
    },
    "mint": {
        "label": "薄荷绿",
        "gradient": ["#EDF2E9", "#B1CD9B"],
        "accent": "#9DAF93",
        "vipBg": "#CFDFC3",
        "vipText": "#617258",
    },
    "haze": {
        "label": "雾霾蓝",
        "gradient": ["#E9F0F3", "#C0DCE9"],
        "accent": "#8FA4AF",
        "vipBg": "#CED8DF",
        "vipText": "#405660",
    },
    "taro": {
        "label": "香芋紫",
        "gradient": ["#F0EBF3", "#CFBCDA"],
        "accent": "#A89CAF",
        "vipBg": "#DCD3E0",
        "vipText": "#574861",
    },
    "milk": {
        "label": "奶茶色",
        "gradient": ["#F4EEE3", "#DFC9A1"],
        "accent": "#B6A57A",
        "vipBg": "#E0D8C1",
        "vipText": "#5D5435",
    },
}

TOKENS = {
    "meta": {
        "scope": "membership-card-only",
        "canvas": {"width": 390, "height": 844, "unit": "pt"},
        "source": "card/demo.html (extracted, no Figma)",
        "platforms": ["Android XML", "iOS SwiftUI"],
        "conflictRule": [
            "Visual: capture PNG at ?flow=&capture=1 (390 logical width, scale=1)",
            "Behavior/copy/state: PRD-会员卡管理.md + demo.html",
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
        "textStrong": "#1A1A1A",
        "border": "#D7D7D5",
        "disabled": "#EDEDED",
        "cardDivider": "rgba(0,0,0,0.04)",
        "infoBg": "#E7F1FF",
        "infoText": "#1A70FE",
        "warnBg": "#FFF8E6",
        "warnText": "#E37318",
        "neutralBg": "#EDEDED",
        "neutralText": "#929292",
        "switchIncludeOn": "#34C759",
        "switchQtyOn": "#FF7043",
        "shellChrome": "#E8EAED",
    },
    "typography": {
        "fontText": {
            "ios": "PingFang SC",
            "android": "sans-serif",
            "note": "Prototype also cites Source Han Sans SC; prefer PingFang on iOS, system sans on Android",
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
        "scalePt": [0, 2, 4, 6, 8, 10, 12, 14, 16, 20, 24, 32, 40, 48],
        "common": {
            "pageH": 16,
            "sectionGap": 12,
            "rowV": 14,
            "rowH": 16,
            "chipHPad": 12,
            "bottomBarPad": 16,
            "sheetTopPad": 20,
            "listCardGap": 12,
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
    },
    "touch": {
        "minHeightPt": 44,
        "navBarHeightPt": 44,
        "bottomPrimaryButtonHeightPt": 44,
        "safeBottomHintPt": 34,
    },
    "cardFaceThemes": CARD_COLORS,
}

SCREENS = [
    ("list-active", "会员卡列表 · 在售", "screen0", "主列表；分组筛选；footer 复制/快速分组/办卡退卡"),
    ("list-shelved", "会员卡列表 · 已下架", "screen0", "已下架 Tab；footer 无办卡"),
    ("card-groups", "分组管理", "screen-card-groups", "拖排序；新建；行菜单"),
    ("card-group-members", "编辑成员", "screen-card-group-members", "多选卡入组"),
    ("card-group-create", "新建分组 Dialog", "screen-card-groups", "名称≤20，不可重名"),
    ("card-item-group", "设置分组 Sheet", "screen0", "一卡多组"),
    ("detail-active", "会员卡详情 · 在售", "screen6", "顶栏下架/编辑；运营数据+卡面"),
    ("detail-shelved", "会员卡详情 · 已下架", "screen6", "底栏重新上架|已持卡管理"),
    ("create-step1", "Step1 基本信息", "screen10", "名称/购买金额/有效期/卡面色"),
    ("create-step2", "Step2 权益组合", "screen9", "面值/项目/产品/折扣开关"),
    ("create-step3", "Step3 用卡策略", "screen11", "退卡规则+业绩规则"),
    ("create-success", "创建成功", "screen7", "返回列表|立即办卡"),
    ("issue-success", "办卡成功", "screen8", "返回列表|继续办卡"),
    ("pick-projects", "添加项目权益", "screen2", "价目项目+计次参数"),
    ("pick-products", "添加产品权益", "screen2p", "行内数量"),
    ("pick-discount-list", "添加折扣权益", "screen4", "标尺/固定金额"),
    ("card-issue-new", "选择会员 · 办卡", "overlay", "单选→去结账"),
    ("card-quick-issue", "确认办卡", "screen-quick-issue", "选服务员工"),
    ("card-issue-holders", "选择会员 · 退卡/延期", "overlay", "持卡管理"),
    ("card-extend", "延期行内面板", "overlay", "时长+参考费用"),
    ("card-refund", "退卡估值 Sheet", "overlay", "建议退款可改"),
    ("card-shelf", "下架确认", "overlay", "Dialog"),
    ("card-reshelf", "重新上架确认", "overlay", "Dialog"),
    ("card-stats-help", "运营数据说明", "overlay", "Dialog"),
    ("card-unlimited-validity", "永久转有限", "overlay", "不限次冲突"),
]


def write_tokens_json() -> None:
    path = OUT / "tokens" / "design-tokens.json"
    path.write_text(json.dumps(TOKENS, ensure_ascii=False, indent=2), encoding="utf-8")


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
        ("text_strong", "textStrong"),
        ("border", "border"),
        ("disabled", "disabled"),
        ("info_bg", "infoBg"),
        ("info_text", "infoText"),
        ("warn_bg", "warnBg"),
        ("warn_text", "warnText"),
        ("neutral_bg", "neutralBg"),
        ("neutral_text", "neutralText"),
        ("switch_include_on", "switchIncludeOn"),
        ("switch_qty_on", "switchQtyOn"),
    ]
    for android_name, key in mapping:
        lines.append(f'    <color name="{android_name}">{c[key]}</color>')
    # card themes
    for theme, vals in CARD_COLORS.items():
        lines.append(f'    <color name="card_{theme}_accent">{vals["accent"]}</color>')
        lines.append(f'    <color name="card_{theme}_vip_bg">{vals["vipBg"]}</color>')
        lines.append(f'    <color name="card_{theme}_vip_text">{vals["vipText"]}</color>')
        lines.append(f'    <color name="card_{theme}_grad_start">{vals["gradient"][0]}</color>')
        lines.append(f'    <color name="card_{theme}_grad_end">{vals["gradient"][1]}</color>')
    lines.append("</resources>")
    (OUT / "android" / "values" / "colors.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_android_dimens() -> None:
    lines = ['<?xml version="1.0" encoding="utf-8"?>', "<resources>"]
    # design width reference: 390dp
    lines.append("    <!-- Logical design width = 390dp; implement on phone with match_parent + these dens. -->")
    for i, v in enumerate(TOKENS["spacing"]["scalePt"]):
        lines.append(f'    <dimen name="space_{v}">{v}dp</dimen>')
    common = TOKENS["spacing"]["common"]
    for k, v in common.items():
        lines.append(f'    <dimen name="space_{k}">{v}dp</dimen>')
    for k, v in TOKENS["radius"].items():
        if isinstance(v, list):
            continue
        if k == "pill":
            lines.append(f'    <dimen name="radius_pill">999dp</dimen>')
        else:
            lines.append(f'    <dimen name="radius_{k}">{v}dp</dimen>')
    for k, v in TOKENS["typography"]["sizesPt"].items():
        lines.append(f'    <dimen name="text_{k}">{v}sp</dimen>')
    lines.append(f'    <dimen name="touch_min">{TOKENS["touch"]["minHeightPt"]}dp</dimen>')
    lines.append(f'    <dimen name="nav_bar">{TOKENS["touch"]["navBarHeightPt"]}dp</dimen>')
    lines.append(f'    <dimen name="btn_primary_h">{TOKENS["touch"]["bottomPrimaryButtonHeightPt"]}dp</dimen>')
    lines.append(f'    <dimen name="design_width">390dp</dimen>')
    lines.append("</resources>")
    (OUT / "android" / "values" / "dimens.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_android_styles() -> None:
    content = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!-- Membership-card core styles · map from prototype classes -->

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
    <style name="Text.Amount" parent="Text.Body">
        <!-- Bind TCloudNumber via fontFamily if bundled -->
        <item name="android:textSize">@dimen/text_title1</item>
    </style>

    <!-- btn-main -->
    <style name="Btn.Main">
        <item name="android:layout_height">@dimen/btn_primary_h</item>
        <item name="android:background">@color/brand</item>
        <item name="android:textColor">@android:color/white</item>
        <item name="android:textSize">@dimen/text_body</item>
        <item name="android:gravity">center</item>
        <item name="android:minHeight">@dimen/touch_min</item>
    </style>
    <!-- card-face-act--solid -->
    <style name="Btn.CardFace.Solid" parent="Btn.Main">
        <item name="android:paddingLeft">@dimen/space_12</item>
        <item name="android:paddingRight">@dimen/space_12</item>
    </style>
    <!-- card-face-act--outline -->
    <style name="Btn.CardFace.Outline">
        <item name="android:layout_height">@dimen/btn_primary_h</item>
        <item name="android:background">@android:color/transparent</item>
        <item name="android:textColor">@color/text_primary</item>
        <item name="android:textSize">@dimen/text_body</item>
        <item name="android:minHeight">@dimen/touch_min</item>
    </style>

    <!-- form-row -->
    <style name="Form.Row">
        <item name="android:paddingTop">@dimen/space_rowV</item>
        <item name="android:paddingBottom">@dimen/space_rowV</item>
        <item name="android:paddingLeft">@dimen/space_rowH</item>
        <item name="android:paddingRight">@dimen/space_rowH</item>
        <item name="android:background">@color/surface</item>
        <item name="android:minHeight">@dimen/touch_min</item>
    </style>

    <!-- page-tabs / shelf segment -->
    <style name="Tab.Shelf">
        <item name="android:textSize">@dimen/text_body</item>
        <item name="android:minHeight">@dimen/touch_min</item>
    </style>
</resources>
'''
    (OUT / "android" / "values" / "styles.xml").write_text(content, encoding="utf-8")


def write_ios_tokens() -> None:
    c = TOKENS["color"]
    lines = [
        "// DesignTokens.swift — membership card · generated from prototype (no Figma)",
        "// Canvas: 390×844 pt. Do not hardcode magic numbers outside this file.",
        "import SwiftUI",
        "",
        "enum AppColor {",
    ]
    swift_map = [
        ("brand", "brand"),
        ("brandSoft", "brandSoft"),
        ("brandBorder", "brandBorder"),
        ("success", "success"),
        ("successSoft", "successSoft"),
        ("bgPage", "bgPage"),
        ("surface", "surface"),
        ("textPrimary", "textPrimary"),
        ("textSecondary", "textSecondary"),
        ("textStrong", "textStrong"),
        ("border", "border"),
        ("disabled", "disabled"),
        ("infoBg", "infoBg"),
        ("infoText", "infoText"),
        ("warnBg", "warnBg"),
        ("warnText", "warnText"),
    ]
    for name, key in swift_map:
        hexv = c[key].lstrip("#")
        lines.append(f'    static let {name} = Color(hex: "{hexv}")')
    lines += [
        "}",
        "",
        "enum AppSpace {",
    ]
    for v in TOKENS["spacing"]["scalePt"]:
        lines.append(f"    static let s{v}: CGFloat = {v}")
    for k, v in TOKENS["spacing"]["common"].items():
        lines.append(f"    static let {k}: CGFloat = {v}")
    lines += [
        "}",
        "",
        "enum AppRadius {",
        "    static let xs: CGFloat = 4",
        "    static let sm: CGFloat = 6",
        "    static let md: CGFloat = 8",
        "    static let lg: CGFloat = 10",
        "    static let xl: CGFloat = 12",
        "    static let xxl: CGFloat = 16",
        "    static let pill: CGFloat = 999",
        "}",
        "",
        "enum AppFont {",
        "    static func text(_ size: CGFloat, weight: Font.Weight = .regular) -> Font {",
        "        .system(size: size, weight: weight)",
        "        // Prefer PingFang SC if registered: Font.custom(\"PingFangSC-Regular\", size: size)",
        "    }",
        "    static func data(_ size: CGFloat, weight: Font.Weight = .regular) -> Font {",
        "        // Bundle TCloudNumber-*.ttf then: Font.custom(\"TCloudNumber\", size: size)",
        "        .system(size: size, weight: weight).monospacedDigit()",
        "    }",
        "    static let caption: CGFloat = 11",
        "    static let footnote: CGFloat = 12",
        "    static let subhead: CGFloat = 13",
        "    static let body: CGFloat = 14",
        "    static let callout: CGFloat = 15",
        "    static let headline: CGFloat = 16",
        "    static let title3: CGFloat = 17",
        "    static let title2: CGFloat = 18",
        "    static let title1: CGFloat = 20",
        "}",
        "",
        "struct CardFaceTheme: Equatable {",
        "    let id: String",
        "    let label: String",
        "    let gradStart: Color",
        "    let gradEnd: Color",
        "    let accent: Color",
        "    let vipBg: Color",
        "    let vipText: Color",
        "}",
        "",
        "enum CardFaceThemes {",
        "    static let all: [CardFaceTheme] = [",
    ]
    for tid, vals in CARD_COLORS.items():
        lines.append(
            f'        .init(id: "{tid}", label: "{vals["label"]}", '
            f'gradStart: Color(hex: "{vals["gradient"][0].lstrip("#")}"), '
            f'gradEnd: Color(hex: "{vals["gradient"][1].lstrip("#")}"), '
            f'accent: Color(hex: "{vals["accent"].lstrip("#")}"), '
            f'vipBg: Color(hex: "{vals["vipBg"].lstrip("#")}"), '
            f'vipText: Color(hex: "{vals["vipText"].lstrip("#")}")),'
        )
    lines += [
        "    ]",
        '    static var `default`: CardFaceTheme { all.first { $0.id == "peach" }! }',
        "}",
        "",
        "extension Color {",
        "    init(hex: String) {",
        "        let scanner = Scanner(string: hex)",
        "        var rgb: UInt64 = 0",
        "        scanner.scanHexInt64(&rgb)",
        "        let r = Double((rgb >> 16) & 0xFF) / 255",
        "        let g = Double((rgb >> 8) & 0xFF) / 255",
        "        let b = Double(rgb & 0xFF) / 255",
        "        self.init(.sRGB, red: r, green: g, blue: b, opacity: 1)",
        "    }",
        "}",
        "",
    ]
    (OUT / "ios" / "DesignTokens.swift").write_text("\n".join(lines), encoding="utf-8")


def write_icons_md() -> None:
    content = """# 图标清单 · 会员卡管理

来源：`card/assets/`（已复制到本目录 `icons/`）。  
**规则：** Cursor 实现时只用本清单文件名；禁止用截图当图标；内联 SVG 若未列出则对照截图后导出补齐。

| 文件（handoff/icons） | 用途 | Android 建议名 | SwiftUI 建议 Image |
|----------------------|------|----------------|-------------------|
| member-card-clone.svg | 列表 footer「复制建卡」 | `ic_member_card_clone` | `memberCardClone` |
| member-card-vip.svg | （可选）VIP 角标矢量；原型多用色块字 VIP | `ic_member_card_vip` | `memberCardVip` |
| benefit-card-trash.svg | Step2 权益 ticket 删除 | `ic_benefit_trash` | `benefitTrash` |
| catalog-group-check-off.svg | 设置分组未选 | `ic_group_check_off` | `groupCheckOff` |
| catalog-group-check-on.svg | 设置分组已选 | `ic_group_check_on` | `groupCheckOn` |
| catalog-group-drag.svg | 分组管理拖手柄 | `ic_group_drag` | `groupDrag` |
| catalog-group-drag-line.svg | 拖拽装饰 | `ic_group_drag_line` | `groupDragLine` |
| catalog-group-drag-line-mid.svg | 拖拽装饰 | `ic_group_drag_line_mid` | `groupDragLineMid` |
| catalog-group-empty-lines.svg | 分组空态装饰 | `ic_group_empty_lines` | `groupEmptyLines` |
| catalog-member-check-off.svg | 编辑成员未选 | `ic_member_check_off` | `memberCheckOff` |
| catalog-member-check-on.svg | 编辑成员已选 | `ic_member_check_on` | `memberCheckOn` |
| catalog-hint-close.svg | 提示关闭 | `ic_hint_close` | `hintClose` |
| catalog-bound-card.svg | 绑卡相关提示 | `ic_bound_card` | `boundCard` |
| catalog-empty-box.svg | 空态盒 | `ic_empty_box` | `emptyBox` |

## 仍多为内联 SVG（需按截图导出补齐）

导航返回、帮助 `?`、Sheet 关闭、Segment 指示、金额键盘删除、成功勾选等。实现时：

1. 打开 `captures/<flow>.png` 对照  
2. 从 `demo.html` 搜索对应 `<svg` 导出到 `icons/`  
3. 转 Android Vector / 加入 Asset Catalog  

## 字体

金额数字：打包 `card/assets/fonts/TCloudNumber/`（Light/Regular/Bold）。
"""
    (OUT / "ICONS.md").write_text(content, encoding="utf-8")
    (OUT / "android" / "drawable-readme" / "README.md").write_text(
        "将 `../../icons/*.svg` 转为 VectorDrawable 放入工程 `res/drawable/`，命名见 ICONS.md。\n",
        encoding="utf-8",
    )


def write_components_md() -> None:
    content = """# COMPONENTS · 会员卡管理

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
"""
    (OUT / "COMPONENTS.md").write_text(content, encoding="utf-8")


def write_screens() -> None:
    index_rows = ["# SCREEN-INDEX · 会员卡管理", "", "| flow id | 标题 | 对照截图 | 规格 |", "|---------|------|----------|------|"]
    for fid, title, screen, note in SCREENS:
        md = f"""# {title}

| 字段 | 值 |
|------|-----|
| flow | `{fid}` |
| 原型深链 | [`demo.html?flow={fid}&capture=1`](../demo.html?flow={fid}&capture=1) |
| 对照截图 | [`captures/{fid}.png`](../captures/{fid}.png)（若缺失则先跑 capture 脚本） |
| DOM/Screen | `{screen}` |
| 说明 | {note} |

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
实现会员卡「{title}」（flow={fid}）。
平台：Android XML + iOS SwiftUI。
只使用 native-handoff-member-card/tokens 与 COMPONENTS.md。
对照 captures/{fid}.png，禁止臆造间距/颜色/图标。
不要实现假 iOS 状态栏。
```
"""
        (OUT / "screens" / f"{fid}.md").write_text(md, encoding="utf-8")
        index_rows.append(f"| `{fid}` | {title} | [png](captures/{fid}.png) | [spec](screens/{fid}.md) |")
    (OUT / "SCREEN-INDEX.md").write_text("\n".join(index_rows) + "\n", encoding="utf-8")


def write_sample_android() -> None:
    xml = '''<?xml version="1.0" encoding="utf-8"?>
<!-- SAMPLE ONLY · 会员卡列表在售 · 示范命名与 Token 用法，非完整可运行工程 -->
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/root_card_list"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@color/bg_page">

    <LinearLayout
        android:id="@+id/nav_bar"
        android:layout_width="0dp"
        android:layout_height="@dimen/nav_bar"
        android:gravity="center_vertical"
        android:orientation="horizontal"
        android:paddingStart="@dimen/space_pageH"
        android:paddingEnd="@dimen/space_pageH"
        android:background="@color/surface"
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
            android:text="会员卡管理" />

        <View
            android:layout_width="@dimen/touch_min"
            android:layout_height="@dimen/touch_min" />
    </LinearLayout>

    <!-- 在售 | 已下架 -->
    <com.google.android.material.tabs.TabLayout
        android:id="@+id/tab_shelf"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:background="@color/surface"
        app:layout_constraintTop_toBottomOf="@id/nav_bar"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent" />

    <!-- 分组筛选轨 -->
    <HorizontalScrollView
        android:id="@+id/group_bar"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:scrollbars="none"
        android:paddingStart="@dimen/space_pageH"
        android:paddingEnd="@dimen/space_8"
        app:layout_constraintTop_toBottomOf="@id/tab_shelf"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent" />

    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/rv_cards"
        android:layout_width="0dp"
        android:layout_height="0dp"
        android:clipToPadding="false"
        android:padding="@dimen/space_pageH"
        app:layout_constraintTop_toBottomOf="@id/group_bar"
        app:layout_constraintBottom_toTopOf="@id/bottom_bar"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent" />

    <FrameLayout
        android:id="@+id/bottom_bar"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:padding="@dimen/space_bottomBarPad"
        android:background="@color/surface"
        android:elevation="4dp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent">

        <Button
            android:id="@+id/btn_add_card"
            style="@style/Btn.Main"
            android:layout_width="match_parent"
            android:text="添加会员卡" />
    </FrameLayout>
</androidx.constraintlayout.widget.ConstraintLayout>
'''
    (OUT / "samples" / "android" / "fragment_card_list.xml").write_text(xml, encoding="utf-8")

    item = '''<?xml version="1.0" encoding="utf-8"?>
<!-- SAMPLE · item_member_card.xml · 对照 COMPONENTS MemberCardRow -->
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:layout_marginBottom="@dimen/space_listCardGap"
    android:background="@color/surface">

    <RelativeLayout
        android:id="@+id/header_compact"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:padding="@dimen/space_12">
        <!-- gradient background set in code from card_*_grad_* -->
        <TextView android:id="@+id/tv_vip" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="VIP" />
        <TextView android:id="@+id/tv_name" style="@style/Text.Body" android:layout_toEndOf="@id/tv_vip" android:layout_width="wrap_content" android:layout_height="wrap_content" />
        <TextView android:id="@+id/tv_price" style="@style/Text.Amount" android:layout_alignParentEnd="true" android:layout_width="wrap_content" android:layout_height="wrap_content" />
    </RelativeLayout>

    <LinearLayout
        android:id="@+id/panel_face"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="@dimen/space_12" />

    <LinearLayout
        android:id="@+id/footer_actions"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:padding="@dimen/space_12">
        <Button android:id="@+id/btn_clone" style="@style/Btn.CardFace.Outline" android:layout_width="wrap_content" android:text="复制建卡" />
        <View android:layout_width="0dp" android:layout_height="0dp" android:layout_weight="1" />
        <Button android:id="@+id/btn_group" style="@style/Btn.CardFace.Outline" android:layout_width="wrap_content" android:text="快速分组" />
        <Button android:id="@+id/btn_issue" style="@style/Btn.CardFace.Solid" android:layout_width="wrap_content" android:text="办卡/退卡" />
    </LinearLayout>
</LinearLayout>
'''
    (OUT / "samples" / "android" / "item_member_card.xml").write_text(item, encoding="utf-8")


def write_sample_ios() -> None:
    swift = '''// CardListView.swift — SAMPLE SwiftUI · 会员卡列表（在售）
// 对照：screens/list-active.md + captures/list-active.png
// 仅示范结构与 Token；数据层请接真实 API。

import SwiftUI

struct MemberCardListItem: Identifiable {
    let id: String
    let name: String
    let priceText: String
    let themeId: String
    let shelved: Bool
}

struct CardListView: View {
    enum ShelfTab: String, CaseIterable { case active = "在售"; case shelved = "已下架" }

    @State private var shelf: ShelfTab = .active
    @State private var activeGroupId: String = "all"
    let groups: [(id: String, name: String)]
    let cards: [MemberCardListItem]
    var onBack: () -> Void = {}
    var onAdd: () -> Void = {}
    var onOpen: (String) -> Void = { _ in }
    var onClone: (String) -> Void = { _ in }
    var onQuickGroup: (String) -> Void = { _ in }
    var onIssue: (String) -> Void = { _ in }
    var onManageGroups: () -> Void = {}

    var body: some View {
        VStack(spacing: 0) {
            HStack {
                Button(action: onBack) { Image(systemName: "chevron.left") }
                    .frame(width: 44, height: 44)
                Spacer()
                Text("会员卡管理")
                    .font(AppFont.text(AppFont.title3, weight: .semibold))
                    .foregroundStyle(AppColor.textStrong)
                Spacer()
                Color.clear.frame(width: 44, height: 44)
            }
            .padding(.horizontal, AppSpace.pageH)
            .background(AppColor.surface)

            Picker("", selection: $shelf) {
                ForEach(ShelfTab.allCases, id: \\.self) { Text($0.rawValue).tag($0) }
            }
            .pickerStyle(.segmented)
            .padding(.horizontal, AppSpace.pageH)
            .padding(.vertical, AppSpace.s8)
            .background(AppColor.surface)

            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: AppSpace.s8) {
                    ForEach([("all", "全部")] + groups, id: \\.0) { id, name in
                        Button(name) { activeGroupId = id }
                            .font(AppFont.text(AppFont.body, weight: activeGroupId == id ? .semibold : .regular))
                            .foregroundStyle(activeGroupId == id ? AppColor.brand : AppColor.textSecondary)
                    }
                    Button(action: onManageGroups) {
                        Image(systemName: "gearshape")
                    }
                }
                .padding(.horizontal, AppSpace.pageH)
            }
            .padding(.vertical, AppSpace.s8)

            ScrollView {
                LazyVStack(spacing: AppSpace.listCardGap) {
                    ForEach(cards) { card in
                        MemberCardRow(
                            item: card,
                            showIssue: shelf == .active,
                            onOpen: { onOpen(card.id) },
                            onClone: { onClone(card.id) },
                            onQuickGroup: { onQuickGroup(card.id) },
                            onIssue: { onIssue(card.id) }
                        )
                    }
                }
                .padding(AppSpace.pageH)
            }

            PrimaryButton(title: "添加会员卡", action: onAdd)
                .padding(AppSpace.bottomBarPad)
                .background(AppColor.surface)
        }
        .background(AppColor.bgPage)
    }
}

struct MemberCardRow: View {
    let item: MemberCardListItem
    var showIssue: Bool = true
    var onOpen: () -> Void
    var onClone: () -> Void
    var onQuickGroup: () -> Void
    var onIssue: () -> Void

    private var theme: CardFaceTheme {
        CardFaceThemes.all.first { $0.id == item.themeId } ?? .default
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            Button(action: onOpen) {
                HStack {
                    Text("VIP")
                        .font(AppFont.text(10, weight: .bold))
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(theme.vipBg)
                        .foregroundStyle(theme.vipText)
                        .clipShape(RoundedRectangle(cornerRadius: AppRadius.xs))
                    Text(item.name)
                        .font(AppFont.text(AppFont.body, weight: .semibold))
                        .foregroundStyle(AppColor.textStrong)
                    if item.shelved {
                        Text("已下架")
                            .font(AppFont.text(AppFont.caption))
                            .foregroundStyle(AppColor.textSecondary)
                    }
                    Spacer()
                    Text(item.priceText)
                        .font(AppFont.data(AppFont.title1))
                        .foregroundStyle(AppColor.textStrong)
                }
                .padding(AppSpace.s12)
                .background(
                    LinearGradient(colors: [theme.gradStart, theme.gradEnd], startPoint: .leading, endPoint: .trailing)
                )
            }
            .buttonStyle(.plain)

            // Face panel: bind real benefit lines from ViewModel
            Color.clear.frame(height: 8)

            HStack {
                Button(action: onClone) {
                    Label("复制建卡", image: "memberCardClone")
                }
                Spacer()
                Button("快速分组", action: onQuickGroup)
                if showIssue {
                    Button("办卡/退卡", action: onIssue)
                        .buttonStyle(.borderedProminent)
                        .tint(AppColor.brand)
                }
            }
            .padding(AppSpace.s12)
        }
        .background(AppColor.surface)
        .clipShape(RoundedRectangle(cornerRadius: AppRadius.xl))
    }
}

struct PrimaryButton: View {
    let title: String
    var action: () -> Void
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(AppFont.text(AppFont.body, weight: .semibold))
                .foregroundStyle(.white)
                .frame(maxWidth: .infinity)
                .frame(height: 44)
                .background(AppColor.brand)
                .clipShape(RoundedRectangle(cornerRadius: AppRadius.xl))
        }
    }
}
'''
    # Fix double-escaped backslashes from writing in Python string - I used \\. which becomes \. in file - good for Swift
    (OUT / "samples" / "ios" / "CardListView.swift").write_text(swift.replace("\\\\", "\\"), encoding="utf-8")


def write_readme() -> None:
    content = """# 会员卡管理 · Native Handoff（方案 B）

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
"""
    (OUT / "README.md").write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    write_tokens_json()
    write_android_colors()
    write_android_dimens()
    write_android_styles()
    write_ios_tokens()
    write_icons_md()
    write_components_md()
    write_screens()
    write_sample_android()
    write_sample_ios()
    write_readme()
    print("Generated under", OUT)


if __name__ == "__main__":
    main()
