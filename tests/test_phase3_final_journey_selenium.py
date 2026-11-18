
import os
import unittest
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = os.getenv(
    "DATA_INTELLIGENCE_URL",
    "https://downtime-frontend-phase3.onrender.com"
).rstrip("/")

EVIDENCE_DIR = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "evidence"
    / "13-final-selenium"
)


class Phase3FinalJourneySeleniumTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1200")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        cls.driver = webdriver.Chrome(options=options)
        cls.wait = WebDriverWait(cls.driver, 60)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "driver"):
            cls.driver.quit()

    def capture_screenshot(self, filename):
        screenshot_path = EVIDENCE_DIR / filename

        saved = self.driver.save_screenshot(str(screenshot_path))
        self.assertTrue(saved, f"Screenshot was not saved: {screenshot_path}")
        self.assertTrue(screenshot_path.is_file())

        print(f"SCREENSHOT: {screenshot_path}")

    def page_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def test_final_operational_and_intelligence_journey(self):

        # 1. Open the Operational Dashboard.
        self.driver.get(f"{BASE_URL}/")

        self.wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "h1"))
        )

        operational_text = self.page_text()

        self.assertIn(
            "Downtime Root Cause Explorer",
            operational_text
        )

        self.assertTrue(
            self.driver.find_elements(
                By.XPATH,
                "//a[normalize-space()='Data Intelligence']"
            ),
            "Data Intelligence navigation link is missing."
        )

        self.capture_screenshot(
            "post6-01-operational-dashboard.png"
        )

        # 2. Navigate to Data Intelligence through the page link.
        intelligence_link = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//a[normalize-space()='Data Intelligence']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            intelligence_link
        )

        self.wait.until(
            lambda driver: driver.current_url.rstrip("/")
            == f"{BASE_URL}/data-intelligence"
        )

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//nav[@aria-label='Main navigation']")
            )
        )

        intelligence_text = self.page_text()

        # 3. Verify approved Data Intelligence metadata and content.
        self.assertIn("Downtime Intelligence", intelligence_text)
        self.assertIn("1.1.0", intelligence_text)
        self.assertIn("1.0.0", intelligence_text)
        self.assertIn("PASS", intelligence_text)
        self.assertIn("Grounded Data Assistant", intelligence_text)

        self.capture_screenshot(
            "post6-02-data-intelligence.png"
        )

        # 4. Return to the Operational Dashboard through its page link.
        operational_link = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//a[normalize-space()='Operational Dashboard']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            operational_link
        )

        self.wait.until(
            lambda driver: driver.current_url.rstrip("/")
            == BASE_URL
        )

        self.wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "h1"))
        )

        returned_text = self.page_text()

        self.assertIn(
            "Downtime Root Cause Explorer",
            returned_text
        )

        self.capture_screenshot(
            "post6-03-return-operational-dashboard.png"
        )

        # 5. Confirm the Data Intelligence navigation remains available.
        self.assertTrue(
            self.driver.find_elements(
                By.XPATH,
                "//a[normalize-space()='Data Intelligence']"
            ),
            "Data Intelligence navigation disappeared after returning."
        )

        print("FINAL JOURNEY RESULT: PASS")
        print(f"BASE URL: {BASE_URL}")
        print(f"EVIDENCE DIRECTORY: {EVIDENCE_DIR}")


if __name__ == "__main__":

