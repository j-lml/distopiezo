class World extends Element {
  
 
   World (float x, float y, float z, float w) {
     super(x,y,z,w);
     
    
    cs=#FFCC00;
    
  }
  
  void display() {
      fill(cf);
      stroke(cs);
      noFill();
    
      pushMatrix();
      changeCoord();

    
      translate(x+w/2, y+w/2, z+w/2);
      box(w);    
      
      popMatrix();
  }
  
}


class Axis extends Element {
  
 
   Axis (float x, float y, float z, float w) {
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
      changeCoord();
      
      translate(x, y, z);    
      rotateY(0.0);
      
      drawAxes(w);
    
      popMatrix();
  }
  
}
