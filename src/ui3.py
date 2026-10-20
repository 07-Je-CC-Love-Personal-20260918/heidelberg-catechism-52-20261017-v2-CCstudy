# -*- coding: utf-8 -*-
"""v3 层：ccifellowship.org 原文（一字不差）· 重点/难点突出 · 大字号 · 记忆墙 · 原文阅读室页面"""
import html, re
from cci_text import HC, BC, COD, CREEDS, INTRO
from ui2 import ic, E
import ui4

SRC = "https://ccifellowship.org"
FN = re.compile(r'(?<=[^\d\s:：\-第,，(（])(\d{1,2})(?![章节条项年月日世号次篇:：\d])(?=[，。；、：”！？）」\s]|$|[\u4e00-\u9fff])')


def strip_fn(a):
    return FN.sub('', a)


def fn_html(a):
    """答案原文：脚注数字保持原字符，仅以上标呈现"""
    return '<br>'.join(FN.sub(r'<sup>\1</sup>', E(x)) for x in a.split('\n'))


def refs_html(refs):
    if not refs:
        return ''
    return ('<details class="refs"><summary>%s经文出处 · %d 条</summary><ol>%s</ol></details>'
            % (ic("book", "ic s"), len(refs), ''.join('<li>%s</li>' % E(r) for r in refs)))


def patch_lds(LDS):
    """以 ccifellowship.org 原文替换问答文本（供搜索/背诵/自测使用的纯文本去掉脚注号）"""
    for d in LDS:
        d["qas"] = [[n, HC[n]["q"], strip_fn(HC[n]["a"]).replace("\n", " ")] for n, _, _ in d["qas"]]


def render_ld(d, A, PL):
    k = d["key"]
    q0, q1 = d["qas"][0][0], d["qas"][-1][0]
    qn = "问 %d" % q0 if q0 == q1 else "问 %d–%d" % (q0, q1)
    left = (q0 - 1) / 129 * 100
    wid = max((q1 - q0 + 1) / 129 * 100, 1.2)
    qas = ''.join('<div class="qa"><div class="qn">%s第 %d 问</div><div class="q">%s</div>'
                  '<p class="a">%s</p>%s</div>' % (ic("mic", "ic s"), n, E(HC[n]["q"]), fn_html(HC[n]["a"]),
                                                    refs_html(HC[n]["refs"])) for n, _, _ in d["qas"])
    terms = ''.join('<div class="term"><span class="%s">%s</span><span class="tgloss">%s%s</span></div>'
                    % (cls, E(t), '' if tr == "—" else '<i>%s</i>' % E(tr), E(gl))
                    for cls, t, tr, gl in d["terms"])
    _pt = lambda L: ''.join('<p class="pt"><b>%s。</b>%s</p>' % (E(t), E(x)) for t, x in L)
    ana = _pt(d["analysis"][:2]) + ('<details class="ana-more"><summary>＋ 再看 %d 点</summary>%s</details>'
                                    % (len(d["analysis"]) - 2, _pt(d["analysis"][2:])) if len(d["analysis"]) > 2 else '')
    ang = _pt(d["angles"])
    emo, app = ui4.EMO[d["n"] - 1], ui4.APP[d["n"] - 1]
    verses = ''.join('<span class="vchip">%s</span>' % E(v.strip()) for v in d["verses"].split("；") if v.strip())
    s = " ".join([d["title"], d["theme"], d["part"], d["core"], d["logic"], d["memo"], d["caution"],
                  d["context"], d["canon"], d["confess"], d["verses"], ui4.APP[d["n"] - 1],
                  " ".join(q + a for _, q, a in d["qas"]),
                  " ".join(t + x for t, x in d["analysis"] + d["angles"]),
                  " ".join(t + tr + gl for _, t, tr, gl in d["terms"]), "主日%d LD%d" % (d["n"], d["n"])])

    def tile(icon, lab, body, cls=""):
        return '<div class="tile %s"><div class="tl">%s<span>%s</span></div>%s</div>' % (cls, ic(icon), lab, body)

    return f'''<section class="ld v2 v3 {k} rv" id="ld{d['n']}" data-n="{d['n']}" data-s="{A(s)}">
<div class="ld-h"><div class="ld-no">{d['n']}</div><div class="ld-ht"><h3>{E(d['title'])}</h3>
<div class="ld-meta"><span>主日 {d['n']}</span><span>{qn}</span><span class="pp">{E(d['part'])} · {PL[d['part']]}</span><span>{E(d['theme'])}</span></div>
<div class="qpos" title="在 129 问中的位置"><i style="left:{left:.2f}%;width:{wid:.2f}%"></i></div></div>
<div class="ld-emo" aria-hidden="true">{emo}</div><label class="chk"><input type="checkbox" data-n="{d['n']}">已背熟</label></div>
<div class="keyline"><div class="kb kb-core"><span class="badge b-key">{ic("core", "ic s")}重点</span><p>{E(d['core'])}</p></div>
<div class="kb kb-memo"><span class="badge b-memo">{ic("key", "ic s")}记忆钥匙</span><p>{E(d['memo'])}</p></div>
<div class="kb kb-app"><span class="badge b-app">{ic("flow", "ic s")}今日应用</span><p>{E(app)}</p></div></div>
<div class="ld-g">
 <div class="ld-main">{qas}<div class="srcnote">问答原文引自 <a href="{SRC}/books/book-of-praise/confessions/heidelberg-catechism" target="_blank" rel="noopener">ccifellowship.org</a></div></div>
 <div class="ld-side">
  {tile("flow", "逻辑推进 · 承前启后", '<p>%s</p>' % E(d['logic']), "t-logic")}
  {tile("clock", "真实背景 · 为什么写", '<p>%s</p>' % E(d['context']), "t-ctx")}
  {tile("alert", "难点 · 误读警示", '<p>%s</p>' % E(d['caution']), "t-warn")}
 </div>
</div>
<div class="ld-g3">
 {tile("brain", "神学剖析", ana, "wide t-ana")}
 {tile("book", "经文根据", '<div class="vchips">%s</div>' % verses)}
</div>
<details class="deep"><summary>{ic("layers")}<span>延伸阅读：正典定位 · 原文钥词 · 多视角 · 信条互参</span>{ic("chev", "ic chev")}</summary>
<div class="ld-g3">
 {tile("arc", "正典定位", '<p>%s</p>' % E(d['canon']))}
 {tile("lang", "原文钥词", '<div class="terms">%s</div>' % terms)}
 {tile("eye", "多视角对照", ang, "wide")}
 {tile("link", "信条互参", '<p class="cf">%s</p>' % ui4.confess_links(d['confess']))}
</div></details></section>'''


