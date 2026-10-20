# -*- coding: utf-8 -*-
"""v7：问题图表重绘（无重叠、手机完整显示）+ 图表全屏查看 + 动画"""
import math
import charts as C

PARTC = {"总纲": "prologue", "困苦": "misery", "拯救": "deliver", "感恩": "gratitude"}


def fig(cap, body, note=""):
    """手机端等比缩放完整显示；可点「放大」全屏横向查看"""
    return ('<figure class="fig7"><figcaption>%s</figcaption><div class="zbox">%s'
            '<button class="zbtn" type="button" aria-label="全屏查看">⤢ 放大</button></div>%s</figure>'
            % (cap, body, '<p class="fnote7">%s</p>' % note if note else ''))


# ── 1. 三重结构比例（HTML，永远完整） ──
def triring():
    segs = [("misery", "🪞", "困苦", "MISERIA", 9, "主日 2–4", "问 3–11"),
            ("deliver", "✝️", "拯救", "LIBERATIO", 74, "主日 5–31", "问 12–85"),
            ("gratitude", "🙏", "感恩", "GRATITUDO", 44, "主日 32–52", "问 86–129")]
    bar = ''.join('<div class="tr-seg %s" style="--w:0;flex-grow:%d;--i:%d"><span>%d%%</span></div>'
                  % (k, n, i, round(n / 129 * 100)) for i, (k, e, t, la, n, ld, q) in enumerate(segs))
    cards = ''.join('<div class="tr-card %s" style="--i:%d"><em>%s</em><b>%s</b><i>%s</i><p>%d 问 · %s · %s</p></div>'
                    % (k, i, e, t, la, n, ld, q) for i, (k, e, t, la, n, ld, q) in enumerate(segs))
    return ('<figure class="fig7"><figcaption>图 · 三重结构与篇幅比例：律法定罪仅占 7%%，福音与感恩占 93%%</figcaption>'
            '<div class="tr-quote"><span>罗 7:24</span>「我真是苦啊！谁能救我脱离这取死的身体呢？」'
            '<b>→</b><span>罗 7:25</span>「感谢神，靠着我们的主耶稣基督就能脱离了。」</div>'
            '<div class="tr-bar">%s</div><div class="tr-cards">%s</div>'
            '<p class="fnote7">⚖️ 十诫在首（问 3–5）作<b>定罪之镜</b>，在尾（问 92–115）作<b>感恩之规</b>——同一部律法，位置决定性质。</p></figure>'
            % (bar, cards))


# ── 2. 降卑与升高（SVG 重排 + 手机竖排阶梯） ──
PARA = C.PARA


