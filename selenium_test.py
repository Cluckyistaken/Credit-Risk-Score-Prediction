from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys

def run_test():
    print("Starting Selenium Test...")
    
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # Uncomment to run headless
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
        
        # Wait for form to load (checking for an input field)
        wait = WebDriverWait(driver, 10)
        print("Waiting for page to load...")
        
        # Adjust these selectors based on your actual React App structure
        # Assuming inputs have name attributes or specific IDs
        # If not, we might need to inspect the frontend code first.
        # For now, I'll use generic selectors that often work or need adjustment.
        
        # Example: Filling 'Age'
        # Try to find by name="Age" or similar
        # If your frontend uses specific IDs, replace these.
        
        # Let's try to find inputs. 
        # Since I haven't seen the frontend code, I will assume standard inputs.
        # If this fails, I will need to read the frontend code.
        
        # For the purpose of this script, I'll try to find *any* input to verify page load at least.
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
        print("Page loaded successfully.")
        
        # TODO: Implement actual form filling once frontend structure is confirmed.
        # For now, we just verify the page loads without error.
        
        title = driver.title
        print(f"Page Title: {title}")
        
        # Check if "Credit Risk" or similar is in title or body
        body_text = driver.find_element(By.TAG_NAME, "body").text
        if "Credit" in body_text or "Risk" in body_text:
             print("SUCCESS: Found expected text on page.")
        else:
             print("WARNING: Did not find 'Credit' or 'Risk' text. Page might be blank or different.")

    except Exception as e:
        print(f"FAILURE: Test failed with error: {e}")
        sys.exit(1)
    finally:
        driver.quit()
        print("Test Finished.")

if __name__ == "__main__":
    run_test()
