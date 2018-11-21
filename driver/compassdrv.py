import zmq
import random
import sys
import time
import logging

from logging.handlers import TimedRotatingFileHandler


context=None
socket=None
logger=None
PORT = "8000"
TYPE_DRV = "COMPASS"
MACHINE_NAME = "M1"
APP_NAME = "COMPASS_DRV"
HEADER= TYPE_DRV + ";" + MACHINE_NAME + ";" + APP_NAME

_angle=0;

def get_angle():
    return _angle;

def set_angle(angle):
    global _angle

    try:
        new_angle=float(angle)
    except:
        return

    new_angle = new_angle % 360
    if (new_angle != _angle):
        _angle=new_angle
        send_sts()

def logger_init(path):
    global TYPE_DRV
    global APP_NAME
    global MACHINE_NAME

    #logger
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s", "%Y%m%d %H%M%S")
    logger = logging.getLogger(APP_NAME)
    logger.setLevel(logging.DEBUG)

    #to console
    consoleHandler=logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    #to file
    timehandler = TimedRotatingFileHandler(path,
                                       when="d",
                                       interval=1,
                                       backupCount=5)
    timehandler.setFormatter(logFormatter)
    logger.addHandler(timehandler)

    #init
    logger.debug( "logger_init()" )
    logger.info("machine name: " + MACHINE_NAME )
    logger.info("app name: " + APP_NAME )
    logger.info("driver: " + TYPE_DRV )
    logger.info("log file: " + path )

    return logger

def zmq_init():
    global PORT
    logger.debug( "zmq_init()" )
    logger.info( "zmq: " + zmq.pyzmq_version() )

#    if len(sys.argv) > 1:
#        PORT =  sys.argv[1]
#        int(PORT)

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % PORT)

    logger.info( "bind: " + PORT )

    return socket

def help():
    logger.debug("help()")
    print("drv - v0.1")
    print("help:    muestra ayuda")
    print("run:     ejecuta programa principal")
    print("compass:     ejecuta programa principal")
    exit(0);

def send_msg(topic,message_data):
    socket.send("%s %s" % (topic, message_data))
    logger.info("" + "["+ topic +"]," + message_data )

def send_hello():
    # hi;type;machine_name;app_name;status;val1;val2;val3
    cad="HI"  + ";" + HEADER + ";"
    send_msg( "HI" , cad)

def send_sts():
    # sts;type;machine_name;app_name;status;val1;val2;val3
    cad="STS"  + ";" + HEADER + ";" + "ON" + ";" + str(get_angle()) + ";"
    send_msg( "STS" , cad)

def run():
    logger.debug("run()")
    while True:
        topic = random.randrange(9999,10005)
        messagedata = random.randrange(1,215) - 80
        print "%d %d" % (topic, messagedata)
        #socket.send("%d %d" % (topic, messagedata))
        socket.send("%d %d" % (topic, messagedata))
        time.sleep(1)

def compass():
    logger.debug("compass()")
    count=0
    HEARTBEAT=5
    while True:
        count=count+1
        if ( count % HEARTBEAT == 0):
            count=0
            rango = random.randrange(0,36000)
            rango = float(rango) / float(100)
            set_angle(rango)

        time.sleep(1)


def parse_commands():
    logger.debug("parse_commands()")
    params=sys.argv
    print(params)
    if len(params)<=1:
        help()

    func,param="",""
    items=None
    try:
        #ejecuta la funcion correspondiente
        #   a) si no tiene parametros: ej app run => run()
        #   b) si tiene un param: ej app test:connection => test("connection")
        items=params[1].split(':')
        if (len(items)==1):
            globals()[items[0]]()
        if (len(items)==2):
            globals()[items[0]](items[1])
    except Exception as e:
        print getattr(e, 'message', repr(e))
        help()




if __name__ == "__main__":
    #LOGGING
    log_file = APP_NAME.lower() + ".log"
    logger=logger_init(log_file)
    #ZMQ
    socket=zmq_init()
    send_hello()

    #MAIN
    parse_commands()
