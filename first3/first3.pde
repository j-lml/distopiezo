import peasy.*;
import org.zeromq.ZMQ;
 

PeasyCam camera;
PiezoDisto disto;
World world;
Axis axis;
Point p; 
ZMQ.Socket subscriber;

ArrayList<Point> points = new ArrayList<Point>();
float y = 100;

 

// The statements in the setup() function
// run once when the program begins
void setup() { 
  //ZMQ
  ZMQ.Context context = ZMQ.context(1);
  subscriber = context.socket(ZMQ.SUB);
  subscriber.connect("tcp://127.0.0.1:8001");
  subscriber.connect("tcp://127.0.0.1:8002");
  subscriber.connect("tcp://127.0.0.1:8003");
  String filter="STS";
  subscriber.subscribe(filter.getBytes());
  subscriber.setReceiveTimeOut(10);
  
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


    disto=new PiezoDisto(
      +15 + (int)random(30),
      +15 + (int)random(30),
      +15 + (int)random(30),
     10);
      
    world= new World(0,0,0,50);
    
    axis= new Axis(0,0,0,10);    
    p= new Point(-1,-1,-1);
    
    for (int i=0; i<10000; i++) {
      points.add( new Point( (int)random(1300),
      (int)random(1300),
      (int)random(1300) ) );    
    }
    
    
      
    disto.changeColor();
    
    camera.rotateX(0);
    camera.rotateY(0);
    camera.rotateZ(0);
    

  //noLoop();

}



// The statements in draw() are run until the
// program is stopped. Each statement is run in
// sequence and after the last line is read, the first
// line is run again.
void draw() {  
  
  //set the background to black
  background(0);   
  
  //world
  world.display();
  disto.display();  
  axis.display();
  
  //puntos
  p.display(); 
  
  for (Point part : points) {
    part.display();
  }
  
  //ZMQ
   //Msg msg = ZMQ.recv(subscriber, ZMQ.ZMQ_DONTWAIT);
  String rcv = subscriber.recvStr();
  if (rcv != null) {
    println(rcv);
    String[] items = split(rcv, ';');
    
    String _command=items[0];
    String _type=items[1];
    String _machine=items[2];
    String _element=items[3];
    String _status=items[4];   
    String _p1="";
    String _p2="";
    String _p3="";
    
    if (_type.equals("COMPASS")) {
        _p1=items[5];
        disto.setAngle( float(_p1) );
    }
    
    if (_type.equals("ACCELERO")) {
      _p1=items[5];  //x
      _p2=items[6];  //y
      _p3=items[7];  //z    
      disto.setInc( float(_p2) );
    }
    
    if (_type.equals("DISTO")) {        
    }
    
    
    
  }
  


}

 

void mousePressed() {

  //loop();

}
