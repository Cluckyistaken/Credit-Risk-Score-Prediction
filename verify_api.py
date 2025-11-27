import urllib.request
import json
import sys

def verify_api():
    url = "http://127.0.0.1:8000/api/ml/score"
    data = {
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
    
    print(f"Sending POST request to {url}...")
    try:
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        jsondata = json.dumps(data)
        jsondataasbytes = jsondata.encode('utf-8')
        req.add_header('Content-Length', len(jsondataasbytes))
        
        response = urllib.request.urlopen(req, jsondataasbytes)
        result = json.loads(response.read())
        
        print(f"Response Code: {response.getcode()}")
        print(f"Response Body: {result}")
        
        if "risk_score" in result and "prediction" in result:
             print("SUCCESS: API returned valid prediction.")
        else:
             print("FAILURE: API response missing expected keys.")
             
    except urllib.error.URLError as e:
        print(f"FAILURE: Could not connect to API: {e}")
    except Exception as e:
        print(f"FAILURE: Error during request: {e}")

if __name__ == "__main__":
    verify_api()
