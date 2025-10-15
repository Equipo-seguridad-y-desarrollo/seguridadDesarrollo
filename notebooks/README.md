# Notebooks - Scripts de Recopilación de Datos

Este directorio contiene scripts y notebooks para la recopilación y análisis de datos de seguridad en México.

## Script: datos_seguridad_mexico.py

Script para descargar datos de seguridad desde fuentes oficiales mexicanas.

### Datos que descarga:

1. **Indicador de percepción de inseguridad** (INEGI/ENVIPE)
   - Periodicidad: Anual
   - Cobertura: 2011-2025
   - Geografía: Nacional y por entidad federativa
   - Unidad: Personas de 18+ años por cada 100,000 que perciben inseguridad

2. **Incidencia delictiva estatal** (SESNSP)
   - Periodicidad: Mensual
   - Cobertura: Enero 2015 - Agosto 2025
   - Geografía: Por entidad federativa
   - Unidad: Hechos delictivos (conteos mensuales)

### Configuración:

1. Copiar el archivo `.env.example` de la raíz del proyecto a `.env`:
   ```bash
   cp ../.env.example ../.env
   ```

2. Obtener un token de API de INEGI:
   - Visitar: https://www.inegi.org.mx/app/api/
   - Solicitar un token de desarrollador
   - Copiar el token obtenido

3. Editar el archivo `.env` y configurar el token:
   ```
   INEGI_API_TOKEN=tu_token_aqui
   ```

### Uso:

```bash
cd notebooks
python datos_seguridad_mexico.py
```

### Archivos generados:

- `indicador_inseguridad_estados.csv`: Percepción de inseguridad por estado
- `incidencia_delictiva_estatal_2015_2025.csv`: Incidencia delictiva mensual

### Requisitos:

- Python 3.8+
- requests
- pandas
- python-dotenv

Instalar dependencias desde la raíz del proyecto:
```bash
pip install -r requirements.txt
```
