import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from config.settings import PALETA_COLORES, THEME_LAYOUT
from src.data_loader import parse_multiselect_column

# Helper para aplicar estilos comunes a todos los gráficos de forma consistente
def _apply_standard_styling(fig, show_legend=False):
    fig.update_layout(**THEME_LAYOUT)
    if not show_legend:
        fig.update_layout(showlegend=False)
    return fig

# ---------------------------------------------
# GRÁFICOS DE LA SECCIÓN: DEMANDA DE MATERIALES
# ---------------------------------------------
def create_q1_frequency_chart(df):
    p1_counts = df["Q1_frecuencia_falta"].value_counts().reset_index()
    p1_counts.columns = ["Frecuencia", "Estudiantes"]
    fig = px.bar(
        p1_counts,
        y="Frecuencia",
        x="Estudiantes",
        orientation='h',
        title="¿Con qué frecuencia te falta un artículo cotidiano?",
        color="Frecuencia",
        color_discrete_sequence=PALETA_COLORES
    )
    return _apply_standard_styling(fig)

def create_q2_needed_articles_chart(df):
    q2_parsed = parse_multiselect_column(df, "Q2_articulos_falta").reset_index()
    q2_parsed.columns = ["Tipo de Artículo", "Menciones"]
    fig = px.bar(
        q2_parsed,
        x="Menciones",
        y="Tipo de Artículo",
        orientation='h',
        title="Artículos más necesitados (Respuestas Múltiples)",
        color="Tipo de Artículo",
        color_discrete_sequence=PALETA_COLORES
    )
    return _apply_standard_styling(fig)

def create_q3_current_solutions_chart(df):
    p3_counts = df["Q3_solucion_actual"].value_counts().reset_index()
    p3_counts.columns = ["Solución", "Estudiantes"]
    fig = px.pie(
        p3_counts,
        names="Solución",
        values="Estudiantes",
        title="¿Cómo suelen solucionar la falta de artículos hoy en día?",
        color_discrete_sequence=PALETA_COLORES
    )
    return _apply_standard_styling(fig, show_legend=True)

def create_q4_priority_filters_chart(df):
    q4_parsed = parse_multiselect_column(df, "Q4_filtros_busqueda").reset_index()
    q4_parsed.columns = ["Filtro de Búsqueda", "Menciones"]
    fig = px.bar(
        q4_parsed,
        x="Menciones",
        y="Filtro de Búsqueda",
        orientation='h',
        title="Filtros de búsqueda prioritarios (Elegir máx 2)",
        color="Filtro de Búsqueda",
        color_discrete_sequence=PALETA_COLORES
    )
    return _apply_standard_styling(fig)

# ---------------------------------------------
# GRÁFICOS DE LA SECCIÓN: OFERTA Y MONETIZACIÓN
# ---------------------------------------------
def create_q5_own_articles_chart(df):
    q5_counts = df["Q5_articulos_disponibles"].value_counts().reset_index()
    q5_counts.columns = ["Disponibilidad", "Estudiantes"]
    fig = px.pie(
        q5_counts,
        names="Disponibilidad",
        values="Estudiantes",
        title="¿Tienen artículos en buen estado útiles para compartir?",
        color_discrete_sequence=PALETA_COLORES
    )
    return _apply_standard_styling(fig, show_legend=True)

def create_q6_renting_barriers_chart(df):
    q6_counts = df["Q6_barrera_compartir"].value_counts().reset_index()
    q6_counts.columns = ["Barrera Mayor", "Estudiantes"]
    fig = px.bar(
        q6_counts,
        x="Estudiantes",
        y="Barrera Mayor",
        orientation='h',
        title="Mayor temor / barrera para alquilar artículos",
        color="Barrera Mayor",
        color_discrete_sequence=PALETA_COLORES
    )
    return _apply_standard_styling(fig)

def create_q7_weekly_discounts_chart(df):
    q7_counts = df["Q7_descuento_semanal"].value_counts().reset_index()
    q7_counts.columns = ["Utilidad Descuento", "Estudiantes"]
    fig = px.bar(
        q7_counts,
        x="Utilidad Descuento",
        y="Estudiantes",
        title="Utilidad percibida de descuentos semanales",
        color="Utilidad Descuento",
        color_discrete_sequence=[PALETA_COLORES[1], PALETA_COLORES[3]]
    )
    return _apply_standard_styling(fig)

def create_q8_pausing_button_chart(df):
    q8_counts = df["Q8_boton_pausar"].value_counts().reset_index()
    q8_counts.columns = ["Interés Botón", "Estudiantes"]
    fig = px.bar(
        q8_counts,
        x="Interés Botón",
        y="Estudiantes",
        title="Relevancia de botón de 'Pausar Anuncios'",
        color="Interés Botón",
        color_discrete_sequence=[PALETA_COLORES[2], PALETA_COLORES[5]]
    )
    return _apply_standard_styling(fig)

def create_q9_views_stats_chart(df):
    q9_counts = df["Q9_estadisticas_vistas"].value_counts().reset_index()
    q9_counts.columns = ["Interés Estadísticas", "Estudiantes"]
    fig = px.pie(
        q9_counts,
        names="Interés Estadísticas",
        values="Estudiantes",
        title="Interés del propietario por estadísticas de vistas",
        color_discrete_sequence=[PALETA_COLORES[0], PALETA_COLORES[5]]
    )
    return _apply_standard_styling(fig, show_legend=True)

