# -*- coding: utf-8 -*-
"""v11：历史·地图·文化页（真实地图＋示意图，瓦片多源自动切换）· 多主题 · 目录可拖宽 · 角落导航 · 去打印"""
import json, html as _h

E = lambda s: _h.escape(str(s), quote=False)

# ───────── 时间线事件（带真实坐标） ─────────
EVENTS = [
 (1517, "维滕堡", 51.866, 12.646, "路德张贴《九十五条论纲》", "宗教改革开端：因信称义重新被宣讲。", "misery"),
 (1529, "马尔堡", 50.810, 8.771, "马尔堡会谈", "路德与慈运理在十五条中同意十四条，唯独圣餐破裂——海德堡第 75–80 问的远因。", "misery"),
 (1530, "奥格斯堡", 48.371, 10.898, "《奥格斯堡信条》", "路德宗的标准告白；日后帝国只承认它与罗马天主教。", "misery"),
 (1536, "巴塞尔", 47.559, 7.588, "加尔文《基督教要义》初版", "改革宗神学的系统化起点。", "deliver"),
 (1549, "苏黎世", 47.377, 8.540, "《苏黎世共识》", "加尔文与布灵格在圣餐上达成一致：真实而属灵的临在。", "deliver"),
 (1555, "奥格斯堡", 48.371, 10.898, "奥格斯堡和约", "「教随国定」：改革宗不在受保护之列，海德堡的处境由此紧张。", "misery"),
 (1559, "海德堡", 49.410, 8.694, "腓特烈三世继任选侯", "普法尔茨选侯国转向改革宗。", "gratitude"),
 (1560, "海德堡", 49.410, 8.694, "海德堡圣餐之争", "赫斯胡斯与克莱布茨在祭坛前争夺圣杯；选侯决心编一部统一的要理。", "misery"),
 (1561, "图尔奈", 50.606, 3.389, "《比利时信条》", "德·布雷投书城堡墙内，向西班牙王证明改革宗信徒不是叛民。", "deliver"),
 (1563, "海德堡", 49.410, 8.694, "《海德堡要理问答》出版", "乌尔西努与俄利维亚努主笔；同年三版，第三版加入第 80 问全文。", "gratitude"),
 (1566, "奥格斯堡", 48.371, 10.898, "帝国议会上的辩护", "腓特烈三世以圣经为本为要理辩护，未被定罪。", "gratitude"),
 (1568, "韦瑟尔", 51.663, 6.617, "韦瑟尔会议", "流亡中的低地改革宗规划教会秩序，采用海德堡要理。", "deliver"),
 (1571, "埃姆登", 53.367, 7.206, "埃姆登总会", "低地改革宗的「母会」：长老会议体制成形。", "deliver"),
 (1618, "多特勒支", 51.813, 4.673, "多特总会（1618–19）", "审订海德堡与比利时信条，制定多特信经——合一三信条完成。", "gratitude"),
]

WORLD = [
 ("海德堡", 49.41, 8.69, "1563 诞生", "gratitude"),
 ("多特勒支 · 荷兰", 51.81, 4.67, "1619 定为合一三信条之一", "deliver"),
 ("德布勒森 · 匈牙利", 47.53, 21.63, "匈牙利改革宗沿用至今", "deliver"),
 ("纽约（新阿姆斯特丹）", 40.71, -74.01, "1628 荷兰改革宗会众", "misery"),
 ("开普敦 · 南非", -33.92, 18.42, "荷兰东印度公司时代传入", "misery"),
 ("雅加达（巴达维亚）", -6.21, 106.85, "荷兰东印度公司时代传入", "misery"),
 ("大急流城 · 美国", 42.96, -85.67, "基督教改革宗教会（CRC）", "prologue"),
 ("安大略 · 加拿大", 43.33, -79.80, "加拿大改革宗教会（CanRC）、URCNA", "prologue"),
 ("首尔 · 韩国", 37.57, 126.98, "改革宗神学院与教会使用", "prologue"),
 ("香港 · 华语教会", 22.32, 114.17, "中文译本：华人改革宗教会教导", "prologue"),
]

CULTURE = {
 "head": ["", "🏰 普法尔茨（海德堡）", "📜 萨克森（维滕堡）", "⛰️ 日内瓦", "🌷 低地（荷兰）"],
 "rows": [
  ["政体", "选侯国：帝国七选侯之一", "选侯国／公国", "城市共和国", "西班牙治下诸省 → 联省共和国"],
  ["教会体制", "选侯颁行《教会规程》（1563）", "领主监管的路德宗教会", "长老与牧师共治（宗教法庭）", "长老会议制（埃姆登 1571）"],
  ["标志文献", "海德堡要理问答", "奥格斯堡信条、路德大小要理", "要义、日内瓦要理", "比利时信条、多特信经"],
  ["敬拜特色", "去除圣像与祭坛，用桌领圣餐", "保留祭坛、圣像与部分礼仪", "朴素敬拜、唱诗篇", "达特努斯诗篇、下午要理讲道"],
  ["圣餐观", "真实而属灵的临在", "基督身体「在、与、下」饼杯", "真实而属灵的临在", "同海德堡"],
  ["处境压力", "帝国法不承认改革宗", "相对安全", "四邻天主教势力", "西班牙宗教裁判与战争"],
 ]}

