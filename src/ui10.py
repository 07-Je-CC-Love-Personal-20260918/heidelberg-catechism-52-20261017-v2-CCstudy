# -*- coding: utf-8 -*-
"""v10：多页面拆分（轻量、原生顺滑）· 共享 assets · 跨页链接重写 · 全站搜索索引 · 每部分一页纸要点 · 原生页面过渡与预渲染"""
import json, os, re, html as _h

E = lambda s: _h.escape(str(s), quote=False)
A = lambda s: _h.escape(str(s), quote=True)

PAGES = [  # file, emoji, short, long, LD range or None
    ("index.html", "🏛️", "总论", "总论 · 圣经全景与历史", None),
    ("p1-misery.html", "🪞", "困苦", "总纲与困苦 · 主日 1–4", (1, 4)),
    ("p2-christ.html", "✝️", "中保", "拯救 · 中保与圣子 · 主日 5–19", (5, 19)),
    ("p3-spirit.html", "🔥", "圣灵·圣礼", "拯救 · 圣灵、教会与圣礼 · 主日 20–31", (20, 31)),
    ("p4-law.html", "📋", "十诫", "感恩 · 十诫 · 主日 32–44", (32, 44)),
    ("p5-prayer.html", "🙏", "祷告", "感恩 · 祷告 · 主日 45–52", (45, 52)),
    ("topics.html", "🗂️", "专题·附录", "跨主日专题 · 结语 · 附录", None),
]

SUMMARY = {
 "p1-misery.html": ("misery", "先量出安慰有多大，才知道困苦有多深。",
   [("🕊️", "问 1 是全书总纲", "所有权转移：身体与灵魂、生与死，都不属自己，属于信实的救主耶稣基督。"),
    ("3️⃣", "问 2 三件必知", "困苦 → 拯救 → 感恩，正是罗马书 1–3、3–11、12–16 的骨架。"),
    ("🪞", "律法作镜（问 3–5）", "基督把律法总结为爱神爱人；照这面镜子，我本性倾向恨神恨邻舍。"),
    ("🍎", "败坏的来源（问 6–8）", "神造人本好，有真知识、公义、圣洁；堕落出于亚当，人性全然败坏，非重生不能行善。"),
    ("⚖️", "公义不打折（问 9–11）", "神极其慈悲，也极其公义；罪必受永刑——这一步把人逼到唯一的出路：中保。")],
   "罗 7:24–25", [1, 2, 3, 4]),
 "p2-christ.html": ("deliver", "唯一能满足神公义的中保：真神、真人、义人——耶稣基督。",
   [("🌉", "中保的条件（问 12–18）", "人犯罪须由人偿还；须是义人，才不为自己受罚；须是真神，才能承受神的烈怒并赐回生命。"),
    ("🔑", "真信心（问 21–23）", "确知（知识）＋确信（信靠），内容就是使徒信经。"),
    ("🔺", "三一与父（主日 8–10）", "一神三位；全能的创造主是我的父，护理使万事临到都出于父手，使我在逆境中忍耐、顺境中感恩。"),
    ("👑", "名与职分（主日 11–13）", "耶稣＝唯一救主；基督＝先知、祭司、君王，我因受膏有分于他的职分。"),
    ("📉", "降卑到升高（主日 14–19）", "成孕、受苦、十架、降在阴间（灵魂极苦）；复活、升天、坐右边、再来——每一步都问「对我有何益处」。")],
   "腓 2:6–11", list(range(5, 20))),
 "p3-spirit.html": ("deliver", "基督所成就的，圣灵借教会、圣道与圣礼施行在我身上。",
   [("🔥", "圣灵（主日 20）", "与父子同为真神，也赐给了我，使我借真信心有分于基督和他一切恩惠。"),
    ("⛪", "教会与相通（主日 21–22）", "神子借道与灵从全人类中召集、保护、保守选民的会众；我是其中活的肢体，盼望身体复活与永生。"),
    ("🧥", "唯独信心称义（主日 23–24）", "神把基督的义算为我的，如同我从未犯罪；善行不能使人称义，却必然结出果子。"),
    ("📖", "圣道与圣礼（主日 25–30）", "圣灵借讲道生发信心，借圣礼坚固；洗礼与圣餐是福音应许可见的记号与印证。"),
    ("🗝️", "天国的钥匙（主日 31）", "讲道与教会纪律——对信者开、对不悔改者关。")],
   "罗 10:17", list(range(20, 32))),
 "p4-law.html": ("gratitude", "得救不靠善行；得救之人必然行善——十诫是感恩的规范。",
   [("🌳", "为何仍要行善（主日 32）", "基督用灵更新我们：以生命感谢神、借果子确知信心、用敬虔的生活为邻舍赢得基督。"),
    ("🔄", "真悔改（主日 33）", "旧人死、新人活；善行出于真信心、照着神的律法、为神的荣耀。"),
    ("1️⃣", "第一块法版（主日 34–38）", "独一的神、按神吩咐的方式敬拜、圣名、安息（主日聚会，一生歇恶工）。"),
    ("🤲", "第二块法版（主日 39–43）", "权柄、生命、贞洁、财物、真理——每一条都从行为追到心。"),
    ("❤️", "律法的严格（主日 44）", "最圣洁的人今生也只有顺服的小开端；仍要宣讲律法，使我们更认罪、更投靠基督、更求圣灵。")],
   "罗 12:1", list(range(32, 45))),
 "p5-prayer.html": ("gratitude", "祷告是感恩最主要的部分——照主祷文向天上的父求。",
   [("🙏", "必要性（主日 45）", "神只将恩典与圣灵赐给不住恳切祈求、并为此感谢的人。"),
    ("👨‍👦", "称呼（主日 46）", "「我们在天上的父」：孩子般的敬畏与信靠，不以属地的方式想像神。"),
    ("✨", "前三求为神（主日 47–49）", "尊你的名为圣、愿你的国降临、愿你的旨意行在地上。"),
    ("🥖", "后三求为人（主日 50–52）", "日用的饮食、免我们的债（我们也饶恕人）、不叫我们遇见试探。"),
    ("✅", "阿们（问 129）", "神垂听我的祷告，比我心里感觉到的更确实。")],
   "太 6:9–13", list(range(45, 53))),
}

