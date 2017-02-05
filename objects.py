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
        """
        Given the point of view and a vector representing 
        a ray from the point of view, return the point of
        intersection between the ray and the sphere
        """
        direction = ray-source / np.linalg.norm(ray - source)
        center_direction = source - self.center
        # Coefficients for quadratic equation
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
        """
        Given a point of intersection return the normal
        vector to the surface of the sphere
        """
        vec = intersection - self.center
        return vec/np.linalg.norm(vec)
