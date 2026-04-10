class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}, {self.price}$"


class ShoppingCart:
    def __init__(self, items=None):
        if items is None:
            self.items = []
        else:
            self.items = list(items)

    def add(self, item):
        if isinstance(item, Item):
            self.items.append(item)

    def total(self):
        return sum(item.price for item in self.items)

    def remove(self, name):
        self.items = [item for item in self.items if item.name != name]

    def __str__(self):
        if not self.items:
            return ""
        return "\n".join(str(item) for item in self.items)

item1 = Item("Apple", 2)
item2 = Item("Banana", 3)
item3 = Item("Apple", 5)

cart = ShoppingCart([item1, item2])
cart.add(item3)

print(cart)

print("Total:", cart.total())  # 10

cart.remove("Apple")

print(cart)