VT_CSS = r"""
/* ===== v10：原生页面过渡（View Transitions）· 页面导航条 · 一页纸要点 ===== */
@view-transition{navigation:auto}
::view-transition-old(root){animation:vt-out .28s cubic-bezier(.4,0,.2,1) both}
::view-transition-new(root){animation:vt-in .42s cubic-bezier(.2,.8,.2,1) both}
@keyframes vt-out{to{opacity:0;transform:translate3d(0,-10px,0) scale(.995)}}
@keyframes vt-in{from{opacity:0;transform:translate3d(0,18px,0)}}
.topbar{view-transition-name:topbar}.side{view-transition-name:side}
@media (prefers-reduced-motion:reduce){::view-transition-old(root),::view-transition-new(root){animation:none}}
.pstrip{display:flex;gap:8px;overflow-x:auto;padding:14px 0 6px;margin:0 0 4px;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.pstrip::-webkit-scrollbar{display:none}
.pstrip a{flex:none;display:flex;align-items:center;gap:6px;padding:7px 14px;border-radius:99px;font-family:var(--sans);font-size:14px;font-weight:600;
  color:var(--ink-2);background:var(--paper-2);border:1px solid var(--rule);text-decoration:none;transition:transform .2s,background .2s,color .2s}
.pstrip a:hover{transform:translateY(-2px);color:var(--royal)}
.pstrip a.cur{background:var(--royal);border-color:var(--royal);color:#fff;box-shadow:0 6px 16px -8px var(--royal)}
.pnav{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:34px 0 10px}
.pnav a{display:grid;gap:2px;padding:16px 18px;border-radius:16px;text-decoration:none;color:var(--ink);background:var(--paper-2);border:1px solid var(--rule);
  box-shadow:var(--sh);transition:transform .25s,box-shadow .25s}
.pnav a:hover{transform:translateY(-3px);box-shadow:var(--sh2)}
.pnav a.nx{text-align:right}
.pnav small{font-family:var(--sans);font-size:12.5px;color:var(--muted);letter-spacing:.08em}
.pnav b{font-size:18px;color:var(--royal)}
.pnav span{font-size:28px}
@media (max-width:560px){.pnav{grid-template-columns:1fr}.pnav a.nx{text-align:left}}
/* 一页纸 */
.onepage{--pc:var(--deliver);margin:14px 0 6px;border-radius:20px;padding:20px clamp(14px,3vw,28px);
  background:linear-gradient(140deg,color-mix(in srgb,var(--pc) 16%,var(--paper-2)),var(--paper-2) 70%);border:1.5px solid color-mix(in srgb,var(--pc) 35%,var(--rule));box-shadow:var(--sh2)}
.onepage.misery{--pc:var(--misery)}.onepage.gratitude{--pc:var(--gratitude)}
.op-h{display:flex;flex-wrap:wrap;align-items:center;gap:8px 14px}
.op-h .badge{background:var(--pc)}
.op-h h2{margin:0;font-family:var(--disp);font-size:clamp(22px,3vw,30px);color:var(--pc)}
.op-thesis{margin:12px 0 14px;font-size:1.18em;font-weight:800;line-height:1.6;color:var(--ink);padding:10px 16px;border-radius:4px 12px 12px 4px;
  background:color-mix(in srgb,var(--pc) 11%,var(--paper));border-left:6px solid var(--pc)}
.op-pts{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:10px;counter-reset:op}
.op-pt{counter-increment:op;position:relative;border-radius:14px;padding:12px 14px 12px 54px;background:var(--paper);border:1px solid var(--rule);
  animation:rise .5s both;animation-delay:calc(var(--i)*.08s)}
.op-pt::before{content:counter(op);position:absolute;left:12px;top:12px;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;
  font-family:var(--sans);font-weight:800;font-size:14px;color:#fff;background:var(--pc)}
.op-pt b{display:block;font-size:15.5px;color:var(--pc)}
.op-pt b em{font-style:normal;margin-right:4px}
.op-pt p{margin:4px 0 0;font-size:.95em;line-height:1.75}
.op-chain{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin-top:14px}
.op-chain a{font-family:var(--sans);font-size:13px;padding:4px 10px;border-radius:99px;background:color-mix(in srgb,var(--pc) 12%,var(--paper));color:var(--ink);text-decoration:none;
  border:1px solid color-mix(in srgb,var(--pc) 30%,transparent);transition:background .2s}
.op-chain a:hover{background:var(--pc);color:#fff}
.op-chain i{font-style:normal;color:var(--pc);font-weight:800}
.op-verse{margin-left:auto;font-family:var(--sans);font-size:13px;font-weight:700;color:#fff;background:var(--pc);border-radius:8px;padding:3px 10px}
/* 全站搜索面板 */
.sres{position:fixed;left:50%;transform:translateX(-50%);top:calc(var(--tbh) + 6px);z-index:120;width:min(720px,calc(100vw - 20px));max-height:min(70vh,640px);overflow:auto;
  background:var(--paper);border:1px solid var(--rule);border-radius:16px;box-shadow:0 24px 60px -20px rgba(0,0,0,.35);padding:8px;display:none}
.sres.on{display:block;animation:fadein .18s ease}
.sres a{display:grid;grid-template-columns:auto 1fr;gap:2px 10px;padding:9px 12px;border-radius:10px;text-decoration:none;color:var(--ink)}
.sres a:hover,.sres a.sel{background:color-mix(in srgb,var(--royal) 9%,transparent)}
.sres a .se{grid-row:span 2;font-size:22px}
.sres a b{font-size:15px}.sres a b small{font-family:var(--sans);font-size:12px;color:var(--muted);font-weight:400;margin-left:6px}
.sres a i{font-style:normal;font-size:13.5px;color:var(--ink-2);line-height:1.6}
.sres mark{background:color-mix(in srgb,var(--gratitude) 35%,transparent);color:inherit;border-radius:3px;padding:0 1px}
.sres .sh{font-family:var(--sans);font-size:12px;color:var(--muted);padding:6px 12px}
"""

