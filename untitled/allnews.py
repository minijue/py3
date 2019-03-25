import jieba
from gensim.corpora.dictionary import Dictionary

textfile = "/home/wangjue/files/allnews.txt"
num_topic = int(input("number:"))
f = open(textfile, "r", encoding="utf-8")
lines = f.readlines()
f.close()

stoplist = open("/home/wangjue/files/", "r", encoding="utf-8").read()
stoplist = set(w.strip() for w in stoplist)

segtexts = []
for line in lines:
    doc = []
    for w in list(jieba.cut(line, cut_all=True)):
        if len(w) > 1 and w not in stoplist:
            doc.append(w)
    segtexts.append(doc)

dictionary = Dictionary(segtexts)
dictionary.filter_extremes(2, 1.0, keep_n=1000)
corpus=[dictionary.doc2bow]
