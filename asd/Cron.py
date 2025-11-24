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
        return "Error leyendo"

    times_backup = deepcopy(times)

    try:
        if hora < '00' or hora > '23':
            return "Hora invalida"
        if minuto < '00' or minuto > '59':
            return "Min invalido"

        match (tarea):
            case Tarea.ELIMINAR_TAREA:
                comando = 'del'
                if hora in times['TIMES'] and minuto in times['TIMES'][hora]:
                    ID = hora + minuto
                    times['TIMES'][hora].remove(minuto)
                    if not times['TIMES'][hora]:
                        del times['TIMES'][hora]
                    subprocess.run([script_path, comando, ID], check=True)
                    mensaje = f"Tarea {hora}{minuto} del"
                else:
                    mensaje = f"Sin tarea {hora}{minuto}"

            case Tarea.AGREGAR_TAREA:
                comando = 'add'
                if hora in times['TIMES']:
                    if minuto in times['TIMES'][hora]:
                        mensaje = "Tarea ya existe"
                    else:
                        times['TIMES'][hora].append(minuto)
                        subprocess.run([script_path, comando, hora, minuto, f'{hora}{minuto}'], check=True)
                        mensaje = f"Tarea {hora}{minuto} ok"
                else:
                    times['TIMES'][hora] = [minuto]
                    subprocess.run([script_path, comando, hora, minuto, f'{hora}{minuto}'], check=True)
                    mensaje = f"Tarea {hora}{minuto} ok"

            case Tarea.BORRAR_TAREAS_HORA:
                comando = 'del'
                if hora in times['TIMES']:
                    for minuto in times['TIMES'][hora]:
                        ID = hora + minuto
                        subprocess.run([script_path, comando, ID], check=True)
                    del times['TIMES'][hora]
                    mensaje = f"Tareas {hora}** del"
                else:
                    mensaje = f"Sin tareas {hora}"

            case Tarea.BORRAR_TODAS_LAS_TAREAS:
                comando = 'del'
                for hora_, minutos in times['TIMES'].items():
                    for minuto_ in minutos:
                        ID = hora_ + minuto_
                        subprocess.run([script_path, comando, ID], check=True)
                times['TIMES'].clear()
                mensaje = "Todas borradas"

            case Tarea.DISPENSAR_COMIDA:
                subprocess.run(['python3', 'scripts/dispensa_comida.py'], check=True)
                mensaje = "Dispensado ok"

            case Tarea.OBTENER_IDS_TAREAS:
                ids = ''
                for h, mins in times['TIMES'].items():
                    for m in mins:
                        ids += f"{h}{m};"
                mensaje = ids.strip(";")

            case None:
                mensaje = "Tarea desconoc."

    except Exception as e:
        with open('data/times.json', 'w', encoding='ascii') as f:
            json.dump(times_backup, f, indent=4)
        mensaje = "Error despacho"
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