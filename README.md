# distopiezo
este proyecto contiene un conjunto de herramientas para evaluar la generación de mapas 3d virtuales

```
\
 |-data    modelos 3d en .stl para la generación y nubes de puntos en *.txt para la simulación
 |-driver  utilidades python para creacion y generación de nubes de puntos
 |-first   programa en processing para pintado en 3d
 --test    programas de prueba para acceso a dispositivos (motores o inclinómetro)
```

## arquitectura
el objetivo es crear pequeñas utilidades y que cada una haga una tarea en concreto de forma que sea muy sencillo crear nuevas utilidades o crear nuevos comportamientos (comandos) de esas utilidades.

todas las utilidades que hereden de `BaseDriver` obtienen una funcionalidad de partida que les permite:
   * acceder a las órdenes del intérprete de comandos
   * publicar información en la red (*Zmq* `PUB`)
   * recibir órdenes por la red (*Zmq* `SUB`)


## utilidades python

### intersections.py
codigo original de Fiti

### generator.py

cloud:    crea una nube de puntos a partir de un espacio stl dado, usando una estrategia determinada (`sphere`)  desde una posicion dada X,Y,Z.

los ficheros STL y el resultado se almancenan en `DATAPATH` que, si no se indica lo contrario es `./data`.

```
python generator.py cloud:turing.stl,sphere,1,1,1
```

actualmente solo se encuentra implementada la estrategia de puntos `sphere`, pero se pueden crear distintas estrategias simplemente cerando un metodo equivalente a `def sphere(self, filename, fileoutput, ray_origin):`

### simul.py

a partir de un fichero con el formato `output_x_y_z.txt` envía tanto la posición del disto (x,y,z) como los puntos que contiene el fichero uno a uno. Estos puntos se pueden visualizar con el programa de *processing*.

```
python simul.py file:output_x_y_z.txt
```

otros comandos:

envio de un punto en rango 50, de forma constante, punto determinado o posición de la estación:

```
python simul.py random:50
python simul.py constant:50
python simul.py send_point:x,y,z
python simul.py send_station:x,y,z
```

envio recurrente cada `HEARTBEAT` (definido en `BaseDrv` a 3s) en rango 50:
```
python simul.py run:random,50
python simul.py run:constant,50
```



