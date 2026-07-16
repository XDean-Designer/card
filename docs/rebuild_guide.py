# -*- coding: utf-8 -*-
"""Rebuild docs/guide.html — sole browsable docs hub (do not use index.html as hub)."""
from pathlib import Path
import json
import re

DOCS_DIR = Path(__file__).resolve().parent
OUT_NAME = "guide.html"
FILES = [
    "README.md",
    "00-scope.md",
    "01-data-model.md",
    "02-api-catalog.md",
    "03-rules-cases.md",
    "04-page-map.md",
    "05-acceptance.md",
]

bundle = {name: (DOCS_DIR / name).read_text(encoding="utf-8") for name in FILES}
bundle_json = json.dumps(bundle, ensure_ascii=False, separators=(",", ":"))
assert "</script>" not in bundle_json.lower()

APP_JS = r'''
(function () {
  const DOCS = {
    home: { title: '总览', file: 'README.md' },
    '00-scope.md': { title: '00 · 范围一页纸', file: '00-scope.md' },
    '01-data-model.md': { title: '01 · 领域数据模型', file: '01-data-model.md' },
    '02-api-catalog.md': { title: '02 · 接口目录草案', file: '02-api-catalog.md' },
    '03-rules-cases.md': { title: '03 · 规则与验收算例', file: '03-rules-cases.md' },
    '04-page-map.md': { title: '04 · 页面对照', file: '04-page-map.md' },
    '05-acceptance.md': { title: '05 · 验收清单', file: '05-acceptance.md' },
  };

  try {
    window.__DOCS_BUNDLE__ = JSON.parse(document.getElementById('docs-bundle').textContent);
  } catch (e) {
    window.__DOCS_BUNDLE__ = {};
    console.error('docs bundle parse failed', e);
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function rewriteHref(href) {
    if (/^\.\/[\w.-]+\.md$/.test(href)) {
      return '#' + href.slice(2).replace(/\.md$/, '');
    }
    const m = href.match(/^(?:\.\/)?(?:index|guide)\.html#(home|[\w.-]+)$/);
    if (m) return '#' + m[1];
    if (/^#(home|[\w.-]+)$/.test(href)) return href;
    return href;
  }

  function inlineFormat(text) {
    let s = escapeHtml(text);
    s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, label, href) => {
      const h = rewriteHref(href);
      return '<a href="' + escapeHtml(h) + '">' + label + '</a>';
    });
    s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
    s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    s = s.replace(/\\\(/g, '(').replace(/\\\)/g, ')');
    s = s.replace(/\\\[/g, '[').replace(/\\\]/g, ']');
    return s;
  }

  function splitTableCells(line) {
    const raw = line.replace(/^\|/, '').replace(/\|$/, '');
    const cells = [];
    let cur = '';
    for (let i = 0; i < raw.length; i++) {
      if (raw[i] === '\\' && raw[i + 1] === '|') {
        cur += '|';
        i++;
      } else if (raw[i] === '|') {
        cells.push(cur.trim());
        cur = '';
      } else {
        cur += raw[i];
      }
    }
    cells.push(cur.trim());
    return cells;
  }

  function renderMarkdown(src) {
    const lines = String(src).replace(/\r\n/g, '\n').split('\n');
    const out = [];
    let i = 0;
    let inCode = false;
    let codeBuf = [];
    let listType = null;

    function closeList() {
      if (!listType) return;
      out.push(listType === 'ul' ? '</ul>' : '</ol>');
      listType = null;
    }
    function flushCode() {
      out.push('<pre><code>' + escapeHtml(codeBuf.join('\n')) + '</code></pre>');
      codeBuf = [];
      inCode = false;
    }

    while (i < lines.length) {
      const line = lines[i];
      if (line.startsWith('```')) {
        if (inCode) flushCode();
        else { closeList(); inCode = true; codeBuf = []; }
        i++; continue;
      }
      if (inCode) { codeBuf.push(line); i++; continue; }

      if (/^\|/.test(line) && i + 1 < lines.length && /^\|?\s*-/.test(lines[i + 1])) {
        closeList();
        const rows = [];
        while (i < lines.length && /^\|/.test(lines[i])) {
          const cells = splitTableCells(lines[i]);
          if (!/^[\s:-]+$/.test(cells.join(''))) rows.push(cells);
          i++;
        }
        if (rows.length) {
          out.push('<table><thead><tr>' + rows[0].map(c => '<th>' + inlineFormat(c) + '</th>').join('') + '</tr></thead><tbody>');
          rows.slice(1).forEach(r => {
            out.push('<tr>' + r.map(c => '<td>' + inlineFormat(c) + '</td>').join('') + '</tr>');
          });
          out.push('</tbody></table>');
        }
        continue;
      }

      if (/^---+$/.test(line.trim())) { closeList(); out.push('<hr />'); i++; continue; }

      const h = line.match(/^(#{1,3})\s+(.*)$/);
      if (h) {
        closeList();
        const lv = h[1].length;
        out.push('<h' + lv + '>' + inlineFormat(h[2]) + '</h' + lv + '>');
        i++; continue;
      }

      if (/^>\s?/.test(line)) {
        closeList();
        const parts = [];
        while (i < lines.length && /^>\s?/.test(lines[i])) {
          parts.push(lines[i].replace(/^>\s?/, ''));
          i++;
        }
        out.push('<blockquote><p>' + inlineFormat(parts.join(' ')) + '</p></blockquote>');
        continue;
      }

      const ul = line.match(/^[-*]\s+(.*)$/);
      if (ul) {
        if (listType !== 'ul') { closeList(); out.push('<ul>'); listType = 'ul'; }
        out.push('<li>' + inlineFormat(ul[1]) + '</li>');
        i++; continue;
      }
      const ol = line.match(/^\d+\.\s+(.*)$/);
      if (ol) {
        if (listType !== 'ol') { closeList(); out.push('<ol>'); listType = 'ol'; }
        out.push('<li>' + inlineFormat(ol[1]) + '</li>');
        i++; continue;
      }

      if (!line.trim()) { closeList(); i++; continue; }
      closeList();
      out.push('<p>' + inlineFormat(line) + '</p>');
      i++;
    }
    closeList();
    if (inCode) flushCode();
    return out.join('\n');
  }

  function currentKey() {
    const hash = (location.hash || '#home').slice(1);
    if (hash === 'home' || !hash) return 'home';
    if (DOCS[hash + '.md']) return hash + '.md';
    if (DOCS[hash]) return hash;
    return 'home';
  }

  function navigateTo(hash) {
    const next = (hash || 'home').replace(/^#/, '');
    if (location.hash.slice(1) === next) {
      loadDoc();
    } else {
      location.hash = next;
    }
  }

  function loadDoc() {
    const key = currentKey();
    const meta = DOCS[key] || DOCS.home;
    document.getElementById('pageTitle').textContent = meta.title;
    document.querySelectorAll('.nav a.doc').forEach(a => {
      a.classList.toggle('is-on', a.dataset.doc === key || (key === 'home' && a.dataset.doc === 'home'));
    });
    const el = document.getElementById('content');
    const text = (window.__DOCS_BUNDLE__ && window.__DOCS_BUNDLE__[meta.file]) || '';
    if (!text) {
      el.className = 'article error';
      el.innerHTML = '<p>未找到文档 <code>' + escapeHtml(meta.file) + '</code>。请运行 <code>python rebuild_guide.py</code> 重建本页。</p>';
      return;
    }
    el.className = 'article md';
    el.innerHTML = renderMarkdown(text);
    el.querySelectorAll('a[href^="#"]').forEach(a => {
      a.addEventListener('click', (ev) => {
        const href = a.getAttribute('href') || '';
        if (href.startsWith('#') && href.length > 1) {
          ev.preventDefault();
          navigateTo(href.slice(1));
        }
      });
    });
    window.scrollTo(0, 0);
  }

  document.querySelectorAll('.nav a.doc').forEach(a => {
    a.addEventListener('click', (ev) => {
      const href = a.getAttribute('href') || '';
      if (!href.startsWith('#')) return;
      ev.preventDefault();
      navigateTo(href.slice(1) || 'home');
    });
  });

  window.addEventListener('hashchange', loadDoc);
  loadDoc();
})();
'''

