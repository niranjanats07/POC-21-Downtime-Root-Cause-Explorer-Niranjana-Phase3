import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

root = Path(__file__).resolve().parents[1]
evidence = root / "docs" / "evidence" / "13-final-selenium"
evidence.mkdir(parents=True, exist_ok=True)

driver_path = os.environ.get(
    "SE_CHROMEDRIVER",
    str(Path.home() / ".cache/selenium/chromedriver/win64/157.0.8103.78/chromedriver.exe")
)

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=390,844")
driver = webdriver.Chrome(service=Service(driver_path), options=options)
driver.set_window_size(390, 844)
driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {"width": 390, "height": 844, "deviceScaleFactor": 1, "mobile": True})
driver.set_page_load_timeout(90)
wait = WebDriverWait(driver, 60)
base_url = os.environ.get("DATA_INTELLIGENCE_URL", "http://localhost:3000")

try:
    driver.get(base_url)
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Data Intelligence")))
    driver.save_screenshot(str(evidence / "post6-04-operational-dashboard-mobile.png"))

    driver.find_element(By.LINK_TEXT, "Data Intelligence").click()
    wait.until(EC.url_contains("/data-intelligence"))
    wait.until(EC.visibility_of_element_located((By.XPATH, "//nav[@aria-label='Main navigation']")))
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(., 'Downtime Intelligence')]")))
    driver.save_screenshot(str(evidence / "post6-05-data-intelligence-mobile.png"))

    metrics = driver.execute_script("""
        return {
          viewportWidth: window.innerWidth,
          viewportHeight: window.innerHeight,
          documentWidth: document.documentElement.scrollWidth,
          documentHeight: document.documentElement.scrollHeight
        };
    """)
    print("MOBILE VIEWPORT METRICS:", metrics)
    print("OPERATIONAL SCREENSHOT:", evidence / "post6-04-operational-dashboard-mobile.png")
    print("DATA INTELLIGENCE SCREENSHOT:", evidence / "post6-05-data-intelligence-mobile.png")
    print("MOBILE SCREENSHOT CAPTURE: PASS")
finally:
    driver.quit()
