class Word:
    def __init__(self, word):
        self.word = word

    def __repr__(self):
        return f"Word('{self.word}')"

    def __str__(self):
        return self.word.capitalize()

    def _len(self):
        return len(self.word)

    def __eq__(self, other):
        if isinstance(other, Word):
            return self._len() == other._len()
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Word):
            return self._len() != other._len()
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Word):
            return self._len() < other._len()
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Word):
            return self._len() <= other._len()
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Word):
            return self._len() > other._len()
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Word):
            return self._len() >= other._len()
        return NotImplemented

w1 = Word("hello")
w2 = Word("world")
w3 = Word("hi")

print(w1 == w2)
print(w1 > w3)
print(w3 < w2)
print(w1)
print(repr(w1))