SEARCH_JS = r"""
(function(){var d=document,box=d.getElementById('q');if(!box)return;var IDX=null,panel=d.createElement('div');panel.className='sres';d.body.appendChild(panel);
function load(cb){if(IDX)return cb();if(window.HC_SEARCH){IDX=window.HC_SEARCH;return cb();}var s=d.createElement('script');s.src='assets/search.js';s.onload=function(){IDX=window.HC_SEARCH||[];cb();};s.onerror=function(){IDX=[];cb();};d.head.appendChild(s);}
function esc(t){return t.replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c];});}
function snip(s,v){var i=s.toLowerCase().indexOf(v);if(i<0)return esc(s.slice(0,60));var a=Math.max(0,i-22);return (a?'…':'')+esc(s.slice(a,i))+'<mark>'+esc(s.substr(i,v.length))+'</mark>'+esc(s.slice(i+v.length,i+v.length+40))+'…';}
var t;box.addEventListener('input',function(){clearTimeout(t);t=setTimeout(run,120);});
box.addEventListener('focus',function(){if(box.value.trim())run();});
function run(){var v=box.value.trim().toLowerCase();if(!v){panel.classList.remove('on');return;}
 load(function(){var out=[];for(var i=0;i<IDX.length;i++){var x=IDX[i];var tl=x.t.toLowerCase();var sc=tl.indexOf(v)>-1?3:(x.s.toLowerCase().indexOf(v)>-1?1:0);if(sc){if(x.u.indexOf('#ld')>-1)sc+=1;out.push([sc,i,x]);}}
 out.sort(function(a,b){return b[0]-a[0]||a[1]-b[1];});out=out.slice(0,40).map(function(z){return z[2];});
  panel.innerHTML=out.length?'<div class="sh">找到 '+out.length+(out.length>=40?'+':'')+' 处 · 回车打开第一项 · Esc 关闭</div>'+out.map(function(x,k){return '<a href="'+x.u+'"'+(k?'':' class="sel"')+'><span class="se">'+x.e+'</span><b>'+esc(x.t)+'<small>'+esc(x.p)+'</small></b><i>'+snip(x.s,v)+'</i></a>';}).join(''):'<div class="sh">没有找到「'+esc(box.value.trim())+'」</div>';
  panel.classList.add('on');});}
box.addEventListener('keydown',function(e){if(e.key==='Escape'){panel.classList.remove('on');box.blur();}if(e.key==='Enter'){var a=panel.querySelector('a');if(a){location.href=a.getAttribute('href');panel.classList.remove('on');}}});
d.addEventListener('click',function(e){if(!e.target.closest('.sres')&&e.target!==box)panel.classList.remove('on');if(e.target.closest('.sres a'))panel.classList.remove('on');});
})();
"""


