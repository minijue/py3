import requests
import re
import os

base = "http://www.ecjtu.jx.cn"

p = requests.get(base)
p.encoding = "utf-8"
pc = p.text
imglist = re.findall("img src=\"[a-zA-Z0-9_/.]+\"", pc)
link = ""
file = ""
i = 0

path = "pics"
ise = os.path.exists(path)
if not ise:
    os.makedirs(path)

for img in imglist:
    img = img[9:len(img) - 1]
    if img[0:1] == "//":
        link = "http:" + img
    elif img[0] == '/':
        link = base + img
    else:
        link = img
    index = link.rfind("/")
    lastfile = file
    lastfile = lastfile[lastfile.rfind("/") + 1:len(lastfile)]
    file = link[index + 1:len(link)]
    if file == lastfile:
        file = str(i) + "-" + file
        i = i + 1
    print(file)

    file = path + "/" + file
    image = requests.get(link)
    f = open(file, "ab")
    f.write(image.content)
    f.close()