def parabola():
    W, H = 960, 380
    L, R = 150, 920
    n = len(PARA)
    pts = []
    for i, (name, ld, depth) in enumerate(PARA):
        x = L + i * (R - L) / (n - 1)
        y = 80 + depth * 210
        pts.append((x, y, name, ld, depth))
    d = "M%.0f %.0f " % pts[0][:2]
    for a, b in zip(pts, pts[1:]):
        mx = (a[0] + b[0]) / 2
        d += "C%.0f %.0f %.0f %.0f %.0f %.0f " % (mx, a[1], mx, b[1], b[0], b[1])
    o = ['<svg viewBox="0 34 %d %d" class="svg7 para7" role="img" aria-label="基督降卑与升高曲线">' % (W, H - 34),
         '<defs><linearGradient id="pg" x1="0" x2="1"><stop offset="0" stop-color="var(--misery)"/>'
         '<stop offset=".55" stop-color="var(--deliver)"/><stop offset="1" stop-color="var(--gratitude)"/></linearGradient></defs>',
         '<rect x="0" y="40" width="%d" height="60" class="band up"/>' % W,
         '<rect x="0" y="270" width="%d" height="60" class="band dn"/>' % W,
         '<text class="ax7" x="16" y="76">⬆ 升高</text><text class="ax7 s" x="16" y="94">exaltatio</text>',
         '<text class="ax7" x="16" y="306">⬇ 降卑</text><text class="ax7 s" x="16" y="324">humiliatio</text>',
         '<path class="pline" d="%s"/>' % d]
    # 主日分段刻度
    seen = {}
    for x, y, name, ld, dp in pts:
        seen.setdefault(ld, []).append(x)
    for ld, xs in seen.items():
        a, b = min(xs) - 26, max(xs) + 26
        o.append('<rect class="ldband" x="%.0f" y="346" width="%.0f" height="24" rx="12"/>' % (a, b - a))
        o.append('<text class="ldl" x="%.0f" y="363" text-anchor="middle">主日 %d</text>' % ((a + b) / 2, ld))
    for i, (x, y, name, ld, dp) in enumerate(pts):
        ty = y + 32 if dp >= .5 else y - 18
        o.append('<circle class="pn" cx="%.0f" cy="%.0f" r="7" style="--i:%d"/>' % (x, y, i))
        o.append('<text class="pl" x="%.0f" y="%.0f" text-anchor="middle" style="--i:%d">%s</text>' % (x, ty, i, name))
    o.append('</svg>')
    steps = ''.join('<li style="--d:%.2f;--i:%d"><b>%s</b><span>主日 %d</span></li>'
                    % (dp, i, name, ld) for i, (name, ld, dp) in enumerate(PARA))
    return ('<figure class="fig7"><figcaption>图 · 降卑与升高：信经的基督论段落在海德堡中的曲线（主日 14–19）</figcaption>'
            '<div class="zbox para-svg">%s<button class="zbtn" type="button">⤢ 放大</button></div>'
            '<ol class="para-steps">%s</ol>'
            '<p class="fnote7">📉 从道成肉身一路下降到「地狱之苦」（问 44：十架上灵魂的极度痛苦），再从复活一路升到再来审判——腓 2:6–11 的形状。</p></figure>'
            % (''.join(o), steps))


# ── 3. 问答密度（长句移出 SVG） ──
def qa_bars(LDS):
    W, H = 900, 230
    bw = (W - 80) / 52
    mx = max(len(d["qas"]) for d in LDS)
    o = ['<svg viewBox="0 0 %d %d" class="svg7" role="img" aria-label="每主日问答数量分布">' % (W, H)]
    for k in range(1, mx + 1):
        y = 200 - k * (160 / mx)
        o.append('<line class="grat" x1="46" y1="%.0f" x2="880" y2="%.0f"/>' % (y, y))
        o.append('<text class="g7" x="34" y="%.0f" text-anchor="end">%d</text>' % (y + 5, k))
    for i, d in enumerate(LDS):
        c = len(d["qas"]); h = c * (160 / mx); x = 50 + i * bw
        o.append('<rect class="qb7 %s" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" style="--i:%d">'
                 '<title>主日 %d · %s · %d 问</title></rect>' % (PARTC[d["part"]], x, 200 - h, bw - 3, h, i, d["n"], d["title"], c))
        if d["n"] % 5 == 0 or d["n"] == 1:
            o.append('<text class="g7" x="%.1f" y="222" text-anchor="middle">%d</text>' % (x + bw / 2 - 1, d["n"]))
    o.append('</svg>')
    return fig("图 · 52 主日的问答密度分布：哪几处海德堡说得最多", ''.join(o),
               "📊 唯一的五问峰值在<b>主日 16</b>（死、埋葬、降在阴间）；四问的八处集中在中保、信心、升天、圣礼、悔改、第一诫与祷告——"
               "<b>海德堡说得最多的地方，正是历史上争得最凶的地方。</b>")


# ── 4. 欧洲地图（编号标注 + 图例，零重叠） ──
LABEL_OFF = {"Basel": (-12, 18, "end"), "Strasbourg": (-12, -4, "end"), "Zürich": (12, 16, "start"),
             "Genève": (-12, 4, "end"), "Heidelberg": (14, -4, "start"), "Emden": (12, -4, "start"),
             "Dordrecht": (-12, -8, "end"), "Antwerpen": (-12, 14, "end"), "Westminster": (-12, 4, "end"),
             "Edinburgh": (12, 4, "start"), "Wittenberg": (12, 4, "start"), "Debrecen": (-12, -10, "end"),
             "Trento": (12, 4, "start"), "Roma": (12, 4, "start")}


