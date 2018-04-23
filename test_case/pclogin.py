# coding:utf-8
from  selenium  import webdriver
import time
from tools import Memcache,logger
from tools import readconfig


class CaipiaoLogin:
	def __init__(self):
		self.driver = webdriver.Firefox()
		#self.driver.implicitly_wait(30)
		self.base_url = "http://caipiao.1768.com"
		self.uname = 'hm_txz'
		self.pwd = 'test1324'
	def login(self):
		driver = self.driver
		driver.get(self.base_url)
		time.sleep(3)
		driver.find_element_by_xpath('//*[@id="head_top_login"]').click()
		time.sleep(10)
		driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/ul[1]/li[1]').click()
		time.sleep(2)
		driver.find_element_by_xpath('//*[@id="id_pawform"]/div[1]/input').send_keys(self.uname)
		time.sleep(2)
		driver.find_element_by_xpath('//*[@id="txzpwd"]').send_keys(self.pwd)
		driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div[2]/span').click()
		time.sleep(10)
		driver.refresh()
		time.sleep(10)
		cookie = driver.get_cookies()
		driver.quit()
		dic = {}
		for i in cookie:
			keys = i['name']
			value = i ['value']
			dic[keys] = value
		Memcache().setmem('caipiao_pc_login_cookie',dic)#写入memcache
		with open('cookie.txt','w') as f :#将cookie写入data下的cookie文件
			f.write(str(dic))
		

if __name__ == '__main__':
	# pclogin = CaipiaoLogin()
	# pclogin.login()
	mem = Memcache().getmem('caipiao_pc_login_cookie')
	print mem
	import requests
	url = 'http://caipiao.1768.com/index.php?act=order_base&st=lottery_pay'
	data ={'multiple': 1, 'issue': '2018046', 'is_add': 2, 'lottery_id': 200, 'betnum': '040609172124-08$', 'betstr': '040609172124-08$01~1'}

	cookie = requests.utils.cookiejar_from_dict(eval(mem), cookiejar=None, overwrite=True)
	session = requests.Session()
	session.cookies = cookie	
	s = session.post(url= url ,data = data ).content
	print s
