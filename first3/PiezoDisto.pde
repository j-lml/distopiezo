class Element {
  int x, y, z, w;
  
  color cf,cs;
  
}

class PiezoDisto extends Element {

  PiezoDisto (int x, int y, int z, int w) {
    this.x = x;
    this.y = y;
    this.z = z;
    this.w = w;
    this.changeColor();
    
  }

  void changeColor() {
    cf = color(
      int(random(0, 255)),
      int(random(0, 255)),
      int(random(0, 255))
    );    
    
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

class World {
  
   int x, y, z, w;  
   color cf,cs;
   
   World (int x, int y, int z, int w) {
    this.x = x;
    this.y = y;
    this.z = z;
    this.w = w;    
    
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
