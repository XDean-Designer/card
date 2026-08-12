// DesignTokens.swift — 开单记账 · 方案 B
// Source: tokens/design-tokens.json · Do not invent colors/spacing outside this file.

import SwiftUI

enum AppColor {
    static let brand = Color(hex: "#F32F41")
    static let brandSoft = Color(hex: "#FFF2F2")
    static let brandBorder = Color(hex: "#FFD5D9")
    static let success = Color(hex: "#2BA471")
    static let bgPage = Color(hex: "#F7F7F7")
    static let surface = Color(hex: "#FFFFFF")
    static let textPrimary = Color(hex: "#333333")
    static let textSecondary = Color(hex: "#929292")
    static let textMid = Color(hex: "#666666")
    static let textStrong = Color(hex: "#1A1A1A")
    static let border = Color(hex: "#D7D7D5")
    static let borderLight = Color(hex: "#E8E8E8")
    static let accentOrange = Color(hex: "#FF7043")
    static let folderTabIdle = Color(hex: "#EFEFEF")
    static let folderTabIdleText = Color(hex: "#8A8A8A")
    static let continueAdd = Color(hex: "#5FA890")
    static let offerNone = Color(hex: "#C47B7B")
    static let offerManual = Color(hex: "#7A9BB8")
    static let slipNoCard = Color(hex: "#5C5C5C")
    static let trash = Color(hex: "#F32F41")
}

enum AppSpace {
    static let pageH: CGFloat = 16
    static let s4: CGFloat = 4
    static let s6: CGFloat = 6
    static let s8: CGFloat = 8
    static let s12: CGFloat = 12
    static let s16: CGFloat = 16
    static let s24: CGFloat = 24
    static let billActionGap: CGFloat = 30
    static let folderSlant: CGFloat = 18
}

enum AppRadius {
    static let sm: CGFloat = 6
    static let md: CGFloat = 8
    static let lg: CGFloat = 10
    static let xl: CGFloat = 12
    static let pill: CGFloat = 999
}

enum AppFont {
    static let caption: CGFloat = 11
    static let footnote: CGFloat = 12
    static let subhead: CGFloat = 13
    static let body: CGFloat = 14
    static let title3: CGFloat = 17
    static let title1: CGFloat = 20
    static func text(_ size: CGFloat, weight: Font.Weight = .regular) -> Font {
        .system(size: size, weight: weight)
    }
    static func data(_ size: CGFloat, weight: Font.Weight = .regular) -> Font {
        // Bundle TCloudNumber if available
        .system(size: size, weight: weight).monospacedDigit()
    }
}

extension Color {
    init(hex: String) {
        let h = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: h).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch h.count {
        case 6: (a, r, g, b) = (255, int >> 16, int >> 8 & 0xff, int & 0xff)
        case 8: (a, r, g, b) = (int >> 24, int >> 16 & 0xff, int >> 8 & 0xff, int & 0xff)
        default: (a, r, g, b) = (255, 0, 0, 0)
        }
        self.init(.sRGB, red: Double(r)/255, green: Double(g)/255, blue: Double(b)/255, opacity: Double(a)/255)
    }
}
