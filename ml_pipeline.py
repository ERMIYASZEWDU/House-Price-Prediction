"""Shared ML pipeline: feature engineering, outlier removal, and best models."""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

FEATURE_COLUMNS = [
    'area', 'bedrooms', 'bathrooms', 'stories', 'mainroad', 'guestroom',
    'basement', 'hotwaterheating', 'airconditioning', 'parking', 'prefarea',
    'furnishingstatus', 'total_rooms', 'bath_bed_ratio', 'has_amenities', 'premium_count',
]

CATEGORICAL_MAPPINGS = {
    'mainroad': {'yes': 1, 'no': 0},
    'guestroom': {'yes': 1, 'no': 0},
    'basement': {'yes': 1, 'no': 0},
    'hotwaterheating': {'yes': 1, 'no': 0},
    'airconditioning': {'yes': 1, 'no': 0},
    'prefarea': {'yes': 1, 'no': 0},
    'furnishingstatus': {'furnished': 2, 'semi-furnished': 1, 'unfurnished': 0},
}


def encode_categoricals(df):
    """Encode object columns using LabelEncoder or known mappings."""
    df = df.copy()
    for col, mapping in CATEGORICAL_MAPPINGS.items():
        if col in df.columns and df[col].dtype == object:
            df[col] = df[col].map(mapping)
    for col in df.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
    return df


def engineer_features(df):
    """Add derived features used by the best models."""
    df = df.copy()
    if 'price' in df.columns:
        df['price_per_sqft'] = df['price'] / df['area']
    df['total_rooms'] = df['bedrooms'] + df['bathrooms']
    df['bath_bed_ratio'] = df['bathrooms'] / (df['bedrooms'] + 1)
    df['has_amenities'] = (
        (df['guestroom'] == 1) |
        (df['basement'] == 1) |
        (df['airconditioning'] == 1)
    ).astype(int)
    df['premium_count'] = (
        df['guestroom'] + df['basement'] +
        df['airconditioning'] + df['hotwaterheating']
    )
    return df


def remove_outliers(df):
    """Remove price outliers using IQR."""
    Q1 = df['price'].quantile(0.25)
    Q3 = df['price'].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return df[(df['price'] >= lower) & (df['price'] <= upper)].copy()


def prepare_dataset(csv_path='Housing.csv'):
    """Load CSV and return raw df plus cleaned feature matrix."""
    df = pd.read_csv(csv_path)
    df_processed = encode_categoricals(df)
    df_processed = engineer_features(df_processed)
    df_clean = remove_outliers(df_processed)
    X = df_clean.drop(['price', 'price_per_sqft'], axis=1)
    y = df_clean['price']
    return df, df_clean, X, y


def build_feature_row(
    area, bedrooms, bathrooms, stories,
    mainroad, guestroom, basement, hotwaterheating,
    airconditioning, parking, prefarea, furnishingstatus,
):
    """Build a single-row feature DataFrame for prediction."""
    row = {
        'area': area,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'stories': stories,
        'mainroad': mainroad,
        'guestroom': guestroom,
        'basement': basement,
        'hotwaterheating': hotwaterheating,
        'airconditioning': airconditioning,
        'parking': parking,
        'prefarea': prefarea,
        'furnishingstatus': furnishingstatus,
    }
    df = pd.DataFrame([row])
    df = engineer_features(df)
    return df[FEATURE_COLUMNS]


def _evaluate(model, X_train, X_test, y_train, y_test, name):
    pred = model.predict(X_test)
    return {
        'model': model,
        'name': name,
        'r2': r2_score(y_test, pred),
        'mae': mean_absolute_error(y_test, pred),
        'rmse': np.sqrt(mean_squared_error(y_test, pred)),
        'predictions': pred,
        'actual': y_test,
    }


def train_all_models(csv_path='Housing.csv', test_size=0.2, random_state=42):
    """Train Enhanced Linear, Random Forest, and Gradient Boosting; return best."""
    df_raw, df_clean, X, y = prepare_dataset(csv_path)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    candidates = [
        ('Enhanced Linear', LinearRegression()),
        ('Random Forest', RandomForestRegressor(
            n_estimators=100, max_depth=15, min_samples_split=5,
            random_state=random_state, n_jobs=-1,
        )),
        ('Gradient Boosting', GradientBoostingRegressor(
            n_estimators=100, learning_rate=0.1, max_depth=5,
            random_state=random_state,
        )),
    ]

    results = {}
    for name, model in candidates:
        model.fit(X_train, y_train)
        results[name] = _evaluate(model, X_train, X_test, y_train, y_test, name)

    best_name = max(results, key=lambda k: results[k]['r2'])
    return {
        'df_raw': df_raw,
        'df_clean': df_clean,
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'results': results,
        'best_model': results[best_name]['model'],
        'best_name': best_name,
        'best_score': results[best_name]['r2'],
    }
