import numpy as np
import matplotlib.pyplot as plt

class Sphere():
    """
    Object representing a sphere in the scene
    """
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
    
    def intersection_point(self, source, ray):
        direction = ray-source / np.linalg.norm(ray - source)
        center_direction = source - self.center
        a = direction @ direction
        b = 2 * direction @ center_direction
        c = center_direction @ center_direction - np.square(self.radius) 
        discriminant_sq = b*b - 4*a*c
        if discriminant_sq < 0:
            return None
        else:
            solution_1 = (-b + np.sqrt(discriminant_sq))/(2*a)
            solution_2 = (-b - np.sqrt(discriminant_sq))/(2*a)
            t = min(solution_1, solution_2)
        return source + t * direction

    def normal_vector(self, intersection):
        return intersection - self.center

    def color(self, intersection_point, light_sources):
        base_color = 0.5
        color = 0
        normal_vector = self.normal_vector(intersection_point)
        for light_source in light_sources:
            normed_light = (intersection_point - light_source.point)
            normed_light /= np.linalg.norm(normed_light)
            color += base_color * (normal_vector @ normed_light)
        return color