# ---------------- 信经背诵室（原文） ----------------
CREED_META = [("rd-apostles", "Symbolum Apostolicum", "deliver"),
              ("rd-nicene", "Symbolum Nicaeno-Constantinopolitanum · 381", "teal"),
              ("rd-athan", "Symbolum Quicunque", "misery")]


def creed_lines(i, c):
    if i == 2:  # 亚他那修：按原文条号分句
        out = []
        for l in c["lines"]:
            out += [x.strip() for x in re.split(r'(?=\d+\) )', l) if x.strip()]
        return out
    out = []
    for l in c["lines"]:
        out += [x for x in re.findall(r'[^；]+；?', l) if x.strip()]
    return out


def readers_section():
    tabs = ''.join('<button class="rtab%s" data-r="%s">%s</button>' % (" on" if i == 0 else "", m[0], E(c["name"]))
                   for i, (c, m) in enumerate(zip(CREEDS, CREED_META)))
    panes = []
    for i, (c, (rid, lat, col)) in enumerate(zip(CREEDS, CREED_META)):
        ls = creed_lines(i, c)
        body = ''.join('<p class="rl" style="--c:var(--%s)">%s</p>' % (col, E(x)) for x in ls)
        panes.append('<article class="rpane%s" id="%s"><header><h3>%s</h3><div class="rlat">%s</div>'
                     '<p class="rintro">%s</p></header>%s</article>'
                     % (" on" if i == 0 else "", rid, E(c["name"]), E(lat), E(c["intro"]), body))
    return ('<div class="reader glass"><div class="rbar">%s<span class="sp"></span>'
            '<button class="btn" id="rHide">逐句遮盖</button><button class="btn" id="rSize">字号</button>'
            '<a class="btn" href="texts.html#creeds">全文页 ↗</a></div>%s'
            '<p class="rnote">信经正文一字不差引自 <a href="%s/books/book-of-praise/creeds" target="_blank" rel="noopener">'
            'ccifellowship.org · 信经</a>，仅按分号／条号分行以便背诵。点「逐句遮盖」后轻点每句可显示或再遮盖。</p></div>'
            ) % (tabs, ''.join(panes), SRC)


