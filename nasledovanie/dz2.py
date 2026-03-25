class Counter:
    def __init__(self, start=0):
        self.value = max(0, start)

    def inc(self, n=1):
        self.value += n

    def dec(self, n=1):
        self.value -= n
        if self.value < 0:
            self.value = 0

class NonDecCounter(Counter):
    def dec(self, n=1):
        pass

c1 = NonDecCounter(5)
c1.inc(3)
c1.dec(10)

print(c1.value)

class LimitedCounter(Counter):
    def __init__(self, start=0, limit=10):
        super().__init__(start)
        self.limit = limit
        if self.value > self.limit:
            self.value = self.limit

    def inc(self, n=1):
        self.value += n
        if self.value > self.limit:
            self.value = self.limit

c2 = LimitedCounter(8, limit=10)
c2.inc(5)
print(c2.value)

c2.dec(3)
print(c2.value)