// CardListView.swift — SAMPLE SwiftUI · 会员卡列表（在售）
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
                ForEach(ShelfTab.allCases, id: \.self) { Text($0.rawValue).tag($0) }
            }
            .pickerStyle(.segmented)
            .padding(.horizontal, AppSpace.pageH)
            .padding(.vertical, AppSpace.s8)
            .background(AppColor.surface)

            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: AppSpace.s8) {
                    ForEach([("all", "全部")] + groups, id: \.0) { id, name in
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
