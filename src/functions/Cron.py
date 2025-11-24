from __future__ import annotations
import subprocess, json
from unittest import case
from src.interface.Instructions import Tarea
from copy import deepcopy

def despachar_tarea(tarea: Tarea, hora:str, minuto: str, script_path:str = 'scripts/cron/anx_cron.sh') -> str:
    mensaje = ""
    try:
        with open('data/times.json', 'r', encoding='ascii') as f:
            times = json.load(f)
    except Exception as e:
        print("Error al leer times.json:", e)
        mensaje =  "Error al leer la configuración de tareas."
        return mensaje

    times_backup = deepcopy(times)

    try:
        if hora < '00' or hora > '23':
            mensaje =  f"Hora inválida: {hora}; debe estar entre 00 y 23."
        if minuto < '00' or minuto > '59':
            mensaje =  f"Minuto inválido: {minuto}; debe estar entre 00 y 59."
        

        match (tarea):
            case Tarea.ELIMINAR_TAREA:
                comando = 'del'
                if hora  in times['TIMES']:
                    if minuto in times['TIMES'][hora]:
                        ID = hora+minuto
                        times['TIMES'][hora].remove(minuto)
                        if not times['TIMES'][hora]:
                            del times['TIMES'][hora]
                        subprocess.run(['scripts/cron/anx_cron.sh', comando, ID], check=True)
                        mensaje =  f"Tarea a las {hora}:{minuto} eliminada."
                    else:
                        mensaje =  f"No hay tarea programada a las {hora}:{minuto}."
                    
            case Tarea.AGREGAR_TAREA:
                comando = 'add'
                if hora in times['TIMES']:
                    if minuto in times['TIMES'][hora]:
                        mensaje =  f"Ya existe una tarea programada a las {hora}:{minuto}."
                    else:
                        times['TIMES'][hora].append(minuto)
                        subprocess.run(['scripts/cron/anx_cron.sh', comando, hora, minuto, f'{hora}{minuto}'], check=True)
                        mensaje =  f"Tarea a las {hora}:{minuto} agregada."
                else:
                    times['TIMES'][hora] = [minuto]
                    subprocess.run(['scripts/cron/anx_cron.sh', comando, hora, minuto, f'{hora}{minuto}'], check=True)
                    mensaje =  f"Tarea a las {hora}:{minuto} agregada."
                

            case Tarea.BORRAR_TAREAS_HORA:
                comando = 'del'
                if hora in times['TIMES']:
                    for minuto in times['TIMES'][hora]:
                        ID = hora+minuto
                        subprocess.run(['scripts/cron/anx_cron.sh', comando, ID], check=True)
                    del times['TIMES'][hora]
                    mensaje =  f"Tareas a las {hora}:** eliminadas."
                
                else:
                    mensaje =  f"No hay tareas programadas a las {hora}:**."
            
            case Tarea.BORRAR_TODAS_LAS_TAREAS:
                comando = 'del'
                for hora, minutos in times['TIMES'].items():
                    for minuto in minutos:
                        ID = hora+minuto
                        subprocess.run(['scripts/cron/anx_cron.sh', comando, ID], check=True)
                times['TIMES'].clear()
                mensaje =  "Todas las tareas eliminadas."
            
            case Tarea.DISPENSAR_COMIDA:
                subprocess.run(['python3', 'scripts/dispensa_comida.py'], check=True)
                mensaje =  "Comida dispensada."
            
            case Tarea.OBTENER_IDS_TAREAS:
                ids_tareas = ''
                for hora, minutos in times['TIMES'].items():
                    for minuto in minutos:
                        ids_tareas += f"{hora}:{minuto};"
                mensaje =  ids_tareas.strip()
            
            case None:
                mensaje =  "Tarea desconocida."
        
    except Exception as e:
        with open('data/times.json', 'w', encoding='ascii') as f:
            json.dump(times_backup, f, indent=4)
        mensaje =  f"Error al despachar tarea: {str(e)}"
    finally:
        with open('data/times.json', 'w', encoding='ascii') as f:
            json.dump(times, f, indent=4)
        return mensaje

if __name__ == "__main__":
    # Ejemplo de uso
    resultado = despachar_tarea(Tarea.AGREGAR_TAREA, '14', '30')
    print(resultado)

    # resultado = despachar_tarea(Tarea.ELIMINAR_TAREA, '14', '30')
    # print(resultado)

    #python -m src.functions.Cron