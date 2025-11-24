
class Evento:
    def __init__(self, tipo:Tarea, datos:Dict, respuesta:List):
        self.tipo:Tarea = tipo
        self.datos:Dict[str,str] = datos
        self.respuesta:List = respuesta

class WorkerCron(threading.Thread):
    fila:Queue[Evento] = Queue()
    fila_lock = threading.Lock()
    script_path = 'scripts/cron/anx_cron.sh'

    @classmethod
    def post(cls, task):
        with cls.fila_lock:
            cls.fila.put(task)
    
    def __init__(self):
        with open('data/times.json', 'r') as f:
            self.times = json.load(f)
        super().__init__()
        self.end = False

    def run(self):
        while not(self.end and WorkerCron.fila.empty()):
            try:
                evento:Evento = WorkerCron.fila.get(timeout=1)
                if evento:
                    self.despachar(evento)
            except Empty:
                time.sleep(1)
                pass

        

    def despachar(self, evento:Evento):
        try:
            match(evento.tipo):
                case Tarea.ELIMINAR_TAREA:
                    tarea_id:str = evento.datos.get('tarea_id', '') 
                    if not tarea_id:
                        raise ValueError("Falta el ID de la tarea a eliminar.")
                    comando = 'del'
                    self.ejecutar_script(
                        script_path=WorkerCron.script_path,
                        comando=comando,
                        ID=tarea_id
                    )
                case Tarea.AGREGAR_TAREA:
                    hora:str = evento.datos.get('hora', '')
                    minuto:str = evento.datos.get('minuto', '')
                    if not hora or not minuto:
                        raise ValueError("Faltan hora o minuto para agregar la tarea.")
                    comando = 'add'
                    self.ejecutar_script(
                        script_path=WorkerCron.script_path,
                        comando=comando,
                        hora=hora,
                        minuto=minuto
                    )
                    evento.respuesta.append('Tarea agregada correctamente.')
                case Tarea.OBTENER_IDS_TAREAS:
                    ids_tareas = ''
                    for hora, minutos in self.times['TIMES'].items():
                        for minuto, tarea_id in minutos.items():
                            ids_tareas += f"{tarea_id} "
                    evento.respuesta.append(ids_tareas.strip())
                case Tarea.FINALIZAR:
                    self.save_times()
                    self.finalizar()
                    evento.respuesta.append('WorkerCron finalizado.')
        except ValueError as v:
            
            evento.respuesta.append(str(v))

    def ejecutar_script(self, script_path:str, comando:str, hora:str = '', minuto:str= '', ID:str = '') -> None:
        if comando not in ['add', 'del']:
            raise ValueError(f"Comando inválido: {comando}; debe ser 'add' o 'del'.")
        if hora and (not hora.isdigit() or not (0 <= int(hora) <= 23)):
            raise ValueError(f"Hora inválida: {hora}; debe estar entre 0 y 23.")
        if minuto and (not minuto.isdigit() or not (0 <= int(minuto) <= 59)):
            raise ValueError(f"Minuto inválido: {minuto}; debe estar entre 0 y 59.")
        if comando == 'del' and  (ID  and len(ID) != 4):
            raise ValueError(f"ID inválido: {ID}; deben ser de 4 caracteres.")
        
        match(comando):
            case 'add':
                id_tarea = hora + minuto 
                self.modificar_times(comando, id_tarea)
                subprocess.run([script_path, comando, hora, minuto, id_tarea], check=True)
            case 'del':
                self.modificar_times(comando, ID)
                subprocess.run([script_path, comando, ID], check=True)

    def modificar_times(self, comando: str, id_tarea:str):
        hora = id_tarea[:2]
        minuto = id_tarea[2:]
    
        match(comando):
            case 'add':
                self.times['TIMES'][hora][minuto] = id_tarea 
            case 'del':
                del self.times['TIMES'][hora][minuto]

    def save_times(self):
        with open('data/times.json', 'w') as f:
            json.dump(self.times, f, indent=4)

    def finalizar(self)->None:
        self.end = True

    def format_times(self) -> str:
        out = []
        out.append("HORA | MINUTO | ID")
        out.append("------------------------")
        
        for hora, minutos in self.times["TIMES"].items():
            if not minutos:
                continue
            
            # primer renglón para esa hora
            first = True
            for minuto, id4 in sorted(minutos.items()):
                if first:
                    out.append(f"{hora:>4} | {minuto:>6} | {id4}")
                    first = False
                else:
                    out.append(f"     | {minuto:>6} | {id4}")
            
            out.append("------------------------")
        
        return "\n".join(out)

    

def parse_bool(entrada :str) -> bool:
    if entrada in ['True', 'true', '1', 'yes', 'y']:
        return True
    elif entrada in ['False', 'false', '0', 'no', 'n']:
        return False
    else:
        raise ValueError(f"Invalid boolean string: {entrada}")