def map_europe():
    P, CITIES, FLOWS = C.P, C.CITIES, C.FLOWS
    idx = {c[1]: c for c in CITIES}
    o = ['<svg viewBox="0 0 900 585" class="svg7 map7" role="img" aria-label="十六世纪改革宗欧洲影响流向示意图">']
    for lon in range(-5, 25, 5):
        x = P(50, lon)[0]
        o.append('<line x1="%.0f" y1="20" x2="%.0f" y2="560" class="grat"/><text x="%.0f" y="576" class="g7" text-anchor="middle">%d°E</text>' % (x, x, x, lon))
    for lat in range(42, 58, 3):
        y = P(lat, 0)[1]
        o.append('<line x1="24" y1="%.0f" x2="876" y2="%.0f" class="grat"/><text x="4" y="%.0f" class="g7">%d°N</text>' % (y, y, y + 4, lat))
    regions = [("神圣罗马帝国", 50.6, 11.5, 300, 190, "t"), ("低地", 51.9, 5.0, 120, 76, "b"), ("瑞士", 46.9, 8.0, 118, 58, "b"),
               ("不列颠", 53.6, -2.2, 132, 130, "t"), ("法兰西", 47.2, 2.2, 150, 150, "c"), ("匈牙利", 47.4, 20.5, 118, 62, "b"),
               ("意大利", 44.0, 11.8, 108, 150, "c")]
    for name, la, lo, w, hh, pos in regions:
        x, y = P(la, lo)
        o.append('<rect class="region" x="%.0f" y="%.0f" width="%d" height="%d" rx="28"/>' % (x - w / 2, y - hh / 2, w, hh))
        ty = {"t": y - hh / 2 + 18, "b": y + hh / 2 - 8, "c": y + 4}[pos]
        tx = x + (70 if name == "神圣罗马帝国" else 0)
        o.append('<text class="rg7" x="%.0f" y="%.0f" text-anchor="middle">%s</text>' % (tx, ty, name))
    for a, b, lab, side in FLOWS:
        (x1, y1), (x2, y2) = P(idx[a][2], idx[a][3]), P(idx[b][2], idx[b][3])
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        cx, cy = mx - dy / L * 46 * side, my + dx / L * 46 * side
        o.append('<path class="flow7" d="M%.0f %.0f Q%.0f %.0f %.0f %.0f"/>' % (x1, y1, cx, cy, x2, y2))
    leg = []
    for i, (zh, en, la, lo, note, tag) in enumerate(CITIES):
        x, y = P(la, lo)
        r = 9 if tag == "hd" else 7
        if tag == "hd":
            o.append('<circle class="pulse" cx="%.0f" cy="%.0f" r="9"/>' % (x, y))
        o.append('<circle class="cn7%s" cx="%.0f" cy="%.0f" r="%d"/>' % (" key" if tag == "hd" else "", x, y, r))
        o.append('<text class="cnum" x="%.0f" y="%.0f" text-anchor="middle">%d</text>' % (x, y + 3.5, i + 1))
        dx, dy, anc = LABEL_OFF.get(en, (12, 4, "start"))
        o.append('<text class="cl7%s" x="%.0f" y="%.0f" text-anchor="%s">%s</text>' % (" key" if tag == "hd" else "", x + dx, y + dy, anc, zh))
        leg.append('<li%s><b>%d</b><span>%s</span><em>%s</em></li>' % (' class="key"' if tag == "hd" else '', i + 1, zh, note))
    o.append('</svg>')
    flows = ''.join('<li>%s</li>' % lab for a, b, lab, s in FLOWS)
    return ('<figure class="fig7"><figcaption>图 · 改革宗欧洲：海德堡在影响网络中的位置（按真实经纬度定位；虚线为人物与文献流向）</figcaption>'
            '<div class="zbox">%s<button class="zbtn" type="button">⤢ 放大</button></div>'
            '<div class="mapleg"><ol class="mlc">%s</ol><div class="mlf"><b>➰ 流向</b><ul>%s</ul></div></div></figure>'
            % (''.join(o), ''.join(leg), flows))


