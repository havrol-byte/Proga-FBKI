class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


class Circle:
    def __init__(self, radius, center):
        if not isinstance(center, Point):
            raise TypeError("center должен быть экземпляром Point")

        self.radius = radius
        self.center = center

    def __str__(self):
        return f"({self.center.x}, {self.center.y}), r = {self.radius}"

p = Point(3, 4)
c = Circle(10, p)

print(p)
print(c)