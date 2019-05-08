class Student:	# 基类定义
	def __init__(self, name='', midterm=0, final=0):
	    self.__name = name
	    self._midterm = midterm
	    self._final = final
	def __setName(self, name):
	    self._name = name
	def __getName(self):
	    return self._name
	name = property(__getName, __setName)
	def setidterm(self, midterm):
	    self._midterm = midterm
	def setFinal(self, final):
	    self._final = final
		
class LGStudent:		# 派生类定义
	def calcSemGrade(self):
	    return (self._midterm + self._final)/2	# 基类成员

	def setMidterm(self, midterm):
            super.setMidterm(midterm)

        def setFinal(self, final):
            super.setFinal(final)
         
	
	def __str__(self):	# 转换为字符串
	    return self.name + '\t' + self.calcSemGrade() # 基类属性


lg=LGStudent()
lg.name = "zhang3"
lg.setMidterm(90)
lg.setFinal(87)
print(lg)
