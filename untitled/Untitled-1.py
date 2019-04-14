class Student:  # 基类定义
    def __init__(self, name='', midterm=0, final=0):
        self.__name = name  # 私有成员
        self._midterm = midterm  # 保护成员
        self._final = final

    def __setName(self, name):
        self._name = name

    def __getName(self):
        return self._name

    name = property(__getName, __setName)

    def setMidterm(self, midterm):
        self._midterm = midterm

    def setFinal(self, final):
        self._final = final


class LGStudent(Student):  # 派生类定义
    def calcSemGrade(self):
        return (self._midterm + self._final) / 2  # 基类成员

    def __str__(self):  # 转换为字符串
        return self.name + '\t' + str(self.calcSemGrade())  # 基类属性


lg = LGStudent()
lg.name = "zhang3"
lg.setMidterm(60)
lg.setFinal(70)
print(lg)