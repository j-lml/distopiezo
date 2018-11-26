

class PiezoDisto extends Element {
  
  
  float _azimuth=0;  //FRENTE=0 IZQ=-90 DCHA=90 ATRAS=180
  float _polar=0;
  float _radio=0;
  
  ArrayList<Point> _points = new ArrayList<Point>();
  

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
  
  Point getCartesianPoint(float x, float y, float z) {
    
    Point point=new Point( x, y, z );
    //la referencia es el propio disto!
    point.setReference(this.x,this.y,this.z);   
    
    return point;
  }

  
  Point getPolarPoint(float rho, float theta, float phi) {
    float x, y, z;
    //theta: inclinacion
    //phi:   angulo
    
    println("r,t,p "+ rho, theta, phi);
    
    //ajustes para que sea como en pantalla
    theta=-1.0*theta+90;
    phi=phi+90;
    
    
    theta=radians(theta);
    phi=radians(phi);    
    println("r,tr,pr "+ rho, theta, phi);
    
    
    x = rho * sin(theta) * cos(phi);
    y = rho * sin(theta) * sin(phi);
    z = rho * cos(theta);
    
    //Point point=new Point( x, y, z );  //referencia a 0
    Point point=this.getCartesianPoint( x, y, z ); //referencia a disto
    
    return point;
  }
  
  Point getPolarPoint(float rho) {
    return this.getPolarPoint(rho, this._polar, this._azimuth);   
  }
  
  void addPoint(float rho) {
    Point p=this.getPolarPoint(rho);
    _points.add(p);
  }
  
   


  void display() {
    fill(cf);
    stroke(cs);
    
    pushMatrix();
      changeCoord();
       
      translate(x, y, z);    
      rotateZ(radians(_azimuth));
      rotateX(radians(_polar));
      box(w/10, w, w/10);
      
      stroke(192,192,192);
     
     
      line(0,0,0, 0,w+1,0);
    popMatrix();
    
    
    for (Point part : _points) {
        part.display();
     } 
      
   
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
  
  int _transp=255;
  void drawTrace() {
    if (_transp>0) {_transp-=5;}
    stroke(175,200,200,_transp);
    line(0,0,0, x,y,z);
  }
  
  void display() {
      fill(cf);
      stroke(cs);
      //noFill();
    
    
      pushMatrix();
      changeCoord();       
      
      translate(ox, oy, oz); 
      drawTrace();
      
      pushMatrix();      
      translate(x, y, z);    
      //rotateY(0.0);
      
      drawLines(w);
      //box(0.5);    
      popMatrix();
      
      popMatrix();
  }
  
}
