import peasy.*;

 

PeasyCam camera;
PiezoDisto disto;
 

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

    camera = new PeasyCam(this, 0, 0, 0, 50);

    camera.setMinimumDistance(0);

    camera.setMaximumDistance(500);


    disto=new PiezoDisto(
      -15 + (int)random(30),
      -15 + (int)random(30),
      -15 + (int)random(30),
      5 + (int)random(15));
      
    disto.changeColor();
   

  //noLoop();

}

 

// The statements in draw() are run until the

// program is stopped. Each statement is run in

// sequence and after the last line is read, the first

// line is run again.

void draw() {

  background(0);   // Set the background to black

 

  pushMatrix();

 

  translate(58, 48, 0);

  rotateY(0.0);

  noFill();

  box(40);

  

  popMatrix();
  
  
  disto.display();

 

  

}

 

void mousePressed() {

  //loop();

}
