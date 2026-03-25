class BasicPlan:
    def __init__(self):
        self.can_stream = True
        self.can_download = True
        self.has_SD = True
        self.has_HD = False
        self.has_UHD = False
        self.num_of_devices = 1
        self.price = 8.99

class SilverPlan(BasicPlan):
    def __init__(self):
        super().__init__()
        self.has_HD = True
        self.num_of_devices = 2
        self.price = 12.99


class GoldPlan(BasicPlan):
    def __init__(self):
        super().__init__()
        self.has_HD = True
        self.has_UHD = True
        self.num_of_devices = 4
        self.price = 15.99

basic = BasicPlan()
silver = SilverPlan()
gold = GoldPlan()

print(vars(basic))
print(vars(silver))
print(vars(gold))