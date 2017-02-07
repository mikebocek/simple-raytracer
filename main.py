import numpy as np
from scipy.misc import imsave

from objects import Sphere
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
                point_color = self.trace_ray(self.camera.pos, v)
                if point_color is not None:
                    self.pixels[i, j, :] = truncate(255 * point_color.color[0:3], 0, 255)

                else:
                    self.pixels[i, j, :] = np.array([0,0,0])
        return self.pixels

    def trace_ray(self, point, vector):
        for obj in self.objects:
            intersection = obj.intersection_point(point, vector)
            if intersection is not None:
                point_color = Color([0,0,0.0])
                for light_source in self.lights:
                    point_color.color += obj.shade(intersection, light_source).color
                return point_color
        else:
            return None

def truncate(vector, minimum, maximum):
    """
    Given an array, and a minimum and maximum, clips all
    the values in the array to lie between the minimum and 
    maximum
    """
    min_truncated = np.max(np.array([vector, np.full(vector.shape, minimum, dtype=np.int64)]), axis=0)
    return np.min(np.array([min_truncated, np.full(vector.shape, maximum, dtype=np.int64)]), axis=0)


def main():
    
    camera = Camera(np.array([0,0,-4.0]), np.array([0,0,2.0]), 240, 320, 30, 2)
    
    spheres = [Sphere(np.array([0,0,5]), 0.5, Color([1,0,0]), [LambertShader()]),
               Sphere(np.array([2,1,5]), 0.5, Color([0,1,0]), [LambertShader()])]
    lights = [PointLight(np.array([0,2,-4.0]))]
    
    scene = Scene(camera, spheres,lights)

    pixels = scene.render()
   
    np.save('test.npy', pixels)
    imsave('Sphere.png', pixels)

if __name__ == '__main__':
    main()
