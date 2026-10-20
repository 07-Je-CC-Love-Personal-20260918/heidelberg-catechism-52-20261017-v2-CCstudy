# -*- coding: utf-8 -*-
"""v5 导航层：精确锚点跳转（动态顶栏高度 + 二次校正）、移动端抽屉统一、去 content-visibility 抖动"""

CSS5 = r"""
:root{--tbh:56px}
html{scroll-padding-top:calc(var(--tbh) + 14px)}
[id]{scroll-margin-top:calc(var(--tbh) + 14px)}
.ld{content-visibility:visible!important;contain-intrinsic-size:none!important}
@media (max-width:980px){
  .side{top:var(--tbh)!important;height:calc(100dvh - var(--tbh))!important}
  body.nav .scrim{inset:var(--tbh) 0 0!important}
}
.toc a.flash,.flash-t{animation:flash 1.2s ease}
@keyframes flash{0%{box-shadow:0 0 0 0 color-mix(in srgb,var(--brass) 60%,transparent)}100%{box-shadow:0 0 0 14px transparent}}
"""

JS5 = r"""
(function(){var d=document,b=d.body,tb=d.querySelector('.topbar');
function setH(){if(tb)d.documentElement.style.setProperty('--tbh',tb.getBoundingClientRect().height+'px');}
setH();addEventListener('resize',setH,{passive:true});
function H(){return (tb?tb.getBoundingClientRect().height:56)+14;}
function reveal(t){t.classList.add('in');t.querySelectorAll('.rv').forEach(function(x){x.classList.add('in');});
  var p=t.closest('details');while(p){p.open=true;p=p.parentElement&&p.parentElement.closest('details');}}
function go(id,push){var t=d.getElementById(id);if(!t)return false;reveal(t);
  var y=function(){return t.getBoundingClientRect().top+scrollY-H();};
  var Y=y(),dist=Y-scrollY,V=innerHeight;
  if(Math.abs(dist)>V*1.5){scrollTo({top:Y-Math.sign(dist)*V*.5,behavior:'auto'});}
  requestAnimationFrame(function(){scrollTo({top:y(),behavior:'smooth'});});
  var n=0;(function fix(){if(++n>6)return;setTimeout(function(){var dy=t.getBoundingClientRect().top-H();
    if(Math.abs(dy)>4){scrollTo({top:scrollY+dy,behavior:n<3?'smooth':'auto'});fix();}},n<3?420:160);})();
  t.classList.remove('flash-t');void t.offsetWidth;t.classList.add('flash-t');
  if(push!==false)history.replaceState(null,'','#'+id);return true;}
d.addEventListener('click',function(e){var a=e.target.closest('a[href^="#"]');if(!a)return;
  var id=decodeURIComponent(a.getAttribute('href').slice(1));if(!id)return;
  if(go(id)){e.preventDefault();e.stopPropagation();b.classList.remove('nav');b.classList.remove('tocopen');}},true);
/* 抽屉统一：texts 页旧的 tocopen 映射到 nav */
new MutationObserver(function(){if(b.classList.contains('tocopen')){b.classList.remove('tocopen');b.classList.toggle('nav');}})
  .observe(b,{attributes:true,attributeFilter:['class']});
if(location.hash){var id=decodeURIComponent(location.hash.slice(1));setTimeout(function(){go(id,false);},120);}
})();
"""

import os as _os
_V = open(_os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "VERSION")).read().strip()
VERSION = "%s · %s-%s-%s" % (_V.split("-")[1], _V[:4], _V[4:6], _V[6:8])

