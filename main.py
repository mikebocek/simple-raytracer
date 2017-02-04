import numpy as np
import matplotlib.pyplot as plt

from objects import Camera, Sphere

height = 480
width = 640

c = Camera(np.array([0,0,-4]), np.array([0,0,1.0]), width, height, 30, 1)
spheres = [Sphere(np.array([-3,1,5]), 1), Sphere(np.array([0,1,3]), 1)]

pixels = np.zeros((height, width))

for i in range(width):
    for j in range(height):
        v = c.vector_from_pixels(i, j)
        for sphere in spheres:
            p = sphere.intersection_point(c.pos, v)
            if p is not None:
                pixels[j, i] = 1
                break


plt.imshow(pixels)
plt.savefig('sphere.png')
