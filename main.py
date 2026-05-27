import os
import sys
import subprocess

# ---------------------------------------------
# VERIFICACIÓN E INSTALACIÓN DE DEPENDENCIAS
# ---------------------------------------------
def verify_and_install_dependencies():
    """
    Verifica las dependencias del proyecto. Si falta alguna,
    intenta instalarlas utilizando requirements.txt de forma silenciosa.
    """
    dependencies = {
        "pandas": "pandas",
        "openpyxl": "openpyxl",
        "streamlit": "streamlit",
        "plotly": "plotly"
    }
    
    missing = []
    for lib, import_name in dependencies.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(lib)
            
    if missing:
        print(f"[WARN] Faltan dependencias criticas: {', '.join(missing)}")
        print("[INFO] Intentando instalar dependencias desde requirements.txt...")
        
        req_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
        if not os.path.exists(req_path):
            with open(req_path, "w", encoding="utf-8") as f:
                f.write("pandas>=2.0.0\nopenpyxl>=3.1.0\nstreamlit>=1.30.0\nplotly>=5.18.0\n")
                
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_path])
            print("[OK] Dependencias instaladas con exito.")
        except Exception as e:
            print(f"[ERROR] Error al instalar dependencias de manera automatica: {e}")
            print(f"Por favor, ejecuta manualmente: pip install -r requirements.txt")
            sys.exit(1)

# Validar antes de continuar
verify_and_install_dependencies()

# Importar configuraciones y módulos modularizados
from config.settings import EXCEL_PATH, HTML_OUTPUT_PATH, PALETA_COLORES
from src.data_loader import load_and_preprocess_data, parse_multiselect_column, PREGUNTAS_MAP
import src.charts as charts
import plotly.offline as pyo
import pandas as pd

