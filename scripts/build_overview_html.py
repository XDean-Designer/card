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

MERMAID_FIT_CSS = (
    ".mermaid{margin:12px 0 20px;padding:16px;background:#fafbfc;"
    "border:1px solid var(--border);border-radius:10px;"
    "overflow:auto;text-align:center;width:100%;box-sizing:border-box;"
    "height:auto!important;max-width:100%}"
    ".mermaid svg{display:block;margin:0 auto;"
    "max-width:100%!important;width:100%!important;height:auto!important}"
    ".mermaid .nodeLabel,.mermaid .edgeLabel,.mermaid foreignObject,"
    ".mermaid .label,.mermaid foreignObject div,.mermaid foreignObject span,"
    ".mermaid .cluster-label,.mermaid .cluster span{"
    "font-size:16px!important;line-height:1.35!important}"
    ".mermaid--xl .nodeLabel,.mermaid--xl .edgeLabel,"
    ".mermaid--xl foreignObject,.mermaid--xl .label,"
    ".mermaid--xl foreignObject div,.mermaid--xl foreignObject span,"
    ".mermaid--xl .cluster-label,.mermaid--xl .cluster span{"
    "font-size:17px!important;line-height:1.4!important}"
)

MERMAID_FIT_SCRIPT = r"""
<script src="assets/vendor/mermaid.min.js"></script>
<script>
(function(){
  if (!window.mermaid) return;

  function fitMermaidBoxes() {
    document.querySelectorAll('.mermaid').forEach(function (box) {
      var svg = box.querySelector('svg');
      if (!svg) return;
      // Fit entirely inside the module frame (no transform overflow)
      svg.removeAttribute('width');
      svg.removeAttribute('height');
      svg.style.width = '100%';
      svg.style.maxWidth = '100%';
      svg.style.height = 'auto';
      svg.style.transform = 'none';
      svg.style.margin = '0 auto';
      box.style.height = 'auto';
      box.style.minHeight = '0';
      box.style.overflow = 'auto';
    });
  }

  mermaid.initialize({
    startOnLoad: false,
    securityLevel: 'loose',
    theme: 'base',
    themeVariables: {
      primaryColor: '#fff5f6',
      primaryBorderColor: '#F32F41',
      primaryTextColor: '#1f2329',
      secondaryColor: '#f2f3f5',
      tertiaryColor: '#ffffff',
      lineColor: '#8f959e',
      fontFamily: 'PingFang SC, Microsoft YaHei, sans-serif',
      fontSize: '16px'
    }
  });

  function run() {
    var p = mermaid.run({ querySelector: '.mermaid' });
    Promise.resolve(p).then(function () {
      requestAnimationFrame(function () {
        fitMermaidBoxes();
        setTimeout(fitMermaidBoxes, 80);
        setTimeout(fitMermaidBoxes, 320);
      });
    }).catch(function () {
      fitMermaidBoxes();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
  window.addEventListener('resize', function () {
    clearTimeout(window.__mermaidFitT);
    window.__mermaidFitT = setTimeout(fitMermaidBoxes, 100);
  });
})();
</script>
"""


def md_to_body(text: str) -> str:
    html = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists"],
    )

    def unescape(s: str) -> str:
        return (
            s.replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&amp;", "&")
            .replace("&quot;", '"')
        )

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
    out2, n = re.subn(
        r"\.mermaid\{[^}]+\}"
        r"\.mermaid svg\{[^}]+\}",
        MERMAID_FIT_CSS,
        out,
        count=1,
    )
    if n != 1:
        out2, n = re.subn(
            r"\.mermaid\{.*?\}"
            r"(?:\.mermaid[^{]*\{.*?\})*",
            MERMAID_FIT_CSS,
            out,
            count=1,
            flags=re.S,
        )
    if n != 1:
        raise SystemExit(f"mermaid CSS replace failed n={n}")
    out = out2

    for h3, tag in (
        (r"2\.4 项目创建与管理（价目表）", "price-main"),
        (r"2\.5 会员卡管理", "card-main"),
    ):
        out, n_xl = re.subn(
            rf"(<h3>{h3}</h3>\s*<h4>主链路</h4>\s*)"
            r'<div class="mermaid(?: mermaid--xl)?"[^>]*>',
            rf'\1<div class="mermaid mermaid--xl" data-diagram="{tag}">',
            out,
            count=1,
        )
        if n_xl != 1:
            raise SystemExit(f"mermaid--xl inject failed for {tag} n={n_xl}")

    out4, n3 = re.subn(
        r"<script src=\"assets/vendor/mermaid\.min\.js\"></script>\s*"
        r"<script>[\s\S]*?</script>\s*</body>",
        MERMAID_FIT_SCRIPT.strip() + "\n\n</body>",
        out,
        count=1,
    )
    if n3 != 1:
        raise SystemExit(f"mermaid script replace failed n={n3}")
    out = out4

    path = CARD / "RTB产品计划概览.html"
    path.write_text(out, encoding="utf-8")
    assert "一、产品总览" in out
    assert "fitMermaidBoxes" in out
    assert 'data-diagram="price-main"' in out
    assert 'data-diagram="card-main"' in out
    assert "① 列表" in out
    assert "④ 分组" in out
    print("wrote", path, "bytes", path.stat().st_size)


if __name__ == "__main__":
    main()
