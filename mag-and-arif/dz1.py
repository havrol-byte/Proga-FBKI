class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        if isinstance(other, tuple) and len(other) == 2:
            if all(isinstance(i, (int, float)) for i in other):
                return self.x == other[0] and self.y == other[1]
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result

v1 = Vector(1, 2)
v2 = Vector(1, 2)
v3 = Vector(2, 3)

print(v1 == v2)
print(v1 != v3)
print(v1 == (1, 2))
print(v1 != (2, 2))