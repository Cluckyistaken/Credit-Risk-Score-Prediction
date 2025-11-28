from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys

def run_test():
    print("Starting Selenium End-to-End Test...")
    
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # Keep commented to see the browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Initialize Driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # 1. Navigate to Frontend
        url = "http://localhost:5173" # Default Vite port
        print(f"Navigating to {url}...")
        driver.get(url)
        
        # 2. Wait for form to load
        wait = WebDriverWait(driver, 10)
        print("Waiting for form inputs...")
        wait.until(EC.presence_of_element_located((By.NAME, "name")))
        
        # 3. Fill Form
        print("Filling application form...")
        driver.find_element(By.NAME, "name").send_keys("John Doe")
        driver.find_element(By.NAME, "age").send_keys("35")
        driver.find_element(By.NAME, "amount").send_keys("5000")
        driver.find_element(By.NAME, "duration").send_keys("12")
        driver.find_element(By.NAME, "purpose").send_keys("car")
        
        # 4. Submit
        print("Submitting form...")
        submit_btn = driver.find_element(By.TAG_NAME, "button")
        submit_btn.click()
        
        # 5. Wait for Result
        print("Waiting for result...")
        # Wait for text containing "Result:" or "Error:"
        result_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Result:') or contains(text(), 'Error:')]")))
        
        result_text = result_element.text
        print(f"Test Completed. Message: {result_text}")
        
        if "Result:" in result_text:
            print("SUCCESS: Prediction received.")
        else:
            print("FAILURE: Received error from backend.")
            
        # 6. Visibility Delay
        print("Keeping browser open for 5 seconds...")
        time.sleep(5)

    except Exception as e:
        print(f"FAILURE: Test failed with error: {e}")
        sys.exit(1)
    finally:
        driver.quit()
        print("Test Finished.")

if __name__ == "__main__":
    run_test()
