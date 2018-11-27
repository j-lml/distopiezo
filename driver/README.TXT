
HEADER= TYPE_DRV;MACHINE_NAME;APP_NAME;
STATUS= ON | OFF

//-----------------------------------------
// COMANDOS
//-----------------------------------------

python generator.py cloud:turing.stl,sphere,1,1,1
python simul.py file:output_x_y_z.txt



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