def patch(Cm, C2m):
    Cm.triring, Cm.parabola, Cm.map_europe = triring, parabola, map_europe
    C2m.qa_bars = qa_bars
    _old = Cm.fig

    def fig2(cap, body, cls=""):
        if "<svg " in body:
            return ('<figure class="%s"><figcaption>%s</figcaption><div class="zbox">%s'
                    '<button class="zbtn" type="button">⤢ 放大</button></div></figure>' % (cls, cap, body))
        return _old(cap, body, cls)
    Cm.fig = fig2
    C2m.fig = fig2


CSS7 = r"""
/* ===== v7：图表完整显示 · 全屏查看 · 动画 ===== */
.fscroll>svg{min-width:0!important}
.zbox{position:relative}
.zbox>svg{width:100%;height:auto;display:block}
.zbtn{position:absolute;right:6px;top:6px;font-family:var(--sans);font-size:12px;padding:4px 10px;border-radius:99px;border:1px solid var(--rule);
  background:var(--glass);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);color:var(--ink-2);cursor:pointer;opacity:.85;z-index:2}
.zbtn:hover{opacity:1;color:var(--royal)}
@media (min-width:1100px){.zbtn{opacity:0;transition:opacity .2s}.zbox:hover .zbtn{opacity:.9}}
.zoverlay{position:fixed;inset:0;z-index:200;background:color-mix(in srgb,var(--paper) 97%,transparent);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
  display:flex;flex-direction:column;animation:fadein .25s ease}
@keyframes fadein{from{opacity:0}}
.zoverlay .zhead{display:flex;align-items:center;gap:10px;padding:10px 14px;border-bottom:1px solid var(--rule);font-family:var(--sans);font-size:14px}
.zoverlay .zhead span{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--ink-2)}
.zoverlay .zbody{flex:1;overflow:auto;-webkit-overflow-scrolling:touch;padding:14px}
.zoverlay .zbody>svg{width:max(100%,980px);height:auto;display:block}
.zoverlay .zhint{font-family:var(--sans);font-size:12px;color:var(--muted);padding:6px 14px 12px;text-align:center}
.fnote7{margin:10px 0 0;font-size:.95em;line-height:1.8;color:var(--ink-2);background:color-mix(in srgb,var(--brass) 9%,transparent);border-radius:10px;padding:8px 12px}
/* triring */
.tr-quote{font-size:.95em;line-height:1.8;color:var(--ink-2);margin:4px 0 12px}
.tr-quote span{display:inline-block;font-family:var(--sans);font-size:12px;font-weight:700;color:#fff;background:var(--misery);border-radius:6px;padding:0 7px;margin:0 4px}
.tr-quote span:nth-of-type(2){background:var(--gratitude)}
.tr-quote b{color:var(--brass);margin:0 6px}
.tr-bar{display:flex;height:46px;border-radius:12px;overflow:hidden;box-shadow:var(--sh)}
.tr-seg{flex-basis:0;flex-shrink:1;display:grid;place-items:center;color:#fff;font-family:var(--sans);font-weight:700;font-size:14px;min-width:40px;
  transform-origin:left;animation:grow .9s cubic-bezier(.2,.8,.2,1) both;animation-delay:calc(var(--i)*.18s)}
.tr-seg.misery{background:var(--misery)}.tr-seg.deliver{background:var(--deliver)}.tr-seg.gratitude{background:var(--gratitude)}
@keyframes grow{from{transform:scaleX(0)}}
.tr-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:10px}
.tr-card{--c:var(--deliver);border-radius:14px;padding:12px 14px;border-top:4px solid var(--c);background:color-mix(in srgb,var(--c) 9%,var(--paper));
  display:grid;grid-template-columns:auto 1fr;gap:0 10px;align-items:center;animation:rise .6s both;animation-delay:calc(.3s + var(--i)*.15s)}
.tr-card.misery{--c:var(--misery)}.tr-card.gratitude{--c:var(--gratitude)}
.tr-card em{grid-row:span 2;font-style:normal;font-size:30px}
.tr-card b{font-family:var(--disp);font-size:22px;color:var(--c)}
.tr-card i{font-style:normal;font-family:var(--sans);font-size:11.5px;letter-spacing:.12em;color:var(--muted)}
.tr-card p{grid-column:1/-1;margin:6px 0 0;font-family:var(--sans);font-size:13.5px;color:var(--ink-2)}
@media (max-width:640px){.tr-cards{grid-template-columns:1fr}}
/* parabola */
.svg7 .band.up{fill:color-mix(in srgb,var(--gratitude) 9%,transparent)}.svg7 .band.dn{fill:color-mix(in srgb,var(--misery) 8%,transparent)}
.ax7{font-family:var(--sans);font-size:17px;font-weight:700;fill:var(--ink-2)}.ax7.s{font-size:12px;font-weight:400;fill:var(--muted)}
.pline{fill:none;stroke:url(#pg);stroke-width:5;stroke-linecap:round;stroke-dasharray:2000;stroke-dashoffset:2000}
.in .pline,.fig7 .pline{animation:draw 2.4s .2s ease forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.pn{fill:var(--paper);stroke:var(--royal);stroke-width:3;animation:pop .5s both;animation-delay:calc(.3s + var(--i)*.18s);transform-box:fill-box;transform-origin:center}
.pl{font-family:var(--serif);font-size:17px;font-weight:700;fill:var(--ink);animation:fadein .5s both;animation-delay:calc(.4s + var(--i)*.18s)}
.ldband{fill:color-mix(in srgb,var(--deliver) 14%,transparent)}
.ldl{font-family:var(--sans);font-size:13px;font-weight:600;fill:var(--deliver)}
.para-steps{display:none;list-style:none;margin:0;padding:0}
@media (max-width:640px){
  .para-svg{display:none}
  .para-steps{display:grid;gap:6px}
  .para-steps li{display:flex;justify-content:space-between;align-items:center;gap:8px;border-radius:10px;padding:8px 12px;
    margin-left:calc(var(--d)*38%);background:linear-gradient(90deg,color-mix(in srgb,var(--deliver) calc(20% + var(--d)*30%),var(--paper)),var(--paper));
    border-left:4px solid color-mix(in srgb,var(--misery) calc(var(--d)*100%),var(--gratitude));animation:rise .5s both;animation-delay:calc(var(--i)*.08s)}
  .para-steps b{font-size:15.5px}.para-steps span{font-family:var(--sans);font-size:12px;color:var(--muted);white-space:nowrap}
}
/* qa bars */
.g7{font-family:var(--sans);font-size:13px;fill:var(--muted)}
.qb7{transform-box:fill-box;transform-origin:bottom;animation:grow-y .7s both;animation-delay:calc(var(--i)*.02s)}
.qb7.prologue{fill:var(--prologue)}.qb7.misery{fill:var(--misery)}.qb7.deliver{fill:var(--deliver)}.qb7.gratitude{fill:var(--gratitude)}
@keyframes grow-y{from{transform:scaleY(0)}}
/* map */
.flow7{fill:none;stroke:var(--brass);stroke-width:2;stroke-dasharray:8 6;animation:flowmv 1.6s linear infinite}
@keyframes flowmv{to{stroke-dashoffset:-28}}
.cn7{fill:var(--deliver)}.cn7.key{fill:var(--misery)}
.cnum{font-family:var(--sans);font-size:10px;font-weight:700;fill:#fff;pointer-events:none}
.cl7{font-family:var(--serif);font-size:15px;font-weight:700;fill:var(--ink);paint-order:stroke;stroke:var(--paper);stroke-width:4px}
.cl7.key{fill:var(--misery);font-size:18px}
.rg7{font-family:var(--sans);font-size:12px;letter-spacing:.2em;fill:var(--muted)}
.mapleg{display:grid;grid-template-columns:2fr 1fr;gap:12px;margin-top:10px}
.mapleg ol.mlc{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:6px}
.mapleg ol.mlc>li{display:grid;grid-template-columns:24px auto 1fr;gap:6px;align-items:baseline;font-size:14px;padding:4px 8px;border-radius:8px;background:var(--paper-3)}
.mapleg ol.mlc>li b{display:grid;place-items:center;width:20px;height:20px;border-radius:50%;background:var(--deliver);color:#fff;font-family:var(--sans);font-size:11px}
.mapleg ol.mlc>li.key{background:color-mix(in srgb,var(--misery) 14%,transparent)}.mapleg ol.mlc>li.key b{background:var(--misery)}
.mapleg ol.mlc>li em{font-style:normal;font-family:var(--sans);font-size:12px;color:var(--muted)}
.mapleg .mlf{background:color-mix(in srgb,var(--brass) 10%,transparent);border-radius:10px;padding:8px 12px;font-size:14px}
.mapleg .mlf ul{display:block;margin:4px 0 0;padding-left:1.1em;line-height:1.8}
@media (max-width:860px){.mapleg{grid-template-columns:1fr}}
"""

