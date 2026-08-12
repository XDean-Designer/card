// BillDeskView.swift — SAMPLE · 点单台（bill-bill）
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
                            ForEach(0..<4, id: \.self) { _ in
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
