print("Python works!")

from flask import Flask
print("Flask imported successfully!")

app = Flask(__name__)
print("Flask app created!")

@app.route('/')
def home():
    return "Hello!"

print("Starting server...")
app.run(debug=True, port=5000)