# ---------------------------------------------
# COMPILACIÓN DEL REPORTE INTERACTIVO PREMIUM (HTML)
# ---------------------------------------------
def generate_redesigned_html_report():
    print(f"[INFO] Iniciando pipeline ETL para la carga de datos de la encuesta...")
    try:
        df = load_and_preprocess_data(EXCEL_PATH)
    except Exception as e:
        print(f"[ERROR] Error al cargar los datos en el orquestador: {e}")
        return False
        
    print(f"[INFO] Generando graficos y tablas pregunta por pregunta cronologicamente...")
    
    total_encuestas = len(df)
    
    # Calcular métricas globales para las tarjetas de resumen
    freq_alta = len(df[df["Q1_frecuencia_falta"].str.contains("Frecuentemente", na=False)])
    pct_freq_alta = (freq_alta / total_encuestas * 100) if total_encuestas > 0 else 0
    
    poseen_art = len(df[df["Q5_articulos_disponibles"].str.contains("Sí|Tengo 1", na=False)])
    pct_poseen = (poseen_art / total_encuestas * 100) if total_encuestas > 0 else 0

    conf_seg = len(df[df["Q10_registro_institucional"].str.contains("confianza", na=False)])
    pct_conf = (conf_seg / total_encuestas * 100) if total_encuestas > 0 else 0

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
    
    questions_html = []
    
    for idx, key in enumerate(q_keys, 1):
        question_text = PREGUNTAS_MAP[key]
        
        # Generar gráfico interactivo Plotly.js
        fig_fn = preguntas_graficos[key]
        fig = fig_fn(df)
        div_chart = pyo.plot(fig, include_plotlyjs=False, output_type='div')
        
        # Calcular tabla de frecuencias en HTML
        if key in ["Q2_articulos_falta", "Q4_filtros_busqueda", "Q12_metodo_retiro"]:
            counts = parse_multiselect_column(df, key)
            pcts = (counts / total_encuestas * 100) if total_encuestas > 0 else 0
            
            table_rows = []
            for option, count, pct in zip(counts.index, counts.values, pcts):
                table_rows.append(f"<tr><td>{option}</td><td><b>{count}</b></td><td class='pct-cell'>{pct:.1f}%</td></tr>")
            
            headers = "<th>Respuesta Seleccionada (Forms)</th><th>Menciones (Votos)</th><th>Porcentaje de Muestra (%)</th>"
        else:
            counts = df[key].value_counts()
            pcts = df[key].value_counts(normalize=True) * 100
            
            table_rows = []
            for option, count, pct in zip(counts.index, counts.values, pcts):
                table_rows.append(f"<tr><td>{option}</td><td><b>{count}</b></td><td class='pct-cell'>{pct:.1f}%</td></tr>")
                
            headers = "<th>Respuesta Seleccionada (Forms)</th><th>Votos (Conteo)</th><th>Porcentaje (%)</th>"
            
        rows_str = "\n".join(table_rows)
        
        question_card_html = f"""
        <div class="question-card-wrapper">
            <div class="question-header-bar">
                <span class="q-badge">Pregunta {idx}</span>
                <span class="q-title">{question_text}</span>
            </div>
            <div class="question-card-body">
                <div class="chart-section">
                    {div_chart}
                </div>
                <div class="table-section">
                    <h4 class="table-title">Distribución de Respuestas</h4>
                    <table class="freq-table">
                        <thead>
                            <tr>
                                {headers}
                            </tr>
                        </thead>
                        <tbody>
                            {rows_str}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        """
        questions_html.append(question_card_html)
        
    all_questions_html = "\n".join(questions_html)

    print(f"[INFO] Compilando plantilla HTML con diseno cronologico (Pregunta por Pregunta)...")
    
    # Estructurar la plantilla HTML con un diseño ultra premium
    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UPAO Link - Reporte Cronológico del Forms</title>
    <!-- Cargar Plotly.js para la interactividad de los div -->
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: 'Outfit', sans-serif;
            background-color: #0b0f19;
            color: #f8fafc;
            line-height: 1.6;
            padding: 30px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        /* Encabezado Premium con gradiente moderno */
        header {{
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 35px;
            border-radius: 20px;
            margin-bottom: 35px;
            border-left: 6px solid #00C2FF;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        }}
        header h1 {{
            font-size: 34px;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(to right, #ffffff, #00C2FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        header p {{
            color: #94a3b8;
            font-size: 16px;
            margin-top: 6px;
        }}
        
        /* Grid de Tarjetas Métricas */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #131b2e 0%, #0b0f19 100%);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 18px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        .metric-card:hover {{
            transform: translateY(-4px);
            border-color: #00C2FF;
            box-shadow: 0 12px 20px -5px rgba(0, 194, 255, 0.2);
        }}
        .metric-title {{
            color: #64748b;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }}
        .metric-value {{
            font-size: 38px;
            font-weight: 800;
            color: #00C2FF;
            background: linear-gradient(to right, #00C2FF, #2ECC71);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .metric-subtitle {{
            color: #475569;
            font-size: 12px;
            margin-top: 6px;
        }}
        
        /* Tarjetas Cronológicas de Preguntas */
        .question-card-wrapper {{
            background: linear-gradient(135deg, #131b2e 0%, #0f1423 100%);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            margin-bottom: 40px;
            overflow: hidden;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
            border-left: 5px solid #00C2FF;
        }}
        .question-header-bar {{
            background: rgba(30, 41, 59, 0.5);
            padding: 20px 25px;
            display: flex;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }}
        .q-badge {{
            background: #00C2FF;
            color: #0f1423;
            font-weight: 800;
            font-size: 12px;
            padding: 6px 14px;
            border-radius: 20px;
            margin-right: 15px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
        }}
        .q-title {{
            font-size: 18px;
            font-weight: 600;
            color: #ffffff;
        }}
        .question-card-body {{
            display: grid;
            grid-template-columns: 3fr 2fr;
            gap: 25px;
            padding: 30px;
        }}
        @media (max-width: 960px) {{
            .question-card-body {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .chart-section {{
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 350px;
        }}
        
        .table-section {{
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }}
        .table-title {{
            color: #00C2FF;
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        /* Tabla de Frecuencias Premium */
        .freq-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
            background: rgba(30, 41, 59, 0.25);
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.04);
        }}
        .freq-table th {{
            background: rgba(0, 194, 255, 0.08);
            color: #00C2FF;
            text-align: left;
            padding: 12px 16px;
            font-weight: 600;
            border-bottom: 1px solid rgba(0, 194, 255, 0.15);
        }}
        .freq-table td {{
            padding: 12px 16px;
            color: #e2e8f0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
        }}
        .freq-table tr:last-child td {{
            border-bottom: none;
        }}
        .freq-table tr:hover {{
            background: rgba(255, 255, 255, 0.02);
        }}
        .pct-cell {{
            color: #2ECC71 !important;
            font-weight: 600;
        }}
        
        /* Footer */
        footer {{
            text-align: center;
            padding: 50px 0 20px 0;
            color: #475569;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Encabezado de la página -->
        <header>
            <h1>🎓 UPAO Link - Reporte Cronológico del Cuestionario</h1>
            <p>Análisis pregunta por pregunta (1 al 20) de la encuesta sobre intercambio y alquiler de materiales académicos en la UPAO.</p>
        </header>

        <!-- Tarjetas Métricas Principales -->
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-title">Respuestas Recibidas</div>
                <div class="metric-value">{total_encuestas}</div>
                <div class="metric-subtitle">Estudiantes encuestados</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Falta de Insumos</div>
                <div class="metric-value">{pct_freq_alta:.1f}%</div>
                <div class="metric-subtitle">Requieren materiales frecuentemente</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Artículos en Campus</div>
                <div class="metric-value">{pct_poseen:.1f}%</div>
                <div class="metric-subtitle">Disposición para compartir</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Validación UPAO</div>
                <div class="metric-value">{pct_conf:.1f}%</div>
                <div class="metric-subtitle">Apoyan el registro institucional</div>
            </div>
        </div>

        <!-- LISTADO SECUENCIAL DE PREGUNTAS (1 AL 20) -->
        <h2 style="font-size:24px; font-weight:800; margin: 40px 0 25px 0; color:#00C2FF; border-bottom: 2px solid rgba(255,255,255,0.06); padding-bottom:10px;">📋 Resultados Detallados de las Preguntas (Forms)</h2>
        
        {all_questions_html}

        <footer>
            <p>Reporte oficial generado con tecnología interactiva Plotly en Python. © 2026 UPAO Link Analytics.</p>
        </footer>
    </div>
</body>
</html>
"""
    try:
        # Asegurar la existencia del directorio de reportes
        os.makedirs(os.path.dirname(HTML_OUTPUT_PATH), exist_ok=True)
        
        with open(HTML_OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(html_template)
        print(f"[OK] Reporte estatico interactivo generado con exito en '{HTML_OUTPUT_PATH}'!")
        return True
    except Exception as e:
        print(f"[ERROR] Error al escribir el reporte HTML: {e}")
        return False

# ---------------------------------------------
# EJECUCIÓN PRINCIPAL
# ---------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("INICIANDO ANALIZADOR DE ENCUESTAS MODULAR - UPAO")
    print("=" * 60)
    
    # 1. Compilar el reporte estático premium en reports/
    generate_redesigned_html_report()
    print("-" * 60)
    
    # 2. Desplegar el Dashboard Dinámico con Streamlit
    print("[INFO] Lanzando Dashboard dinamico (Streamlit) en el navegador local...")
    try:
        app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "app.py")
        subprocess.Popen(["streamlit", "run", app_path, "--browser.gatherUsageStats=false", "--server.headless=false"], shell=True)
        print("[OK] Dashboard dinámico en ejecución.")
    except Exception as e:
        print(f"[WARN] No se pudo lanzar Streamlit automáticamente: {e}")
        print("Puedes iniciarlo ejecutando manualmente: streamlit run src/app.py")
        
    print("\n[OK] Proceso modular completado con exito!")