# ───────── 示意图：莱茵走廊 ─────────
RHINE = [("巴塞尔", 520, "印刷中心"), ("斯特拉斯堡", 455, "布塞珥"), ("施派尔", 380, "帝国议会"),
         ("海德堡", 330, "1563 要理"), ("美因茨", 270, "选侯·大主教"), ("科隆", 190, "天主教重镇"),
         ("韦瑟尔", 130, "1568 会议"), ("埃姆登", 50, "1571 总会")]


def rhine_svg():
    pts = []
    o = ['<svg viewBox="0 0 520 580" class="svg7 rhine" role="img" aria-label="莱茵河走廊示意图">',
         '<defs><linearGradient id="rv" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#5FA8D3"/><stop offset="1" stop-color="#2457C5"/></linearGradient></defs>',
         '<path class="river" d="M250 560 C230 500 290 470 260 420 C230 370 300 350 270 300 C240 250 300 220 270 170 C245 120 290 90 260 30" stroke="url(#rv)"/>',
         '<path class="river small" d="M270 330 C320 320 370 335 430 320"/><text class="rl7" x="440" y="318">内卡河</text>',
         '<text class="rl7 big" x="300" y="560">莱茵河 · 自南向北</text>',
         '<path class="idea" d="M250 560 C230 500 290 470 260 420 C230 370 300 350 270 300 C240 250 300 220 270 170 C245 120 290 90 260 30"/>']
    for i, (n, y, note) in enumerate(RHINE):
        x = 268 + (10 if i % 2 else -6)
        left = i % 2 == 0
        key = n == "海德堡"
        o.append('<g class="rc%s" style="--i:%d"><circle cx="%d" cy="%d" r="%d"/>' % (" key" if key else "", i, x, y, 10 if key else 7))
        if left:
            o.append('<text class="rn" x="%d" y="%d" text-anchor="end">%s</text><text class="rs" x="%d" y="%d" text-anchor="end">%s</text></g>' % (x - 16, y - 2, n, x - 16, y + 16, note))
        else:
            o.append('<text class="rn" x="%d" y="%d">%s</text><text class="rs" x="%d" y="%d">%s</text></g>' % (x + 16, y - 2, n, x + 16, y + 16, note))
    o.append('<text class="rl7" x="16" y="34">⬆ 北海 · 低地</text><text class="rl7" x="16" y="560">⬇ 瑞士 · 日内瓦方向</text></svg>')
    return ''.join(o)


def history_sections():
    tl = ''.join('<button class="tl11 %s" data-i="%d" type="button"><b>%d</b><span>%s</span><em>📍 %s</em><p>%s</p></button>'
                 % (c, i, y, E(t), E(p), E(x)) for i, (y, p, la, lo, t, x, c) in enumerate(EVENTS))
    ev = [{"y": y, "p": p, "la": la, "lo": lo, "t": t, "x": x, "c": c} for (y, p, la, lo, t, x, c) in EVENTS]
    wd = [{"p": p, "la": la, "lo": lo, "t": t, "c": c} for (p, la, lo, t, c) in WORLD]
    th = ''.join('<th>%s</th>' % E(x) for x in CULTURE["head"])
    tr = ''.join('<tr>%s</tr>' % ''.join(('<th>%s</th>' if j == 0 else '<td>%s</td>') % E(c) for j, c in enumerate(r)) for r in CULTURE["rows"])
    return (
     '<section class="sec histsec" id="hist-intro"><div class="eyebrow">HISTORIA · GEOGRAPHIA · CULTURA</div>'
     '<h2>历史 · 地图 · 文化：一部要理问答诞生的现场</h2>'
     '<p class="lead">《海德堡要理问答》生在莱茵—内卡河交汇的大学城，夹在路德宗诸邦、天主教主教领与帝国法庭之间。'
     '先看时间与地点，再看它如何从一座城走向五大洲。</p>'
     '<div class="hstats"><div><b>1386</b>海德堡大学建校</div><div><b>7</b>帝国选侯之一</div><div><b>3</b>个月内连出三版</div><div><b>40+</b>种语言译本</div></div></section>'
     '<section class="sec histsec" id="hist-map"><div class="eyebrow">MAPPA · 1517 → 1619</div><h2>互动时间线 × 真实地图</h2>'
     '<p class="lead">点按左侧年份，地图飞到事件发生地；也可直接点地图上的编号。</p>'
     '<div class="hgrid"><div class="tlwrap">%s</div><div class="mapbox"><div id="mapEU" class="lmap" aria-label="宗教改革欧洲地图"></div>'
     '<div class="mapnote" id="mapEUnote">地图加载中…</div></div></div>'
     '<script type="application/json" id="evData">%s</script></section>'
     '<section class="sec histsec" id="hist-rhine"><div class="eyebrow">SCHEMA</div><h2>示意图：莱茵走廊——思想顺流北上</h2>'
     '<p class="lead">从巴塞尔、斯特拉斯堡到海德堡，再顺莱茵而下到韦瑟尔、埃姆登：印刷品、流亡者与要理问答沿着同一条河传播。</p>'
     '<div class="rhwrap"><div class="zbox">%s<button class="zbtn" type="button">⤢ 放大</button></div>'
     '<div class="rhnote"><div class="tile"><div class="tl">🏰<span>为什么是海德堡</span></div><p>大学（1386）提供神学家，选侯提供政治保护，莱茵水道提供印刷与流通。三者在一座城里交汇。</p></div>'
     '<div class="tile"><div class="tl">🛶<span>流亡者网络</span></div><p>低地改革宗难民经莱茵下游的韦瑟尔、埃姆登组织教会，把海德堡要理带回荷兰。</p></div>'
     '<div class="tile t-warn"><div class="tl">⚠️<span>压力来源</span></div><p>南有特伦特会议，北有路德宗诸邦，帝国法只承认两种宗教——每一处措辞都要经得起帝国议会的审查。</p></div></div></div></section>'
     '<section class="sec histsec" id="hist-world"><div class="eyebrow">ORBIS</div><h2>从一座城到五大洲：传播地图</h2>'
     '<p class="lead">随荷兰贸易、移民与宣教传遍世界；今天仍是欧陆改革宗教会（CanRC、URCNA、PRC、Heritage Reformed 等）的标准教理。</p>'
     '<div class="mapbox wide"><div id="mapWorld" class="lmap" aria-label="海德堡要理问答全球传播地图"></div><div class="mapnote" id="mapWorldnote"></div></div>'
     '<script type="application/json" id="wdData">%s</script></section>'
     '<section class="sec histsec" id="hist-culture"><div class="eyebrow">CULTURA</div><h2>文化区域对照：同一场改革，四种面貌</h2>'
     '<div class="tw"><table class="cult"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
     '<p class="fnote7">🔎 读要理时记住处境：海德堡的温和语气是写给帝国审查者看的，第 80 问的锋利是写给特伦特会议看的，第 1 问的「安慰」是写给在战争与瘟疫中的会众看的。</p></section>'
    ) % (tl, json.dumps(ev, ensure_ascii=False), rhine_svg(), json.dumps(wd, ensure_ascii=False), th, tr)


