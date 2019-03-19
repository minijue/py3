import calfunc
import random

from reportlab.pdfgen import canvas

n = int(input('Please input the number:'))
if n > 0:
    x = 1
    y = 1
    p = canvas.Canvas('kousuan.pdf')
    for i in range(n):
        tp = random.randint(1, 4)
        if tp == 1:  # plus
            p.drawString(x, y, calfunc.ranplus())
        elif tp == 2:  # subtract
            p.drawString(x, y, calfunc.ransub())
        elif tp == 3:  # multiply
            p.drawString(x, y, calfunc.ranmul())
        elif tp == 4:  # divide
            p.drawString(x, y, calfunc.randivintbl())
        else:
            print('error')
            break
        x += 70
        if (i + 1) % 4 == 0:
            y += 30
            x = 1

    p.showPage()
    p.save()