SHELL = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>研发开工包 · 会员卡权益组合版</title>
  <style>
    :root {
      --brand: #F32F41; --brand-soft: #FFF2F2; --brand-line: #FFD5D9;
      --bg: #F0F1EF; --card: #fff; --text: #2A2C2A; --muted: #7A7D78;
      --line: #D8DAD5; --ink: #161916; --code-bg: #1f2923; --code-fg: #d7e0d8;
      --nav-w: 240px;
      --font: "PingFang SC", "Source Han Sans SC", "Microsoft YaHei", sans-serif;
      --mono: ui-monospace, Consolas, "Cascadia Mono", monospace;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0; font-family: var(--font); color: var(--text); line-height: 1.6;
      background: radial-gradient(900px 480px at 0% -5%, #e8ece6 0%, transparent 55%), var(--bg);
    }
    a { color: var(--brand); }
    .layout { display: grid; grid-template-columns: var(--nav-w) 1fr; min-height: 100vh; }
    .nav {
      position: sticky; top: 0; height: 100vh; overflow: auto;
      padding: 18px 12px; background: rgba(255,255,255,.92);
      border-right: 1px solid var(--line); backdrop-filter: blur(8px);
    }
    .nav__brand { font-size: 11px; font-weight: 700; color: var(--brand); letter-spacing: .04em; margin: 0 8px 4px; }
    .nav__title { font-size: 14px; font-weight: 700; color: var(--ink); margin: 0 8px 14px; line-height: 1.35; }
    .nav a.doc {
      display: block; padding: 9px 10px; border-radius: 8px; color: var(--text);
      text-decoration: none; font-size: 13px; margin-bottom: 2px;
    }
    .nav a.doc:hover, .nav a.doc.is-on { background: var(--brand-soft); color: var(--brand); }
    .nav a.doc small { display: block; font-size: 11px; color: var(--muted); margin-top: 2px; font-weight: 400; }
    .nav__meta { margin: 16px 8px 0; padding-top: 12px; border-top: 1px solid var(--line); font-size: 12px; color: var(--muted); }
    .nav__meta a { display: block; margin-top: 6px; color: var(--brand); text-decoration: none; }
    .main { padding: 24px 28px 64px; max-width: 920px; }
    .hero {
      background: var(--card); border: 1px solid var(--line); border-radius: 14px;
      padding: 18px 20px; margin-bottom: 18px;
    }
    .hero h1 { margin: 0 0 6px; font-size: 22px; color: var(--ink); }
    .hero p { margin: 0; font-size: 13px; color: var(--muted); }
    .article {
      background: var(--card); border: 1px solid var(--line); border-radius: 14px;
      padding: 22px 24px 28px; min-height: 320px;
    }
    .article.error { color: var(--brand); }
    .md h1 { font-size: 22px; margin: 0 0 14px; color: var(--ink); }
    .md h2 { font-size: 17px; margin: 22px 0 10px; color: var(--ink); padding-top: 4px; border-top: 1px solid var(--line); }
    .md h2:first-child { border-top: none; padding-top: 0; }
    .md h3 { font-size: 15px; margin: 16px 0 8px; color: var(--ink); }
    .md p, .md li { font-size: 14px; }
    .md ul, .md ol { padding-left: 1.25em; margin: 8px 0; }
    .md li + li { margin-top: 4px; }
    .md blockquote {
      margin: 12px 0; padding: 10px 14px; border-left: 3px solid var(--brand);
      background: var(--brand-soft); color: #7a372c; border-radius: 0 8px 8px 0; font-size: 13px;
    }
    .md hr { border: none; border-top: 1px solid var(--line); margin: 20px 0; }
    .md table {
      width: 100%; border-collapse: collapse; font-size: 13px; margin: 10px 0 14px;
      display: block; overflow-x: auto;
    }
    .md th, .md td {
      border: 1px solid var(--line); padding: 8px 10px; text-align: left; vertical-align: top;
    }
    .md th { background: #f6f7f5; font-weight: 600; color: var(--ink); white-space: nowrap; }
    .md code {
      font-family: var(--mono); font-size: 12px; background: #eef0ed;
      padding: 1px 5px; border-radius: 4px;
    }
    .md pre {
      background: var(--code-bg); color: var(--code-fg); padding: 12px 14px;
      border-radius: 10px; overflow-x: auto; font-size: 12px; line-height: 1.5;
    }
    .md pre code { background: none; padding: 0; color: inherit; font-size: inherit; }
    .md a { text-decoration: none; }
    .md a:hover { text-decoration: underline; }
    .md strong { font-weight: 700; }
    @media (max-width: 860px) {
      .layout { grid-template-columns: 1fr; }
      .nav { position: relative; height: auto; border-right: none; border-bottom: 1px solid var(--line); }
      .main { padding: 16px; }
    }
  </style>
</head>
<body>
  <div class="layout">
    <aside class="nav">
      <div class="nav__brand">研发 · 最小开工包</div>
      <div class="nav__title">会员卡 · 权益组合版</div>
      <a class="doc is-on" href="#home" data-doc="home"><strong>总览</strong><small>阅读顺序与权威源</small></a>
      <a class="doc" href="#00-scope" data-doc="00-scope.md"><strong>00 范围</strong><small>本期做 / 不做</small></a>
      <a class="doc" href="#01-data-model" data-doc="01-data-model.md"><strong>01 数据模型</strong><small>实体 · 字段 · 状态</small></a>
      <a class="doc" href="#02-api-catalog" data-doc="02-api-catalog.md"><strong>02 接口目录</strong><small>API 草案</small></a>
      <a class="doc" href="#03-rules-cases" data-doc="03-rules-cases.md"><strong>03 规则算例</strong><small>延期 / 退卡</small></a>
      <a class="doc" href="#04-page-map" data-doc="04-page-map.md"><strong>04 页面对照</strong><small>原型 ↔ 接口</small></a>
      <a class="doc" href="#05-acceptance" data-doc="05-acceptance.md"><strong>05 验收清单</strong><small>本期 P0</small></a>
      <div class="nav__meta">
        相关入口
        <a href="../demo.html">交互原型</a>
        <a href="../prd-review.html">PRD 评审页</a>
        <a href="../logic.html">逻辑算例</a>
        <a href="../index.html">演示包首页</a>
      </div>
    </aside>
    <main class="main">
      <header class="hero">
        <h1 id="pageTitle">研发开工包</h1>
        <p id="pageHint">新入口 guide.html · 左侧切换文档 · 内容已内嵌</p>
      </header>
      <article class="article md" id="content">加载中…</article>
    </main>
  </div>

<script type="application/json" id="docs-bundle">''' + bundle_json + r'''</script>
<script>
''' + APP_JS.strip() + r'''
</script>

</body>
</html>
'''

out = DOCS_DIR / OUT_NAME
out.write_text(SHELL, encoding="utf-8")

# Redirect stub — old index.html is retired as hub
redirect = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="refresh" content="0; url=guide.html" />
  <link rel="canonical" href="guide.html" />
  <title>入口已迁移 · 研发开工包</title>
  <script>
    location.replace('guide.html' + (location.hash || ''));
  </script>
</head>
<body>
  <p style="font-family: system-ui, sans-serif; padding: 24px;">
    文档浏览入口已迁至 <a href="guide.html">guide.html</a>（本页不再承载文档内容）。
  </p>
</body>
</html>
'''
(DOCS_DIR / "index.html").write_text(redirect, encoding="utf-8")

text = out.read_text(encoding="utf-8")
m = re.search(r'id="docs-bundle">(.*?)</script>', text, re.S)
d = json.loads(m.group(1))
assert set(d.keys()) == set(FILES)
assert text.find('id="docs-bundle"') < text.find("function currentKey")
assert text.count("<script") == 2
print("OK", out, "size", len(text), "keys", len(d))
print("OK redirect ->", DOCS_DIR / "index.html")
