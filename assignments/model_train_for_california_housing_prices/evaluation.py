#!/usr/bin/env python3
"""
evaluate.py - House Price Prediction Model Evaluator

This script loads a trained model and makes predictions on new test data.
Usage: python evaluate.py
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

def load_model(model_path='house_price_model.pkl'):
    """Load the trained model from pickle file"""
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print(f"✅ Model loaded successfully from {model_path}")
        return model
    except FileNotFoundError:
        print(f"❌ Error: Model file '{model_path}' not found!")
        print("Make sure you've saved your trained model as 'house_price_model.pkl'")
        return None
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return None

def load_and_preprocess_test_data(csv_path='test_data.csv'):
    """Load and preprocess the test data"""
    try:
        # Load test data
        test_df = pd.read_csv(csv_path)
        print(f"✅ Test data loaded: {test_df.shape[0]} rows, {test_df.shape[1]} columns")
        
        # Display basic info
        print(f"📊 Test data columns: {list(test_df.columns)}")
        
        # Check for missing values
        missing = test_df.isnull().sum().sum()
        if missing > 0:
            print(f"⚠️  Found {missing} missing values - filling with median...")
            test_df = test_df.fillna(test_df.median())
        
        return test_df
    
    except FileNotFoundError:
        print(f"❌ Error: Test data file '{csv_path}' not found!")
        return None
    except Exception as e:
        print(f"❌ Error loading test data: {str(e)}")
        return None

def preprocess_for_prediction(test_df):
    """Apply the same preprocessing as training data"""
    
    processed_df = test_df.copy()
    
    # 1. One-hot encode ocean_proximity if it exists
    if 'ocean_proximity' in processed_df.columns:
        print("🔄 Applying one-hot encoding to ocean_proximity...")
        processed_df = pd.get_dummies(processed_df, columns=['ocean_proximity'], 
                                    prefix='ocean_proximity', drop_first=True, dtype=int)
    
    # 2. Create derived features if possible
    if 'households' in processed_df.columns and 'total_rooms' in processed_df.columns:
        print("🔄 Creating derived features...")
        processed_df['rooms_per_household'] = processed_df['total_rooms'] / (processed_df['households'] + 1e-8)
        
    if 'households' in processed_df.columns and 'population' in processed_df.columns:
        processed_df['population_per_household'] = processed_df['population'] / (processed_df['households'] + 1e-8)
    
    if 'total_bedrooms' in processed_df.columns and 'total_rooms' in processed_df.columns:
        processed_df['bedrooms_per_room'] = processed_df['total_bedrooms'] / (processed_df['total_rooms'] + 1e-8)
    
    if 'median_income' in processed_df.columns and 'total_rooms' in processed_df.columns:
        processed_df['income_per_room'] = processed_df['median_income'] / (processed_df['total_rooms'] + 1e-8)
    
    # 3. Scale numerical features
    print("🔄 Scaling numerical features...")
    
    # Identify numerical columns (exclude dummy variables)
    numerical_cols = processed_df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Scale the features (Note: In production, you should save and load the scaler from training)
    scaler = StandardScaler()
    processed_df[numerical_cols] = scaler.fit_transform(processed_df[numerical_cols])
    
    return processed_df

def make_predictions(model, processed_data):
    """Make predictions using the loaded model"""
    try:
        predictions = model.predict(processed_data)
        print(f"✅ Predictions made successfully for {len(predictions)} samples")
        return predictions
    except Exception as e:
        print(f"❌ Error making predictions: {str(e)}")
        print("This might be due to feature mismatch between training and test data.")
        return None

def display_results(original_data, processed_data, predictions, top_n=10):
    """Display the prediction results"""
    
    # Create results dataframe
    results_df = pd.DataFrame()
    
    # Add some key original features for context
    if 'longitude' in original_data.columns:
        results_df['longitude'] = original_data['longitude']
    if 'latitude' in original_data.columns:
        results_df['latitude'] = original_data['latitude']
    if 'median_income' in original_data.columns:
        results_df['median_income'] = original_data['median_income']
    if 'ocean_proximity' in original_data.columns:
        results_df['ocean_proximity'] = original_data['ocean_proximity']
    
    # Add predictions
    results_df['predicted_house_value'] = predictions
    
    # Convert predictions back to more readable format (if they were standardized)
    # Note: These are still in standardized units
    results_df['predicted_house_value_formatted'] = results_df['predicted_house_value'].apply(
        lambda x: f"${x:.2f} (standardized)" if abs(x) < 10 else f"${x:.2f} (standardized)"
    )
    
    print("\n" + "="*80)
    print("🏠 HOUSE PRICE PREDICTIONS")
    print("="*80)
    
    print(f"\n📋 Showing top {top_n} predictions:")
    print("-" * 80)
    
    # Display results
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(results_df.head(top_n).to_string(index=True))
    
    # Summary statistics
    print("\n" + "="*80)
    print("📊 PREDICTION SUMMARY")
    print("="*80)
    print(f"Total predictions made: {len(predictions)}")
    print(f"Average predicted value: {np.mean(predictions):.4f} (standardized)")
    print(f"Min predicted value: {np.min(predictions):.4f} (standardized)")
    print(f"Max predicted value: {np.max(predictions):.4f} (standardized)")
    print(f"Standard deviation: {np.std(predictions):.4f}")
    
    # Save results
    results_df.to_csv('prediction_results.csv', index=False)
    print(f"\n💾 Results saved to 'prediction_results.csv'")

def main():
    """Main evaluation pipeline"""
    print("🚀 Starting House Price Model Evaluation")
    print("="*50)
    
    # Load model
    model = load_model('house_price_model.pkl')  # Change filename if needed
    if model is None:
        return
    
    # Load test data
    test_data = load_and_preprocess_test_data('test_data.csv')  # Change filename if needed
    if test_data is None:
        return
    
    # Preprocess test data
    print("\n🔧 Preprocessing test data...")
    processed_data = preprocess_for_prediction(test_data)
    
    print(f"✅ Processed data shape: {processed_data.shape}")
    print(f"📋 Final features: {list(processed_data.columns)}")
    
    # Make predictions
    print("\n🔮 Making predictions...")
    predictions = make_predictions(model, processed_data)
    if predictions is None:
        return
    
    # Display results
    display_results(test_data, processed_data, predictions, top_n=15)
    
    print("\n🎉 Evaluation completed successfully!")

if __name__ == "__main__":
    main()