CSS5 += r"""
.sec{padding:26px 0 4px;margin-top:18px}
.hero{padding:36px 0 22px}
.ld.v2{margin:16px 0}
.part-div{margin:30px 0 4px;padding:14px 0 8px}
.blkgrid,.bento{gap:12px;margin:12px 0}
.vstamp{display:block;margin-top:14px;font-family:var(--sans);font-size:11px;letter-spacing:.12em;color:var(--muted);opacity:.7}
/* heatmap */
.hm{display:grid;grid-template-columns:repeat(auto-fill,minmax(64px,1fr));gap:6px}
.hm a{--a:0;position:relative;display:grid;place-items:center;aspect-ratio:1.25;border-radius:10px;text-decoration:none;
  font-family:var(--sans);font-size:13px;font-weight:600;color:var(--ink);
  background:color-mix(in srgb,var(--c) calc(var(--a)*100%),var(--paper-3));transition:transform .2s,box-shadow .2s}
.hm a b{font-size:15px;color:inherit}.hm a.hot i{opacity:.9}.hm.cod a{aspect-ratio:auto;height:68px}.hm a i{font-style:normal;font-size:10.5px;opacity:.75;font-weight:400}
.hm a.hot{color:#fff}
.hm a:hover{transform:translateY(-3px) scale(1.06);box-shadow:var(--sh2);z-index:2}
.hm a .tip{position:absolute;bottom:calc(100% + 6px);left:50%;transform:translateX(-50%);white-space:nowrap;padding:5px 9px;border-radius:8px;
  background:var(--ink);color:var(--paper);font-size:12px;font-weight:400;opacity:0;pointer-events:none;transition:opacity .15s}
.hm a .tip{display:none}.hm a:hover .tip{display:block;opacity:1}@media (max-width:640px){.hm a .tip{display:none!important}}
.hmleg{display:flex;align-items:center;gap:8px;margin:10px 0 0;font-family:var(--sans);font-size:12.5px;color:var(--muted)}
.hmleg span{width:120px;height:10px;border-radius:9px;background:linear-gradient(90deg,var(--paper-3),var(--c))}
.hmh{font-family:var(--sans);font-size:13.5px;font-weight:700;margin:14px 0 8px;color:var(--c)}
"""


def heatmap(LDS, E):
    import re
    from cci_text import BC, COD
    bc, cod = {}, {}
    rom = {"I": 1, "II": 2, "III": 3, "IV": 3, "III/IV": 3, "V": 4}
    for d in LDS:
        for m in re.finditer(r'BC\s?(\d{1,2})(?:[–-](\d{1,2}))?', d["confess"]):
            a, z = int(m.group(1)), int(m.group(2) or m.group(1))
            for k in range(a, min(z, 37) + 1):
                bc.setdefault(k, []).append(d["n"])
        for m in re.finditer(r'CoD\s?(III/IV|I{1,3}|IV|V)', d["confess"]):
            cod.setdefault(rom[m.group(1)], []).append(d["n"])
    mx = max(len(v) for v in bc.values()) if bc else 1

    def cell(href, lab, sub, lds, m):
        a = len(lds) / m if m else 0
        tip = ("主日 " + "、".join(map(str, sorted(set(lds))))) if lds else "未直接引用"
        return ('<a href="%s" class="%s" style="--a:%.2f"><span><b>%s</b><br><i>%s</i></span><span class="tip">%s</span></a>'
                % (href, "hot" if a > .55 else "", .12 + .88 * a if lds else 0, lab, sub, tip))
    short = lambda t: re.sub(r'^第.+?条\s*(论)?', '', t).replace('“','').replace('”','')[:4]
    h1 = ''.join(cell("texts.html#bc%d" % a["no"], a["no"], E(short(a["title"])), bc.get(a["no"], []), mx) for a in BC)
    mc = max(len(v) for v in cod.values()) if cod else 1
    h2 = ''.join(cell("texts.html#cod%d" % (j + 1), ["一", "二", "三四", "五"][j], "项教义", cod.get(j + 1, []), mc)
                 for j in range(len(COD)))
    return ('<figure class="fig"><figcaption>图 · 信条互参热力图：52 主日的「信条互参」引用了比利时信条哪几条、多特信经哪几项（颜色越深引用越多；悬停看主日，点按读原文）</figcaption>'
            '<div class="hmh" style="--c:var(--deliver)">比利时信条 · 37 条</div><div class="hm" style="--c:var(--deliver)">%s</div>'
            '<div class="hmh" style="--c:var(--misery)">多特信经 · 四项教义</div><div class="hm cod" style="--c:var(--misery);grid-template-columns:repeat(4,1fr)">%s</div>'
            '<div class="hmleg" style="--c:var(--deliver)">少<span></span>多</div></figure>') % (h1, h2)
