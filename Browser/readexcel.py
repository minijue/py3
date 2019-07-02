if __name__ == '__main__':
    print("Please use me as a module.")


class OneClass:
    def __init__(self, name):
        self.name = name
        self.students = {}
        self.norm = None
        self.exam = None
        self.scale = 0.0
        self.score = 100

    def AddStudentScore(self, name, nscore, escore):
        self.students[name] = (nscore, escore)

    def GetStudentScore(self, name):
        score = self.students.get(name, None)
        if score is not None:
            return score[0], score[1]
        else:
            return -1, -1


def GetClasses(path):
    pass
