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
   * publicar por red información
   * recibir por red órdenes



## utilidades python

## dependecias

