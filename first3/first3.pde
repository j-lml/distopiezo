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
  subscriber.connect("tcp://127.0.0.1:5556");
  String filter="";
  subscriber.subscribe(filter.getBytes());
  
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
  //String rcv = subscriber.recvStr();
  //println(rcv);


}

 

void mousePressed() {

  //loop();

}
