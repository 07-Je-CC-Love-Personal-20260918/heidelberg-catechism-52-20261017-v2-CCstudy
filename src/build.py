# -*- coding: utf-8 -*-
import html, io, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import LDS, INTRO, TIMELINE, TABLES, CLOSURES, MEMO_TIPS
from css import CSS
from js import JS
import charts as C
from creeds import ECUMENICAL, UNITY, ISOMORPH, TEMPER
from story import TYPOLOGY, THEMES, BT_SECTION, CT_SECTION
from quiz import QUIZ, MNEMONICS, ANCHORS, PAIRS, PASTORAL

E = lambda s: html.escape(str(s), quote=False)
A = lambda s: html.escape(str(s), quote=True)
PL = {"总纲": "PROOEMIUM", "困苦": "MISERIA", "拯救": "LIBERATIO", "感恩": "GRATITUDO"}
INTROD = {s["id"]: s for s in INTRO}


def table(t):
    o = ['<div class="tw"><table><thead><tr>'] + ['<th>%s</th>' % E(x) for x in t["head"]]
    o.append('</tr></thead><tbody>')
    for r in t["rows"]:
        o.append('<tr>' + ''.join('<td>%s</td>' % E(c) for c in r) + '</tr>')
    o.append('</tbody></table></div>')
    return ''.join(o)


def sec(sid, eyebrow, title, lead, body="", cls="introsec"):
    return ('<section class="sec %s" id="%s"><div class="eyebrow">%s</div><h2>%s</h2>'
            '%s%s</section>' % (cls, sid, E(eyebrow), E(title),
                                '<p class="lead">%s</p>' % E(lead) if lead else '', body))


def blocks(bl):
    return ''.join('<div class="blk"><h3>%s</h3><p>%s</p></div>' % (E(a), E(b)) for a, b in bl)


def fig_timeline():
    keys = {"1563", "1560", "1619", "1618–19"}
    rows = ''.join(
        '<div class="tl-row%s"><div class="tl-yr">%s</div><div class="tl-body">'
        '<div class="tl-t">%s</div><div class="tl-d">%s</div></div></div>'
        % (' key' if y in keys else '', E(y), E(t), E(dd)) for y, t, dd in TIMELINE)
    return C.fig("图 · 时间线：从九十五条到合一三信条（红点为直接促成海德堡的三个节点）", rows)


def creed_card(c, kind):
    return ('<div class="card"><div class="lt">%s</div><h3>%s</h3><div class="dt">%s%s</div>'
            '<dl><dt>来历与处境</dt><dd>%s</dd>'
            '<dt>体裁</dt><dd>%s</dd>'
            '<dt>最值得记住的一处</dt><dd class="kq">%s</dd>'
            '<dt>与海德堡的关系</dt><dd>%s</dd>'
            '<dt>须说明的一点</dt><dd>%s</dd></dl></div>'
            % (E(c["latin"]), E(c["name"]), E(c["date"]),
               "　·　" + E(c.get("author", "")) if c.get("author") else "",
               E(c["origin"]), E(c["genre"]), E(c["key"]),
               E(c["hc"]) if c["hc"] != "—" else "本书自身", E(c["note"])))


