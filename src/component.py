from adt import *


class component:
    def __init__(self, name) -> None:
        self.name = name

    def alpha(self, n, x, y):
        return None

    def Mx(self):
        return [lambda n,z : z]

    def My(self):
        return [lambda n,z : z]

    def __str__(self) -> str:
        return self.name


class CRZ0N(component):
    def alpha(self, n, x, y):
        Eq = delta(BVtrunc(x, n), BVtrunc(y, n))
        return sumPhase([phase(Eq, BVref(x, 0))])

    def Mx(self):
        return [lambda n, y: y]

    def My(self):
        return [lambda n, x: x]


class move1(component):
    def alpha(self, n, x, y):
        Eq = delta(BVtrunc(x, n-1), BVtrunc(y, n, 1)) * \
            delta(BVref(y, 0), bv(0))
        return getSumPhase([(Eq, bv(0))])

    def Mx(self):
        return [lambda n, y: BVtrunc(y, n, 1), lambda n, y: BVtrunc(y, n, 1) | 1 << n]

    def My(self):
        return [lambda n, x: BVtrunc(x, n-1) << 1, lambda n, x: BVtrunc(x, n-1) << 1 | bv(1)]


class CRZN(component):
    def alpha(self, n, x, y):
        Eq = delta(BVtrunc(x, n-1), BVtrunc(y, n-1))
        d0 = Eq*delta(BVref(y, n), bv(0))
        d1 = Eq*delta(BVref(y, n), bv(1))
        return getSumPhase([(d0, bv(0)), (d1, BVtrunc(x, n))])

    def Mx(self):
        return [lambda n, y: BVtrunc(y, n-1),
                lambda n, y: BVtrunc(y, n-1) | (bv(1) << n)]

    def My(self):
        return [lambda n, x: BVtrunc(x, n-1),
                lambda n, x: BVtrunc(x, n-1) | (bv(1) << n)]



class H0(component):
    def alpha(self, n, x, y):
        Eq = If(n > 0, delta(BVtrunc(x, n, 1), BVtrunc(y, n, 1)), bv(1))
        d0 = Eq*delta(BVref(y, 0), bv(0))
        d1 = Eq*delta(BVref(y, 0), bv(1))
        return getSumPhase([(d0, bv(0)), (d1, BVref(x, 0))])

    def Mx(self):
        return [lambda n, y: BVtrunc(y, n, 1) | bv(0),
                lambda n, y: BVtrunc(y, n, 1) | bv(1)]

    def My(self):
        return [lambda n, x: BVtrunc(x, n, 1) | bv(0),
                lambda n, x: BVtrunc(x, n, 1) | bv(1)]


class HN(component):
    def alpha(self, n, x, y):
        Eq = If(n > 0, delta(BVtrunc(x, n-1), BVtrunc(y, n-1)), bv(1))
        d0 = Eq*delta(BVref(y, n), bv(0))
        d1 = Eq*delta(BVref(y, n), bv(1))
        return sumPhase([phase(d0, bv(0)), phase(d1, BVref(x, n))])

    def Mx(self):
        return [lambda n, y: BVtrunc(y, n-1) | bv(0) << n,
                lambda n, y: BVtrunc(y, n-1) | bv(1) << n]

    def My(self):
        return [lambda n, x: BVtrunc(x, n-1) | bv(0) << n,
                lambda n, x: BVtrunc(x, n-1) | bv(1) << n]


def oneBitAdder(x, y, a, b, c):
    Eq1 = delta(BVref(x, a), BVref(y, a))
    Eq2 = delta(BVref(y, b), BVref(BVref(x, a) + BVref(x, b) + BVref(x, c), 0))
    Eq3 = delta(BVref(y, c), BVref(BVref(x, a) + BVref(x, b) + BVref(x, c), 1))
    return getSumPhase([(Eq1*Eq2*Eq3, bv(0))])

class MAJN(component):
    def alpha(self, n, x, y):
        return oneBitAdder(x, y, n/2, n, 0)

    def Mx(self):
        return [lambda n, y: BVtrunc(y, n-1, 1)<<1 | bv(1), lambda n, y: BVtrunc(y, n-1, 1)<<1, lambda n, y: BVtrunc(y, n-1, 1)<<1 | bv(1) << n, lambda n, y: BVtrunc(y, n-1, 1)<<1 | (bv(1) | bv(1) << n)]

    def My(self):
        return [lambda n, y: BVtrunc(y, n-1, 1)<<1 | bv(1), lambda n, y: BVtrunc(y, n-1, 1)<<1, lambda n, y: BVtrunc(y, n-1, 1)<<1 | bv(1) << n, lambda n, y: BVtrunc(y, n-1, 1)<<1 | (bv(1) | bv(1) << n)]


class Ident(component):
    def alpha(self, n, x, y):
        Eq = delta(x, y)
        return getSumPhase([(Eq, bv(0))])

    def Mx(self):
        return [lambda n,z : z]

    def My(self):
        return [lambda n,z : z]