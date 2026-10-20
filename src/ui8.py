# -*- coding: utf-8 -*-
"""v8：六色主题词记忆标记（字色 + 底纹 + 下划线多重编码）· 经文引用标记 · 图例 · 开关"""
import re

CATS = [
    ("mk-god", "🔺", "神 · 三一 · 主权", ["三位一体", "三一", "圣父", "天父", "护理", "主权", "拣选", "预定", "创造主", "独一真神", "全能"]),
    ("mk-sin", "🪞", "罪 · 律法 · 审判", ["罪债", "罪恶", "原罪", "败坏", "堕落", "咒诅", "定罪", "愁苦", "困苦", "律法", "审判", "魔鬼", "地狱", "死亡", "行为之约"]),
    ("mk-chr", "✝️", "基督 · 拯救 · 恩典", ["耶稣基督", "基督", "中保", "十字架", "十架", "宝血", "救赎", "赎价", "挽回", "称义", "恩典", "复活", "升天", "道成肉身", "替代"]),
    ("mk-spi", "🔥", "圣灵 · 信心 · 圣礼", ["圣灵", "真信心", "信心", "确据", "安慰", "圣礼", "洗礼", "圣餐", "印证", "重生"]),
    ("mk-cov", "🤝", "圣约 · 教会 · 国度", ["恩典之约", "圣约", "教会", "圣徒相通", "国度", "天国的钥匙", "钥匙", "选民", "子民"]),
    ("mk-gra", "🙏", "感恩 · 成圣 · 生活", ["感恩", "感谢", "善行", "悔改", "归正", "成圣", "祷告", "十诫", "顺服", "爱邻舍", "安息"]),
]
TERMS = sorted(((w, c) for c, e, n, ws in CATS for w in ws), key=lambda x: -len(x[0]))
RX = re.compile("|".join(re.escape(w) for w, c in TERMS))
CLS = dict(TERMS)
VERSE = re.compile(r'((?:创|出|利|民|申|书|士|得|撒上|撒下|王上|王下|代上|代下|拉|尼|斯|伯|诗|箴|传|歌|赛|耶|哀|结|但|何|珥|摩|俄|拿|弥|鸿|哈|番|该|亚|玛|太|可|路|约|徒|罗|林前|林后|加|弗|腓|西|帖前|帖后|提前|提后|多|门|来|雅|彼前|彼后|约一|约二|约三|约壹|约贰|约叁|犹|启)\s?\d{1,3}:\d{1,3}(?:[–-]\d{1,3})?)')
SKIP = {"script", "style", "svg", "h1", "h2", "h3", "a", "button", "summary", "figcaption", "label", "title", "textarea", "option", "sup", "nav", "header"}
SKIP_CLS = re.compile(r'class="(?:[^"]*\s)?(?:qn|q|vchip|vchips|ld-meta|badge|toc|mw|g52|hm|mapleg|refs|srcnote|cfa|tl|rph|rlat|rtab|eyebrow|act3|stats|zbtn|qbar|reader|mklegend|fc-[\w-]*|tr-[\w-]*|terms|term|foot)(?=[\s"])')


def _mark_text(t):
    t = VERSE.sub(r'<span class="mk-v">\1</span>', t)
    parts = re.split(r'(<span class="mk-v">.*?</span>)', t)
    out = []
    seen = set()
    for p in parts:
        if p.startswith('<span class="mk-v">'):
            out.append(p)
        else:
            def rep(m, seen=seen):
                w = m.group(0)
                if w in seen:
                    return w
                seen.add(w)
                return '<mark class="mk %s">%s</mark>' % (CLS[w], w)
            out.append(RX.sub(rep, p))
    return ''.join(out)


def mark(html):
    """只处理 <main> 内的正文文本节点；跳过标题、链接、按钮、图、原文问答题干等"""
    i0 = html.index('<main'); i1 = html.index('</main>')
    head, body, tail = html[:i0], html[i0:i1], html[i1:]
    toks = re.split(r'(<[^>]+>)', body)
    stack = []  # 记录被跳过的元素
    out = []
    for tk in toks:
        if tk.startswith('<'):
            m = re.match(r'<(/?)([a-zA-Z0-9]+)', tk)
            if m:
                closing, tag = m.group(1) == '/', m.group(2).lower()
                void = tag in ("br", "img", "input", "hr", "meta", "link", "source", "wbr") or tk.endswith('/>')
                if not closing and not void:
                    skip = tag in SKIP or bool(SKIP_CLS.search(tk))
                    stack.append((tag, skip))
                elif closing:
                    for k in range(len(stack) - 1, -1, -1):
                        if stack[k][0] == tag:
                            del stack[k:]
                            break
            out.append(tk)
        else:
            if tk.strip() and not any(s for _, s in stack):
                out.append(_mark_text(tk))
            else:
                out.append(tk)
    return head + ''.join(out) + tail


