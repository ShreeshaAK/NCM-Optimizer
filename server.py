
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# Load trained model
model = joblib.load("ncm_ridge_model.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        ni = float(data['ni'])
        co = float(data['co'])
        mn = float(data['mn'])

        # ✅ Check sum
        total = ni + co + mn
        if abs(total - 100) > 0.01:
            return jsonify({'error': 'Total must be 100%'}), 400

        # Dummy prediction (replace with your trained model later)
        prediction = 60 + (ni * 0.1) - (co * 0.05) + (mn * 0.08)
        accuracy = max(0, min(100, prediction))  # keep within [0,100]

        # Baseline (1:1:1 = 33.33 each)
        baseline_pred = 60 + (33.3 * 0.1) - (33.3 * 0.05) + (33.3 * 0.08)
        baseline = max(0, min(100, baseline_pred))

        confidence = "High" if accuracy > baseline else "Moderate"

        return jsonify({
            'accuracy': round(accuracy, 2),
            'confidence': confidence,
            'baseline': round(baseline, 2)
        })
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
