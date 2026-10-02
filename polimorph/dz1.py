from abc import ABC, abstractmethod


class Dinosaur(ABC):

    @abstractmethod
    def get_personal_name(self):
        pass

    @abstractmethod
    def get_breed(self):
        pass

    @abstractmethod
    def get_height(self):
        pass

    @abstractmethod
    def get_weight(self):
        pass

    @abstractmethod
    def get_diet(self):
        pass


class Carnivore(Dinosaur):
    def __init__(self, name, breed, height, weight):
        self.name = name
        self.breed = breed
        self.height = height
        self.weight = weight

    def get_personal_name(self):
        return self.name

    def get_breed(self):
        return self.breed

    def get_height(self):
        return self.height

    def get_weight(self):
        return self.weight

    def get_diet(self):
        return "Carnivore"


class Herbivore(Dinosaur):
    def __init__(self, name, breed, height, weight):
        self.name = name
        self.breed = breed
        self.height = height
        self.weight = weight

    def get_personal_name(self):
        return self.name

    def get_breed(self):
        return self.breed

    def get_height(self):
        return self.height

    def get_weight(self):
        return self.weight

    def get_diet(self):
        return "Herbivore"


class DinosaurPark:
    def __init__(self):
        self.dinosaurs = []

    def add_dinosaur(self, dinosaur):
        if isinstance(dinosaur, Dinosaur):
            self.dinosaurs.append(dinosaur)

    def list_dinosaurs(self):
        return [
            f"{d.get_personal_name()} ({d.get_breed()})"
            for d in self.dinosaurs
        ]

    def list_carnivores(self):
        return [
            d.get_personal_name()
            for d in self.dinosaurs
            if d.get_diet() == "Carnivore"
        ]

    def list_herbivores(self):
        return [
            d.get_personal_name()
            for d in self.dinosaurs
            if d.get_diet() == "Herbivore"
        ]


d1 = Carnivore("Rex", "Tyrannosaurus", 6, 8000)
d2 = Herbivore("Leafy", "Brachiosaurus", 12, 30000)
d3 = Carnivore("Spike", "Velociraptor", 2, 100)

park = DinosaurPark()
park.add_dinosaur(d1)
park.add_dinosaur(d2)
park.add_dinosaur(d3)

print("Все динозавры:", park.list_dinosaurs())
print("Плотоядные:", park.list_carnivores())
print("Травоядные:", park.list_herbivores())