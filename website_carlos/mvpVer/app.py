import gradio as gr
import sys
import os

# Add ml_grace directory to path to import model utilities
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ml_grace')))
from model_utils import predict_both

def analyze_risk(
    gender, age, academic_pressure, study_satisfaction, 
    study_hours, sleep_duration, dietary_habits, 
    family_history, financial_stress
):
    """
    Use trained ML models to predict depression and suicidal thoughts risk.
    """
    try:
        # Get predictions from ML models
        predictions = predict_both(
            gender=gender,
            age=age,
            academic_pressure=academic_pressure,
            study_satisfaction=study_satisfaction,
            sleep_duration=sleep_duration,
            dietary_habits=dietary_habits,
            study_hours=study_hours,
            financial_stress=financial_stress,
            family_history=family_history
        )
        
        # Format depression result
        dep_prob = predictions['depression_probability']
        if dep_prob >= 0.65:
            dep_result = f"Depression Risk: HIGH ({dep_prob:.1%})"
        elif dep_prob >= 0.35:
            dep_result = f"Depression Risk: MODERATE ({dep_prob:.1%})"
        else:
            dep_result = f"Depression Risk: LOW ({dep_prob:.1%})"
        
        # Format suicidal thoughts result
        sui_prob = predictions['suicidal_probability']
        if sui_prob >= 0.5:
            suicide_result = f"Suicidal Thoughts Risk: DETECTED ({sui_prob:.1%})"
        else:
            suicide_result = f"Suicidal Thoughts Risk: LOW ({sui_prob:.1%})"
        
        # Combine results
        final_text = f"{dep_result}\n{suicide_result}"
        
    except Exception as e:
        final_text = f"Error: Unable to process prediction. {str(e)}"

    # Resources Text
    resources_md = """
    ### Help Resources
    
    If you feel overwhelmed, please seek professional help.
    
    *   **Suicide Prevention Lifeline:** 988 (USA) / [Your local number]
    *   **Student Health Services:** Contact your university counseling center.
    *   **Emergency:** Call 911 or go to the nearest hospital.
    """
    
    return final_text, resources_md


# UI Layout
with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Early Identification of Distress Signals
        
        **Disclaimer:** This tool is an academic prototype demonstration. It is **NOT** a real medical diagnosis.
        
        Please complete the following survey to analyze risk factors.
        """
    )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Demographics")
            gender = gr.Radio(["Male", "Female"], label="Gender")
            age = gr.Slider(18, 30, step=1, label="Age")
            
            gr.Markdown("### Academic Factors")
            academic_pressure = gr.Slider(1, 5, step=1, label="Academic Pressure (1-5)")
            study_satisfaction = gr.Slider(1, 5, step=1, label="Study Satisfaction (1-5)")
            study_hours = gr.Number(label="Study Hours per day (Avg)")
            
        with gr.Column():
            gr.Markdown("### Health & Lifestyle")
            sleep_duration = gr.Dropdown(
                ["Less than 5 hours", "5-6 hours", "7-8 hours", "More than 8 hours"], 
                label="Sleep Duration"
            )
            dietary_habits = gr.Dropdown(
                ["Healthy", "Moderate", "Unhealthy"], 
                label="Dietary Habits"
            )
            family_history = gr.Radio(["Yes", "No"], label="Family History of Mental Illness")
            financial_stress = gr.Slider(1, 5, step=1, label="Financial Stress (1-5)")
            
    analyze_btn = gr.Button("Analyze Risk", variant="primary", size="lg")
    
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column():
            result_label = gr.Label(label="Analysis Results")
            resources_output = gr.Markdown(label="Resources")

            
    analyze_btn.click(
        fn=analyze_risk,
        inputs=[
            gender, age, academic_pressure, study_satisfaction, 
            study_hours, sleep_duration, dietary_habits, 
            family_history, financial_stress
        ],
        outputs=[result_label, resources_output]
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Default(primary_hue="red", secondary_hue="pink"), share=True)
