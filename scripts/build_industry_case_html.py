# -*- coding: utf-8 -*-
"""Build HTML preview for 行业案例/美业门店案例整理.md."""
import pathlib
import markdown

ROOT = pathlib.Path(r'd:\RTB优化工程')
CARD = ROOT / 'card'
PACK = ROOT / '剑琅联盟-卡模板演示包'
MD = ROOT / '行业案例' / '美业门店案例整理.md'
HTML_NAME = '行业案例-美业门店案例整理.html'
MD_HREF = '../行业案例/美业门店案例整理.md'

TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
:root{{--brand:#F32F41;--text:#1f2329;--text-sec:#646a73;--border:#e5e6eb;--bg:#f5f6f7;--card:#fff;--code-bg:#f2f3f5;--th-bg:#f8f9fa;--link:#3370ff}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;color:var(--text);background:var(--bg);line-height:1.7;font-size:15px}}
.topbar{{position:sticky;top:0;z-index:20;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;padding:10px 20px;background:rgba(255,255,255,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--border)}}
.topbar__title{{font-size:14px;font-weight:600}}.topbar__hint{{font-size:12px;color:var(--text-sec);font-weight:400;margin-left:8px}}
.topbar__actions{{display:flex;gap:8px;flex-wrap:wrap}}
.topbar a{{display:inline-flex;align-items:center;height:32px;padding:0 12px;border-radius:6px;font-size:13px;text-decoration:none;font-weight:500}}
.topbar a.primary{{background:var(--brand);color:#fff}}.topbar a.ghost{{background:var(--card);color:var(--text);border:1px solid var(--border)}}
.wrap{{max-width:960px;margin:0 auto;padding:24px 20px 64px}}
.article{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:32px 40px 48px;box-shadow:0 1px 2px rgba(0,0,0,.04)}}
@media(max-width:640px){{.article{{padding:20px 16px 32px;border-radius:0;border-left:none;border-right:none}}}}
.article>h1:first-child{{margin-top:0}}
h1{{font-size:28px;font-weight:700;line-height:1.35;margin:0 0 16px}}
h2{{font-size:22px;font-weight:650;margin:40px 0 14px;padding-bottom:8px;border-bottom:1px solid var(--border)}}
h3{{font-size:17px;font-weight:650;margin:28px 0 10px}}h4{{font-size:15px;font-weight:650;margin:20px 0 8px}}
p{{margin:0 0 12px}}a{{color:var(--link);text-decoration:none}}a:hover{{text-decoration:underline}}
ul,ol{{margin:0 0 14px;padding-left:1.4em}}li{{margin:4px 0}}
hr{{border:none;border-top:1px solid var(--border);margin:28px 0}}
blockquote{{margin:12px 0 16px;padding:10px 14px;border-left:3px solid var(--brand);background:#fff5f6;color:var(--text-sec);border-radius:0 8px 8px 0}}
blockquote p{{margin:0}}
code{{font-family:ui-monospace,Consolas,monospace;font-size:.9em;background:var(--code-bg);padding:1px 6px;border-radius:4px}}
pre{{background:#1f2329;color:#f5f6f7;padding:14px 16px;border-radius:8px;overflow-x:auto;font-size:13px;line-height:1.55;margin:0 0 16px}}
pre code{{background:none;padding:0;color:inherit}}
table{{width:100%;border-collapse:collapse;margin:0 0 18px;font-size:13px;display:block;overflow-x:auto;border:1px solid var(--border);border-radius:8px}}
th,td{{border:1px solid var(--border);padding:8px 10px;text-align:left;vertical-align:top;min-width:64px}}
th{{font-weight:600;white-space:nowrap;background:var(--th-bg)}}td{{background:#fff}}
tr:nth-child(even) td{{background:#fafbfc}}
.foot-note{{margin-top:28px;padding-top:16px;border-top:1px solid var(--border);font-size:12px;color:var(--text-sec)}}
strong{{font-weight:650}}
</style>
</head>
<body>
  <div class="topbar">
    <div class="topbar__title">{top}<span class="topbar__hint">阅读预览 · 用于对照验证原型</span></div>
    <div class="topbar__actions">
      <a class="ghost" href="demo.html">打开交互原型</a>
      <a class="ghost" href="{md_href}" download>下载 Markdown</a>
      <a class="primary" href="{md_href}" target="_blank" rel="noopener">打开源文件 .md</a>
    </div>
  </div>
  <div class="wrap"><article class="article">
{body}
<p class="foot-note">{foot}</p>
</article></div>
</body>
</html>
'''


def main():
    md_text = MD.read_text(encoding='utf-8')
    body = markdown.markdown(
        md_text,
        extensions=['tables', 'fenced_code', 'sane_lists'],
    )
    out = TEMPLATE.format(
        title='行业案例 · 美业门店案例整理（预览）',
        top='行业案例 · 美业门店案例整理',
        md_href=MD_HREF,
        body=body,
        foot='源文件：<code>行业案例/美业门店案例整理.md</code>。本页仅作阅读预览；交互以 <code>demo.html</code> 为准。验证时请填写第 6 节检查清单。',
    )
    for dest in (CARD / HTML_NAME, PACK / HTML_NAME):
        dest.write_text(out, encoding='utf-8')
        print('wrote', dest)


if __name__ == '__main__':
    main()
