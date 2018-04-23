# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests,re
from tools import readconfig,file_to_cookie,url2Dict,pc_bet_data,logger,Memcache
from bs4 import *
import tools




class Pcbet(object):
	def __init__(self):
		self.mem = Memcache()
		self.base_url = readconfig('base_url')


		self.cookie = eval(self.mem.getmem('caipiao_pc_login_cookie'))
		cookie_jar = requests.utils.cookiejar_from_dict(self.cookie, cookiejar=None, overwrite=True)
		self.session = requests.Session()
		self.session.cookies = cookie_jar
		#requests.utils.add_dict_to_cookiejar(self.session.cookies,self.cookie)
		


	def pc_touzhu(self,lotteryid):
		import urllib
		#获取投注form表单，pc_bet_data传递的参数详情见data文件中的bet_info
		if lotteryid>10000:
			forms_data = pc_bet_data(lotteryid)
			print lotteryid
			print forms_data
			bet_url = readconfig('num_bet_url')
			print bet_url
		else:
			forms_data = eval(self.mem.getmem("bet_{lotteryid}".format(**locals())).replace(' ',''))
			if lotteryid ==2521:
				forms_data['lotterytype']='exy'
			if lotteryid in num_for_lotteryid('jclq'):
				bet_url = readconfig('jclq_bet_url')
			elif lotteryid in num_for_lotteryid('jczq'):
				bet_url = readconfig('jczq_bet_url')
		#发送投注请求
		print bet_url
		print forms_data
		s = self.session.post(url=bet_url, data=forms_data).content
		if eval(s).get('url'):
			# 获取返回值中的url参数
			url = eval(s).get('url')
		else:
			logger('投注失败',"投注结果:{}".format(s))
			return
		# 拼接url
		url = self.base_url+urllib.unquote(url)[1:]
		# 获取url中的参数信息，以字典形式返回
		data_info = url2Dict(url)
		#记录投注结果
		logger(lotteryid,"{}投注成功,orderid:{}".format(data_info.get('lotteryname'),data_info.get('orderid')))
		# 请求上一个请求返回的url,跳转支付页面
		html = self.session.get(url).content
		#返回支付页面html及sid，userid等data信息
		return html,data_info



	def pay_cj(self,lotteryid):
		html,data_info = self.pc_touzhu(lotteryid)
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
	def _run(self):
		from data import num_for_lotteryid
		# for jczq in num_for_lotteryid('jczq'):
		# 	self.pc_touzhu(jczq)
		# for jclq in num_for_lotteryid('jclq'):
		# 	self.pc_touzhu(jclq)
		for i in range(10001,10029):
			print "num:{}".format(i)
			self.pc_touzhu(i)
if __name__ == '__main__':
	bet = Pcbet()
	bet._run()
