import os
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = os.getenv("DATA_INTELLIGENCE_URL", "http://localhost:3001")


class DataIntelligencePageTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1000")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(options=options)
        cls.wait = WebDriverWait(cls.driver, 20)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get(f"{BASE_URL}/data-intelligence")
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h1[contains(., 'Downtime Intelligence')]")
            )
        )

    def test_page_loads(self):
        self.assertIn("Downtime Intelligence", self.driver.page_source)
        self.assertIn("Track A - Comparative Intelligence", self.driver.page_source)

    def test_operational_dashboard_navigation_exists(self):
        link = self.wait.until(
            EC.presence_of_element_located(
                (By.LINK_TEXT, "Operational Dashboard")
            )
        )
        self.assertTrue(link.is_displayed())

    def test_results_table_and_quality_are_visible(self):
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h2[contains(., 'Ranked Comparative Intelligence')]")
            )
        )
        rows = self.driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        self.assertGreater(len(rows), 0)
        self.assertIn("validated", self.driver.page_source)

    def test_machine_filter(self):
        dropdown = self.wait.until(
            EC.element_to_be_clickable((By.ID, "result-dimension"))
        )
        Select(dropdown).select_by_value("machine")

        self.wait.until(
            lambda driver: "MCH-" in driver.find_element(
                By.TAG_NAME, "body"
            ).text
        )
        self.assertIn("MCH-", self.driver.find_element(By.TAG_NAME, "body").text)

    def test_supporting_sections_are_present(self):
        page_text = self.driver.find_element(By.TAG_NAME, "body").text
        for heading in (
            "Supporting Evidence",
            "Methodology",
            "Limitations and Responsible Use",
        ):
            with self.subTest(section=heading):
                self.assertIn(heading, page_text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
