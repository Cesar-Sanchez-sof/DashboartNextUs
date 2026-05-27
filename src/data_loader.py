import os
import pandas as pd

# Mapeo de claves internas del dataframe a preguntas legibles y limpias en español
PREGUNTAS_MAP = {
    "timestamp": "Marca temporal",
    "email": "Dirección de correo electrónico",
    
    "Q1_frecuencia_falta": (
        "Durante el ciclo académico, ¿con qué frecuencia te falta un artículo cotidiano "
        "(ej. calculadora, libro, adaptador) que necesitas urgente pero no tienes presupuesto para comprar?"
    ),
    
    "Q2_articulos_falta": "¿Qué tipo de artículos te suelen hacer falta por solo un par de días?",
    
    "Q3_solucion_actual": "Actualmente, cuando te falta algo temporalmente, ¿cómo sueles solucionarlo?",
    
    "Q4_filtros_busqueda": (
        "Si usaras una plataforma para alquilar estos artículos a bajo costo, "
        "¿qué filtros de búsqueda serían los más importantes para ti? (Elige máximo 2)"
    ),
    
    "Q5_articulos_disponibles": "¿Tienes artículos de estudio en buen estado que usas muy poco y que podrían servirle a otro estudiante?",
    
    "Q6_barrera_compartir": "Si pudieras ganar dinero extra alquilando esas cosas en el campus, ¿cuál sería tu mayor barrera para hacerlo?",
    
    "Q7_descuento_semanal": (
        "Al publicar un artículo, ¿qué tan útil sería poder configurar descuentos automáticos "
        "si alguien te lo alquila por toda una semana en lugar de un solo día?"
    ),
    
    "Q8_boton_pausar": (
        "Si te vas de vacaciones o tienes exámenes, ¿te gustaría tener un botón para "
        "\"Pausar\" temporalmente tus anuncios sin tener que borrarlos?"
    ),
    
    "Q9_estadisticas_vistas": "Como dueño del artículo, ¿te interesaría ver estadísticas de cuántas personas han visto tu anuncio?",
    
    "Q10_registro_institucional": (
        "Para garantizar la seguridad de todos, la plataforma exigirá registrarse obligatoriamente "
        "con el correo institucional (@upao.edu.pe) y código de alumno. ¿Qué opinas de esto?"
    ),
    
    "Q11_deposito_garantia": (
        "Imagina que vas a alquilar un libro por S/ 3 al día. Para proteger al dueño, se te pide pagar un "
        "\"depósito de garantía\" que se te reembolsará en máximo 48 horas al devolverlo. ¿Aceptarías esta condición?"
    ),
    
    "Q12_metodo_retiro": "Como propietario que alquila sus cosas, ¿qué método preferirías para retirar tus ganancias de la plataforma?",
    
    "Q13_comision_seguro": (
        "Para que la plataforma cubra el seguro contra daños y mantenga los servidores, retendría una comisión (ej. 30%) "
        "sobre el costo del alquiler. Sabiendo esto, ¿te animarías a publicar tus artículos?"
    ),
    
    "Q14_herramienta_coordinacion": "Para coordinar el punto exacto de encuentro en la universidad, ¿qué herramienta prefieres usar?",
    
    "Q15_metodo_confirmacion": (
        "Al momento de entregar físicamente el artículo, ¿qué método te parece más seguro "
        "para confirmar en el sistema que el periodo de alquiler ha comenzado?"
    ),
    
    "Q16_cancelacion_reserva": "Si tuvieras un inconveniente de último minuto, ¿consideras importante poder cancelar una reserva ya aceptada con 24 horas de anticipación?",
    
    "Q17_extension_plazo": "Si alquilaste un artículo por 2 días pero tu proyecto se extendió, ¿qué harías?",
    
    "Q18_resolucion_disputas": (
        "Si al devolver el artículo el dueño afirma (injustamente) que le hiciste un daño "
        "y no quiere liberar tu garantía, ¿qué esperarías del sistema?"
    ),
    
    "Q19_importancia_resenas": "¿Qué tan importante es para ti poder ver y dejar reseñas (de 1 a 5 estrellas) sobre el comportamiento de otros estudiantes?",
    
    "Q20_penalidad_retraso": "Si una persona se retrasa en devolver un artículo, ¿qué penalidad crees que sería la más justa?"
}

