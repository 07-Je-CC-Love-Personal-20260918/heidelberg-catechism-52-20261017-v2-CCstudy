# -*- coding: utf-8 -*-
"""v4 层：每主日记忆图标 + 一句应用 · 信条互参直链原文 · 三幕动态流程 · 鲜明配色"""
import re
from ui2 import ic, E

# 每主日一个记忆图标（画面钩子）
EMO = ["🕊️", "🪞", "🍎", "⚖️", "🌉", "👑", "🔑", "🔺", "🌍", "🌧️",
       "✝️", "🫒", "👶", "🌟", "🩸", "⚰️", "🌅", "☁️", "⚖️", "🔥",
       "⛪", "🌱", "🧥", "🍇", "📖", "💧", "👪", "🍞", "🍷", "🚫",
       "🗝️", "🌳", "🔄", "1️⃣", "🖼️", "🗣️", "✋", "🕯️", "👨‍👩‍👧", "🛡️",
       "💍", "🤲", "🗨️", "❤️", "🙏", "👨‍👦", "✨", "🏰", "🎯", "🥖",
       "🧾", "🗡️"]

# 每主日一句应用：落到今天的生活
APP = [
 "遇事先问「我属谁」，不先问「我感觉如何」。",
 "每日以神的律法照镜，不以别人作比较的尺。",
 "停止「我本性还好」的自我辩护，承认败坏之深。",
 "不拿神的慈爱抵消祂的公义，十字架两者都成全。",
 "放弃一切自我补偿的宗教努力，只寻求合格的中保。",
 "在痛苦中仰望真神真人的基督，不另找第二个中保。",
 "信心要有内容：能逐句用使徒信经说出你信什么。",
 "敬拜与祷告都要三一：向父、借子、靠圣灵。",
 "物质世界是父的作品，劳动与享受都可献为敬拜。",
 "在疾病、贫穷与失败中说：没有一样是偶然。",
 "不在圣徒、功德或自己里面寻找救恩的另一部分。",
 "以先知、祭司、君王的身份活着：认信、献己、争战。",
 "称呼基督为「主」，就让祂主宰钱包、时间与身体。",
 "基督取了真人性：你的软弱祂体恤，你的身体有尊贵。",
 "被冤枉时记得：无罪者在审判官前被定罪，为了你。",
 "面对死亡不再惧怕：它已从刑罚变成进入永生的门。",
 "复活给今天三样东西：称义、新生命、身体复活的凭据。",
 "心思向上：我们的肉身已在天上，祂的灵在我们里面。",
 "审判日不是威胁而是盼望：审判官就是替你受审者。",
 "确据与成圣都是圣灵的工作，不靠情绪也不靠意志。",
 "委身于一间有纯正讲道、圣礼与劝惩的地方教会。",
 "今天的盼望有身体、有大地：照此看待疾病与环境。",
 "每天回到唯独信心：神看我如同从未犯罪。",
 "行善出于感恩，不为记账；赏赐也是恩典。",
 "珍惜主日的讲道与圣礼：圣灵借此生发并坚固信心。",
 "犯罪后记住受洗之名：洗净是真实的，回到基督。",
 "以圣约家庭养育儿女：教导、祷告、带他们进教会。",
 "领餐时向上举心：基督真实临在，借圣灵喂养你。",
 "不把饼当成神，也不把圣餐当成空记号。",
 "领餐前自省悔改，教会也要守护圣餐的圣洁。",
 "接受教会的劝诫为爱的钥匙，而不是冒犯。",
 "善行是信心的果子与见证，也是邻舍得益处的路。",
 "悔改是一生的动作：治死旧我，活出新我。",
 "察验心中何物占据神的位置：钱、名、人、安全感。",
 "敬拜照神所吩咐的方式，不按自己的创意与口味。",
 "说话、玩笑、网络发言都不轻慢神的名。",
 "起誓只在必要且合法时，平日说话诚实如誓。",
 "主日停下工作，进入敬拜；把它当作永远安息的预尝。",
 "顺服父母与上司，同时为他们祷告并宽容其软弱。",
 "治死怒气、仇恨与报复：心中的恨就是杀人的根。",
 "身体是圣灵的殿：远离色情，持守婚约。",
 "诚实工作，慷慨施予：私有财产是管家职分。",
 "不传话、不贴标签，替邻舍的名誉说公道话。",
 "最小的贪念也是罪：在知足中学会感恩。",
 "祷告是感恩生活最主要的部分，每日定时开口。",
 "开口称「父」：孩子般信靠，不像雇工般讨价。",
 "所求所行先问：这能否使神的名被尊为圣？",
 "为讲道、宣教与世界各地的教会代祷。",
 "把「我要」换成「愿你的旨意」，从小决定开始。",
 "日用的饮食也要求：承认一切供应都从神手而来。",
 "向神求赦免时，同时饶恕得罪你的人。",
 "在试探中求神扶持，并以「阿们」确信祂必垂听。",
]

