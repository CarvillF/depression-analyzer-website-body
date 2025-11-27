import gradio as gr
import random
import matplotlib.pyplot as plt
import pandas as pd

def analyze_risk(
    gender, age, academic_pressure, study_satisfaction, cgpa, 
    work_study_hours, sleep_duration, dietary_habits, suicidal_thoughts, 
    family_history, financial_stress
):
    """
    Mock backend logic to simulate risk analysis.
    """
    risk_score = 0
    if academic_pressure > 3:
        risk_score += 1
    if study_satisfaction < 3:
        risk_score += 1
    if sleep_duration in ["Less than 5 hours", "5-6 hours"]:
        risk_score += 1
    if suicidal_thoughts == "Yes":
        risk_score += 2
    if family_history == "Yes":
        risk_score += 1
    if financial_stress > 3:
        risk_score += 1
        
    is_depressed = risk_score >= 3
    
    result_text = "Riesgo Detectado" if is_depressed else "Sin Riesgo Aparente"
    
    # Mock Insights Chart
    # Simulating "Your Academic Pressure vs Average"
    fig = plt.figure(figsize=(6, 4))
    categories = ['Tu Presión', 'Promedio Estudiantes']
    values = [academic_pressure, 3.5] # 3.5 is a mock average
    colors = ['#ff6b6b', '#4ecdc4']
    
    plt.bar(categories, values, color=colors)
    plt.ylim(0, 5)
    plt.ylabel('Nivel de Presión (1-5)')
    plt.title('Comparativa de Presión Académica')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Resources Text
    resources_md = """
    ### Recursos de Ayuda
    
    Si te sientes abrumado, por favor busca ayuda profesional.
    
    *   **Línea de Prevención del Suicidio:** 988 (EE.UU.) / [Tu número local]
    *   **Servicios de Salud Estudiantil:** Contacta a la consejería de tu universidad.
    *   **Urgencias:** Llama al 911 o acude al hospital más cercano.
    """
    
    return result_text, fig, resources_md

# UI Layout
# Note: Removed theme=gr.themes.Soft() due to compatibility issue with installed Gradio version.
with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Early Identification of Distress Signals
        
        **Disclaimer:** Esta herramienta es un prototipo académico demostrativo. **NO** es un diagnóstico médico real.
        
        Por favor, completa la siguiente encuesta para analizar los factores de riesgo.
        """
    )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Datos Demográficos")
            gender = gr.Radio(["Male", "Female"], label="Gender")
            age = gr.Slider(18, 30, step=1, label="Age")
            
            gr.Markdown("### Factores Académicos")
            academic_pressure = gr.Slider(1, 5, step=1, label="Academic Pressure (1-5)")
            study_satisfaction = gr.Slider(1, 5, step=1, label="Study Satisfaction (1-5)")
            cgpa = gr.Number(label="CGPA / Grades")
            work_study_hours = gr.Number(label="Work/Study Hours per day")
            
        with gr.Column():
            gr.Markdown("### Salud y Estilo de Vida")
            sleep_duration = gr.Dropdown(
                ["Less than 5 hours", "5-6 hours", "7-8 hours", "More than 8 hours"], 
                label="Sleep Duration"
            )
            dietary_habits = gr.Dropdown(
                ["Healthy", "Moderate", "Unhealthy"], 
                label="Dietary Habits"
            )
            suicidal_thoughts = gr.Radio(["Yes", "No"], label="Have you ever had suicidal thoughts?")
            family_history = gr.Radio(["Yes", "No"], label="Family History of Mental Illness")
            financial_stress = gr.Slider(1, 5, step=1, label="Financial Stress (1-5)")
            
    analyze_btn = gr.Button("Analizar Riesgo", variant="primary", size="lg")
    
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column():
            result_label = gr.Label(label="Resultado del Análisis")
            resources_output = gr.Markdown(label="Recursos")
        with gr.Column():
            chart_output = gr.Plot(label="Insights")
            
    analyze_btn.click(
        fn=analyze_risk,
        inputs=[
            gender, age, academic_pressure, study_satisfaction, cgpa, 
            work_study_hours, sleep_duration, dietary_habits, suicidal_thoughts, 
            family_history, financial_stress
        ],
        outputs=[result_label, chart_output, resources_output]
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Default(primary_hue="red", secondary_hue="pink"), share=True)