# ---------------- 新可视化 ----------------
def donut(LDS):
    parts = [("总纲", "prologue", 1, 2), ("困苦", "misery", 2, 9), ("拯救", "deliver", 3, 74), ("感恩", "gratitude", 4, 44)]
    # 依 LDS 计算主日数
    cnt = {p: sum(1 for d in LDS if d["part"] == p) for p, *_ in parts}
    R, C = 70, 2 * 3.14159 * 70
    off, segs, leg = 0, [], []
    for i, (p, col, _, qs) in enumerate(parts):
        L = qs / 129 * C
        segs.append('<circle r="%d" cx="100" cy="100" fill="none" stroke="var(--%s)" stroke-width="30" '
                    'stroke-dasharray="%.1f %.1f" stroke-dashoffset="%.1f" class="dseg" style="animation-delay:%.2fs"/>'
                    % (R, col, L, C - L, -off, i * .25))
        off += L
        leg.append('<div class="dl" style="--c:var(--%s)"><b>%d</b><span>%s</span><em>%d 问 · %d 主日 · %.0f%%</em></div>'
                   % (col, qs, p, qs, cnt[p], qs / 129 * 100))
    svg = ('<svg viewBox="0 0 200 200" class="donut" role="img" aria-label="129 问按四部分分布">'
           '<g transform="rotate(-90 100 100)">%s</g>'
           '<text x="100" y="96" text-anchor="middle" class="dn1">129</text>'
           '<text x="100" y="118" text-anchor="middle" class="dn2">问 · 52 主日</text></svg>') % ''.join(segs)
    return ('<figure class="fig"><figcaption>图 · 129 问的比例：拯救占过半，感恩占三分之一，困苦只占 7%%——'
            '先知罪，但重心在恩典与感恩</figcaption><div class="dwrap">%s<div class="dleg">%s</div></div></figure>'
            % (svg, ''.join(leg)))


def memory_wall(LDS):
    cells = ''.join('<a class="mw %s" href="#ld%d"><span class="mwe">%s</span><span class="mwn">%d</span><b>%s</b><i>%s</i><u>→ %s</u></a>'
                    % (d["key"], d["n"], ui4.EMO[d["n"] - 1], d["n"], E(d["title"]), E(d["core"]), E(ui4.APP[d["n"] - 1])) for d in LDS)
    return ('<figure class="fig"><figcaption>图 · 52 句重点记忆墙（每主日一句本质核心；颜色＝困苦／拯救／感恩，点按跳转）</figcaption>'
            '<div class="mwall">%s</div></figure>' % cells)


def forms_stats():
    items = [("比利时信条", "1561", "37 条", "认信 · 系统", "deliver", "book"),
             ("海德堡要理问答", "1563", "129 问 / 52 主日", "教导 · 安慰", "gratitude", "mic"),
             ("多特信经", "1619", "%d 项教义 · %d 条 + 驳谬" % (len(COD), sum(len(x["arts"]) - 1 for x in COD)), "辩护 · 恩典", "misery", "alert")]
    return '<div class="fstats">%s</div>' % ''.join(
        '<a class="fst" href="texts.html#%s" style="--c:var(--%s)">%s<b>%s</b><span>%s · %s</span><em>%s</em></a>'
        % (["bc", "hc", "cod"][i], c, ic(icon), E(n), y, E(cnt), E(g)) for i, (n, y, cnt, g, c, icon) in enumerate(items))


