# -*- coding: utf-8 -*-
"""全部手绘 SVG 图：CSS 变量着色，双主题自适应，prefers-reduced-motion 降级"""
import math

def fig(cap, body, cls=""):
    return ('<figure class="%s"><figcaption>%s</figcaption>%s</figure>' % (cls, cap, body))

# ══════════════════════ 1. 改革宗欧洲地图 ══════════════════════
LON0, LAT0, SX, SY = -7.0, 57.5, 27.0, 30.0
def P(lat, lon):
    return ((lon - LON0) * SX + 30, (LAT0 - lat) * SY + 26)

CITIES = [
    ("维滕堡", "Wittenberg", 51.87, 12.65, "1517 九十五条", "w"),
    ("苏黎世", "Zürich", 47.37, 8.54, "慈运理／布灵格", "z"),
    ("日内瓦", "Genève", 46.20, 6.14, "加尔文；俄利维亚努受学", "g"),
    ("斯特拉斯堡", "Strasbourg", 48.58, 7.75, "布塞珥；加尔文流寓", ""),
    ("巴塞尔", "Basel", 47.56, 7.59, "厄科兰帕迪乌斯；印刷中心", ""),
    ("海德堡", "Heidelberg", 49.41, 8.69, "1563 要理问答", "hd"),
    ("埃姆登", "Emden", 53.37, 7.21, "1571 会议：低地教会母会", ""),
    ("多特勒支", "Dordrecht", 51.81, 4.67, "1618–19 多特总会", "dt"),
    ("安特卫普", "Antwerpen", 51.22, 4.40, "1561 比利时信条投书", ""),
    ("威斯敏斯特", "Westminster", 51.50, -0.13, "1643–49 威敏标准", ""),
    ("爱丁堡", "Edinburgh", 55.95, -3.19, "诺克斯；苏格兰长老宗", ""),
    ("德布勒森", "Debrecen", 47.53, 21.63, "匈牙利改革宗采纳 HC", ""),
    ("特伦特", "Trento", 46.07, 11.12, "1545–63 特伦特会议", "tr"),
    ("罗马", "Roma", 41.90, 12.50, "教廷", ""),
]

FLOWS = [
    ("Wittenberg", "Heidelberg", "墨兰顿 → 乌尔西努", 1),
    ("Genève", "Heidelberg", "加尔文 → 俄利维亚努", -1),
    ("Zürich", "Heidelberg", "布灵格的支持", -1),
    ("Heidelberg", "Emden", "1563 → 低地", 1),
    ("Emden", "Dordrecht", "1571 → 1618", 1),
    ("Heidelberg", "Debrecen", "1567 匈牙利采纳", -1),
    ("Antwerpen", "Dordrecht", "比利时信条并列审订", -1),
]

