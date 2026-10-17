# -*- coding: utf-8 -*-
"""把 ccifellowship.org 抓取结果（cci.json + titles.json）解析为 src/cci_text.py。
用法: python3 tools/cci_parse.py <cci.json> <titles.json> > src/cci_text.py"""
import json, re, sys
d = json.load(open(sys.argv[1])); T = json.load(open(sys.argv[2]))
P = "/books/book-of-praise/"
def ttl(k): return T[k][0].split(" | ")[0].strip()
def lines(k): return [l for l in d[k].split("\n") if l.strip()]

# --- 海德堡 ---
HC = {}; LDQ = {}
for k in d:
    m = re.search(r"lord-day-(\d+)$", k)
    if not m: continue
    ld = int(m.group(1)); cur = None
    for l in lines(k):
        s = l.strip(); mq = re.match(r"^(\d+)[．.] ?问：(.*)$", s)
        if mq and not l.startswith(" "):
            cur = int(mq.group(1)); HC[cur] = {"q": mq.group(2), "a": "", "refs": [], "ld": ld}
            LDQ.setdefault(ld, []).append(cur)
        elif s.startswith("答："):
            HC[cur]["a"] = s[2:]
        elif l.startswith(" "):
            HC[cur]["refs"].append(s)
        else:
            HC[cur]["a"] += "\n" + s
assert sorted(HC) == list(range(1, 130)), sorted(set(range(1,130))-set(HC))

def articles(prefix):
    out = []
    ks = [k for k in d if k.startswith(prefix + "/") and re.search(r"/\d+$", k)]
    ks.sort(key=lambda k: int(k.rsplit("/", 1)[1]))
    for k in ks:
        body, refs = [], []
        for l in lines(k):
            (refs if l.startswith(" ") else body).append(l.strip())
        out.append({"no": int(k.rsplit("/", 1)[1]), "title": ttl(k), "body": body, "refs": refs})
    return out

BC = articles(P + "confessions/the-belgic-confession")
COD = []
for sec in ["section1", "section2", "section3-4", "section5"]:
    pre = P + "confessions/canons-of-dort/" + sec
    COD.append({"title": ttl(pre), "arts": articles(pre)})

def creed(slug):
    ls = lines(P + "creeds/" + slug)
    return {"name": ttl(P + "creeds/" + slug), "intro": ls[0], "lines": ls[1:]}
CREEDS = [creed("apostles-creed"), creed("nicene-creed"), creed("athanasian-creed")]
INTRO = {"hc": d[P + "confessions/heidelberg-catechism"], "bc": d[P + "confessions/the-belgic-confession"],
         "cod": d[P + "confessions/canons-of-dort"], "creeds": d[P + "creeds"]}

print("# -*- coding: utf-8 -*-")
print('"""自动生成：文本一字不差取自 https://ccifellowship.org （基督教华人网络团契 · 赞美诗集 Book of Praise 中译）。勿手改；重抓用 tools/cci_parse.py"""')
for n, v in [("HC", HC), ("LDQ", LDQ), ("BC", BC), ("COD", COD), ("CREEDS", CREEDS), ("INTRO", INTRO)]:
    print("%s = %r" % (n, v))