# ---------------- 原文阅读室（texts.html） ----------------
def texts_page(CSS, CSS2, ICONS, LDS, PL):
    nav, body = [], []
    nav.append('<div class="toc-h">三大普世信经</div>')
    body.append('<section class="sec" id="creeds"><div class="eyebrow">SYMBOLA OECUMENICA</div><h2>三大普世信经</h2>'
                '<p class="lead">%s</p>' % E(INTRO["creeds"].split("\n")[0]))
    for i, (c, (rid, lat, col)) in enumerate(zip(CREEDS, CREED_META)):
        nav.append('<a href="#t-%s"><span class="no">%d</span>%s</a>' % (rid, i + 1, E(c["name"])))
        body.append('<article class="tx" id="t-%s" style="--pc:var(--%s)"><h3>%s<small>%s</small></h3><p class="tintro">%s</p>%s</article>'
                    % (rid, col, E(c["name"]), E(lat), E(c["intro"]),
                       ''.join('<p class="tl1">%s</p>' % E(x) for x in creed_lines(i, c))))
    body.append('</section>')

    nav.append('<div class="toc-h">海德堡要理问答 · 52 主日</div>')
    body.append('<section class="sec" id="hc"><div class="eyebrow">CATECHESIS PALATINA · 1563</div><h2>海德堡要理问答</h2>'
                '<p class="lead">%s</p>' % E(INTRO["hc"].split("\n")[0]))
    last = None
    for d in LDS:
        if d["part"] != last:
            last = d["part"]
            body.append('<div class="tpart %s">%s · %s</div>' % (d["key"], E(d["part"]), PL[d["part"]]))
        nav.append('<a href="#hc%d"><span class="no">%d</span>%s</a>' % (d["n"], d["n"], E(d["title"])))
        qa = ''.join('<div class="tqa" id="q%d"><div class="tq"><b>%d．</b>问：%s</div><div class="ta">答：%s</div>%s</div>'
                     % (n, n, E(HC[n]["q"]), fn_html(HC[n]["a"]), refs_html(HC[n]["refs"])) for n, _, _ in d["qas"])
        body.append('<article class="tx %s" id="hc%d"><h3><span class="tno">主日 %d</span>%s'
                    '<a class="tback" href="index.html#ld%d">解读 ↗</a></h3>%s</article>'
                    % (d["key"], d["n"], d["n"], E(d["title"]), d["n"], qa))
    body.append('</section>')

    nav.append('<div class="toc-h">比利时信条 · 37 条</div>')
    body.append('<section class="sec" id="bc"><div class="eyebrow">CONFESSIO BELGICA · 1561</div><h2>比利时信条</h2>'
                '<p class="lead">%s</p>' % E(INTRO["bc"].split("\n")[0]))
    for a in BC:
        nav.append('<a href="#bc%d"><span class="no">%d</span>%s</a>' % (a["no"], a["no"], E(re.sub(r'^第.+?条\s*', '', a["title"]))))
        body.append('<article class="tx deliver" id="bc%d"><h3>%s</h3>%s%s</article>'
                    % (a["no"], E(a["title"]), ''.join('<p>%s</p>' % fn_html(p) for p in a["body"]), refs_html(a["refs"])))
    body.append('</section>')

    nav.append('<div class="toc-h">多特信经 · 四项教义</div>')
    body.append('<section class="sec" id="cod"><div class="eyebrow">CANONES DORDRACENI · 1618–19</div><h2>多特信经</h2>'
                '<p class="lead">%s</p>' % E(INTRO["cod"].split("\n")[0]))
    for j, s in enumerate(COD):
        sid = "cod%d" % (j + 1)
        nav.append('<a href="#%s"><span class="no">%s</span>%s</a>' % (sid, ["一", "二", "三四", "五"][j], E(s["title"])))
        body.append('<div class="tpart misery" id="%s">%s</div>' % (sid, E(s["title"])))
        for a in s["arts"]:
            body.append('<article class="tx misery%s"><h3>%s</h3>%s%s</article>'
                        % (" rej" if "错谬" in a["title"] else "", E(a["title"]),
                           ''.join('<p>%s</p>' % fn_html(p) for p in a["body"]), refs_html(a["refs"])))
    body.append('</section>')

    return ('<!DOCTYPE html><html lang="zh-Hans"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<title>原文阅读室 · 三大信经与三项联合信条</title>'
            '<meta name="description" content="三大普世信经与三项联合信条（海德堡要理问答、比利时信条、多特信经）中文全文，一字不差引自 ccifellowship.org。">'
            '<style>%s%s%s</style></head><body class="texts">%s<div id="prog"></div>'
            '<div class="topbar"><div class="tb"><button class="btn on" id="tocBtn">目录</button>'
            '<div class="brand">原文阅读室 · <b>TEXTUS</b></div><div class="sp"></div>'
            '<div class="tbs"><input id="q" type="search" placeholder="在全文中查找…" aria-label="查找"></div>'
            '<button class="btn" id="fsBtn">字号</button><button class="btn" id="themeBtn">主题</button>'
            '<a class="btn" href="index.html">← 返回解读</a></div></div><div class="scrim"></div>'
            '<div class="shell"><nav class="side"><div class="toc">%s</div></nav><main class="main">'
            '<header class="hero"><div class="lat">TEXTUS RECEPTUS · FORMULAE UNITATIS</div><h1>原文阅读室</h1>'
            '<div class="zh">三大普世信经 · 海德堡要理问答 · 比利时信条 · 多特信经</div><div class="rl"></div>'
            '<p class="ld">本页全部信经与信条正文均<strong>一字不差</strong>引自 '
            '<a href="%s" target="_blank" rel="noopener">基督教华人网络团契 ccifellowship.org</a>（Book of Praise 中译），'
            '包括其脚注编号（以上标显示）与经文出处。只作排版，不改一字。</p>%s</header>%s'
            '<footer class="srcfoot">文本来源：<a href="%s">ccifellowship.org</a> · 排版：海德堡 52 主日学习站 v3</footer>'
            '</main></div><script>%s</script></body></html>'
            % (CSS, CSS2, CSS3, ICONS, ''.join(nav), SRC, forms_stats(), ''.join(body), SRC, TEXTS_JS))


