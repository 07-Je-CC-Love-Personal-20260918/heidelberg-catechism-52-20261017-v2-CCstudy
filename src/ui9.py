# -*- coding: utf-8 -*-
"""v9：性能（按需渲染、离屏暂停动画、精简毛玻璃）· Lenis 惯性平滑滚动 · 新版重点标记（无波浪线）· 序数徽章"""
import os, re

_D = os.path.dirname(os.path.abspath(__file__))
LENIS_JS = open(os.path.join(_D, "vendor", "lenis.min.js"), encoding="utf-8").read()
LENIS_CSS = open(os.path.join(_D, "vendor", "lenis.css"), encoding="utf-8").read()

CSS9 = LENIS_CSS + r"""
/* ===== v9 性能 ===== */
#prog{width:100%!important;transform-origin:0 50%;transform:scaleX(0);will-change:transform}
html.lenis,html.lenis body{height:auto}
html{scroll-behavior:auto!important}
.ld,.appsec{content-visibility:auto!important;contain-intrinsic-size:auto 1400px!important}
.sec.introsec{content-visibility:auto;contain-intrinsic-size:auto 1200px}
/* 毛玻璃只留顶栏与弹层；大面积容器改实色半透明 */
.glass:not(.topbar),.zbtn,.mklegend,.reader,.fc-wrap{backdrop-filter:none!important;-webkit-backdrop-filter:none!important;background:color-mix(in srgb,var(--paper-2) 94%,transparent)!important}
.topbar{backdrop-filter:blur(14px) saturate(1.3);-webkit-backdrop-filter:blur(14px) saturate(1.3)}
/* 常驻无限动画：标题图标改为悬停才动；其余离屏暂停 */
.h2e{animation:none!important;transition:transform .35s cubic-bezier(.3,1.6,.5,1)}
.sec h2:hover .h2e{transform:rotate(-10deg) scale(1.18)}
.ld-emo{animation:none!important;transition:transform .4s cubic-bezier(.3,1.6,.5,1)}
.ld.v3:hover .ld-emo{transform:translateY(-4px) rotate(-6deg) scale(1.08)}
.flow7,.a3e,.a3arrow span,.hero h1,.fc-emo,.pulse{animation-play-state:paused!important}
.live .flow7,.live .a3e,.live .a3arrow span,.live.hero h1,.live .hero h1,.live .fc-emo,.live .pulse,.hero.live h1{animation-play-state:running!important}
.tile,.mw,.hm a,.cards .card{will-change:auto}
.tile:hover,.mw:hover{transition-duration:.2s}
/* 入场动画更轻：只做透明度与小位移，GPU 合成 */
.rv{transition:opacity .5s ease,transform .5s cubic-bezier(.2,.8,.2,1)!important}
html.io .rv:not(.in){transform:translate3d(0,14px,0)}

/* ===== v9 重点标记：不再使用波浪线 ===== */
mark.mk{font-weight:700;padding:0 2px;margin:0 1px;border-radius:4px;-webkit-box-decoration-break:clone;box-decoration-break:clone;text-decoration:none!important;border:0!important;box-shadow:none!important}
/* 神 · 三一：紫字 + 浅紫区块 */
mark.mk-god{color:#6A3FC0!important;background:rgba(112,72,192,.12)!important}
/* 罪 · 律法：红字 + 红色实线下划 */
mark.mk-sin{color:#C21F35!important;background:none!important;box-shadow:inset 0 -2px 0 rgba(194,31,53,.75)!important;border-radius:0}
/* 基督 · 恩典：蓝字 + 下半荧光 */
mark.mk-chr{color:#1D4FBF!important;background:linear-gradient(transparent 52%,rgba(36,87,197,.20) 52%)!important}
/* 圣灵 · 信心：青字 + 青色虚线下划 */
mark.mk-spi{color:#0B8475!important;background:none!important;border-bottom:2px dashed rgba(11,148,132,.8)!important;border-radius:0;padding-bottom:1px}
/* 圣约 · 教会：绿字 + 左侧色条区块 */
mark.mk-cov{color:#2E7D32!important;background:rgba(46,125,50,.10)!important;box-shadow:inset 3px 0 0 #2E7D32!important;padding-left:5px;border-radius:2px 4px 4px 2px}
/* 感恩 · 生活：棕金字 + 黄色马克笔 */
mark.mk-gra{color:#8A4E00!important;background:linear-gradient(104deg,rgba(255,206,64,0) .9%,rgba(255,206,64,.55) 2.4%,rgba(255,206,64,.38) 96%,rgba(255,206,64,0) 99%)!important}
:root[data-theme="dark"] mark.mk-god{color:#C9B5FF!important;background:rgba(183,155,255,.16)!important}
:root[data-theme="dark"] mark.mk-sin{color:#FF8A98!important;box-shadow:inset 0 -2px 0 rgba(255,122,138,.8)!important}
:root[data-theme="dark"] mark.mk-chr{color:#A9C2FF!important;background:linear-gradient(transparent 52%,rgba(126,166,255,.25) 52%)!important}
:root[data-theme="dark"] mark.mk-spi{color:#5FE0CC!important;border-bottom-color:rgba(79,216,196,.8)!important}
:root[data-theme="dark"] mark.mk-cov{color:#9BE0A0!important;background:rgba(143,214,148,.12)!important;box-shadow:inset 3px 0 0 #8FD694!important}
:root[data-theme="dark"] mark.mk-gra{color:#FFD27A!important;background:rgba(255,194,80,.18)!important}
@media (prefers-color-scheme:dark){
 :root:not([data-theme="light"]) mark.mk-god{color:#C9B5FF!important;background:rgba(183,155,255,.16)!important}
 :root:not([data-theme="light"]) mark.mk-sin{color:#FF8A98!important;box-shadow:inset 0 -2px 0 rgba(255,122,138,.8)!important}
 :root:not([data-theme="light"]) mark.mk-chr{color:#A9C2FF!important;background:linear-gradient(transparent 52%,rgba(126,166,255,.25) 52%)!important}
 :root:not([data-theme="light"]) mark.mk-spi{color:#5FE0CC!important;border-bottom-color:rgba(79,216,196,.8)!important}
 :root:not([data-theme="light"]) mark.mk-cov{color:#9BE0A0!important;background:rgba(143,214,148,.12)!important;box-shadow:inset 3px 0 0 #8FD694!important}
 :root:not([data-theme="light"]) mark.mk-gra{color:#FFD27A!important;background:rgba(255,194,80,.18)!important}}
body.nomark mark.mk{font-weight:inherit;padding:0;margin:0}
/* 序数徽章：第一／第二／第三… 变成彩色圆章 */
.ord{display:inline-block;font-family:var(--sans);font-size:.78em;font-weight:800;color:#fff;border-radius:99px;padding:1px 8px;margin:0 3px 0 1px;vertical-align:.08em;
  background:var(--oc,#2457C5);box-shadow:0 2px 6px -2px var(--oc,#2457C5)}
.ord.o1{--oc:#D2283E}.ord.o2{--oc:#2457C5}.ord.o3{--oc:#DB8A0B}.ord.o4{--oc:#0B9484}.ord.o5{--oc:#7048C0}.ord.o6{--oc:#2E7D32}
body.nomark .ord{background:none;color:inherit;box-shadow:none;font-weight:inherit;padding:0;margin:0;font-size:1em}
/* 「不是…而是…」对照句：左灰右亮 */
.vs-no{color:var(--muted)}.vs-no::before{content:'✗';font-family:var(--sans);font-size:.75em;font-weight:800;color:#fff;background:#B7A9A0;border-radius:50%;display:inline-grid;place-items:center;width:1.35em;height:1.35em;margin:0 3px;vertical-align:.1em}
.vs-yes::before{content:'✓';font-family:var(--sans);font-size:.75em;font-weight:800;color:#fff;background:var(--teal);border-radius:50%;display:inline-grid;place-items:center;width:1.35em;height:1.35em;margin:0 4px 0 2px;vertical-align:.1em}
.vs-yes{font-weight:700;color:var(--ink);background:color-mix(in srgb,var(--teal) 13%,transparent);border-radius:4px;padding:0 3px}
body.nomark .vs-no{color:inherit}body.nomark .vs-no::before,body.nomark .vs-yes::before{display:none}body.nomark .vs-yes{background:none;font-weight:inherit}
"""

