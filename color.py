from numbers import Number
import numpy as np

class Color():
    def __init__(self, color):
        # If alpha channel is not provided
        if len(color) == 3:
            self.color = np.array(list(color)+[1], dtype=np.float64)
        elif len(color) == 4:
            self.color = np.array(color, dtype=np.float64)
        else:
            raise ValueError("Unrecognized color format")
        if (self.color > 1).sum():
            raise ValueError("Colors must lie in rgba space between 0 and 1")

    def __add__(self, other):
        # Return sum of channels, but clipped to 255
        return np.min(np.array([self.color + other.color, 
                       np.ones(4)]), axis=0
                     )

    def __mul__(self, other):
        if isinstance(other, Number):
            altered_colors = np.append(self.color[0:3] * other, self.color[3])
            return np.min(np.array([altered_colors, 
                           np.ones(4)]), axis=0
                         )
        else:
            raise ValueError("Can only multiply color by scalar")

    def __repr__(self):
        return 'Color(r: {} g: {} b: {} a: {})'.format(*list(self.color))