HIST_CSS = r"""
/* ===== v11 历史·地图·文化 ===== */
.hstats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin:14px 0}
.hstats div{border-radius:14px;padding:12px 14px;background:linear-gradient(140deg,color-mix(in srgb,var(--deliver) 14%,var(--paper-2)),var(--paper-2));font-family:var(--sans);font-size:13px;color:var(--ink-2)}
.hstats b{display:block;font-family:var(--disp);font-size:28px;color:var(--deliver);line-height:1.1}
.hgrid{display:grid;grid-template-columns:minmax(260px,380px) 1fr;gap:14px;align-items:start}
.tlwrap{display:grid;gap:8px;max-height:560px;overflow:auto;padding-right:4px;overscroll-behavior:contain}
.tl11{--c:var(--deliver);text-align:left;cursor:pointer;display:grid;grid-template-columns:62px 1fr;gap:0 10px;padding:10px 12px;border-radius:12px;border:1px solid var(--rule);
  background:var(--paper-2);color:var(--ink);font:inherit;transition:transform .2s,box-shadow .2s,border-color .2s}
.tl11.misery{--c:var(--misery)}.tl11.gratitude{--c:var(--gratitude)}
.tl11 b{grid-row:span 3;font-family:var(--disp);font-size:22px;color:var(--c);align-self:center}
.tl11 span{font-weight:700;font-size:15px}.tl11 em{font-style:normal;font-family:var(--sans);font-size:12px;color:var(--muted)}
.tl11 p{margin:2px 0 0;font-size:13.5px;line-height:1.6;color:var(--ink-2)}
.tl11:hover{transform:translateX(3px)}
.tl11.on{border-color:var(--c);box-shadow:0 8px 20px -12px var(--c);background:color-mix(in srgb,var(--c) 10%,var(--paper-2))}
.mapbox{position:relative;isolation:isolate;z-index:0;border-radius:16px;overflow:hidden;border:1px solid var(--rule);box-shadow:var(--sh2);background:var(--paper-3)}
.lmap{height:560px;width:100%;position:relative;z-index:0;isolation:isolate}
.mapbox.wide .lmap{height:480px}
.mapnote{position:absolute;left:10px;bottom:10px;z-index:500;font-family:var(--sans);font-size:12px;padding:4px 10px;border-radius:99px;background:color-mix(in srgb,var(--paper) 90%,transparent);color:var(--muted);pointer-events:none}
.mapnote:empty{display:none}
.lmap .leaflet-popup-content{font-family:var(--serif);font-size:14px;line-height:1.6;margin:10px 14px}
.lmap .leaflet-popup-content b{color:#1D3F8F}
.pin11{width:30px;height:30px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);display:grid;place-items:center;box-shadow:0 6px 12px -4px rgba(0,0,0,.4);border:2px solid #fff}
.pin11 span{transform:rotate(45deg);color:#fff;font:700 12px/1 -apple-system,"PingFang SC",sans-serif}
.pin11.misery{background:#D2283E}.pin11.deliver{background:#2457C5}.pin11.gratitude{background:#DB8A0B}.pin11.prologue{background:#7048C0}
.pin11.pulse11{animation:pinpulse 1.2s ease 2}
@keyframes pinpulse{50%{box-shadow:0 0 0 14px rgba(219,138,11,.25)}}
.leaflet-container{font:inherit;background:#DDE6EE}
@media (max-width:860px){.hgrid{grid-template-columns:1fr}.tlwrap{max-height:none;grid-auto-flow:column;grid-auto-columns:78%;overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory}.tl11{scroll-snap-align:start}.lmap{height:420px}}
/* 莱茵示意图 */
.rhwrap{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px;align-items:start}
.rhnote{display:grid;gap:10px}
@media (max-width:860px){.rhwrap{grid-template-columns:1fr}}
.rhine .river{fill:none;stroke-width:14;stroke-linecap:round;opacity:.85}
.rhine .river.small{stroke:#5FA8D3;stroke-width:7}
.rhine .idea{fill:none;stroke:#FFC250;stroke-width:3;stroke-dasharray:6 14;animation:flowmv 1.4s linear infinite}
.rhine .rc circle{fill:#fff;stroke:#1D3F8F;stroke-width:3}
.rhine .rc.key circle{fill:#D2283E;stroke:#fff}
.rhine .rn{font-family:var(--serif);font-size:17px;font-weight:800;fill:var(--ink)}
.rhine .rc.key .rn{fill:#D2283E;font-size:19px}
.rhine .rs{font-family:var(--sans);font-size:12px;fill:var(--muted)}
.rhine .rl7{font-family:var(--sans);font-size:13px;fill:var(--muted)}.rhine .rl7.big{font-weight:700;fill:#2457C5}
.cult th:first-child{white-space:nowrap}
"""

