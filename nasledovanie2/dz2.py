class Animal:
    def __init__(self, name):
        self.name = name

    def makeNoise(self):
        return "Некоторый звук"

    def eat(self):
        return "Некоторая еда"

    def getDescription(self):
        return "Животное"

class Dog(Animal):
    def makeNoise(self):
        return "Гав-гав"

    def eat(self):
        return "Мясо, кости"

    def getDescription(self):
        return "Собака — друг человека"

class Cat(Animal):
    def makeNoise(self):
        return "Мяу"

    def eat(self):
        return "Рыба, корм"

    def getDescription(self):
        return "Кошка — пушистый тыгыдык"

class Bear(Animal):
    def makeNoise(self):
        return "ААА"

    def eat(self):
        return "Ягоды, рыба, мед"   

    def getDescription(self):
        return "Медведь — сел в машину и..."

class Veterinarian:
    def treatAnimal(self, animal: Animal):
        print(f"Пришел на прием: {animal.name}")
        print(f"Описание: {animal.getDescription()}")

animals = [
    Dog("Шарик"),
    Cat("Мурка"),
    Bear("Медведь")
]

vet = Veterinarian()

print("Прием у ветеринара:")
for a in animals:
    vet.treatAnimal(a)
    print("")

print("Звуки и питание:")
for a in animals:
    print(f"{a.name}: звук - {a.makeNoise()}, ест {a.eat()}")