CODMAP = {"I": 1, "II": 2, "III": 3, "IV": 3, "III/IV": 3, "V": 4}


def confess_links(s):
    s = E(s)
    s = re.sub(r'BC\s?(\d{1,2})', lambda m: '<a class="cfa bc" href="texts.html#bc%s" title="比利时信条原文">BC %s</a>' % (m.group(1), m.group(1)), s)
    s = re.sub(r'CoD\s?(III/IV|I{1,3}|IV|V)', lambda m: '<a class="cfa cod" href="texts.html#cod%d" title="多特信经原文">CoD %s</a>' % (CODMAP[m.group(1)], m.group(1)), s)
    s = re.sub(r'(?<![#\w])问\s?(\d{1,3})', lambda m: '<a class="cfa hc" href="texts.html#q%s">问 %s</a>' % (m.group(1), m.group(1)), s)
    return s


def three_acts():
    acts = [("misery", "🪞", "困苦", "MISERIA", "问 3–11", "律法如镜：我有多深的罪与困苦"),
            ("deliver", "✝️", "拯救", "LIBERATIO", "问 12–85", "福音如门：基督如何救我脱离"),
            ("gratitude", "🙏", "感恩", "GRATITUDO", "问 86–129", "律法如路：我当如何感谢神")]
    cells = []
    for i, (k, e, t, la, q, g) in enumerate(acts):
        cells.append('<div class="act3 %s" style="animation-delay:%.2fs"><div class="a3e">%s</div>'
                     '<b>%s</b><i>%s · %s</i><p>%s</p></div>' % (k, i * .18, e, t, la, q, g))
        if i < 2:
            cells.append('<div class="a3arrow" aria-hidden="true"><span></span><span></span><span></span></div>')
    return ('<div class="act3wrap"><div class="a3top">🕊️ 问 1–2 · 唯一的安慰 → 三件必须知道的事</div>'
            '<div class="act3row">%s</div></div>' % ''.join(cells))


