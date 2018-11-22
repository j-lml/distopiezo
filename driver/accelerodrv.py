#!/usr/bin/python
# -*- coding: utf-8 -*-

import zmq
import random
import sys
import time
import logging

from logging.handlers import TimedRotatingFileHandler

from basedrv import *


class AcceleroDriver(BaseDriver):

    _gyrox = 0
    _gyroy = 0
    _gyroz = 0


    def __init__(self):
        self.PORT = "8002"
        self.TYPE_DRV = "ACCELERO"
        self.MACHINE_NAME = "M1"
        self.APP_NAME = "A1"
        BaseDriver.__init__(self)


    #--------------------------------------
    #   PROPIEDADES
    #--------------------------------------
    @property
    def girox(self):
        return self._gyrox;

    @girox.setter
    def girox(self, giro):
        try:
            new_angle=float(giro)
        except:
            self.logger.debug("girox ["+ giro +"] - no es float()")
            return

        if new_angle < -90.0 or new_angle > 90:
            self.logger.debug("girox ["+ giro +"] - no esta en rago -90,90")
            return

        if (new_angle != self.girox):
            self._gyrox=new_angle
            self.send_sts()

    @property
    def giroy(self):
        return self._gyroy;

    @giroy.setter
    def giroy(self, giro):
        try:
            new_angle=float(giro)
        except:
            self.logger.debug("giroy ["+ giro +"] - no es float()")
            return

        if new_angle < -90.0 or new_angle > 90:
            self.logger.debug("giroy ["+ giro +"] - no esta en rago -90,90")
            return

        if (new_angle != self.giroy):
            self._gyroy=new_angle
            self.send_sts()

    @property
    def giroz(self):
        return self._gyroz;

    @giroz.setter
    def giroz(self, giro):
        try:
            new_angle=float(giro)
        except:
            self.logger.debug("giroz ["+ giro +"] - no es float()")
            return

        if new_angle < -90.0 or new_angle > 90:
            self.logger.debug("giroz ["+ giro +"] - no esta en rago -90,90")
            return

        if (new_angle != self.giroz):
            self._gyroz=new_angle
            self.send_sts()


    #--------------------------------------
    #   COMANDOS
    #--------------------------------------
    def send_sts(self):
        # sts;type;machine_name;app_name;status;val1;val2;val3
        cad="STS"  + ";" + self.HEADER + ";" + str(self.status) + ";" + str(self.girox) + ";" + str(self.giroy) + ";" + str(self.giroz) + ";"
        self.send_msg( "STS" , cad)

    def random(self):
        self.logger.debug("random()")
        count=0
        while True:
            count=count+1
            if ( count % self.HEARTBEAT == 0):
                count=0
                a = random.randrange(0,18000)
                a = float(a) / float(100)
                a = a - 90
                self.giroy = a

            time.sleep(1)

    def help(self):
        BaseDriver.help(self)
        print("random:     ejecuta programa principal generando posiciones aleatorias")



if __name__ == "__main__":
    drv=AcceleroDriver()
    drv.init()

    #MAIN
    drv.exec_commands()
