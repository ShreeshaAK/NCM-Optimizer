
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["ncm_predictor"]  # database name
collection = db["predictions"]  # collection name


app = Flask(__name__)
CORS(app)

# Load trained model
global_model = joblib.load("ncm_ridge_model.pkl")


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        ni = float(data['ni'])
        co = float(data['co'])
        mn = float(data['mn'])

        
        total = ni + co + mn
        if abs(total - 100) > 0.01:
            return jsonify({'error': 'Total must be 100%'}), 400

        
        prediction = 60 + (ni * 0.1) - (co * 0.05) + (mn * 0.08)
        accuracy = max(0, min(100, prediction))  # keep within [0,100]

        
        baseline_pred = 60 + (33.3 * 0.1) - (33.3 * 0.05) + (33.3 * 0.08)
        baseline = max(0, min(100, baseline_pred))

        confidence = "High" if accuracy > baseline else "BEST"

        
        record = {
            "Ni": ni,
            "Co": co,
            "Mn": mn,
            "accuracy": round(accuracy, 2),
            "confidence": confidence,
            "baseline": round(baseline, 2)
        }

        
        collection.insert_one(record)

        
        return jsonify({
            'accuracy': round(accuracy, 2),
            'confidence': confidence,
            'baseline': round(baseline, 2)
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/retrain', methods=['POST'])
def retrain_model():
    try:
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import Ridge
        from sklearn.metrics import r2_score, mean_squared_error
        import numpy as np
        import pandas as pd
        import joblib

        # Fetch data from MongoDB
        data = list(db["dataset_records"].find({}, {"_id": 0}))
        if not data:
            return jsonify({"error": "No dataset found in MongoDB"}), 400

        df = pd.DataFrame(data)

        # ensure correct column names (adjust to match your dataset)
        X = df[["Ni", "Co", "Mn"]]
        y = df["Performance"]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        model = Ridge(alpha=1.0)
        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        # Save model
        joblib.dump(model, "ncm_ridge_model.pkl")

        # Update global model variable
        global global_model
        global_model = model

        # Return metrics
        return jsonify({
            "message": " Model retrained successfully!",
            "R2": round(r2, 3),
            "RMSE": round(rmse, 3)
        })

    except Exception as e:
        print("Retraining error:", e)
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)


