from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import random

app = Flask(__name__)

# Load the trained ML model from the pickle file
with open("model_Ss_best.pkl", "rb") as model_file:
    model = pickle.load(model_file)

def get_sensor_data():
    # Simulate heart rate within the range of 110 to 155 bpm
    simulated_heart_rate = random.uniform(110, 155)
    
    # Simulate SpO2 within the range of 0.80 to 0.92
    simulated_spo2 = random.uniform(0.80, 0.92)

    # Round values to one decimal place for heart rate and two decimal places for SpO2
    rounded_heart_rate = round(simulated_heart_rate, 1)
    rounded_spo2 = round(simulated_spo2, 2)

    return {'heart_rate': rounded_heart_rate, 'spo2': rounded_spo2}

@app.route('/')
def index():
    sensor_data = get_sensor_data()
    return render_template('indexs.html', sensor_data=sensor_data)

# Update the /predict route in app.py
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        age = float(data['age'])
        weight = float(data['weight'])
        sensor_data = get_sensor_data()

        # Create a pandas DataFrame from the input data
        data_df = pd.DataFrame({
            'Age_filtered': [age],
            'Weight (kg)_filtered': [weight],
            'Heart Rate_filtered': [sensor_data['heart_rate']],
            'SpO2_filtered': [sensor_data['spo2']]
        })

        # Make predictions with the model
        prediction = model.predict(data_df)

        # Update the HTML with the heart rate and SpO2 values
        return jsonify({
            'output': 'yes' if prediction[0] == 1 else 'no',
            'heart_rate': sensor_data['heart_rate'],
            'spo2': sensor_data['spo2']
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
