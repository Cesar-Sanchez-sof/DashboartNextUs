import os

# ---------------------------------------------
# CONFIGURACIÓN DE RUTAS DE DATOS Y ENTRADAS
# ---------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

EXCEL_FILENAME = "Estudio de Necesidades_ Intercambio de Materiales Académicos en el Campus UPAO (Respuestas).xlsx"
EXCEL_PATH = os.path.join(DATA_RAW_DIR, EXCEL_FILENAME)
TXT_QUESTIONNAIRE_PATH = os.path.join(DATA_RAW_DIR, "Encuesta.txt")

HTML_OUTPUT_PATH = os.path.join(REPORTS_DIR, "Reporte_Interactivo_UPAO.html")

# ---------------------------------------------
# PALETAS DE COLORES CORPORATIVOS Y ESTILOS
# ---------------------------------------------
# Una gama premium moderna inspirada en UPAO (azul institucional, celeste brillante, acentos dorados y esmeralda)
PALETA_COLORES = [
    "#00C2FF",  # Celeste Eléctrico
    "#2ECC71",  # Verde Esmeralda (Éxito / Aprobación)
    "#F39C12",  # Amarillo Oro (Aviso / Advertencia)
    "#E74C3C",  # Rojo Coral (Riesgo / Desaprobación)
    "#9B59B6",  # Violeta Amatista (Alternativas)
    "#34495E"   # Gris Pizarra Oscuro (Bases y secundarios)
]

THEME_LAYOUT = dict(
    paper_bgcolor='rgba(30, 41, 59, 0.45)',  # Fondo de tarjeta glassmorphism
    plot_bgcolor='rgba(0, 0, 0, 0)',         # Transparente
    font=dict(color='#ffffff', family='Outfit, sans-serif'),
    margin=dict(t=50, b=40, l=40, r=40)
)
