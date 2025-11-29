from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# ADVICE by symptom and severity
ADVICE = {
    "sleep": {
        "low": "Your sleep looks good! Keep maintaining healthy sleep habits.",
        "medium": "Try going to bed at the same time each night. Create a bedtime routine. Avoid screens 1 hour before bed.",
        "high": "Talk to a doctor about your sleep problems. Try avoiding screens before bed. Keep a sleep diary to identify patterns."
    },
    "social": {
        "low": "You have good social connections! Keep nurturing your relationships.",
        "medium": "Try texting or calling one friend this week. Small steps count! Consider joining a group activity.",
        "high": "It's okay to start small. Even a short text to someone can help. Consider joining an online community related to your interests."
    },
    "energy": {
        "low": "Your energy levels are good! Keep up your healthy habits.",
        "medium": "Try a short 10-minute walk each day. Make sure you're eating regular, nutritious meals throughout the day.",
        "high": "Take breaks and rest when needed. Consider seeing a doctor to rule out physical causes. Try light exercise if possible."
    },
    "mood": {
        "low": "Your mood seems stable! Continue with your current self-care practices.",
        "medium": "Try doing one thing you enjoy each day. Stay connected with friends and family. Practice stress management.",
        "high": "Please talk to someone - a counselor, doctor, or trusted adult. Call 988 for immediate support. You don't have to face this alone."
    },
    "concentration": {
        "low": "Your focus and concentration seem strong!",
        "medium": "Try the Pomodoro Technique - 25 minutes of focus, 5-minute breaks. Minimize distractions in your workspace.",
        "high": "Break tasks into smaller chunks. Use lists and reminders. Ensure you're getting adequate sleep - it affects concentration."
    },
    "appetite": {
        "low": "Your eating patterns appear healthy and stable.",
        "medium": "Try to maintain regular meal times. Keep healthy snacks available. Notice if emotions affect your eating.",
        "high": "Set reminders to eat at regular times. Choose nutrient-dense foods. Consider speaking with a nutritionist or doctor."
    },
    "stress": {
        "low": "Your stress levels seem manageable!",
        "medium": "Practice deep breathing exercises. Take short breaks during the day. Try light physical activity.",
        "high": "Talk to a counselor about stress management techniques. Practice relaxation exercises. Consider what stressors you can reduce."
    },
    "anxiety": {
        "low": "Your anxiety levels appear manageable.",
        "medium": "Practice grounding techniques (5-4-3-2-1 method). Try journaling about your worries. Stay connected with supportive people.",
        "high": "Please speak with a mental health professional. Try breathing exercises (4-7-8 technique). Call 988 if you need immediate support."
    }
}

# Calculate severity level
def get_severity_level(score):
   
    if score <= 3:
        return "low"
    elif score <= 6:
        return "medium"
    else:
        return "high"

# help function (generate advice for one symptom)

def generate_advice_for_symptom(symptom_name, score):
    
    severity = get_severity_level(score)
    
    # Get advice from database
    if symptom_name in ADVICE:
        advice_text = ADVICE[symptom_name][severity]
    else:
        advice_text = "Please consult with a healthcare professional for personalized guidance."
    
    return {
        "score": score,
        "severity": severity,
        "advice": advice_text
    }

# Calculate overall risk
def calculate_overall_risk(scores):
    
    # Calculate average of all scores
    score_values = [score for score in scores.values() if score is not None]
    
    if not score_values:
        return "Unknown", 0
    
    avg_score = sum(score_values) / len(score_values)
    
    # Determine risk level
    if avg_score <= 3:
        risk = "Low Risk"
    elif avg_score <= 6:
        risk = "Moderate Risk"
    else:
        risk = "High Risk"
    
    return risk, round(avg_score, 1)

# door1: HOME PAGE
@app.route('/')
def home():
    return jsonify({
        "message": "Mental Health Advice API is running!",s
        "status": "active",
        "endpoints": {
            "home": "/",
            "get_advice": "/advice (POST)",
            "available_symptoms": "/symptoms (GET)"
        }
    })


#  door 2 get advice (main endpoint)

@app.route('/advice', methods=['POST'])
def get_advice():
    
    try:
        # get survey data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No data provided"
            }), 400
        
        # proces each symptom and generate advice
        symptoms_with_advice = {}
        scores = {}
        
        for symptom, score in data.items():
            if symptom in ADVICE:  # Only process known symptoms
                symptoms_with_advice[symptom] = generate_advice_for_symptom(symptom, score)
                scores[symptom] = score
        
        # calculate overall risk
        overall_risk, avg_score = calculate_overall_risk(scores)
        
        # build response
        response = {
            "status": "success",
            "overall_assessment": {
                "risk_level": overall_risk,
                "average_score": avg_score
            },
            "symptoms": symptoms_with_advice,
            "help_resources": [
                {
                    "name": "988 Suicide & Crisis Lifeline",
                    "contact": "Call or text 988",
                    "availability": "24/7",
                    "description": "Free and confidential support"
                },
                {
                    "name": "Crisis Text Line",
                    "contact": "Text HOME to 741741",
                    "availability": "24/7",
                    "description": "Text-based crisis support"
                },
                {
                    "name": "SAMHSA National Helpline",
                    "contact": "1-800-662-4357",
                    "availability": "24/7",
                    "description": "Treatment referral and information"
                }
            ],
            "disclaimer": "This is an educational tool only and not a substitute for professional medical advice, diagnosis, or treatment. If you're experiencing mental health concerns, please consult a qualified healthcare provider."
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500

# door 3 get avable symptoms
@app.route('/symptoms', methods=['GET'])
def get_symptoms():
    
    return jsonify({
        "status": "success",
        "available_symptoms": list(ADVICE.keys()),
        "score_range": "0-10 (0=no problem, 10=severe problem)"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
