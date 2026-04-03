from abc import ABC, abstractmethod

class ChessPiece(ABC):
    def __init__(self, horizontal, vertical):
        self.horizontal = horizontal
        self.vertical = vertical

    @abstractmethod
    def can_move(self, h, v):
        pass

class King(ChessPiece):
    def can_move(self, h, v):
        horiz_map = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8}
        current_h = horiz_map[self.horizontal]
        current_v = self.vertical
        target_h = horiz_map[h]
        target_v = v
        diff_h = abs(current_h - target_h)
        diff_v = abs(current_v - target_v)
        return diff_h <=1 and diff_v <=1 and (diff_h + diff_v > 0)

class Knight(ChessPiece):
    def can_move(self, h, v):
        horiz_map = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8}
        current_h = horiz_map[self.horizontal]
        current_v = self.vertical
        target_h = horiz_map[h]
        target_v = v
        diff_h = abs(current_h - target_h)
        diff_v = abs(current_v - target_v)
        return (diff_h==2 and diff_v==1) or (diff_h==1 and diff_v==2)

k1 = King('e',4)
k2 = King('a',1)
kn1 = Knight('b',1)
kn2 = Knight('g',8)

pieces = [k1,k2,kn1,kn2]

moves = [('e',5),('f',5),('g',6),('c',3),('d',2),('b',3),('h',7),('f',6)]

for p in pieces:
    for m in moves:
        res = p.can_move(m[0], m[1])
        print(p.__class__.__name__ + " at " + p.horizontal + str(p.vertical) + " can move to " + m[0] + str(m[1]) + ": " + str(res))