JS7 = r"""
(function(){var d=document;
d.addEventListener('click',function(e){var b=e.target.closest('.zbtn');if(!b)return;
 var box=b.closest('.zbox'),svg=box.querySelector('svg');if(!svg)return;var f=box.closest('figure'),cap=f&&f.querySelector('figcaption');
 var o=d.createElement('div');o.className='zoverlay';o.innerHTML='<div class="zhead"><span></span><button class="btn">✕ 关闭</button></div><div class="zbody"></div><div class="zhint">左右滑动查看 · 可双指缩放 · 横屏更佳</div>';
 o.querySelector('span').textContent=cap?cap.textContent:'';o.querySelector('.zbody').appendChild(svg.cloneNode(true));
 function close(){o.remove();d.removeEventListener('keydown',k);d.body.style.overflow='';}
 function k(ev){if(ev.key==='Escape')close();}
 o.querySelector('.btn').onclick=close;o.addEventListener('click',function(ev){if(ev.target===o)close();});d.addEventListener('keydown',k);
 d.body.style.overflow='hidden';d.body.appendChild(o);});
})();
"""

CSS7 += ".mapleg ol.mlc{align-items:start;grid-auto-rows:auto}.mapleg ol.mlc>li{height:auto;min-height:0}.mapleg .mlf li{display:list-item;height:auto;width:auto;background:none;padding:0}"
CSS7 += ".mw{padding-right:40px}"
CSS7 += "@media (max-width:860px){.ld.v3 .ld-h{padding-bottom:44px!important}.ld.v3 .chk{top:auto!important;bottom:12px;right:14px}.ld.v3 .ld-ht h3{padding-right:0!important}}"

