from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load the trained ML model from the pickle file
with open("model_Ss_best.pkl", "rb") as model_file:
    model = pickle.load(model_file)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        age = float(data['age'])
        weight = float(data['weight'])
        heart_rate = float(data['heart_rate'])
        spo2 = float(data['spo2'])

        # Create a pandas DataFrame from the input data
        data_df = pd.DataFrame({'Age_filtered': [age],
                                'Weight (kg)_filtered': [weight],
                                'Heart Rate_filtered': [heart_rate],
                                'SpO2_filtered': [spo2]})

        # Make predictions with the model
        prediction = model.predict(data_df)

        # Return the prediction as a JSON response
        if prediction[0] == 1:
            return jsonify({'output': 'yes'})
        else:
            return jsonify({'output': 'no'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
