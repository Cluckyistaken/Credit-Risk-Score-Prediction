from apps.ml.services import MLService
import pandas as pd

def test_prediction():
    print("Testing MLService prediction...")
    
    # Sample data (based on german_credit_data.csv structure)
    sample_data = {
        'Age': 30,
        'Sex': 'male',
        'Job': 2,
        'Housing': 'own',
        'Saving_accounts': 'little',
        'Checking_account': 'rich',
        'Credit_amount': 1000,
        'Duration': 12,
        'Purpose': 'radio/TV'
    }
    
    try:
        result = MLService.predict(sample_data)
        print(f"Prediction Result: {result}")
        
        if "prediction" in result and "probability" in result:
            print("SUCCESS: Prediction returned expected keys.")
        else:
            print("FAILURE: Prediction missing keys.")
            
    except Exception as e:
        print(f"FAILURE: Error during prediction: {e}")
        import traceback
        traceback.print_exc()

test_prediction()
