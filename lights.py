from color import Color

class PointLight():
    def __init__(self, point, color = Color([1,1,1])):
        self.point = point
        self.color = color