def _chunks(m):
    VOID = {'br', 'img', 'input', 'hr', 'meta', 'link', 'source', 'wbr'}
    depth = 0; start = None; out = []
    for t in re.finditer(r'<(/?)([a-zA-Z0-9]+)((?:"[^"]*"|[^>"])*)>', m):
        cl, tag, rest = t.group(1), t.group(2).lower(), t.group(3)
        selfc = rest.rstrip().endswith('/') or tag in VOID
        if not cl:
            if depth == 0: start = t.start()
            if not selfc: depth += 1
            elif depth == 0: out.append(m[start:t.end()])
        else:
            depth -= 1
            if depth == 0: out.append(m[start:t.end()])
    return out


def _page_of(c):
    m = re.match(r'<section class="ld [^"]*" id="ld(\d+)"', c)
    if m:
        n = int(m.group(1))
        for f, *_, rg in PAGES:
            if rg and rg[0] <= n <= rg[1]:
                return f
    if 'class="sec appsec"' in c[:60] or c.startswith('<div class="foot"'):
        return "topics.html" if 'appsec' in c[:60] else "*"
    return None


def onepage(f, LDS_by_n, EMO):
    k, thesis, pts, verse, lds = SUMMARY[f]
    li = ''.join('<div class="op-pt" style="--i:%d"><b><em>%s</em>%s</b><p>%s</p></div>' % (i, e, E(t), E(x)) for i, (e, t, x) in enumerate(pts))
    chain = '<i>→</i>'.join('<a href="#ld%d">%s %d %s</a>' % (n, EMO[n - 1], n, E(LDS_by_n[n]["title"])) for n in lds)
    return ('<section class="onepage %s" id="onepage"><div class="op-h"><span class="badge b-key">📌 一页纸</span><h2>本页要点</h2><span class="op-verse">%s</span></div>'
            '<div class="op-thesis">%s</div><div class="op-pts">%s</div><div class="op-chain">%s</div></section>') % (k, verse, E(thesis), li, chain)


