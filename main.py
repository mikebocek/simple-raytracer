import numpy as np
import matplotlib.pyplot as plt

from objects import Camera, Sphere, Light

height = 500
width = 500

c = Camera(np.array([0,0,-4]), np.array([0,0,1.0]), width, height, 30, 1)
spheres = [Sphere(np.array([0,-2,5]), 1)]
lights = [Light(np.array([1000,1000,-1000]))]

pixels = np.zeros((height, width))

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
