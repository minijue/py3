import re
import requests

p = requests.get("http://news.fudan.edu.cn/news/xxyw/")
p.encoding = "utf-8"
pc = p.text
baselist = re.findall('base href="http://[a-zA-Z0-9./]+"', pc)
if len(baselist) > 0:
    base = baselist[0][11:len(pc)-1]
    print(base)
    rellist = re.findall('a href="news/[a-zA-Z0-9./]+/[a-zA-Z0-9./]+', pc)
    for r in rellist:
        print(base + r)
