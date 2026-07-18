"""Train the best model and save it for deployment."""

import os
import joblib
from ml_pipeline import train_all_models, FEATURE_COLUMNS

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'best_model.joblib')


def main():
    os.makedirs(MODEL_DIR, exist_ok=True)
    pipeline = train_all_models()

    artifact = {
        'model': pipeline['best_model'],
        'model_name': pipeline['best_name'],
        'r2_score': pipeline['best_score'],
        'feature_columns': FEATURE_COLUMNS,
        'results': {
            name: {'r2': r['r2'], 'mae': r['mae'], 'rmse': r['rmse']}
            for name, r in pipeline['results'].items()
        },
    }
    joblib.dump(artifact, MODEL_PATH)

    print(f"Saved {pipeline['best_name']} (R²={pipeline['best_score']:.4f}) to {MODEL_PATH}")
    for name, metrics in artifact['results'].items():
        print(f"  {name}: R2={metrics['r2']:.4f}, MAE={metrics['mae']:,.0f}")


if __name__ == '__main__':
    main()
