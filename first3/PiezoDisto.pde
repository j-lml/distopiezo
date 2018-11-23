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
  
}

class PiezoDisto extends Element {
  
  
  float _azimuth=0;  //FRENTE=0 IZQ=-90 DCHA=90 ATRAS=180
  float _polar=0;
  float _radio=20;

  PiezoDisto (float x, float y, float z,float w) {
    super(x,y,z,w);
    
    cs=#FFFFFF;    
  }
  
  void setAzimuth(float angle) {
    _azimuth=angle;
  }
  
  void setPolar(float angle) {
    _polar=angle;
  }
  
  void setRadio(float distance) {
    _radio=distance;
  }
  
  PVector getVector(float r) {    
    //a partir de distacia r (y datos de orientacion del disto) => obtener Pvector con coordenadas
    //float x1=r*cos(_azimuth)*sin(_polar);
    //float y1=r*sin(_azimuth)*sin(_polar);
    //float z1=r*cos(_polar);
    
    //float x1=r*cos(_azimuth)*sin(_polar);    
    //float y1=r*cos(_polar);
    //float z1=r*sin(_azimuth)*sin(_polar);
    
    float y1=r*cos(_polar);
    float x1=r*sin(_azimuth)*sin(_azimuth);
    float z1=r*cos(_azimuth)*sin(_polar);
    
    println(_azimuth,_polar,r);
    println(x1,y1,z1);
    println("-------");
    
    
    return new PVector(x1,y1,z1);
  }
  


  void display() {
    fill(cf);
    stroke(cs);
    
    pushMatrix();
       
      translate(x, y, z);    
      rotateZ(radians(_azimuth));
      rotateX(radians(_polar));
      box(w/10, w, w/10);
      
      stroke(192,192,192);
      line(0,0,0, 0,w+1,0);
    popMatrix();
  }
}

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
      
      translate(x, y, z);    
      rotateY(0.0);
      
      drawAxes(w);
    
      popMatrix();
  }
  
}


class Point extends Element {
  
 
   Point (float x, float y, float z) {
     super(x,y,z,1);
    
    cs=#FF0000;
    cf=color(240, 0, 0, 255);
    
  }
  
  
  void drawLines(float size){
    //X  - red
    stroke(cs);    
    line(0-size/2,0,0, size/2,0,0);
    //Y - green
    stroke(cs);
    line(0,0-size/2,0, 0,size/2,0);
    //Z - blue
    stroke(cs);
    line(0,0,0-size/2, 0,0,size/2);
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
