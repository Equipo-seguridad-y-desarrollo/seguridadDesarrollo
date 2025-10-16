# =============================================================================
# Script de Configuracion de Entorno Virtual - Windows PowerShell
# =============================================================================
# Este script automatiza la creacion y configuracion del entorno virtual
# para el proyecto de analisis de Seguridad y Desarrollo en Mexico
#
# Uso:
#   .\setup_env.ps1
#
# =============================================================================

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "CONFIGURACION DE ENTORNO VIRTUAL - PROYECTO SEGURIDAD Y DESARROLLO" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si Python esta instalado
Write-Host "[1/6] Verificando instalacion de Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  OK Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Python no esta instalado o no esta en el PATH" -ForegroundColor Red
    Write-Host "  Por favor, instala Python desde https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Verificar version minima de Python
$pythonVersionNum = python -c "import sys; print(str(sys.version_info.major) + '.' + str(sys.version_info.minor))"
if ([version]$pythonVersionNum -lt [version]"3.8") {
    Write-Host "  ERROR: Se requiere Python 3.8 o superior (tienes $pythonVersionNum)" -ForegroundColor Red
    exit 1
}
Write-Host "  OK Version de Python compatible: $pythonVersionNum" -ForegroundColor Green
Write-Host ""

# Nombre del entorno virtual
$venvName = "venv"
$venvPath = Join-Path $PSScriptRoot $venvName

# Verificar si ya existe un entorno virtual
if (Test-Path $venvPath) {
    Write-Host "[2/6] Entorno virtual existente detectado" -ForegroundColor Yellow
    $response = Read-Host "  Deseas eliminarlo y crear uno nuevo? (s/n)"
    if ($response -eq "s" -or $response -eq "S") {
        Write-Host "  Eliminando entorno virtual anterior..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force $venvPath
        Write-Host "  OK Entorno anterior eliminado" -ForegroundColor Green
    } else {
        Write-Host "  Usando entorno virtual existente" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "[3/6] Activando entorno virtual..." -ForegroundColor Yellow
        & "$venvPath\Scripts\Activate.ps1"
        Write-Host "  OK Entorno virtual activado" -ForegroundColor Green
        Write-Host ""
        Write-Host "[4/6] Actualizando pip..." -ForegroundColor Yellow
        python -m pip install --upgrade pip --quiet
        Write-Host "  OK pip actualizado" -ForegroundColor Green
        Write-Host ""
        Write-Host "[5/6] Instalando/actualizando dependencias..." -ForegroundColor Yellow
        pip install -r requirements.txt
        Write-Host "  OK Dependencias instaladas" -ForegroundColor Green
        Write-Host ""
        Write-Host "[6/6] Verificando instalacion..." -ForegroundColor Yellow
        python -c "import pandas, requests; from dotenv import load_dotenv; print('OK')"
        Write-Host "  OK Verificacion exitosa" -ForegroundColor Green
        Write-Host ""
        Write-Host "================================================================================" -ForegroundColor Green
        Write-Host "CONFIGURACION COMPLETADA!" -ForegroundColor Green
        Write-Host "================================================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Para usar el entorno virtual:" -ForegroundColor Cyan
        Write-Host "  1. Activar: .\venv\Scripts\Activate.ps1" -ForegroundColor White
        Write-Host "  2. Ejecutar scripts: python notebooks\descarga_datos_completa.py" -ForegroundColor White
        Write-Host "  3. Desactivar: deactivate" -ForegroundColor White
        Write-Host ""
        exit 0
    }
}

# Crear nuevo entorno virtual
Write-Host "[2/6] Creando entorno virtual..." -ForegroundColor Yellow
python -m venv $venvName
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: No se pudo crear el entorno virtual" -ForegroundColor Red
    exit 1
}
Write-Host "  OK Entorno virtual creado en: $venvPath" -ForegroundColor Green
Write-Host ""

# Activar entorno virtual
Write-Host "[3/6] Activando entorno virtual..." -ForegroundColor Yellow
& "$venvPath\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: No se pudo activar el entorno virtual" -ForegroundColor Red
    Write-Host "  Intenta ejecutar: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
    exit 1
}
Write-Host "  OK Entorno virtual activado" -ForegroundColor Green
Write-Host ""

# Actualizar pip
Write-Host "[4/6] Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "  OK pip actualizado" -ForegroundColor Green
Write-Host ""

# Instalar dependencias
Write-Host "[5/6] Instalando dependencias..." -ForegroundColor Yellow
Write-Host "  Instalando paquetes esenciales (pandas, numpy, requests, python-dotenv)..." -ForegroundColor Cyan
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: Fallo al instalar dependencias" -ForegroundColor Red
    exit 1
}
Write-Host "  OK Dependencias instaladas correctamente" -ForegroundColor Green
Write-Host ""

# Verificar instalacion
Write-Host "[6/6] Verificando instalacion..." -ForegroundColor Yellow
python -c "import pandas, requests; from dotenv import load_dotenv; print('OK')"
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ERROR: Problema al importar librerias" -ForegroundColor Red
    exit 1
}
Write-Host "  OK Verificacion exitosa" -ForegroundColor Green

# Verificar archivo .env
Write-Host ""
Write-Host "Verificando configuracion del token INEGI..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  OK Archivo .env encontrado" -ForegroundColor Green
    $envContent = Get-Content .env -Raw
    if ($envContent -match "INEGI_API_TOKEN") {
        Write-Host "  OK Token INEGI configurado" -ForegroundColor Green
    } else {
        Write-Host "  ADVERTENCIA: Token INEGI no encontrado en .env" -ForegroundColor Yellow
        Write-Host "    Agrega tu token: INEGI_API_TOKEN=tu_token_aqui" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ADVERTENCIA: Archivo .env no existe" -ForegroundColor Yellow
    Write-Host "    Crea un archivo .env con tu token de INEGI:" -ForegroundColor Yellow
    Write-Host "    INEGI_API_TOKEN=tu_token_aqui" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Green
Write-Host "CONFIGURACION COMPLETADA EXITOSAMENTE!" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "PROXIMOS PASOS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. El entorno virtual esta ACTIVADO en esta sesion" -ForegroundColor White
Write-Host ""
Write-Host "2. Para futuras sesiones, activa el entorno con:" -ForegroundColor White
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Ejecuta el script de descarga:" -ForegroundColor White
Write-Host "   python notebooks\descarga_datos_completa.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Para desactivar el entorno:" -ForegroundColor White
Write-Host "   deactivate" -ForegroundColor Yellow
Write-Host ""
Write-Host "5. Si no tienes token de INEGI, obten uno en:" -ForegroundColor White
Write-Host "   https://www.inegi.org.mx/app/api/" -ForegroundColor Cyan
Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