# ---------------------------------------------
# GRÁFICOS DE LA SECCIÓN: SEGURIDAD Y FINANZAS
# ---------------------------------------------
def create_q10_registration_trust_chart(df):
    q10_counts = df["Q10_registro_institucional"].value_counts().reset_index()
    q10_counts.columns = ["Opinión Registro", "Estudiantes"]
    fig = px.bar(
        q10_counts,
        x="Estudiantes",
        y="Opinión Registro",
        orientation='h',
        title="Opinión sobre validación obligatoria con correo @upao.edu.pe",
        color="Opinión Registro",
        color_discrete_sequence=PALETA_COLORES
    )
    return _apply_standard_styling(fig)

def create_q11_deposit_acceptance_chart(df):
    q11_counts = df["Q11_deposito_garantia"].value_counts().reset_index()
    q11_counts.columns = ["Aceptación", "Estudiantes"]
    fig = px.pie(
        q11_counts,
        names="Aceptación",
        values="Estudiantes",
        title="¿Aceptarías pagar un depósito de garantía temporal?",
        color_discrete_sequence=PALETA_COLORES
    )
    return _apply_standard_styling(fig, show_legend=True)

def create_q12_payout_methods_chart(df):
    q12_parsed = parse_multiselect_column(df, "Q12_metodo_retiro").reset_index()
    q12_parsed.columns = ["Método", "Menciones"]
    fig = px.bar(
        q12_parsed,
        x="Menciones",
        y="Método",
        orientation='h',
        title="Método favorito para retirar ganancias acumuladas",
        color="Método",
        color_discrete_sequence=PALETA_COLORES
    )
    return _apply_standard_styling(fig)

def create_q13_commission_acceptance_chart(df):
    q13_counts = df["Q13_comision_seguro"].value_counts().reset_index()
    q13_counts.columns = ["Aceptación Comisión", "Estudiantes"]
    fig = px.bar(
        q13_counts,
        x="Aceptación Comisión",
        y="Estudiantes",
        title="¿Te animarías a publicar sabiendo que hay una comisión del 30%?",
        color="Aceptación Comisión",
        color_discrete_sequence=PALETA_COLORES
    )
    return _apply_standard_styling(fig)

# ---------------------------------------------
# GRÁFICOS DE LA SECCIÓN: REGLAS Y OPERACIONES
# ---------------------------------------------
def create_q14_meetup_channel_chart(df):
    q14_counts = df["Q14_herramienta_coordinacion"].value_counts().reset_index()
    q14_counts.columns = ["Herramienta", "Estudiantes"]
    fig = px.pie(
        q14_counts,
        names="Herramienta",
        values="Estudiantes",
        title="Canal favorito para coordinar la entrega física en campus",
        color_discrete_sequence=PALETA_COLORES
    )
    return _apply_standard_styling(fig, show_legend=True)

def create_q15_delivery_verification_chart(df):
    q15_counts = df["Q15_metodo_confirmacion"].value_counts().reset_index()
    q15_counts.columns = ["Método", "Estudiantes"]
    fig = px.bar(
        q15_counts,
        x="Estudiantes",
        y="Método",
        orientation='h',
        title="Método de confirmación digital al entregar el artículo",
        color="Método",
        color_discrete_sequence=PALETA_COLORES
    )
    return _apply_standard_styling(fig)

def create_q16_cancelation_importance_chart(df):
    q16_counts = df["Q16_cancelacion_reserva"].value_counts().reset_index()
    q16_counts.columns = ["Importancia", "Estudiantes"]
    fig = px.pie(
        q16_counts,
        names="Importancia",
        values="Estudiantes",
        title="¿Es importante poder cancelar reservas hasta 24h antes?",
        color_discrete_sequence=[PALETA_COLORES[1], PALETA_COLORES[3]]
    )
    return _apply_standard_styling(fig, show_legend=True)

def create_q17_extension_preference_chart(df):
    q17_counts = df["Q17_extension_plazo"].value_counts().reset_index()
    q17_counts.columns = ["Acción", "Estudiantes"]
    fig = px.bar(
        q17_counts,
        x="Estudiantes",
        y="Acción",
        orientation='h',
        title="Acción favorita si necesitas extender el alquiler",
        color="Acción",
        color_discrete_sequence=PALETA_COLORES
    )
    return _apply_standard_styling(fig)

def create_q18_dispute_resolution_chart(df):
    q18_counts = df["Q18_resolucion_disputas"].value_counts().reset_index()
    q18_counts.columns = ["Expectativa del Sistema", "Estudiantes"]
    fig = px.bar(
        q18_counts,
        x="Estudiantes",
        y="Expectativa del Sistema",
        orientation='h',
        title="¿Cómo esperarías que el sistema resuelva disputas injustas de daños?",
        color="Expectativa del Sistema",
        color_discrete_sequence=PALETA_COLORES
    )
    return _apply_standard_styling(fig)

def create_q19_reviews_importance_chart(df):
    q19_counts = df["Q19_importancia_resenas"].value_counts().sort_index().reset_index()
    q19_counts.columns = ["Importancia (1-5)", "Estudiantes"]
    fig = px.bar(
        q19_counts,
        x="Importancia (1-5)",
        y="Estudiantes",
        title="Importancia percibida de calificaciones y reseñas de estrellas",
        labels={"Importancia (1-5)": "Nivel de Importancia (1: Mínimo, 5: Máximo)"},
        color_discrete_sequence=[PALETA_COLORES[4]]
    )
    fig.update_xaxes(tickvals=[1, 2, 3, 4, 5])
    return _apply_standard_styling(fig)

def create_q20_delay_penalties_chart(df):
    q20_counts = df["Q20_penalidad_retraso"].value_counts().reset_index()
    q20_counts.columns = ["Penalidad", "Estudiantes"]
    fig = px.bar(
        q20_counts,
        y="Penalidad",
        x="Estudiantes",
        orientation='h',
        title="Penalidad considerada más justa por retraso en la entrega",
        color="Penalidad",
        color_discrete_sequence=PALETA_COLORES
    )
    return _apply_standard_styling(fig)
