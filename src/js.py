# -*- coding: utf-8 -*-
JS = r"""
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
"""