HIST_JS = r"""
(function(){var d=document;var E1=d.getElementById('mapEU'),E2=d.getElementById('mapWorld');if(!E1&&!E2)return;
function css(h){if(d.querySelector('link[href="'+h+'"]'))return;var l=d.createElement('link');l.rel='stylesheet';l.href=h;d.head.appendChild(l);}
function js(src,cb,fail){var s=d.createElement('script');s.src=src;s.onload=cb;s.onerror=fail;d.head.appendChild(s);}
var TILES=[
 {n:'Esri',u:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',o:{attribution:'© Esri'}},
 {n:'高德',u:'https://webrd0{s}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',o:{subdomains:'1234',attribution:'© 高德地图'}},
 {n:'OSM',u:'https://tile.openstreetmap.org/{z}/{x}/{y}.png',o:{attribution:'© OpenStreetMap'}}];
function base(map,note){var k=0,layer=null,ok=0,bad=0,timer;
 function use(i){if(layer)map.removeLayer(layer);k=i;ok=0;bad=0;var t=TILES[i];layer=L.tileLayer(t.u,Object.assign({maxZoom:18,crossOrigin:true},t.o)).addTo(map);
  note.textContent='底图：'+t.n+' · 载入中…';
  layer.on('tileload',function(){ok++;if(ok===4)note.textContent='底图：'+t.n;});
  layer.on('tileerror',function(){bad++;if(bad>=4&&ok<2)next();});
  clearTimeout(timer);timer=setTimeout(function(){if(ok<2)next();},5000);}
 function next(){if(k+1<TILES.length)use(k+1);else{note.textContent='在线底图暂不可用，请参看上方示意图';}}
 use(0);}
function pin(c,t){return L.divIcon({className:'',html:'<div class="pin11 '+c+'"><span>'+t+'</span></div>',iconSize:[30,30],iconAnchor:[15,30],popupAnchor:[0,-28]});}
function init(){
 if(E1){var ev=JSON.parse(d.getElementById('evData').textContent);var m=L.map(E1,{scrollWheelZoom:false,zoomSnap:.5}).setView([50.2,8.5],5.5);base(m,d.getElementById('mapEUnote'));
  var seen={},mk=[];ev.forEach(function(e,i){var key=e.p;var html='<b>'+e.y+' · '+e.t+'</b><br>📍 '+e.p+'<br>'+e.x;
   if(seen[key]){seen[key].m.bindPopup(seen[key].h+='<hr style="border:0;border-top:1px dashed #ccc">'+html);mk[i]=seen[key].m;return;}
   var mm=L.marker([e.la,e.lo],{icon:pin(e.c,i+1)}).addTo(m).bindPopup(html);seen[key]={m:mm,h:html};mk[i]=mm;});
  L.polyline(ev.map(function(e){return [e.la,e.lo];}),{color:'#DB8A0B',weight:2,dashArray:'6 8',opacity:.8}).addTo(m);
  d.querySelectorAll('.tl11').forEach(function(b){b.addEventListener('click',function(){var e=ev[+b.dataset.i];d.querySelectorAll('.tl11.on').forEach(function(x){x.classList.remove('on')});b.classList.add('on');
   m.flyTo([e.la,e.lo],7,{duration:1.1});setTimeout(function(){mk[+b.dataset.i].openPopup();},1150);});});}
 if(E2){var wd=JSON.parse(d.getElementById('wdData').textContent);var w=L.map(E2,{scrollWheelZoom:false,worldCopyJump:true}).setView([25,20],2);base(w,d.getElementById('mapWorldnote'));
  var hd=[49.41,8.69];wd.forEach(function(p,i){L.marker([p.la,p.lo],{icon:pin(p.c,i+1)}).addTo(w).bindPopup('<b>'+p.p+'</b><br>'+p.t);
   if(i)L.polyline([hd,[p.la,p.lo]],{color:'#2457C5',weight:1.5,opacity:.55,dashArray:'4 6'}).addTo(w);});}
}
function boot(){css('assets/leaflet/leaflet.css');js('assets/leaflet/leaflet.js',init,function(){['mapEUnote','mapWorldnote'].forEach(function(i){var n=d.getElementById(i);if(n)n.textContent='地图组件加载失败，请参看示意图';});});}
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){if(es.some(function(x){return x.isIntersecting;})){io.disconnect();boot();}},{rootMargin:'400px'});[E1,E2].forEach(function(x){if(x)io.observe(x);});}else boot();
})();
"""

