import numpy as np
import matplotlib.pyplot as plt

from color import Color

class Sphere():
    """
    Object representing a sphere in the scene
    """
    def __init__(self, center, radius, texture, shaders):
        self.center = center
        self.radius = radius
        self.shaders = shaders
        self.texture = texture 
    
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

    def shade(self, point, light_source):
        composite_color = Color([0,0,0])
        for shader in self.shaders:
            composite_color.color += shader.compute_color(point, self.normal_vector(point), self.texture, light_source).color
        return composite_color

    def __eq__(self, other):
        """
        Equality comparison
        """
        return all(self.center == other.center) and self.radius == other.radius

class Plane():
    def __init__(self, center, normal, texture, shaders):
        self.center = center
        self.normal = normal/np.linalg.norm(normal)
        self.texture = texture
        self.shaders = shaders
        self.offset =  -(self.center @ self.normal)

    def intersection_point(self, source, ray):
        ray = ray / np.linalg.norm(ray)
        a = -(self.normal @ ray)
        b = (self.normal @ source) + self.offset
        if a == 0:
            return None
        t = b/a
        if t < 0: # Intersection is behind camera
            return None
        return source + (t * ray)

    def normal_vector(self, point):
        return self.normal

    def shade(self, point, light_source):
        composite_color = Color([0,0,0])
        for shader in self.shaders:
           composite_color.color += shader.compute_color(point, self.normal_vector(point), self.texture, light_source).color
        return composite_color
