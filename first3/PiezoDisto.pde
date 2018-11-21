class Element {
  int x, y, z, w;  
  color cf,cs;
  
  Element (int x, int y, int z, int w) {
    this.x = x;
    this.y = y;
    this.z = z;
    this.w = w;   
    
    cs=#FFFFFF;    
    cf=#FFFFFF;
  }
  
  
  void changeColor() {
    cf = color(
      int(random(0, 255)),
      int(random(0, 255)),
      int(random(0, 255))
    );    
    
     cs=#FFFFFF;
  }
  
}

class PiezoDisto extends Element {
  
  float inc=0;
  float ori=-90;  //FRENTE=0 IZQ=90 DCHA=-90 ATRAS=180

  PiezoDisto (int x, int y, int z, int w) {
    super(x,y,z,w);
    
    cs=#FFFFFF;    
  }
  
  void setAngle(float angle) {
    ori=angle;
  }
  
  void setInc(float angle) {
    inc=angle;
  }
  


  void display() {
    fill(cf);
    stroke(cs);
    
    pushMatrix();
       
      translate(x, y, z);    
      rotateY(radians(ori));
      rotateX(radians(inc));
      box(w/10,w/10,w);
      
      stroke(192,192,192);
      line(0,0,0,0,0,w+1);
    popMatrix();
  }
}

class World extends Element {
  
 
   World (int x, int y, int z, int w) {
     super(x,y,z,w);
     
    
    cs=#FFCC00;
    
  }
  
  void display() {
      fill(cf);
      stroke(cs);
      noFill();
    
      pushMatrix();

    
      translate(x+w/2, y+w/2, z+w/2);
      box(w);    
      
      popMatrix();
  }
  
}


class Axis extends Element {
  
 
   Axis (int x, int y, int z, int w) {
     super(x,y,z,w);
    
    cs=#FFCC00;
    
  }
  
  void drawAxes(float size){
    //X  - red
    stroke(192,0,0);
    line(0,0,0,size,0,0);
    //Y - green
    stroke(0,192,0);
    line(0,0,0,0,size,0);
    //Z - blue
    stroke(0,0,192);
    line(0,0,0,0,0,size);
  }
  
  void display() {
      fill(cf);
      stroke(cs);
      noFill();
    
      pushMatrix();
      
      translate(x, y, z);    
      rotateY(0.0);
      
      drawAxes(w);
    
      popMatrix();
  }
  
}


class Point extends Element {
  
 
   Point (int x, int y, int z) {
     super(x,y,z,1);
    
    cs=#FF0000;
    cf=color(240, 0, 0, 255);
    
  }
  
  
  void drawLines(float size){
    //X  - red
    stroke(cs);    
    line(0-size/2,0,0,size/2,0,0);
    //Y - green
    stroke(cs);
    line(0,0-size/2,0,0,size/2,0);
    //Z - blue
    stroke(cs);
    line(0,0,0-size/2,0,0,size/2);
  }
  
  void display() {
      fill(cf);
      stroke(cs);
      //noFill();
    
      pushMatrix();
      
      translate(x, y, z);    
      rotateY(0.0);
      
      drawLines(w);
      //box(0.5);
    
      popMatrix();
  }
  
}
