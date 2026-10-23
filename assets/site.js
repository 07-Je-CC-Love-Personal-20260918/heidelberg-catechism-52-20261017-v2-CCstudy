try{
(function(){
var d=document,b=d.body,root=d.documentElement;

/* theme → v11 多主题 */

/* ---- toc hide / drawer ---- */
var shell=d.querySelector('.shell');
function toggleToc(){
  if(window.innerWidth<=1080){b.classList.toggle('nav');
    d.getElementById('tocBtn').classList.toggle('on',b.classList.contains('nav'));}
  else{shell.classList.toggle('hid');
    d.getElementById('tocBtn').classList.toggle('on',!shell.classList.contains('hid'));}
}
d.getElementById('tocBtn').onclick=toggleToc;
d.getElementById('tocOpen').onclick=function(){shell.classList.remove('hid');
  d.getElementById('tocBtn').classList.add('on');};
var scrim=d.querySelector('.scrim');if(scrim)scrim.onclick=function(){b.classList.remove('nav');};
d.querySelectorAll('.toc a').forEach(function(a){a.addEventListener('click',function(){b.classList.remove('nav');});});
d.addEventListener('keydown',function(e){if(e.key==='Escape')b.classList.remove('nav');});

/* ---- drill mode ---- */
var drill=d.getElementById('drillBtn');
drill.onclick=function(){
  b.classList.toggle('drill');drill.classList.toggle('on');
  drill.textContent=b.classList.contains('drill')?'退出背诵':'背诵';
  d.querySelectorAll('.qa.open').forEach(function(q){q.classList.remove('open');});
};
d.querySelectorAll('.qa').forEach(function(q){
  q.addEventListener('click',function(){if(b.classList.contains('drill'))q.classList.toggle('open');});
});

/* ---- memorised marks ---- */
var DONE={};
try{DONE=JSON.parse(localStorage.getItem('hc-done')||'{}');}catch(e){DONE={};}
function sync(n,on){
  var c=d.querySelector('.g52[data-n="'+n+'"]'),l=d.querySelector('.toc a[data-n="'+n+'"]');
  if(c)c.classList.toggle('done',on);if(l)l.classList.toggle('done',on);
}
d.querySelectorAll('.chk input').forEach(function(cb){
  var n=cb.getAttribute('data-n');
  if(DONE[n]){cb.checked=true;sync(n,true);}
  cb.addEventListener('change',function(){
    DONE[n]=cb.checked;if(!cb.checked)delete DONE[n];
    sync(n,cb.checked);
    var _dc=d.getElementById('doneCount');if(_dc)_dc.textContent=Object.keys(DONE).length;
    try{localStorage.setItem('hc-done',JSON.stringify(DONE));}catch(e){}
  });
});
var _dc=d.getElementById('doneCount');if(_dc)_dc.textContent=Object.keys(DONE).length;

/* search → v10 全站搜索 */

/* ---- scroll spy (rAF + getBoundingClientRect) ---- */
var secs=[].slice.call(d.querySelectorAll('section[id]'));
var links={};d.querySelectorAll('.toc a').forEach(function(a){links[a.getAttribute('href').slice(1)]=a;});
var side=d.querySelector('.side'),cur=null,tick=false;
function spy(){
  tick=false;var best=null,bd=1e9;
  for(var i=0;i<secs.length;i++){
    var r=secs[i].getBoundingClientRect();
    if(r.bottom<60)continue;
    var dd=Math.abs(r.top-70);
    if(r.top<=140&&r.bottom>140){best=secs[i];break;}
    if(dd<bd){bd=dd;best=secs[i];}
  }
  if(best&&best.id!==cur){
    cur=best.id;
    var a=links[cur];
    d.querySelectorAll('.toc a.active').forEach(function(x){x.classList.remove('active');});
    if(a){a.classList.add('active');
      if(a.offsetTop<side.scrollTop||a.offsetTop>side.scrollTop+side.clientHeight-70)
        side.scrollTop=a.offsetTop-side.clientHeight/2;}
  }
  d.getElementById('toTop').classList.toggle('show',window.scrollY>700);
}
var lastSpy=0,spyT=null;window.addEventListener('scroll',function(){var n=Date.now();if(n-lastSpy>110){lastSpy=n;if(!tick){tick=true;requestAnimationFrame(spy);}}clearTimeout(spyT);spyT=setTimeout(function(){if(!tick){tick=true;requestAnimationFrame(spy);}},140);},{passive:true});
spy();

/* ---- reveal animations (stop when off-screen to save power) ---- */
if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){e.target.classList.toggle('in',e.isIntersecting);});
  },{rootMargin:'0px 0px -12% 0px',threshold:.12});
  d.querySelectorAll('figure').forEach(function(f){io.observe(f);});
}else{d.querySelectorAll('figure').forEach(function(f){f.classList.add('in');});}

