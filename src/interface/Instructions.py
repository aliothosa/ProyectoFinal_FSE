from enum import Enum, auto

class Tarea(Enum):
    ELIMINAR_TAREA = auto() # A
    AGREGAR_TAREA = auto() # B
    BORRAR_TAREAS_HORA = auto() # BB
    OBTENER_IDS_TAREAS = auto() # Caso especial (# # #)
    BORRAR_TODAS_LAS_TAREAS = auto() # BA
    DISPENSAR_COMIDA = auto() # AA
    