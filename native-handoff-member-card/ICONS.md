# 图标清单 · 会员卡管理

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
