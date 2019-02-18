import requests

stocks = ["sh600766", "sz000001", "sz000021"]
for s in stocks:
    pc = requests.get("https://hq.sinajs.cn/?_=0.5711938992255801&list=" + s)
    pc.encoding = "gb2312"
    s = pc.text

    data = s[s.find("=") + 2:len(s) - 3]
    pslist = data.split(",")
    print(pslist[0] + ": 开盘价：" + pslist[1] + "，当前价：" + pslist[2] + "，当前涨幅：" + str(
        (float(pslist[2]) - float(pslist[1]))*100 / float(pslist[1]))+"%")
