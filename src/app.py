import sys
import os

# Asegurar que el directorio raíz del proyecto esté en el path de Python para importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px

from config.settings import EXCEL_PATH
from src.data_loader import load_and_preprocess_data, parse_multiselect_column, PREGUNTAS_MAP
import src.charts as charts

# Configuración inicial de Streamlit
st.set_page_config(
    page_title="UPAO Link - Cuestionario Completo",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo visual inyectado CSS para un look moderno de alta gama (identidad corporativa UPAO)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }
        
        /* Contenedores premium para métricas principales */
        .metric-card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
            text-align: center;
            transition: all 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-4px);
            border-color: #00C2FF;
        }
        .metric-title {
            color: #94a3b8;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }
        .metric-value {
            font-size: 34px;
            font-weight: 800;
            background: linear-gradient(to right, #00C2FF, #2ECC71);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .metric-subtitle {
            color: #64748b;
            font-size: 12px;
            margin-top: 6px;
        }
        
        /* Diseño de tarjetas de pregunta */
        .question-card {
            background: rgba(30, 41, 59, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 25px;
            border-left: 5px solid #00C2FF;
        }
        .question-header {
            color: #ffffff;
            font-weight: 800;
            font-size: 18px;
            margin-bottom: 15px;
        }
        
        /* Ficha individual */
        .student-profile {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
        }
        .student-header {
            border-bottom: 2px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 15px;
            margin-bottom: 20px;
        }
        .profile-row {
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------
# PIPELINE DE CARGA DE DATOS
# ---------------------------------------------
try:
    df = load_and_preprocess_data(EXCEL_PATH)
except Exception as e:
    st.error(f"Error al cargar el archivo de datos: {e}")
    st.warning("Verifica que el archivo Excel de respuestas se encuentre dentro de 'data/raw/'.")
    st.stop()

# ---------------------------------------------
# DISEÑO DE LA BARRA LATERAL (SIDEBAR)
# ---------------------------------------------
st.sidebar.markdown(
    """
    <div style='text-align: center; margin-bottom: 20px;'>
        <h1 style='color: #00C2FF; font-weight: 800; font-size: 24px; margin-bottom: 5px;'>UPAO Link</h1>
        <p style='color: #94a3b8; font-size: 13px;'>Respuestas del Forms Oficial</p>
    </div>
    <hr style='border: 0; height: 1px; background: rgba(255,255,255,0.1); margin-bottom: 25px;'>
    """,
    unsafe_allow_html=True
)

st.sidebar.subheader("🎯 Filtros de Segmentación")

tipo_correo_opciones = ["Todos los estudiantes", "Solo correos UPAO (@upao.edu.pe)", "Solo correos personales"]
filtro_correo = st.sidebar.selectbox("Filtrar por Dominio de Correo", tipo_correo_opciones)

df_filtered = df.copy()
if filtro_correo == "Solo correos UPAO (@upao.edu.pe)":
    df_filtered = df_filtered[df_filtered["Tipo_Correo"] == "Institucional UPAO"]
elif filtro_correo == "Solo correos personales":
    df_filtered = df_filtered[df_filtered["Tipo_Correo"] == "Personal / Otro"]

st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.info(
    "📊 **Fidelidad con tu Forms**\n\n"
    "Este dashboard muestra las preguntas en el mismo orden cronológico (1 al 20) y con las frecuencias exactas "
    "de tu formulario de Google Forms."
)

st.sidebar.markdown(
    """
    <div style='text-align: center; color: #64748b; font-size: 11px; margin-top: 30px;'>
        Fidelidad de Formulario v3.0
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------
# CABECERA DE LA PÁGINA
# ---------------------------------------------
st.markdown(
    """
    <div style='background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%); padding: 25px; border-radius: 16px; margin-bottom: 25px; border-left: 6px solid #00C2FF;'>
        <h1 style='color: #ffffff; margin: 0; font-size: 32px; font-weight: 800;'>🎓 Cuestionario UPAO Link - Respuestas Oficiales</h1>
        <p style='color: #94a3b8; font-size: 15px; margin-top: 5px; margin-bottom: 0;'>
            Análisis secuencial pregunta por pregunta y navegador de respuestas individuales.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------
# PESTAÑAS PRINCIPALES (REPRESENTAN EL FORMS)
# ---------------------------------------------
tab_resumen, tab_preguntas, tab_individual, tab_base_datos = st.tabs([
    "📊 Resumen del Forms",
    "📋 Respuestas Pregunta por Pregunta (1 - 20)",
    "👤 Respuestas Individuales",
    "🗃️ Base de Datos Completa"
])

# ==============================================================================
# PESTAÑA 1: RESUMEN DEL FORMS
# ==============================================================================
with tab_resumen:
    col1, col2, col3, col4 = st.columns(4)
    total_encuestas = len(df_filtered)
    
    # Cálculos globales
    freq_alta = len(df_filtered[df_filtered["Q1_frecuencia_falta"].str.contains("Frecuentemente", na=False)])
    porcentaje_freq_alta = (freq_alta / total_encuestas * 100) if total_encuestas > 0 else 0
    
    poseen_articulos = len(df_filtered[df_filtered["Q5_articulos_disponibles"].str.contains("Sí|Tengo 1", na=False)])
    porcentaje_poseen = (poseen_articulos / total_encuestas * 100) if total_encuestas > 0 else 0
    
    confianza_upao = len(df_filtered[df_filtered["Q10_registro_institucional"].str.contains("confianza", na=False)])
    porcentaje_confianza = (confianza_upao / total_encuestas * 100) if total_encuestas > 0 else 0

    with col1:
        st.markdown(f"""<div class="metric-card"><div class="metric-title">Respuestas Totales</div><div class="metric-value">{total_encuestas}</div><div class="metric-subtitle">Alumnos respondieron</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card"><div class="metric-title">Falta de Insumos</div><div class="metric-value">{porcentaje_freq_alta:.1f}%</div><div class="metric-subtitle">Sufren de escasez urgente</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card"><div class="metric-title">Artículos en Campus</div><div class="metric-value">{porcentaje_poseen:.1f}%</div><div class="metric-subtitle">Disposición para compartir</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card"><div class="metric-title">Verificación de Identidad</div><div class="metric-value">{porcentaje_confianza:.1f}%</div><div class="metric-subtitle">Seguridad vía @upao.edu.pe</div></div>""", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.subheader("💡 Resumen Ejecutivo")
        st.markdown(
            """
            Este dashboard representa con total fidelidad la encuesta de **Estudio de Necesidades: Intercambio de Materiales Académicos en el Campus UPAO**.
            
            * **Falta Frecuente**: Los estudiantes experimentan falta temporal de artículos (calculadoras, separatas, adaptadores) pero no tienen presupuesto para adquirirlos temporalmente.
            * **Oferta Subutilizada**: Los alumnos tienen artículos acumulados en sus hogares que están dispuestos a rentar.
            * **Filtros de Seguridad**: La validación de correo institucional brinda la confianza requerida por los prestadores.
            
            *Navega a la siguiente pestaña para ver el análisis pregunta por pregunta.*
            """
        )
    with col_right:
        correo_counts = df_filtered["Tipo_Correo"].value_counts().reset_index()
        correo_counts.columns = ["Tipo de Correo", "Cantidad"]
        fig_correo = px.pie(
            correo_counts, 
            names="Tipo de Correo", 
            values="Cantidad", 
            title="Correos registrados",
            color_discrete_sequence=["#00C2FF", "#F39C12"]
        )
        fig_correo.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#ffffff')
        st.plotly_chart(fig_correo, use_container_width=True)

# ==============================================================================
# PESTAÑA 2: RESPUESTAS PREGUNTA POR PREGUNTA (1 - 20)
# ==============================================================================
with tab_preguntas:
    st.subheader("📋 Cuestionario Cronológico de Google Forms")
    st.caption("A continuación se detallan las 20 preguntas de la encuesta en su orden de secuencia original, con sus respectivos gráficos de frecuencia y tablas de porcentajes.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Mapeo de cada pregunta a su respectivo método gráfico en charts.py
    preguntas_graficos = {
        "Q1_frecuencia_falta": charts.create_q1_frequency_chart,
        "Q2_articulos_falta": charts.create_q2_needed_articles_chart,
        "Q3_solucion_actual": charts.create_q3_current_solutions_chart,
        "Q4_filtros_busqueda": charts.create_q4_priority_filters_chart,
        "Q5_articulos_disponibles": charts.create_q5_own_articles_chart,
        "Q6_barrera_compartir": charts.create_q6_renting_barriers_chart,
        "Q7_descuento_semanal": charts.create_q7_weekly_discounts_chart,
        "Q8_boton_pausar": charts.create_q8_pausing_button_chart,
        "Q9_estadisticas_vistas": charts.create_q9_views_stats_chart,
        "Q10_registro_institucional": charts.create_q10_registration_trust_chart,
        "Q11_deposito_garantia": charts.create_q11_deposit_acceptance_chart,
        "Q12_metodo_retiro": charts.create_q12_payout_methods_chart,
        "Q13_comision_seguro": charts.create_q13_commission_acceptance_chart,
        "Q14_herramienta_coordinacion": charts.create_q14_meetup_channel_chart,
        "Q15_metodo_confirmacion": charts.create_q15_delivery_verification_chart,
        "Q16_cancelacion_reserva": charts.create_q16_cancelation_importance_chart,
        "Q17_extension_plazo": charts.create_q17_extension_preference_chart,
        "Q18_resolucion_disputas": charts.create_q18_dispute_resolution_chart,
        "Q19_importancia_resenas": charts.create_q19_reviews_importance_chart,
        "Q20_penalidad_retraso": charts.create_q20_delay_penalties_chart
    }
    
    # Listar las preguntas secuencialmente del 1 al 20
    q_keys = list(PREGUNTAS_MAP.keys())[2:] # Omitir timestamp y email
    
    for idx, key in enumerate(q_keys, 1):
        question_text = PREGUNTAS_MAP[key]
        
        # HTML custom card container
        st.markdown(f"""
            <div class="question-card">
                <div class="question-header">Pregunta {idx}: {question_text}</div>
            </div>
        """, unsafe_allow_html=True)
        
        col_chart, col_table = st.columns([3, 2])
        
        with col_chart:
            # Renderizar gráfico Plotly dinámico
            if key in preguntas_graficos:
                fig_fn = preguntas_graficos[key]
                st.plotly_chart(fig_fn(df_filtered), use_container_width=True, key=f"chart_{key}")
                
        with col_table:
            # Calcular tabla de frecuencias y porcentajes
            st.markdown("<div style='font-size:14px; font-weight:600; margin-bottom:8px;'>Tabla de Frecuencias:</div>", unsafe_allow_html=True)
            
            # Chequeamos si es multi-select (Q2, Q4, Q12)
            if key in ["Q2_articulos_falta", "Q4_filtros_busqueda", "Q12_metodo_retiro"]:
                counts = parse_multiselect_column(df_filtered, key)
                pcts = (counts / total_encuestas * 100) if total_encuestas > 0 else 0
                freq_table = pd.DataFrame({
                    "Respuesta Seleccionada": counts.index,
                    "Votos (Conteo)": counts.values,
                    "Porcentaje de Muestra (%)": [f"{p:.1f}%" for p in pcts]
                })
            else:
                counts = df_filtered[key].value_counts()
                pcts = df_filtered[key].value_counts(normalize=True) * 100
                freq_table = pd.DataFrame({
                    "Respuesta Seleccionada": counts.index,
                    "Votos (Conteo)": counts.values,
                    "Porcentaje (%)": [f"{p:.1f}%" for p in pcts]
                })
                
            st.dataframe(freq_table, hide_index=True, use_container_width=True)
            
        st.markdown("<br><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.06); margin-bottom: 30px;'>", unsafe_allow_html=True)

# ==============================================================================
# PESTAÑA 3: RESPUESTAS INDIVIDUALES (Ficha del Estudiante)
# ==============================================================================
with tab_individual:
    st.subheader("👤 Visor de Respuestas Individuales por Estudiante")
    st.caption("Selecciona una dirección de correo para revisar la ficha de encuesta digitalizada con todas sus respuestas en orden.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Crear selector de correos
    estudiantes_opciones = df["email"].tolist()
    seleccion_estudiante = st.selectbox("Seleccionar Alumno a Consultar:", estudiantes_opciones)
    
    if seleccion_estudiante:
        # Extraer fila del estudiante seleccionado
        student_data = df[df["email"] == seleccion_estudiante].iloc[0]
        
        # HTML Profile Container
        st.markdown(f"""
            <div class="student-profile">
                <div class="student-header">
                    <h2 style="color:#00C2FF; margin:0; font-weight:800; font-size:24px;">Ficha Oficial de Cuestionario</h2>
                    <p style="color:#94a3b8; font-size:14px; margin-top:5px; margin-bottom:0;">
                        <b>Estudiante:</b> {seleccion_estudiante} &nbsp;|&nbsp; <b>Fecha de Envío:</b> {student_data['timestamp']}
                    </p>
                </div>
        """, unsafe_allow_html=True)
        
        # Renders secuencial 1 al 20
        q_keys_ind = list(PREGUNTAS_MAP.keys())[2:] # Omitir email y timestamp
        for idx, key in enumerate(q_keys_ind, 1):
            question_text = PREGUNTAS_MAP[key]
            student_answer = str(student_data[key])
            
            st.markdown(f"""
                <div class="profile-row">
                    <div style="font-weight:600; color:#94a3b8; font-size:14px; margin-bottom:3px;">
                        Pregunta {idx}: {question_text}
                    </div>
                    <div style="color:#ffffff; font-weight:800; font-size:16px; padding-left:10px; border-left:3px solid #2ECC71;">
                        {student_answer}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# PESTAÑA 4: BASE DE DATOS COMPLETA
# ==============================================================================
with tab_base_datos:
    st.subheader("🗃️ Repositorio Completo de Datos Limpios")
    st.caption("Explora y descarga la base de datos completa de las 23 respuestas del Excel preprocesada y desinfectada de errores de codificación.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    
    # Crear botón de descarga en CSV
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Base de Datos en CSV",
        data=csv_data,
        file_name="Cuestionario_UPAO_Limpio.csv",
        mime="text/csv"
    )
