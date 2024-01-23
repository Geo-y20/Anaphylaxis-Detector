from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load the trained ML model from the pickle file
with open("model_Ss_best.pkl", "rb") as model_file:
    model = pickle.load(model_file)

def get_sensor_data():
    # Simulate sensor data (replace this with your desired simulated values)
    simulated_heart_rate = 75.0
    simulated_spo2 = 98.0

    return {'heart_rate': simulated_heart_rate, 'spo2': simulated_spo2}

@app.route('/')
def index():
    sensor_data = get_sensor_data()
    return render_template('indexa.html', sensor_data=sensor_data)

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
