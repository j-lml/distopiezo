#!/usr/bin/python
# -*- coding: utf-8 -*-

import zmq
import random
import sys
import time
import logging

from logging.handlers import TimedRotatingFileHandler

from basedrv import *


class CompassDriver(BaseDriver):

    _angle=0;

    def __init__(self):
        self.PORT = "8001"
        self.TYPE_DRV = "COMPASS"
        self.MACHINE_NAME = "M1"
        self.APP_NAME = "C1"
        BaseDriver.__init__(self)

    #--------------------------------------
    #   PROPIEDADES
    #--------------------------------------
    @property
    def angle(self):
        return self._angle;

    @angle.setter
    def angle(self, giro):

        try:
            new_angle=float(giro)
        except:
            self.logger.debug("angle ["+ giro +"] - no es float()")
            return

        new_angle = new_angle % 360

        if (new_angle != self.angle):
            self._angle=new_angle
            self.send_sts()

    #--------------------------------------
    #   COMANDOS
    #--------------------------------------

    def send_sts(self):
        # sts;type;machine_name;app_name;status;val1;val2;val3
        cad=str(self.angle) + ";"
        self.send_event( "STS" , cad)

    def random(self,valor=360):
        valor=int(valor)  #provoca excepcion si no es int
        a = random.randrange(0,valor*100)
        a = float(a) / float(100)
        self.angle=a

    def constant(self,valor=0):
        valor=int(valor)    #provoca excepcion si no es int
        self.angle=valor
        self.send_sts()     #manda siempre (aunque no cambie el valor)

    def help(self):
        BaseDriver.help(self)
        print("random:     ejecuta programa principal generando posiciones aleatorias")



if __name__ == "__main__":
    drv=CompassDriver()
    drv.init()

    #MAIN
    drv.exec_cmd_command()
