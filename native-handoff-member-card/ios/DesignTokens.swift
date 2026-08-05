// DesignTokens.swift — membership card · generated from prototype (no Figma)
// Canvas: 390×844 pt. Do not hardcode magic numbers outside this file.
import SwiftUI

enum AppColor {
    static let brand = Color(hex: "F32F41")
    static let brandSoft = Color(hex: "FFF2F2")
    static let brandBorder = Color(hex: "FFD5D9")
    static let success = Color(hex: "2BA471")
    static let successSoft = Color(hex: "E8F8F2")
    static let bgPage = Color(hex: "F7F7F7")
    static let surface = Color(hex: "FFFFFF")
    static let textPrimary = Color(hex: "333333")
    static let textSecondary = Color(hex: "929292")
    static let textStrong = Color(hex: "1A1A1A")
    static let border = Color(hex: "D7D7D5")
    static let disabled = Color(hex: "EDEDED")
    static let infoBg = Color(hex: "E7F1FF")
    static let infoText = Color(hex: "1A70FE")
    static let warnBg = Color(hex: "FFF8E6")
    static let warnText = Color(hex: "E37318")
}

enum AppSpace {
    static let s0: CGFloat = 0
    static let s2: CGFloat = 2
    static let s4: CGFloat = 4
    static let s6: CGFloat = 6
    static let s8: CGFloat = 8
    static let s10: CGFloat = 10
    static let s12: CGFloat = 12
    static let s14: CGFloat = 14
    static let s16: CGFloat = 16
    static let s20: CGFloat = 20
    static let s24: CGFloat = 24
    static let s32: CGFloat = 32
    static let s40: CGFloat = 40
    static let s48: CGFloat = 48
    static let pageH: CGFloat = 16
    static let sectionGap: CGFloat = 12
    static let rowV: CGFloat = 14
    static let rowH: CGFloat = 16
    static let chipHPad: CGFloat = 12
    static let bottomBarPad: CGFloat = 16
    static let sheetTopPad: CGFloat = 20
    static let listCardGap: CGFloat = 12
}

enum AppRadius {
    static let xs: CGFloat = 4
    static let sm: CGFloat = 6
    static let md: CGFloat = 8
    static let lg: CGFloat = 10
    static let xl: CGFloat = 12
    static let xxl: CGFloat = 16
    static let pill: CGFloat = 999
}

enum AppFont {
    static func text(_ size: CGFloat, weight: Font.Weight = .regular) -> Font {
        .system(size: size, weight: weight)
        // Prefer PingFang SC if registered: Font.custom("PingFangSC-Regular", size: size)
    }
    static func data(_ size: CGFloat, weight: Font.Weight = .regular) -> Font {
        // Bundle TCloudNumber-*.ttf then: Font.custom("TCloudNumber", size: size)
        .system(size: size, weight: weight).monospacedDigit()
    }
    static let caption: CGFloat = 11
    static let footnote: CGFloat = 12
    static let subhead: CGFloat = 13
    static let body: CGFloat = 14
    static let callout: CGFloat = 15
    static let headline: CGFloat = 16
    static let title3: CGFloat = 17
    static let title2: CGFloat = 18
    static let title1: CGFloat = 20
}

struct CardFaceTheme: Equatable {
    let id: String
    let label: String
    let gradStart: Color
    let gradEnd: Color
    let accent: Color
    let vipBg: Color
    let vipText: Color
}

enum CardFaceThemes {
    static let all: [CardFaceTheme] = [
        .init(id: "peach", label: "蜜桃色", gradStart: Color(hex: "F4EAE5"), gradEnd: Color(hex: "EED1C3"), accent: Color(hex: "C4A394"), vipBg: Color(hex: "E2D0C6"), vipText: Color(hex: "694E42")),
        .init(id: "mint", label: "薄荷绿", gradStart: Color(hex: "EDF2E9"), gradEnd: Color(hex: "B1CD9B"), accent: Color(hex: "9DAF93"), vipBg: Color(hex: "CFDFC3"), vipText: Color(hex: "617258")),
        .init(id: "haze", label: "雾霾蓝", gradStart: Color(hex: "E9F0F3"), gradEnd: Color(hex: "C0DCE9"), accent: Color(hex: "8FA4AF"), vipBg: Color(hex: "CED8DF"), vipText: Color(hex: "405660")),
        .init(id: "taro", label: "香芋紫", gradStart: Color(hex: "F0EBF3"), gradEnd: Color(hex: "CFBCDA"), accent: Color(hex: "A89CAF"), vipBg: Color(hex: "DCD3E0"), vipText: Color(hex: "574861")),
        .init(id: "milk", label: "奶茶色", gradStart: Color(hex: "F4EEE3"), gradEnd: Color(hex: "DFC9A1"), accent: Color(hex: "B6A57A"), vipBg: Color(hex: "E0D8C1"), vipText: Color(hex: "5D5435")),
    ]
    static var `default`: CardFaceTheme { all.first { $0.id == "peach" }! }
}

extension Color {
    init(hex: String) {
        let scanner = Scanner(string: hex)
        var rgb: UInt64 = 0
        scanner.scanHexInt64(&rgb)
        let r = Double((rgb >> 16) & 0xFF) / 255
        let g = Double((rgb >> 8) & 0xFF) / 255
        let b = Double(rgb & 0xFF) / 255
        self.init(.sRGB, red: r, green: g, blue: b, opacity: 1)
    }
}
