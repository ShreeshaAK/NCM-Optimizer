import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import joblib

# Load dataset
df = pd.read_csv('synthetic_ncm_dopant_dataset.csv')

# Features and label
X = df[['ni_pct', 'co_pct', 'mn_pct', 'temp_C', 'c_rate']]
y = df['predicted_accuracy']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))



print(f'R² Score: {r2:.2f}')
print(f'RMSE: {rmse:.2f}')

# Save model
joblib.dump(model, 'ncm_rf_model.pkl')
print('✅ Model saved as ncm_rf_model.pkl')
