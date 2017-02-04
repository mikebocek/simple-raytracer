import numpy as np
import matplotlib.pyplot as plt

class Camera():
    def __init__(self, pos, look_position, x_pixels, y_pixels, field_of_view, distance_from_plane):
        self.pos = pos
        self.look_vector = (pos - look_position)
        self.look_vector /= np.linalg.norm(self.look_vector)

        self.x_pixels = x_pixels
        self.y_pixels = y_pixels

        self._obtain_basis_vectors()
        self._obtain_look_parameters(field_of_view, distance_from_plane)


        # Some basic checks on the parameters
        assert 0 < field_of_view < 180
        assert x_pixels > 0 and isinstance(x_pixels, int)
        assert y_pixels > 0 and isinstance(y_pixels, int)

    def vector_from_pixels(self, x_pos, y_pos):
        # Ray should be cast within the camera frame
        assert x_pos < self.x_pixels and y_pos < self.y_pixels
        y_component = (self.v * (y_pos/self.y_pixels))
        x_component = (self.u * (x_pos * self.width/self.x_pixels))
        look_vector = self.lower_plane_position + x_component  + y_component
        return look_vector / np.linalg.norm(look_vector)

    def _obtain_basis_vectors(self):
        self.u = np.cross(self.look_vector, np.array([0,1,0]))
        self.u /= np.linalg.norm(self.u)
        self.v = np.cross(self.look_vector, self.u) # Guaranteed to be normalized
    def _obtain_look_parameters(self, field_of_view, distance_from_plane):
        aspect_ratio = self.x_pixels/self.y_pixels
        C = self.pos - self.look_vector
        self.height = 2 * distance_from_plane * np.tan(field_of_view/180 * np.pi * 0.5)
        self.width = self.height * aspect_ratio
        self.lower_plane_position = C - (self.u * self.width/2) - (self.v * self.height/2)

class Sphere():
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

class Light():
    def __init__(self, point):
        self.point = point
