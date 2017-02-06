import numpy as np
from scipy.misc import imsave

from objects import Sphere
from camera import Camera
from lights import PointLight
from shaders import LambertShader
from color import Color

width = 320
height = 240

c = Camera(np.array([0,0,-4.0]), np.array([0,0,2.0]), height, width, 30, 2)
spheres = [Sphere(np.array([0,0,5]), 0.5), Sphere(np.array([2,1,5]), 1)]
lights = [PointLight(np.array([0,2,-4.0]))]#, PointLight(np.array([0,-400,10]))]

pixels = np.zeros((height, width, 3))

material = LambertShader()
texture = Color([1,0,0])
bg_color = Color([0,0,0])

def truncate(vector, minimum, maximum):
    min_truncated = np.max(np.array([vector, np.full(vector.shape, minimum, dtype=np.int64)]), axis=0)
    return np.min(np.array([min_truncated, np.full(vector.shape, maximum, dtype=np.int64)]), axis=0)


def main():
    for i in range(height):
        for j in range(width):
            v = c.vector_from_pixels(i, j)
            for sphere in spheres:
                p = sphere.intersection_point(c.pos, v)
                if p is not None:
                    n = sphere.normal_vector(p)
                    point_color = Color([0,0,0.0])
                    for light_source in lights:
                        point_color.color += material.shade(p, n, texture, light_source).color
                    pixels[i, j, :] = truncate(255 * point_color.color[0:3], 0, 255)
                    """for light_source in lights:
                        v = p - light_source.point
                        shadow = False
                        for other_sphere in spheres:
                            p2 = other_sphere.intersection_point(p, v)
                            if p2 is not None and other_sphere != sphere:
                                shadow = True
                        if not shadow:
                            point_color.color += material.shade(p, n, texture, light_source).color
                    pixels[i, j, :] = truncate(255 * point_color.color[0:3], 0, 255)
                    break
                else:
                    pixels[i, j, :] = truncate(255*bg_color.color[0:3], 0 ,255)
"""
    np.save('test.npy', pixels)
    imsave('Sphere.png', pixels)

if __name__ == '__main__':
    main()
