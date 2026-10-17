# 海德堡要理问答 · 52 主日全景解读

欧陆改革宗（三项联合信条）视角的《海德堡要理问答》（Catechesis Palatina, 1563）全书解读，
输出为一个**完全自含的单页 HTML**：无外部字体、无 CDN、无构建依赖，离线可用，手机与桌面自适应。

**v3 更新 · 2026-10-17**（仓库沿用 v2 名称）
- 三大普世信经与三项联合信条正文**一字不差**取自 [ccifellowship.org](https://ccifellowship.org)：129 问答（含脚注号与经文出处）、比利时信条 37 条、多特信经四项教义（含错谬反驳）、使徒／尼西亚／亚他那修信经
- 新增 **原文阅读室** `texts.html`：四部文献全文、可隐藏目录、全文查找、字号切换，与解读页双向跳转
- 重点突出：每主日顶部「重点」与「记忆钥匙」高亮条，「难点 · 误读警示」前置；正典定位／原文钥词等次要层收进「延伸阅读」
- 字号整体放大（正文 18.5px，手机 17.5px），标签与图注不小于 12.5px
- 新可视化：129 问四部分比例动态环图、52 句重点记忆墙、三项联合信条数据卡

**v2 · 2026-10-17** —— 平铺自适应网格、毛玻璃、图标与入场动画、信经背诵室、三项联合信条深度对比

| 部署 | 链接 |
|---|---|
| GitHub Pages | https://07-je-cc-love-personal-20260918.github.io/heidelberg-catechism-52-20261017-v2-CCstudy/ |
| 原文阅读室 | 以上任一站点加 `/texts.html` |
| Surge | https://heidelberg-catechism-52-20261017-v2-ccstudy.surge.sh |
| Netlify | https://heidelberg-catechism-52-20261017-v2-ccstudy.netlify.app |
| 仓库 | https://github.com/07-Je-CC-Love-Personal-20260918/heidelberg-catechism-52-20261017-v2-CCstudy |

推送 `main` 后 Actions 自动重建并部署 Surge（需仓库密钥 `SURGE_TOKEN`）与 Netlify（组织密钥 `NETLIFY_AUTH_TOKEN_20260918`）；GitHub Pages 从 `main` 根目录发布。

## 内容

| 部分 | 内容 |
|---|---|
| 总论 I–VIII | 为什么写（1555 和约 / 1560 圣餐之争 / 三版沿革）· 三重结构 · 正典弧线与救赎史故事线 · 圣经神学（预表链条、正典主题）· 圣约神学（救赎之约／行为之约／恩典之约）· 三大普世信经与三项联合信条 · 四层释经进路 · 改革宗欧洲影响地图 · 文本版本与要理讲道传统 · 思维导图与 52 主日罗盘 |
| 主日 1–52 | 每主日十一层：问答原文 → 本质核心 → 逻辑推进（承前启后）→ 经文根据 → 原文钥词（希伯来／希腊／拉丁）→ 真实背景 → 神学剖析 → 正典定位 → 多视角对照 → 信条互参 → 误读警示 → 记忆钥匙 |
| 结语 | 三重闭环：救赎史与圣约 / 正典故事弧 / 困苦—拯救—感恩 |
| 附录 A–L | 基督三职 · 救恩次序与动态链 · 圣餐四立场 · 十诫总表 · 主祷文六求 · 教会纪律流程 · 对手立场总表 · 原文钥词汇编 · 52 主日速查索引 · 成对记忆与人生处境索引 · 背诵方案／口诀／数字锚点 · 交互自测 |

可视化：欧洲影响流向地图（按真实经纬度）、救赎史八幕故事线、降卑—升高抛物线、圣约结构树、
三层权威地基、三重结构比例图、横向思维导图、救恩次序动态链、教会纪律流程图、17 张数据表。

交互：全文搜索、背诵模式（遮盖答案逐问自测）、52 格进度罗盘（本地持久化）、
交互自测与评分、三态主题（明／暗／跟随系统）、可折叠目录、阅读进度条、A4 打印样式。

## 目录结构

```
texts.html          # 构建产物：原文阅读室（ccifellowship.org 全文）
index.html          # 构建产物，直接可部署（Pages / Netlify 的站点根文件）
src/
  cci_text.py       # 自动生成：ccifellowship.org 原文（勿手改）
  ui3.py            # v3 层：原文问答、重点/难点、记忆墙、阅读室页面
  data.py           # 52 主日全部内容（问答、解读、原文钥词…）
  creeds.py         # 三大普世信经 + 三项联合信条
  story.py          # 圣经神学与圣约神学章节、预表链条、正典主题
  quiz.py           # 自测题库、口诀、数字锚点、成对记忆、人生处境索引
  charts.py         # 全部 SVG/HTML 图表
  css.py  js.py     # 样式与交互
  build.py          # 装配脚本
netlify.toml        # Netlify 配置（publish = "."）
.github/workflows/build.yml   # push 到 src/ 时自动重建 index.html 并提交
```

## 本地重建

```bash
cd src && python3 build.py     # 产出 ../index.html，无第三方依赖
```

改内容只改 `src/data.py`；改版式只改 `src/css.py`；加图只改 `src/charts.py`。
推送后 GitHub Actions 会自动重建 `index.html`，GitHub Pages 随之更新。

## 技术约定

- 不引用 Google Fonts 等外部资源（部署地网络不可达），全部使用系统字体栈回退。
- 目录滚动高亮用 `rAF + getBoundingClientRect`；动画入场用 IntersectionObserver，
  离开视口即移除以停掉无限动画省电；完整 `prefers-reduced-motion` 降级。
- 主日卡片使用 `content-visibility:auto` 控制长页渲染开销。
- 浏览器存储全部包在 try/catch 中，禁用时优雅降级。

## 说明

信经与信条正文引自 ccifellowship.org（`tools/cci_parse.py` 解析抓取结果生成 `src/cci_text.py`）；
解读依欧陆改革宗正统神学立场撰写，供讲道预备、要理教育与个人背诵之用。

SOLI DEO GLORIA