/* ---- quiz ---- */
var QZ=d.querySelectorAll('.qz');
function grade(){
  var right=0,wrong=[];
  QZ.forEach(function(q){
    var ans=+q.getAttribute('data-a'),pick=q.querySelector('input:checked');
    q.classList.add('done');
    q.querySelectorAll('.opt').forEach(function(o,i){
      o.classList.remove('ok','no');
      if(i===ans)o.classList.add('ok');
      else if(pick&&+pick.value===i)o.classList.add('no');
    });
    if(pick&&+pick.value===ans)right++;else wrong.push(q.getAttribute('data-i'));
  });
  d.getElementById('score').textContent='得分 '+right+' / '+QZ.length+
    (wrong.length?'　错题：第 '+wrong.join('、')+' 题':'　全对');
}
if(d.getElementById('gradeBtn'))d.getElementById('gradeBtn').onclick=grade;
if(d.getElementById('resetBtn'))d.getElementById('resetBtn').onclick=function(){
  QZ.forEach(function(q){q.classList.remove('done');
    q.querySelectorAll('.opt').forEach(function(o){o.classList.remove('ok','no');});
    q.querySelectorAll('input').forEach(function(i){i.checked=false;});});
  d.getElementById('score').textContent='';
};

d.getElementById('toTop').onclick=function(){if(window.__lenis)window.__lenis.scrollTo(0,{duration:1.1});else window.scrollTo({top:0,behavior:'smooth'});};

})();

}catch(e){console.error(e)}
try{
(function(){
var d=document;
/* group consecutive intro .blk into tiled grids */
d.querySelectorAll('.sec').forEach(function(s){
  var kids=[].slice.call(s.children),run=[];
  function flush(){if(run.length>1){var g=d.createElement('div');g.className='blkgrid';
    run[0].parentNode.insertBefore(g,run[0]);run.forEach(function(x){g.appendChild(x);});}run=[];}
  kids.forEach(function(k){if(k.classList.contains('blk'))run.push(k);else flush();});flush();
});
/* reveal */
var els=d.querySelectorAll('.rv,.sec,.fig,.card');
if('IntersectionObserver' in window){
  els.forEach(function(e){if(!e.classList.contains('rv'))e.classList.add('rv');});
  var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}});},{rootMargin:'0px 0px -6% 0px'});
  els.forEach(function(e){io.observe(e);});
  setTimeout(function(){var h=location.hash&&d.querySelector(location.hash);if(h)h.scrollIntoView();},60);
}else els.forEach(function(e){e.classList.add('in');});
/* search / jump must reveal */
d.addEventListener('click',function(e){var a=e.target.closest('a[href^="#"]');if(!a)return;
  var t=d.querySelector(a.getAttribute('href'));if(t){t.classList.add('in');t.querySelectorAll('.rv').forEach(function(x){x.classList.add('in');});}});
/* reader */
var rd=d.querySelector('.reader');if(!rd)return;
rd.querySelectorAll('.rtab').forEach(function(b){b.onclick=function(){
  rd.querySelectorAll('.rtab').forEach(function(x){x.classList.toggle('on',x===b);});
  rd.querySelectorAll('.rpane').forEach(function(p){p.classList.toggle('on',p.id===b.dataset.r);});};});
d.getElementById('rHide').onclick=function(){rd.classList.toggle('cov');this.classList.toggle('on');
  rd.querySelectorAll('.rl').forEach(function(l){l.classList.remove('sh');});};
