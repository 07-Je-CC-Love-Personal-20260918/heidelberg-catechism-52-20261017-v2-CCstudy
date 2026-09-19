# -*- coding: utf-8 -*-
"""专题图表"""
from charts import fig

# ── 迦克墩四边界 ──────────────────────────────────────────
def chalcedon():
    o = ['<svg viewBox="0 0 900 520" class="svgfig" role="img" aria-label="迦克墩四条边界与四种越界">']
    o.append('<rect class="ch-field" x="230" y="120" width="440" height="280" rx="6"/>')
    o.append('<text class="ch-ct" x="450" y="248" text-anchor="middle">位格的联合</text>')
    o.append('<text class="ch-cs" x="450" y="272" text-anchor="middle">unio personalis</text>')
    o.append('<text class="ch-cs" x="450" y="294" text-anchor="middle">二性一位，不可分离亦不可混同</text>')
    edges = [
        ("不混乱", "ἀσυγχύτως", 450, 108, "middle", "越界：欧迪奇一性论", "人性被神性吞没 → 问 16 落空", 48, 70),
        ("不改变", "ἀτρέπτως", 196, 254, "end", "越界：亚波里拿留", "以道取代理性魂 → 未取用者未得医治", 200, 222),
        ("不分割", "ἀδιαιρέτως", 704, 254, "start", "越界：聂斯托利", "拆成两位 → 问 17 落空", 200, 222),
        ("不离散", "ἀχωρίστως", 450, 424, "middle", "越界：幻影说／嗣子论", "无真死，或无无限的价值", 462, 484),
    ]
    for zh, gk, x, y, anc, err, why, ey, ey2 in edges:
        o.append('<text class="ch-e" x="%d" y="%d" text-anchor="%s">%s</text>' % (x, y, anc, zh))
        o.append('<text class="ch-g" x="%d" y="%d" text-anchor="%s">%s</text>' % (x, y + 17, anc, gk))
        o.append('<text class="ch-x" x="%d" y="%d" text-anchor="%s">%s</text>' % (x, ey, anc, err))
        o.append('<text class="ch-w" x="%d" y="%d" text-anchor="%s">%s</text>' % (x, ey2, anc, why))
    for x1, y1, x2, y2 in [(450, 120, 450, 84), (230, 260, 200, 260), (670, 260, 700, 260), (450, 400, 450, 438)]:
        o.append('<path class="ch-a" d="M%d %d L%d %d"/>' % (x1, y1, x2, y2))
    o.append('<text class="ch-n" x="450" y="504" text-anchor="middle">'
             '海德堡的落点：问 35（不改变·不混乱）· 问 47–48（不分割·不离散）· 问 33（神性的真实）</text>')
    o.append('</svg>')
    return fig("图 · 迦克墩四条边界：四个副词，四种越界，四种救恩的失败", ''.join(o))

# ── 确据三柱 ──────────────────────────────────────────────
def assurance():
    o = ['<svg viewBox="0 0 900 380" class="svgfig" role="img" aria-label="确据的三根柱子">']
    o.append('<rect class="as-top" x="90" y="44" width="720" height="52" rx="3"/>')
    o.append('<text class="as-tt" x="450" y="76" text-anchor="middle">确据 · certitudo salutis（问 1、129）</text>')
    cols = [("① 神的应许", "客观根基", "问 1, 60, 129", "「神白白地、全然出于恩典，将基督完全的补赎、公义与圣洁归给我」", "p1"),
            ("② 圣灵的作证", "内在见证", "问 1, 21, 53", "「祂也借圣灵使我确知有永生」；圣灵在心里作成信心并永远同住", "p2"),
            ("③ 果子的印证", "旁证，非根据", "问 86, 彼后 1:10", "「使我们各人从自己的信心果子上确知自己的信心」", "p3")]
    x = 90
    for t, s, ref, quote, cls in cols:
        o.append('<rect class="as-col %s" x="%d" y="120" width="220" height="180" rx="3"/>' % (cls, x))
        o.append('<text class="as-h" x="%d" y="150" text-anchor="middle">%s</text>' % (x + 110, t))
        o.append('<text class="as-s" x="%d" y="170" text-anchor="middle">%s</text>' % (x + 110, s))
        o.append('<text class="as-r" x="%d" y="190" text-anchor="middle">%s</text>' % (x + 110, ref))
        # 引文折行
        q = quote
        line, lines = "", []
        for ch in q:
            line += ch
            if len(line) >= 13:
                lines.append(line); line = ""
        if line: lines.append(line)
        for i, ln in enumerate(lines[:5]):
            o.append('<text class="as-q" x="%d" y="%d" text-anchor="middle">%s</text>' % (x + 110, 216 + i * 17, ln))
        x += 250
    o.append('<rect class="as-base" x="90" y="316" width="720" height="40" rx="3"/>')
    o.append('<text class="as-b" x="450" y="342" text-anchor="middle">'
             '次序不可倒：应许在先，圣灵在中，果子在后。以果子求确据者，必陷入自我审查的循环。</text>')
    o.append('</svg>')
    return fig("图 · 确据的三根柱子与它们不可颠倒的次序", ''.join(o))