JS9 = LENIS_JS + r"""
;(function(){var d=document,H=d.documentElement;
/* 0) 进度条：缓存总高，只写 transform */
var tot=1,pt=false;function rec(){tot=Math.max(1,H.scrollHeight-innerHeight);}rec();addEventListener('resize',rec,{passive:true});
setInterval(rec,2500);addEventListener('load',rec);
addEventListener('scroll',function(){if(pt)return;pt=true;requestAnimationFrame(function(){pt=false;var g=d.getElementById('prog');if(g)g.style.transform='scaleX('+(scrollY/tot).toFixed(4)+')';});},{passive:true});
/* 1) 离屏暂停无限动画 */
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){e.target.classList.toggle('live',e.isIntersecting);});},{rootMargin:'120px 0px'});
 d.querySelectorAll('figure,.hero,.act3wrap,.fc-wrap').forEach(function(x){io.observe(x);});}
/* 2) 惯性平滑滚动（桌面滚轮；触屏保持原生） */
var touch=matchMedia('(pointer:coarse)').matches,rm=matchMedia('(prefers-reduced-motion:reduce)').matches;
if(window.Lenis&&!touch&&!rm){
 d.querySelectorAll('.side,.zoverlay,.fc-back,.tw,.fscroll,.rpane,.mklegend').forEach(function(x){x.setAttribute('data-lenis-prevent','');});
 var L=new Lenis({duration:1.05,easing:function(t){return Math.min(1,1.001-Math.pow(2,-10*t));},smoothWheel:true,wheelMultiplier:1,touchMultiplier:1.2});
 window.__lenis=L;function raf(t){L.raf(t);requestAnimationFrame(raf);}requestAnimationFrame(raf);
 new MutationObserver(function(){var o=d.querySelector('.zoverlay');if(o){o.setAttribute('data-lenis-prevent','');L.stop();}else L.start();}).observe(d.body,{childList:true});
}
})();
"""