TEXTS_JS = r"""
(function(){var d=document,b=d.body,ls={};try{ls=window.localStorage||{}}catch(e){}
var sh=d.querySelector('.shell'),tb=d.getElementById('tocBtn'),sc=d.querySelector('.scrim');
function mob(){return innerWidth<980}
tb.onclick=function(){if(mob()){b.classList.toggle('tocopen')}else{sh.classList.toggle('hid');tb.classList.toggle('on')}};
sc.onclick=function(){b.classList.remove('tocopen')};
d.querySelectorAll('.toc a').forEach(function(a){a.addEventListener('click',function(){if(mob())b.classList.remove('tocopen')})});
var th=['auto','light','dark'],ti=0;try{ti=Math.max(0,th.indexOf(ls.getItem('hcTheme')))}catch(e){}
function at(){if(th[ti]==='auto')d.documentElement.removeAttribute('data-theme');else d.documentElement.setAttribute('data-theme',th[ti])}
at();d.getElementById('themeBtn').onclick=function(){ti=(ti+1)%3;at();try{ls.setItem('hcTheme',th[ti])}catch(e){}};
var fs=[1,1.12,.92],fi=0;d.getElementById('fsBtn').onclick=function(){fi=(fi+1)%3;d.documentElement.style.setProperty('--tz',fs[fi])};
var q=d.getElementById('q'),arts=[].slice.call(d.querySelectorAll('.tx')),t;
q.addEventListener('input',function(){clearTimeout(t);t=setTimeout(function(){var v=q.value.trim();
 arts.forEach(function(a){a.classList.toggle('hidden',!!v&&a.textContent.indexOf(v)<0)})},150)});
var p=d.getElementById('prog');addEventListener('scroll',function(){var h=d.documentElement;
 p.style.width=(h.scrollTop/(h.scrollHeight-h.clientHeight)*100)+'%'},{passive:true});
})();
"""

