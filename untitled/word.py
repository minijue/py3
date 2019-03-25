import jieba.analyse

jieba.load_userdict("/home/wangjue/files/user_dict.txt")

text = "在厦门学习互联网大数据技术,厦门学习互联网,大数据";
seg_list = jieba.cut(text, cut_all=False)
u = "/".join(seg_list)
print(u)
tag = jieba.analyse.extract_tags(text, topK=5)
print(",".join(tag))
tag = jieba.analyse.extract_tags(text, topK=5, withWeight=True)
print(tag)