def split(h, LDS, EMO, outdir):
    """把单页 h 拆成多页；返回 {文件名: html}；同时写 assets/"""
    os.makedirs(os.path.join(outdir, "assets"), exist_ok=True)
    LDS_by_n = {d["n"]: d for d in LDS}
    # 1) 抽出样式与脚本到共享文件
    styles = re.findall(r'<style>(.*?)</style>', h, flags=re.S)
    css = '\n'.join(styles) + VT_CSS
    h = re.sub(r'<style>.*?</style>', '', h, flags=re.S)
    scripts = [s for s in re.findall(r'<script>(.*?)</script>', h, flags=re.S)]
    big = max(scripts, key=len)
    h = h.replace('<script>%s</script>' % big, '')
    js = big + SEARCH_JS
    open(os.path.join(outdir, "assets", "site.css"), "w", encoding="utf-8").write(css)
    open(os.path.join(outdir, "assets", "site.js"), "w", encoding="utf-8").write(js)
    # 2) 拆分 main
    i0 = h.index('<main'); i0 = h.index('>', i0) + 1; i1 = h.index('</main>')
    head, main, tail = h[:i0], h[i0:i1], h[i1:]
    chunks = _chunks(main)
    pages = {f: [] for f, *_ in PAGES}
    shared = []
    cur = "index.html"
    for c in chunks:
        p = _page_of(c)
        if c.startswith('<div class="part-div"'):
            # 部分分隔条跟随下一个块所在页面，先暂存
            shared.append(c); continue
        if p == "*":
            for f in pages: pages[f].append(c)
            continue
        if p is None:
            p = cur if cur != "topics.html" or 'appsec' in c[:60] else cur
        if shared:
            pages[p].extend(shared); shared = []
        pages[p].append(c); cur = p
    # 3) 搜索索引（并删除 data-s）
    idx = []
    for f, e, sh, lg, rg in PAGES:
        for c in pages[f]:
            m = re.match(r'<section class="ld [^"]*" id="ld(\d+)" data-n="\d+" data-s="([^"]*)"', c)
            if m:
                n = int(m.group(1)); d = LDS_by_n[n]
                idx.append({"u": "%s#ld%d" % (f, n), "e": EMO[n - 1], "t": "主日 %d · %s" % (n, d["title"]), "p": lg.split(" · ")[0],
                            "s": _h.unescape(m.group(2))})
                continue
            m = re.match(r'<section class="sec [^"]*" id="([\w-]+)">', c)
            if m:
                tt = re.search(r'<h2>(?:<span class="h2e">[^<]*</span>)?(.*?)</h2>', c, flags=re.S)
                txt = re.sub(r'<[^>]+>', '', c)
                idx.append({"u": "%s#%s" % (f, m.group(1)), "e": e, "t": _h.unescape(re.sub(r'<[^>]+>', '', tt.group(1))) if tt else m.group(1),
                            "p": lg.split(" · ")[0], "s": _h.unescape(re.sub(r'\s+', ' ', txt))[:900]})
    open(os.path.join(outdir, "assets", "search.js"), "w", encoding="utf-8").write(
        "window.HC_SEARCH=" + json.dumps(idx, ensure_ascii=False, separators=(',', ':')) + ";")
    for f in pages:
        pages[f] = [re.sub(r' data-s="[^"]*"', '', c) for c in pages[f]]
    # 4) id → 页面
    where = {}
    for f, cs in pages.items():
        for c in cs:
            if c.startswith('<div class="foot"'): continue
            for i in re.findall(r'\sid="([^"]+)"', c):
                where.setdefault(i, f)
    for i in re.findall(r'\sid="([^"]+)"', head + tail):
        where.setdefault(i, None)  # 全局元素
    # 5) 组装每页
    out = {}
    order = [p[0] for p in PAGES]
    for k, (f, e, sh, lg, rg) in enumerate(PAGES):
        strip = '<nav class="pstrip" aria-label="分页">%s<a href="texts.html">📜 原文</a></nav>' % ''.join(
            '<a href="%s"%s>%s %s</a>' % (pf, ' class="cur" aria-current="page"' if pf == f else '', pe, ps) for pf, pe, ps, pl, pr in PAGES)
        body = strip
        if f != "index.html":
            body += '<div id="sNote" class="lead hidden"></div>'
        if f in SUMMARY:
            body += onepage(f, LDS_by_n, EMO)
        body += ''.join(pages[f])
        prv = PAGES[k - 1] if k > 0 else None
        nxt = PAGES[k + 1] if k + 1 < len(PAGES) else ("texts.html", "📜", "原文", "原文阅读室 · 信经与信条全文", None)
        nav = '<nav class="pnav">%s%s</nav>' % (
            ('<a class="pv" href="%s"><small>← 上一页</small><span>%s</span><b>%s</b></a>' % (prv[0], prv[1], prv[3])) if prv else '<span></span>',
            '<a class="nx" href="%s"><small>下一页 →</small><span>%s</span><b>%s</b></a>' % (nxt[0], nxt[1], nxt[3]))
        # 页脚放最后
        foot = [c for c in pages[f] if c.startswith('<div class="foot"')]
        if foot:
            body = body.replace(foot[0], '') + nav + foot[0]
        else:
            body += nav
        hh = head
        hh = re.sub(r'<title>.*?</title>', '<title>%s · 海德堡要理问答 52 主日</title>' % E(lg), hh, count=1)
        hh = hh.replace('</head>', '<link rel="stylesheet" href="assets/site.css">'
                        '<script type="speculationrules">%s</script></head>' % json.dumps(
                            {"prerender": [{"where": {"href_matches": "/*"}, "eagerness": "moderate"}],
                             "prefetch": [{"urls": [p for p in order if p != f][:7] + ["texts.html"], "eagerness": "eager"}]}), 1)
        page = hh + body + tail.replace('</body>', '<script src="assets/site.js" defer></script></body>', 1)

        def fix(m):
            i = m.group(2)
            w = where.get(i)
            if w and w != f:
                return '%shref="%s#%s"' % (m.group(1), w, i)
            return m.group(0)
        page = re.sub(r'(\s)href="#([^"]+)"', fix, page)
        # 目录：标记本页
        out[f] = page
    return out, where


def fix_texts(t, where):
    def rep(m):
        i = m.group(1)
        return 'href="%s#%s"' % (where.get(i) or "index.html", i)
    t = re.sub(r'href="index\.html#([^"]+)"', rep, t)
    t = t.replace('</head>', '<style>@view-transition{navigation:auto}::view-transition-old(root){animation:vt-out .28s ease both}::view-transition-new(root){animation:vt-in .42s ease both}'
                  '@keyframes vt-out{to{opacity:0}}@keyframes vt-in{from{opacity:0;transform:translate3d(0,16px,0)}}</style>'
                  '<script type="speculationrules">{"prerender":[{"where":{"href_matches":"/*"},"eagerness":"moderate"}]}</script></head>', 1)
    return t