def clean_spanish_text(text):
    """
    Corrige los errores de codificación comunes derivados de la exportación del Excel.
    """
    if not isinstance(text, str):
        return text
    
    replacements = {
        'con qu': '¿con qué',
        'Qu': '¿Qué',
        'Cmo': '¿Cómo',
        'Tienes': '¿Tienes',
        'Cul': '¿Cuál',
        'te gustara': '¿te gustaría',
        'te interesara': '¿te interesaría',
        'Aceptaras': '¿Aceptarías',
        'Te animaras': '¿Te animarías',
        'Consideras': '¿Consideras',
        '': ''
    }
    
    for bad, good in replacements.items():
        text = text.replace(bad, good)
        
    corrupt_words = {
        'acadmico': 'académico',
        'con qu': 'con qué',
        'artculo': 'artículo',
        'artculos': 'artículos',
        'das': 'días',
        'daen': 'dañen',
        'dao': 'daño',
        'Cmo': 'Cómo',
        'bsqueda': 'búsqueda',
        'seran': 'serían',
        'ms': 'más',
        'dueo': 'dueño',
        'dueos': 'dueños',
        'calificacin': 'calificación',
        'podran': 'podrían',
        'til': 'útil',
        'asegurara': 'aseguraría',
        'exmenes': 'exámenes',
        'gustara': 'gustaría',
        'botn': 'botón',
        'interesara': 'interesaría',
        'estadsticas': 'estadísticas',
        'cntas': 'cuántas',
        'exigir': 'exigirá',
        'cdigo': 'código',
        'cdigo': 'código',
        'daos': 'daños',
        'daos': 'daños',
        'retendra': 'retendría',
        'retenda': 'retendría',
        'comisin': 'comisión',
        'comision': 'comisión',
        'fsicamente': 'físicamente',
        'fsicamente': 'físicamente',
        'ltimo': 'último',
        'ltimo': 'último',
        'anticipacin': 'anticipación',
        'anticipacin': 'anticipación',
        'extendi': 'extendió',
        'extendi': 'extendió',
        'haras': 'harías',
        'haras': 'harías',
        'esperaras': 'esperarías',
        'esperaras': 'esperarías',
        'reseas': 'reseñas',
        'reseas': 'reseñas',
        'sera': 'sería',
        'seria': 'sería',
        'depsito': 'depósito',
        'depsito': 'depósito',
        'garanta': 'garantía',
        'garanta': 'garantía',
        'reembolsar': 'reembolsará',
        'reembolsar': 'reembolsará',
        'mximo': 'máximo',
        'mximo': 'máximo',
        'preferiras': 'preferirías',
        'preferiras': 'preferirías',
    }
    
    for bad, good in corrupt_words.items():
        text = text.replace(bad, good)
        
    return text.strip()

def load_and_preprocess_data(excel_path):
    """
    Carga el Excel de la encuesta, renombra y limpia las columnas y las celdas de texto.
    """
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"No se pudo encontrar el archivo Excel en {excel_path}")
        
    df = pd.read_excel(excel_path)
    
    # Mapeo posicional para evitar problemas con la codificación de las cabeceras originales
    expected_cols = [
        "timestamp", 
        "email", 
        "Q1_frecuencia_falta", 
        "Q2_articulos_falta", 
        "Q3_solucion_actual",
        "Q4_filtros_busqueda", 
        "Q5_articulos_disponibles", 
        "Q6_barrera_compartir", 
        "Q7_descuento_semanal", 
        "Q8_boton_pausar", 
        "Q9_estadisticas_vistas", 
        "Q10_registro_institucional", 
        "Q11_deposito_garantia", 
        "Q12_metodo_retiro", 
        "Q13_comision_seguro", 
        "Q14_herramienta_coordinacion", 
        "Q15_metodo_confirmacion", 
        "Q16_cancelacion_reserva", 
        "Q17_extension_plazo", 
        "Q18_resolucion_disputas", 
        "Q19_importancia_resenas", 
        "Q20_penalidad_retraso"
    ]
    
    # Renombrar columnas posicionalmente
    current_cols = list(df.columns)
    rename_dict = {}
    for i, new_col in enumerate(expected_cols):
        if i < len(current_cols):
            rename_dict[current_cols[i]] = new_col
            
    df = df.rename(columns=rename_dict)
    
    # Limpiar y corregir texto en cada celda del DataFrame
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(clean_spanish_text)
        
    # Limpieza particular para Q19 (que puede venir como número o string)
    df["Q19_importancia_resenas"] = pd.to_numeric(df["Q19_importancia_resenas"], errors='coerce').fillna(3).astype(int)
    
    # Clasificación por dominio de correo electrónico para análisis de perfil
    df["Tipo_Correo"] = df["email"].apply(lambda x: "Institucional UPAO" if "@upao.edu.pe" in str(x).lower() else "Personal / Otro")
    
    return df

def parse_multiselect_column(df, column_name):
    """
    Parsea las columnas de respuesta múltiple (casillas de verificación en Google Forms)
    que vienen como texto separado por comas, y retorna una serie con los conteos individuales.
    """
    if column_name not in df.columns:
        return pd.Series(dtype=int)
        
    all_options = []
    for val in df[column_name].dropna():
        # Separar por coma
        parts = [p.strip() for p in val.split(',')]
        # Filtrar vacíos
        parts = [clean_spanish_text(p) for p in parts if p.strip()]
        all_options.extend(parts)
        
    return pd.Series(all_options).value_counts()