def legend():
    chips = ''.join('<span class="mkl">%s <mark class="mk %s">%s</mark></span>' % (e, c, n) for c, e, n, ws in CATS)
    return ('<div class="mklegend glass" id="mkLegend"><b>🎨 颜色记忆法</b>%s'
            '<span class="mkl"><span class="mk-v">罗 8:28</span> 经文</span>'
            '<button class="btn" id="mkBtn" type="button">标记：开</button></div><!--MKSTAT-->' % chips)


CSS8 = r"""
/* ===== v8：主题词记忆标记 ===== */
mark.mk{background:none;color:inherit;padding:0 1px;border-radius:3px;font-weight:600;transition:background .25s,color .25s}
.mk-god{color:#7048C0;background:linear-gradient(transparent 62%,rgba(112,72,192,.16) 62%)!important}

.mk-chr{color:#1D4FBF;background:linear-gradient(transparent 55%,rgba(36,87,197,.17) 55%)!important}
.mk-spi{color:#0B8475;border-bottom:2px dotted rgba(11,148,132,.7)}
.mk-cov{color:#2E7D32;background:rgba(46,125,50,.10)!important;box-shadow:inset 0 -1px 0 rgba(46,125,50,.5)}
.mk-gra{color:#9A5B00;background:linear-gradient(100deg,rgba(255,200,60,.0) 0,rgba(255,200,60,.45) 8%,rgba(255,200,60,.3) 92%,rgba(255,200,60,0) 100%)!important}
:root[data-theme="dark"] .mk-god{color:#C3AEFF}:root[data-theme="dark"] .mk-sin{color:#FF8A98}:root[data-theme="dark"] .mk-chr{color:#9DB8FF}
:root[data-theme="dark"] .mk-spi{color:#5FE0CC}:root[data-theme="dark"] .mk-cov{color:#8FD694}:root[data-theme="dark"] .mk-gra{color:#FFC860}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .mk-god{color:#C3AEFF}:root:not([data-theme="light"]) .mk-sin{color:#FF8A98}
 :root:not([data-theme="light"]) .mk-chr{color:#9DB8FF}:root:not([data-theme="light"]) .mk-spi{color:#5FE0CC}:root:not([data-theme="light"]) .mk-cov{color:#8FD694}:root:not([data-theme="light"]) .mk-gra{color:#FFC860}}
.mk-v{font-family:var(--sans);font-size:.86em;font-weight:600;color:var(--teal);background:color-mix(in srgb,var(--teal) 11%,transparent);border-radius:5px;padding:0 4px;white-space:nowrap}
body.nomark mark.mk{color:inherit!important;background:none!important;text-decoration:none!important;border:0!important;box-shadow:none!important;font-weight:inherit}
body.nomark .mk-v{background:none;color:inherit;font-weight:inherit}
.mklegend{position:relative;display:flex;flex-wrap:wrap;align-items:center;gap:6px 12px;margin:14px 0;padding:8px 14px;
  border:1px solid var(--rule);border-radius:14px;box-shadow:var(--sh);font-size:14px}
.mklegend>b{font-family:var(--sans);font-size:13px}
.mkl{white-space:nowrap}
.mklegend .btn{margin-left:auto;padding:4px 12px;font-size:12.5px}
.mklegend.mini .mkl{display:none}
@media (max-width:760px){.mklegend{position:static}.mklegend .mkl{font-size:13px}}
/* 主日卡片：本质核心关键词放大闪光 */
.kb-core mark.mk{font-size:1.04em}
.ld.v3.in .kb-core mark.mk{animation:mkpop .6s ease both;animation-delay:.5s}
@keyframes mkpop{0%{filter:brightness(1)}40%{filter:brightness(1.35) saturate(1.4)}100%{filter:none}}
"""

JS8 = r"""
(function(){var d=document,b=d.body,btn=d.getElementById('mkBtn');if(!btn)return;var ls;try{ls=localStorage}catch(e){}
function set(off){b.classList.toggle('nomark',off);btn.textContent='标记：'+(off?'关':'开');btn.classList.toggle('on',!off);try{ls&&ls.setItem('hcMark',off?'0':'1')}catch(e){}}
var off=false;try{off=ls&&ls.getItem('hcMark')==='0'}catch(e){}set(off);
btn.onclick=function(){set(!b.classList.contains('nomark'));};
})();
"""