# ── 圣餐：基督人性所在 ─────────────────────────────────────
def supper_space():
    o = ['<svg viewBox="0 0 900 420" class="svgfig" role="img" aria-label="四种圣餐论中基督人性的位置">']
    o.append('<line class="axis" x1="60" y1="96" x2="840" y2="96"/>')
    o.append('<text class="sp-z" x="60" y="86">天上 · 父的右边（徒 3:21）</text>')
    o.append('<line class="axis" x1="60" y1="330" x2="840" y2="330"/>')
    o.append('<text class="sp-z" x="60" y="352">地上 · 桌前的饼与杯</text>')
    views = [("罗马", "质变：饼酒的实体变为身体", "down", "sv-r"),
             ("路德宗", "人性无所不在，与饼酒同在", "both", "sv-l"),
             ("记念说", "人性只在天上，饼酒纯为记号", "none", "sv-z"),
             ("改革宗", "人性在天上，圣灵把我们举上去", "up", "sv-c")]
    x = 110
    for name, gist, arrow, cls in views:
        o.append('<rect class="sv %s" x="%d" y="110" width="170" height="210" rx="4"/>' % (cls, x))
        o.append('<text class="sv-t" x="%d" y="136" text-anchor="middle">%s</text>' % (x + 85, name))
        cx = x + 85
        if arrow == "down":
            o.append('<path class="sv-a" d="M%d 156 L%d 296"/>' % (cx, cx))
            o.append('<circle class="sv-n" cx="%d" cy="300" r="8"/>' % cx)
            o.append('<text class="sv-lb" x="%d" y="182" text-anchor="middle">基督降到饼中</text>' % cx)
        elif arrow == "both":
            o.append('<path class="sv-a" d="M%d 156 L%d 296"/>' % (cx, cx))
            o.append('<circle class="sv-n" cx="%d" cy="160" r="8"/>' % cx)
            o.append('<circle class="sv-n" cx="%d" cy="300" r="8"/>' % cx)
            o.append('<text class="sv-lb" x="%d" y="200" text-anchor="middle">人性无所不在</text>' % cx)
        elif arrow == "none":
            o.append('<circle class="sv-n" cx="%d" cy="160" r="8"/>' % cx)
            o.append('<text class="sv-lb" x="%d" y="200" text-anchor="middle">天地之间无往来</text>' % cx)
        else:
            o.append('<path class="sv-a up" d="M%d 296 L%d 160"/>' % (cx, cx))
            o.append('<circle class="sv-n" cx="%d" cy="160" r="8"/>' % cx)
            o.append('<text class="sv-lb" x="%d" y="200" text-anchor="middle">圣灵举我们上去</text>' % cx)
            o.append('<text class="sv-lb" x="%d" y="218" text-anchor="middle">sursum corda</text>' % cx)
        # gist 折行
        line, lines = "", []
        for ch in gist:
            line += ch
            if len(line) >= 10:
                lines.append(line); line = ""
        if line: lines.append(line)
        for i, ln in enumerate(lines[:4]):
            o.append('<text class="sv-g" x="%d" y="%d" text-anchor="middle">%s</text>' % (cx, 246 + i * 16, ln))
        x += 190
    o.append('<text class="ch-n" x="450" y="392" text-anchor="middle">'
             '争的从来不是「是否临在」，而是「人性在哪里」——问 47–48 一旦定下，问 75–80 的每一句都随之确定</text>')
    o.append('</svg>')
    return fig("图 · 四种圣餐论的空间结构：基督的人性现在在哪里", ''.join(o))

SUPPER_TL = [
 ("1524", "慈运理与路德书信交锋", "「这是我的身体」当作字面还是转喻"),
 ("1529", "马尔堡会谈", "十五条中十四条达成一致，第十五条（圣餐）破裂"),
 ("1536", "维滕堡协议", "南德城市与路德暂时妥协，未及瑞士"),
 ("1549", "苏黎世共识", "加尔文与布灵格达成一致，改革宗立场定型"),
 ("1551", "韦斯特法尔论战", "路德宗正统派全面攻击加尔文派"),
 ("1560", "海德堡圣餐之争", "赫斯胡斯与克莱布茨当众抢夺圣器，腓特烈三世罢免双方"),
 ("1562", "特伦特第二十二会期", "确立弥撒为真实的赎罪祭，并咒诅否认者"),
 ("1563", "《海德堡要理问答》", "问 75–82 成形；第二版加入第 80 问，第三版加重措辞"),
 ("1577", "《协同式》", "路德宗正式确立属性相通与人性无所不在"),
 ("1619", "多特总会", "审订海德堡，宣告与神的话完全相符"),
]

def supper_timeline():
    rows = ''.join(
        '<div class="tl-row%s"><div class="tl-yr">%s</div><div class="tl-body">'
        '<div class="tl-t">%s</div><div class="tl-d">%s</div></div></div>'
        % (' key' if y in ("1560", "1562", "1563") else '', y, t, d) for y, t, d in SUPPER_TL)
    return fig("图 · 圣餐论战时间线：海德堡问 75–82 写于这场论战的第四十年", rows)

