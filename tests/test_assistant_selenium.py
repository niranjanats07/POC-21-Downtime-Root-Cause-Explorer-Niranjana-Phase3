
import os
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = os.getenv(
    "DATA_INTELLIGENCE_URL",
    "https://downtime-frontend-phase3.onrender.com"
).rstrip("/")


class GroundedAssistantSeleniumTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
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

    def setUp(self):
        self.driver.get(f"{BASE_URL}/data-intelligence")

        self.wait.until(
            EC.visibility_of_element_located(
                (By.ID, "data-assistant-title")
            )
        )

    def ask_question(self, question):
        textarea = self.wait.until(
            EC.element_to_be_clickable(
                (By.ID, "assistant-question")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            textarea
        )

        textarea.clear()
        textarea.send_keys(question)

        button = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//button[normalize-space()='Ask assistant']"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            button
        )

        self.wait.until(
            lambda driver: button.is_displayed() and button.is_enabled()
        )

        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[normalize-space()='Ask assistant']"
                )
            )
        )

        self.driver.execute_script("arguments[0].click();", button)

        self.wait.until(
            lambda driver: any(
                message in driver.find_element(
                    By.TAG_NAME, "body"
                ).text
                for message in [
                    "Grounded answer",
                    "Question outside supported scope",
                    "Request not permitted",
                    "Assistant unavailable",
                    "Unable to answer"
                ]
            )
        )

        return self.driver.find_element(
            By.TAG_NAME, "body"
        ).text

    def test_assistant_loads(self):
        page_text = self.driver.find_element(
            By.TAG_NAME, "body"
        ).text

        self.assertIn("Grounded Data Assistant", page_text)
        self.assertIn("Mode A", page_text)
        self.assertIn(
            "Ask about the approved Track A results",
            page_text
        )

    def test_overall_summary_is_grounded(self):
        page_text = self.ask_question(
            "Give me an overall summary."
        )

        self.assertIn("Grounded answer", page_text)
        self.assertIn("30 incidents", page_text)
        self.assertIn("2,795", page_text)
        self.assertIn("RES-0001", page_text)
        self.assertIn("synthetic", page_text.lower())

    def test_highest_downtime_machine(self):
        page_text = self.ask_question(
            "Which machine has the highest observed downtime?"
        )

        self.assertIn("Grounded answer", page_text)
        self.assertIn("MCH-02", page_text)
        self.assertIn("850", page_text)
        self.assertIn("RES-0005", page_text)

    def test_evidence_and_version_metadata(self):
        page_text = self.ask_question(
            "Which machine ranks highest by downtime?"
        )

        self.assertIn("Evidence references", page_text)
        self.assertIn("RES-0005", page_text)
        self.assertIn("Data 1.1.0", page_text)
        self.assertIn("Method 1.0.0", page_text)
        self.assertIn("Quality PASS", page_text)
        self.assertIn("synthetic", page_text.lower())

    def test_unsupported_question_is_scoped(self):
        page_text = self.ask_question(
            "What is the weather tomorrow?"
        )

        self.assertIn(
            "Question outside supported scope",
            page_text
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