def map_europe():
    idx = {c[1]: c for c in CITIES}
    o = ['<svg viewBox="0 0 900 585" class="svgfig map" role="img" '
         'aria-label="十六世纪改革宗欧洲影响流向示意图">']
    # graticule
    for lon in range(-5, 25, 5):
        x = P(50, lon)[0]
        o.append('<line x1="%.0f" y1="20" x2="%.0f" y2="560" class="grat"/>' % (x, x))
        o.append('<text x="%.0f" y="576" class="grat-l" text-anchor="middle">%d°E</text>' % (x, lon))
    for lat in range(42, 58, 3):
        y = P(lat, 0)[1]
        o.append('<line x1="24" y1="%.0f" x2="876" y2="%.0f" class="grat"/>' % (y, y))
        o.append('<text x="10" y="%.0f" class="grat-l">%d°N</text>' % (y + 4, lat))
    # 区域示意
    regions = [
        ("神圣罗马帝国", 50.6, 11.5, 300, 190),
        ("低地十七省", 51.9, 5.0, 120, 76),
        ("瑞士邦联", 46.9, 8.0, 118, 58),
        ("不列颠", 53.6, -2.2, 132, 130),
        ("法兰西", 47.2, 2.2, 150, 150),
        ("匈牙利", 47.4, 20.5, 118, 62),
        ("意大利", 44.0, 11.8, 108, 150),
    ]
    for name, la, lo, w, hh in regions:
        x, y = P(la, lo)
        o.append('<rect class="region" x="%.0f" y="%.0f" width="%d" height="%d" rx="28"/>'
                 % (x - w / 2, y - hh / 2, w, hh))
        o.append('<text class="region-l" x="%.0f" y="%.0f" text-anchor="middle">%s</text>'
                 % (x, y - hh / 2 + 18, name))
    # 影响流向
    for a, b, lab, side in FLOWS:
        (x1, y1), (x2, y2) = P(idx[a][2], idx[a][3]), P(idx[b][2], idx[b][3])
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        cx, cy = mx - dy / L * 46 * side, my + dx / L * 46 * side
        o.append('<path class="flow" d="M%.0f %.0f Q%.0f %.0f %.0f %.0f"/>' % (x1, y1, cx, cy, x2, y2))
        tx, ty = (x1 + 2 * cx + x2) / 4, (y1 + 2 * cy + y2) / 4
        o.append('<text class="flow-l" x="%.0f" y="%.0f" text-anchor="middle">%s</text>' % (tx, ty - 5, lab))
    # 城市
    for zh, en, la, lo, note, tag in CITIES:
        x, y = P(la, lo)
        big = tag in ("hd", "dt", "w", "g", "tr")
        o.append('<circle class="node%s" cx="%.0f" cy="%.0f" r="%d"/>'
                 % (" node-key" if tag == "hd" else ("" if not big else " node-big"), x, y, 8 if tag == "hd" else (6 if big else 4)))
        if tag == "hd":
            o.append('<circle class="pulse" cx="%.0f" cy="%.0f" r="8"/>' % (x, y))
        anc = "start" if lo < 14 else "end"
        off = 13 if anc == "start" else -13
        o.append('<text class="city" x="%.0f" y="%.0f" text-anchor="%s">%s</text>' % (x + off, y - 1, anc, zh))
        o.append('<text class="city-n" x="%.0f" y="%.0f" text-anchor="%s">%s</text>' % (x + off, y + 13, anc, note))
    o.append('</svg>')
    return fig("图 · 改革宗欧洲：海德堡在影响网络中的位置（按真实经纬度定位的示意图；虚线为人物与文献的流向）",
               ''.join(o))

# ══════════════════════ 2. 救赎史故事线（八幕）══════════════════════
ACTS = [
    ("一", "创造", "创 1–2", "照形像造人，有真理的仁义与圣洁", "问 6, 26", "a1"),
    ("二", "堕落", "创 3", "悖逆、咒诅、被逐；同时听见第一个福音", "问 7–11, 19", "a2"),
    ("三", "应许", "创 12–50", "亚伯拉罕之约：后裔、地土、万国之福", "问 19, 74", "a3"),
    ("四", "出埃及与律法", "出 1–40", "先救赎，后颁律；会幕中神与人同住", "问 92, 103", "a4"),
    ("五", "王国与先知", "撒下 7；耶 31", "永远的国位；新约的应许：律法写在心上", "问 31, 56", "a5"),
    ("六", "成全", "路 1–约 20", "道成肉身、受苦、复活、升天", "问 35–49", "a6"),
    ("七", "教会", "徒 2–启 3", "圣灵浇灌，从万民中召聚保守的会众", "问 53–85", "a7"),
    ("八", "新创造", "启 21–22", "神与人同住，成为万有中的主", "问 52, 57–58, 123", "a8"),
]

def storyline():
    rows = []
    for no, name, ref, gist, hc, cid in ACTS:
        rows.append(
            '<div class="act %s"><div class="act-n">第%s幕</div>'
            '<div class="act-t">%s</div><div class="act-r">%s</div>'
            '<div class="act-g">%s</div><div class="act-h">%s</div></div>' % (cid, no, name, ref, gist, hc))
    return fig("图 · 救赎历史故事线：八幕圣经剧与海德堡的落点",
               '<div class="acts">%s</div>'
               '<p class="fnote">海德堡只在第一、二、六、七、八幕直接发言，'
               '第三至五幕则以「福音自乐园即开始、藉族长先知传扬、以献祭礼仪预表」一句总括（问 19）——'
               '这是它对旧约最重要的一句表态：旧约不是律法的时代，而是同一福音的早期施行。</p>' % ''.join(rows))

