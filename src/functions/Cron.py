from __future__ import annotations
import subprocess, json
from unittest import case
from src.interface.Instructions import Tarea
from copy import deepcopy

def despachar_tarea(tarea: Tarea, hora:str, minuto: str,
                    script_path:str = 'scripts/cron/anx_cron.sh') -> str:

    mensaje = ""
    error = False

    # --- lectura segura ---
    try:
        with open('data/times.json', 'r', encoding='ascii') as f:
            times = json.load(f)
    except Exception as e:
        print("Error al leer times.json:", e)
        return "Error leyendo"

    times_backup = deepcopy(times)

    # --- validación ---
    try:
        h = int(hora)
        m = int(minuto)
        if not (0 <= h <= 23):
            return "Hora invalida"
        if not (0 <= m <= 59):
            return "Min invalido"
    except:
        return "Formato invalido"

    ID = f"{h:02d}{m:02d}"

    try:
        match tarea:

            case Tarea.ELIMINAR_TAREA:
                comando = 'del'
                if hora in times['TIMES'] and minuto in times['TIMES'].get(hora, []):
                    times['TIMES'][hora].remove(minuto)
                    if not times['TIMES'][hora]:
                        del times['TIMES'][hora]
                    subprocess.run([script_path, comando, ID], check=True)
                    mensaje = f"Tarea {ID} del"
                else:
                    mensaje = f"Sin tarea {ID}"

            case Tarea.AGREGAR_TAREA:
                comando = 'add'
                if hora in times['TIMES']:
                    if minuto in times['TIMES'].get(hora, []):
                        mensaje = "Tarea ya existe"
                    else:
                        times['TIMES'][hora].append(minuto)
                        subprocess.run([script_path, comando, hora, minuto, ID], check=True)
                        mensaje = f"Tarea {ID} ok"
                else:
                    times['TIMES'][hora] = [minuto]
                    subprocess.run([script_path, comando, hora, minuto, ID], check=True)
                    mensaje = f"Tarea {ID} ok"

            case Tarea.BORRAR_TAREAS_HORA:
                comando = 'del'
                minutos = times['TIMES'].get(hora, [])
                if minutos:  
                    for minuto_ in list(minutos):
                        ID_ = f"{int(hora):02d}{int(minuto_):02d}"
                        subprocess.run([script_path, comando, ID_], check=True)
                    del times['TIMES'][hora]
                    mensaje = f"Tareas {hora}** del"
                else:
                    mensaje = f"Sin tareas {hora}"


            case Tarea.BORRAR_TODAS_LAS_TAREAS:
                comando = 'del'
                for h_, mins in list(times['TIMES'].items()):
                    for m_ in mins:
                        ID_ = f"{int(h_):02d}{int(m_):02d}"
                        subprocess.run([script_path, comando, ID_], check=True)
                times['TIMES'].clear()
                mensaje = "Todas borradas"

            case Tarea.DISPENSAR_COMIDA:
                subprocess.run(['python3', 'scripts/dispensa_comida.py'], check=True)
                mensaje = "Dispensado ok"

            case Tarea.OBTENER_IDS_TAREAS:
                ids = []
                for h_ in sorted(times['TIMES']):
                    for m_ in sorted(times['TIMES'][h_]):
                        ids.append(f"{h_}{m_}")
                mensaje = ";".join(ids)

            case None:
                mensaje = "Tarea desconoc."

    except Exception as e:
        error = True
        print("Error:", e)
        with open('data/times.json', 'w', encoding='ascii') as f:
            json.dump(times_backup, f, indent=4)
        mensaje = "Error despacho"

    finally:
        if not error:
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