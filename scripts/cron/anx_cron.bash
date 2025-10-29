#!/usr/bin/env bash
# Script: cron_update.sh
# Uso:
#   ./cron_update.sh add HH MM ID
#   ./cron_update.sh del ID

set -euo pipefail

# Configuración de variables

# Direccion del interprete de python
PYTHON="$HOME/Projects/ProyectoFinal_FSE/venvFSE/bin/python3" 
# Direccion del script programado para ejecutarse.
SCRIPT="$HOME/Projects/scripts/dispensa_comida.py"
# Direccion del directorio de logs para la ejecución del script por si suceden errores
LOG_DIR="$HOME/cron_logs"
# Definición fine un entorno limpio y predecible dentro del cron.
CRON_PATH="/usr/local/bin:/usr/bin:/bin"

# Crea el directorio de logs si no existe
mkdir -p "$LOG_DIR"

# FUNCIONES DEL SCRIPT

# Validacion de argumentos de ejecución
valid_hhmm() {
  local hh="$1" mm="$2"
  [[ "$hh" =~ ^([01]?[0-9]|2[0-3])$ ]] && [[ "$mm" =~ ^([0-5]?[0-9])$ ]]
}

# Adición de una ejecución con cron, revisa si ya existe el id y lo sobreescribe si es necesario
add_entry() {
  local hh="$1" mm="$2" id="$3"
  local log="$LOG_DIR/dispensa_${id}.log"
  local line="$mm $hh * * * /usr/bin/env PATH=$CRON_PATH \"$PYTHON\" \"$SCRIPT\" >> \"$log\" 2>&1  # tag:$id"
  # borra previo y añade el nuevo
  (crontab -l 2>/dev/null | grep -v "# tag:$id"; echo "$line") | crontab -
  echo "True; Añadido/actualizado ID=$id ($hh:$mm)"
}

# Eliminación de una ejecución del cron.
del_entry() {
  local id="$1"
  crontab -l 2>/dev/null | grep -v "# tag:$id" | crontab -
  echo "TRUE; Eliminado ID=$id"
}

# Lógica principal
cmd="${1:-}"
case "$cmd" in
  add)
    hh="${2:-}"; mm="${3:-}"; id="${4:-}"
    [[ -n "$hh" && -n "$mm" && -n "$id" ]] || { echo "False; Uso: $0 add HH MM ID"; exit 1; }
    valid_hhmm "$hh" "$mm" || { echo "False; Hora o minuto inválido"; exit 1; }
    add_entry "$hh" "$mm" "$id"
    ;;
  del)
    id="${2:-}"
    [[ -n "$id" ]] || { echo "False; Uso: $0 del ID"; exit 1; }
    del_entry "$id"
    ;;
  *)
    echo "False; Uso:"
    echo "  $0 add HH MM ID"
    echo "  $0 del ID"
    exit 1
    ;;
esac
