
HEADER= TYPE_DRV;MACHINE_NAME;APP_NAME;
STATUS= ON | OFF

//-----------------------------------------
// COMANDOS
//-----------------------------------------

python generator.py cloud:turing.stl,sphere,1,1,1
python simul.py file:output_x_y_z.txt

//-----------------------------------------
//PUERTOS
//-----------------------------------------
basedrv     8000,9000
compass     8001,9001
accelero    8002,9002
disto       8003,9003
simul       8005,9005
generator   8006,9006
controller  8007,9007



//-----------------------------------------
// EVENTOS (STS)
//-----------------------------------------
son tipos de eventos,

//envio de puntos
POLAR;HEADER;STATUS;rho;theta(inc);phi(ang);
PCART;HEADER;STATUS;x;y;z;

//envio de posicion de estacion
STATION;HEADER;STATUS;x;y;z;


//-----------------------------------------
// COMANDOS (COMMANDS)
//-----------------------------------------
CHANGE_STATION;ORIGIN
SENDFILE;
