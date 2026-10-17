# -*- coding: utf-8 -*-
"""v2 视觉层：平铺自适应网格、毛玻璃、图标、动画、信经背诵室、三信条对比"""
import html
from creeds_text import READERS, FORMS_CMP, WHY_THREE, TRIAD

E = lambda s: html.escape(str(s), quote=False)

_P = {
 "book": '<path d="M4 4h7a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4z"/><path d="M20 4h-6a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h7z"/>',
 "cross": '<path d="M12 2v20M5 8h14"/>',
 "core": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1" fill="currentColor"/>',
 "flow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "scroll": '<path d="M8 3h11v15a3 3 0 0 1-3 3H6a3 3 0 0 1-3-3V6h5"/><path d="M8 3v13"/>',
 "lang": '<path d="M4 5h9M8.5 3v2M6 5c1 4 4 7 7 8M11 5c-1 4-4 7-7 8"/><path d="M14 21l4-9 4 9M15.5 18h5"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
 "brain": '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 3 3h1V4z"/><path d="M15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-3 3h-1V4z"/>',
 "arc": '<path d="M3 18c4-12 14-12 18 0"/><circle cx="3" cy="18" r="1.5"/><circle cx="21" cy="18" r="1.5"/>',
 "eye": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "link": '<path d="M10 14a4 4 0 0 0 6 0l3-3a4 4 0 0 0-6-6l-1 1"/><path d="M14 10a4 4 0 0 0-6 0l-3 3a4 4 0 0 0 6 6l1-1"/>',
 "alert": '<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18v.5"/>',
 "key": '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3"/>',
 "map": '<path d="M12 21s-7-6-7-12a7 7 0 0 1 14 0c0 6-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
 "layers": '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
 "chev": '<path d="M6 9l6 6 6-6"/>',
}
ICONS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true">'
         + ''.join('<symbol id="i-%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
                   'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">%s</symbol>' % (k, v)
                   for k, v in _P.items()) + '</svg>')


def ic(name, cls="ic"):
    return '<svg class="%s" aria-hidden="true"><use href="#i-%s"/></svg>' % (cls, name)


PARTC = {"总纲": "prologue", "困苦": "misery", "拯救": "deliver", "感恩": "gratitude"}


def render_ld(d, A, PL):
    k = d["key"]
    q0, q1 = d["qas"][0][0], d["qas"][-1][0]
    qn = "问 %d" % q0 if q0 == q1 else "问 %d–%d" % (q0, q1)
    left = (q0 - 1) / 129 * 100
    wid = max((q1 - q0 + 1) / 129 * 100, 1.2)
    qas = ''.join('<div class="qa"><div class="qn">%s 问 %d</div><div class="q">%s</div>'
                  '<p class="a">%s</p></div>' % (ic("mic", "ic s"), n, E(q), E(a)) for n, q, a in d["qas"])
    terms = ''.join('<div class="term"><span class="%s">%s</span><span class="tgloss">%s%s</span></div>'
                    % (cls, E(t), '' if tr == "—" else '<i>%s</i>' % E(tr), E(gl))
                    for cls, t, tr, gl in d["terms"])
    ana = ''.join('<p class="pt"><b>%s。</b>%s</p>' % (E(t), E(x)) for t, x in d["analysis"])
    ang = ''.join('<p class="pt"><b>%s。</b>%s</p>' % (E(t), E(x)) for t, x in d["angles"])
    verses = ''.join('<span class="vchip">%s</span>' % E(v.strip()) for v in d["verses"].split("；") if v.strip())
    s = " ".join([d["title"], d["theme"], d["part"], d["core"], d["logic"], d["memo"], d["caution"],
                  d["context"], d["canon"], d["confess"], d["verses"],
                  " ".join(q + a for _, q, a in d["qas"]),
                  " ".join(t + x for t, x in d["analysis"] + d["angles"]),
                  " ".join(t + tr + gl for _, t, tr, gl in d["terms"]), "主日%d LD%d" % (d["n"], d["n"])])

    def tile(icon, lab, body, cls=""):
        return '<div class="tile %s"><div class="tl">%s<span>%s</span></div>%s</div>' % (cls, ic(icon), lab, body)

    return f'''<section class="ld v2 {k} rv" id="ld{d['n']}" data-n="{d['n']}" data-s="{A(s)}">
<div class="ld-h"><div class="ld-no">{d['n']}</div><div class="ld-ht"><h3>{E(d['title'])}</h3>
<div class="ld-meta"><span>主日 {d['n']}</span><span>{qn}</span><span class="pp">{E(d['part'])} · {PL[d['part']]}</span><span>{E(d['theme'])}</span></div>
<div class="qpos" title="在 129 问中的位置"><i style="left:{left:.2f}%;width:{wid:.2f}%"></i></div></div>
<label class="chk"><input type="checkbox" data-n="{d['n']}">已背熟</label></div>
<div class="ld-g">
 <div class="ld-main">{qas}
  <div class="core">{ic("core")}<div>{E(d['core'])}</div></div>
  <div class="memo">{ic("key")}<div>{E(d['memo'])}</div></div>
 </div>
 <div class="ld-side">
  {tile("flow", "逻辑推进", '<p>%s</p>' % E(d['logic']), "t-logic")}
  {tile("book", "经文根据", '<div class="vchips">%s</div>' % verses)}
  {tile("clock", "真实背景 · 为什么写", '<p>%s</p>' % E(d['context']), "t-ctx")}
 </div>
</div>
<div class="ld-g3">
 {tile("brain", "神学剖析", ana, "wide")}
 {tile("arc", "正典定位", '<p>%s</p>' % E(d['canon']))}
 {tile("lang", "原文钥词", '<div class="terms">%s</div>' % terms)}
</div>
<details class="deep"><summary>{ic("layers")}<span>深入：多视角对照 · 信条互参 · 误读警示</span>{ic("chev", "ic chev")}</summary>
<div class="ld-g3">
 {tile("eye", "多视角对照", ang, "wide")}
 {tile("link", "信条互参", '<p class="cf">%s</p>' % E(d['confess']))}
 {tile("alert", "误读警示", '<p>%s</p>' % E(d['caution']), "t-warn")}
</div></details></section>'''


