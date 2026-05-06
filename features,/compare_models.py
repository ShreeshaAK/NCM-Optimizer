# compare_models_with_plot.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

from xgboost import XGBRegressor 

import warnings
warnings.filterwarnings("ignore")

# Load dataset
df = pd.read_csv("synthetic_ncm_dopant_dataset.csv")
X = df[["ni_pct", "co_pct", "mn_pct", "temp_C", "c_rate"]]
y = df["predicted_accuracy"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Models
models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(),
    "Decision Tree": DecisionTreeRegressor(),
    "Random Forest": RandomForestRegressor(),
    "Gradient Boosting": GradientBoostingRegressor(),
    "XGBoost": XGBRegressor(), 
    "SVR": SVR(),
    "KNN Regressor": KNeighborsRegressor()
}

results = []

# Evaluate each model
for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    r2 = r2_score(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    results.append({"Model": name, "R2": r2, "RMSE": rmse})

# Convert to DataFrame
results_df = pd.DataFrame(results)

# --- Plot R² ---
sns.set(style="whitegrid")
plt.figure(figsize=(10, 5))
sns.barplot(data=results_df, x="Model", y="R2", palette="Blues_d")
plt.title("Model Comparison: R² Score")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("r2_comparison.png")
plt.show()

# --- Plot RMSE ---
plt.figure(figsize=(10, 5))
sns.barplot(data=results_df, x="Model", y="RMSE", palette="Reds_d")
plt.title("Model Comparison: RMSE")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("rmse_comparison.png")
plt.show()

