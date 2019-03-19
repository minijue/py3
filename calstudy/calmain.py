import random
import time

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

import calfunc

n = int(input('Please input the number:'))
if n > 0:
    t = time.localtime()
    # 以时间和次数组合成文件名
    filename = '{:4d}-{:02d}-{:02d} {:02d}{:02d}{:02d}({}).pdf'.format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour,
                                                                       t.tm_min, t.tm_sec, n)
    pdf = SimpleDocTemplate(filename,
                            pagesize=(A4[0], A4[1]),
                            rightMargin=20,
                            leftMargin=20,
                            topMargin=20,
                            bottomMargin=20)
    t = set()
    elements = []

    for i in range(n):
        tp = random.randint(1, 4)
        if tp == 1:  # plus
            t.add(calfunc.ranplus())
        elif tp == 2:  # subtract
            t.add(calfunc.ransub())
        elif tp == 3:  # multiply
            t.add(calfunc.ranmul())
        elif tp == 4:  # divide
            t.add(calfunc.randivintbl())
        else:
            print('error')
            break
        if len(t) % 5 == 0:
            elements.append(list(t))
            t.clear()

    etable = Table(elements, rowHeights=38, colWidths=110)
    etable.setStyle(
        TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 14),  # 字体大小
            ('ALIGN', (-1, 0), (-2, 0), 'LEFT'),  # 对齐
            ('TEXTCOLOR', (0, 1), (-2, -1), colors.black),  # 设置表格内文字颜色
            ('GRID', (0, 0), (-1, -1), 0, colors.white),  # 设置表格框线
        ])
    )
    contents = [etable]
    pdf.build(contents)