def readers_section():
    tabs = ''.join('<button class="rtab%s" data-r="%s">%s</button>' % (" on" if i == 0 else "", r["id"], E(r["name"]))
                   for i, r in enumerate(READERS))
    panes = []
    for i, r in enumerate(READERS):
        body = ''.join('<div class="rp"><div class="rph" style="--c:var(--%s)">%s</div>%s</div>'
                       % (r["color"], E(h), ''.join('<p class="rl">%s</p>' % E(x) for x in lines))
                       for h, lines in r["parts"])
        panes.append('<article class="rpane%s" id="%s"><header><h3>%s</h3><div class="rlat">%s</div></header>%s</article>'
                     % (" on" if i == 0 else "", r["id"], E(r["name"]), E(r["latin"]), body))
    return ('<div class="reader glass"><div class="rbar">%s<span class="sp"></span>'
            '<button class="btn" id="rHide">逐句遮盖</button><button class="btn" id="rSize">字号</button></div>%s'
            '<p class="rnote">诵读文本据拉丁／希腊原文译出，句读按背诵节奏分行；正式礼仪诵读请以所属教会采用的标准中译本为准。'
            '点按「逐句遮盖」后，轻点每一句即可显示或再次遮盖。</p></div>') % (tabs, ''.join(panes))


def forms_section(table, fig):
    tri = ''.join('<div class="tri" style="--c:var(--%s)"><b>%s</b><span>%s</span><em>%s</em></div>'
                  % (c, E(a), E(b), E(x)) for a, b, x, c in TRIAD)
    why = ''.join('<div class="tile"><div class="tl">%s<span>%s</span></div><p>%s</p></div>'
                  % (ic("core"), E(a), E(b)) for a, b in WHY_THREE)
    tl = ('<svg viewBox="0 0 720 150" class="ftl" role="img" aria-label="三项联合信条时间与地理">'
          '<line x1="40" y1="75" x2="680" y2="75" stroke="var(--rule)" stroke-width="2"/>'
          + ''.join('<g class="pop" style="animation-delay:%.1fs"><circle cx="%d" cy="75" r="11" fill="var(--%s)"/>'
                    '<text x="%d" y="45" text-anchor="middle" class="t1">%s</text>'
                    '<text x="%d" y="112" text-anchor="middle" class="t2">%s</text>'
                    '<text x="%d" y="132" text-anchor="middle" class="t3">%s</text></g>'
                    % (i * .35, x, c, x, y, x, n, x, p)
                    for i, (x, y, n, p, c) in enumerate([
                        (90, "1561", "比利时信条", "图尔奈", "deliver"),
                        (250, "1563", "海德堡要理问答", "海德堡", "gratitude"),
                        (420, "1610", "抗辩派五条", "豪达", "muted"),
                        (610, "1618–19", "多特信经 · 合一三信条", "多特勒支", "misery")]))
          + '</svg>')
    return (fig("图 · 三项联合信条：时间与地点（1561 → 1619）", tl)
            + '<div class="triad">%s</div>' % tri
            + fig("表 · 三项联合信条深度对比", table(FORMS_CMP))
            + '<div class="eyebrow" style="margin-top:22px">为什么是三份，而不是一份？</div>'
            + '<div class="bento">%s</div>' % why)


