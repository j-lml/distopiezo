#!/usr/bin/python
# -*- coding: utf-8 -*-

import zmq
import random
import sys
import time
import logging
import string

from logging.handlers import TimedRotatingFileHandler

#pip install zmq
#pip install
#pip install numpy
#pip install numpy-stl
#eliminar pip unistall stl si error)

class BaseDriver(object):

    logger=None

    _context=None
    _pub_socket=None
    _sub_socket=None
    _status="ON"

    PORT = "8000"
    TYPE_DRV = "GENERIC"
    MACHINE_NAME = "M1"
    APP_NAME = "GENERIC_DRV"

    HEARTBEAT=3


    def __init__(self):
        pass

    #--------------------------------------
    #   PROPIEDADES
    #--------------------------------------
    @property
    def header(self):
        return self.TYPE_DRV + ";" + self.MACHINE_NAME + ";" + self.APP_NAME

    @property
    def name(self):
        return self.APP_NAME;

    @name.setter
    def name(self, nombre):
        self.APP_NAME=nombre

    @property
    def status(self):
        return self._status;

    @status.setter
    def status(self, estado):
        if estado not in ["ON", "OFF", "ERR"]:
            self.logger.debug("estado ["+ estado +"] - no valido")
            return

        if (estado != self.status):
            self._status=estado
            self.send_sts()

    #--------------------------------------
    #   METODOS PROTECTED (usados de forma interna ppalmente)
    #--------------------------------------
    def set_random_name(self):
        self.APP_NAME='DISTO'+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

    #--------------------------------------
    #   METODOS INIT
    #--------------------------------------
    def logger_init(self):
        #logger
        path = self.APP_NAME.lower() + ".log"

        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

        logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s", "%Y%m%d %H%M%S")
        self.logger = logging.getLogger(self.APP_NAME)
        self.logger.setLevel(logging.DEBUG)

        #to console
        consoleHandler=logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        self.logger.addHandler(consoleHandler)

        #to file
        timehandler = TimedRotatingFileHandler(path,
                                           when="d",
                                           interval=1,
                                           backupCount=5)
        timehandler.setFormatter(logFormatter)
        self.logger.addHandler(timehandler)

        #init
        self.logger.debug( "logger_init()" )
        self.logger.info("machine name: " + self.MACHINE_NAME )
        self.logger.info("app name: " + self.APP_NAME )
        self.logger.info("driver: " + self.TYPE_DRV )
        self.logger.info("log file: " + path )

    def zmq_pub_port(self):
        return self.PORT
    def zmq_sub_port(self):
        return str( int(self.PORT) + 1000 )
    def zmq_init(self):
        self.logger.debug( "zmq_init()" )
        self.logger.info( "zmq: " + zmq.pyzmq_version() )


        #contexto
        self._context = zmq.Context()
        #pub socket
        self._pub_socket = self._context.socket(zmq.PUB)
        self._pub_socket.bind("tcp://*:%s" % self.zmq_pub_port() )
        #sub socket
        self._sub_socket = self._context.socket(zmq.SUB)
        self._sub_socket.connect("tcp://localhost:%s" % self.zmq_sub_port())

        #subscribir a tema
        filter = ""
        # Python 2 - ascii bytes to unicode str
        if isinstance(filter, bytes):
            filter = filter.decode('ascii')
        self._sub_socket.setsockopt_string(zmq.SUBSCRIBE, filter)


        self.logger.info( "pub  bind: " + self.zmq_pub_port() )
        self.logger.info( "sub bind: " + self.zmq_sub_port() )

    def init(self):
        #LOGGING
        self.logger_init()
        #ZMQ
        self.zmq_init()
        #envia saludo para inicializar msg. se necesita pq se pierde el primero!
        self.send_hello()

    #--------------------------------------
    #   GESTION SOCKET
    #--------------------------------------

    #envia mensaje a pelo
    def send_msg(self,topic,message_data):
        #ref: http://zguide.zeromq.org/php:chapter2#Pub-Sub-Message-Envelopes
        #topic y msg en mismo nivel:
        #self._pub_socket.send("%s %s" % (topic, message_data))
        #para separar topic de msg:
        self._pub_socket.send_multipart([topic, message_data])
        self.logger.info("" + "["+ topic +"]," + message_data )

    def send_command(self,command,data):
        msg=command + ";" + self.header + ";" + data;
        self.send_msg("COMMAND", msg)

    def send_event(self,event,data):
        msg=event + ";" + self.header + ";"+ self.status + ";" + data;
        self.send_msg("EVENT", msg)

    #bloquea la ejecucion hasta que llega por socket el comando deseado y al final ejecuta la funcion
    def wait_sck_command(self, command, timeout=10):
        received=False
        self.logger.info("basedrv::wait_sck_commmand() - esperando comando: " + command)
        times=0
        while not received and times<=timeout:
            try:
                #msg = self._sub_socket.recv_string()
                topic = self._sub_socket.recv_string(flags=zmq.NOBLOCK)
                msg = self._sub_socket.recv_string(flags=zmq.NOBLOCK)
                self.logger.debug("comando topic: " + topic)
                self.logger.debug("comando rcv: " + msg)
                items = msg.split(';')
                if topic=="COMMAND" and items[0].upper()==command:
                    received=True
            except zmq.Again as e:
                pass

            if received==False:
                self.logger.debug("basedrv::wait_sck_commmand() - no message received yet. waiting " + command)

            time.sleep(1)
            times+=1

        if times>=timeout:
            self.logger.info("basedrv::wait_sck_commmand() - timeout "+ str(timeout) + "s esperando comando: " + command)
            exit(0)

        if received==True:
            self.logger.info("basedrv::wait_sck_commmand() - recibido comando: " + command)
            self.exec_command(command)

    #lee de sub_socket pero no bloque. devuelve None,None,None si error
    def read_sck_command(self):
        topic=None
        cmd=None
        msg=None
        try:
            #msg = self._sub_socket.recv_string()
            topic = self._sub_socket.recv_string(flags=zmq.NOBLOCK)
            msg = self._sub_socket.recv_string(flags=zmq.NOBLOCK)
            cmd=msg.split(';')[0]
        except zmq.Again as e:
            pass
        return topic,cmd,msg

    #lee de sub_socket y bloquea
    def read_sck_command_sync(self):
        topic = self._sub_socket.recv_string()
        msg = self._sub_socket.recv_string()
        cmd=msg.split(';')[0]
        return topic,cmd,msg

    #--------------------------------------
    #   GESTION COMANDOS
    #--------------------------------------

    #ejecuta la funcion que corresponda
    def exec_command(self,command):
        #ejecuta funcion con params separados por : . usado por linea de comandos o subscripcion de comandos
        self.logger.debug("basedrv::exec_command() - "+command)
        func,param="",""
        items=None
        try:
            #ejecuta la funcion correspondiente
            #   a) si no tiene parametros: ej app run => run()
            #   b) si tiene un param: ej app test:connection => test("connection")
            items=command.split(':')
            if (len(items)==1):
                #self.globals()[items[0]]()
                func = getattr(self, items[0] )
                func()
            if (len(items)==2):
                #self.globals()[items[0]](items[1])
                func = getattr(self, items[0] )
                func(items[1])
        except Exception as e:
            self.logger.error("basedrv::exec_comnand() - error al ejecutar funcion." + repr(items))
            print getattr(e, 'message', repr(e))

    #ejecuta la funcion recibida mediante socket (no bloquea)
    def exec_sck_command(self):
        topic, cmd, msg = self.read_sck_command()
        if topic=="COMMAND":
            self.exec_command(cmd)

    #carga el comando y los parametros desde linea de comandos
    def exec_cmd_command(self):
        self.logger.debug("basedrv::exec_cmd_command()")
        params=sys.argv
        if len(params)<=1:
            self.help()
            self.logger.error("basedrv::exec_cmd_command() - faltan parametros. ej: app.py comando:params")
            exit(0)

        self.exec_command(params[1])
        exit(0)



    #--------------------------------------
    #   COMANDOS
    #--------------------------------------
    def help(self):
        self.logger.debug("help()")
        print("basedrv - v0.1")
        print("send_hello   lanza un unico evento. debe ser recibido por todos")
        print("run:comando  ejecuta de forma repetida programa principal. ej: app.py run:send_hello")
        print("help:        muestra ayuda")

    def send_hello(self):
        # hi;type;machine_name;app_name;status;val1;val2;val3        
        self.send_event( "HI" , "")

    def test(self):
        logger.debug("test()")
        while True:
            topic = random.randrange(9999,10005)
            messagedata = random.randrange(1,215) - 80
            self.logger.info( "%d %d" % (topic, messagedata) )
            #socket.send("%d %d" % (topic, messagedata))
            self._pub_socket.send("%d %d" % (topic, messagedata))
            time.sleep(1)

    def run(self,mode):
        #modo   run:        consigue ejecutar la funcion de siguiete param
        #ej:    run:help
        #ej:    run:random,3
        self.logger.debug("run(mode)"+mode)
        count=0
        while True:
            count=count+1
            if ( count % self.HEARTBEAT == 0):
                items=mode.split(',')
                func=None
                if (len(items)==1):
                    func = getattr(self, items[0] )
                    func()  #ejecuta sin params
                if (len(items)==2):
                    func = getattr(self, items[0] )
                    func(items[1]) #ejecuta con params (string comma separated)

                #    self.error("run(mode) - no existe modo: " + mode)

            self.exec_sck_command()
            time.sleep(1)

    def exit(self, errno=0):
        exit(errno)


if __name__ == "__main__":
    drv=BaseDriver()

    drv.init()
    drv.help()
