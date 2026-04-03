class Product:
    def __init__(self, name: str, price: float, weight: float):
        self.__name = name
        self.__price = price
        self.__weight = weight

    def get_name(self):
        return self.__name

    def set_name(self, value: str):
        self.__name = value

    def get_price(self):
        return self.__price

    def set_price(self, value: float):
        self.__price = value

    def get_weight(self):
        return self.__weight

    def set_weight(self, value: float):
        self.__weight = value


class Buy(Product):
    def __init__(self, name: str, price: float, weight: float, quantity: int):
        super().__init__(name, price, weight)
        self.__quantity = quantity
        self.__total_price = self.__calc_total_price()
        self.__total_weight = self.__calc_total_weight()

    def __calc_total_price(self):
        return self.get_price() * self.__quantity

    def __calc_total_weight(self):
        return self.get_weight() * self.__quantity

    def get_quantity(self):
        return self.__quantity

    def set_quantity(self, value: int):
        self.__quantity = value
        self.__total_price = self.__calc_total_price()
        self.__total_weight = self.__calc_total_weight()

    def get_total_price(self):
        return self.__total_price

    def get_total_weight(self):
        return self.__total_weight


class Check(Buy):
    def __init__(self, name: str, price: float, weight: float, quantity: int):
        super().__init__(name, price, weight, quantity)

    def print_check(self):
        print("=== Чек ===")
        print("Товар:", self.get_name())
        print("Цена за единицу:", self.get_price())
        print("Вес за единицу:", self.get_weight())
        print("Количество:", self.get_quantity())
        print("Общая цена:", self.get_total_price())
        print("Общий вес:", self.get_total_weight())
        print("============")

ch = Check("Молоко", 120.0, 1.0, 3)
ch.print_check()