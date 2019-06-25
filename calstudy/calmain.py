import random
import time

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

import calfunc

pdfmetrics.registerFont(TTFont('cambria', 'cambria.ttc'))
n = int(input('Please input the number:'))
if n > 0:
    t = time.localtime()
    # 以时间和次数组合成文件名
    filename = 's{:4d}-{:02d}-{:02d} {:02d}{:02d}{:02d}({}).pdf'.format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour,
                                                                        t.tm_min, t.tm_sec, n)
    pdf = SimpleDocTemplate(filename,
                            pagesize=(A4[0], A4[1]),
                            rightMargin=20,
                            leftMargin=20,
                            topMargin=20,
                            bottomMargin=20)
    t = set()
    elements = []
    counts = [0] * 4

    calfuncs = [lambda x: calfunc.ranplus(x), lambda x: calfunc.ransub(x), lambda x: calfunc.ranmul(x),
                lambda x: calfunc.randiv(x)]  # 用lambda表达式作为列表元素
    for i in range(n):
        tp = random.randint(0, 3)
        # tp = 3
        counts[tp] += 1
        exp = calfuncs[tp](n * 0.03)
        while len(elements) > 0 and exp in elements[-1]:  # 相邻行去重
            exp = calfuncs[tp](n * 0.03)
        t.add(exp)

        if len(t) % 3 == 0:
            elements.append(list(t))
            t.clear()

    etable = Table(elements, rowHeights=38, colWidths=180)
    etable.setStyle(
        TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'cambria'),  # 字体
            ('FONTSIZE', (0, 0), (-1, -1), 15),  # 字体大小
            ('ALIGN', (-1, 0), (-2, 0), 'LEFT'),  # 对齐
            ('TEXTCOLOR', (0, 0), (0, 0), colors.black),  # 设置表格内文字颜色
            ('GRID', (-1, 0), (-2, 0), 0, colors.white),  # 设置表格框线
        ])
    )
    contents = [etable]
    pdf.build(contents)

    print(f'生成成功，其中加法 {counts[0]} 题，减法 {counts[1]} 题，乘法 {counts[2]} 题，除法 {counts[3]} 题。')
