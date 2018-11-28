#!/usr/bin/python
# -*- coding: utf-8 -*-

import zmq
import random
import sys
import time
import logging
import string

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
    #   COMANDOS SUB
    #--------------------------------------
    def wait_sendfile(self):
        received=False
        command="SENDFILE"
        self.logger.info("esperando comando: " + command)
        while not received:
            try:
                #msg = self._sub_socket.recv_string()
                topic = self._sub_socket.recv_string(flags=zmq.NOBLOCK)
                msg = self._sub_socket.recv_string(flags=zmq.NOBLOCK)
                self.logger.info("comando topic: " + topic)
                self.logger.info("comando rcv: " + msg)
                items = msg.split(';')
                if items[0]==command:
                    received=True
            except zmq.Again as e:
                self.logger.debug("No message received yet")

            time.sleep(1)


    #--------------------------------------
    #   COMANDOS PUB
    #--------------------------------------

    def send_point(self):
        # sts;type;machine_name;app_name;status;val1;val2;val3
        #cad="PPOLAR"  + ";" + self.header + ";" + str(self.status) + ";" + str(_x) + ";" + str(_y) + ";" + str(_z) + ";"
        cad="PCART"  + ";" + self.header + ";" + str(self.status) + ";" + str(_x) + ";" + str(_y) + ";" + str(_z) + ";"
        self.send_msg( "STS" , cad)

    def send_station(self,x,y,z):
        # sts;type;machine_name;app_name;status;val1;val2;val3
        #cad="P_POLAR"  + ";" + self.header + ";" + str(self.status) + ";" + str(_x) + ";" + str(_y) + ";" + str(_z) + ";"
        self.set_random_name()
        cad="STATION"  + ";" + self.header + ";" + str(self.status) + ";" + str(x) + ";" + str(y) + ";" + str(z) + ";"
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

    def file(self,filename="output_x_y_z.txt"):
        global _x;
        global _y;
        global _z;

        coords=filename[:-4]        #borra .txt
        items=coords.split("_")     #x,y,z
        if (len(items)!=4):
            self.logger.warning("faltan elementos de posicion en nombre " + filename)

        self.wait_sendfile()
        self.send_station(10.0*float(items[1]), 10.0*float(items[2]), 10.0*float(items[3]) )
        time.sleep(1)

        with open(filename) as f:
            #content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            #content = [x.strip() for x in content]
            for line in f:
                elems=line.rstrip().split(';')
                if len(elems) == 3:
                    _x=10.0*float(elems[0]);
                    _y=10.0*float(elems[1]);
                    _z=10.0*float(elems[2]);
                    self.send_point()

            exit(0)



    def constant(self,valor=50):
        valor=int(valor)    #provoca excepcion si no es int
        self.send_point()     #manda siempre (aunque no cambie el valor)




if __name__ == "__main__":
    drv=SimulDriver()
    drv.init()

    #MAIN
    drv.exec_commands()
