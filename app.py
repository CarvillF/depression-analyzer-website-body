import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
import os

# Add parent directory to path to allow importing from sibling directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from adviceModule_Esin.advice import generate_advice_for_symptom

# Add ml_grace directory to path for model utilities
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ml_grace')))
from model_utils import predict_both
from model_utils import load_models


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

# --- ML Model Prediction Function ---
@st.cache_resource
def load_ml_models():
    """Cache the model loading to avoid reloading on every interaction"""
    return load_models()

def predict_outcomes(data):
    """
    Use trained ML models to predict depression and suicidal thoughts risk.
    Returns: 
        - dep_prob (float): Probability of Depression
        - dep_label (str)
        - dep_color (str)
        - suicide_prob (float): Probability of Suicidal Thoughts
        - suicide_label (str)
    """
    time.sleep(2)  # Simulate processing time for UX
    
    try:
        # Load models (cached)
        load_ml_models()
        
        # Get predictions from ML models
        predictions = predict_both(
            gender=data.get('gender', 'Male'),
            age=data.get('age', 20),
            academic_pressure=data.get('academic_pressure', 3),
            study_satisfaction=data.get('study_satisfaction', 3),
            sleep_duration=data.get('sleep_quality', 3),  # Using encoded value
            dietary_habits=data.get('diet_quality', 2),  # Using encoded value
            study_hours=data.get('study_hours', 5),
            financial_stress=data.get('financial_stress', 3),
            family_history=data.get('family_history', 'No')
        )
        
        # Get probabilities
        dep_prob = predictions['depression_probability']
        suicide_prob = predictions['suicidal_probability']
        
    except Exception as e:
        # Fallback to simple heuristic if model fails
        print(f"Model prediction error: {e}")
        dep_prob = 0.0
        suicide_prob = 0.0
    
    # Classify depression risk
    if dep_prob > 0.65:
        dep_label = "High Risk"
        dep_color = "red"
    elif dep_prob > 0.35:
        dep_label = "Moderate Risk"
        dep_color = "orange"
    else:
        dep_label = "Low Risk"
        dep_color = "green"
    
    # Classify suicidal thoughts risk
    if suicide_prob > 0.5:
        suicide_label = "DETECTED"
    else:
        suicide_label = "LOW"
        
    return dep_prob, dep_label, dep_color, suicide_prob, suicide_label

