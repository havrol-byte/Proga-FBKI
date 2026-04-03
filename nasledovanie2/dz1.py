class Bachelor:
    def __init__(self, firstName, lastName, group, averageMark):
        self.firstName = firstName
        self.lastName = lastName
        self.group = group
        self.averageMark = averageMark

    def getScholarship(self):
        if self.averageMark == 5:
            return 10000
        elif self.averageMark > 3:
            return 5000
        else:
            return 0


class Undergraduate(Bachelor):
    def __init__(self, firstName, lastName, group, averageMark, research):
        super().__init__(firstName, lastName, group, averageMark)
        self.research = research

    def getScholarship(self):
        if self.averageMark == 5:
            return 15000
        elif self.averageMark > 3:
            return 7500
        else:
            return 0


students = [
    Bachelor("Иван", "Иванов", "101", 5),
    Bachelor("Петр", "Петров", "102", 4),
    Bachelor("Сергей", "Сергеев", "103", 3),
    Undergraduate("Анна", "Андреева", "201", 5, "тема 1"),
    Undergraduate("Ольга", "Соколова", "202", 4, "тема 2"),
    Undergraduate("Михаил", "Кузнецов", "203", 3, "тема 3")
]

for s in students:
    print(s.firstName, s.lastName, "стипендия:", s.getScholarship(), "р.")