def render_ld(d):
    k = d["key"]
    qas = ''.join('<div class="qa"><div class="qn">问 %d</div><div class="q">%s</div>'
                  '<p class="a">%s</p></div>' % (n, E(q), E(a)) for n, q, a in d["qas"])
    terms = ''.join('<div class="term"><span class="%s">%s</span><span class="tgloss">%s%s</span></div>'
                    % (cls, E(t), '' if tr == "—" else '<i>%s</i>' % E(tr), E(gl))
                    for cls, t, tr, gl in d["terms"])
    ana = ''.join('<p class="pt"><b>%s。</b>%s</p>' % (E(t), E(x)) for t, x in d["analysis"])
    ang = ''.join('<p class="pt"><b>%s。</b>%s</p>' % (E(t), E(x)) for t, x in d["angles"])
    qn = ("问 %d" % d["qas"][0][0]) if len(d["qas"]) == 1 else ("问 %d–%d" % (d["qas"][0][0], d["qas"][-1][0]))
    s = " ".join([d["title"], d["theme"], d["part"], d["core"], d["logic"], d["memo"],
                  d["caution"], d["context"], d["canon"], d["confess"], d["verses"],
                  " ".join(q + a for _, q, a in d["qas"]),
                  " ".join(t + x for t, x in d["analysis"] + d["angles"]),
                  " ".join(t + tr + gl for _, t, tr, gl in d["terms"]),
                  "主日%d LD%d" % (d["n"], d["n"])])
    return f'''<section class="ld {k}" id="ld{d['n']}" data-n="{d['n']}" data-s="{A(s)}">
<div class="ld-h"><div class="ld-no">{d['n']}</div><div class="ld-ht"><h3>{E(d['title'])}</h3>
<div class="ld-meta"><span>主日 {d['n']}</span><span>{qn}</span><span>{E(d['part'])} · {PL[d['part']]}</span><span>{E(d['theme'])}</span></div></div>
<label class="chk"><input type="checkbox" data-n="{d['n']}">已背熟</label></div>
<div class="ld-b">{qas}
<div class="core">{E(d['core'])}</div>
<div class="field"><div class="logic">{E(d['logic'])}</div></div>
<div class="field"><div class="flab">经文根据</div><p class="vs">{E(d['verses'])}</p></div>
<div class="field"><div class="flab">原文钥词</div><div class="terms">{terms}</div></div>
<div class="field"><div class="flab">真实背景 · 为什么这样写</div><p>{E(d['context'])}</p></div>
<div class="field"><div class="flab">神学剖析</div>{ana}</div>
<div class="field"><div class="flab">正典定位</div><p>{E(d['canon'])}</p></div>
<div class="field"><div class="flab">多视角对照</div>{ang}</div>
<div class="field"><div class="flab">信条互参</div><p class="cf">{E(d['confess'])}</p></div>
<div class="field"><div class="caution">{E(d['caution'])}</div></div>
<div class="field f-memo"><div class="memo">{E(d['memo'])}</div></div></div></section>'''


