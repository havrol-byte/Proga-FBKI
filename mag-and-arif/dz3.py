class FoodInfo:
    def __init__(self, proteins, fats, carbohydrates):
        self.proteins = proteins
        self.fats = fats
        self.carbohydrates = carbohydrates

    def __repr__(self):
        return f"FoodInfo({self.proteins}, {self.fats}, {self.carbohydrates})"

    def __add__(self, other):
        if isinstance(other, FoodInfo):
            return FoodInfo(
                self.proteins + other.proteins,
                self.fats + other.fats,
                self.carbohydrates + other.carbohydrates
            )
        return NotImplemented

    def __mul__(self, n):
        if isinstance(n, (int, float)):
            return FoodInfo(
                self.proteins * n,
                self.fats * n,
                self.carbohydrates * n
            )
        return NotImplemented

    def __truediv__(self, n):
        if isinstance(n, (int, float)):
            return FoodInfo(
                self.proteins / n,
                self.fats / n,
                self.carbohydrates / n
            )
        return NotImplemented

    def __floordiv__(self, n):
        if isinstance(n, (int, float)):
            return FoodInfo(
                self.proteins // n,
                self.fats // n,
                self.carbohydrates // n
            )
        return NotImplemented

f1 = FoodInfo(10, 5, 20)
f2 = FoodInfo(5, 5, 10)

print(f1 + f2)  
print(f1 * 2)
print(f1 / 2)
print(f1 // 2)