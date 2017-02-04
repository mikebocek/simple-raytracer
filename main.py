import numpy as np
import matplotlib.pyplot as plt

from objects import Sphere
from camera import Camera
from lights import PointLight

height = 500
width = 500

c = Camera(np.array([0,0,-4.0]), np.array([0,0,2.0]), width, height, 30, 2)
spheres = [Sphere(np.array([0,0,5]), 1)]
lights = [PointLight(np.array([1000,1000,-1000])), PointLight(np.array([1000,-1000,45]))]

pixels = np.zeros((height, width))

def main():
    for i in range(width):
        for j in range(height):
            v = c.vector_from_pixels(i, j)
            for sphere in spheres:
                p = sphere.intersection_point(c.pos, v)
                if p is not None:
                    pixels[j, i] = sphere.color(p, lights)
                    break


    plt.imshow(pixels, cmap='Greys')
    plt.axis('off')

    plt.savefig('sphere.png')

if __name__ == '__main__':
    main()
