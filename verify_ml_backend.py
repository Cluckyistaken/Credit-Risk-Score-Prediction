import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.join(os.getcwd(), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from apps.ml.services import MLService

import traceback
import sklearn
import xgboost
import pandas
import numpy

def test_prediction():
    print(f"Scikit-learn version: {sklearn.__version__}")
    print(f"XGBoost version: {xgboost.__version__}")
    print(f"Pandas version: {pandas.__version__}")
    print(f"Numpy version: {numpy.__version__}")

    print("Testing MLService...")
    
    # Sample data (based on german credit data columns)
    sample_data = {
        "Age": 30,
        "Sex": "male",
        "Job": 2,
        "Housing": "own",
        "Saving_accounts": "little",
        "Checking_account": "moderate",
        "Credit_amount": 5000,
        "Duration": 12,
        "Purpose": "radio/TV"
    }
    
    try:
        result = MLService.predict(sample_data)
        print("Prediction Result:", result)
        
        if "prediction" in result and "probability" in result:
            print("SUCCESS: Model produced a prediction.")
        else:
            print("FAILURE: Result format incorrect.")
            
    except Exception as e:
        print(f"FAILURE: Error during prediction: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_prediction()