CSS4 = r"""
/* ===== v4：鲜明配色 · 图标 · 动画 ===== */
:root{--misery:#D2283E;--deliver:#2457C5;--gratitude:#DB8A0B;--prologue:#7048C0;--teal:#0B9484;
  --royal:#1D3F8F;--rubric:#C21F35;--brass:#C27C0E}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--misery:#FF7A8A;--deliver:#7EA6FF;--gratitude:#FFC250;--prologue:#B79BFF;--teal:#4FD8C4;--royal:#9DB8FF;--rubric:#FF7A8A;--brass:#FFC250}}
:root[data-theme="dark"]{--misery:#FF7A8A;--deliver:#7EA6FF;--gratitude:#FFC250;--prologue:#B79BFF;--teal:#4FD8C4;--royal:#9DB8FF;--rubric:#FF7A8A;--brass:#FFC250}
#prog{height:3px;background:linear-gradient(90deg,var(--prologue),var(--misery),var(--deliver),var(--gratitude))}
.hero h1{background:linear-gradient(100deg,var(--royal),var(--prologue) 35%,var(--misery) 60%,var(--gratitude));
  -webkit-background-clip:text;background-clip:text;color:transparent;background-size:200% 100%;animation:hue 9s ease-in-out infinite alternate}
@keyframes hue{to{background-position:100% 0}}
.sec h2{display:flex;align-items:center;gap:10px}
.sec h2::before{content:"";width:10px;height:28px;border-radius:6px;flex:none;background:linear-gradient(var(--deliver),var(--gratitude))}
/* three acts */
.act3wrap{margin:26px 0 6px}
.a3top{display:inline-block;font-family:var(--sans);font-size:14px;font-weight:600;padding:6px 14px;border-radius:99px;
  background:color-mix(in srgb,var(--prologue) 14%,transparent);color:var(--prologue);margin-bottom:12px}
.act3row{display:grid;grid-template-columns:1fr 54px 1fr 54px 1fr;align-items:stretch}
.act3{--c:var(--deliver);border-radius:18px;padding:16px 18px;color:var(--ink);
  background:linear-gradient(150deg,color-mix(in srgb,var(--c) 22%,var(--paper)),var(--paper) 80%);
  border:1.5px solid color-mix(in srgb,var(--c) 45%,transparent);animation:rise .7s cubic-bezier(.2,.8,.2,1) both}
.act3.misery{--c:var(--misery)}.act3.gratitude{--c:var(--gratitude)}
.a3e{font-size:38px;line-height:1;animation:bob 3.2s ease-in-out infinite}
.act3 b{display:block;font-family:var(--disp);font-size:28px;color:var(--c);margin-top:6px}
.act3 i{font-style:normal;font-family:var(--sans);font-size:12.5px;color:var(--muted);letter-spacing:.08em}
.act3 p{margin:6px 0 0;font-size:16px;line-height:1.7}
.a3arrow{display:flex;align-items:center;justify-content:center;gap:5px}
.a3arrow span{width:7px;height:7px;border-radius:50%;background:var(--brass);animation:dot 1.4s infinite}
.a3arrow span:nth-child(2){animation-delay:.2s}.a3arrow span:nth-child(3){animation-delay:.4s}
@keyframes dot{0%,100%{opacity:.2;transform:scale(.7)}50%{opacity:1;transform:scale(1.15)}}
@keyframes bob{50%{transform:translateY(-5px) rotate(-4deg)}}
@keyframes rise{from{opacity:0;transform:translateY(16px)}}
@media (max-width:760px){.act3row{grid-template-columns:1fr}.a3arrow{height:30px;transform:rotate(90deg)}}
/* LD icon + application */
.ld.v3 .ld-no{position:relative}
.ld-emo{font-size:34px;line-height:1;align-self:center;filter:drop-shadow(0 4px 8px rgba(0,0,0,.15))}
.ld.v3.in .ld-emo{animation:bob 3.6s ease-in-out infinite}
.keyline{grid-template-columns:minmax(0,1.5fr) minmax(0,1fr) minmax(0,1fr)}
.kb-app{background:linear-gradient(120deg,color-mix(in srgb,var(--teal) 18%,var(--paper)),var(--paper));
  border:1.5px solid color-mix(in srgb,var(--teal) 45%,transparent)}
.b-app{background:var(--teal)}
@media (max-width:1100px){.keyline{grid-template-columns:1fr 1fr}.kb-core{grid-column:1/-1}}
@media (max-width:640px){.keyline{grid-template-columns:1fr}}
.ana-more{margin-top:4px}
.ana-more>summary{cursor:pointer;font-family:var(--sans);font-size:13px;color:var(--pc);list-style:none}
.ana-more>summary::-webkit-details-marker{display:none}
a.cfa{display:inline-block;padding:0 7px;margin:1px 0;border-radius:6px;font-family:var(--sans);font-size:.9em;text-decoration:none}
a.cfa.bc{background:color-mix(in srgb,var(--deliver) 13%,transparent);color:var(--deliver)}
a.cfa.cod{background:color-mix(in srgb,var(--misery) 13%,transparent);color:var(--misery)}
a.cfa.hc{background:color-mix(in srgb,var(--gratitude) 16%,transparent);color:var(--brass)}
.mw .mwe{font-size:20px;position:absolute;right:10px;top:8px}
.mw{position:relative}
.mw u{text-decoration:none;font-size:13px;color:var(--teal);grid-column:2}
.toc a .emo{margin-right:4px}
.tile:hover .ic{transform:rotate(-8deg) scale(1.1)}
.tile .ic{transition:transform .3s}
@media (max-width:860px){.ld.v3 .ld-h{position:relative;flex-wrap:nowrap;align-items:flex-start}.ld-emo{position:absolute;left:18px;top:76px;font-size:26px}.ld.v3 .ld-h .ld-no{margin-bottom:34px}.ld.v3 .chk{position:absolute;right:12px;top:12px;font-size:12px}.ld.v3 .ld-ht h3{padding-right:70px}}
@media (prefers-reduced-motion:reduce){.a3e,.ld-emo,.a3arrow span,.hero h1{animation:none!important}}
"""