def build():
    o = io.StringIO(); w = o.write
    w('<!DOCTYPE html><html lang="zh-Hans"><head><meta charset="utf-8">')
    w('<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">')
    w('<meta name="theme-color" content="#1F3864">')
    w('<title>海德堡要理问答 · 52 主日全景解读｜欧陆改革宗</title>')
    w('<meta name="description" content="海德堡要理问答 129 问 52 主日全景解读：时间线、救赎史故事线、圣经神学、圣约神学、'
      '三大普世信经与三项联合信条、地图、思维导图、流程图与背诵系统。">')
    w('<link rel="icon" href="data:image/svg+xml,'
      '%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E'
      '%3Crect width=%2732%27 height=%2732%27 fill=%27%231F3864%27/%3E'
      '%3Ctext x=%2716%27 y=%2723%27 font-size=%2720%27 text-anchor=%27middle%27 fill=%27%23F6F2E8%27%3EH%3C/text%3E%3C/svg%3E">')
    w('<style>%s</style></head><body><div id="prog"></div>' % CSS)

    # topbar
    w('<div class="topbar"><div class="tb">'
      '<button class="btn" id="menuBtn">目录</button>'
      '<button class="btn on" id="tocBtn">目录</button>'
      '<div class="brand">CATECHESIS <b>PALATINA</b> · 1563</div><div class="sp"></div>'
      '<div class="tbs"><input id="q" type="search" placeholder="搜索关键词、问号、主题…" aria-label="搜索"></div>'
      '<button class="btn" id="drillBtn">背诵模式</button>'
      '<button class="btn" id="themeBtn">主题</button>'
      '<button class="btn" id="printBtn">打印</button>'
      '</div></div><div class="scrim"></div>')

    # ---------- sidebar ----------
    NAV_INTRO = [("intro-why", "I", "为什么会有这本要理问答"),
                 ("intro-frame", "II", "跳出框架看骨架"),
                 ("intro-canon", "III", "正典弧线与救赎史故事线"),
                 ("bt-canon", "III·A", "圣经神学：跟随故事"),
                 ("bt-cov", "III·B", "圣约神学：全书的语法"),
                 ("intro-compare", "IV", "三大普世信经与三项联合信条"),
                 ("intro-method", "V", "释经进路：四层读法"),
                 ("intro-map", "VI", "改革宗欧洲：影响流向地图"),
                 ("intro-text", "VII", "文本、版本与要理讲道传统"),
                 ("compass", "VIII", "思维导图与 52 主日罗盘")]
    APPS = [("ap-munus", "A", "基督三职"), ("ap-ordo", "B", "救恩次序与动态链"),
            ("ap-sac", "C", "圣餐四立场"), ("ap-dec", "D", "十诫总表"),
            ("ap-lp", "E", "主祷文六求"), ("ap-keys", "F", "教会纪律流程"),
            ("ap-opp", "G", "对手立场总表"), ("ap-lex", "H", "原文钥词汇编"),
            ("ap-index", "I", "52 主日速查索引"), ("ap-pair", "J", "成对记忆与人生处境"),
            ("ap-memo", "K", "背诵方案 · 口诀 · 数字锚点"), ("ap-quiz", "L", "%d 题交互自测" % len(QUIZ))]

    w('<div class="shell"><nav class="side"><div class="toc">')
    w('<div class="toc-h">总论 · PROLEGOMENA</div>')
    for sid, no, t in NAV_INTRO:
        w('<a href="#%s"><span class="no">%s</span>%s</a>' % (sid, no, E(t)))
    last = None
    for d in LDS:
        if d["part"] != last:
            last = d["part"]
            w('<div class="toc-h">%s · %s</div>' % (E(d["part"]), PL[d["part"]]))
        w('<a href="#ld%d" data-n="%d"><span class="no">%d</span>%s</a>' % (d["n"], d["n"], d["n"], E(d["title"])))
    w('<div class="toc-h">结语 · CONCLUSIO</div>'
      '<a href="#closure"><span class="no">·</span>三重闭环</a>')
    w('<div class="toc-h">附录 · APPENDIX</div>')
    for sid, no, t in APPS:
        w('<a href="#%s"><span class="no">%s</span>%s</a>' % (sid, no, E(t)))
    w('</div></nav><main class="main">')

    # ---------- hero ----------
    w('<header class="hero"><div class="lat">CATECHESIS PALATINA · HEIDELBERGENSIS</div>'
      '<h1>海德堡要理问答</h1><div class="zh">52 主日 · 129 问答 · 全景解读</div><div class="rl"></div>'
      '<p class="ld">这不是一本教义提纲，而是一位牧者在瘟疫、战争与政治恐惧中写给会众的一句回答：'
      '<strong>你活着、你死了，凭什么安然？</strong>'
      '本页按欧陆改革宗正统神学，先从整本圣经的故事线与圣约结构看骨架，再逐主日剖析'
      '前因后果、真实处境、写了什么、如何应用，并以三大普世信经与三项联合信条为坐标。</p>'
      '<div class="stats">')
    for b_, t in [("1563", "海德堡首版"), ("129", "问答"), ("52", "主日"), ("3", "困苦·拯救·感恩"),
                  ("10", "总论专章"), ("12", "附录"), ("%d" % 20, "图表"), ("%d" % len(QUIZ), "自测题")]:
        w('<div><b>%s</b>%s</div>' % (b_, t))
    w('</div></header><div id="sNote" class="lead hidden" style="margin-top:20px"></div>')

    # ---------- 总论 ----------
    s = INTROD["intro-why"]
    w(sec(s["id"], s["eyebrow"], s["title"], s["lead"], blocks(s["blocks"]) + fig_timeline()))

    s = INTROD["intro-frame"]
    w(sec(s["id"], s["eyebrow"], s["title"], s["lead"], blocks(s["blocks"]) + C.triring()))

    s = INTROD["intro-canon"]
    w(sec(s["id"], s["eyebrow"], s["title"], s["lead"],
          blocks(s["blocks"]) + C.storyline() + C.parabola()))

    w(sec(BT_SECTION["id"], BT_SECTION["eyebrow"], BT_SECTION["title"], BT_SECTION["lead"],
          blocks(BT_SECTION["blocks"])
          + C.fig("表 · 预表链条：旧约的影子与新约的实体（含改革宗对预表解经的三条约束）", table(TYPOLOGY))
          + C.fig("表 · 六条正典主题在圣经故事中的推进，与海德堡的落点", table(THEMES))))

    w(sec(CT_SECTION["id"], CT_SECTION["eyebrow"], CT_SECTION["title"], CT_SECTION["lead"],
          blocks(CT_SECTION["blocks"]) + C.covenant_tree()
          + C.fig("表 · 恩典之约的施行阶段：一约，多种施行", table(TABLES["covenant"]))))

    s = INTROD["intro-compare"]
    w(sec(s["id"], s["eyebrow"], "在信条家族中的位置：三大普世信经与三项联合信条", s["lead"],
          C.foundation()
          + '<div class="eyebrow" style="margin-top:28px">三大普世信经 · SYMBOLA OECUMENICA</div>'
          + '<div class="cards">%s</div>' % ''.join(creed_card(c, "e") for c in ECUMENICAL)
          + '<div class="eyebrow" style="margin-top:28px">三项联合信条 · DRIE FORMULIEREN VAN ENIGHEID</div>'
          + '<div class="cards">%s</div>' % ''.join(creed_card(c, "u") for c in UNITY)
          + C.fig("表 · 三段同构：使徒信经的骨架如何贯穿海德堡、比利时信条与多特信经", table(ISOMORPH))
          + C.fig("表 · 家族气质对照：六份文件各自在回答什么问题", table(TEMPER))
          + C.fig("表 · 改革宗信条家族分工", table(TABLES["confessions"]))))

    s = INTROD["intro-method"]
    w(sec(s["id"], s["eyebrow"], s["title"], s["lead"],
          blocks(s["blocks"])
          + C.fig("表 · 律法的三重用途：同一部律法，三种功用", table(TABLES["law_uses"]))))

    w(sec("intro-map", "总论 VI", "改革宗欧洲：海德堡在影响网络中的位置",
          "《海德堡要理问答》不是在真空中写成的。它上承维滕堡的墨兰顿、日内瓦的加尔文与苏黎世的布灵格，"
          "下启埃姆登、多特勒支与德布勒森。把这些城市按真实经纬度摆在一张图上，"
          "宗教改革的人物流向、文献流向与政治压力便一目了然。",
          C.map_europe()
          + '<div class="blk"><h3>三条上游</h3><p>'
          '① 维滕堡—墨兰顿：乌尔西努是墨兰顿的学生，海德堡的条理、温和的语气与教育取向由此而来。'
          '② 日内瓦—加尔文：俄利维亚努曾在日内瓦受学，圣约架构、圣灵论与文体的锋利由此而来。'
          '③ 苏黎世—布灵格：在圣餐论上提供了《第二瑞士信条》一系的支持，使海德堡的表述不至被视为孤立。'
          '</p></div>'
          '<div class="blk"><h3>三条下游</h3><p>'
          '① 低地国家：1563 年经埃姆登流入，1568 年威塞尔会议采纳，1618–19 年多特总会正式列为合一三信条之一。'
          '② 匈牙利与特兰西瓦尼亚：1567 年德布勒森总会采纳，至今仍是匈牙利改革宗教会的标准。'
          '③ 北美与南非：随荷兰移民与差会传出，成为今日全球改革宗教会共用的教理教材。</p></div>'
          '<div class="blk"><h3>压力来源</h3><p>'
          '特伦特（1545–63）在南，其第二十二会期确立弥撒为真实献祭，直接促成第 80 问的加入与加重；'
          '帝国议会在东，1566 年奥格斯堡会议上腓特烈三世以此书自辩而未被定罪；'
          '西班牙军队在西北，低地的改革宗信徒正为同一信仰付出生命。</p></div>'))

    s = INTROD["intro-text"]
    w(sec(s["id"], s["eyebrow"], s["title"], s["lead"], blocks(s["blocks"])))

    # 罗盘
    cells = ''.join('<a class="g52 %s" data-n="%d" href="#ld%d" title="主日%d · %s">%d</a>'
                    % (d["key"], d["n"], d["n"], d["n"], A(d["title"]), d["n"]) for d in LDS)
    leg = ''.join('<span><i style="background:var(--%s)"></i>%s</span>'
                  % ({"总纲": "prologue", "困苦": "misery", "拯救": "deliver", "感恩": "gratitude"}[z], z)
                  for z in ["总纲", "困苦", "拯救", "感恩"])
    w(sec("compass", "总论 VIII", "思维导图与 52 主日罗盘",
          "一年一轮，一主日一问答——这是 1563 年《普法尔茨教会规程》的原始设计，"
          "也是欧陆改革宗要理讲道传统的起点。下图先给出全书的语义结构，再给出可点按跳转的进度罗盘。",
          C.mindmap()
          + C.fig('图 · 52 主日全景罗盘（点按跳转；勾选「已背熟」后变金色，已背 <b id="doneCount">0</b> / 52）',
                  '<div class="grid52">%s</div><div class="legend">%s'
                  '<span><i style="background:var(--brass)"></i>已背熟</span></div>' % (cells, leg))))

    # ---------- 52 主日 ----------
    last = None
    for d in LDS:
        if d["part"] != last:
            last = d["part"]
            desc = {"总纲": "全书的胚胎：一句话包含其余 128 问",
                    "困苦": "问 3–11 · 律法作定罪之镜，量出困苦的深度",
                    "拯救": "问 12–85 · 使徒信经的展开：中保、三一、教会、圣礼",
                    "感恩": "问 86–129 · 十诫作感恩之规，主祷文作感恩之息"}[d["part"]]
            w('<div class="part-div"><div><div class="n">%s</div><h2>%s</h2></div>'
              '<div class="zh">%s</div></div>' % (PL[d["part"]], E(d["part"]), E(desc)))
        w(render_ld(d))

    # ---------- 结语 ----------
    w(sec("closure", "结语", "三重闭环：全书如何收束",
          "一部真正的神学作品必须能自我收束。《海德堡要理问答》同时运行三条回环，并在最后一问把它们一起系紧。",
          '<div class="clos">%s</div>' % ''.join(
              '<div class="c"><b>%s</b><p>%s</p></div>' % (E(t), E(x)) for t, x in CLOSURES),
          cls="appsec"))

    # ---------- 附录 ----------
    def ap(sid, eyebrow, title, lead, body):
        w(sec(sid, eyebrow, title, lead, body, cls="appsec"))

    ap("ap-munus", "附录 A", "基督三职与信徒的受膏",
       "munus triplex 不是三种角色，而是教会存在形态的模板：祂受膏，我们有分于祂的受膏。",
       table(TABLES["munus"]))
    ap("ap-ordo", "附录 B", "救恩次序：分布表与动态链",
       "海德堡不以体系顺序陈述救恩次序，却把每一环节都安置在牧养语境中——这正是它与教义学教科书的分别。",
       table(TABLES["ordo"]) + C.ordo_flow())
    ap("ap-sac", "附录 C", "圣餐四立场对照",
       "分歧的关键不在「是否真实临在」，而在「以何方式临在」——归根到底是基督人性在何处的问题（问 47–48）。",
       table(TABLES["sacrament"]))
    ap("ap-dec", "附录 D", "十诫总表（正面所命 · 反面所禁）",
       "海德堡采用加尔文式 4+6 分法，并对每条诫命同时给出禁令与积极要求（《要义》II.8.8 的解经原则）。",
       table(TABLES["decalogue"]))
    ap("ap-lp", "附录 E", "主祷文六求总表",
       "前三求向神（名、国、旨意），后三求为己（饼、赦、保守）。次序即神学：神的荣耀先于我的需要。",
       table(TABLES["lords_prayer"]))
    ap("ap-keys", "附录 F", "天国钥匙：教会纪律流程",
       "第二把钥匙的运作有明确程序，其终点是复纳而非排除。", C.keys_flow())
    ap("ap-opp", "附录 G", "对手立场总表：每一处措辞加重的理由",
       "凡要理问答写得格外精细或格外强硬之处，背后几乎都站着一个具体的对手。找到对手，就找到了措辞的理由。",
       table(TABLES["opponents"]))

    # 钥词汇编
    order = {"hb": 0, "gk": 1, "ltn": 2}
    buckets = {"hb": [], "gk": [], "ltn": []}
    seen = set()
    for d in LDS:
        for cls, t, tr, gl in d["terms"]:
            if (t, tr) in seen: continue
            seen.add((t, tr)); buckets[cls].append((t, tr, gl, d["n"]))
    def gb(items, title):
        rows = ''.join('<div class="term"><span class="%s">%s</span><span class="tgloss">%s%s　'
                       '<a href="#ld%d">主日 %d</a></span></div>'
                       % (cls, E(t), '' if tr == "—" else '<i>%s</i>' % E(tr), E(gl), n, n)
                       for (t, tr, gl, n), cls in [(x, k) for k, v in [(title[1], items)] for x in v])
        return ('<div class="flab" style="margin-top:22px">%s（%d 条）</div><div class="terms">%s</div>'
                % (title[0], len(items), rows))
    lex = (gb(buckets["hb"], ("希伯来文 · עִבְרִית", "hb"))
           + gb(buckets["gk"], ("希腊文 · Ἑλληνική", "gk"))
           + gb(buckets["ltn"], ("拉丁术语 · Termini Latini", "ltn")))
    ap("ap-lex", "附录 H", "原文钥词汇编",
       "要理问答虽以德文写成，其神学判断却常系于一个希伯来文或希腊文的词。以下按语种汇集，附出处主日。", lex)

    ap("ap-index", "附录 I", "52 主日速查索引：一句话看全书",
       "把 52 个「本质核心」并排读一遍，全书的论证走向便一览无余——复习时最有效率的一页。",
       table(TABLES["index52"]))

    ap("ap-pair", "附录 J", "成对记忆与人生处境索引",
       "海德堡极爱成对陈述，成对记忆效率最高；而真正用得上它的时刻，往往是人生的某个具体处境。",
       table(PAIRS) + C.fig("表 · 人生处境索引：此刻该翻到哪一问", table(PASTORAL)))

    mn = ''.join('<div class="mn"><div class="k">%s</div><div class="v">%s</div>'
                 '<div class="d">%s</div></div>' % (E(a), E(b), E(c)) for a, b, c in MNEMONICS)
    anch = ''.join('<div class="an"><b>%s</b><span>%s</span></div>' % (E(a), E(b)) for a, b in ANCHORS)
    tips = ''.join('<div class="t"><b>%s</b>%s</div>' % (E(a), E(b)) for a, b in MEMO_TIPS)
    ap("ap-memo", "附录 K", "背诵方案 · 口诀 · 数字锚点",
       "要理问答本为背诵而设。配合顶部的「背诵模式」（遮盖答案、点按逐问自测）与罗盘进度，可按下列方案推进。",
       table(TABLES["memo_plans"])
       + '<div class="flab" style="margin-top:24px">八组口诀</div><div class="mnem">%s</div>' % mn
       + '<div class="flab" style="margin-top:24px">数字锚点</div><div class="anch">%s</div>' % anch
       + '<div class="flab" style="margin-top:24px">五种记忆法</div><div class="tip">%s</div>' % tips)

    # quiz（定种子打乱选项，避免正解位置偏移）
    rnd = random.Random(20260919)
    qz = []
    for i, (qt, opts, ans, ex, ld) in enumerate(QUIZ, 1):
        pairs = list(enumerate(opts))
        rnd.shuffle(pairs)
        new_ans = [j for j, (orig, _) in enumerate(pairs) if orig == ans][0]
        ops = ''.join('<label class="opt"><input type="radio" name="qz%d" value="%d">%s</label>'
                      % (i, j, E(txt)) for j, (_, txt) in enumerate(pairs))
        qz.append('<div class="qz" data-a="%d" data-i="%d"><div class="qt"><i>%02d</i>%s</div>%s'
                  '<div class="ex">%s　<a href="#ld%d">→ 主日 %d</a></div></div>'
                  % (new_ans, i, i, E(qt), ops, E(ex), ld, ld))
    ap("ap-quiz", "附录 L", "%d 题交互自测" % len(QUIZ),
       "覆盖全书三部分的关键判断。答完点「评分」，系统会标出正解、列出错题并给出解析与跳转链接。",
       '<div class="qbar"><button class="btn" id="gradeBtn">评分</button>'
       '<button class="btn" id="resetBtn">重做</button><span id="score"></span></div>'
       '<div class="quiz">%s</div>' % ''.join(qz))

    # ---------- footer ----------
    w('<div class="foot">《海德堡要理问答》1563 年首版，普法尔茨选侯腓特烈三世颁行，'
      '乌尔西努与俄利维亚努主笔，1619 年多特总会审订，列为欧陆改革宗「合一三信条」之一。<br>'
      '本页问答文字为便于诵读与理解所作的简明中译；解读部分依欧陆改革宗正统神学立场撰写，'
      '供讲道预备、要理教育与个人背诵之用。正式引用与教会公用，请以贵会所采纳的标准中译本为准。<br>'
      'BC＝比利时信条　CoD＝多特信经　WCF＝威斯敏斯特信条　WSC/WLC＝威斯敏斯特小／大要理问答<br><br>'
      'SOLI DEO GLORIA</div>')
    w('</main></div><button id="tocOpen">目录</button>'
      '<button id="toTop" aria-label="回到顶部">↑</button>')
    w('<script>%s</script></body></html>' % JS)
    return o.getvalue()


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "index.html")
    h = build()
    open(out, "w", encoding="utf-8").write(h)
    print("bytes:", len(h.encode("utf-8")), "->", out)