CSS2 = r"""
/* ===== v2 layer ===== */
:root{--glass:color-mix(in srgb,var(--paper-2) 72%,transparent);--r:16px;
  --sh2:0 10px 30px -12px rgba(20,22,28,.18),0 2px 6px -2px rgba(20,22,28,.06)}
.shell{max-width:none}
.tb{max-width:none}
.main{padding:0 clamp(14px,3vw,44px) 110px}
.hero .ld,.lead{max-width:none}
.sec>p.lead{max-width:62em}
.ic{width:18px;height:18px;flex:none;vertical-align:-3px}
.ic.s{width:13px;height:13px;margin-right:4px}
.glass,.topbar{background:var(--glass);backdrop-filter:blur(16px) saturate(1.4);-webkit-backdrop-filter:blur(16px) saturate(1.4)}
.hero{position:relative;overflow:hidden;border-radius:0 0 var(--r) var(--r)}
.hero::before{content:"";position:absolute;inset:-40% -10% auto auto;width:60vw;height:60vw;max-width:720px;max-height:720px;
  background:radial-gradient(circle,rgba(31,56,100,.16),transparent 62%),radial-gradient(circle at 70% 70%,rgba(160,118,34,.16),transparent 55%);
  animation:float 18s ease-in-out infinite alternate;pointer-events:none;z-index:-1}
@keyframes float{to{transform:translate(-8%,10%) rotate(18deg)}}
/* intro blocks tile */
.sec{display:block}
.sec .blk{background:var(--paper-2);border:1px solid var(--rule);border-radius:12px;padding:16px 18px;box-shadow:var(--sh)}
.blkgrid,.bento{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:14px;margin:16px 0}
.blkgrid .blk{margin:0}
/* LD v2 */
.ld.v2{max-width:none;border-radius:var(--r);overflow:hidden;box-shadow:var(--sh2);border:1px solid var(--rule);
  background:var(--paper-2);margin:26px 0;--pc:var(--deliver)}
.ld.v2.misery{--pc:var(--misery)}.ld.v2.gratitude{--pc:var(--gratitude)}.ld.v2.prologue{--pc:var(--prologue)}
.ld.v2 .ld-h{background:linear-gradient(120deg,color-mix(in srgb,var(--pc) 16%,var(--paper-2)),var(--paper-2) 70%);
  border-bottom:1px solid var(--rule);display:flex;gap:16px;align-items:flex-start;padding:16px 20px}
.ld.v2 .ld-no{background:var(--pc);color:#fff;border-radius:14px;min-width:54px;height:54px;display:grid;place-items:center;
  font-size:24px;box-shadow:0 6px 16px -6px var(--pc)}
.ld.v2 .ld-ht{flex:1;min-width:0}
.ld.v2 .ld-meta{display:flex;flex-wrap:wrap;gap:6px}
.ld.v2 .ld-meta span{font-family:var(--sans);font-size:11px;padding:2px 9px;border-radius:99px;background:var(--paper-3);color:var(--ink-2);white-space:nowrap}
.ld.v2 .ld-meta .pp{background:var(--pc);color:#fff}
.qpos{position:relative;height:5px;border-radius:9px;background:var(--paper-3);margin-top:10px;overflow:hidden}
.qpos i{position:absolute;top:0;bottom:0;background:var(--pc);border-radius:9px}
.ld-g{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:16px;padding:18px 20px 4px}
.ld-g3{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:14px;padding:12px 20px 18px}
.ld-g3 .wide{grid-column:span 2}
.ld-side{display:grid;gap:12px;align-content:start}
.tile{background:var(--paper);border:1px solid var(--rule);border-radius:12px;padding:12px 15px;min-width:0;
  transition:transform .25s ease,box-shadow .25s ease}
.tile:hover{transform:translateY(-2px);box-shadow:var(--sh2)}
.tile p{margin:0 0 6px;font-size:15.5px;line-height:1.75;color:var(--ink-2)}
.tile .tl{display:flex;align-items:center;gap:7px;font-family:var(--sans);font-size:11.5px;letter-spacing:.12em;
  color:var(--pc,var(--brass));margin-bottom:6px;font-weight:600}
.tile.t-warn{background:color-mix(in srgb,var(--rubric) 7%,var(--paper));border-color:color-mix(in srgb,var(--rubric) 30%,var(--rule))}
.tile.t-warn .tl{color:var(--rubric)}
.tile.t-ctx .tl{color:var(--teal)}
.ld.v2 .qa{border-left:3px solid var(--pc);background:color-mix(in srgb,var(--pc) 5%,transparent);border-radius:0 10px 10px 0;padding:10px 14px}
.ld.v2 .qa .q{font-size:17.5px}
.ld.v2 .qa .a{font-size:17px;color:var(--ink);line-height:1.9}
.ld.v2 .core,.ld.v2 .memo{display:flex;gap:10px;align-items:flex-start;border-radius:12px;padding:12px 15px;margin:12px 0;border:0}
.ld.v2 .core::before,.ld.v2 .memo::before{display:none}
.ld.v2 .core{background:linear-gradient(135deg,color-mix(in srgb,var(--royal) 13%,transparent),transparent);color:var(--royal);font-weight:600}
.ld.v2 .memo{background:linear-gradient(135deg,color-mix(in srgb,var(--brass) 20%,transparent),transparent);color:var(--ink)}
.ld.v2 .core .ic,.ld.v2 .memo .ic{margin-top:4px}
.ld.v2 .memo .ic{color:var(--brass)}
.vchips{display:flex;flex-wrap:wrap;gap:5px}
.vchip{font-family:var(--sans);font-size:12px;padding:2px 8px;border-radius:7px;background:color-mix(in srgb,var(--teal) 12%,transparent);color:var(--teal)}
details.deep{border-top:1px dashed var(--rule)}
details.deep>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:8px;padding:11px 20px;
  font-family:var(--sans);font-size:13px;color:var(--muted)}
details.deep>summary::-webkit-details-marker{display:none}
details.deep>summary:hover{color:var(--royal)}
details.deep .chev{margin-left:auto;transition:transform .25s}
details.deep[open] .chev{transform:rotate(180deg)}
details.deep[open]>.ld-g3{animation:drop .35s ease}
@keyframes drop{from{opacity:0;transform:translateY(-6px)}}
/* reveal */
.rv{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .6s cubic-bezier(.2,.7,.2,1)}
.rv.in{opacity:1;transform:none}
/* reader */
.reader{border:1px solid var(--rule);border-radius:var(--r);padding:16px clamp(12px,3vw,28px);box-shadow:var(--sh2)}
.rbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:12px}
.rbar .sp{flex:1}
.rtab{border:1px solid var(--rule);background:var(--paper);color:var(--ink-2);border-radius:99px;padding:6px 16px;
  font-family:var(--sans);font-size:14px;cursor:pointer;transition:all .2s}
.rtab.on{background:var(--royal);color:#fff;border-color:var(--royal)}
.rpane{display:none;columns:2 340px;column-gap:34px}
.rpane.on{display:block;animation:drop .35s ease}
.rpane header{column-span:all;margin-bottom:8px}
.rpane h3{font-family:var(--disp);font-size:26px;margin:0;color:var(--royal)}
.rlat{font-family:var(--disp);font-size:12px;letter-spacing:.2em;color:var(--brass)}
.rp{break-inside:avoid;margin:0 0 14px}
.rph{display:inline-block;font-family:var(--sans);font-size:12px;letter-spacing:.14em;color:#fff;background:var(--c);
  border-radius:99px;padding:2px 12px;margin-bottom:6px}
.rl{margin:0 0 4px;font-size:var(--rfs,19px);line-height:1.9;color:var(--ink);transition:filter .25s,background .25s;border-radius:6px}
.reader.cov .rl{filter:blur(6px);background:var(--paper-3);cursor:pointer;user-select:none}
.reader.cov .rl.sh{filter:none;background:transparent}
.rnote{font-size:13px;color:var(--muted);margin:10px 0 0}
/* forms */
.ftl{width:100%;height:auto;display:block}
.ftl .t1{font-family:var(--disp);font-size:16px;fill:var(--ink)}
.ftl .t2{font-family:var(--sans);font-size:13px;fill:var(--ink-2)}
.ftl .t3{font-family:var(--sans);font-size:11px;fill:var(--muted)}
.pop{animation:pop .7s cubic-bezier(.2,1.4,.4,1) both;transform-box:fill-box;transform-origin:center}
@keyframes pop{from{opacity:0;transform:scale(.4)}}
.triad{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));gap:12px;margin:14px 0}
.tri{border-radius:14px;padding:16px;background:linear-gradient(140deg,color-mix(in srgb,var(--c) 22%,var(--paper-2)),var(--paper-2));
  border:1px solid color-mix(in srgb,var(--c) 35%,var(--rule));display:grid;gap:2px}
.tri b{font-family:var(--disp);font-size:36px;color:var(--c);line-height:1}
.tri span{font-weight:600;color:var(--ink)}
.tri em{font-style:normal;font-family:var(--sans);font-size:12.5px;color:var(--muted)}
/* tables & figures */
.tw{border-radius:12px;border:1px solid var(--rule);overflow-x:auto}
.tw table{margin:0}
.tw tbody tr:nth-child(odd){background:color-mix(in srgb,var(--paper-3) 55%,transparent)}
.tw tbody tr:hover{background:color-mix(in srgb,var(--brass) 10%,transparent)}
.cards .card{border-radius:14px;transition:transform .25s,box-shadow .25s}
.cards .card:hover{transform:translateY(-3px);box-shadow:var(--sh2)}
.toc a{border-radius:8px;transition:background .2s,padding .2s}
.toc a:hover{padding-left:12px}
@media (max-width:860px){
  .ld-g{grid-template-columns:1fr}
  .ld-g3 .wide{grid-column:auto}
  .ld.v2 .ld-h{flex-wrap:wrap;padding:14px}
  .ld-g,.ld-g3{padding-left:12px;padding-right:12px}
  details.deep>summary{padding:11px 12px}
}
@media (prefers-reduced-motion:reduce){.rv{opacity:1;transform:none;transition:none}.hero::before,.pop{animation:none}}
@media print{.rv{opacity:1;transform:none}details.deep>*{display:block}}
"""

