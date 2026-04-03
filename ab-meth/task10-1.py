import abc

class Middle(abc.ABC):
    def __init__(self, user_votes, expert_votes):
        self.user_votes = user_votes                   # пользовательские оценки
        self.expert_votes = expert_votes               # оценки критиков

    def get_correct_user_votes(self):
        """Возвращает нормализованный список пользовательских оценок
        без слишком низких и слишком высоких значений"""
        return [vote for vote in self.user_votes if 10 < vote < 90]

    def get_correct_expert_votes(self):
        """Возвращает нормализованный список оценок критиков
        без слишком низких и слишком высоких значений"""
        return [vote for vote in self.expert_votes if 5 < vote < 95]

    @abc.abstractmethod
    def get_average(self, users=True):
        """Абстрактный метод для вычисления среднего значения"""
        pass

class Average(Middle):
    def get_average(self, users=True):
        """Возвращает среднее арифметическое пользовательских оценок или
        оценок критиков в зависимости от значения параметра users"""
        if users:
            votes = self.get_correct_user_votes()
        else:
            votes = self.get_correct_expert_votes()

        return sum(votes) / len(votes)

class Median(Middle):
    def get_average(self, users=True):
        """Возвращает медиану пользовательских оценок или
        оценок критиков в зависимости от значения параметра users"""
        if users:
            votes = sorted(self.get_correct_user_votes())
        else:
            votes = sorted(self.get_correct_expert_votes())

        return votes[len(votes) // 2]

class Harmonic(Middle):
    def get_average(self, users=True):
        """Возвращает среднее гармоническое пользовательских оценок или
        оценок критиков в зависимости от значения параметра users"""
        if users:
            votes = self.get_correct_user_votes()
        else:
            votes = self.get_correct_expert_votes()

        return len(votes) / sum(map(lambda vote: 1 / vote, votes))

if __name__ == "__main__":
    user_votes = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95]
    expert_votes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    avg = Average(user_votes, expert_votes)
    med = Median(user_votes, expert_votes)
    harm = Harmonic(user_votes, expert_votes)

    print("Average user:", avg.get_average(users=True))
    print("Average expert:", avg.get_average(users=False))
    print("Median user:", med.get_average(users=True))
    print("Median expert:", med.get_average(users=False))
    print("Harmonic user:", harm.get_average(users=True))
    print("Harmonic expert:", harm.get_average(users=False))