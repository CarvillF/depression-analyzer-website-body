# Early identification of distress signals for students for the promotion of mental health using classification of forests

## Project overview and purpose 
Mental health challenges amoung students are incresing especially stress and anxiety. Many people do not seek help early because limited counseling resources.  

We propose an AI-powered early warning system that analyzes anonymous student data. Using machine learning classification models and sentiment analysis, the system can flag early signs of distress and provide resources for the user.

The ethical implications of following the Al predictions in delicate areas like medicine, and who to blame when something goes wrong. Student data must be anonymized, and participation must be voluntary. AI should never analyze private messages or data without explicit permission.
 
## External links
Video demo: https://youtu.be/kceowfLu7RA  
Hosted website: https://mental-health-checker.streamlit.app/

## Installation and setup instructions 

### How to develop the frontend
1. In the folder `website_carlos`, create a virtual environment and activate it. Commands: `py -m venv .venv` and `py .venv\Scripts\Activate.ps1` (in Vscode terminal).
2. Install the requirements. Commands: `py -m pip install -r requirements.txt`.
3. Run the app.py file. Commands: `py app.py`.

### How to run the model and reproduce results 
Please refer to `/docs/ML docs/README.md` for detailed instructions on running the machine learning models.

## Technologies or libraries used
gradio  
matplotlib  
numpy  
os  
pandas  
pickle  
plotly  
scikit-learn    
streamlit  
subprocess  
sys  

## Author(s) and contribution summary

#### Carlos Vladimir Flores Villacís
Developed and integrated the front end of the application. Refactored code to align with VGC standards and hosted website on streamlit.  

#### Esin Karapinar
Developed the customized advice module based on user inputs. Assisted Carlos with code functions.  

#### Grace Marrone
Developed the machine learning algorithm to make predictions based on user input. Assisted Carlos with code functions.  
