#// задача 1 \\

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __str__(self):
        return f"Вектор на плоскости с координатами ({self.x}, {self.y})"


v1 = Vector(3, 4)
v2 = Vector(-1, 2)

print(v1)
print(repr(v1))

print(v2)
print(repr(v2))

#// задача 2 \\

class IPAddress:
    def __init__(self, ipaddress):
        if isinstance(ipaddress, str):
            parts = ipaddress.split('.')
            self.ip = [int(p) for p in parts]
        elif isinstance(ipaddress, (list, tuple)):
            self.ip = list(ipaddress)
        else:
            raise ValueError("Неверный формат IP-адреса")

        if len(self.ip) != 4 or not all(0 <= x <= 255 for x in self.ip):
            raise ValueError("IP-адрес должен состоять из 4 чисел от 0 до 255")

    def __repr__(self):
        return f"IPAddress('{self.__str__()}')"

    def __str__(self):
        return '.'.join(map(str, self.ip))

ip1 = IPAddress("192.168.1.1")
ip2 = IPAddress([10, 0, 0, 1])

print(ip1)
print(repr(ip1))

print(ip2)
print(repr(ip2))