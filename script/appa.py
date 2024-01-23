from flask import Flask, render_template, request, jsonify
import pickle
import serial
import pandas as pd

app = Flask(__name__)
serialcom = serial.Serial('COM8', 9600)
serialcom.timeout = 1

# Load the trained ML model from the pickle file
with open("model_Ss_best.pkl", "rb") as model_file:
    model = pickle.load(model_file)

def send_command(command):
    serialcom.write(command.encode())  # Send command to Arduino

def get_sensor_data():
    try:
        data = serialcom.readline().decode().strip()
        print("Raw Sensor Data:", data)  # Print raw data for verification

        # Assuming the sensor data is in the format "heart_rate,spo2"
        readings = data.split(',')
        if len(readings) == 2:
            heart_rate = float(readings[0])
            spo2 = float(readings[1])
            print("Heart Rate:", heart_rate)
            print("SpO2:", spo2)
            return {'heart_rate': heart_rate, 'spo2': spo2}
        else:
            return {'error': 'Invalid sensor data format'}
    except serial.SerialException as e:
        print("Serial communication error:", e)
        return {'error': 'Sensor data not available'}

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