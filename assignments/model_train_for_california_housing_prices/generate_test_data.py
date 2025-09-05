#!/usr/bin/env python3
"""
generate_test_data.py - Generate sample test data for model evaluation

This script creates a CSV file with 50 sample rows of housing data for testing.
The data mimics California housing dataset structure but WITHOUT the target variable.
"""

import pandas as pd
import numpy as np

def generate_test_data(n_samples=50):
    """Generate realistic test data for California housing prediction"""
    
    np.random.seed(42)  # For reproducible results
    
    # Generate realistic California housing data
    data = {
        # Geographic coordinates (California range)
        'longitude': np.random.uniform(-124.35, -114.31, n_samples),
        'latitude': np.random.uniform(32.54, 41.95, n_samples),
        
        # Housing characteristics
        'housing_median_age': np.random.randint(1, 53, n_samples),
        'total_rooms': np.random.randint(100, 8000, n_samples),
        'total_bedrooms': None,  # Will calculate based on total_rooms
        'population': np.random.randint(50, 4000, n_samples),
        'households': None,  # Will calculate based on population
        'median_income': np.random.uniform(0.5, 15.0, n_samples),
        
        # Ocean proximity (categorical)
        'ocean_proximity': np.random.choice([
            'INLAND', 'NEAR BAY', '<1H OCEAN', 'ISLAND', 'NEAR OCEAN'
        ], n_samples, p=[0.4, 0.2, 0.2, 0.05, 0.15])  # Realistic distribution
    }
    
    # Create derived realistic values
    # Households typically 2-4 people per household
    data['households'] = (data['population'] / np.random.uniform(2.0, 4.5, n_samples)).astype(int)
    data['households'] = np.maximum(data['households'], 1)  # At least 1 household
    
    # Bedrooms typically 20-30% of total rooms
    bedroom_ratio = np.random.uniform(0.15, 0.35, n_samples)
    data['total_bedrooms'] = (data['total_rooms'] * bedroom_ratio).astype(int)
    data['total_bedrooms'] = np.maximum(data['total_bedrooms'], 1)  # At least 1 bedroom
    
    # Create DataFrame
    test_df = pd.DataFrame(data)
    
    # Add some realistic constraints
    # Ensure households don't exceed population
    test_df['households'] = np.minimum(test_df['households'], test_df['population'])
    
    # Ensure bedrooms don't exceed rooms
    test_df['total_bedrooms'] = np.minimum(test_df['total_bedrooms'], test_df['total_rooms'])
    
    return test_df

def add_sample_descriptions(test_df):
    """Add a description column to make results more interpretable"""
    descriptions = []
    
    for idx, row in test_df.iterrows():
        # Create a simple description based on the data
        if row['ocean_proximity'] == 'ISLAND':
            location = "Island location"
        elif row['ocean_proximity'] == '<1H OCEAN':
            location = "Near ocean (< 1 hour)"
        elif row['ocean_proximity'] == 'NEAR BAY':
            location = "Near bay"
        elif row['ocean_proximity'] == 'NEAR OCEAN':
            location = "Near ocean"
        else:
            location = "Inland"
            
        income_level = "Low" if row['median_income'] < 3 else "Medium" if row['median_income'] < 7 else "High"
        age_desc = "New" if row['housing_median_age'] < 10 else "Old" if row['housing_median_age'] > 40 else "Medium age"
        
        desc = f"{location}, {income_level} income, {age_desc} housing"
        descriptions.append(desc)
    
    test_df['description'] = descriptions
    return test_df

def create_test_data_file(filename='test_data.csv', n_samples=50):
    """Create and save test data to CSV file"""
    
    print(f"🏗️  Generating {n_samples} test samples...")
    
    # Generate the data
    test_df = generate_test_data(n_samples)
    
    # Add descriptions for better interpretation
    test_df = add_sample_descriptions(test_df)
    
    # Display sample of generated data
    print("\n📋 Sample of generated test data:")
    print("=" * 80)
    print(test_df.head(10).to_string(index=True))
    
    # Save to CSV (without target variable)
    columns_to_save = ['longitude', 'latitude', 'housing_median_age', 'total_rooms', 
                      'total_bedrooms', 'population', 'households', 'median_income', 
                      'ocean_proximity', 'description']
    
    test_df[columns_to_save].to_csv(filename, index=False)
    
    print(f"\n💾 Test data saved to '{filename}'")
    print(f"📊 Dataset contains {len(test_df)} rows and {len(columns_to_save)} columns")
    print(f"🎯 Features: {columns_to_save[:-1]}")  # Exclude description
    print(f"📝 Note: 'description' column is just for context, not used in prediction")
    
    # Display summary statistics
    print("\n📈 Data Summary:")
    print("=" * 50)
    print(f"Longitude range: {test_df['longitude'].min():.2f} to {test_df['longitude'].max():.2f}")
    print(f"Latitude range: {test_df['latitude'].min():.2f} to {test_df['latitude'].max():.2f}")
    print(f"Median income range: ${test_df['median_income'].min():.1f}k to ${test_df['median_income'].max():.1f}k")
    print(f"Housing age range: {test_df['housing_median_age'].min()} to {test_df['housing_median_age'].max()} years")
    
    print("\n🌊 Ocean proximity distribution:")
    print(test_df['ocean_proximity'].value_counts())
    
    return test_df

if __name__ == "__main__":
    print("🏠 California Housing Test Data Generator")
    print("=" * 50)
    
    # Generate test data
    test_data = create_test_data_file('test_data.csv', n_samples=50)
    
    print("\n✅ Test data generation completed!")
    print("\nTo run predictions:")
    print("1. Make sure your trained model is saved as 'best_house_price_model.pkl'")
    print("2. Run: python evaluate.py")