rd.addEventListener('click',function(e){var l=e.target.closest('.rl');if(l&&rd.classList.contains('cov'))l.classList.toggle('sh');});
var fs=[19,22,16],fi=0;d.getElementById('rSize').onclick=function(){fi=(fi+1)%3;rd.style.setProperty('--rfs',fs[fi]+'px');};
})();

}catch(e){console.error(e)}
try{
(function(){var d=document,b=d.body,tb=d.querySelector('.topbar');
function setH(){if(tb)d.documentElement.style.setProperty('--tbh',tb.getBoundingClientRect().height+'px');}
setH();addEventListener('resize',setH,{passive:true});
function H(){return (tb?tb.getBoundingClientRect().height:56)+14;}
function SC(top,smooth){var L=window.__lenis;if(L){L.scrollTo(top,{immediate:!smooth,duration:smooth?0.9:0,force:true});}else{window.scrollTo({top:top,behavior:smooth?'smooth':'auto'});}}
function reveal(t){t.classList.add('in');t.querySelectorAll('.rv').forEach(function(x){x.classList.add('in');});
  var p=t.closest('details');while(p){p.open=true;p=p.parentElement&&p.parentElement.closest('details');}}
function go(id,push){var t=d.getElementById(id);if(!t)return false;reveal(t);
  var y=function(){return t.getBoundingClientRect().top+scrollY-H();};
  var Y=y(),dist=Y-scrollY,V=innerHeight;
  if(Math.abs(dist)>V*1.5){SC(Y-Math.sign(dist)*V*.5,false);}
  requestAnimationFrame(function(){SC(y(),true);});
  var n=0;(function fix(){if(++n>10)return;setTimeout(function(){var dy=t.getBoundingClientRect().top-H();
    if(Math.abs(dy)>4){SC(scrollY+dy,n<2);fix();}else if(n<8){fix();}},n<2?380:120);})();
  t.classList.remove('flash-t');void t.offsetWidth;t.classList.add('flash-t');
  if(push!==false)history.replaceState(null,'','#'+id);return true;}
d.addEventListener('click',function(e){var a=e.target.closest('a[href^="#"]');if(!a)return;
  var id=decodeURIComponent(a.getAttribute('href').slice(1));if(!id)return;
  if(go(id)){e.preventDefault();e.stopPropagation();b.classList.remove('nav');b.classList.remove('tocopen');}},true);
/* 抽屉统一：texts 页旧的 tocopen 映射到 nav */
new MutationObserver(function(){if(b.classList.contains('tocopen')){b.classList.remove('tocopen');b.classList.toggle('nav');}})
  .observe(b,{attributes:true,attributeFilter:['class']});
if(location.hash){var id=decodeURIComponent(location.hash.slice(1));
 /* 首次带锚点打开：逐帧瞬时校正直到连续稳定（懒渲染区块会改变高度） */
 var t0=performance.now(),ok=0;(function snap(){var t=d.getElementById(id);if(!t)return;reveal(t);
  var dy=t.getBoundingClientRect().top-H();if(Math.abs(dy)>3){ok=0;SC(scrollY+dy,false);}else ok++;
  if(ok<6&&performance.now()-t0<2500)requestAnimationFrame(snap);else{t.classList.remove('flash-t');void t.offsetWidth;t.classList.add('flash-t');}})();
 addEventListener('load',function(){var t=d.getElementById(id);if(t){var dy=t.getBoundingClientRect().top-H();if(Math.abs(dy)>3)SC(scrollY+dy,false);}});}
})();

}catch(e){console.error(e)}
try{
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

}catch(e){console.error(e)}
try{
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

}catch(e){console.error(e)}
try{
(function(){var d=document,b=d.body,btn=d.getElementById('mkBtn');if(!btn)return;var ls;try{ls=localStorage}catch(e){}
function set(off){b.classList.toggle('nomark',off);btn.textContent='标记：'+(off?'关':'开');btn.classList.toggle('on',!off);try{ls&&ls.setItem('hcMark',off?'0':'1')}catch(e){}}
var off=false;try{off=ls&&ls.getItem('hcMark')==='0'}catch(e){}set(off);
btn.onclick=function(){set(!b.classList.contains('nomark'));};
})();

}catch(e){console.error(e)}
try{(function(){var e=`1.3.27`;function t(e,t,n){return Math.max(e,Math.min(t,n))}function n(e,t,n){return(1-n)*e+n*t}function r(e,t,r,i){return n(e,t,1-Math.exp(-r*i))}function i(e,t){return(e%t+t)%t}var a=class{isRunning=!1;value=0;from=0;to=0;currentTime=0;lerp;duration;easing;onUpdate;advance(e){if(!this.isRunning)return;let n=!1;if(this.duration&&this.easing){this.currentTime+=e;let r=t(0,this.currentTime/this.duration,1);n=r>=1;let i=n?1:this.easing(r);this.value=this.from+(this.to-this.from)*i}else this.lerp?(this.value=r(this.value,this.to,this.lerp*60,e),Math.round(this.value)===Math.round(this.to)&&(this.value=this.to,n=!0)):(this.value=this.to,n=!0);n&&this.stop(),this.onUpdate?.(this.value,n)}stop(){this.isRunning=!1}fromTo(e,t,{lerp:n,duration:r,easing:i,onStart:a,onUpdate:o}){this.from=this.value=e,this.to=t,this.lerp=n,this.duration=r,this.easing=i,this.currentTime=0,this.isRunning=!0,a?.(),this.onUpdate=o}};function o(e,t){let n;return function(...r){clearTimeout(n),n=setTimeout(()=>{n=void 0,e.apply(this,r)},t)}}var s=class{width=0;height=0;scrollHeight=0;scrollWidth=0;debouncedResize;wrapperResizeObserver;contentResizeObserver;constructor(e,t,{autoResize:n=!0,debounce:r=250}={}){this.wrapper=e,this.content=t,n&&(this.debouncedResize=o(this.resize,r),this.wrapper instanceof Window?window.addEventListener(`resize`,this.debouncedResize):(this.wrapperResizeObserver=new ResizeObserver(this.debouncedResize),this.wrapperResizeObserver.observe(this.wrapper)),this.contentResizeObserver=new ResizeObserver(this.debouncedResize),this.contentResizeObserver.observe(this.content)),this.resize()}destroy(){this.wrapperResizeObserver?.disconnect(),this.contentResizeObserver?.disconnect(),this.wrapper===window&&this.debouncedResize&&window.removeEventListener(`resize`,this.debouncedResize)}resize=()=>{this.onWrapperResize(),this.onContentResize()};onWrapperResize=()=>{this.wrapper instanceof Window?(this.width=window.innerWidth,this.height=window.innerHeight):(this.width=this.wrapper.clientWidth,this.height=this.wrapper.clientHeight)};onContentResize=()=>{this.wrapper instanceof Window?(this.scrollHeight=this.content.scrollHeight,this.scrollWidth=this.content.scrollWidth):(this.scrollHeight=this.wrapper.scrollHeight,this.scrollWidth=this.wrapper.scrollWidth)};get limit(){return{x:this.scrollWidth-this.width,y:this.scrollHeight-this.height}}},c=class{events={};emit(e,...t){let n=this.events[e]||[];for(let e=0,r=n.length;e<r;e++)n[e]?.(...t)}on(e,t){return this.events[e]?this.events[e].push(t):this.events[e]=[t],()=>{this.events[e]=this.events[e]?.filter(e=>t!==e)}}off(e,t){this.events[e]=this.events[e]?.filter(e=>t!==e)}destroy(){this.events={}}};let l={passive:!1};function u(e,t){return e===1?16.666666666666668:e===2?t:1}var d=class{touchStart={x:0,y:0};lastDelta={x:0,y:0};window={width:0,height:0};emitter=new c;constructor(e,t={wheelMultiplier:1,touchMultiplier:1}){this.element=e,this.options=t,window.addEventListener(`resize`,this.onWindowResize),this.onWindowResize(),this.element.addEventListener(`wheel`,this.onWheel,l),this.element.addEventListener(`touchstart`,this.onTouchStart,l),this.element.addEventListener(`touchmove`,this.onTouchMove,l),this.element.addEventListener(`touchend`,this.onTouchEnd,l)}on(e,t){return this.emitter.on(e,t)}destroy(){this.emitter.destroy(),window.removeEventListener(`resize`,this.onWindowResize),this.element.removeEventListener(`wheel`,this.onWheel,l),this.element.removeEventListener(`touchstart`,this.onTouchStart,l),this.element.removeEventListener(`touchmove`,this.onTouchMove,l),this.element.removeEventListener(`touchend`,this.onTouchEnd,l)}onTouchStart=e=>{let{clientX:t,clientY:n}=e.targetTouches?e.targetTouches[0]:e;this.touchStart.x=t,this.touchStart.y=n,this.lastDelta={x:0,y:0},this.emitter.emit(`scroll`,{deltaX:0,deltaY:0,event:e})};onTouchMove=e=>{let{clientX:t,clientY:n}=e.targetTouches?e.targetTouches[0]:e,r=-(t-this.touchStart.x)*this.options.touchMultiplier,i=-(n-this.touchStart.y)*this.options.touchMultiplier;this.touchStart.x=t,this.touchStart.y=n,this.lastDelta={x:r,y:i},this.emitter.emit(`scroll`,{deltaX:r,deltaY:i,event:e})};onTouchEnd=e=>{this.emitter.emit(`scroll`,{deltaX:this.lastDelta.x,deltaY:this.lastDelta.y,event:e})};onWheel=e=>{let{deltaX:t,deltaY:n,deltaMode:r}=e,i=u(r,this.window.width),a=u(r,this.window.height);t*=i,n*=a,t*=this.options.wheelMultiplier,n*=this.options.wheelMultiplier,this.emitter.emit(`scroll`,{deltaX:t,deltaY:n,event:e})};onWindowResize=()=>{this.window={width:window.innerWidth,height:window.innerHeight}}};let f=e=>Math.min(1,1.001-2**(-10*e));var p=class{_isScrolling=!1;_isStopped=!1;_isLocked=!1;_preventNextNativeScrollEvent=!1;_resetVelocityTimeout=null;_rafId=null;_isDraggingSelection=!1;reducedMotionMediaQuery=window.matchMedia(`(prefers-reduced-motion: reduce)`);isTouching;isIos;time=0;userData={};lastVelocity=0;velocity=0;direction=0;options;targetScroll;animatedScroll;animate=new a;emitter=new c;dimensions;virtualScroll;constructor({wrapper:t=window,content:n=document.documentElement,eventsTarget:r=t,smoothWheel:i=!0,syncTouch:a=!1,syncTouchLerp:o=.075,touchInertiaExponent:c=1.7,duration:l,easing:u,lerp:p=.1,infinite:m=!1,orientation:h=`vertical`,gestureOrientation:g=h===`horizontal`?`both`:`vertical`,touchMultiplier:_=1,wheelMultiplier:v=1,autoResize:y=!0,prevent:b,virtualScroll:x,overscroll:S=!0,autoRaf:C=!1,anchors:w=!1,autoToggle:T=!1,allowNestedScroll:E=!1,__experimental__naiveDimensions:D=!1,naiveDimensions:O=D,stopInertiaOnNavigate:k=!1,respectReducedMotion:A=!0}={}){window.lenisVersion=e,window.lenis||(window.lenis={}),window.lenis.version=e,h===`horizontal`&&(window.lenis.horizontal=!0),a===!0&&(window.lenis.touch=!0),this.isIos=/(iPad|iPhone|iPod)/g.test(navigator.userAgent),(!t||t===document.documentElement)&&(t=window),typeof l==`number`&&typeof u!=`function`?u=f:typeof u==`function`&&typeof l!=`number`&&(l=1),this.options={wrapper:t,content:n,eventsTarget:r,smoothWheel:i,syncTouch:a,syncTouchLerp:o,touchInertiaExponent:c,duration:l,easing:u,lerp:p,infinite:m,gestureOrientation:g,orientation:h,touchMultiplier:_,wheelMultiplier:v,autoResize:y,prevent:b,virtualScroll:x,overscroll:S,autoRaf:C,anchors:w,autoToggle:T,allowNestedScroll:E,naiveDimensions:O,stopInertiaOnNavigate:k,respectReducedMotion:A},this.dimensions=new s(t,n,{autoResize:y}),this.updateClassName(),this.targetScroll=this.animatedScroll=this.actualScroll,this.options.wrapper.addEventListener(`scroll`,this.onNativeScroll),this.options.wrapper.addEventListener(`scrollend`,this.onScrollEnd,{capture:!0}),(this.options.anchors||this.options.stopInertiaOnNavigate)&&this.options.wrapper.addEventListener(`click`,this.onClick),this.options.wrapper.addEventListener(`pointerdown`,this.onPointerDown),this.virtualScroll=new d(r,{touchMultiplier:_,wheelMultiplier:v}),this.virtualScroll.on(`scroll`,this.onVirtualScroll),this.options.autoToggle&&(this.checkOverflow(),this.rootElement.addEventListener(`transitionend`,this.onTransitionEnd)),this.options.autoRaf&&(this._rafId=requestAnimationFrame(this.raf))}destroy(){this.emitter.destroy(),this._resetVelocityTimeout!==null&&(clearTimeout(this._resetVelocityTimeout),this._resetVelocityTimeout=null),this.options.wrapper.removeEventListener(`scroll`,this.onNativeScroll),this.options.wrapper.removeEventListener(`scrollend`,this.onScrollEnd,{capture:!0}),this.options.wrapper.removeEventListener(`pointerdown`,this.onPointerDown),(this.options.anchors||this.options.stopInertiaOnNavigate)&&this.options.wrapper.removeEventListener(`click`,this.onClick),this.virtualScroll.destroy(),this.dimensions.destroy(),this.cleanUpClassName(),this._rafId&&cancelAnimationFrame(this._rafId)}on(e,t){return this.emitter.on(e,t)}off(e,t){return this.emitter.off(e,t)}onScrollEnd=e=>{e instanceof CustomEvent||(this.isScrolling===`smooth`||this.isScrolling===!1)&&e.stopPropagation()};dispatchScrollendEvent=()=>{this.options.wrapper.dispatchEvent(new CustomEvent(`scrollend`,{bubbles:this.options.wrapper===window,detail:{lenisScrollEnd:!0}}))};get overflow(){let e=this.isHorizontal?`overflow-x`:`overflow-y`;return getComputedStyle(this.rootElement)[e]}checkOverflow(){[`hidden`,`clip`].includes(this.overflow)?this.internalStop():this.internalStart()}onTransitionEnd=e=>{e.propertyName?.includes(`overflow`)&&e.target===this.rootElement&&this.checkOverflow()};setScroll(e){this.isHorizontal?this.options.wrapper.scrollTo({left:e,behavior:`instant`}):this.options.wrapper.scrollTo({top:e,behavior:`instant`})}onClick=e=>{let t=e.composedPath().filter(e=>e instanceof HTMLAnchorElement&&e.href).map(e=>new URL(e.href)),n=new URL(window.location.href);if(this.options.anchors){let e=t.find(e=>n.host===e.host&&n.pathname===e.pathname&&e.hash);if(e){let t=typeof this.options.anchors==`object`&&this.options.anchors?this.options.anchors:void 0,n=decodeURIComponent(e.hash);this.scrollTo(n,t);return}}if(this.options.stopInertiaOnNavigate&&t.some(e=>n.host===e.host&&n.pathname!==e.pathname)){this.reset();return}};onPointerDown=e=>{e.button===1&&this.reset()};isTouchOnSelectionHandle(e){let t=window.getSelection();if(!t||t.isCollapsed||t.rangeCount===0)return!1;let n=e.targetTouches[0]??e.changedTouches[0];if(!n)return!1;let r=t.getRangeAt(0).getClientRects();if(r.length===0)return!1;let i=r[0],a=r[r.length-1],o=Math.hypot(n.clientX-i.left,n.clientY-i.top)<=40,s=Math.hypot(n.clientX-a.right,n.clientY-a.bottom)<=40;return o||s}onVirtualScroll=e=>{if(typeof this.options.virtualScroll==`function`&&this.options.virtualScroll(e)===!1)return;let{deltaX:t,deltaY:n,event:r}=e;if(this.emitter.emit(`virtual-scroll`,{deltaX:t,deltaY:n,event:r}),r.ctrlKey||r.lenisStopPropagation)return;let i=r.type.includes(`touch`),a=r.type.includes(`wheel`);if(i&&this.isIos&&(r.type===`touchstart`&&(this._isDraggingSelection=this.isTouchOnSelectionHandle(r)),this._isDraggingSelection)){r.type===`touchend`&&(this._isDraggingSelection=!1);return}this.isTouching=r.type===`touchstart`||r.type===`touchmove`;let o=t===0&&n===0;if(this.options.syncTouch&&i&&r.type===`touchstart`&&o&&!this.isStopped&&!this.isLocked){this.reset();return}let s=this.options.gestureOrientation===`vertical`&&n===0||this.options.gestureOrientation===`horizontal`&&t===0;if(o||s)return;let c=r.composedPath();c=c.slice(0,c.indexOf(this.rootElement));let l=this.options.prevent,u=Math.abs(t)>=Math.abs(n)?`horizontal`:`vertical`;if(c.find(e=>e instanceof HTMLElement&&(typeof l==`function`&&l?.(e)||e.hasAttribute?.(`data-lenis-prevent`)||u===`vertical`&&e.hasAttribute?.(`data-lenis-prevent-vertical`)||u===`horizontal`&&e.hasAttribute?.(`data-lenis-prevent-horizontal`)||i&&e.hasAttribute?.(`data-lenis-prevent-touch`)||a&&e.hasAttribute?.(`data-lenis-prevent-wheel`)||this.options.allowNestedScroll&&this.hasNestedScroll(e,{deltaX:t,deltaY:n}))))return;if(this.isStopped||this.isLocked){r.cancelable&&r.preventDefault();return}if(!(this.options.syncTouch&&i||this.options.smoothWheel&&a)){this.isScrolling=`native`,this.animate.stop(),r.lenisStopPropagation=!0;return}let d=n;this.options.gestureOrientation===`both`?d=Math.abs(n)>Math.abs(t)?n:t:this.options.gestureOrientation===`horizontal`&&(d=t),(!this.options.overscroll||this.options.infinite||this.options.wrapper!==window&&this.limit>0&&(this.animatedScroll>0&&this.animatedScroll<this.limit||this.animatedScroll===0&&n>0||this.animatedScroll===this.limit&&n<0))&&(r.lenisStopPropagation=!0),r.cancelable&&r.preventDefault();let f=i&&this.options.syncTouch,p=i&&r.type===`touchend`;p&&(d=Math.sign(d)*Math.abs(this.velocity)**this.options.touchInertiaExponent),this.scrollTo(this.targetScroll+d,{programmatic:!1,...f?{lerp:p?this.options.syncTouchLerp:1}:{lerp:this.options.lerp,duration:this.options.duration,easing:this.options.easing}})};resize(){this.dimensions.resize(),this.animatedScroll=this.targetScroll=this.actualScroll,this.emit()}emit(){this.emitter.emit(`scroll`,this)}onNativeScroll=()=>{if(this._resetVelocityTimeout!==null&&(clearTimeout(this._resetVelocityTimeout),this._resetVelocityTimeout=null),this._preventNextNativeScrollEvent){this._preventNextNativeScrollEvent=!1;return}if(this.isScrolling===!1||this.isScrolling===`native`){let e=this.animatedScroll;this.animatedScroll=this.targetScroll=this.actualScroll,this.lastVelocity=this.velocity,this.velocity=this.animatedScroll-e,this.direction=Math.sign(this.animatedScroll-e),this.isStopped||(this.isScrolling=`native`),this.emit(),this.velocity!==0&&(this._resetVelocityTimeout=setTimeout(()=>{this.lastVelocity=this.velocity,this.velocity=0,this.isScrolling=!1,this.emit()},400))}};reset(){this.isLocked=!1,this.isScrolling=!1,this.animatedScroll=this.targetScroll=this.actualScroll,this.lastVelocity=this.velocity=0,this.animate.stop()}start(){if(this.isStopped){if(this.options.autoToggle){this.rootElement.style.removeProperty(`overflow`);return}this.internalStart()}}internalStart(){this.isStopped&&(this.reset(),this.isStopped=!1,this.emit())}stop(){if(!this.isStopped){if(this.options.autoToggle){this.rootElement.style.setProperty(`overflow`,`clip`);return}this.internalStop()}}internalStop(){this.isStopped||(this.reset(),this.isStopped=!0,this.emit())}raf=e=>{let t=e-(this.time||e);this.time=e,this.animate.advance(t*.001),this.options.autoRaf&&(this._rafId=requestAnimationFrame(this.raf))};scrollTo(e,{offset:n=0,immediate:r=!1,lock:i=!1,programmatic:a=!0,lerp:o=a?this.options.lerp:void 0,duration:s=a?this.options.duration:void 0,easing:c=a?this.options.easing:void 0,onStart:l,onComplete:u,force:d=!1,userData:p}={}){if(this.prefersReducedMotion&&(a?r=!0:(o=1,s=void 0,c=void 0)),(this.isStopped||this.isLocked)&&!d)return;let m=e,h=n;if(typeof m==`string`&&[`top`,`left`,`start`,`#`].includes(m))m=0;else if(typeof m==`string`&&[`bottom`,`right`,`end`].includes(m))m=this.limit;else{let e=null;if(typeof m==`string`?(e=m.startsWith(`#`)?document.getElementById(m.slice(1)):document.querySelector(m),e||(m===`#top`?m=0:console.warn(`Lenis: Target not found`,m))):m instanceof Element&&(e=m),e){if(this.options.wrapper!==window){let e=this.rootElement.getBoundingClientRect();h-=this.isHorizontal?e.left:e.top}let t=e.getBoundingClientRect(),n=getComputedStyle(e),r=this.isHorizontal?Number.parseFloat(n.scrollMarginLeft):Number.parseFloat(n.scrollMarginTop),i=getComputedStyle(this.rootElement),a=this.isHorizontal?Number.parseFloat(i.scrollPaddingLeft):Number.parseFloat(i.scrollPaddingTop);m=(this.isHorizontal?t.left:t.top)+this.animatedScroll-(Number.isNaN(r)?0:r)-(Number.isNaN(a)?0:a)}}if(typeof m==`number`){if(m+=h,this.options.infinite){if(a){this.targetScroll=this.animatedScroll=this.scroll;let e=m-this.animatedScroll;e>this.limit/2?m-=this.limit:e<-this.limit/2&&(m+=this.limit)}}else m=t(0,m,this.limit);if(m===this.targetScroll){l?.(this),u?.(this);return}if(this.userData=p??{},r){this.animatedScroll=this.targetScroll=m,this.setScroll(this.scroll),this.reset(),this.preventNextNativeScrollEvent(),this.emit(),u?.(this),this.userData={},requestAnimationFrame(()=>{this.dispatchScrollendEvent()});return}a||(this.targetScroll=m),typeof s==`number`&&typeof c!=`function`?c=f:typeof c==`function`&&typeof s!=`number`&&(s=1),this.animate.fromTo(this.animatedScroll,m,{duration:s,easing:c,lerp:o,onStart:()=>{i&&(this.isLocked=!0),this.isScrolling=`smooth`,l?.(this)},onUpdate:(e,t)=>{this.isScrolling=`smooth`,this.lastVelocity=this.velocity,this.velocity=e-this.animatedScroll,this.direction=Math.sign(this.velocity),this.animatedScroll=e,this.setScroll(this.scroll),a&&(this.targetScroll=e),t||this.emit(),t&&(this.reset(),this.emit(),u?.(this),this.userData={},requestAnimationFrame(()=>{this.dispatchScrollendEvent()}),this.preventNextNativeScrollEvent())}})}}preventNextNativeScrollEvent(){this._preventNextNativeScrollEvent=!0,requestAnimationFrame(()=>{this._preventNextNativeScrollEvent=!1})}hasNestedScroll(e,{deltaX:t,deltaY:n}){let r=Date.now();e._lenis||={};let i=e._lenis,a,o,s,c,l,u,d,f,p,m;if(r-(i.time??0)>2e3){i.time=Date.now();let t=window.getComputedStyle(e);if(i.computedStyle=t,a=[`auto`,`overlay`,`scroll`].includes(t.overflowX),o=[`auto`,`overlay`,`scroll`].includes(t.overflowY),l=[`auto`].includes(t.overscrollBehaviorX),u=[`auto`].includes(t.overscrollBehaviorY),i.hasOverflowX=a,i.hasOverflowY=o,!(a||o))return!1;d=e.scrollWidth,f=e.scrollHeight,p=e.clientWidth,m=e.clientHeight,s=d>p,c=f>m,i.isScrollableX=s,i.isScrollableY=c,i.scrollWidth=d,i.scrollHeight=f,i.clientWidth=p,i.clientHeight=m,i.hasOverscrollBehaviorX=l,i.hasOverscrollBehaviorY=u}else s=i.isScrollableX,c=i.isScrollableY,a=i.hasOverflowX,o=i.hasOverflowY,d=i.scrollWidth,f=i.scrollHeight,p=i.clientWidth,m=i.clientHeight,l=i.hasOverscrollBehaviorX,u=i.hasOverscrollBehaviorY;if(!(a&&s||o&&c))return!1;let h=Math.abs(t)>=Math.abs(n)?`horizontal`:`vertical`,g,_,v,y,b,x;if(h===`horizontal`)g=Math.round(e.scrollLeft),_=d-p,v=t,y=a,b=s,x=l;else if(h===`vertical`)g=Math.round(e.scrollTop),_=f-m,v=n,y=o,b=c,x=u;else return!1;return!x&&(g>=_||g<=0)?!0:(v>0?g<_:g>0)&&y&&b}get rootElement(){return this.options.wrapper===window?document.documentElement:this.options.wrapper}get limit(){return this.options.naiveDimensions?this.isHorizontal?this.rootElement.scrollWidth-this.rootElement.clientWidth:this.rootElement.scrollHeight-this.rootElement.clientHeight:this.dimensions.limit[this.isHorizontal?`x`:`y`]}get isHorizontal(){return this.options.orientation===`horizontal`}get actualScroll(){let e=this.options.wrapper;return this.isHorizontal?e.scrollX??e.scrollLeft:e.scrollY??e.scrollTop}get scroll(){return this.options.infinite?i(this.animatedScroll,this.limit):this.animatedScroll}get progress(){return this.limit===0?1:this.scroll/this.limit}get isScrolling(){return this._isScrolling}set isScrolling(e){this._isScrolling!==e&&(this._isScrolling=e,this.updateClassName())}get isStopped(){return this._isStopped}set isStopped(e){this._isStopped!==e&&(this._isStopped=e,this.updateClassName())}get isLocked(){return this._isLocked}set isLocked(e){this._isLocked!==e&&(this._isLocked=e,this.updateClassName())}get isSmooth(){return this.isScrolling===`smooth`}get prefersReducedMotion(){return this.options.respectReducedMotion&&this.reducedMotionMediaQuery.matches}get className(){let e=`lenis`;return this.options.autoToggle&&(e+=` lenis-autoToggle`),this.isStopped&&(e+=` lenis-stopped`),this.isLocked&&(e+=` lenis-locked`),this.isScrolling&&(e+=` lenis-scrolling`),this.isScrolling===`smooth`&&(e+=` lenis-smooth`),e}updateClassName(){this.cleanUpClassName(),this.className.split(` `).forEach(e=>{this.rootElement.classList.add(e)})}cleanUpClassName(){for(let e of Array.from(this.rootElement.classList))(e===`lenis`||e.startsWith(`lenis-`))&&this.rootElement.classList.remove(e)}};globalThis.Lenis=p,globalThis.Lenis.prototype=p.prototype})();

;(function(){var d=document,H=d.documentElement;
/* 0) 进度条：缓存总高，只写 transform */
var tot=1,pt=false;function rec(){tot=Math.max(1,H.scrollHeight-innerHeight);}rec();addEventListener('resize',rec,{passive:true});
setInterval(rec,2500);addEventListener('load',rec);
addEventListener('scroll',function(){if(pt)return;pt=true;requestAnimationFrame(function(){pt=false;var g=d.getElementById('prog');if(g)g.style.transform='scaleX('+(scrollY/tot).toFixed(4)+')';});},{passive:true});
/* 1) 离屏暂停无限动画 */
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){e.target.classList.toggle('live',e.isIntersecting);});},{rootMargin:'120px 0px'});
 d.querySelectorAll('figure,.hero,.act3wrap,.fc-wrap').forEach(function(x){io.observe(x);});}
