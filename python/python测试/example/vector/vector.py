class Vector:
    def __init__(self, x, y):
        if isinstance(x, (int, float)) and \
           isinstance(y, (int, float)):
            self.x = x
            self.y = y
        else:
            raise ValueError("not a number")
    def add(self, other):
        return Vector(self.x + other.x,
                      self.y + other.y)
    def mul(self, factor):
        return Vector(self.x * other.x,
                      self.y * other.y)
    def dot(self, factor):
        return self.x * other.x + self.y * other.y
    
    def norm(self):
        return (self.x * self.x + self.y * self.y) ** 0.5