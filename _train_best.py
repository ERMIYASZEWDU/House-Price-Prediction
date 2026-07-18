import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

df = pd.read_csv('Housing.csv')
df_processed = df.copy()
for col in df_processed.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    df_processed[col] = le.fit_transform(df_processed[col])

df_processed['price_per_sqft'] = df_processed['price'] / df_processed['area']
df_processed['total_rooms'] = df_processed['bedrooms'] + df_processed['bathrooms']
df_processed['bath_bed_ratio'] = df_processed['bathrooms'] / (df_processed['bedrooms'] + 1)
df_processed['has_amenities'] = (
    (df_processed['guestroom'] == 1) |
    (df_processed['basement'] == 1) |
    (df_processed['airconditioning'] == 1)
).astype(int)
df_processed['premium_count'] = (
    df_processed['guestroom'] +
    df_processed['basement'] +
    df_processed['airconditioning'] +
    df_processed['hotwaterheating']
)

Q1 = df_processed['price'].quantile(0.25)
Q3 = df_processed['price'].quantile(0.75)
IQR = Q3 - Q1
df_clean = df_processed[
    (df_processed['price'] >= Q1 - 1.5 * IQR) &
    (df_processed['price'] <= Q3 + 1.5 * IQR)
].copy()

X = df_clean.drop(['price', 'price_per_sqft'], axis=1)
y = df_clean['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

results = []
for name, model in [
    ('Enhanced Linear', LinearRegression()),
    ('Random Forest', RandomForestRegressor(n_estimators=100, max_depth=15, min_samples_split=5, random_state=42, n_jobs=-1)),
    ('Gradient Boosting', GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)),
]:
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    results.append((name, r2_score(y_test, pred), mean_absolute_error(y_test, pred), np.sqrt(mean_squared_error(y_test, pred))))

for r in results:
    print(f"{r[0]}: R2={r[1]:.4f}, MAE={r[2]:,.0f}, RMSE={r[3]:,.0f}")

best = max(results, key=lambda x: x[1])
print(f"BEST: {best[0]} R2={best[1]:.4f}")
print("FEATURES:", list(X.columns))
