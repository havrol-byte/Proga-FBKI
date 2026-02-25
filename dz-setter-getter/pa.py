# // задача 1 \\

class Soda:
    def __init__(self, dope = None):
        self.dope = dope

    def show_my_drink(self):
        if self.dope == None:
            return 'Обычная газировка'
        else:
            return f'Газировка и {self.dope}'
        
    def get_dope(self):
        return self.dope
    
    def set_dope(self, name):
        if len(name) > 2:
            self.dope = name

# // задача 2 \\

class KgToPounds:
    def __init__(self, kg):
        if kg >= 0:
            self.kg = kg
        else:
            self.kg = 0
            print('Неверные данные \nКол-во КГ = 0')

    def to_pounds(self):
        return self.kg * 2,205
    
    def set_kg(self, nkg):
        if nkg >= 0:
            self.kg = nkg
    
    def ger_kg(self):
        return self.kg

# // задача 3 \\

class Aeroflot:
    def __init__(self, point, number, plane_type, time = '00:00'):
        self.point = point
        self.number = number
        self.plane_type = plane_type
        if time:
            self.time = time

    def set_point(self, nPoint):
        if len(nPoint) >= 2:
            self.point = nPoint
    
    def set_number(self, nNumber):
        self.number = nNumber

    def set_point(self, nPlane_type):
        self.plane_type = nPlane_type

    def set_point(self, nTime):
        if len(nTime) == 5:
            self.time = nTime

            