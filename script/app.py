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
    # Get the input data from the request as JSON
    data = request.get_json()

    # Convert the data to a pandas DataFrame
    data_df = pd.DataFrame([data])

    # Make predictions with the model
    prediction = model.predict(data_df)

    # Return the prediction as a JSON response
    if prediction[0] == 1:  # Assuming the model outputs 1 for "yes" and 0 for "no"
        return jsonify({'output': 'yes'})
    else:
        return jsonify({'output': 'no'})

if __name__ == "__main__":
    app.run(debug=True)