# ───────── 多主题 ─────────
THEMES = [("auto", "🌓", "跟随系统"), ("light", "📜", "羊皮纸"), ("forest", "🌲", "森林"), ("ocean", "🌊", "海洋"),
          ("rose", "🌸", "玫瑰"), ("ink", "🖋️", "墨韵"), ("dark", "🌙", "夜读"), ("starry", "✨", "星空")]

THEME_CSS = r"""
/* ===== v11 主题（浅色 palette 覆盖；深色 palette 基于 dark） ===== */
:root[data-theme="forest"]{--paper:#EEF3EC;--paper-2:#FAFDF8;--paper-3:#E2EBDF;--rule:#C9D8C4;--ink:#132017;--ink-2:#3C4B40;--muted:#6D7D70;
 --royal:#1E5B3A;--deliver:#1E6B45;--misery:#B23A2E;--gratitude:#B07A10;--prologue:#5B4A8A;--teal:#0E7C70;--brass:#A87212;--rubric:#B23A2E}
:root[data-theme="ocean"]{--paper:#EAF2F8;--paper-2:#F8FBFE;--paper-3:#DCE8F2;--rule:#BFD3E4;--ink:#0E1B26;--ink-2:#3A4C5C;--muted:#6B7F90;
 --royal:#0F4C81;--deliver:#1565C0;--misery:#C62F4B;--gratitude:#D08A0A;--prologue:#5E4BB5;--teal:#00838F;--brass:#B9770E;--rubric:#C62F4B}
:root[data-theme="rose"]{--paper:#FBF0F1;--paper-2:#FFFAFA;--paper-3:#F4E1E4;--rule:#E8CBD0;--ink:#24151A;--ink-2:#55404A;--muted:#8C7480;
 --royal:#8E2950;--deliver:#3B5BB5;--misery:#C2185B;--gratitude:#C77700;--prologue:#7B3FA0;--teal:#00796B;--brass:#B06A00;--rubric:#C2185B}
:root[data-theme="ink"]{--paper:#F2F1EE;--paper-2:#FFFFFF;--paper-3:#E6E4DF;--rule:#CFCBC2;--ink:#111111;--ink-2:#3A3A3A;--muted:#6E6E6E;
 --royal:#111111;--deliver:#1F3A93;--misery:#B71C1C;--gratitude:#8D6E00;--prologue:#4A148C;--teal:#00695C;--brass:#8D6E00;--rubric:#B71C1C}
:root[data-theme="starry"]{--paper:#0F1024;--paper-2:#17183A;--paper-3:#1F2150;--rule:#34376B;--ink:#ECEBFF;--ink-2:#C2C0EA;--muted:#8E8CC0;
 --royal:#B9AEFF;--deliver:#8FB0FF;--misery:#FF8FB1;--gratitude:#FFD36E;--prologue:#C9A4FF;--teal:#6FE3D4;--brass:#FFD36E;--rubric:#FF8FB1;--sh:0 1px 2px rgba(0,0,0,.5)}
:root[data-theme="starry"] body{background:radial-gradient(1200px 600px at 80% -10%,rgba(150,120,255,.18),transparent),var(--paper)}
.thpick{position:fixed;z-index:130;top:calc(var(--tbh) + 6px);right:12px;display:none;grid-template-columns:repeat(2,minmax(120px,1fr));gap:6px;padding:10px;border-radius:16px;
 background:var(--paper-2);border:1px solid var(--rule);box-shadow:0 24px 50px -20px rgba(0,0,0,.35)}
.thpick.on{display:grid;animation:fadein .18s ease}
.thpick button{display:flex;align-items:center;gap:8px;padding:8px 12px;border-radius:10px;border:1px solid var(--rule);background:var(--paper);color:var(--ink);font:600 13.5px var(--sans);cursor:pointer}
.thpick button i{width:16px;height:16px;border-radius:50%;flex:none;box-shadow:inset 0 0 0 2px rgba(255,255,255,.6)}
.thpick button.cur{border-color:var(--royal);box-shadow:0 0 0 2px color-mix(in srgb,var(--royal) 35%,transparent)}
"""
THEME_SW = {"auto": "linear-gradient(90deg,#F6F2E8 50%,#13151B 50%)", "light": "#F6F2E8", "forest": "#1E6B45", "ocean": "#1565C0",
            "rose": "#C2185B", "ink": "#111", "dark": "#1A1D25", "starry": "linear-gradient(135deg,#17183A,#7B5CFF)"}

THEME_JS = r"""
(function(){var d=document,R=d.documentElement,btn=d.getElementById('themeBtn');if(!btn)return;var ls;try{ls=localStorage}catch(e){}
var TH=%s,SW=%s;
function apply(k){if(k==='auto')R.removeAttribute('data-theme');else R.setAttribute('data-theme',k);
 var t=TH.filter(function(x){return x[0]===k;})[0]||TH[0];btn.textContent=t[1]+' '+t[2];try{ls&&ls.setItem('hc-theme',k);}catch(e){}
 p.querySelectorAll('button').forEach(function(b){b.classList.toggle('cur',b.dataset.k===k);});}
var p=d.createElement('div');p.className='thpick';p.innerHTML=TH.map(function(t){return '<button type="button" data-k="'+t[0]+'"><i style="background:'+SW[t[0]]+'"></i>'+t[1]+' '+t[2]+'</button>';}).join('');d.body.appendChild(p);
var k='auto';try{k=(ls&&ls.getItem('hc-theme'))||'auto';}catch(e){}apply(k);
btn.onclick=function(e){e.stopPropagation();p.classList.toggle('on');};
p.addEventListener('click',function(e){var b=e.target.closest('button');if(b){apply(b.dataset.k);p.classList.remove('on');}});
d.addEventListener('click',function(e){if(!e.target.closest('.thpick'))p.classList.remove('on');});
})();
""" % (json.dumps([list(t) for t in THEMES], ensure_ascii=False), json.dumps(THEME_SW))

