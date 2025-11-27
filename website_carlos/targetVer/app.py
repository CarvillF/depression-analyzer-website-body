import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Page Config
st.set_page_config(
    page_title="Depression Analyzer", 
    page_icon="🧠", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- CSS Customization for "Premium" Feel ---
st.markdown("""
    <style>
    .stProgress > div > div > div > div {
        background-color: #4ecdc4;
    }
    .stButton>button {
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Session State Initialization ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = {}

# --- Mock Backend Logic ---
def predict_risk(data):
    """
    Simulates a call to a Random Forest model.
    Returns: probability (float), label (str), color (str)
    """
    time.sleep(2) # Simulate network/processing latency
    
    # Simple heuristic for demonstration
    score = 0
    # Academic Factors
    if data.get('academic_pressure', 0) >= 4: score += 1.5
    if data.get('study_satisfaction', 0) <= 2: score += 1
    
    # Health Factors
    if data.get('sleep_quality', 0) <= 2: score += 1.5
    if data.get('financial_stress', 0) >= 4: score += 1
    if data.get('family_history') == "Sí": score += 1
    
    # Normalize to a probability roughly between 0.1 and 0.9
    base_prob = 0.15
    prob = base_prob + (score * 0.12)
    
    # Add some random noise to make it feel "calculated"
    prob += np.random.uniform(-0.02, 0.02)
    prob = min(0.98, max(0.02, prob))
    
    if prob > 0.65:
        label = "Riesgo Alto"
        color = "red"
    elif prob > 0.35:
        label = "Riesgo Moderado"
        color = "orange"
    else:
        label = "Riesgo Bajo"
        color = "green"
        
    return prob, label, color

# --- Navigation Functions ---
def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

def restart():
    st.session_state.step = 1
    st.session_state.data = {}

# --- Sidebar ---
with st.sidebar:
    st.title("🧠 Depression Analyzer")
    st.markdown("---")
    st.info(
        """
        **Sobre este proyecto:**
        
        Esta herramienta utiliza Inteligencia Artificial (simulada) para detectar patrones de riesgo de depresión en estudiantes.
        
        Basado en el dataset: *Student Depression Dataset (Kaggle)*.
        """
    )
    st.warning(
        "⚠️ **Disclaimer:** Esta aplicación es un prototipo educativo. No sustituye el diagnóstico de un profesional."
    )
    st.markdown("---")
    st.caption("v2.0 - Target Product")

# --- Main Content ---

# Progress Bar (Only for steps 1-3)
if st.session_state.step < 4:
    st.markdown(f"### Paso {st.session_state.step} de 3")
    progress_val = (st.session_state.step - 1) / 3
    st.progress(progress_val)

# ---------------- STEP 1: PERFIL ----------------
if st.session_state.step == 1:
    st.header("👤 Perfil y Datos Básicos")
    st.markdown("Comencemos con información general para calibrar el modelo.")
    
    with st.form("step1_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Edad", min_value=16, max_value=60, value=20)
            gender = st.selectbox("Género", ["Masculino", "Femenino", "Otro"])
        with col2:
            city = st.text_input("Ciudad de Residencia", placeholder="Ej. Madrid, Lima, CDMX")
            year = st.selectbox("Año de Carrera", ["1er Año", "2do Año", "3er Año", "4to Año", "5to Año+"])
            
        st.markdown("---")
        submitted = st.form_submit_button("Siguiente ➡️", type="primary")
        
        if submitted:
            if not city.strip():
                st.error("⚠️ Por favor ingresa tu ciudad para continuar.")
            else:
                st.session_state.data.update({
                    "age": age, "gender": gender, "city": city, "year": year
                })
                next_step()
                st.rerun()

# ---------------- STEP 2: ACADÉMICO ----------------
elif st.session_state.step == 2:
    st.header("📚 Entorno Académico")
    st.markdown("Factores relacionados con tu vida universitaria.")
    
    with st.form("step2_form"):
        col1, col2 = st.columns(2)
        with col1:
            cgpa = st.number_input("CGPA (Promedio Acumulado)", min_value=0.0, max_value=10.0, value=3.5, step=0.1, help="Escala de 0 a 10")
        with col2:
            study_satisfaction = st.slider("Satisfacción con tus Estudios", 1, 5, 3, help="1 = Muy Insatisfecho, 5 = Muy Satisfecho")
        
        st.markdown("#### Presión Académica")
        academic_pressure = st.slider("Nivel de Presión Percibida (1-5)", 1, 5, 3)
        
        with st.expander("ℹ️ Guía para calificar la Presión Académica"):
            st.markdown("""
            *   **1 (Muy Baja):** Te sientes completamente relajado/a.
            *   **2 (Baja):** Tienes tareas pero son manejables.
            *   **3 (Moderada):** Presión normal de época de clases.
            *   **4 (Alta):** Te sientes ansioso/a por las entregas frecuentemente.
            *   **5 (Muy Alta):** La presión afecta tu sueño o salud.
            """)
            
        st.markdown("---")
        c1, c2 = st.columns([1, 1])
        with c1:
            back = st.form_submit_button("⬅️ Atrás")
        with c2:
            submitted = st.form_submit_button("Siguiente ➡️", type="primary")
            
        if back:
            prev_step()
            st.rerun()
        if submitted:
            st.session_state.data.update({
                "cgpa": cgpa, 
                "study_satisfaction": study_satisfaction, 
                "academic_pressure": academic_pressure
            })
            next_step()
            st.rerun()

# ---------------- STEP 3: SALUD Y BIENESTAR ----------------
elif st.session_state.step == 3:
    st.header("❤️ Salud y Bienestar")
    st.markdown("Hábitos de vida y factores externos.")
    
    with st.form("step3_form"):
        col1, col2 = st.columns(2)
        with col1:
            sleep = st.selectbox("Horas de Sueño (Promedio)", ["Menos de 5 h", "5-6 h", "7-8 h", "Más de 8 h"])
            diet = st.selectbox("Hábitos Alimenticios", ["No Saludable", "Moderado", "Saludable"])
        with col2:
            history = st.radio("Historial Familiar de Depresión", ["Sí", "No"], horizontal=True)
            
        st.markdown("#### Situación Financiera")
        financial_stress = st.slider("Nivel de Estrés Financiero", 1, 5, 3, help="1 = Sin preocupaciones, 5 = Dificultades severas")
        
        # Mappings for data processing
        sleep_map = {"Menos de 5 h": 1, "5-6 h": 2, "7-8 h": 4, "Más de 8 h": 5}
        diet_map = {"No Saludable": 1, "Moderado": 3, "Saludable": 5}
        
        st.markdown("---")
        c1, c2 = st.columns([1, 1])
        with c1:
            back = st.form_submit_button("⬅️ Atrás")
        with c2:
            submitted = st.form_submit_button("🚀 Calcular Probabilidad", type="primary")
            
        if back:
            prev_step()
            st.rerun()
        if submitted:
            st.session_state.data.update({
                "sleep_raw": sleep,
                "sleep_quality": sleep_map[sleep],
                "diet_raw": diet,
                "diet_quality": diet_map[diet],
                "family_history": history,
                "financial_stress": financial_stress
            })
            next_step()
            st.rerun()

# ---------------- STEP 4: DASHBOARD DE RESULTADOS ----------------
elif st.session_state.step == 4:
    # Full width for results
    
    # Simulation of processing
    if 'processed' not in st.session_state:
        with st.spinner("🔄 Analizando patrones en tus respuestas..."):
            prob, label, color = predict_risk(st.session_state.data)
            st.session_state.result = {"prob": prob, "label": label, "color": color}
            st.session_state.processed = True
            time.sleep(0.5) # Extra smooth feel
            st.rerun()
    
    # Retrieve results
    res = st.session_state.result
    prob = res['prob']
    label = res['label']
    color = res['color']
    
    # Header
    st.title("📊 Resultados del Análisis")
    if prob < 0.4:
        st.success("Análisis completado exitosamente.")
    elif prob < 0.7:
        st.warning("Análisis completado. Se detectaron algunos factores de riesgo.")
    else:
        st.error("Análisis completado. Atención requerida.")

    # Main Dashboard Layout
    col_gauge, col_radar = st.columns([1, 1.2])
    
    with col_gauge:
        st.subheader("Probabilidad de Depresión")
        # Gauge Chart
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = prob * 100,
            number = {'suffix': "%"},
            title = {'text': f"Nivel: <span style='color:{color}'>{label}</span>", 'font': {'size': 20}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 35], 'color': "rgba(76, 175, 80, 0.3)"},
                    {'range': [35, 65], 'color': "rgba(255, 152, 0, 0.3)"},
                    {'range': [65, 100], 'color': "rgba(244, 67, 54, 0.3)"}],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': prob * 100}}))
        
        fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
    with col_radar:
        st.subheader("Tú vs. Estudiante Promedio")
        
        # Prepare Data for Radar
        categories = ['Presión Acad.', 'Satisfacción', 'Estrés Fin.', 'Calidad Sueño', 'Dieta']
        
        # Normalize user values to 0-5 scale roughly for visualization
        # Sleep (1,2,4,5) -> direct
        # Diet (1,3,5) -> direct
        user_vals = [
            st.session_state.data['academic_pressure'],
            st.session_state.data['study_satisfaction'],
            st.session_state.data['financial_stress'],
            st.session_state.data['sleep_quality'],
            st.session_state.data['diet_quality']
        ]
        
        # Mock Average Data (Static for now)
        avg_vals = [3.0, 3.5, 2.5, 3.5, 3.0]
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=avg_vals,
            theta=categories,
            fill='toself',
            name='Promedio',
            line_color='gray',
            opacity=0.5
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=user_vals,
            theta=categories,
            fill='toself',
            name='Tú',
            line_color='#4ecdc4'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )),
            showlegend=True,
            height=350,
            margin=dict(l=40, r=40, t=20, b=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")
    
    # Recommendations Section
    st.subheader("💡 Recomendaciones Personalizadas")
    
    rec_col1, rec_col2 = st.columns([2, 1])
    
    with rec_col1:
        if prob > 0.5:
            st.markdown(
                """
                <div style="padding: 20px; border-radius: 10px; background-color: rgba(255, 0, 0, 0.1); border-left: 5px solid red;">
                    <h4>⚠️ Riesgo Elevado Detectado</h4>
                    <p>Tus respuestas indican niveles altos de estrés y factores de riesgo asociados a la depresión.</p>
                    <ul>
                        <li><strong>Busca apoyo:</strong> No dudes en contactar a los servicios de bienestar estudiantil.</li>
                        <li><strong>Habla con alguien:</strong> Compartir tus sentimientos con un amigo o familiar puede ayudar.</li>
                        <li><strong>Prioriza el descanso:</strong> Intenta regular tu ciclo de sueño.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="padding: 20px; border-radius: 10px; background-color: rgba(0, 255, 0, 0.1); border-left: 5px solid green;">
                    <h4>✅ Estado Saludable</h4>
                    <p>Tus indicadores sugieren un buen equilibrio entre vida académica y personal.</p>
                    <ul>
                        <li>Sigue manteniendo tus hábitos de sueño y alimentación.</li>
                        <li>Si sientes que la presión aumenta, toma descansos activos.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True
            )
            
    with rec_col2:
        st.markdown("### 📞 Recursos")
        st.markdown(
            """
            *   **Emergencias:** 911
            *   **Línea de Vida:** 988
            *   **Consejería Univ:** (555) 123-4567
            """
        )

    st.markdown("---")
    if st.button("🔄 Realizar Nueva Encuesta"):
        # Clear specific keys or just reset step
        st.session_state.processed = False # Reset flag
        restart()
        st.rerun()
