from datetime import datetime

import requests
from bs4 import BeautifulSoup

url = "http://news.sina.com.cn/o/2018-10-19/doc-ifxeuwws5952620.shtml"

res = requests.get(url)
res.encoding = "utf-8"
soup = BeautifulSoup(res.text, 'lxml')
news_dict = {}

news_title = soup.select('h1.main-title')[0].text.strip()
nt = datetime.strptime(soup.select('span.date')[0].text.strip(), "%Y年%m月%d日 %H:%M")
news_time = datetime.strftime(nt, '%Y-%m-%d %H:%M')
news_dict['time'] = news_time

news_source = soup.select('.source')[0].text
news_author = soup.select('p.show_author')[0].text

news_article = soup.select('div#article>p')
tmp_str = ""
for i in range(len(news_article) - 1):
    tmp_str += news_article[i].text + '\r\n'
news_dict['article'] = tmp_str

news_pic = soup.select('div.img_wrapper>img')
news_pic_list = []
for pic in news_pic:
    print(pic.get("src"))
    news_pic_list.append(pic.get("src"))

print("Time:" + news_time + ", Title:" + news_title + ", Author: " + news_author + ", Source:" + news_source)
print("There are " + str(len(news_pic_list)) + " pictures.")
