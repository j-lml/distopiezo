#!/usr/bin/python
# -*- coding: utf-8 -*-


import numpy
import time
from stl import mesh, stl

def ray_triangle_intersection(ray_near, ray_dir, v123):
    v1, v2, v3 = v123
    eps = 0.000001
    edge1 = v2 - v1
    edge2 = v3 - v1
    pvec = numpy.cross(ray_dir, edge2)
    det = edge1.dot(pvec)
    if abs(det) < eps:
        return False, None
    inv_det = 1. / det
    tvec = ray_near - v1
    u = tvec.dot(pvec) * inv_det
    if u < 0. or u > 1.:
        return False, None
    qvec = numpy.cross(tvec, edge1)
    v = ray_dir.dot(qvec) * inv_det
    if v < 0. or u + v > 1.:
        return False, None

    t = edge2.dot(qvec) * inv_det
    if t < eps:
        return False, None

    return True, t

def pol2cart(rho, theta, phi):
    x = rho * numpy.sin(theta) * numpy.cos(phi)
    y = rho * numpy.sin(theta) * numpy.sin(phi)
    z = rho * numpy.cos(theta)
    return numpy.array([x, y, z])


if __name__ == "__main__":
    start_time = time.time()

    # Using an existing stl file:
    your_mesh = mesh.Mesh.from_file('../data/turing.stl')
    ray_origin = numpy.array([1,1,1])

    file = open('output_xyz.txt','w')

    d_theta = numpy.pi / 90.0
    theta = 0.0
    while theta < numpy.pi:

        d_phi = (2*numpy.pi / 180.0 / numpy.sin(theta)) if (numpy.sin(theta) > 0) else (2*numpy.pi)
        phi = 0.0
        while phi < 2*numpy.pi:

            ray_dir = pol2cart(1.0, theta, phi)

            for i in range(your_mesh.v0.size/3):
                hit, distance = ray_triangle_intersection(ray_origin, ray_dir, [your_mesh.v0[i], your_mesh.v1[i], your_mesh.v2[i]])
                if hit:
                    point = pol2cart(distance, theta, phi)
                    file.write('{0};{1};{2}\n'.format(point[0], point[1], point[2]))

            phi = phi + d_phi

        theta = theta + d_theta

    file.close()
