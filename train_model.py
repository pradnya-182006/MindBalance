import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load data
try:
    df = pd.read_csv('social_media_addiction_data.csv')
except Exception as e:
    print("❌ ERROR: Could not load 'social_media_addiction_data.csv'.")
    print("Please make sure the file exists in the same directory as this script.")
    exit(1)

# Define features and target
# We'll predict 'Status' (High Risk vs Low Risk)
X = df.drop(['Status', 'Addicted_Score'], axis=1)
y = df['Status']

# Identify categorical and numerical columns
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
numerical_cols = X.select_dtypes(exclude=['object']).columns.tolist()

# Preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ])

# XGBoost model
model = XGBClassifier(eval_metric='logloss', random_state=42)

# Pipeline
clf_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', model)
])

# Hyperparameter tuning
param_dist = {
    'model__n_estimators': [100, 200, 300],
    'model__max_depth': [3, 5, 7, 10],
    'model__learning_rate': [0.01, 0.05, 0.1, 0.2],
    'model__subsample': [0.6, 0.8, 1.0],
    'model__colsample_bytree': [0.6, 0.8, 1.0]
}

print("Starting fine-tuning...")
random_search = RandomizedSearchCV(
    clf_pipeline, param_distributions=param_dist, 
    n_iter=20, cv=5, scoring='accuracy', n_jobs=-1, verbose=1, random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

random_search.fit(X_train, y_train)

# Best model
best_model = random_search.best_estimator_
y_pred = best_model.predict(X_test)

print(f"Best Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("Best Params:", random_search.best_params_)
print(classification_report(y_test, y_pred))

# Save the best model
with open('best_model.pkl', 'wb') as f:
    pickle.dump(best_model, f)

# Save feature info
with open('features.pkl', 'wb') as f:
    pickle.dump({'numerical': numerical_cols, 'categorical': categorical_cols}, f)

print("Model and features saved successfully!")
