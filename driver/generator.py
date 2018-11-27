#!/usr/bin/python
# -*- coding: utf-8 -*-


import numpy
import time
from stl import mesh, stl



import zmq
import random
import sys
import time
import logging

from logging.handlers import TimedRotatingFileHandler

from basedrv import *

#directorio donde se encuentran los modelos STL
DATAPATH="../data/"

#--------------------------------------
#   METODOS
#--------------------------------------
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



class GeneratorDriver(BaseDriver):


    def __init__(self):
        self.PORT = "8006"
        self.TYPE_DRV = "GENERATOR"
        self.MACHINE_NAME = "M1"
        self.APP_NAME = "G1"
        BaseDriver.__init__(self)

    #--------------------------------------
    #   PROPIEDADES
    #--------------------------------------

    #--------------------------------------
    #   METODOS
    #--------------------------------------

    def help(self):
        BaseDriver.help(self)
        print("cloud:     genera cloudpoints. ej: ")

    def sphere(self, filename, fileoutput, ray_origin):
        # Using an existing stl file:
        your_mesh = mesh.Mesh.from_file(filename)
        file = open(fileoutput,'w')

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

    #--------------------------------------
    #   COMANDOS
    #--------------------------------------

    #ej: python generator.py cloud:turing.stl,sphere,1,1,1
    def cloud(self, params='turing.stl,sphere,1,1,1)'):
        start_time = time.time()

        plist=params.split(",")

        #origen por defecto
        ray_origin = numpy.array([1,1,1])
        #origen si se pasa por params
        #ej: python generator.py sphere:turing.stl,1,2,1
        if (len(plist)==5):
            ray_origin = numpy.array([float(plist[2]),float(plist[3]),float(plist[4])])


        #fichero stl
        filename=DATAPATH+plist[0];
        #nombre de fichero = output_xyz.txt
        fileoutput="output_"+str(ray_origin[0])+"_"+str(ray_origin[1])+"_"+str(ray_origin[2])+".txt"

        self.logger.info("path de modelos: " + DATAPATH);
        self.logger.info("modelo a cargar: " + filename);
        self.logger.info("output: " + fileoutput)
        self.logger.info("origen: " + repr(ray_origin))

        #si hay param[1] => ejecutar funcion indicada
        #si no => ejecutar funcion por defecto (sphere)
        if (len(plist)>=2):
            func = getattr(self, plist[1] )
            func(filename,fileoutput,ray_origin)
        else:
            sphere(filename,fileoutput,ray_origin)




if __name__ == "__main__":
    drv=GeneratorDriver()
    drv.init()

    #MAIN
    drv.exec_commands()
