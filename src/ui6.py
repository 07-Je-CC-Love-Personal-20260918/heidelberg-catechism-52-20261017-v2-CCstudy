# -*- coding: utf-8 -*-
"""v6：52 主日闪卡速记（翻面 · 左右切换 · 随机 · 只练未背熟）"""
import json
import ui4


def flashcards(LDS, E):
    deck = [{"n": d["n"], "e": ui4.EMO[d["n"] - 1], "t": d["title"], "p": d["part"], "k": d["key"],
             "q": "问 %d–%d" % (d["qas"][0][0], d["qas"][-1][0]) if len(d["qas"]) > 1 else "问 %d" % d["qas"][0][0],
             "c": d["core"], "m": d["memo"], "a": ui4.APP[d["n"] - 1]} for d in LDS]
    return ('<div class="fc-wrap glass" id="fc"><div class="fc-bar">'
            '<button class="btn" data-f="prev" aria-label="上一张">←</button>'
            '<span class="fc-pos"><b id="fcN">1</b> / <span id="fcT">52</span></span>'
            '<button class="btn" data-f="next" aria-label="下一张">→</button>'
            '<button class="btn" data-f="rand">🎲 随机</button>'
            '<button class="btn" data-f="todo">只练未背熟</button>'
            '<span class="fc-hint">点卡片或按空格翻面 · ←→ 切换</span></div>'
            '<div class="fc-stage"><div class="fc-card" id="fcCard" tabindex="0" role="button" aria-label="翻面">'
            '<div class="fc-face fc-front"><div class="fc-emo" id="fcE"></div><div class="fc-no" id="fcNo"></div>'
            '<div class="fc-title" id="fcTi"></div><div class="fc-q" id="fcQ"></div><div class="fc-ask">它的本质核心是什么？</div></div>'
            '<div class="fc-face fc-back"><div class="fc-row k"><span>重点</span><p id="fcC"></p></div>'
            '<div class="fc-row m"><span>记忆钥匙</span><p id="fcM"></p></div>'
            '<div class="fc-row a"><span>今日应用</span><p id="fcA"></p></div>'
            '<a class="fc-go" id="fcGo" href="#ld1">读本主日全文 →</a></div></div></div>'
            '<div class="fc-dots" id="fcDots"></div></div>'
            '<script type="application/json" id="fcData">%s</script>') % json.dumps(deck, ensure_ascii=False).replace("</", "<\\/")


CSS6 = r"""
.toc a .no{min-width:3.2em;margin-right:2px}
.fc-wrap{border:1px solid var(--rule);border-radius:var(--r);padding:14px clamp(10px,2.5vw,22px) 16px;box-shadow:var(--sh2);margin:14px 0}
.fc-bar{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-bottom:12px}
.fc-pos{font-family:var(--sans);font-size:14px;min-width:64px;text-align:center}
.fc-pos b{font-size:20px;color:var(--royal)}
.fc-hint{margin-left:auto;font-family:var(--sans);font-size:12.5px;color:var(--muted)}
.fc-stage{perspective:1400px}
.fc-card{--pc:var(--deliver);position:relative;min-height:300px;transform-style:preserve-3d;transition:transform .6s cubic-bezier(.3,.9,.3,1);cursor:pointer;outline:none}
.fc-card.misery{--pc:var(--misery)}.fc-card.gratitude{--pc:var(--gratitude)}.fc-card.prologue{--pc:var(--prologue)}
.fc-card.flip{transform:rotateY(180deg)}
.fc-card.swap{animation:swap .35s ease}
@keyframes swap{from{opacity:.2;transform:translateX(24px)}}
.fc-face{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden;border-radius:18px;padding:22px clamp(16px,3vw,32px);
  display:flex;flex-direction:column;justify-content:center;border:1.5px solid color-mix(in srgb,var(--pc) 45%,transparent)}
.fc-front{align-items:center;text-align:center;background:linear-gradient(150deg,color-mix(in srgb,var(--pc) 26%,var(--paper)),var(--paper) 75%)}
.fc-back{transform:rotateY(180deg);gap:10px;justify-content:safe center;background:var(--paper);overflow:auto}
.fc-emo{font-size:58px;line-height:1;animation:bob 3s ease-in-out infinite}
.fc-no{margin-top:8px;font-family:var(--sans);font-size:13px;letter-spacing:.18em;color:#fff;background:var(--pc);border-radius:99px;padding:3px 14px}
.fc-title{font-family:var(--disp);font-size:clamp(26px,4vw,38px);color:var(--pc);margin:10px 0 2px;line-height:1.25}
.fc-q{font-family:var(--sans);font-size:13.5px;color:var(--muted)}
.fc-ask{margin-top:14px;font-size:15px;color:var(--ink-2);border-top:1px dashed var(--rule);padding-top:10px}
.fc-row{display:grid;grid-template-columns:86px 1fr;gap:10px;align-items:start}
.fc-row span{font-family:var(--sans);font-size:12.5px;font-weight:700;color:#fff;border-radius:99px;padding:3px 0;text-align:center}
.fc-row.k span{background:var(--pc)}.fc-row.m span{background:var(--brass)}.fc-row.a span{background:var(--teal)}
.fc-row p{margin:0;line-height:1.75}
.fc-row.k p{font-weight:700;font-size:1.06em}
.fc-go{align-self:flex-end;font-family:var(--sans);font-size:13.5px;color:var(--teal)}
.fc-dots{display:grid;grid-template-columns:repeat(26,1fr);gap:3px;margin-top:12px}
.fc-dots i{height:6px;border-radius:9px;background:var(--paper-3);cursor:pointer;transition:background .2s,transform .2s}
.fc-dots i.d{background:var(--brass)}
.fc-dots i.on{background:var(--royal);transform:scaleY(1.8)}
@media (max-width:640px){.fc-card{min-height:460px}.fc-hint{display:none}.fc-row{grid-template-columns:1fr}.fc-row span{justify-self:start;padding:3px 12px}.fc-dots{grid-template-columns:repeat(13,1fr)}}
"""

