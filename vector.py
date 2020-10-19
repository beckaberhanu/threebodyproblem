import math


class Vector:
    def __init__(self, values):
        self.values = values

    def get(self, index):
        return self.values[index]

    def norm(self):
        out = 0
        for i in self.values:
            out += i**2
        out = math.sqrt(out)
        return out

    def toList(self):
        return self.values

    def __str__(self):
        strOut = '['
        for i in self.values:
            strOut += str(round(i)) + ","
        strOut = strOut[:-1] + ']'
        return strOut
        # return str(self.values)
        # return 'Vector:' + str(self.values)

    def __repr__(self):
        return self.__str__()

    def __add__(self, vec2):
        out = [None]*len(self.values)
        for i in range(len(self.values)):
            out[i] = self.values[i] + vec2.get(i)
        return Vector(out)

    def __sub__(self, vec2):
        out = [None]*len(self.values)
        for i in range(len(self.values)):
            out[i] = self.values[i] - vec2.get(i)
        return Vector(out)

    def __mul__(self, num):
        out = [None]*len(self.values)
        for i in range(len(self.values)):
            out[i] = self.values[i] * num
        return Vector(out)

    def __rmul__(self, num):
        out = [None]*len(self.values)
        for i in range(len(self.values)):
            out[i] = self.values[i] * num
        return Vector(out)

    def __truediv__(self, num):
        out = [None]*len(self.values)
        for i in range(len(self.values)):
            out[i] = self.values[i] / num
        return Vector(out)

    def __floordiv__(self, num):
        out = [None]*len(self.values)
        for i in range(len(self.values)):
            out[i] = self.values[i] // num
        return Vector(out)
