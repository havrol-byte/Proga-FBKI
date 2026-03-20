class Circle:
    def __init__(self, radius):
        self.radius = radius

    @classmethod
    def from_diameter(cls, diameter):
        return cls(diameter / 2)

c1 = Circle(10)
c2 = Circle.from_diameter(20)

print(c1.radius)
print(c2.radius)