# ══════════════════════ 3. 圣约树 ══════════════════════
def covenant_tree():
    o = ['<svg viewBox="0 0 900 470" class="svgfig" role="img" aria-label="圣约神学结构图">']
    def box(x, y, w, hh, t1, t2, cls, anchor=None):
        s = ['<rect class="cbox %s" x="%d" y="%d" width="%d" height="%d" rx="4"/>' % (cls, x, y, w, hh)]
        s.append('<text class="cbox-t" x="%d" y="%d" text-anchor="middle">%s</text>' % (x + w // 2, y + 24, t1))
        if t2:
            s.append('<text class="cbox-s" x="%d" y="%d" text-anchor="middle">%s</text>' % (x + w // 2, y + 44, t2))
        return ''.join(s)
    o.append(box(300, 16, 300, 58, "救赎之约 pactum salutis", "永恒中父与子的约定（约 17:4–6；诗 110）", "c0"))
    o.append('<path class="carrow" d="M450 74 L450 106"/>')
    o.append(box(70, 106, 320, 58, "行为之约 foedus operum", "亚当为全人类的元首（创 2:17；罗 5:12）", "c1"))
    o.append(box(510, 106, 320, 58, "恩典之约 foedus gratiae", "基督为选民的元首（创 3:15；罗 5:18–19）", "c2"))
    o.append('<path class="carrow" d="M450 74 L230 100 M450 74 L670 100"/>')
    o.append('<text class="clab" x="250" y="188">违背 → 咒诅、死、全然败坏（问 7–11）</text>')
    o.append('<text class="clab" x="560" y="188">成全 → 主动顺服与被动顺服（问 37, 60）</text>')
    o.append('<path class="carrow dash" d="M230 196 Q450 226 660 200"/>')
    o.append('<text class="clab mid" x="450" y="232" text-anchor="middle">第二亚当承担第一亚当所欠（林前 15:22, 45）</text>')
    adms = [("亚伯拉罕", "创 17", "割礼"), ("摩西", "出 19–24", "逾越节"),
            ("大卫", "撒下 7", "王权"), ("新约", "耶 31", "洗礼／圣餐")]
    x = 90
    for name, ref, sign in adms:
        o.append(box(x, 266, 172, 62, name, ref + " · " + sign, "c3"))
        if x > 90:
            o.append('<path class="carrow" d="M%d 297 L%d 297"/>' % (x - 18, x - 2))
        x += 190
    o.append('<text class="clab mid" x="450" y="356" text-anchor="middle">'
             '一个实质（substantia），多种施行（administrationes）——同一位中保、同一种信心、同一份产业</text>')
    o.append('<path class="carrow" d="M450 366 L450 396"/>')
    o.append(box(280, 396, 340, 58, "圣约公式", "「我要作你的神，你要作我的子民」→ 问 26「我的神与我的父」", "c4"))
    o.append('</svg>')
    return fig("图 · 圣约神学结构：海德堡没有一问以「圣约」为题，圣约却是它的语法", ''.join(o))

# ══════════════════════ 4. 52 主日思维导图 ══════════════════════
CLUSTERS = [
    ("总纲", "prologue", [(1, "唯一的安慰")]),
    ("律法之镜", "misery", [(2, "认识困苦"), (3, "创造与堕落"), (4, "公义与怜悯")]),
    ("中保", "deliver", [(5, "必要与资格"), (6, "这中保是谁")]),
    ("信心·三一", "deliver", [(7, "真信心"), (8, "三位一体")]),
    ("圣父·护理", "deliver", [(9, "创造之父"), (10, "护理")]),
    ("圣子·名号", "deliver", [(11, "耶稣"), (12, "基督三职"), (13, "独生子与主")]),
    ("降卑", "deliver", [(14, "道成肉身"), (15, "受苦"), (16, "死与阴间")]),
    ("升高", "deliver", [(17, "复活"), (18, "升天"), (19, "右边与再来")]),
    ("圣灵·教会", "deliver", [(20, "圣灵"), (21, "教会"), (22, "复活永生")]),
    ("称义", "deliver", [(23, "因信称义"), (24, "善行与功德")]),
    ("圣礼", "deliver", [(25, "圣道圣礼"), (26, "洗礼"), (27, "婴儿洗"), (28, "圣餐"), (29, "反变质"), (30, "弥撒与纪律")]),
    ("钥匙", "deliver", [(31, "天国钥匙")]),
    ("感恩之因", "gratitude", [(32, "为何行善"), (33, "真悔改")]),
    ("十诫", "gratitude", [(34, "第一诫"), (35, "第二诫"), (36, "第三诫"), (37, "起誓"), (38, "第四诫"),
                           (39, "第五诫"), (40, "第六诫"), (41, "第七诫"), (42, "第八诫"), (43, "第九诫"), (44, "第十诫")]),
    ("祷告", "gratitude", [(45, "祷告要素"), (46, "天父"), (47, "第一求"), (48, "第二求"), (49, "第三求"),
                           (50, "第四求"), (51, "第五求"), (52, "第六求与阿们")]),
]

def mindmap():
    """横向思维导图（HTML 树），16 个语义簇，避免放射式标签重叠"""
    parts = [("总纲", "prologue", "PROOEMIUM"), ("困苦", "misery", "MISERIA"),
             ("拯救", "deliver", "LIBERATIO"), ("感恩", "gratitude", "GRATITUDO")]
    o = ['<div class="mm"><div class="mm-root"><b>海德堡要理问答</b>'
         '<span>129 问 · 52 主日 · 3 部分 · 16 个语义簇</span></div>']
    for zh, key, la in parts:
        cls = [c for c in CLUSTERS if c[1] == key]
        if not cls:
            continue
        o.append('<div class="mm-br %s"><div class="mm-bh"><b>%s</b><i>%s</i>'
                 '<em>%d 簇 · %d 主日</em></div><div class="mm-cls">'
                 % (key, zh, la, len(cls), sum(len(c[2]) for c in cls)))
        for name, k, items in cls:
            chips = ''.join('<a class="chip" href="#ld%d"><b>%d</b>%s</a>' % (n, n, t)
                            for n, t in items)
            o.append('<div class="mm-cl"><div class="mm-cn">%s</div>'
                     '<div class="mm-chips">%s</div></div>' % (name, chips))
        o.append('</div></div>')
    o.append('</div>')
    return fig("图 · 52 主日思维导图：三大分支、十六个语义簇（点按任一主日直接跳转）",
               ''.join(o) +
               '<p class="fnote">注意「拯救」一支独占十簇：从中保的必要一路走到天国的钥匙，'
               '完全按使徒信经的次序展开。这一支的长度本身就是海德堡的神学宣告——'
               '认识罪只需一簇，认识基督需要十簇。</p>')

# ══════════════════════ 5. 救恩次序流程链 ══════════════════════
ORDO_FLOW = [
    ("永恒", "拣选 electio", "问 54", "神子从起初到末了为自己拣选"),
    ("圣灵", "有效呼召 vocatio", "问 65", "藉福音的宣讲在心里作工"),
    ("圣灵", "重生 regeneratio", "问 8", "非借神的灵重生，则无行善之能"),
    ("人", "信心 fides", "问 21", "确知的知识＋坚定的信靠"),
    ("法庭", "称义 iustificatio", "问 60", "如同从未犯罪，如同亲自守全"),
    ("生命", "成圣 sanctificatio", "问 86", "按祂形像更新；老我死、新我活"),
    ("护卫", "坚忍 perseverantia", "问 1, 127", "一根头发也不能掉落；直到完全得胜"),
    ("终局", "得荣 glorificatio", "问 58", "今生已尝开端，来世完全"),
]

def ordo_flow():
    o = ['<div class="chain">']
    for i, (who, name, ref, gist) in enumerate(ORDO_FLOW):
        o.append('<div class="ch" style="--i:%d"><div class="ch-who">%s</div>'
                 '<div class="ch-n">%s</div><div class="ch-r">%s</div>'
                 '<div class="ch-g">%s</div></div>' % (i, who, name, ref, gist))
        if i < len(ORDO_FLOW) - 1:
            o.append('<div class="ch-a" style="--i:%d">↓</div>' % i)
    o.append('</div>')
    return fig("图 · 救恩次序动态链：注意「谁在动作」——八环中只有一环的主语是人，而那一环本身也是圣灵所作成的（问 65）",
               ''.join(o))

# ══════════════════════ 6. 降卑—升高抛物线 ══════════════════════
PARA = [("道成肉身", 14, 0.06), ("受苦", 15, 0.36), ("被定罪", 15, 0.52),
        ("十架咒诅", 15, 0.72), ("死与埋葬", 16, 0.94), ("地狱之苦", 16, 1.00),
        ("复活", 17, 0.70), ("升天", 18, 0.34), ("坐右边", 19, 0.10), ("再来审判", 19, 0.0)]

def parabola():
    W, H = 900, 330
    o = ['<svg viewBox="0 0 %d %d" class="svgfig" role="img" aria-label="基督降卑与升高抛物线">' % (W, H)]
    pts = []
    for i, (name, ld, depth) in enumerate(PARA):
        x = 70 + i * (W - 150) / (len(PARA) - 1)
        y = 60 + depth * 200
        pts.append((x, y, name, ld))
    d = "M%.0f %.0f " % (pts[0][0], pts[0][1]) + " ".join(
        "L%.0f %.0f" % (p[0], p[1]) for p in pts[1:])
    o.append('<line class="axis" x1="40" y1="60" x2="870" y2="60"/>')
    o.append('<text class="axis-l" x="40" y="50">升高 exaltatio</text>')
    o.append('<line class="axis" x1="40" y1="268" x2="870" y2="268"/>')
    o.append('<text class="axis-l" x="40" y="288">降卑 humiliatio</text>')
    o.append('<path class="para" d="%s"/>' % d)
    for x, y, name, ld in pts:
        o.append('<circle class="pnode" cx="%.0f" cy="%.0f" r="5"/>' % (x, y))
        up = y > 160
        o.append('<text class="pt-l" x="%.0f" y="%.0f" text-anchor="middle">%s</text>'
                 % (x, y + (22 if up else -14), name))
        o.append('<text class="pt-s" x="%.0f" y="%.0f" text-anchor="middle">主日 %d</text>'
                 % (x, y + (36 if up else -28), ld))
    o.append('</svg>')
    return fig("图 · 降卑与升高：信经的基督论段落在海德堡中的曲线（主日 14–19）", ''.join(o))

# ══════════════════════ 7. 天国钥匙流程图 ══════════════════════
KEYS = [("私下劝戒", "太 18:15", "弟兄相待，不声张"),
        ("两三人同去", "太 18:16", "句句都定准"),
        ("告诉教会", "太 18:17", "报告长老团"),
        ("禁领圣礼", "问 82, 85", "护卫圣约与会众"),
        ("逐出团契", "林前 5:13", "神在天上亦如此"),
        ("悔改则复纳", "林后 2:6–8", "纪律的正当终点")]

def keys_flow():
    o = ['<div class="flowh">']
    for i, (t, ref, gist) in enumerate(KEYS):
        cls = "fx-end" if i == len(KEYS) - 1 else ""
        o.append('<div class="fx %s" style="--i:%d"><div class="fx-n">%d</div>'
                 '<div class="fx-t">%s</div><div class="fx-r">%s</div><div class="fx-g">%s</div></div>'
                 % (cls, i, i + 1, t, ref, gist))
    o.append('</div>')
    return fig("图 · 教会纪律流程（第二把钥匙）：六步的终点是复纳，不是排除",
               ''.join(o) + '<p class="fnote">第一把钥匙是讲道（问 84）：向信的人宣告赦罪，向不悔改的人宣告定罪。'
               '两把钥匙同属一个福音，故纪律若脱离讲道即成暴政，讲道若无纪律即成纵容。</p>')

# ══════════════════════ 8. 三层地基 ══════════════════════
def foundation():
    o = ['<svg viewBox="0 0 900 320" class="svgfig" role="img" aria-label="三层权威地基图">']
    layers = [
        (40, 240, 820, 60, "三大普世信经 · 使徒信经／尼西亚信经／亚他那修信经", "全体正统教会共有——三一与基督论的边界", "f1"),
        (110, 160, 680, 60, "三项联合信条 · 比利时信条／海德堡要理问答／多特信经", "欧陆改革宗共有——恩典教义与教会实践", "f2"),
        (190, 80, 520, 60, "地方教会的章程、礼拜规程与教理讲道", "在此二层之上建造", "f3"),
    ]
    for x, y, w, hh, t1, t2, cls in layers:
        o.append('<rect class="fl %s" x="%d" y="%d" width="%d" height="%d" rx="3"/>' % (cls, x, y, w, hh))
        o.append('<text class="fl-t" x="%d" y="%d" text-anchor="middle">%s</text>' % (x + w // 2, y + 26, t1))
        o.append('<text class="fl-s" x="%d" y="%d" text-anchor="middle">%s</text>' % (x + w // 2, y + 46, t2))
    o.append('<text class="fl-n" x="450" y="42" text-anchor="middle">'
             'norma normata（被规范的规范）——之上唯有圣经：norma normans</text>')
    o.append('<line class="axis" x1="40" y1="56" x2="860" y2="56"/>')
    o.append('</svg>')
    return fig("图 · 三层权威地基：争论之前，先问「这是哪一层的分歧」",
               ''.join(o) + '<p class="fnote">三一论的分歧动摇第一层，是正统与异端之别；'
               '圣餐或婴儿洗的分歧属第二层，是宗派之别；礼拜次序与讲道安排属第三层，是自由与智慧之事。'
               '把第三层的分歧当作第一层来争，是教会冲突最常见的病源。</p>')

# ══════════════════════ 9. 三重结构环 ══════════════════════
def triring():
    o = ['<svg viewBox="0 0 900 300" class="svgfig" role="img" aria-label="三重结构与篇幅比例">']
    total, x = 129, 60
    segs = [("困苦 MISERIA", 9, "主日 2–4 · 问 3–11", "seg-m"),
            ("拯救 LIBERATIO", 74, "主日 5–31 · 问 12–85", "seg-d"),
            ("感恩 GRATITUDO", 44, "主日 32–52 · 问 86–129", "seg-g")]
    W = 780
    for name, n, sub, cls in segs:
        w = W * n / total
        o.append('<rect class="%s" x="%.0f" y="80" width="%.0f" height="72" rx="2"/>' % (cls, x, w))
        o.append('<text class="seg-t" x="%.0f" y="112" text-anchor="middle">%s</text>' % (x + w / 2, name))
        o.append('<text class="seg-s" x="%.0f" y="134" text-anchor="middle">%s</text>' % (x + w / 2, sub if w > 150 else ""))
        o.append('<text class="seg-p" x="%.0f" y="170" text-anchor="middle">%d 问 · %d%%</text>'
                 % (x + w / 2, n, round(n / total * 100)))
        x += w
    o.append('<text class="clab mid" x="450" y="44" text-anchor="middle">'
             '罗 7:24 「我真是苦啊！谁能救我脱离这取死的身体呢？」 → 罗 7:25 「感谢神，靠着我们的主耶稣基督就能脱离了。」</text>')
    o.append('<path class="carrow dash" d="M96 200 Q450 262 810 200"/>')
    o.append('<text class="clab mid" x="450" y="282" text-anchor="middle">'
             '十诫在首（问 3–5）作定罪之镜，在尾（问 92–115）作感恩之规——同一部律法，位置决定性质</text>')
    o.append('</svg>')
    return fig("图 · 三重结构与篇幅比例：律法定罪仅占 7%，福音与感恩占 93%", ''.join(o))
