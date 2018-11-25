class Element {
  float x, y, z, w;  
  color cf,cs;
  
  Element (float x, float y, float z, float w) {
    this.x = x;
    this.y = y;
    this.z = z;
    this.w = w;   
    
    cs=#FFFFFF;    
    cf=#FFFFFF;
  }
  
  float getX() {return x;}
  float getY() {return y;}
  float getZ() {return z;}
  
  
  void changeColor() {
    cf = color(
      int(random(0, 255)),
      int(random(0, 255)),
      int(random(0, 255))
    );    
    
     cs=#FFFFFF;
  }
  
  void changeCoord() {
    scale(-1, 1, 1);
  }
  
  float ox,oy,oz;
  void setReference(float x, float y, float z) {
    ox=x;
    oy=y;
    oz=z;
  }
  
}
