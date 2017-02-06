import numpy as np

from color import Color

class LambertShader():
    @staticmethod
    def shade(intersection_point, normal_vector, material_color, light_source):
        normed_light = (light_source.point - intersection_point)
        normed_light /= np.linalg.norm(normed_light)
        return Color(material_color.color[0:3] * (normal_vector @ normed_light))