# ───────── 目录可拖宽 + 动态高亮强化 ─────────
TOC_CSS = r"""
@media (min-width:981px){.shell:not(.hid){grid-template-columns:var(--tocw,300px) minmax(0,1fr)!important}}
.tocgrip{position:fixed;top:0;left:0;width:12px;height:100vh;cursor:col-resize;z-index:60;touch-action:none;display:none}
.tocgrip::after{content:"";position:absolute;top:50%;left:4px;width:4px;height:46px;margin-top:-23px;border-radius:4px;background:var(--rule);transition:background .2s,height .2s}
.tocgrip:hover::after,.tocgrip.drag::after{background:var(--royal);height:80px;margin-top:-40px}
body.tocdrag{cursor:col-resize;user-select:none}

.toc a.active{background:linear-gradient(90deg,color-mix(in srgb,var(--royal) 16%,transparent),transparent)!important;border-left:3px solid var(--rubric)!important;color:var(--royal)!important;font-weight:700}
.toc a.active .emo{display:inline-block;animation:bob 1.6s ease-in-out 2}
.toc a .qr{font-family:var(--sans);font-size:11.5px;color:var(--muted);margin-left:3px;white-space:nowrap;font-weight:400}
.toc a.active .qr{color:var(--rubric)}
"""
TOC_JS = r"""
(function(){var d=document,sh=d.querySelector('.shell'),side=d.querySelector('.side');if(!sh||!side)return;var ls;try{ls=localStorage}catch(e){}
try{var w=ls&&ls.getItem('hc-tocw');if(w)sh.style.setProperty('--tocw',w+'px');}catch(e){}
var g=d.createElement('div');g.className='tocgrip';g.title='拖动调整目录宽度（双击复原）';d.body.appendChild(g);
var mob=function(){return matchMedia('(max-width:980px)').matches;};
function place(){var r=side.getBoundingClientRect();var shown=r.width>40&&r.right>20&&getComputedStyle(side).visibility!=='hidden'&&!(sh.classList.contains('hid')&&!mob())&&(!mob()||d.body.classList.contains('nav'));
 g.style.display=shown?'block':'none';if(shown){g.style.left=(r.right-6)+'px';g.style.top=Math.max(r.top,0)+'px';g.style.height=Math.min(r.height,innerHeight-Math.max(r.top,0))+'px';}}
var x0=null,w0;g.addEventListener('pointerdown',function(e){x0=e.clientX;var cv=parseFloat(mob()?getComputedStyle(d.documentElement).getPropertyValue('--tocw-m'):sh.style.getPropertyValue('--tocw'));w0=cv||side.getBoundingClientRect().width;g.setPointerCapture(e.pointerId);g.classList.add('drag');d.body.classList.add('tocdrag');e.preventDefault();e.stopPropagation();});
g.addEventListener('pointermove',function(e){if(x0==null)return;var tw;if(mob()){var nw=Math.max(220,Math.min(innerWidth*.92,w0+e.clientX-x0));tw=nw;d.documentElement.style.setProperty('--tocw-m',nw+'px');}
 else{var nw2=Math.max(200,Math.min(620,w0+e.clientX-x0));tw=nw2;sh.style.setProperty('--tocw',nw2+'px');}place();
 try{ls&&ls.setItem(mob()?'hc-tocw-m':'hc-tocw',Math.round(tw));}catch(e){}});
function end(){if(x0==null)return;x0=null;g.classList.remove('drag');d.body.classList.remove('tocdrag');place();}
g.addEventListener('pointerup',end);g.addEventListener('pointercancel',end);
g.addEventListener('dblclick',function(){sh.style.removeProperty('--tocw');d.documentElement.style.removeProperty('--tocw-m');try{ls&&ls.removeItem('hc-tocw');ls&&ls.removeItem('hc-tocw-m');}catch(e){}place();});
try{var wm=ls&&ls.getItem('hc-tocw-m');if(wm)d.documentElement.style.setProperty('--tocw-m',wm+'px');}catch(e){}
addEventListener('resize',place,{passive:true});addEventListener('scroll',function(){if(!mob())place();},{passive:true});
new MutationObserver(function(){setTimeout(place,260);place();}).observe(d.body,{attributes:true,attributeFilter:['class']});
new MutationObserver(function(){setTimeout(place,260);}).observe(sh,{attributes:true,attributeFilter:['class']});
setTimeout(place,50);setTimeout(place,600);
/* 顶栏高度随换行变化 → 更新 --tbh */
var tb=d.querySelector('.topbar');if(tb&&'ResizeObserver' in window)new ResizeObserver(function(){d.documentElement.style.setProperty('--tbh',tb.getBoundingClientRect().height+'px');place();}).observe(tb);
/* 当前页的主日链接也高亮页面分组 */
var cur=location.pathname.split('/').pop()||'index.html';d.querySelectorAll('.toc a').forEach(function(a){var h=a.getAttribute('href')||'';if(h.charAt(0)==='#'||h.indexOf(cur)===0)a.classList.add('here');});
})();
"""

