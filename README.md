# 海德堡要理问答 · 52 主日全景解读

> **版本标识：`heidelberg-catechism-52-20261020-v5-CCstudy`**（主题-日期-版本号-CCstudy）
> 仓库与域名不含版本号；当前版本号与日期显示在网页页脚。

欧陆改革宗（三项联合信条）视角的《海德堡要理问答》（Catechesis Palatina, 1563）全书解读。
信经与信条正文一字不差引自 [ccifellowship.org](https://ccifellowship.org)。

| 部署 | 链接 |
|---|---|
| GitHub Pages | https://07-je-cc-love-personal-20260918.github.io/heidelberg-catechism-52-CCstudy/ |
| Surge | https://heidelberg-catechism-52-ccstudy.surge.sh |
| Netlify | https://heidelberg-catechism-52-ccstudy.netlify.app |
| 原文阅读室 | 以上任一站点 + `/texts.html` |
| 仓库 | https://github.com/07-Je-CC-Love-Personal-20260918/heidelberg-catechism-52-CCstudy |

推送 `main` 后 GitHub Actions 自动重建并部署三站（仓库密钥 `SURGE_TOKEN`／`SURGE_LOGIN`，组织密钥 `NETLIFY_AUTH_TOKEN_20260918`）。

## 恢复点（Releases / Tags）

| 标记 | 日期 | 说明 |
|---|---|---|
| `v5-20261020` | 2026-10-20 | 目录精确跳转、去版本号改名、信条互参热力图、紧凑排版 |
| `v4-20261020` | 2026-10-20 | 改名前最后版本：记忆图标、今日应用、三幕流程、鲜明配色 |

恢复：`git checkout <标记>` 后推送到 `main`，或在 Releases 页下载源码包。

## 更新说明

**v5 · 2026-10-20**
- 目录链接全部修复并逐一核对（主页 85 个、原文页 96 个，电脑与手机共 362 次点击测试全部落点准确）：动态顶栏高度、二次校正滚动、长距离先瞬移再平滑、移动端抽屉统一、去掉导致落点漂移的 content-visibility
- 仓库更名 `heidelberg-catechism-52-CCstudy`，三站域名同步去掉日期与版本号；版本号移至页脚
- 新增「信条互参热力图」：52 主日引用比利时信条 37 条与多特信经四项教义的分布，点按直达原文
- 排版收紧：减少章节与卡片间空白

**v4 · 2026-10-20** — 52 主日记忆图标、今日应用、三幕动态流程图、鲜明四色配色、信条互参直链原文

**v3 · 2026-10-17** — ccifellowship.org 原文（129 问答含脚注与经文出处、比利时信条、多特信经、三大信经）、原文阅读室 `texts.html`、重点／难点前置、大字号、记忆墙、比例环图

**v2 · 2026-10-17** — 平铺自适应网格、毛玻璃、图标与入场动画、信经背诵室、三项联合信条深度对比

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
  ui4.py            # v4 层：记忆图标、今日应用、三幕流程、配色
  ui5.py            # v5 层：精确锚点导航、热力图、版本号
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
