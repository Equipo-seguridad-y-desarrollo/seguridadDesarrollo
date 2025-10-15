# INSTRUCCIONES DE INSTALACIÓN - Entorno Virtual (venv)

## Paso 1: Crear y activar entorno virtual

### Windows PowerShell:
```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Si hay error de permisos, ejecutar primero:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Paso 2: Actualizar pip
```powershell
python -m pip install --upgrade pip
```

## Paso 3: Instalar dependencias MÍNIMAS (recomendado)
```powershell
# Instalar solo lo necesario para scripts de descarga y procesamiento
pip install -r requirements-minimal.txt
```

### O instalar dependencias completas (si tienes Python 3.11+)
```powershell
pip install -r requirements.txt
```

### O instalar manualmente una por una
```powershell
pip install pandas
pip install numpy
pip install requests
pip install python-dotenv
pip install matplotlib
pip install seaborn
pip install jupyter
pip install openpyxl
```

## Paso 4: Verificar instalación
```powershell
python -c "import pandas; import numpy; import requests; print('✓ Todas las dependencias instaladas correctamente')"
```

## Paso 5: Ejecutar scripts

### Descarga de datos:
```powershell
python notebooks/datos_seguridad_mexico.py --token 32805429-135c-9311-70c1-0b963c6f8317
```

### Procesamiento de datos:
```powershell
python notebooks/procesar_datos_seguridad.py
```

## Solución de problemas comunes

### Error: "ModuleNotFoundError: No module named 'dotenv'"
```powershell
pip install python-dotenv
```

### Error: "ModuleNotFoundError: No module named 'pandas'"
```powershell
pip install pandas
```

### Error con contourpy en Python 3.10
```powershell
# Instalar versión compatible
pip install "contourpy<1.3.0"
```

### Verificar qué Python estás usando
```powershell
python --version
which python  # En Linux/Mac
where python  # En Windows
```

## Alternativa: Usar conda

Si prefieres usar conda en lugar de venv:

```powershell
# Crear entorno conda
conda create -n seguridad python=3.11 -y

# Activar entorno
conda activate seguridad

# Instalar dependencias
conda install pandas numpy requests matplotlib seaborn jupyter openpyxl -y
pip install python-dotenv
```

## Notas importantes

- **Python recomendado**: 3.11 o superior
- **Python mínimo**: 3.8
- Si usas Python 3.10, usa `requirements-minimal.txt`
- Los scripts SOLO requieren: pandas, numpy, requests, python-dotenv
- Los notebooks requieren además: matplotlib, seaborn, jupyter
