import peasy.*;
import org.zeromq.ZMQ;
import java.util.Map; 

PeasyCam camera;
World world;
Axis axis;
Point p; 
ZMQ.Socket subscriber;
ZMQ.Socket publisher;


  

HashMap<String,PiezoDisto> distos = new HashMap<String,PiezoDisto>();


ArrayList<Point> points = new ArrayList<Point>();
float y = 100;

 

// The statements in the setup() function
// run once when the program begins
void setup() { 
  //ZMQ
  ZMQ.Context context = ZMQ.context(1);
  subscriber = context.socket(ZMQ.SUB);
  subscriber.connect("tcp://127.0.0.1:8001");  //compass
  subscriber.connect("tcp://127.0.0.1:8002");  //accel
  subscriber.connect("tcp://127.0.0.1:8003");  //disto
  subscriber.connect("tcp://127.0.0.1:8005");  //simulador
  String filter="STS";
  subscriber.subscribe(filter.getBytes());
  subscriber.setReceiveTimeOut(10);
  
  //realiza peticiones al simulador
  publisher = context.socket(ZMQ.PUB);
  publisher.bind("tcp://127.0.0.1:9005");  //simulator commands
  delay(100);
 
  
  //SCREEN
  size(640, 480, P3D);
 
  //INIT
  stroke(255);     // Set stroke color to white

    // PeasyCam constructor:
    // PeasyCam(PApplet parent,
    //          double lookAtX, double lookAtY, double lookAtZ,
    //          double distance);
    camera = new PeasyCam(this, 0, 0, 0, 1500);
    camera.setMinimumDistance(0);
    camera.setMaximumDistance(500);

    PiezoDisto disto;
    disto=new PiezoDisto(
      +15 + (int)random(30),
      +15 + (int)random(30),
      +15 + (int)random(30),
     10);             
    disto.changeColor();
    disto.setAzimuth(0);
    disto.setPolar(0); 
    distos.put("PROCESSING",disto);
      
    //crea mundo 
    world= new World(0,0,0,50);    
    axis= new Axis(0,0,0,10);
    
    //crea punto de ref
    p= new Point(-1,-1,-1);
    p.setReference(0,0,0);
    points.add(p);
    
    /*
    for (int i=0; i<1; i++) {
      points.add( new Point( (int)random(1300),
      (int)random(1300),
      (int)random(1300) ) );    
    } */
    
    
   
    
    p=new Point( 1, 1, 1 );
    p.setReference(0,0,0);
    points.add( p );
    p=new Point( 2, 2, 2 );
    p.setReference(2,2,2);
    points.add( p );
    
    p=disto.getCartesianPoint(0,12,0);
    points.add( p );
    p=disto.getPolarPoint(13,0,-0);
    points.add( p );
    
    
    
    camera.rotateX(0);
    camera.rotateY(0);
    camera.rotateZ(0);    

  //noLoop();

}


long _oldtime=0;

// The statements in draw() are run until the
// program is stopped. Each statement is run in
// sequence and after the last line is read, the first
// line is run again.
void draw() {
  
  //ejecuta cada 5 segundos
  long _time=millis();
  if (_time - 5000 > _oldtime) {
      _oldtime=_time;
      publisher.sendMore("COMMAND".getBytes());
      publisher.send("SENDFILE".getBytes());
  } 
  
  //set the background to black
  background(0);   
  
  //IMP: left handed = processing  , right handed = opengl  
  //
  //https://www.evl.uic.edu/ralph/508S98/coordinates.html
  //https://forum.processing.org/one/topic/righ-handed-co-ordinate-system.html
  
  
  //world
  world.display();
  
  //pinta distos
  //Using an enhanced loop to iterate over each entry
  for (Map.Entry me : distos.entrySet()) {
    //print(me.getKey() + " is ");
    //println(me.getValue());
    PiezoDisto d;
    d=(PiezoDisto) me.getValue();
    d.display();
  }
  
  //ejes
  axis.display();
  
  //puntos
  p.display();   
  for (Point part : points) {
    part.display();
  }
  
  //ZMQ
   //Msg msg = ZMQ.recv(subscriber, ZMQ.ZMQ_DONTWAIT);
  String topic=null;
  String rcv=null;
  
  topic= subscriber.recvStr();
  if (topic != null) {
    rcv= subscriber.recvStr();
  }
  
  if (rcv != null) {
    println(rcv);
    String[] items = split(rcv, ";");    
    
    String _command=items[0];
    String _type="";
    String _machine="";
    String _element="";
    String _status="";   
    String _p1="";
    String _p2="";
    String _p3="";
 
    if (items.length >= 5) {
       _command=items[0];
       _type=items[1];
       _machine=items[2];
       _element=items[3];
       _status=items[4];
    }
    
        
    if (_command.contains("STATION") && _type.equals("SIMUL")) {     
      _p1=items[5];  //x
      _p2=items[6];  //y
      _p3=items[7];  //z
      
      PiezoDisto d=new PiezoDisto(float(_p1),float(_p2),float(_p3),10);
      d.setReference(0,0,0);
      d.setName(_element.toUpperCase());
      d.changeColor();
      distos.put(d.getName(), d);
    }
    
    
    //-- OBTIENE EL DISTO AL QUE SE REFIERE EL COMANDO -------
    PiezoDisto disto;
    disto=distos.get( _element.toUpperCase() );    
    if (disto==null) {
        disto=new PiezoDisto(float(_p1),float(_p2),float(_p3),10);
        disto.setReference(0,0,0);
        disto.setName(_element.toUpperCase());      
    }
    
    //-- COMANDOS DE DISPOSITIVO ------------------------------
    if (_command.equals("STS") && _type.equals("COMPASS") ) {
        _p1=items[5];
        disto.setAzimuth( float(_p1) );
    }
    
    if (_command.equals("STS") && _type.equals("ACCELERO")) {
      _p1=items[5];  //x
      _p2=items[6];  //y
      _p3=items[7];  //z    
      disto.setPolar( float(_p1) );
    }
    
    if (_command.equals("STS") && _type.equals("DISTO")) {
       _p1=items[5];  //r       
       disto.addPoint( float(_p1) );
    }
    
    //-- COMANDOS DE SIMULADOR ---------------------------------
    if (_command.equals("PCART") && _type.equals("SIMUL")) {      
       _p1=items[5];  //rho. dist
       _p2=items[6];  //theta. incli
       _p3=items[7];  //phi. angulo
       Point point=disto.getCartesianPoint(float(_p1),float(_p2),float(_p3));
       disto.addPoint(point);       
    }
    
    
    if (_command.equals("PPOLAR") && _type.equals("SIMUL")) {
       _p1=items[5];  //rho. dist
       _p2=items[6];  //theta. incli
       _p3=items[7];  //phi. angulo
       Point point=disto.getPolarPoint(float(_p1),float(_p2),float(_p3));
       disto.addPoint(point);       
    }
    

    
    
    
    
  }
  


}

 

void mousePressed() {

  //loop();

}
