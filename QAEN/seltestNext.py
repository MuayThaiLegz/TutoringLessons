from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class TestGoogleSearch(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    def setUp(self):
        self.driver.get("http://www.google.com")

    def test_title(self):
        self.assertEqual(self.driver.title, "Google")

    def test_search_field_exists(self):
        search_field = self.driver.find_element(By.NAME, "q")
        self.assertIsNotNone(search_field)

    def test_search_python(self):
        search_field = self.driver.find_element(By.NAME, "q")
        search_field.send_keys("Python")
        search_field.submit()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='g']")))

        search_results = self.driver.find_elements_by_xpath("//div[@class='g']")
        self.assertGreater(len(search_results), 0)

    def tearDown(self):
        self.driver.get("http://www.google.com")

    @classmethod
    def tearDownClass(cls):
        
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
