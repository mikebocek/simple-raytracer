import numpy as np

from color import Color

class LambertShader():
    @staticmethod
    def shade(intersection_point, normal_vector, material_color, light_sources):
        color = material_color
        for light_source in light_sources[:1]:
            normed_light = (intersection_point - light_source.point)
            normed_light /= np.linalg.norm(normed_light)
            color.color = np.array([0,0.3,0]) * (normal_vector @ normed_light)
        return color
