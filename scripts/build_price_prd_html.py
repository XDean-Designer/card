# -*- coding: utf-8 -*-
"""Build PRD HTML previews from Markdown for 项目创建与管理."""
import re
import pathlib
import markdown

ROOT = pathlib.Path(r'd:\RTB优化工程')
CARD = ROOT / 'card'
PACK = ROOT / '剑琅联盟-卡模板演示包'

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
.wrap{{max-width:920px;margin:0 auto;padding:24px 20px 64px}}
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
table{{width:100%;border-collapse:collapse;margin:0 0 18px;font-size:14px;display:block;overflow-x:auto;border:1px solid var(--border);border-radius:8px}}
th,td{{border:1px solid var(--border);padding:10px 12px;text-align:left;vertical-align:top;min-width:72px}}
th{{font-weight:600;white-space:nowrap;background:var(--th-bg)}}td{{background:#fff}}
tr:nth-child(even) td{{background:#fafbfc}}
.foot-note{{margin-top:28px;padding-top:16px;border-top:1px solid var(--border);font-size:12px;color:var(--text-sec)}}
.mermaid{{margin:12px 0 20px;padding:16px;background:#fafbfc;border:1px solid var(--border);border-radius:10px;overflow-x:auto;text-align:center}}
.mermaid svg{{max-width:100%;height:auto}}
</style>
</head>
<body>
  <div class="topbar">
    <div class="topbar__title">{top}<span class="topbar__hint">阅读预览 · 表格与标题已排版</span></div>
    <div class="topbar__actions">
      <a class="ghost" href="demo.html">打开交互原型</a>
      <a class="ghost" href="{md_name}" download>下载 Markdown</a>
      <a class="primary" href="{md_name}" target="_blank" rel="noopener">打开源文件 .md</a>
    </div>
  </div>
  <div class="wrap"><article class="article">
{body}
<p class="foot-note">{foot}</p>
</article></div>

<script src="assets/vendor/mermaid.min.js"></script>
<script>
(function(){{
  if (!window.mermaid) return;
  mermaid.initialize({{
    startOnLoad: true,
    securityLevel: 'loose',
    theme: 'base',
    themeVariables: {{
      primaryColor: '#fff5f6',
      primaryBorderColor: '#F32F41',
      primaryTextColor: '#1f2329',
      secondaryColor: '#f2f3f5',
      tertiaryColor: '#ffffff',
      lineColor: '#8f959e',
      fontFamily: 'PingFang SC, Microsoft YaHei, sans-serif'
    }}
  }});
}})();
</script>

</body>
</html>
'''


def md_to_body(text: str) -> str:
    html = markdown.markdown(
        text,
        extensions=['tables', 'fenced_code', 'sane_lists'],
    )

    def unescape(s: str) -> str:
        return s.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')

    html = re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        lambda m: '<div class="mermaid">\n' + unescape(m.group(1)) + '\n</div>',
        html,
        flags=re.S,
    )
    return html


def main():
    jobs = [
        {
            'md': CARD / 'PRD-项目创建与管理.md',
            'html_name': 'PRD-项目创建与管理.html',
            'title': 'PRD-项目创建与管理（预览）',
            'top': 'PRD-项目创建与管理',
            'foot': '给 AI / 研发请使用同目录 <code>PRD-项目创建与管理.md</code>；本页仅作阅读预览。交互以 <code>demo.html</code> 为准。',
        },
        {
            'md': CARD / 'PRD-项目创建与管理-精简版.md',
            'html_name': 'PRD-项目创建与管理-精简版.html',
            'title': 'PRD-项目创建与管理 · 精简版（预览）',
            'top': 'PRD-项目创建与管理 · 精简版',
            'foot': '精简版仅含模块 1–3；完整规格见 <code>PRD-项目创建与管理.md</code>。交互以 <code>demo.html</code> 为准。',
        },
    ]

    for job in jobs:
        md_text = job['md'].read_text(encoding='utf-8')
        body = md_to_body(md_text)
        out = TEMPLATE.format(
            title=job['title'],
            top=job['top'],
            md_name=job['md'].name,
            body=body,
            foot=job['foot'],
        )
        for t in (CARD / job['html_name'], PACK / job['html_name']):
            t.write_text(out, encoding='utf-8')
            print('wrote', t)
        pack_md = PACK / job['md'].name
        pack_md.write_text(md_text, encoding='utf-8')
        print('wrote', pack_md)

    for p in [
        CARD / 'PRD-项目创建与管理.md',
        CARD / 'PRD-项目创建与管理-精简版.md',
        PACK / 'PRD-项目创建与管理.md',
        PACK / 'PRD-项目创建与管理-精简版.md',
        CARD / 'PRD-项目创建与管理.html',
        CARD / 'PRD-项目创建与管理-精简版.html',
    ]:
        t = p.read_text(encoding='utf-8')
        assert 'v1.5' in t, p
        assert '已下架' in t, p
        assert ('上传封面图' in t) or ('封面' in t), p
        assert '修改记录' not in t and '变更记录' not in t and '已知待修' not in t
        assert '无关键字搜索' in t or '无搜索' in t or 'v1.5-lite' in t or t.count('+添加') >= 1
        assert '悬浮球' not in t or '无悬浮球' in t or '无右下悬浮球' in t, p
        print('ok', p.name)
    print('done')


if __name__ == '__main__':
    main()
