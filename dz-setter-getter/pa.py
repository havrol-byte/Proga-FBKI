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

    def get_point(self):
        return self.point
    
    def get_number(self):
        return self.number
    
    def get_plane_type(self):
        return self.plane_type
    
    def get_time(self):
        return self.time

    def reaming_time(self, time_now = '00:00'):
        time1 = time_now.split(':')
        time2 = self.time.split(':')
        for i in range(2):
            time1[i] = int(time1[i])
            time2[i] = int(time2[i])
        result = [time1[0] - time2[0], time1[1] - time2[1]]

        if result[1] < 0:
            result[0] -= 1
            result[1] += 60
        if result[0] < 0:
            print('Ошибка во времени, либо вы опоздали')
        else: 
            print(f'Осталось {result[0]} ч {result[1]} мин до вылета')