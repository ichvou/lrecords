#coding: utf-8
import xlrd,unittest
import time
from selenium import webdriver
from methods import search_by_name
import sys
from ddt import ddt, data, unpack

reload(sys)
sys.setdefaultencoding("utf-8")

file_name = "excelddt_data.xlsx"

#csv为中文的未考虑
def get_date(file_name):
	rows = []
	book = xlrd.open_workbook(file_name)
	sheet = book.sheet_by_index(0)
	for row_idx in range(1, sheet.nrows):
		rows.append(list(sheet.row_values(row_idx, 0, sheet.ncols)))
	return rows

@ddt
class LoginTest(unittest.TestCase):

	
	@classmethod
	def setUpClass(cls):
		cls.driver = webdriver.Chrome()
		cls.driver.implicitly_wait(30)
		cls.driver.maximize_window()
		cls.driver.get("http://172.18.84.226")

	def test_login_by_workno(self):
		workNo = self.driver.find_element_by_id("username")
		workNo.send_keys("")
		workPwd = self.driver.find_element_by_id("password")
		workPwd.send_keys("")
		vCode = self.driver.find_element_by_id("code")
		vCode.send_keys("")
		loginButton = self.driver.find_element_by_id("signin")
		loginButton.click()
		time.sleep(1.5)
		# print self.driver.title
		userNo = self.driver.find_element_by_id("workno")
		self.assertEqual("", userNo.text)


	@data(*get_date(file_name))
	@unpack
	def test_search_case_by_name(self,searchKeyword):
		searchXpath = "//*[@id=\"warp-box\"]/div[1]/div/form/input[1]"
#		searchKeyword = u"大明宫中央广场"
		search_by_name(self.driver,searchXpath,searchKeyword)
		searchButton = self.driver.find_element_by_id("searchBtn")
		time.sleep(2)
		searchButton.click()
		time.sleep(2)
		searchResult = self.driver.find_element_by_class_name("cutstr")
		self.assertEqual(searchKeyword, searchResult.get_attribute("title"))
		time.sleep(3)
		print searchKeyword
#		self.driver.refresh()


	
	@classmethod
	def tearDownClass(cls):
		cls.driver.quit()

if __name__ == '__main__':
	unittest.main(verbosity=2)