SEC_EMO = {"intro-why": "🏰", "intro-frame": "🧭", "intro-canon": "📜", "bt-canon": "📖", "bt-cov": "🤝",
           "intro-compare": "🏛️", "creed-reader": "🎙️", "forms-cmp": "⚖️", "intro-method": "🔍", "intro-map": "🗺️",
           "intro-text": "🖋️", "compass": "🧠", "flash": "🃏", "closure": "♾️",
           "ap-munus": "👑", "ap-ordo": "⛓️", "ap-sac": "🍞", "ap-dec": "📋", "ap-lp": "🙏", "ap-keys": "🗝️",
           "ap-opp": "🛡️", "ap-lex": "🔤", "ap-index": "🗂️", "ap-pair": "🔗", "ap-memo": "💡", "ap-quiz": "✅"}


def add_icons(html):
    import re
    for k, e in SEC_EMO.items():
        html = html.replace('<a href="#%s"><span class="no">' % k, '<a href="#%s"><span class="emo">%s</span><span class="no">' % (k, e), 1)
        html = re.sub(r'(<section class="sec[^"]*" id="%s">.*?<h2>)' % re.escape(k), lambda m: m.group(1) + '<span class="h2e">%s</span>' % e, html, count=1, flags=re.S)
    return html

CSS7 += ".h2e{font-size:.85em;margin-right:2px;display:inline-block;animation:bob 4s ease-in-out infinite}.sec h2:has(.h2e)::before{display:none}"
CSS7 += ".toc a{display:flex;align-items:baseline;gap:5px}.toc a .emo{flex:none;width:1.3em;text-align:center;margin:0}.toc a .no{flex:none;min-width:2.4em!important;margin:0}"
