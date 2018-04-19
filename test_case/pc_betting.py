# coding:utf-8
import requests,re
from tools import bet_str,readconfig,file_to_cookie,url2Dict,get_num_issue,xpath,pc_bet_data
from bs4 import *




class Pcbet(object):
	def __init__(self):
		self.base_url = readconfig('base_url')
		self.bet_url = readconfig('bet_url')
		self.session = requests.Session()
		self.cookie = file_to_cookie()

	def pc_touzhu(self):
		import urllib
		# bet_info = bet_str(200, 6, 1, "01")
		# form_data = {
		# 	"issue": get_num_issue(201),#此处需要改成从接口获取
		# 	"lottery_id": 201,#同上
		# 	"betstr": '13$2_2~2',
		# 	"betnum": None,
		# 	"multiple": 1,
		# 	"is_add": 2
		# }
		#获取投注form表单，pc_bet_data传递的参数详情见data文件中的bet_info
		forms_data = pc_bet_data('04')
		#发送投注请求
		s = self.session.post(url=self.bet_url, cookies=self.cookie, data=forms_data)
		print s.content
		# 获取返回值中的url参数
		url = eval(s.content)['url']
		# 拼接url
		url = self.base_url+urllib.unquote(url)[1:]
		# 获取url中的参数信息，以字典形式返回
		data_info = url2Dict(url)
		# 请求上一个请求返回的url,跳转支付页面
		html = self.session.get(url, cookies=self.cookie).content
		#返回支付页面html及sid，userid等data信息
		return html,data_info



	def pay_cj(self):
		html,data_info = self.pc_touzhu()
		soup = BeautifulSoup(html, 'html5lib')
		sign = [x.get('value') for x in soup.find_all('input', id='ext_sign')][0]
		url = readconfig('pay_cj')
		datas = {
			'userid' : data_info.get('userid'),
			'pid':data_info.get('pid'),
			'sid':data_info.get('sid'),
			'inputrmb':0,
			'inputrmbtp':data_info.get('amount'),
			'prebuyid':data_info.get('prebuyid'),
			'isdjq':0,
			'djqid':0,
			'isredbag':0,
			'redbagid':0,
			'iswlt':0,
			'istpoint':0,
			'sendtime':0,
			'mobile':readconfig('mobile'),
			'orderid':data_info.get('orderid'),
			'fangan':0,
			'danbao':0,
			'selfdb':0,
			'fanyong':5,
			'limit_flag':'true',
			'ext_sign':sign,
			'inputrmbcf':data_info.get('amount'),
			'support_fangan':1
		}
		info =self.session.post(url = url,data = datas,cookies = self.cookie).json()
		return info


	def get_user_info(self):#获取用户信息接口
		url = readconfig('get_userinfo')
		s = self.session.get(url,cookies = self.cookie)
		info =  s.json()
		return info

if __name__ == '__main__':
	zf = Pcbet()
	zf.pc_touzhu()