from typing import List, Dict, Any
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error
import polars as pl
import os

class HousePricePredictor:
    def __init__(self, train_data_path: str, test_data_path: str):
        self.train_data = pl.read_csv(train_data_path)
        self.test_data = pl.read_csv(test_data_path)
        self.model_results = {}
        self.output_directory = 'src/real_estate_toolkit/ml_models/outputs/'
        os.makedirs(self.output_directory, exist_ok=True)

    def clean_data(self):
        # Assume handling missing values and correcting data types
        self.train_data = self.train_data.fill_missing(pl.median(self.train_data.select(pl.col('SalePrice'))))
        self.test_data = self.test_data.fill_missing(pl.median(self.test_data.select(pl.col('SalePrice'))))

    def prepare_features(self, target_column='SalePrice', selected_predictors=None):
        y = self.train_data.select(target_column)
        X = self.train_data.drop(target_column) if not selected_predictors else self.train_data.select(selected_predictors)
        
        numeric_features = X.select(pl.col('*').exclude(pl.Utf8)).columns
        categorical_features = X.select(pl.col('*').is_in(numeric_features).is_not()).columns

        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])

        X_preprocessed = preprocessor.fit_transform(X)

        return train_test_split(X_preprocessed, y, test_size=0.2, random_state=42)

    def train_baseline_models(self):
        X_train, X_test, y_train, y_test = self.prepare_features()
        models = {
            'Linear Regression': LinearRegression(),
            'RandomForestRegressor': RandomForestRegressor(n_estimators=100),
            'GradientBoostingRegressor': GradientBoostingRegressor()
        }

        for model_name, model in models.items():
            pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
            pipeline.fit(X_train, y_train)
            y_pred_train = pipeline.predict(X_train)
            y_pred_test = pipeline.predict(X_test)

            self.model_results[model_name] = {
                'metrics': {
                    'MSE': mean_squared_error(y_test, y_pred_test),
                    'MAE': mean_absolute_error(y_test, y_pred_test),
                    'R2': r2_score(y_test, y_pred_test),
                    'MAPE': mean_absolute_percentage_error(y_test, y_pred_test)
                },
                'model': model
            }

        return self.model_results

    def forecast_sales_price(self, model_type='LinearRegression'):
        # Load best model or specified model
        model = self.model_results[model_type]['model']
        X_test_preprocessed = self.prepare_features(self.test_data)
        predictions = model.predict(X_test_preprocessed)

        submission_df = pl.DataFrame({'Id': self.test_data['Id'], 'SalePrice': predictions})
        submission_df.write_csv(os.path.join(self.output_directory, 'submission.csv'))