# ───────── 角落导航 ─────────
FAB_CSS = r"""
#toTop{display:none!important}
.fab{position:fixed;right:max(12px,env(safe-area-inset-right));bottom:max(14px,env(safe-area-inset-bottom));z-index:90;display:flex;flex-direction:column;align-items:flex-end;gap:6px}
.fab .fset{display:flex;flex-direction:column;gap:6px;opacity:0;transform:translateY(8px) scale(.9);pointer-events:none;transition:opacity .2s,transform .2s}
.fab.open .fset{opacity:1;transform:none;pointer-events:auto}
.fab button,.fab a{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;border:1px solid var(--rule);background:color-mix(in srgb,var(--paper-2) 92%,transparent);
 color:var(--ink-2);font:600 16px/1 var(--sans);cursor:pointer;text-decoration:none;box-shadow:0 6px 18px -8px rgba(0,0,0,.35);transition:transform .15s,background .2s,color .2s}
.fab button:hover,.fab a:hover{transform:scale(1.08);color:var(--royal)}
.fab .fmain{opacity:.55}.fab:hover .fmain,.fab.open .fmain{opacity:1}
.fab [data-tip]{position:relative}
.fab [data-tip]:hover::before{content:attr(data-tip);position:absolute;right:48px;top:50%;transform:translateY(-50%);white-space:nowrap;font:500 12px var(--sans);
 background:var(--ink);color:var(--paper);padding:4px 8px;border-radius:6px}
@media print{.fab{display:none}}
"""
FAB_HTML = ('<div class="fab" id="fab"><div class="fset">'
            '<a href="index.html" data-tip="主页" aria-label="主页">⌂</a>'
            '<button type="button" data-f="back" data-tip="返回" aria-label="返回">←</button>'
            '<button type="button" data-f="fwd" data-tip="前进" aria-label="前进">→</button>'
            '<button type="button" data-f="top" data-tip="到顶部" aria-label="到顶部">⤒</button>'
            '<button type="button" data-f="bot" data-tip="到底部" aria-label="到底部">⤓</button>'
            '</div><button type="button" class="fmain" data-f="tog" data-tip="导航" aria-label="展开导航">⋯</button></div>')
FAB_JS = r"""
(function(){var d=document,f=d.getElementById('fab');if(!f)return;
function to(y){var L=window.__lenis;if(L)L.scrollTo(y,{duration:1.0});else scrollTo({top:y,behavior:'smooth'});}
f.addEventListener('click',function(e){var b=e.target.closest('[data-f]');if(!b)return;var k=b.dataset.f;
 if(k==='tog'){f.classList.toggle('open');return;}
 if(k==='back')history.back();else if(k==='fwd')history.forward();else if(k==='top')to(0);else if(k==='bot')to(d.documentElement.scrollHeight);});
if(matchMedia('(hover:hover)').matches){f.addEventListener('mouseenter',function(){f.classList.add('open');});f.addEventListener('mouseleave',function(){f.classList.remove('open');});}
d.addEventListener('click',function(e){if(!e.target.closest('#fab'))f.classList.remove('open');});
})();
"""

CSS11 = HIST_CSS + THEME_CSS + TOC_CSS + FAB_CSS
JS11 = THEME_JS + TOC_JS + FAB_JS + HIST_JS

