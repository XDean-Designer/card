# -*- coding: utf-8 -*-
"""Build PRD HTML previews from Markdown for 会员卡管理."""
import re
import pathlib
import markdown

ROOT = pathlib.Path(r'd:\RTB优化工程')
CARD = ROOT / 'card'

# Reuse shell template from price PRD builder
_price = (CARD / 'scripts' / 'build_price_prd_html.py').read_text(encoding='utf-8')
ns = {}
exec(compile(_price.split('def main')[0] + '\npass\n', 'build_price_prd_html.py', 'exec'), ns)
TEMPLATE = ns['TEMPLATE']


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
            'md': CARD / 'PRD-会员卡管理.md',
            'html_name': 'PRD-会员卡管理.html',
            'title': 'PRD-会员卡管理（预览）',
            'top': 'PRD-会员卡管理',
            'foot': '给 AI / 研发请使用同目录 <code>PRD-会员卡管理.md</code>；本页仅作阅读预览。交互以 <code>demo.html</code> 为准。',
        },
        {
            'md': CARD / 'PRD-会员卡管理-精简版.md',
            'html_name': 'PRD-会员卡管理-精简版.html',
            'title': 'PRD-会员卡管理 · 精简版（预览）',
            'top': 'PRD-会员卡管理 · 精简版',
            'foot': '精简版含模块 1–5（公式与本期任务摘要）；完整规格见 <code>PRD-会员卡管理.md</code>（含 §8 / §13）。交互以 <code>demo.html</code> 为准。',
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
        path = CARD / job['html_name']
        path.write_text(out, encoding='utf-8')
        assert '修改记录' not in out and '变更记录' not in out
        assert 'v1.15' in out
        print('wrote', path)

    for p in [
        CARD / 'PRD-会员卡管理.md',
        CARD / 'PRD-会员卡管理-精简版.md',
        CARD / 'PRD-会员卡管理.html',
        CARD / 'PRD-会员卡管理-精简版.html',
    ]:
        t = p.read_text(encoding='utf-8')
        assert 'v1.15' in t, p
        assert '确认办卡' in t, p
        assert '立即办卡' in t, p
        assert '橙→红' in t, p
        assert '橙色 Switch' in t or '橙色' in t, p
        assert '修改记录' not in t and '变更记录' not in t
        assert '卡管理' in t, p
        assert '应付' in t, p
        assert 'FinalizeIssue' in t or '§7.7' in t or '7.7' in t, p
        assert '延期费用' in t or '参考费用' in t, p
        print('ok', p.name)
    print('done')


if __name__ == '__main__':
    main()
