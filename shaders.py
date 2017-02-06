import numpy as np

from color import Color

class LambertShader():
    @staticmethod
    def shade(intersection_point, normal_vector, material_color, light_sources):
        color = material_color
        for light_source in light_sources[:1]:
            normed_light = (intersection_point - light_source.point)
            normed_light /= np.linalg.norm(normed_light)
            color = Color(material_color.color[0:3] * (normal_vector @ normed_light))
        return color