ORD = re.compile(r'(?<![\w>])(第[一二三四五六])([，、：:])')
ORDMAP = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6}
VSRX = re.compile(r'不是([^，。；：「」<>]{2,24}?)，而是([^，。；：「」<>]{2,26})(?=[，。；：！？」）—]|$)')


def enhance(html):
    """在已标记的 <main> 正文里加入序数徽章与「不是…而是…」对照（只改样式，不改文字）"""
    i0 = html.index('<main'); i1 = html.index('</main>')
    head, body, tail = html[:i0], html[i0:i1], html[i1:]
    toks = re.split(r'(<[^>]+>)', body)
    skip = 0
    out = []
    for tk in toks:
        if tk.startswith('<'):
            m = re.match(r'<(/?)(script|style|svg|h2|h3|button|summary|figcaption|label|textarea|a)\b', tk)
            if m:
                skip += -1 if m.group(1) else 1
                skip = max(skip, 0)
            out.append(tk)
            continue
        if skip or not tk.strip():
            out.append(tk); continue
        tk = ORD.sub(lambda m: '<span class="ord o%d">%s</span>%s' % (ORDMAP[m.group(1)[1]], m.group(1), m.group(2)), tk)
        tk = VSRX.sub(lambda m: '不是<span class="vs-no">%s</span>，而是<span class="vs-yes">%s</span>' % (m.group(1), m.group(2)), tk)
        out.append(tk)
    return head + ''.join(out) + tail


def mark_stats(html, CATS):
    """统计各部分（困苦/拯救/感恩）主日卡片里六类主题词的分布，生成堆叠条形图"""
    parts = [("misery", "🪞 困苦", "主日 2–4"), ("deliver", "✝️ 拯救", "主日 5–31"), ("gratitude", "🙏 感恩", "主日 32–52")]
    secs = re.findall(r'<section class="ld v2 v3 (\w+) rv".*?</section>', html, flags=re.S)
    bodies = re.findall(r'(<section class="ld v2 v3 (\w+) rv".*?</section>)', html, flags=re.S)
    cnt = {k: {c: 0 for c, *_ in CATS} for k, *_ in parts}
    for body, k in bodies:
        if k in cnt:
            for c, *_ in CATS:
                cnt[k][c] += body.count('mk %s"' % c)
    rows = []
    for k, lab, sub in parts:
        tot = sum(cnt[k].values()) or 1
        segs = ''.join('<i class="ms-%s" style="flex-grow:%d" title="%s %d"><span>%s</span></i>'
                       % (c, cnt[k][c], n, cnt[k][c], ('%d%%' % round(cnt[k][c] / tot * 100)) if cnt[k][c] / tot > .09 else '')
                       for c, e, n, ws in CATS if cnt[k][c])
        rows.append('<div class="msrow"><b>%s</b><em>%s</em><div class="msbar">%s</div></div>' % (lab, sub, segs))
    leg = ''.join('<span><i class="ms-%s"></i>%s %s</span>' % (c, e, n.split(' · ')[0]) for c, e, n, ws in CATS)
    return ('<figure class="fig7 msfig"><figcaption>图 · 主题词的重心迁移：同样六类词，在三部分里的比重如何变化（由正文标记自动统计）</figcaption>'
            '%s<div class="msleg">%s</div><p class="fnote7">📈 困苦部分红色（罪 · 律法）最重；进入拯救，蓝色（基督）与青色（圣灵 · 圣礼）接管；到感恩部分，金色（感恩 · 生活）成为最大份额——<b>全书的重心从「我的罪」移向「基督」，再落在「感恩的生活」。</b></p></figure>'
            % (''.join(rows), leg))


CSS9 += r"""
.msrow{display:grid;grid-template-columns:92px 1fr;gap:4px 12px;align-items:center;margin:8px 0}
.msrow b{font-size:16px}.msrow em{grid-column:1;grid-row:2;font-style:normal;font-family:var(--sans);font-size:12px;color:var(--muted)}
.msbar{grid-column:2;grid-row:1/3;display:flex;height:34px;border-radius:10px;overflow:hidden;box-shadow:var(--sh)}
.msbar i{flex-basis:0;display:grid;place-items:center;color:#fff;font-style:normal;font-family:var(--sans);font-size:12px;font-weight:700;min-width:3px;
  transform-origin:left;animation:grow .9s cubic-bezier(.2,.8,.2,1) both}
.ms-mk-god{background:#7048C0}.ms-mk-sin{background:#D2283E}.ms-mk-chr{background:#2457C5}.ms-mk-spi{background:#0B9484}.ms-mk-cov{background:#2E7D32}.ms-mk-gra{background:#DB8A0B}
.msleg{display:flex;flex-wrap:wrap;gap:6px 14px;margin-top:10px;font-family:var(--sans);font-size:13px;color:var(--ink-2)}
.msleg i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:4px;vertical-align:-1px}
@media (max-width:640px){.msrow{grid-template-columns:74px 1fr}.msrow b{font-size:14.5px}}
"""
