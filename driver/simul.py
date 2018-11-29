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

    SCALE = 10.0

    def __init__(self):
        self.PORT = "8005"
        self.TYPE_DRV = "SIMUL"
        self.MACHINE_NAME = "M1"
        self.APP_NAME = "S1"
        BaseDriver.__init__(self)



    #--------------------------------------
    #   COMANDOS PUB
    #--------------------------------------
    def help(self):
        BaseDriver.help(self)
        print("random       lanza un evento con puntos cartesianos aleatorios. usado en pruebas.")
        print("constant     lanza un evento con puntos cartesianos concretos. usado en pruebas.")
        print("send_point:x,y,z      lanza un evento con punto cartesianos concreto")
        print("send_station:x,y,z    lanza un evento con estacion en cierto punto")
        print("file:nombrefich_x_y_z.txt    procesa el fichero de puntos indicado")

    def random(self,valor=50):
        valor=int(valor)  #provoca excepcion si no es int
        x = random.randrange(0,valor)
        y = random.randrange(0,valor)
        z = random.randrange(0,valor)
        self.send_point(x,y,z)

    def constant(self,valor=50):
        valor=int(valor)    #provoca excepcion si no es int
        self.send_point(valor,valor,valor)     #manda siempre (aunque no cambie el valor)

    def send_point(self,x,y,z):
        try:
            x=self.SCALE*float(x);
            y=self.SCALE*float(y);
            z=self.SCALE*float(z);

            # sts;type;machine_name;app_name;status;val1;val2;val3
            #cad="PPOLAR"  + ";" + self.header + ";" + str(self.status) + ";" + str(x) + ";" + str(y) + ";" + str(z) + ";"
            cad="PCART"  + ";" + self.header + ";" + str(self.status) + ";" + str(x) + ";" + str(y) + ";" + str(z) + ";"
            self.send_msg( "STS" , cad)
        except:
            self.logger.error("simul::send_point() - parametro no es de tipo float "+str(x)+","+str(y)+","+str(z))

    def send_station(self,x,y,z):
        try:
            x=float(self.SCALE)*float(x);
            self.logger.debug("simul::send_station() - " + str(x))
            y=float(self.SCALE)*float(y);
            self.logger.debug("simul::send_station() - " + str(y))
            z=float(self.SCALE)*float(z);
            self.logger.debug("simul::send_station() - " + str(z))


            # sts;type;machine_name;app_name;status;val1;val2;val3
            #cad="P_POLAR"  + ";" + self.header + ";" + str(self.status) + ";" + str(_x) + ";" + str(_y) + ";" + str(_z) + ";"
            self.set_random_name()
            self.logger.info("simul::send_station() - " + self.name)
            cad="STATION"  + ";" + self.header + ";" + str(self.status) + ";" + str(x) + ";" + str(y) + ";" + str(z) + ";"
            self.send_msg( "STS" , cad)
            self.logger.info("simul::send_station() - " + self.cad)
        except:
            self.logger.error("simul::send_station() - parametro no es de tipo float "+str(x)+","+str(y)+","+str(z))

    def file(self,filename="output_x_y_z.txt"):
        coords=filename[:-4]        #borra .txt
        items=coords.split("_")     #x,y,z
        if (len(items)!=4):
            self.logger.warning("faltan elementos de posicion de disto en nombre " + filename)

        self.wait_sck_command("SENDFILE")
        self.send_station(items[1], items[2], items[3] )
        self.send_msg( "STS" , "START_TRANSMISSION")
        time.sleep(1)

        with open(filename) as f:
            #content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            #content = [x.strip() for x in content]
            for line in f:
                elems=line.rstrip().split(';')
                if len(elems) == 3:
                    self.send_point(elems[0],elems[1],elems[2])
                self.exec_sck_command()

        self.send_msg( "STS" , "END_TRANSMISSION")



if __name__ == "__main__":
    drv=SimulDriver()
    drv.init()

    #MAIN
    drv.exec_cmd_command()
