from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os

<<<<<<< HEAD
# Load .env relative to this file — works regardless of where you launch from
=======
from pathlib import Path
>>>>>>> 442513f08ac651e1e44529b1dab6b67333fcdb59
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["ncm_predictor"]
collection = db["predictions"]

app = Flask(__name__)
CORS(app)

# Load trained Ridge model once at startup (not per request)
global_model = joblib.load("ncm_ridge_model.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        ni = float(data['ni'])
        co = float(data['co'])
        mn = float(data['mn'])

        # Validate: percentages must sum to 100
        total = ni + co + mn
        if abs(total - 100) > 0.01:
            return jsonify({
                'error': f'Ni + Co + Mn must equal 100%. Received: {round(total, 2)}%'
            }), 400

        # Run inference using the trained Ridge model
        features = np.array([[ni, co, mn]])
        prediction = global_model.predict(features)[0]
        accuracy = max(0, min(100, round(float(prediction), 2)))

<<<<<<< HEAD
        # Baseline: equal NCM111 composition (33.3 / 33.3 / 33.4)
        baseline_pred = global_model.predict(np.array([[33.3, 33.3, 33.4]]))[0]
        baseline = max(0, min(100, round(float(baseline_pred), 2)))

        # Confidence: BEST if proposed composition outperforms baseline
        confidence = "BEST" if accuracy > baseline else "High"
=======
        
        baseline_pred = global_model.predict(np.array([[33.3, 33.3, 33.4]]))[0]
        baseline = max(0, min(100, round(float(baseline_pred), 2)))

        confidence = "Best" if accuracy > baseline else "High"
>>>>>>> 442513f08ac651e1e44529b1dab6b67333fcdb59

        # Persist prediction to MongoDB Atlas
        record = {
            "Ni": ni,
            "Co": co,
            "Mn": mn,
            "accuracy": accuracy,
            "confidence": confidence,
            "baseline": baseline
        }
        collection.insert_one(record)

        return jsonify({
            'accuracy': accuracy,
            'confidence': confidence,
            'baseline': baseline
        })

    except Exception as e:
        print("Prediction error:", e)
        return jsonify({'error': str(e)}), 500


@app.route('/retrain', methods=['POST'])
def retrain_model():
    try:
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import Ridge
        from sklearn.metrics import r2_score, mean_squared_error
        import pandas as pd

        # Fetch training data from MongoDB Atlas
        data = list(db["dataset_records"].find({}, {"_id": 0}))
        if not data:
            return jsonify({"error": "No dataset found in MongoDB"}), 400

        df = pd.DataFrame(data)

        # Column names must match synthetic_ncm_dopant_dataset.csv
        X = df[["ni_pct", "co_pct", "mn_pct"]]
        y = df["predicted_accuracy"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = Ridge(alpha=1.0)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        r2   = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        # Overwrite saved model and update in-memory reference
        joblib.dump(model, "ncm_ridge_model.pkl")
        global global_model
        global_model = model

        return jsonify({
            "message": "Model retrained successfully",
            "R2":   round(r2, 3),
            "RMSE": round(rmse, 3)
        })

    except Exception as e:
        print("Retraining error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)