/* 2) 惯性平滑滚动（桌面滚轮；触屏保持原生） */
var touch=matchMedia('(pointer:coarse)').matches,rm=matchMedia('(prefers-reduced-motion:reduce)').matches;
if(window.Lenis&&!touch&&!rm){
 d.querySelectorAll('.side,.zoverlay,.fc-back,.tw,.fscroll,.rpane,.mklegend').forEach(function(x){x.setAttribute('data-lenis-prevent','');});
 var L=new Lenis({duration:1.05,easing:function(t){return Math.min(1,1.001-Math.pow(2,-10*t));},smoothWheel:true,wheelMultiplier:1,touchMultiplier:1.2});
 window.__lenis=L;function raf(t){L.raf(t);requestAnimationFrame(raf);}requestAnimationFrame(raf);
 new MutationObserver(function(){var o=d.querySelector('.zoverlay');if(o){o.setAttribute('data-lenis-prevent','');L.stop();}else L.start();}).observe(d.body,{childList:true});
}
})();

}catch(e){console.error(e)}
try{
(function(){var d=document,R=d.documentElement,btn=d.getElementById('themeBtn');if(!btn)return;var ls;try{ls=localStorage}catch(e){}
var TH=[["auto", "🌓", "跟随系统"], ["light", "📜", "羊皮纸"], ["forest", "🌲", "森林"], ["ocean", "🌊", "海洋"], ["rose", "🌸", "玫瑰"], ["ink", "🖋️", "墨韵"], ["dark", "🌙", "夜读"], ["starry", "✨", "星空"]],SW={"auto": "linear-gradient(90deg,#F6F2E8 50%,#13151B 50%)", "light": "#F6F2E8", "forest": "#1E6B45", "ocean": "#1565C0", "rose": "#C2185B", "ink": "#111", "dark": "#1A1D25", "starry": "linear-gradient(135deg,#17183A,#7B5CFF)"};
function apply(k){if(k==='auto')R.removeAttribute('data-theme');else R.setAttribute('data-theme',k);
 var t=TH.filter(function(x){return x[0]===k;})[0]||TH[0];btn.textContent=t[1]+' '+t[2];try{ls&&ls.setItem('hc-theme',k);}catch(e){}
 p.querySelectorAll('button').forEach(function(b){b.classList.toggle('cur',b.dataset.k===k);});}
var p=d.createElement('div');p.className='thpick';p.innerHTML=TH.map(function(t){return '<button type="button" data-k="'+t[0]+'"><i style="background:'+SW[t[0]]+'"></i>'+t[1]+' '+t[2]+'</button>';}).join('');d.body.appendChild(p);
var k='auto';try{k=(ls&&ls.getItem('hc-theme'))||'auto';}catch(e){}apply(k);
btn.onclick=function(e){e.stopPropagation();p.classList.toggle('on');};
p.addEventListener('click',function(e){var b=e.target.closest('button');if(b){apply(b.dataset.k);p.classList.remove('on');}});
d.addEventListener('click',function(e){if(!e.target.closest('.thpick'))p.classList.remove('on');});
})();

(function(){var d=document,sh=d.querySelector('.shell'),side=d.querySelector('.side');if(!sh||!side)return;var ls;try{ls=localStorage}catch(e){}
try{var w=ls&&ls.getItem('hc-tocw');if(w)sh.style.setProperty('--tocw',w+'px');}catch(e){}
var g=d.createElement('div');g.className='tocgrip';g.title='拖动调整目录宽度（双击复原）';side.appendChild(g);
var x0,w0;g.addEventListener('pointerdown',function(e){x0=e.clientX;w0=side.getBoundingClientRect().width;g.setPointerCapture(e.pointerId);g.classList.add('drag');d.body.classList.add('tocdrag');});
g.addEventListener('pointermove',function(e){if(x0==null)return;var nw=Math.max(200,Math.min(620,w0+e.clientX-x0));sh.style.setProperty('--tocw',nw+'px');});
function end(){if(x0==null)return;x0=null;g.classList.remove('drag');d.body.classList.remove('tocdrag');try{ls&&ls.setItem('hc-tocw',Math.round(side.getBoundingClientRect().width));}catch(e){}}
g.addEventListener('pointerup',end);g.addEventListener('pointercancel',end);
g.addEventListener('dblclick',function(){sh.style.removeProperty('--tocw');try{ls&&ls.removeItem('hc-tocw');}catch(e){}});
/* 当前页的主日链接也高亮页面分组 */
var cur=location.pathname.split('/').pop()||'index.html';d.querySelectorAll('.toc a').forEach(function(a){var h=a.getAttribute('href')||'';if(h.charAt(0)==='#'||h.indexOf(cur)===0)a.classList.add('here');});
})();

(function(){var d=document,f=d.getElementById('fab');if(!f)return;
function to(y){var L=window.__lenis;if(L)L.scrollTo(y,{duration:1.0});else scrollTo({top:y,behavior:'smooth'});}
f.addEventListener('click',function(e){var b=e.target.closest('[data-f]');if(!b)return;var k=b.dataset.f;
 if(k==='tog'){f.classList.toggle('open');return;}
 if(k==='back')history.back();else if(k==='fwd')history.forward();else if(k==='top')to(0);else if(k==='bot')to(d.documentElement.scrollHeight);});
if(matchMedia('(hover:hover)').matches){f.addEventListener('mouseenter',function(){f.classList.add('open');});f.addEventListener('mouseleave',function(){f.classList.remove('open');});}
d.addEventListener('click',function(e){if(!e.target.closest('#fab'))f.classList.remove('open');});
})();

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

}catch(e){console.error(e)}

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
