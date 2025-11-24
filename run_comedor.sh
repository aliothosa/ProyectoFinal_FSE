#!/bin/bash
cd $HOME/Projects/ProyectoFinal_FSE

# activar venv
source venvFSE/bin/activate

# ejecutar como módulo
exec python -m src.main.comedor_automatico
