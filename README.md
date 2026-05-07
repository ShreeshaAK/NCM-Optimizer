# NCM Battery Composition Optimizer

A full-stack machine learning web application that predicts and optimizes the performance of NCM (Nickel–Cobalt–Manganese) lithium-ion battery compositions.

Users adjust Ni, Co, and Mn percentages interactively — the app runs a trained Ridge Regression model and returns a predicted accuracy score compared against the NCM111 baseline (33.3 / 33.3 / 33.4).

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React.js, Recharts, Axios, React Router |
| Backend | Python, Flask, Flask-CORS |
| Machine Learning | scikit-learn (Ridge Regression), joblib, pandas |
| Database | MongoDB Atlas (pymongo) |
| Config | python-dotenv |

---

## Project Structure

```
NCM-Optimizer/
├── backend/
│   ├── server.py                        # Flask API — /predict and /retrain endpoints
│   ├── train_ridge.py                   # Trains Ridge model on 3 features, saves .pkl
│   ├── compare_models.py                # Evaluates multiple models by R² and RMSE
│   ├── generate_dummy_data.py           # Generates synthetic training dataset
│   ├── synthetic_ncm_dopant_dataset.csv # Training data (ni_pct, co_pct, mn_pct, predicted_accuracy)
│   ├── requirements.txt
│   └── .env                            # Not committed — see setup below
├── src/
│   ├── pages/
│   │   ├── Predict.jsx                  # Composition sliders + prediction UI
│   │   ├── Results.jsx                  # Model comparison graphs
│   │   └── Welcome.jsx                  # Landing page
│   └── components/
│       └── Navbar.jsx
└── package.json
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/ShreeshaAK/NCM-Optimizer.git
cd NCM-Optimizer
```

### 2. Backend setup
```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:
```
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```
Get your URI from MongoDB Atlas → Connect → Drivers → Python.

### 3. Train the model
```bash
cd backend
python generate_dummy_data.py   # creates synthetic_ncm_dopant_dataset.csv
python train_ridge.py           # trains model, saves ncm_ridge_model.pkl
```

### 4. Run the backend
```bash
cd backend
python server.py
# Flask starts at http://127.0.0.1:5000
```

### 5. Frontend setup
```bash
cd ..   # back to project root
npm install
npm start
# React starts at http://localhost:3000
```

---

## API Endpoints

### `POST /predict`
Accepts Ni, Co, Mn percentages (must sum to 100%) and returns model prediction.

**Request:**
```json
{ "ni": 60, "co": 20, "mn": 20 }
```

**Response:**
```json
{
  "accuracy": 72.45,
  "confidence": "BEST",
  "baseline": 68.12
}
```

**Edge case handled:** If `Ni + Co + Mn ≠ 100` (float tolerance ±0.01), the request is rejected before reaching the model with an informative error — preventing silent garbage predictions from Ridge Regression.

### `POST /retrain`
Fetches latest records from MongoDB Atlas `dataset_records` collection, retrains the Ridge model, and updates the in-memory model without restarting the server.

---

## ML Pipeline

1. `generate_dummy_data.py` — creates synthetic dataset with `ni_pct`, `co_pct`, `mn_pct`, `predicted_accuracy` columns
2. `train_ridge.py` — trains Ridge Regression on 3 features, evaluates by R² and RMSE, saves `ncm_ridge_model.pkl`
3. `compare_models.py` — compares multiple regression models to justify Ridge selection
4. `server.py` — loads model once at startup, serves predictions via REST API

---

## Key Engineering Decisions

**Why Ridge Regression?**
Compared multiple models using R² and RMSE — Ridge outperformed on the synthetic dataset with regularisation preventing overfitting on the small feature set.

**Why validate before inference?**
Ridge Regression has no concept of physical chemistry constraints. Without the 100% sum check, a user entering Ni=80, Co=70, Mn=60 would receive a confident but meaningless prediction. The validation layer catches this before any ML compute runs.

**Why load the model at startup?**
Loading `joblib` models per request adds ~200ms latency unnecessarily. Loading once into `global_model` at server init means every prediction request hits an already-warm model.

---

## Environment Variables

| Variable | Description |
|---|---|
| `MONGO_URI` | MongoDB Atlas connection string |