# ───────── 背诵模式（自测）重做 ─────────
DRILL_CSS = r"""
/* 背诵模式：只留题目；答案点按显示；记忆钥匙作模糊提示；其余解读全部隐藏 */
body.drill .onepage,body.drill .ld .keyline .kb-core,body.drill .ld .keyline .kb-app,body.drill .ld .ld-side,body.drill .ld .ld-g3,
body.drill .ld details.deep,body.drill .ld .srcnote,body.drill .ld .qa .refs{display:none!important}
body.drill .ld .ld-g{grid-template-columns:1fr!important}
body.drill .ld .keyline{grid-template-columns:1fr!important}
body.drill .ld .kb-memo{cursor:pointer}
body.drill .ld .kb-memo p{filter:blur(7px);user-select:none;transition:filter .25s}
body.drill .ld .kb-memo.show p{filter:none}
body.drill .ld .kb-memo .badge::after{content:" · 想不起来？点按看提示"}
body.drill .ld .kb-memo.show .badge::after{content:" · 提示已显示"}
body.drill .qa{cursor:pointer;transition:background .2s}
body.drill .qa:not(.open):hover{background:color-mix(in srgb,var(--gratitude) 10%,transparent)}
body.drill .qa::after{content:"👆 先自己背出答案，再点按核对"!important;display:block;font-family:var(--sans);font-size:12.5px;color:var(--brass);margin-top:6px}
body.drill .qa.open::after{content:"✅ 已显示 · 再点一次遮住"!important;color:var(--teal)}
body.drill .qa.open .a{display:block!important;animation:fadein .25s ease}
.drillbar{display:none}
body.drill .drillbar{display:flex;position:sticky;top:calc(var(--tbh) + 6px);z-index:30;flex-wrap:wrap;align-items:center;gap:8px 12px;margin:10px 0;padding:10px 14px;
 border-radius:14px;background:color-mix(in srgb,var(--gratitude) 16%,var(--paper-2));border:1.5px solid color-mix(in srgb,var(--gratitude) 45%,transparent);box-shadow:var(--sh2);font-size:14.5px}
.drillbar b{color:var(--gratitude)}
.drillbar .sp{flex:1}
.drillbar .btn{padding:5px 12px;font-size:13px}
#drillBtn.on{background:var(--gratitude)!important;border-color:var(--gratitude)!important;color:#fff!important}
"""
DRILL_JS = r"""
(function(){var d=document,b=d.body,main=d.querySelector('.main');if(!main||!d.querySelector('.ld .qa'))return;
var bar=d.createElement('div');bar.className='drillbar';
bar.innerHTML='<span>🎯 <b>背诵模式</b>：答案与解读已隐藏，只留题目。逐题背出后点按核对；想不起来可点「记忆钥匙」看模糊提示。</span><span class="sp"></span><span id="drCnt"></span><button class="btn" type="button" data-d="all">全部显示</button><button class="btn" type="button" data-d="none">全部遮盖</button><button class="btn" type="button" data-d="exit">退出背诵</button>';
var first=main.querySelector('.ld')||main.firstChild;main.insertBefore(bar,main.querySelector('.onepage')||first);
function cnt(){var all=d.querySelectorAll('.ld .qa').length,op=d.querySelectorAll('.ld .qa.open').length;var c=d.getElementById('drCnt');if(c)c.textContent='已核对 '+op+' / '+all+' 问';}
bar.addEventListener('click',function(e){var x=e.target.closest('[data-d]');if(!x)return;var k=x.dataset.d;
 if(k==='all')d.querySelectorAll('.ld .qa').forEach(function(q){q.classList.add('open');});
 if(k==='none'){d.querySelectorAll('.ld .qa.open,.kb-memo.show').forEach(function(q){q.classList.remove('open','show');});}
 if(k==='exit')d.getElementById('drillBtn').click();cnt();});
d.addEventListener('click',function(e){if(!b.classList.contains('drill'))return;var m=e.target.closest('.ld .kb-memo');if(m)m.classList.toggle('show');if(e.target.closest('.ld .qa'))setTimeout(cnt,0);});
var btn=d.getElementById('drillBtn');if(btn){btn.title='背诵自测：遮住答案与解读，逐题核对';btn.addEventListener('click',function(){setTimeout(cnt,0);if(b.classList.contains('drill')){var t=d.querySelector('.drillbar');if(t&&t.getBoundingClientRect().top<0)t.scrollIntoView({block:'start'});}});}
cnt();})();
"""
CSS11 += DRILL_CSS
JS11 += DRILL_JS

TOC2_CSS = r"""
/* 目录：单行省略（拉宽即可看全）· 分部配色 · 动态高亮 · 手机抽屉也可拉宽 */
@media (min-width:981px){.side{position:sticky}}
@media (max-width:980px){.side{position:fixed!important;width:min(var(--tocw-m,300px),92vw)!important;top:var(--tbh)!important;height:calc(100dvh - var(--tbh))!important}.tocgrip{z-index:70}}
.toc a{--tc:var(--royal);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:flex!important;align-items:center;gap:5px;min-width:0;
  border-left:3px solid transparent;transition:background .2s,border-color .2s,color .2s,padding .2s}
.toc a .t{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.toc a .no,.toc a .emo,.toc a .qr{flex:none}
.toc a .no{color:var(--tc);font-weight:700}
.toc a:hover{background:color-mix(in srgb,var(--tc) 10%,transparent);border-left-color:color-mix(in srgb,var(--tc) 50%,transparent);color:var(--tc)}
.toc a.active{background:linear-gradient(90deg,color-mix(in srgb,var(--tc) 22%,transparent),color-mix(in srgb,var(--tc) 4%,transparent))!important;
  border-left-color:var(--tc)!important;color:var(--tc)!important;box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--tc) 18%,transparent)}
.toc a.active .qr{color:var(--tc)}
.toc-h{color:var(--tc,var(--muted))!important;border-bottom-color:color-mix(in srgb,var(--tc,var(--rule)) 40%,transparent)!important}
.toc a.done .t::after{content:" ✓";color:var(--gratitude)}
"""
TOC2_JS = r"""
(function(){var d=document,toc=d.querySelector('.toc');if(!toc)return;
var C={'总论':'var(--prologue)','总纲':'var(--prologue)','困苦':'var(--misery)','拯救':'var(--deliver)','感恩':'var(--gratitude)','历史':'var(--teal)','跨主日':'#2E7D32','结语':'#2E7D32','附录':'#5B4A2E','三大普世信经':'var(--prologue)','海德堡要理问答':'var(--gratitude)','比利时信条':'var(--deliver)','多特信经':'var(--misery)'};
var cur='var(--royal)';
[].forEach.call(toc.children,function(el){
 if(el.classList.contains('toc-h')){var t=el.textContent;for(var k in C)if(t.indexOf(k)===0){cur=C[k];break;}el.style.setProperty('--tc',cur);return;}
 if(el.tagName==='A'){el.style.setProperty('--tc',el.classList.contains('toc-src')?'var(--teal)':cur);
  if(!el.querySelector('.t')){var sp=d.createElement('span');sp.className='t';[].slice.call(el.childNodes).forEach(function(n){if(n.nodeType===3||(n.nodeType===1&&!/\b(no|emo|qr)\b/.test(n.className)))sp.appendChild(n);});
   var qr=el.querySelector('.qr');if(qr)el.insertBefore(sp,qr);else el.appendChild(sp);}
  el.title=el.textContent.replace(/\s+/g,' ').trim();}});
})();
"""
CSS11 += TOC2_CSS
JS11 += TOC2_JS
