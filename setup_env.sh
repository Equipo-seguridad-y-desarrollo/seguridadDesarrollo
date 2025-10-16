#!/bin/bash
# =============================================================================
# Script de Configuración de Entorno Virtual - Linux/macOS
# =============================================================================
# Este script automatiza la creación y configuración del entorno virtual
# para el proyecto de análisis de Seguridad y Desarrollo en México
#
# Uso:
#   chmod +x setup_env.sh
#   ./setup_env.sh
#
# =============================================================================

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}================================================================================${NC}"
echo -e "${CYAN}CONFIGURACIÓN DE ENTORNO VIRTUAL - PROYECTO SEGURIDAD Y DESARROLLO${NC}"
echo -e "${CYAN}================================================================================${NC}"
echo ""

# Verificar si Python está instalado
echo -e "${YELLOW}[1/6] Verificando instalación de Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}  ✗ ERROR: Python3 no está instalado${NC}"
    echo -e "${RED}  Por favor, instala Python3 primero${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
echo -e "${GREEN}  ✓ Python encontrado: $PYTHON_VERSION${NC}"

# Verificar versión mínima de Python
PYTHON_VERSION_NUM=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION_NUM" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}  ✗ ERROR: Se requiere Python 3.8 o superior (tienes $PYTHON_VERSION_NUM)${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ Versión de Python compatible: $PYTHON_VERSION_NUM${NC}"
echo ""

# Nombre del entorno virtual
VENV_NAME="venv"

# Verificar si ya existe un entorno virtual
if [ -d "$VENV_NAME" ]; then
    echo -e "${YELLOW}[2/6] Entorno virtual existente detectado${NC}"
    read -p "  ¿Deseas eliminarlo y crear uno nuevo? (s/n): " response
    if [ "$response" = "s" ] || [ "$response" = "S" ]; then
        echo -e "${YELLOW}  Eliminando entorno virtual anterior...${NC}"
        rm -rf $VENV_NAME
        echo -e "${GREEN}  ✓ Entorno anterior eliminado${NC}"
    else
        echo -e "${CYAN}  Usando entorno virtual existente${NC}"
        echo ""
        echo -e "${YELLOW}[3/6] Activando entorno virtual...${NC}"
        source $VENV_NAME/bin/activate
        echo -e "${GREEN}  ✓ Entorno virtual activado${NC}"
        echo ""
        echo -e "${YELLOW}[4/6] Actualizando pip...${NC}"
        python -m pip install --upgrade pip --quiet
        echo -e "${GREEN}  ✓ pip actualizado${NC}"
        echo ""
        echo -e "${YELLOW}[5/6] Instalando/actualizando dependencias...${NC}"
        pip install -r requirements.txt
        echo -e "${GREEN}  ✓ Dependencias instaladas${NC}"
        echo ""
        echo -e "${YELLOW}[6/6] Verificando instalación...${NC}"
        python -c "import pandas, requests; from dotenv import load_dotenv; print('  ✓ Todas las librerías principales importadas correctamente')"
        echo ""
        echo -e "${GREEN}================================================================================${NC}"
        echo -e "${GREEN}¡CONFIGURACIÓN COMPLETADA!${NC}"
        echo -e "${GREEN}================================================================================${NC}"
        echo ""
        echo -e "${CYAN}Para usar el entorno virtual:${NC}"
        echo -e "  1. Activar: source venv/bin/activate"
        echo -e "  2. Ejecutar scripts: python notebooks/descarga_datos_completa.py"
        echo -e "  3. Desactivar: deactivate"
        echo ""
        exit 0
    fi
fi

# Crear nuevo entorno virtual
echo -e "${YELLOW}[2/6] Creando entorno virtual...${NC}"
python3 -m venv $VENV_NAME
if [ $? -ne 0 ]; then
    echo -e "${RED}  ✗ ERROR: No se pudo crear el entorno virtual${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ Entorno virtual creado en: ./$VENV_NAME${NC}"
echo ""

# Activar entorno virtual
echo -e "${YELLOW}[3/6] Activando entorno virtual...${NC}"
source $VENV_NAME/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}  ✗ ERROR: No se pudo activar el entorno virtual${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ Entorno virtual activado${NC}"
echo ""

# Actualizar pip
echo -e "${YELLOW}[4/6] Actualizando pip...${NC}"
python -m pip install --upgrade pip --quiet
echo -e "${GREEN}  ✓ pip actualizado${NC}"
echo ""

# Instalar dependencias
echo -e "${YELLOW}[5/6] Instalando dependencias...${NC}"
echo -e "${CYAN}  Instalando paquetes esenciales (pandas, numpy, requests, python-dotenv)...${NC}"
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}  ✗ ERROR: Fallo al instalar dependencias${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ Dependencias instaladas correctamente${NC}"
echo ""

# Verificar instalación
echo -e "${YELLOW}[6/6] Verificando instalación...${NC}"
python -c "import pandas, requests; from dotenv import load_dotenv; print('  ✓ Todas las librerías principales importadas correctamente')"
if [ $? -ne 0 ]; then
    echo -e "${RED}  ✗ ERROR: Problema al importar librerías${NC}"
    exit 1
fi

# Verificar archivo .env
echo ""
echo -e "${YELLOW}Verificando configuración del token INEGI...${NC}"
if [ -f ".env" ]; then
    echo -e "${GREEN}  ✓ Archivo .env encontrado${NC}"
    if grep -q "INEGI_API_TOKEN" .env; then
        echo -e "${GREEN}  ✓ Token INEGI configurado${NC}"
    else
        echo -e "${YELLOW}  ⚠ ADVERTENCIA: Token INEGI no encontrado en .env${NC}"
        echo -e "${YELLOW}    Agrega tu token: INEGI_API_TOKEN=tu_token_aqui${NC}"
    fi
else
    echo -e "${YELLOW}  ⚠ ADVERTENCIA: Archivo .env no existe${NC}"
    echo -e "${YELLOW}    Crea un archivo .env con tu token de INEGI:${NC}"
    echo -e "${YELLOW}    INEGI_API_TOKEN=tu_token_aqui${NC}"
fi

echo ""
echo -e "${GREEN}================================================================================${NC}"
echo -e "${GREEN}¡CONFIGURACIÓN COMPLETADA EXITOSAMENTE!${NC}"
echo -e "${GREEN}================================================================================${NC}"
echo ""
echo -e "${CYAN}PRÓXIMOS PASOS:${NC}"
echo ""
echo -e "1. El entorno virtual está ACTIVADO en esta sesión"
echo ""
echo -e "2. Para futuras sesiones, activa el entorno con:"
echo -e "${YELLOW}   source venv/bin/activate${NC}"
echo ""
echo -e "3. Ejecuta el script de descarga:"
echo -e "${YELLOW}   python notebooks/descarga_datos_completa.py${NC}"
echo ""
echo -e "4. Para desactivar el entorno:"
echo -e "${YELLOW}   deactivate${NC}"
echo ""
echo -e "5. Si no tienes token de INEGI, obtén uno en:"
echo -e "${CYAN}   https://www.inegi.org.mx/app/api/${NC}"
echo ""
echo -e "${CYAN}================================================================================${NC}"
