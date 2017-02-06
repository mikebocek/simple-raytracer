import numpy as np
from scipy.misc import imsave

from objects import Sphere
from camera import Camera
from lights import PointLight
from shaders import LambertShader
from color import Color

width = 640
height = 480

c = Camera(np.array([0,0,-4.0]), np.array([0,0,2.0]), height, width, 30, 2)
spheres = [Sphere(np.array([0,0,5]), 1), Sphere(np.array([4,0,10]), 1)]
lights = [PointLight(np.array([-1000,-1000,1000]))]

pixels = np.zeros((height, width, 3))

material = LambertShader()
texture = Color([0.0,0.3,0.3])
bg_color = Color([0,0,0])

def truncate(vector, minimum, maximum):
    min_truncated = np.max(np.array([vector, np.full(vector.shape, minimum, dtype=np.int64)]), axis=0)
    return np.min(np.array([min_truncated, np.full(vector.shape, maximum, dtype=np.int64)]), axis=0)


def main():
    print(texture.color[0:3])
    for i in range(height):
        for j in range(width):
            v = c.vector_from_pixels(i, j)
            for sphere in spheres:
                p = sphere.intersection_point(c.pos, v)
                if p is not None:
                    n = sphere.normal_vector(p)
                    pixels[i, j, :] = truncate(255 * material.shade(p, n, texture, lights).color[0:3], 0, 255)
                    break
                else:
                    pixels[i, j, :] = truncate(255*bg_color.color[0:3], 0 ,255)

    np.save('test.npy', pixels)
    imsave('Sphere.png', pixels)

if __name__ == '__main__':
    main()
