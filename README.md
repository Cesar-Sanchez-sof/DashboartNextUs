# 🎓 UPAO Link - Analizador de Encuestas Académicas y Dashboard Premium

¡Bienvenido al sistema oficial de analítica e inteligencia de necesidades para **UPAO Link**! 

Este proyecto ha sido estructurado e implementado siguiendo estrictos estándares internacionales de **ingeniería de software y buenas prácticas** (limpieza de código, desacoplamiento de componentes, modularización e interfaces de alta fidelidad estética) para analizar el estudio de mercado sobre el intercambio y alquiler seguro de herramientas de estudio en el campus de la **Universidad Privada Antenor Orrego (UPAO)**.

---

## 🏗️ Arquitectura de Software del Proyecto

El proyecto está diseñado bajo un modelo estructurado por carpetas que aísla de manera clara los datos crudos, la configuración global, el código fuente ejecutable y los reportes finales resultantes:

```
C:\Users\Cesar Sanchez\Documents\ETL\
│
├── config/                  # Archivos de configuración técnica global
│   └── settings.py          # Definición de rutas, colores corporativos UPAO y temas
│
├── data/                    # Repositorio de persistencia estructurada
│   ├── raw/                 # Archivos originales intactos de la encuesta
│   │   ├── Encuesta.txt     # Preguntas base de la encuesta
│   │   └── Estudio de Necesidades_...xlsx  # Set de respuestas en Excel
│   └── processed/           # Datos procesados/limpios listos para modelos
│
├── src/                     # Código Fuente Modular (Paquete Core de la App)
│   ├── __init__.py          # Inicializador del paquete Python
│   ├── data_loader.py       # Pipeline ETL (Extracción, Limpieza y Transformación)
│   ├── charts.py            # Generador desacoplado de visualizaciones interactivas
│   └── app.py               # Frontend interactivo de Streamlit
│
├── reports/                 # Entregables y reportes ejecutivos finales
│   └── Reporte_Interactivo_UPAO.html # Reporte autónomo rediseñado con Glassmorphism
│
├── README.md                # Documentación oficial y guía técnica (Este archivo)
├── requirements.txt         # Declaración estricta de librerías necesarias
├── main.py                  # Orquestador del pipeline completo y compilador de HTML
└── run_dashboard.bat        # Lanzador automático de doble clic para Windows
```

---

## ⚙️ Pipeline ETL e Inteligencia de Datos (`src/data_loader.py`)

Uno de los mayores dolores al procesar respuestas de formularios es la codificación y la inconsistencia en las columnas de selección múltiple. Nuestro pipeline automatiza estos procesos:

1. **Corrección de Codificación (Accents & Characters)**:
   Google Forms y Excel suelen exportar caracteres en español (tildes, *ñ*, signos de interrogación) en formatos corruptos (como `` en lugar de letras con acento). El cargador implementa una función de desinfección sistemática de texto basada en un diccionario determinista de traducción para restaurar la perfecta legibilidad en español.
2. **Robustez Posicional**:
   En lugar de buscar columnas por nombres textuales de preguntas (los cuales pueden cambiar ligeramente si se edita el formulario), el ETL las mapea de manera posicional (índices 0 a 21) asociando claves internas limpias (ej. `Q1_frecuencia_falta`, `Q2_articulos_falta`).
3. **Mapeo de Preguntas Base**:
   Vincula cada clave interna con su pregunta oficial descrita en `Encuesta.txt` para mantener títulos e interpretaciones de gráficos 100% correctos.
4. **Atomic Checkbox Unpacker**:
   Las preguntas de casillas de verificación múltiple (donde el alumno puede marcar más de una opción) se exportan al Excel separadas por comas. El ETL desglosa, limpia espacios, desinfecta el texto y cuenta individualmente cada selección sin duplicar o alterar las filas del conjunto de datos base.

---

## 🎨 Rediseño Visual Premium del Reporte HTML (`reports/`)

Hemos rediseñado el entregable **`Reporte_Interactivo_UPAO.html`** para brindar una experiencia de usuario increíble y ejecutiva:
- **Tema Glassmorphism**: Fondo en azul oscuro espacial profundo (`#0b0f19`) con tarjetas semi-transparentes con bordes brillantes sutiles y efectos de resplandor.
- **Sistema de Pestañas CSS Puro (Zero JS)**: Un sistema de navegación interactivo con tabs que funciona al instante en cualquier navegador web, sin requerir internet, ni dependencias de Javascript complejas, emulando una aplicación moderna.
- **Gráficos Plotly Interactivos**: Cada gráfico permite hacer zoom, pasar el cursor para ver descripciones exactas y descargar como imagen vectorial en alta definición.

---

## 🚀 Guía de Instalación y Ejecución

### Opción 1: Ejecución en Un Solo Clic (Recomendado para Windows)
1. Navega hasta la carpeta raíz del proyecto `C:\Users\Cesar Sanchez\Documents\ETL\`.
2. Haz doble clic en el archivo **`run_dashboard.bat`**.
3. El script de automatización validará tu entorno, instalará dependencias que falten de forma automática, generará el reporte HTML interactivo y desplegará el dashboard dinámico de Streamlit en tu navegador.

### Opción 2: Ejecución Manual en Terminal (PowerShell / CMD)
```bash
# 1. Navegar al directorio del proyecto (No utilizar cd si usas herramientas agenticas)
# 2. Instalar dependencias requeridas
pip install -r requirements.txt

# 3. Ejecutar el orquestador principal
python main.py
```

---

## 🛠️ Buenas Prácticas de Ingeniería Aplicadas
- **Desacoplamiento Estricto (Separation of Concerns)**: La lógica ETL (`data_loader.py`), la lógica de gráficos Plotly (`charts.py`), y la interfaz de usuario (`app.py` y `main.py`) están 100% separadas. Si decides cambiar la interfaz a Dash o Django, puedes reutilizar el ETL y los gráficos sin cambiar una sola línea de código.
- **Protección contra caídas en terminales Windows**: Todos los comandos de impresión en terminal usan caracteres planos seguros (`[INFO]`, `[OK]`, `[WARN]`) para prevenir bloqueos por codificación de emojis (`UnicodeEncodeError`) en la consola estándar de Windows.
- **Portabilidad Absoluta**: El sistema calcula rutas relativas utilizando el directorio de ejecución, asegurando que si mueves la carpeta completa a otro disco u ordenador, seguirá funcionando a la perfección.
