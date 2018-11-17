import peasy.*;

 

PeasyCam camera;
PiezoDisto disto;
World world;
Axis axis;
Point p;


ArrayList<Point> points = new ArrayList<Point>();

float y = 100;

// The statements in the setup() function

// run once when the program begins

void setup() { 

  size(640, 480, P3D);

 

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
      5 + (int)random(15));
      
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

  background(0);   // Set the background to black
  
  world.display();
  disto.display();
  
  axis.display();
  
  p.display();
  
  
  for (Point part : points) {
    part.display();
  }

}

 

void mousePressed() {

  //loop();

}
