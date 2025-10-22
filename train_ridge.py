import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import joblib

# Load data
df = pd.read_csv('synthetic_ncm_dopant_dataset.csv')
X = df[['ni_pct', 'co_pct', 'mn_pct', 'temp_C', 'c_rate']]
y = df['predicted_accuracy']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Ridge model
model = Ridge()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f'R² Score: {r2:.2f}')
print(f'RMSE: {rmse:.2f}')

# Save model
joblib.dump(model, 'ncm_ridge_model.pkl')
print('✅ Ridge model saved as ncm_ridge_model.pkl')
