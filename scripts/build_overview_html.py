# -*- coding: utf-8 -*-
"""Build HTML preview for RTB产品计划概览.md"""
import re
import pathlib
import markdown

ROOT = pathlib.Path(r"d:\RTB优化工程")
CARD = ROOT / "card"

_price = (CARD / "scripts" / "build_price_prd_html.py").read_text(encoding="utf-8")
ns = {}
exec(compile(_price.split("def main")[0] + "\npass\n", "build_price_prd_html.py", "exec"), ns)
TEMPLATE = ns["TEMPLATE"]


def md_to_body(text: str) -> str:
    html = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists"],
    )

    def unescape(s: str) -> str:
        return s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")

    html = re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        lambda m: '<div class="mermaid">\n' + unescape(m.group(1)) + "\n</div>",
        html,
        flags=re.S,
    )
    return html


def main():
    md_path = CARD / "RTB产品计划概览.md"
    md_text = md_path.read_text(encoding="utf-8")
    body = md_to_body(md_text)
    out = TEMPLATE.format(
        title="RTB产品计划概览（预览）",
        top="RTB产品计划概览",
        md_name=md_path.name,
        body=body,
        foot="",
    )
    path = CARD / "RTB产品计划概览.html"
    path.write_text(out, encoding="utf-8")
    assert "一、产品总览" in out
    assert 'class="mermaid"' in out
    assert "staff-salary-detail-pending" in out
    print("wrote", path, "bytes", path.stat().st_size)


if __name__ == "__main__":
    main()