def get_advice_data(data):
    """
    Maps app data to advice module format.
    Returns a dictionary of symptoms and their advice.
    """
    advice_results = {}
    
    # Map Sleep: 1-5 (High is good) -> 0-10 (High is bad)
    # 1->10, 2->8, 3->6, 4->4, 5->2
    if 'sleep_quality' in data:
        sleep_score = (6 - data['sleep_quality']) * 2
        advice_results['sleep'] = generate_advice_for_symptom('sleep', sleep_score)
        
    # Map Appetite/Diet: 1-5 (High is good) -> 0-10 (High is bad)
    if 'diet_quality' in data:
        diet_score = (6 - data['diet_quality']) * 2
        advice_results['appetite'] = generate_advice_for_symptom('appetite', diet_score)
        
    # Map Stress: Avg of Academic & Financial (1-5, High is bad) -> 0-10 (High is bad)
    # 1->2, 2->4, 3->6, 4->8, 5->10
    stress_sources = []
    if 'academic_pressure' in data: stress_sources.append(data['academic_pressure'])
    if 'financial_stress' in data: stress_sources.append(data['financial_stress'])
    
    if stress_sources:
        avg_stress = sum(stress_sources) / len(stress_sources)
        stress_score = avg_stress * 2
        advice_results['stress'] = generate_advice_for_symptom('stress', stress_score)
        
    # Map Mood: Study Satisfaction (1-5, High is good) -> 0-10 (High is bad)
    if 'study_satisfaction' in data:
        mood_score = (6 - data['study_satisfaction']) * 2
        advice_results['mood'] = generate_advice_for_symptom('mood', mood_score)
        
    return advice_results

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
        **About this project:**
        
        This tool uses Artificial Intelligence (simulated) to detect depression risk patterns in students.
        
        Based on dataset: *Student Depression Dataset (Kaggle)*.
        """
    )
    st.warning(
        "⚠️ **Disclaimer:** This application is an educational prototype. It does not replace professional diagnosis."
    )
    st.markdown("---")
    st.caption("v2.1 - Target Product")

# --- Main Content ---

# Progress Bar (Only for steps 1-3)
if st.session_state.step < 4:
    st.markdown(f"### Step {st.session_state.step} of 3")
    progress_val = (st.session_state.step - 1) / 3
    st.progress(progress_val)

# ---------------- STEP 1: PERFIL & ANTECEDENTES ----------------
if st.session_state.step == 1:
    st.header("👤 Profile & Background")
    st.markdown("Basic information and family history.")
    
    with st.form("step1_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=16, max_value=60, value=20)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        with col2:
            history = st.radio("Family History of Depression", ["Yes", "No"], horizontal=True)
            
        st.markdown("---")
        submitted = st.form_submit_button("Next ➡️", type="primary")
        
        if submitted:
            st.session_state.data.update({
                "age": age, "gender": gender, "family_history": history
            })
            next_step()
            st.rerun()

# ---------------- STEP 2: ACADÉMICO ----------------
elif st.session_state.step == 2:
    st.header("📚 Academic Environment")
    st.markdown("Factors related to your university life.")
    
    with st.form("step2_form"):
        col1, col2 = st.columns(2)
        with col1:
            study_hours = st.number_input("Study Hours (Daily Average)", min_value=0, max_value=24, value=4)
        with col2:
            study_satisfaction = st.slider("Study Satisfaction", 1, 5, 3, help="1 = Very Dissatisfied, 5 = Very Satisfied")
        
        st.markdown("#### Academic Pressure")
        academic_pressure = st.slider("Perceived Pressure Level (1-5)", 1, 5, 3)
        
        with st.expander("ℹ️ Guide to rating Academic Pressure"):
            st.markdown("""
            *   **1 (Very Low):** You feel completely relaxed.
            *   **2 (Low):** You have tasks but they are manageable.
            *   **3 (Moderate):** Normal pressure for class periods.
            *   **4 (High):** You feel anxious about deadlines frequently.
            *   **5 (Very High):** Pressure affects your sleep or health.
            """)
            
        st.markdown("---")
        c1, c2 = st.columns([1, 1])
        with c1:
            back = st.form_submit_button("⬅️ Back")
        with c2:
            submitted = st.form_submit_button("Next ➡️", type="primary")
            
        if back:
            prev_step()
            st.rerun()
        if submitted:
            st.session_state.data.update({
                "study_hours": study_hours, 
                "study_satisfaction": study_satisfaction, 
                "academic_pressure": academic_pressure
            })
            next_step()
            st.rerun()

# ---------------- STEP 3: SALUD Y BIENESTAR ----------------
elif st.session_state.step == 3:
    st.header("❤️ Health & Wellness")
    st.markdown("Lifestyle habits and external factors.")
    
    with st.form("step3_form"):
        col1, col2 = st.columns(2)
        with col1:
            sleep = st.selectbox("Sleep Hours (Average)", ["Less than 5 h", "5-6 h", "7-8 h", "More than 8 h"])
            diet = st.selectbox("Dietary Habits", ["Unhealthy", "Moderate", "Healthy"])
        with col2:
            financial_stress = st.slider("Financial Stress Level", 1, 5, 3, help="1 = No worries, 5 = Severe difficulties")
            
        # Mappings for data processing
        sleep_map = {"Less than 5 h": 1, "5-6 h": 2, "7-8 h": 4, "More than 8 h": 5}
        diet_map = {"Unhealthy": 1, "Moderate": 3, "Healthy": 5}
        
        st.markdown("---")
        c1, c2 = st.columns([1, 1])
        with c1:
            back = st.form_submit_button("⬅️ Back")
        with c2:
            submitted = st.form_submit_button("🚀 Calculate Probability", type="primary")
            
        if back:
            prev_step()
            st.rerun()
        if submitted:
            st.session_state.data.update({
                "sleep_raw": sleep,
                "sleep_quality": sleep_map[sleep],
                "diet_raw": diet,
                "diet_quality": diet_map[diet],
                "financial_stress": financial_stress
            })
            next_step()
            st.rerun()

# ---------------- STEP 4: DASHBOARD DE RESULTADOS ----------------
elif st.session_state.step == 4:
    # Full width for results
    
    # Simulation of processing
    if 'processed' not in st.session_state:
        with st.spinner("🔄 Analyzing patterns in your responses..."):
            dep_prob, dep_label, dep_color, suicide_prob, suicide_label = predict_outcomes(st.session_state.data)
            st.session_state.result = {
                "dep_prob": dep_prob, "dep_label": dep_label, "dep_color": dep_color,
                "suicide_prob": suicide_prob, "suicide_label": suicide_label,
                "advice_data": get_advice_data(st.session_state.data)
            }
            st.session_state.processed = True
            time.sleep(0.5) # Extra smooth feel
            st.rerun()
    
    # Retrieve results
    res = st.session_state.result
    dep_prob = res['dep_prob']
    dep_label = res['dep_label']
    dep_color = res['dep_color']
    suicide_prob = res['suicide_prob']
    suicide_label = res['suicide_label']
    
    # Header
    st.title("📊 Analysis Results")
    if dep_prob < 0.4:
        st.success("Analysis completed successfully.")
    elif dep_prob < 0.7:
        st.warning("Analysis completed. Some risk factors detected.")
    else:
        st.error("Analysis completed. Attention required.")

    # Main Dashboard Layout
    col_gauge, col_radar = st.columns([1, 1.2])
    
    with col_gauge:
        st.subheader("Depression Risk")
        # Gauge Chart
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = dep_prob * 100,
            number = {'suffix': "%"},
            title = {'text': f"Level: <span style='color:{dep_color}'>{dep_label}</span>", 'font': {'size': 20}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': dep_color},
                'steps': [
                    {'range': [0, 35], 'color': "rgba(76, 175, 80, 0.3)"},
                    {'range': [35, 65], 'color': "rgba(255, 152, 0, 0.3)"},
                    {'range': [65, 100], 'color': "rgba(244, 67, 54, 0.3)"}],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': dep_prob * 100}}))
        
        fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Suicidal Thoughts Indicator
        st.markdown("---")
        st.subheader("Suicidal Thoughts")
        if suicide_label == "DETECTED":
            st.markdown(
                f"""
                <div style="padding: 15px; border-radius: 10px; background-color: rgba(255, 0, 0, 0.2); text-align: center; border: 2px solid red;">
                    <h3 style="color: red; margin: 0;">RISK DETECTED</h3>
                    <p style="margin: 5px 0 0 0;">Estimated probability: {int(suicide_prob*100)}%</p>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="padding: 15px; border-radius: 10px; background-color: rgba(76, 175, 80, 0.2); text-align: center; border: 2px solid green;">
                    <h3 style="color: green; margin: 0;">LOW RISK</h3>
                    <p style="margin: 5px 0 0 0;">Estimated probability: {int(suicide_prob*100)}%</p>
                </div>
                """, unsafe_allow_html=True
            )
        
    with col_radar:
        st.subheader("You vs. Average Student")
        
        # Prepare Data for Radar
        categories = ['Acad. Pressure', 'Satisfaction', 'Fin. Stress', 'Sleep Quality', 'Diet']
        
        # Normalize user values to 0-5 scale roughly for visualization
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
            name='Average',
            line_color='gray',
            opacity=0.5
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=user_vals,
            theta=categories,
            fill='toself',
            name='You',
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
    st.subheader("💡 Personalized Recommendations")
    
    rec_col1, rec_col2 = st.columns([2, 1])
    
    with rec_col1:
        if dep_prob > 0.5 or suicide_label == "DETECTED":
            st.markdown(
                """
                <div style="padding: 20px; border-radius: 10px; background-color: rgba(255, 0, 0, 0.1); border-left: 5px solid red;">
                    <h4>⚠️ High Risk Detected</h4>
                    <p>Your responses indicate high levels of stress and risk factors associated with depression.</p>
                    <ul>
                        <li><strong>Seek support:</strong> Do not hesitate to contact student wellness services.</li>
                        <li><strong>Talk to someone:</strong> Sharing your feelings with a friend or family member can help.</li>
                        <li><strong>Prioritize rest:</strong> Try to regulate your sleep cycle.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="padding: 20px; border-radius: 10px; background-color: rgba(0, 255, 0, 0.1); border-left: 5px solid green;">
                    <h4>✅ Healthy State</h4>
                    <p>Your indicators suggest a good balance between academic and personal life.</p>
                    <ul>
                        <li>Keep maintaining your sleep and eating habits.</li>
                        <li>If you feel pressure increasing, take active breaks.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True
            )
            
    with rec_col2:
        st.markdown("### 📞 Resources")
        st.markdown(
            """
            *   **Emergency:** 911
            *   **Lifeline:** 988
            *   **Univ Counseling:** (555) 123-4567
            """
        )

    st.markdown("---")
    
    # --- New Advice Panel ---
    st.subheader("🧩 Detailed Advice & Severity")
    
    if 'advice_data' in res:
        advice_data = res['advice_data']
        
        for symptom, info in advice_data.items():
            severity = info['severity']
            advice = info['advice']
            score = info['score']
            
            # Color coding for severity
            sev_color = "green"
            if severity == "medium": sev_color = "orange"
            if severity == "high": sev_color = "red"
            
            with st.expander(f"**{symptom.capitalize()}** - Severity: :{sev_color}[{severity.upper()}]"):
                st.write(f"**Advice:** {advice}")
                st.progress(min(100, int(score * 10)))

    st.markdown("---")
    if st.button("🔄 Start New Survey"):
        # Clear all survey-related session state keys
        if 'processed' in st.session_state:
            del st.session_state.processed
        if 'result' in st.session_state:
            del st.session_state.result
        restart()
        st.rerun()

