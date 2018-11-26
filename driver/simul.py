#!/usr/bin/python
# -*- coding: utf-8 -*-

import zmq
import random
import sys
import time
import logging

from logging.handlers import TimedRotatingFileHandler

from basedrv import *


class SimulDriver(BaseDriver):

    _x = 0
    _y = 0
    _z = 0

    def __init__(self):
        self.PORT = "8005"
        self.TYPE_DRV = "SIMUL"
        self.MACHINE_NAME = "M1"
        self.APP_NAME = "S1"
        BaseDriver.__init__(self)

    #--------------------------------------
    #   PROPIEDADES
    #--------------------------------------

    #--------------------------------------
    #   COMANDOS
    #--------------------------------------

    def send_point(self):
        # sts;type;machine_name;app_name;status;val1;val2;val3
        #cad="P_POLAR"  + ";" + self.HEADER + ";" + str(self.status) + ";" + str(_x) + ";" + str(_y) + ";" + str(_z) + ";"
        cad="PCART"  + ";" + self.HEADER + ";" + str(self.status) + ";" + str(_x) + ";" + str(_y) + ";" + str(_z) + ";"
        self.send_msg( "STS" , cad)

    def help(self):
        BaseDriver.help(self)
        print("random:     ejecuta programa principal generando posiciones aleatorias")

    def random(self,valor=50):
        global _x;
        global _y;
        global _z;
        valor=int(valor)  #provoca excepcion si no es int
        _x = random.randrange(0,valor)
        _y = random.randrange(0,valor)
        _z = random.randrange(0,valor)
        self.send_point()


    def constant(self,valor=50):
        valor=int(valor)    #provoca excepcion si no es int
        self.send_point()     #manda siempre (aunque no cambie el valor)




if __name__ == "__main__":
    drv=SimulDriver()
    drv.init()

    #MAIN
    drv.exec_commands()
