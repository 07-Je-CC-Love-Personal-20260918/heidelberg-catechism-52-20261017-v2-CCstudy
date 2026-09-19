# -*- coding: utf-8 -*-
CSS = r"""
:root{
  --paper:#F6F2E8;--paper-2:#FFFDF7;--paper-3:#F0EADC;--rule:#DCD2BE;
  --ink:#14161C;--ink-2:#474339;--muted:#7C776C;
  --royal:#1F3864;--rubric:#9B1B1E;--brass:#A07622;--teal:#1E5F5B;--plum:#5B3A6E;
  --misery:#9B1B1E;--deliver:#1F3864;--gratitude:#A07622;--prologue:#4A4740;
  --sh:0 1px 2px rgba(20,22,28,.05);
  --serif:"Songti SC","Noto Serif CJK SC","Noto Serif SC","Source Han Serif SC",
    "PingFang SC","Microsoft YaHei",Georgia,serif;
  --disp:"Optima","Songti SC","Noto Serif CJK SC","STZhongsong","Microsoft YaHei",Georgia,serif;
  --sans:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB",
    "Microsoft YaHei","Helvetica Neue",Arial,sans-serif;
  --mono:"SF Mono",Menlo,Consolas,monospace;
}
:root[data-theme="dark"]{
  --paper:#13151B;--paper-2:#1A1D25;--paper-3:#20242E;--rule:#333A47;
  --ink:#E9E4D8;--ink-2:#BDB7A8;--muted:#8B8577;
  --royal:#8FB4EA;--rubric:#E58E90;--brass:#D6B368;--teal:#6FC4BC;--plum:#B99AD1;
  --misery:#E58E90;--deliver:#8FB4EA;--gratitude:#D6B368;--prologue:#9A958A;
  --sh:0 1px 2px rgba(0,0,0,.4);
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#13151B;--paper-2:#1A1D25;--paper-3:#20242E;--rule:#333A47;
    --ink:#E9E4D8;--ink-2:#BDB7A8;--muted:#8B8577;
    --royal:#8FB4EA;--rubric:#E58E90;--brass:#D6B368;--teal:#6FC4BC;--plum:#B99AD1;
    --misery:#E58E90;--deliver:#8FB4EA;--gratitude:#D6B368;--prologue:#9A958A;
    --sh:0 1px 2px rgba(0,0,0,.4);
  }
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--serif);
  font-size:17px;line-height:1.86;overflow-x:hidden;
  background-image:radial-gradient(rgba(160,118,34,.05) 1px,transparent 1px);
  background-size:24px 24px}
a{color:var(--royal);text-decoration:none}
a:hover{text-decoration:underline}
:focus-visible{outline:2px solid var(--brass);outline-offset:2px}
strong,b{color:var(--royal)}
::selection{background:rgba(160,118,34,.25)}

/* progress */
#prog{position:fixed;top:0;left:0;height:2px;background:var(--rubric);z-index:90;width:0}

/* topbar */
.topbar{position:sticky;top:0;z-index:60;background:color-mix(in srgb,var(--paper) 93%,transparent);
  backdrop-filter:saturate(1.3) blur(10px);border-bottom:1px solid var(--rule)}
.tb{max-width:1560px;margin:0 auto;display:flex;align-items:center;gap:8px;padding:7px 14px;flex-wrap:wrap}
.brand{font-family:var(--disp);font-size:13px;letter-spacing:.16em;color:var(--royal);
  white-space:nowrap;font-weight:600}
.brand b{color:var(--rubric)}
.sp{flex:1}
.tbs{flex:0 1 230px;min-width:0}
.tbs input{width:100%;font-family:var(--sans);font-size:13px;padding:7px 10px;
  border:1px solid var(--rule);background:var(--paper-2);color:var(--ink);border-radius:3px}
.btn{font-family:var(--sans);font-size:12px;letter-spacing:.05em;padding:7px 10px;
  border:1px solid var(--rule);background:var(--paper-2);color:var(--ink-2);
  cursor:pointer;border-radius:3px;white-space:nowrap;transition:.15s}
.btn:hover{border-color:var(--brass);color:var(--ink)}
.btn.on{background:var(--royal);border-color:var(--royal);color:var(--paper)}


/* layout + collapsible toc */
.shell{max-width:1560px;margin:0 auto;display:grid;grid-template-columns:300px minmax(0,1fr);
  transition:grid-template-columns .22s ease}
.shell.hid{grid-template-columns:0 minmax(0,1fr)}
.shell.hid .side{opacity:0;pointer-events:none;overflow:hidden;padding:0;border-right:0;width:0}
.side{position:sticky;top:46px;height:calc(100vh - 46px);overflow-y:auto;
  border-right:1px solid var(--rule);padding:16px 12px 70px;scrollbar-width:thin;
  transition:opacity .18s}
.side::-webkit-scrollbar{width:6px}
.side::-webkit-scrollbar-thumb{background:var(--rule);border-radius:3px}
.toc-h{font-family:var(--sans);font-size:10px;letter-spacing:.22em;color:var(--muted);
  margin:15px 0 6px;padding-bottom:5px;border-bottom:1px solid var(--rule)}
.toc-h:first-child{margin-top:0}
.toc a{display:block;font-size:13.7px;line-height:1.45;padding:4px 7px 4px 9px;color:var(--ink-2);
  border-left:2px solid transparent;border-radius:0 2px 2px 0}
.toc a:hover{background:rgba(160,118,34,.09);text-decoration:none;color:var(--ink)}
.toc a.active{border-left-color:var(--rubric);color:var(--royal);background:rgba(31,56,100,.07);
  font-weight:600}
.toc a .no{font-family:var(--sans);font-size:10.5px;color:var(--muted);display:inline-block;min-width:2.5em}
.toc a.done .no::after{content:"✓";color:var(--brass);margin-left:2px}
#tocOpen{position:fixed;left:0;top:96px;z-index:58;display:none;writing-mode:vertical-rl;
  padding:12px 5px;border:1px solid var(--rule);border-left:0;background:var(--paper-2);
  color:var(--royal);cursor:pointer;font-family:var(--sans);font-size:12px;letter-spacing:.2em;
  border-radius:0 4px 4px 0}
.shell.hid ~ #tocOpen{display:block}
.main{padding:0 34px 110px;min-width:0}

/* hero */
.hero{padding:62px 0 38px;border-bottom:2px solid var(--royal)}
.hero .lat{font-family:var(--disp);letter-spacing:.42em;font-size:11.5px;color:var(--brass)}
.hero h1{font-family:var(--disp);font-size:clamp(34px,6.4vw,62px);margin:14px 0 4px;
  letter-spacing:.08em;line-height:1.08;color:var(--royal);font-weight:700}
.hero .zh{font-size:clamp(14px,2.3vw,18px);color:var(--ink-2);letter-spacing:.12em}
.hero .rl{width:66px;height:3px;background:var(--rubric);margin:22px 0}
.hero .ld{max-width:46em;font-size:17.5px;color:var(--ink-2)}
.hero .stats{display:flex;flex-wrap:wrap;gap:12px 28px;margin-top:26px;
  font-family:var(--sans);font-size:10.5px;letter-spacing:.14em;color:var(--muted)}
.hero .stats b{display:block;font-family:var(--disp);font-size:27px;color:var(--rubric);line-height:1.15}

/* sections */
section{scroll-margin-top:62px}
.sec{padding:42px 0 6px;border-top:1px solid var(--rule);margin-top:34px}
.eyebrow{font-family:var(--sans);font-size:10px;letter-spacing:.26em;color:var(--brass);margin-bottom:8px}
.sec h2{font-family:var(--disp);font-size:clamp(22px,3.4vw,31px);margin:0 0 12px;
  color:var(--royal);letter-spacing:.04em;line-height:1.3}
.lead{font-size:17.5px;color:var(--ink-2);max-width:47em;border-left:3px solid var(--brass);
  padding-left:16px;margin:0 0 26px}
.blk{margin:0 0 22px;max-width:51em}
.blk h3{font-family:var(--sans);font-size:13.5px;letter-spacing:.04em;color:var(--rubric);
  margin:0 0 5px;font-weight:600}
.blk p{margin:0}

/* figures */
figure{margin:28px 0;border:1px solid var(--rule);background:var(--paper-2);padding:18px;
  box-shadow:var(--sh);border-radius:3px}
figcaption{font-family:var(--sans);font-size:10.5px;letter-spacing:.16em;color:var(--muted);
  margin-bottom:15px;padding-bottom:7px;border-bottom:1px solid var(--rule);line-height:1.7}
.fnote{margin:14px 0 0;font-size:14px;color:var(--muted);line-height:1.75}
.svgfig{width:100%;height:auto;display:block;overflow:visible}

.fscroll{overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch}
.fscroll::-webkit-scrollbar{height:6px}
.fscroll::-webkit-scrollbar-thumb{background:var(--rule);border-radius:3px}

/* svg common */
.grat{stroke:var(--rule);stroke-width:.7;stroke-dasharray:2 4}
.grat-l{fill:var(--muted);font-size:9px;font-family:var(--sans)}
.region{fill:rgba(31,56,100,.05);stroke:var(--rule);stroke-width:1;stroke-dasharray:5 4}
.region-l{fill:var(--muted);font-size:11px;font-family:var(--sans);letter-spacing:.18em}
.flow{fill:none;stroke:var(--brass);stroke-width:1.6;stroke-dasharray:7 6;opacity:.85}
.in .flow{animation:march 2.4s linear infinite}
.flow-l{fill:var(--ink-2);font-size:10.5px;font-family:var(--sans)}
.node{fill:var(--paper-2);stroke:var(--royal);stroke-width:2}
.node-big{stroke-width:2.5}
.node-key{fill:var(--rubric);stroke:var(--rubric)}
.pulse{fill:none;stroke:var(--rubric);stroke-width:2;opacity:0}
.in .pulse{animation:pulse 2.6s ease-out infinite}
.city{fill:var(--ink);font-size:13px;font-family:var(--serif);font-weight:600;
  paint-order:stroke;stroke:var(--paper-2);stroke-width:3.5px;stroke-linejoin:round}
.city-n{fill:var(--muted);font-size:10px;font-family:var(--sans);
  paint-order:stroke;stroke:var(--paper-2);stroke-width:3px}
.axis{stroke:var(--rule);stroke-width:1}
.axis-l{fill:var(--muted);font-size:11px;font-family:var(--sans);letter-spacing:.14em}
.cbox{fill:var(--paper-3);stroke:var(--rule);stroke-width:1}
.cbox.c0{fill:rgba(91,58,110,.12);stroke:var(--plum)}
.cbox.c1{fill:rgba(155,27,30,.09);stroke:var(--rubric)}
.cbox.c2{fill:rgba(31,56,100,.09);stroke:var(--royal)}
.cbox.c3{fill:rgba(160,118,34,.09);stroke:var(--brass)}
.cbox.c4{fill:rgba(30,95,91,.10);stroke:var(--teal)}
.cbox-t{fill:var(--ink);font-size:14.5px;font-weight:600;font-family:var(--serif)}
.cbox-s{fill:var(--muted);font-size:11.5px;font-family:var(--sans)}
.carrow{fill:none;stroke:var(--brass);stroke-width:1.6;marker-end:none}
.carrow.dash{stroke-dasharray:6 5}
.in .carrow.dash{animation:march 2.6s linear infinite}
.clab{fill:var(--ink-2);font-size:12.5px;font-family:var(--sans)}
.clab.mid{fill:var(--muted)}
.seg-m{fill:var(--misery);opacity:.86}.seg-d{fill:var(--deliver);opacity:.86}
.seg-g{fill:var(--gratitude);opacity:.86}
.seg-t{fill:var(--paper);font-size:14px;font-family:var(--disp);letter-spacing:.1em}
.seg-s{fill:var(--paper);font-size:11px;font-family:var(--sans);opacity:.85}
.seg-p{fill:var(--ink-2);font-size:12px;font-family:var(--sans)}
.fl{stroke-width:1.4}
.fl.f1{fill:rgba(160,118,34,.14);stroke:var(--brass)}
.fl.f2{fill:rgba(31,56,100,.12);stroke:var(--royal)}
.fl.f3{fill:rgba(30,95,91,.10);stroke:var(--teal)}
.fl-t{fill:var(--ink);font-size:14px;font-weight:600;font-family:var(--serif)}
.fl-s{fill:var(--muted);font-size:11.5px;font-family:var(--sans)}
.fl-n{fill:var(--muted);font-size:11.5px;font-family:var(--sans);letter-spacing:.1em}
.para{fill:none;stroke:var(--rubric);stroke-width:2.4;stroke-linejoin:round;
  stroke-dasharray:2400;stroke-dashoffset:2400}
.in .para{animation:draw 2.2s ease-out forwards}
.pnode{fill:var(--paper-2);stroke:var(--rubric);stroke-width:2}
.pt-l{fill:var(--ink);font-size:12.5px;font-family:var(--serif)}
.pt-s{fill:var(--muted);font-size:10px;font-family:var(--sans)}
.mind-c{fill:rgba(31,56,100,.10);stroke:var(--royal);stroke-width:2}
.mind-ct{fill:var(--royal);font-size:19px;font-family:var(--disp);font-weight:700}
.mind-cs{fill:var(--muted);font-size:11.5px;font-family:var(--sans)}
.mind-b{fill:none;stroke-width:1.6;stroke-dasharray:600;stroke-dashoffset:600}
.in .mind-b{animation:draw 1.4s ease-out forwards}
.mind-tw{stroke-width:1;opacity:.55}
.mind-b.misery,.mind-tw.misery,.mind-n.misery{stroke:var(--misery)}
.mind-b.deliver,.mind-tw.deliver,.mind-n.deliver{stroke:var(--deliver)}
.mind-b.gratitude,.mind-tw.gratitude,.mind-n.gratitude{stroke:var(--gratitude)}
.mind-b.prologue,.mind-tw.prologue,.mind-n.prologue{stroke:var(--prologue)}
.mind-n{fill:var(--paper-2);stroke-width:2}
.mind-l{fill:var(--ink);font-size:12.5px;font-family:var(--serif);font-weight:600;
  paint-order:stroke;stroke:var(--paper-2);stroke-width:3.5px}
.mind-leaf{fill:var(--paper-2);stroke-width:1.6}
.mind-leaf.misery{stroke:var(--misery)}.mind-leaf.deliver{stroke:var(--deliver)}
.mind-leaf.gratitude{stroke:var(--gratitude)}.mind-leaf.prologue{stroke:var(--prologue)}
.mind-num{fill:var(--ink-2);font-size:10.5px;font-family:var(--sans)}

/* acts / chain / flow */
.acts{display:grid;grid-template-columns:repeat(8,1fr);gap:0;border:1px solid var(--rule)}
.act{padding:13px 11px;border-right:1px solid var(--rule);opacity:0;transform:translateY(12px)}
.in .act{animation:fadeup .5s ease forwards}
.act:nth-child(1){animation-delay:.02s}.act:nth-child(2){animation-delay:.08s}
.act:nth-child(3){animation-delay:.14s}.act:nth-child(4){animation-delay:.2s}
.act:nth-child(5){animation-delay:.26s}.act:nth-child(6){animation-delay:.32s}
.act:nth-child(7){animation-delay:.38s}.act:nth-child(8){animation-delay:.44s}
.act:last-child{border-right:0}
.act-n{font-family:var(--sans);font-size:9.5px;letter-spacing:.2em;color:var(--brass)}
.act-t{font-family:var(--disp);font-size:17px;color:var(--royal);margin:3px 0 2px}
.act-r{font-family:var(--sans);font-size:10.5px;color:var(--muted);margin-bottom:6px}
.act-g{font-size:13px;line-height:1.6;color:var(--ink-2)}
.act-h{margin-top:7px;font-family:var(--sans);font-size:10.5px;color:var(--rubric)}
.act.a1{background:rgba(160,118,34,.07)}.act.a2{background:rgba(155,27,30,.07)}
.act.a3,.act.a4,.act.a5{background:rgba(30,95,91,.06)}
.act.a6{background:rgba(31,56,100,.10)}.act.a7{background:rgba(31,56,100,.06)}
.act.a8{background:rgba(160,118,34,.12)}

.chain{display:grid;justify-items:center;gap:0}
.ch{width:min(560px,100%);border:1px solid var(--rule);background:var(--paper-3);
  padding:11px 16px;display:grid;grid-template-columns:62px 1fr auto;gap:12px;align-items:baseline;
  opacity:0;transform:translateX(-14px);border-radius:3px}
.in .ch{animation:slidein .45s ease forwards;animation-delay:calc(var(--i)*.09s)}
.ch-who{font-family:var(--sans);font-size:10px;letter-spacing:.14em;color:var(--brass)}
.ch-n{font-size:15.5px;color:var(--royal);font-weight:600}
.ch-r{font-family:var(--sans);font-size:11px;color:var(--muted)}
.ch-g{grid-column:2/4;font-size:13.5px;color:var(--ink-2);line-height:1.6}
.ch-a{color:var(--brass);font-size:15px;line-height:1;padding:3px 0;opacity:0}
.in .ch-a{animation:fadein .3s ease forwards;animation-delay:calc(var(--i)*.09s + .25s)}

.flowh{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}
.fx{border:1px solid var(--rule);background:var(--paper-3);padding:12px 11px;position:relative;
  opacity:0;border-radius:3px}
.in .fx{animation:fadeup .45s ease forwards;animation-delay:calc(var(--i)*.1s)}
.fx-end{background:rgba(30,95,91,.12);border-color:var(--teal)}
.fx-n{font-family:var(--disp);font-size:20px;color:var(--brass);line-height:1}
.fx-t{font-size:14.5px;color:var(--royal);font-weight:600;margin:5px 0 2px}
.fx-r{font-family:var(--sans);font-size:10.5px;color:var(--muted)}
.fx-g{font-size:12.5px;color:var(--ink-2);margin-top:5px;line-height:1.55}

/* timeline */
.tl-row{display:grid;grid-template-columns:70px 1fr;gap:12px;position:relative;padding:7px 0}
.tl-row::before{content:"";position:absolute;left:77px;top:0;bottom:0;width:1px;background:var(--rule)}
.tl-row:first-child::before{top:50%}.tl-row:last-child::before{bottom:50%}
.tl-yr{font-family:var(--disp);font-size:14px;color:var(--rubric);text-align:right;letter-spacing:.02em}
.tl-body{padding-left:16px;position:relative}
.tl-body::before{content:"";position:absolute;left:-4.5px;top:11px;width:9px;height:9px;
  border-radius:50%;background:var(--paper-2);border:2px solid var(--brass)}
.tl-row.key .tl-body::before{background:var(--rubric);border-color:var(--rubric)}
.tl-t{font-size:15.5px;line-height:1.45}
.tl-d{font-size:13.5px;color:var(--muted);line-height:1.5}

/* tables */
.tw{overflow-x:auto;margin:24px 0;border:1px solid var(--rule);background:var(--paper-2);
  box-shadow:var(--sh);border-radius:3px}
table{border-collapse:collapse;width:100%;font-size:14px;min-width:640px}
th{font-family:var(--sans);font-size:11px;letter-spacing:.1em;text-align:left;padding:10px 12px;
  background:var(--royal);color:var(--paper);font-weight:500;white-space:nowrap;position:sticky;top:0}
:root[data-theme="dark"] th{color:#12141A}
td{padding:9px 12px;border-top:1px solid var(--rule);vertical-align:top;line-height:1.62}
tbody tr:nth-child(even){background:rgba(160,118,34,.055)}
tbody tr:hover{background:rgba(31,56,100,.06)}
td:first-child{color:var(--royal);font-weight:600;white-space:nowrap}

/* 52 grid */
.grid52{display:grid;grid-template-columns:repeat(13,1fr);gap:4px}
.g52{aspect-ratio:1;display:flex;align-items:center;justify-content:center;font-family:var(--disp);
  font-size:12.5px;border:1px solid var(--rule);background:var(--paper-2);color:var(--ink-2);
  cursor:pointer;text-decoration:none;transition:transform .12s,background .12s;border-radius:2px}
.g52:hover{transform:translateY(-2px);text-decoration:none;border-color:var(--brass)}
.g52.prologue{border-left:3px solid var(--prologue)}
.g52.misery{border-left:3px solid var(--misery)}
.g52.deliver{border-left:3px solid var(--deliver)}
.g52.gratitude{border-left:3px solid var(--gratitude)}
.g52.done{background:var(--brass);color:var(--paper);border-color:var(--brass)}
.legend{display:flex;flex-wrap:wrap;gap:14px;margin-top:13px;font-family:var(--sans);
  font-size:11px;letter-spacing:.06em;color:var(--muted)}
.legend i{display:inline-block;width:10px;height:10px;margin-right:6px;vertical-align:-1px}

/* mind map (horizontal tree) */
.mm{position:relative;padding-left:4px}
.mm-root{border:1px solid var(--royal);background:rgba(31,56,100,.09);padding:12px 18px;
  border-radius:3px;display:inline-block;margin-bottom:6px}
.mm-root b{font-family:var(--disp);font-size:19px;color:var(--royal);display:block;letter-spacing:.04em}
.mm-root span{font-family:var(--sans);font-size:11px;color:var(--muted)}
.mm-br{display:grid;grid-template-columns:132px 1fr;gap:14px;padding:12px 0 12px 22px;
  position:relative;border-left:2px solid var(--rule)}
.mm-br::before{content:"";position:absolute;left:0;top:30px;width:20px;height:2px;background:var(--rule)}
.mm-br.prologue{border-left-color:var(--prologue)}.mm-br.prologue::before{background:var(--prologue)}
.mm-br.misery{border-left-color:var(--misery)}.mm-br.misery::before{background:var(--misery)}
.mm-br.deliver{border-left-color:var(--deliver)}.mm-br.deliver::before{background:var(--deliver)}
.mm-br.gratitude{border-left-color:var(--gratitude)}.mm-br.gratitude::before{background:var(--gratitude)}
.mm-bh b{display:block;font-family:var(--disp);font-size:19px;color:var(--royal);letter-spacing:.06em}
.mm-bh i{display:block;font-family:var(--sans);font-style:normal;font-size:9.5px;
  letter-spacing:.2em;color:var(--brass)}
.mm-bh em{display:block;font-family:var(--sans);font-style:normal;font-size:11px;
  color:var(--muted);margin-top:4px}
.mm-cls{display:grid;gap:7px}
.mm-cl{display:grid;grid-template-columns:104px 1fr;gap:10px;align-items:start;
  border-left:1px dashed var(--rule);padding-left:12px}
.mm-cn{font-size:14px;color:var(--ink);font-weight:600;line-height:1.5}
.mm-chips{display:flex;flex-wrap:wrap;gap:5px}
.chip{display:inline-flex;align-items:baseline;gap:5px;border:1px solid var(--rule);
  background:var(--paper-3);padding:2px 8px;border-radius:12px;font-size:12.5px;
  color:var(--ink-2);text-decoration:none;transition:.12s}
.chip:hover{border-color:var(--brass);color:var(--ink);text-decoration:none;transform:translateY(-1px)}
.chip b{font-family:var(--disp);font-size:12px;color:var(--rubric)}
@media (max-width:740px){
  .mm-br{grid-template-columns:1fr;gap:8px}
  .mm-cl{grid-template-columns:1fr;gap:4px}
}

/* creed cards */
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:16px}
.card{border:1px solid var(--rule);background:var(--paper-2);border-top:3px solid var(--brass);
  padding:18px;box-shadow:var(--sh);border-radius:3px}
.card h3{margin:0;font-family:var(--disp);font-size:20px;color:var(--royal);letter-spacing:.03em}
.card .lt{font-family:var(--disp);font-size:10px;letter-spacing:.2em;color:var(--brass);margin:4px 0 2px}
.card .dt{font-family:var(--sans);font-size:11px;color:var(--muted);margin-bottom:10px}
.card dl{margin:0}
.card dt{font-family:var(--sans);font-size:9.5px;letter-spacing:.22em;color:var(--brass);
  margin-top:11px;padding-bottom:3px;border-bottom:1px solid var(--rule)}
.card dd{margin:6px 0 0;font-size:14.5px;line-height:1.72;color:var(--ink-2)}
.card .kq{background:rgba(31,56,100,.06);border-left:2px solid var(--royal);padding:8px 12px;
  color:var(--ink);font-size:15px}

/* LD cards */
.part-div{margin:52px 0 6px;padding:20px 0 12px;border-top:3px double var(--royal);
  display:flex;align-items:baseline;gap:18px;flex-wrap:wrap}
.part-div .n{font-family:var(--disp);font-size:10.5px;letter-spacing:.3em;color:var(--brass)}
.part-div h2{font-family:var(--disp);font-size:clamp(23px,3.8vw,33px);margin:0;color:var(--royal)}
.part-div .zh{font-size:13.5px;color:var(--muted)}
.ld{border:1px solid var(--rule);background:var(--paper-2);margin:24px 0;box-shadow:var(--sh);
  border-radius:3px;content-visibility:auto;contain-intrinsic-size:auto 900px}
.ld.prologue{border-left:4px solid var(--prologue)}
.ld.misery{border-left:4px solid var(--misery)}
.ld.deliver{border-left:4px solid var(--deliver)}
.ld.gratitude{border-left:4px solid var(--gratitude)}
.ld-h{padding:17px 24px 13px;border-bottom:1px solid var(--rule);display:flex;
  align-items:flex-start;gap:16px;flex-wrap:wrap;background:var(--paper-3)}
.ld-no{font-family:var(--disp);font-size:33px;line-height:1;color:var(--rubric);min-width:1.5em}
.ld-ht{flex:1;min-width:190px}
.ld-ht h3{margin:0;font-size:22px;letter-spacing:.02em;color:var(--royal);line-height:1.3}
.ld-meta{font-family:var(--sans);font-size:10.5px;letter-spacing:.12em;color:var(--muted);margin-top:5px}
.ld-meta span{margin-right:13px}
.chk{font-family:var(--sans);font-size:11px;color:var(--muted);cursor:pointer;display:flex;
  align-items:center;gap:6px;user-select:none;white-space:nowrap}
.chk input{accent-color:var(--brass);width:15px;height:15px;cursor:pointer}
.ld-b{padding:19px 24px 23px}
.qa{border-left:2px solid var(--brass);padding:2px 0 2px 16px;margin:0 0 15px}
.qa .qn{font-family:var(--disp);font-size:11.5px;color:var(--rubric);letter-spacing:.14em}
.qa .q{font-weight:600;color:var(--royal);margin:2px 0 4px}
.qa .a{margin:0}
.qa .a::before{content:"答 ";font-family:var(--sans);font-size:10.5px;letter-spacing:.18em;color:var(--brass)}
.core{background:rgba(31,56,100,.07);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);
  padding:13px 18px;margin:17px 0;font-size:17.5px;line-height:1.72;color:var(--royal)}
.core::before{content:"本质核心";display:block;font-family:var(--sans);font-size:9.5px;
  letter-spacing:.26em;color:var(--brass);margin-bottom:4px}
.field{margin:15px 0}
.flab{font-family:var(--sans);font-size:10px;letter-spacing:.24em;color:var(--brass);
  padding-bottom:4px;border-bottom:1px solid var(--rule);margin-bottom:8px}
.field p{margin:0 0 8px}
.pt{margin:0 0 10px;padding-left:16px;position:relative}
.pt::before{content:"";position:absolute;left:0;top:.74em;width:6px;height:6px;background:var(--brass)}
.vs{font-size:14px;color:var(--ink-2);font-family:var(--sans);line-height:1.85}
.cf{font-family:var(--sans);font-size:13px;color:var(--royal);background:rgba(31,56,100,.06);
  padding:8px 12px;border-left:2px solid var(--royal)}
.memo{background:rgba(160,118,34,.12);border-left:3px solid var(--brass);padding:12px 16px;font-size:15.5px}
.memo::before{content:"记忆钥匙";display:block;font-family:var(--sans);font-size:9.5px;
  letter-spacing:.26em;color:var(--brass);margin-bottom:4px}
.logic{border-left:2px solid var(--royal);background:rgba(31,56,100,.05);padding:11px 16px;
  font-size:15.5px;line-height:1.76}
.logic::before{content:"逻辑推进 · 承前启后";display:block;font-family:var(--sans);font-size:9.5px;
  letter-spacing:.22em;color:var(--royal);margin-bottom:4px}
.caution{border-left:3px solid var(--rubric);background:rgba(155,27,30,.07);padding:12px 16px;
  font-size:15.5px;line-height:1.76}
.caution::before{content:"误读警示";display:block;font-family:var(--sans);font-size:9.5px;
  letter-spacing:.26em;color:var(--rubric);margin-bottom:4px}
.terms{display:grid;gap:9px}
.term{display:grid;grid-template-columns:minmax(0,auto) 1fr;gap:14px;align-items:baseline}
.gk{font-family:"Palatino Linotype",Palatino,"Times New Roman",serif;font-style:italic;
  color:var(--royal);font-size:18px;white-space:nowrap}
.hb{font-family:"Times New Roman","SBL Hebrew",serif;direction:rtl;unicode-bidi:isolate;
  color:var(--royal);font-size:20px;white-space:nowrap;line-height:1.6}
.ltn{font-family:"Palatino Linotype",Palatino,serif;font-style:italic;color:var(--royal);font-size:17px}
.tgloss{font-size:14.5px;color:var(--ink-2);line-height:1.65}
.tgloss i{font-family:var(--sans);font-style:normal;font-size:11.5px;color:var(--muted);margin-right:9px}

.ch-field{fill:rgba(31,56,100,.08);stroke:var(--royal);stroke-width:1.6}
.ch-ct{fill:var(--royal);font-size:20px;font-family:var(--disp);font-weight:700}
.ch-cs{fill:var(--muted);font-size:12.5px;font-family:var(--sans)}
.ch-e{fill:var(--ink);font-size:15px;font-weight:600;font-family:var(--serif)}
.ch-g{fill:var(--brass);font-size:12px;font-family:"Palatino Linotype",Palatino,serif;font-style:italic}
.ch-x{fill:var(--rubric);font-size:12.5px;font-family:var(--sans)}
.ch-w{fill:var(--muted);font-size:11.5px;font-family:var(--sans)}
.ch-a{stroke:var(--rubric);stroke-width:1.4;stroke-dasharray:4 4;fill:none}
.ch-n{fill:var(--muted);font-size:12px;font-family:var(--sans)}
.as-top{fill:rgba(160,118,34,.16);stroke:var(--brass);stroke-width:1.4}
.as-tt{fill:var(--royal);font-size:17px;font-family:var(--disp);font-weight:700}
.as-col{stroke-width:1.4}
.as-col.p1{fill:rgba(31,56,100,.09);stroke:var(--royal)}
.as-col.p2{fill:rgba(30,95,91,.10);stroke:var(--teal)}
.as-col.p3{fill:rgba(160,118,34,.10);stroke:var(--brass)}
.as-h{fill:var(--ink);font-size:15.5px;font-weight:600;font-family:var(--serif)}
.as-s{fill:var(--rubric);font-size:11.5px;font-family:var(--sans)}
.as-r{fill:var(--muted);font-size:11px;font-family:var(--sans)}
.as-q{fill:var(--ink-2);font-size:11.5px;font-family:var(--serif)}
.as-base{fill:var(--paper-3);stroke:var(--rule);stroke-width:1}
.as-b{fill:var(--ink-2);font-size:12.5px;font-family:var(--sans)}
.sp-z{fill:var(--muted);font-size:11.5px;font-family:var(--sans);letter-spacing:.1em}
.sv{stroke-width:1.4;fill:var(--paper-3);stroke:var(--rule)}
.sv.sv-r{fill:rgba(155,27,30,.08);stroke:var(--rubric)}
.sv.sv-l{fill:rgba(91,58,110,.09);stroke:var(--plum)}
.sv.sv-z{fill:rgba(124,119,108,.10);stroke:var(--muted)}
.sv.sv-c{fill:rgba(31,56,100,.10);stroke:var(--royal)}
.sv-t{fill:var(--ink);font-size:16px;font-weight:600;font-family:var(--serif)}
.sv-a{stroke:var(--brass);stroke-width:2;fill:none;stroke-dasharray:6 5}
.in .sv-a{animation:march 2.4s linear infinite}
.sv-a.up{stroke:var(--teal)}
.sv-n{fill:var(--paper-2);stroke:var(--brass);stroke-width:2}
.sv-lb{fill:var(--rubric);font-size:11.5px;font-family:var(--sans)}
.sv-g{fill:var(--ink-2);font-size:11.5px;font-family:var(--serif)}
.cm-h{fill:var(--brass);font-size:11px;font-family:var(--sans);letter-spacing:.2em}
.cm-a{fill:var(--ink);font-size:13.5px;font-family:var(--serif)}
.cm-b{fill:var(--ink-2);font-size:13px;font-family:var(--serif)}
.cm-q{fill:var(--muted);font-size:11.5px}
.cm-n{fill:var(--paper-2);stroke-width:2}
.cm-n.l{stroke:var(--rubric)}.cm-n.r{stroke:var(--royal)}
.cm-l{fill:none;stroke:var(--brass);stroke-width:1.3;stroke-dasharray:300;stroke-dashoffset:300}
.in .cm-l{animation:draw 1.1s ease-out forwards}
.qb{opacity:.88}
.qb.prologue{fill:var(--prologue)}.qb.misery{fill:var(--misery)}
.qb.deliver{fill:var(--deliver)}.qb.gratitude{fill:var(--gratitude)}
.qb-l{fill:var(--muted);font-size:9.5px;font-family:var(--sans)}
.gws{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}
.gw{border:1px solid var(--rule);background:var(--paper-3);padding:13px 16px;border-radius:3px;
  border-top:3px solid var(--brass)}
.gw-w{font-family:"Palatino Linotype",Palatino,Georgia,serif;font-size:23px;color:var(--royal);
  letter-spacing:.02em}
.gw-z{font-size:14.5px;color:var(--rubric);margin-top:-2px}
.gw-r{font-family:var(--sans);font-size:10.5px;color:var(--muted);margin:4px 0 7px}
.gw-d{font-size:13.5px;color:var(--ink-2);line-height:1.68}

/* closures / tips / mnemonics */
.clos{display:grid;gap:15px}
.clos .c{border:1px solid var(--rule);background:var(--paper-2);padding:16px 20px;
  border-top:3px solid var(--brass);border-radius:3px}
.clos .c b{display:block;font-family:var(--disp);font-size:17px;color:var(--royal);margin-bottom:6px}
.clos .c p{margin:0;color:var(--ink-2)}
.tip{display:grid;gap:12px}
.tip .t{border-left:2px solid var(--brass);padding-left:14px}
.tip .t b{display:block;color:var(--royal);font-size:16px}
.mnem{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}
.mn{border:1px solid var(--rule);background:var(--paper-2);padding:13px 16px;border-radius:3px}
.mn .k{font-family:var(--sans);font-size:10px;letter-spacing:.2em;color:var(--brass)}
.mn .v{font-family:var(--disp);font-size:20px;color:var(--rubric);margin:4px 0 6px;letter-spacing:.14em}
.mn .d{font-size:13.5px;color:var(--ink-2);line-height:1.62}
.anch{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}
.an{border:1px solid var(--rule);background:var(--paper-2);padding:8px 14px;border-radius:3px;
  text-align:center;min-width:92px}
.an b{display:block;font-family:var(--disp);font-size:21px;color:var(--rubric);line-height:1.2}
.an span{font-family:var(--sans);font-size:10.5px;color:var(--muted)}

/* quiz */
.quiz{display:grid;gap:14px}
.qz{border:1px solid var(--rule);background:var(--paper-2);padding:14px 18px;border-radius:3px}
.qz .qt{font-size:16px;color:var(--ink);margin-bottom:9px}
.qz .qt i{font-family:var(--disp);font-style:normal;color:var(--brass);margin-right:8px}
.opt{display:block;padding:6px 10px;margin:3px 0;border:1px solid var(--rule);cursor:pointer;
  font-size:14.5px;border-radius:2px;transition:.12s;background:var(--paper-3)}
.opt:hover{border-color:var(--brass)}
.opt input{margin-right:8px;accent-color:var(--royal)}
.opt.ok{background:rgba(30,95,91,.16);border-color:var(--teal)}
.opt.no{background:rgba(155,27,30,.13);border-color:var(--rubric)}
.qz .ex{display:none;margin-top:9px;font-size:13.5px;color:var(--ink-2);
  border-left:2px solid var(--brass);padding-left:12px;line-height:1.65}
.qz.done .ex{display:block}
.qbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:6px 0 18px}
#score{font-family:var(--disp);font-size:16px;color:var(--rubric)}

/* drill mode */
body.drill .qa .a,body.drill .core,body.drill .field:not(.f-memo){display:none}
body.drill .qa{cursor:pointer}
body.drill .qa.open .a{display:block}
body.drill .qa::after{content:"点按显示答案";display:block;font-family:var(--sans);font-size:10.5px;
  letter-spacing:.14em;color:var(--muted);margin-top:4px}
body.drill .qa.open::after{display:none}

.hidden{display:none !important}
.foot{margin-top:66px;padding-top:22px;border-top:2px solid var(--royal);font-family:var(--sans);
  font-size:12px;color:var(--muted);line-height:1.95}
#toTop{position:fixed;right:18px;bottom:18px;z-index:70;width:42px;height:42px;border-radius:50%;
  border:1px solid var(--rule);background:var(--paper-2);color:var(--royal);cursor:pointer;
  font-size:16px;display:none}
#toTop.show{display:block}
.scrim{display:none}

@keyframes march{to{stroke-dashoffset:-26}}
@keyframes pulse{0%{r:8;opacity:.9}100%{r:30;opacity:0}}
@keyframes draw{to{stroke-dashoffset:0}}
@keyframes fadeup{to{opacity:1;transform:none}}
@keyframes slidein{to{opacity:1;transform:none}}
@keyframes fadein{to{opacity:1}}

@media (max-width:1180px){
  .acts{grid-template-columns:repeat(4,1fr)}
  .act:nth-child(4){border-right:0}
  .flowh{grid-template-columns:repeat(3,1fr)}
}
@media (max-width:900px){
  .brand{display:none}
  .tbs{order:9;flex:1 0 100%}
}
@media (max-width:1080px){
  .shell,.shell.hid{grid-template-columns:1fr}
  .shell.hid .side{opacity:1;pointer-events:auto;width:290px;padding:16px 12px;
    border-right:1px solid var(--rule)}
  .side{position:fixed;top:46px;left:0;width:290px;background:var(--paper);z-index:55;
    transform:translateX(-102%);transition:transform .22s ease;box-shadow:0 0 30px rgba(0,0,0,.2)}
  body.nav .side{transform:none;opacity:1;pointer-events:auto}
  body.nav .scrim{display:block;position:fixed;inset:46px 0 0;background:rgba(10,12,16,.4);z-index:50}
  #tocOpen{display:none !important}
  .main{padding:0 18px 90px}
  .grid52{grid-template-columns:repeat(9,1fr)}
}
@media (max-width:640px){
  body{font-size:16.5px}
  .brand{font-size:11px;letter-spacing:.08em}
  .tbs{flex:1 1 90px}
  .main{padding:0 13px 80px}
  .hero{padding:34px 0 26px}
  .ld-h,.ld-b{padding-left:15px;padding-right:15px}
  .ld-no{font-size:25px}.ld-ht h3{font-size:19px}
  .grid52{grid-template-columns:repeat(7,1fr)}
  .acts{grid-template-columns:1fr}
  .act{border-right:0;border-bottom:1px solid var(--rule)}
  .flowh{grid-template-columns:1fr}
  .term{grid-template-columns:1fr;gap:1px}
  figure{padding:12px}
  .core{font-size:16.5px}
  .lead{font-size:16.5px}
}
@media (max-width:860px){
  .fscroll>svg{min-width:720px}
}
@media (prefers-reduced-motion:reduce){
  *{animation:none !important;transition:none !important;scroll-behavior:auto !important}
  .para,.mind-b{stroke-dashoffset:0 !important}
  .act,.ch,.fx,.ch-a{opacity:1 !important;transform:none !important}
}
@media print{
  .topbar,.side,#toTop,.chk,.scrim,#prog,#tocOpen,.qbar{display:none !important}
  .shell{grid-template-columns:1fr}
  body{background:#fff;color:#000;font-size:10.5pt}
  .ld,figure,.card,.qz{break-inside:avoid;page-break-inside:avoid}
  .qz .ex{display:block}
  @page{size:A4;margin:17mm 15mm}
}
"""