JS2 = r"""
(function(){
var d=document;
/* group consecutive intro .blk into tiled grids */
d.querySelectorAll('.sec').forEach(function(s){
  var kids=[].slice.call(s.children),run=[];
  function flush(){if(run.length>1){var g=d.createElement('div');g.className='blkgrid';
    run[0].parentNode.insertBefore(g,run[0]);run.forEach(function(x){g.appendChild(x);});}run=[];}
  kids.forEach(function(k){if(k.classList.contains('blk'))run.push(k);else flush();});flush();
});
/* reveal */
var els=d.querySelectorAll('.rv,.sec,.fig,.card');
if('IntersectionObserver' in window){
  els.forEach(function(e){if(!e.classList.contains('rv'))e.classList.add('rv');});
  var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}});},{rootMargin:'0px 0px -6% 0px'});
  els.forEach(function(e){io.observe(e);});
  setTimeout(function(){var h=location.hash&&d.querySelector(location.hash);if(h)h.scrollIntoView();},60);
}else els.forEach(function(e){e.classList.add('in');});
/* search / jump must reveal */
d.addEventListener('click',function(e){var a=e.target.closest('a[href^="#"]');if(!a)return;
  var t=d.querySelector(a.getAttribute('href'));if(t){t.classList.add('in');t.querySelectorAll('.rv').forEach(function(x){x.classList.add('in');});}});
/* reader */
var rd=d.querySelector('.reader');if(!rd)return;
rd.querySelectorAll('.rtab').forEach(function(b){b.onclick=function(){
  rd.querySelectorAll('.rtab').forEach(function(x){x.classList.toggle('on',x===b);});
  rd.querySelectorAll('.rpane').forEach(function(p){p.classList.toggle('on',p.id===b.dataset.r);});};});
d.getElementById('rHide').onclick=function(){rd.classList.toggle('cov');this.classList.toggle('on');
  rd.querySelectorAll('.rl').forEach(function(l){l.classList.remove('sh');});};
rd.addEventListener('click',function(e){var l=e.target.closest('.rl');if(l&&rd.classList.contains('cov'))l.classList.toggle('sh');});
var fs=[19,22,16],fi=0;d.getElementById('rSize').onclick=function(){fi=(fi+1)%3;rd.style.setProperty('--rfs',fs[fi]+'px');};
})();
"""