CSS3 = r"""
/* ===== v3 layer：大字号 · 重点/难点 · 记忆墙 ===== */
:root{--tz:1}
body{font-size:calc(18.5px*var(--tz));line-height:1.9}
@media (max-width:640px){body{font-size:calc(17.5px*var(--tz))}}
.toc a{font-size:15px;line-height:1.5;padding:5px 8px 5px 10px}
.toc a .no{font-size:12px}
.toc-h{font-size:12px}
.btn{font-size:13.5px;padding:8px 12px;border-radius:10px}
.brand{font-size:14px}
.tbs input{font-size:15px;padding:8px 12px;border-radius:10px}
.eyebrow{font-size:12.5px}
.blk h3{font-size:16px}
.blk p,.lead{font-size:1em}
figcaption{font-size:13px;letter-spacing:.06em;line-height:1.6}
.fnote{font-size:15px}
table{font-size:15.5px}
th{font-size:13px}
.hero .stats{font-size:12.5px}
.act-g,.ch-g,.fx-g,.tl-d{font-size:15px}
.act-r,.fx-r,.ch-r,.act-h{font-size:12.5px}
.tl-t{font-size:17px}
.mm-cn{font-size:15.5px}
/* LD v3 */
.ld.v3 .ld-h h3{font-size:clamp(24px,3vw,32px);margin:0 0 6px}
.ld.v3 .ld-meta span{font-size:13px;padding:3px 11px}
.ld.v3 .qa{margin:0 0 14px;padding:14px 18px}
.ld.v3 .qa .qn{font-family:var(--sans);font-size:13px;color:var(--pc);letter-spacing:.08em;font-weight:600}
.ld.v3 .qa .q{font-size:1.08em;font-weight:700;color:var(--royal);margin:2px 0 6px}
.ld.v3 .qa .a{font-size:1.03em;line-height:2}
.qa sup,.tx sup{font-size:.62em;color:var(--brass);font-family:var(--sans);margin:0 1px}
.keyline{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:14px;padding:18px 20px 0}
.kb{border-radius:14px;padding:14px 18px;position:relative;overflow:hidden}
.kb p{margin:8px 0 0;font-size:1.06em;line-height:1.8}
.kb-core{background:linear-gradient(120deg,color-mix(in srgb,var(--pc) 20%,var(--paper)),color-mix(in srgb,var(--pc) 6%,var(--paper)));
  border:1.5px solid color-mix(in srgb,var(--pc) 45%,transparent)}
.kb-core p{font-weight:700;color:var(--ink);font-size:1.12em}
.kb-core::after{content:"";position:absolute;inset:0;background:linear-gradient(100deg,transparent 30%,rgba(255,255,255,.35) 50%,transparent 70%);
  transform:translateX(-100%);pointer-events:none}
.ld.v3.in .kb-core::after{animation:shine 1.6s .4s ease}
@keyframes shine{to{transform:translateX(100%)}}
.kb-memo{background:linear-gradient(120deg,color-mix(in srgb,var(--brass) 22%,var(--paper)),var(--paper));border:1.5px dashed color-mix(in srgb,var(--brass) 55%,transparent)}
.badge{display:inline-flex;align-items:center;gap:3px;font-family:var(--sans);font-size:12.5px;font-weight:700;letter-spacing:.1em;
  color:#fff;border-radius:99px;padding:3px 12px 3px 9px}
.b-key{background:var(--pc);box-shadow:0 4px 12px -4px var(--pc)}
.b-memo{background:var(--brass)}
.tile p{font-size:.92em;line-height:1.85}
.tile .tl{font-size:13px;letter-spacing:.08em}
.tile .ic{width:20px;height:20px;padding:3px;border-radius:7px;background:color-mix(in srgb,currentColor 14%,transparent);box-sizing:content-box}
.tile.t-warn{border-width:1.5px}
.tile.t-ana{border-top:3px solid var(--pc)}
.tile.t-logic .tl{color:var(--royal)}
.vchip{font-size:13.5px;padding:3px 10px}
details.deep>summary{font-size:14.5px}
details.deep .tile p,details.deep .pt{opacity:.92}
.pt{font-size:.95em}
.term{font-size:.92em}
.srcnote{font-family:var(--sans);font-size:12px;color:var(--muted);text-align:right}
.srcnote a,.rnote a{color:var(--teal)}
details.refs{margin-top:6px}
details.refs>summary{cursor:pointer;font-family:var(--sans);font-size:13px;color:var(--teal);list-style:none;display:inline-flex;align-items:center;gap:4px}
details.refs>summary::-webkit-details-marker{display:none}
details.refs ol{margin:6px 0 0;padding-left:2.2em;font-family:var(--sans);font-size:13.5px;color:var(--ink-2);line-height:1.7;columns:2 220px}
body.drill .qa .refs{display:none}
@media (max-width:860px){.keyline{grid-template-columns:1fr;padding:14px 12px 0}}
/* reader v3 */
.rpane{columns:2 380px}
.rintro{font-size:14.5px;color:var(--muted);line-height:1.7;margin:8px 0 6px}
.rl{border-left:3px solid var(--c);padding:2px 0 2px 12px;margin:0 0 8px;break-inside:avoid}
/* donut */
.dwrap{display:grid;grid-template-columns:minmax(180px,260px) 1fr;gap:24px;align-items:center}
.donut{width:100%;height:auto}
.dseg{animation:dash 1.2s cubic-bezier(.3,.8,.3,1) both}
@keyframes dash{from{stroke-dasharray:0 999}}
.dn1{font-family:var(--disp);font-size:34px;fill:var(--royal)}
.dn2{font-family:var(--sans);font-size:11px;fill:var(--muted)}
.dleg{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.dl{border-radius:12px;padding:12px 14px;background:color-mix(in srgb,var(--c) 12%,var(--paper));border-left:4px solid var(--c);display:grid}
.dl b{font-family:var(--disp);font-size:30px;color:var(--c);line-height:1}
.dl span{font-weight:700}
.dl em{font-style:normal;font-family:var(--sans);font-size:12.5px;color:var(--muted)}
@media (max-width:640px){.dwrap{grid-template-columns:1fr}.donut{max-width:240px;margin:auto}}
/* memory wall */
.mwall{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,250px),1fr));gap:10px}
.mw{--pc:var(--deliver);display:grid;grid-template-columns:auto 1fr;gap:2px 10px;padding:12px 14px;border-radius:12px;text-decoration:none;color:var(--ink);
  background:linear-gradient(140deg,color-mix(in srgb,var(--pc) 13%,var(--paper)),var(--paper));border:1px solid color-mix(in srgb,var(--pc) 28%,var(--rule));
  transition:transform .25s,box-shadow .25s}
.mw.misery{--pc:var(--misery)}.mw.gratitude{--pc:var(--gratitude)}.mw.prologue{--pc:var(--prologue)}
.mw:hover{transform:translateY(-3px) scale(1.01);box-shadow:var(--sh2)}
.mwn{grid-row:span 2;width:34px;height:34px;border-radius:10px;background:var(--pc);color:#fff;display:grid;place-items:center;font-family:var(--disp);font-size:16px}
.mw b{font-size:15.5px}
.mw i{font-style:normal;font-size:14px;line-height:1.6;color:var(--ink-2)}
/* forms stats */
.fstats{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:12px;margin:18px 0}
.fst{display:grid;gap:2px;padding:16px 18px;border-radius:14px;text-decoration:none;color:var(--ink);
  background:linear-gradient(140deg,color-mix(in srgb,var(--c) 20%,var(--paper-2)),var(--paper-2));border:1px solid color-mix(in srgb,var(--c) 35%,var(--rule));transition:transform .25s}
.fst:hover{transform:translateY(-3px)}
.fst .ic{width:28px;height:28px;color:var(--c)}
.fst b{font-family:var(--disp);font-size:21px;color:var(--c)}
.fst span{font-family:var(--sans);font-size:13.5px}
.fst em{font-style:normal;font-size:13px;color:var(--muted)}
/* texts page */
body.texts .main{max-width:none}
.tx{--pc:var(--deliver);background:var(--paper-2);border:1px solid var(--rule);border-left:4px solid var(--pc);border-radius:14px;padding:16px 20px;margin:14px 0;box-shadow:var(--sh)}
.tx.misery{--pc:var(--misery)}.tx.gratitude{--pc:var(--gratitude)}.tx.prologue{--pc:var(--prologue)}
.tx.rej{border-left-style:dashed}
.tx h3{font-family:var(--disp);font-size:1.25em;color:var(--royal);margin:0 0 10px;display:flex;flex-wrap:wrap;gap:10px;align-items:baseline}
.tx h3 small{font-family:var(--sans);font-size:12px;color:var(--brass);letter-spacing:.16em}
.tno{font-family:var(--sans);font-size:13px;background:var(--pc);color:#fff;border-radius:99px;padding:2px 10px}
.tback{margin-left:auto;font-family:var(--sans);font-size:13px;color:var(--teal)}
.tx p{margin:0 0 10px;line-height:2}
.tintro{font-size:.88em;color:var(--muted)}
.tl1{border-left:3px solid var(--pc);padding-left:12px}
.tqa{padding:10px 0;border-top:1px dashed var(--rule)}
.tqa:first-of-type{border-top:0}
.tq{font-weight:700;color:var(--royal)}
.tq b{color:var(--pc)}
.ta{line-height:2}
.tpart{margin:34px 0 6px;font-family:var(--disp);font-size:1.3em;color:#fff;background:var(--pc,var(--deliver));border-radius:12px;padding:10px 18px}
.tpart.misery{--pc:var(--misery)}.tpart.gratitude{--pc:var(--gratitude)}.tpart.prologue{--pc:var(--prologue)}.tpart.deliver{--pc:var(--deliver)}
.hidden{display:none!important}
.srcfoot{margin:40px 0;font-family:var(--sans);font-size:13px;color:var(--muted);text-align:center}
.hero a{color:var(--teal)}
.toc a.toc-src{background:color-mix(in srgb,var(--teal) 12%,transparent);color:var(--teal);font-weight:600;margin:4px 0 8px}
"""