# ── 使徒信经 ⇄ 海德堡 对应弦图 ─────────────────────────────
CREED_MAP = [
 ("我信上帝，全能的父，创造天地的主", "9–10", "问 26–28"),
 ("我信我主耶稣基督，上帝的独生子", "11–13", "问 29–34"),
 ("因圣灵感孕，由童贞女马利亚所生", "14", "问 35–36"),
 ("在本丢彼拉多手下受难，被钉十架，受死，埋葬", "15–16", "问 37–43"),
 ("祂降在阴间", "16", "问 44"),
 ("第三天从死里复活", "17", "问 45"),
 ("升天，坐在全能父上帝的右边", "18–19", "问 46–51"),
 ("将来必从那里降临，审判活人死人", "19", "问 52"),
 ("我信圣灵", "20", "问 53"),
 ("我信圣而公之教会，圣徒相通", "21", "问 54–55"),
 ("我信罪得赦免", "21, 23", "问 56, 59–61"),
 ("身体复活，并且永生", "22", "问 57–58"),
]

def creed_chord():
    n = len(CREED_MAP)
    H = 60 + n * 38
    o = ['<svg viewBox="0 0 900 %d" class="svgfig" role="img" aria-label="使徒信经条目与海德堡主日的对应">' % H]
    o.append('<text class="cm-h" x="30" y="30">使徒信经 · 十二条目</text>')
    o.append('<text class="cm-h" x="700" y="30">海德堡 · 主日／问</text>')
    for i, (art, lds, qs) in enumerate(CREED_MAP):
        y = 60 + i * 38
        o.append('<text class="cm-a" x="30" y="%d">%s</text>' % (y + 5, art))
        o.append('<circle class="cm-n l" cx="560" cy="%d" r="4"/>' % y)
        o.append('<circle class="cm-n r" cx="676" cy="%d" r="4"/>' % y)
        o.append('<path class="cm-l" d="M560 %d C610 %d 626 %d 676 %d"/>' % (y, y, y, y))
        o.append('<text class="cm-b" x="700" y="%d">主日 %s　<tspan class="cm-q">%s</tspan></text>' % (y + 5, lds, qs))
    o.append('<line class="axis" x1="560" y1="46" x2="560" y2="%d"/>' % (60 + (n - 1) * 38 + 14))
    o.append('</svg>')
    return fig("图 · 使徒信经十二条目与海德堡主日的逐条对应：第二部分的骨架完全由信经支配", ''.join(o))

# ── 每主日问答数分布 ───────────────────────────────────────
def qa_bars(LDS):
    PARTC = {"总纲": "prologue", "困苦": "misery", "拯救": "deliver", "感恩": "gratitude"}
    W, H = 900, 250
    bw = (W - 80) / 52
    o = ['<svg viewBox="0 0 %d %d" class="svgfig" role="img" aria-label="每主日问答数量分布">' % (W, H)]
    mx = max(len(d["qas"]) for d in LDS)
    for k in range(1, mx + 1):
        y = 190 - k * (150 / mx)
        o.append('<line class="grat" x1="46" y1="%.0f" x2="880" y2="%.0f"/>' % (y, y))
        o.append('<text class="grat-l" x="34" y="%.0f" text-anchor="end">%d</text>' % (y + 4, k))
    for i, d in enumerate(LDS):
        c = len(d["qas"])
        h = c * (150 / mx)
        x = 50 + i * bw
        o.append('<rect class="qb %s" x="%.1f" y="%.1f" width="%.1f" height="%.1f">'
                 '<title>主日 %d · %s · %d 问</title></rect>'
                 % (PARTC[d["part"]], x, 190 - h, bw - 2.5, h, d["n"], d["title"], c))
        if d["n"] % 5 == 0 or d["n"] == 1:
            o.append('<text class="qb-l" x="%.1f" y="206" text-anchor="middle">%d</text>' % (x + bw / 2 - 1, d["n"]))
    o.append('<text class="ch-n" x="450" y="232" text-anchor="middle">'
             '唯一的五问峰值在主日 16（死、埋葬、降在阴间）；四问的八处集中在中保、信心、升天、圣礼、悔改、'
             '第一诫与祷告——海德堡说得最多的地方，正是历史上争得最凶的地方</text>')
    o.append('</svg>')
    return fig("图 · 52 主日的问答密度分布：哪几处海德堡说得最多", ''.join(o))

# ── 德文钥词 ───────────────────────────────────────────────
def german_cards(words):
    cards = ''.join(
        '<div class="gw"><div class="gw-w">%s</div><div class="gw-z">%s</div>'
        '<div class="gw-r">%s</div><div class="gw-d">%s</div></div>' % (w, z, r, d)
        for w, z, r, d in words)
    return fig("图 · 德文钥词六则：海德堡的分量常常压在一个词上",
               '<div class="gws">%s</div>' % cards)
