import numpy as np
from scipy.misc import imsave

from objects import Sphere, Plane
from camera import Camera
from lights import PointLight
from shaders import LambertShader
from color import Color

class Scene():
    """
    Holds camera, light and object information and provides methods
    for rendering the scene
    """
    def __init__(self, camera, objects, lights):
        self.camera = camera
        self.objects = objects
        self.lights = lights
        # Array of pixels - width and height of image, with 3 color channels
        self.pixels = np.zeros((camera.x_pixels, camera.y_pixels, 3))

    def render(self):
        """
        Renders the scene described in the class, returning an array of pixel
        values
        """
        for i in range(self.camera.x_pixels):
            for j in range(self.camera.y_pixels):
                v = self.camera.vector_from_pixels(i, j)
                obj, intersection = self.trace_ray(self.camera.pos, v)
                if obj is not None:
                    point_color = Color([0,0,0])
                    shadow = False
                    for light in self.lights:
                        blocking_object, _ = self.trace_ray(intersection, light.point - intersection)
                        if blocking_object is not None and blocking_object != obj:
                            shadow = True
                        if not shadow:
                            point_color.color += obj.shade(intersection, light).color
                    self.pixels[i, j, :] = truncate(255 * point_color.color[0:3], 0, 255)
                else:
                    self.pixels[i, j, :] = np.array([0,0,0])
        return self.pixels

    def trace_ray(self, point, vector):
        distances = np.full(len(self.objects), np.nan)
        intersection_points = np.full((len(self.objects), 3), np.nan)
        for i, obj in enumerate(self.objects):
            intersection = obj.intersection_point(point, vector)
            if intersection is not None:
                intersection_points[i] = intersection
                distances[i] = np.linalg.norm(intersection - self.camera.pos)
        if not (~np.isnan(distances)).sum(): 
            return None, None
        return self.objects[distances.argsort()[0]], intersection_points[distances.argsort()[0], :]

def truncate(vector, minimum, maximum):
    """
    Given an array, and a minimum and maximum, clips all
    the values in the array to lie between the minimum and 
    maximum
    """
    min_truncated = np.max(np.array([vector, np.full(vector.shape, minimum, dtype=np.int64)]), axis=0)
    return np.min(np.array([min_truncated, np.full(vector.shape, maximum, dtype=np.int64)]), axis=0)


def main():
    
    camera = Camera(np.array([0, 3.5,-4]), np.array([0,0,5.0]), 120, 160, 30, 2)
    
    obj = [Sphere(np.array([-1.7,1,3.5]), 0.5, Color([1,0,0]), [LambertShader()]),
           Sphere(np.array([2,1,5]), 3, Color([0,1,0]), [LambertShader()])
           #, Plane(np.array([0,0,7]), np.array([0,0,-1]), Color([0,0,1]), [LambertShader()])
          ]
    lights = [PointLight(np.array([-10,0,4.0]))]
    
    scene = Scene(camera, obj,lights)

    pixels = scene.render()
   
    np.save('test.npy', pixels)
    imsave('Sphere_partial.png', pixels)

if __name__ == '__main__':
    main()
