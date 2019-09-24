from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import unittest
import time
import re 

#dummy test example
#code from: https://selenium-python.readthedocs.io/getting-started.html#using-selenium-with-remote-webdriver


#This test script preivously had problems because docker containers would launch in a random order and sometimes the chrome container would not be up at the time that the container running this script would try to use that container. 
#this caused the tests to fial. 
#I found a script that adds a delay (source: https://github.com/vishnubob/wait-for-it)

class PythonOrgSearch(unittest.TestCase):

	def setUp(self):
		self.driver = webdriver.Remote(command_executor='http://selenium-chrome:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)

	def test_HomePage(self):
		driver = self.driver
		driver.get("http://web1:8000/")
		self.assertIn("Home", driver.title)
		
		
		#elem = driver.find_element_by_name("q")
		#elem.send_keys("pycon")
		#elem.send_keys(Keys.RETURN)
		#assert "No results found." not in driver.page_source

	def test_Login(self):
		driver = self.driver
		driver.get("http://web1:8000/login")
		self.assertIn("Login", driver.title)
		
		
		elem = driver.find_element_by_name("username")
		elem.send_keys("asdf")
		elem = driver.find_element_by_name("password")
		elem.send_keys("password")

		elem = driver.find_element_by_class_name("btn-primary")
		elem.click()
		driver.implicitly_wait(10)
	
		#information on how to search page for some content found here:
		#https://stackoverflow.com/questions/10978923/how-to-check-if-some-text-is-present-on-a-web-page-using-selenium-2
		
		#this code tests to find out that once a user logs in, there exists a log out button
		src = driver.page_source
		text_found = re.search(r'Logout', src)
		self.assertNotEqual(text_found, None)
		
	
		#this code tests to make sure that once a user logs in, there is no log in button on the page
		src = driver.page_source
		text_found = re.search(r'Login', src)
		self.assertEqual(text_found, None)
		
		#this code tests to make sure that once a user logs in and then clicks log out, there is a button to log in again
		elem = driver.find_element_by_partial_link_text("ogout")
		elem.click()
		driver.implicitly_wait(10)
		src = driver.page_source
		text_found = re.search(r'Login', src)
		self.assertNotEqual(text_found, None)
		

		#assert "No results found." not in driver.page_source
	

	def tearDown(self):
		self.driver.close()

if __name__ == "__main__":
	time.sleep(20)
	unittest.main()