JS6 = r"""
(function(){var d=document,W=d.getElementById('fc');if(!W)return;
var all=JSON.parse(d.getElementById('fcData').textContent),deck=all.slice(),i=0,todo=false,card=d.getElementById('fcCard');
function done(){var s={};d.querySelectorAll('.chk input:checked').forEach(function(c){s[c.dataset.n]=1;});return s;}
function $(id){return d.getElementById(id);}
var dots=$('fcDots');dots.innerHTML=all.map(function(x){return '<i data-n="'+x.n+'" title="主日 '+x.n+'"></i>';}).join('');
function show(anim){var x=deck[i];if(!x)return;card.classList.remove('flip','misery','deliver','gratitude','prologue');card.classList.add(x.k);
 $('fcE').textContent=x.e;$('fcNo').textContent='主日 '+x.n+' · '+x.p;$('fcTi').textContent=x.t;$('fcQ').textContent=x.q;
 $('fcC').textContent=x.c;$('fcM').textContent=x.m;$('fcA').textContent=x.a;$('fcGo').setAttribute('href','#ld'+x.n);
 $('fcN').textContent=i+1;$('fcT').textContent=deck.length;
 var s=done();dots.querySelectorAll('i').forEach(function(t){t.classList.toggle('d',!!s[t.dataset.n]);t.classList.toggle('on',+t.dataset.n===x.n);});
 if(anim){card.classList.remove('swap');void card.offsetWidth;card.classList.add('swap');}}
function step(k){i=(i+k+deck.length)%deck.length;show(true);}
W.addEventListener('click',function(e){var b=e.target.closest('[data-f]');if(!b)return;var f=b.dataset.f;
 if(f==='prev')step(-1);else if(f==='next')step(1);else if(f==='rand'){i=Math.floor(Math.random()*deck.length);show(true);}
 else if(f==='todo'){todo=!todo;b.classList.toggle('on',todo);var s=done();deck=todo?all.filter(function(x){return !s[x.n];}):all.slice();if(!deck.length)deck=all.slice();i=0;show(true);}});
var sw=0;card.addEventListener('click',function(e){if(sw){sw=0;return;}if(e.target.closest('a'))return;card.classList.toggle('flip');});
dots.addEventListener('click',function(e){var t=e.target.closest('i');if(!t)return;deck=all.slice();todo=false;i=+t.dataset.n-1;show(true);});
d.addEventListener('keydown',function(e){if(/INPUT|TEXTAREA/.test((e.target.tagName||'')))return;var r=W.getBoundingClientRect();
 if(r.bottom<0||r.top>innerHeight)return;if(e.key==='ArrowRight'){step(1);e.preventDefault();}else if(e.key==='ArrowLeft'){step(-1);e.preventDefault();}
 else if(e.key===' '&&(d.activeElement===card||d.activeElement===d.body)){card.classList.toggle('flip');e.preventDefault();}});
var sx=0;card.addEventListener('touchstart',function(e){sx=e.touches[0].clientX;},{passive:true});
card.addEventListener('touchend',function(e){var dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>50){sw=1;step(dx<0?1:-1);}},{passive:true});
d.addEventListener('change',function(e){if(e.target.matches('.chk input'))show(false);});
show(false);})();
"""
