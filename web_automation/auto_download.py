from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import glob

# --- Configuration ---
# 1. Define the download directory
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads_demo")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# 2. Use a simple, stable file link (Example: Google Drive public PDF)
DOWNLOAD_URL = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf" 
FILE_NAME = "dummy.pdf" 

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False, 
    "download.directory_upgrade": True,
    # FIX: This preference forces Chrome to download PDFs instead of viewing them
    "plugins.always_open_pdf_externally": True 
})
options.add_argument("--start-maximized")

# --- Setup Driver ---
print("Setting up WebDriver...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)


def wait_for_download_complete(download_dir, filename, timeout=30):
    """Waits for the final, non-temporary file to appear in the directory."""
    
    expected_path = os.path.join(download_dir, filename)
    
    # Check for temporary file pattern (Chrome uses .crdownload)
    temp_pattern = os.path.join(download_dir, "*.crdownload")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        
        # 1. Check if the final file exists
        if os.path.exists(expected_path):
            # 2. Check if a temporary file still exists
            # This is crucial: ensures the download isn't still in progress
            if not glob.glob(temp_pattern):
                return True # Success!
        
        time.sleep(1) # Wait 1 second before checking again
        
    return False # Timeout

# --- Execution ---
print(f"Attempting to download file: {FILE_NAME} from: {DOWNLOAD_URL}")

# Simply navigating to the URL will trigger the download with the new preference
driver.get(DOWNLOAD_URL) 

print("Waiting for download to complete (up to 30 seconds)...")

if wait_for_download_complete(DOWNLOAD_DIR, FILE_NAME):
    print(f"File **{FILE_NAME}** saved successfully to: {DOWNLOAD_DIR}")
else:
    print("Download **timed out** or failed to complete. Check if the download preference was applied.")

# Clean up
driver.quit()

print(f"\nDemo complete.")