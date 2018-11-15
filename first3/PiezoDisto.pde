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

  PiezoDisto (int x, int y, int z, int w) {
    super(x,y,z,w);
    
    cs=#FFFFFF;    
  }


  void display() {
    fill(cf);
    stroke(cs);
    
    pushMatrix();
      translate(x, y, z);
      box(w);
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
      
      translate(x, y, z);    
      rotateY(0.0);
      box(w);
    
      popMatrix();
  }
  
}
