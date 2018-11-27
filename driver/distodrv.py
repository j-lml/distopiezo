#!/usr/bin/python
# -*- coding: utf-8 -*-

import zmq
import random
import sys
import time
import logging

from logging.handlers import TimedRotatingFileHandler

from basedrv import *


class DistoDriver(BaseDriver):

    _distance=0;

    def __init__(self):
        self.PORT = "8003"
        self.TYPE_DRV = "DISTO"
        self.MACHINE_NAME = "M1"
        self.APP_NAME = "D1"
        BaseDriver.__init__(self)

    #--------------------------------------
    #   PROPIEDADES
    #--------------------------------------
    @property
    def distance(self):
        return self._distance;

    @distance.setter
    def distance(self, distance):
        try:
            new_distance=float(distance)
        except:
            self.logger.debug("distance ["+ distance +"] - no es float()")
            return

        if (new_distance != self.distance):
            self._distance=new_distance
            self.send_sts()

    #--------------------------------------
    #   COMANDOS
    #--------------------------------------

    def send_sts(self):
        # sts;type;machine_name;app_name;status;val1;val2;val3
        cad="STS"  + ";" + self.header + ";" + str(self.status) + ";" + str(self.distance) + ";"
        self.send_msg( "STS" , cad)

    def help(self):
        BaseDriver.help(self)
        print("random:     ejecuta programa principal generando posiciones aleatorias")

    def random(self,valor=50):
        valor=int(valor)  #provoca excepcion si no es int
        a = random.randrange(0,valor)
        self.distance=a+20 #20 es valor minimo que puede devolver random

    def constant(self,valor=50):
        valor=int(valor)    #provoca excepcion si no es int
        self.distance=valor
        self.send_sts()     #manda siempre (aunque no cambie el valor)








if __name__ == "__main__":
    drv=DistoDriver()
    drv.init()

    #MAIN
    drv.exec_commands()
