from selenium import webdriver
import unittest

class TestSample(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        
    def test_title(self):
        self.driver.get("http://www.google.com")
        self.assertEqual(self.driver.title, "Google")
        
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()