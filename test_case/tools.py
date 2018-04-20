# coding:utf-8
from random import randint,sample
from ConfigParser import ConfigParser
from requests import get
from bs4 import *
import hashlib,urlparse
import os,requests
from urllib import urlencode,quote,unquote
import lxml
import html5lib

def bet_str(lotteryid=None, rednum=None, bluenum=None, wanfa=None):  # lotteryid(int):彩种ID，wanfa(str):01单式，02复式，03胆拖 rednum：红球个数，bluenum:蓝球个数
	dic = {}
	from itertools import combinations, permutations  # combinations不可重复的排列组合，permutations可重复的排列组合
	if lotteryid == 200:  # 双色球
		red = randombet(rednum, 33)
		red_str = ''.join(map(str, red))
		blue = randombet(bluenum, 16)
		blue_str = ''.join(map(str, blue))
		li = red + blue
		count_bet = int(len(list(combinations(red, 6)))) * bluenum
		betnum = "{red}-{blue}$".format(red=red_str, blue=blue_str)
		dic["betnum"] = betnum
		if wanfa == '01':
			if rednum == 6 and bluenum == 1:  # 单式要求红球6个蓝球一个
				betstr = betnum + '01~1'
				dic["betstr"] = betstr
			else:
				dic['errorcode'] = '1001'
				dic['errormsg'] = '单式要求红球等于6个且蓝球等于1个'
				return dic
		elif wanfa == '02':
			if rednum > 6 or bluenum > 1:
				betstr = betnum + '02~{count_bet}'.format(count_bet=count_bet)
				dic["betstr"] = betstr
			else:
				dic['errorcode'] = '1001'
				dic['errormsg'] = '复式要求红球大于6个或蓝球大于1个'
				return dic
		elif wanfa == '03':
			betstr = '[{red}]'.format(red=red_str) + blue_str + '$03~{num}'.format(num=count_bet)
			betnum = '(red)'.format(red=red_str) + blue_str + '$'
		return dic
	elif lotteryid == 201:  # 福彩3D
		red = randombet(rednum, 9)
	elif lotteryid == 202:  # 七乐彩
		pass
	elif lotteryid == 51:  # 大乐透
		pass
	elif lotteryid == 52:  # 七星彩
		pass
	elif lotteryid == 54:  # 排列三
		pass
	elif lotteryid == 53:  # 排列五
		pass
def load_data_file():
	data_path = "D:\\SOFTWARE\\study\\auto\\selenium\\data\\log"
	os.chdir(data_path)

def strf_time(type):
	import time
	if type == 'time':
		return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	else:
		return time.strftime("%Y-%m-%d", time.localtime())
def logger(title,msg):#titile标题，msg内容
	load_data_file()
	log_path = "{}.log".format(strf_time('date'))
	with open(log_path,"a+") as f:
		f.write("\n{}:---[{}]---:{}".format(strf_time('time'),title,msg))

def randombet(nums, count_num, type=0, start=1):  # nums:生成球号码,count_num:球总数,type:0=>不重复，1=>可重复，start从0或者1开始生成，1代表从1开始生成
	li = []
	while len(li) < nums:
		if start == 1:
			number = str(randint(1, count_num))
			if len(number) < 2:
				number = '0' + number
		else:
			number = str(randint(0, count_num))
		li.append(number)
		if type == 0:
			li = list(set(li))
	li = sorted(li)
	return li

def readconfig(key):
    cf = ConfigParser()
    cf.read("D:/SOFTWARE/study/auto/selenium/data/config.conf")
    sections = cf.sections()
    for i in sections:
        kvs = dict(cf.items(i))
        if key in kvs.keys():
            return  kvs[key]
        else :
            pass

def load_cookie_dir():
	'''
	将工作目录切换至数据目录
	:return:
	'''
	import os
	os.chdir("D:\\SOFTWARE\\study\\auto\\selenium\\data")

def file_to_cookie():
	'''
	读取cookie信息
	:return: cookie字典
	'''
	load_cookie_dir()
	fp = open('cookie.txt', 'r').read()
	return eval(fp)

class Memcache(object):
	def __init__(self):
		from pymemcache.client.base import Client
		self.client = Client(("127.0.0.1",11211))
	def setmem(self,key,value):
		return self.client.set(str(key),value)
	def getmem(self,key):
		return self.client.get(key)
	def delmem(self,key):
		return self.client.delete(key)

def md5(data):
	#str = "&".join(sorted(data.split("&")))
	m = hashlib.md5()
	m.update(data)
	return m.hexdigest()

def sha1(data):
	return hashlib.sha1(data).hexdigest()

def get_match(type):#传递竞足或竞篮页面，通过bs4去爬取match_id
	if type == 'zq':
		url = readconfig('jczq_match_url')
	elif type == 'lq':
		url = readconfig('jclq_match_url')
	html = get(url).content
	soup = BeautifulSoup(html, 'html5lib')
	tr = soup.find_all("tr", class_="game-item-detail")
	li = [x.get('data-game-id') for x in soup.find_all("tr", class_="game-item-detail")]
	return  li

def get_num_issue(lotteryid):#获取数字彩期号,从页面抓取在售期号
	from data import bet_url_xpath
	url,path = bet_url_xpath(lotteryid)
	html = requests.get(url=url ).content
	issue = xpath(html,path)
	return issue


def xpath(html,path):
	import lxml
	selector = lxml.etree.HTML(html)
	links = selector.xpath(path)
	data = [x.text for x in links ][0]
	return data


def url2Dict(url):
    query = urlparse.urlparse(url).query
    return dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])

def pc_bet_data(num):
	from data import pc_bet_form,num_for_lotteryid
	datas = pc_bet_form(num)
	lotteryid = datas.get('lotteryid')
	mem = Memcache()
	titles = num_for_lotteryid()
	title = [k for k, v in  titles.items() if num in v][0]
	issue_key = "issue_{}".format(title)
	issue = mem.getmem(issue_key)
	bet = {
		'issue':issue,
		'lottery_id':lotteryid,
		'betstr':datas.get('betstr'),
		'betnum': datas.get('betnum'),
		'multiple':1,
		'is_add':2
	}
	return bet


def jc_bet_data(lotteryid):
	if lotteryid in (20,21,22,23,25,26,2521):
		match_list = Memcache().getmem('zq_matchlist')
	else:
		match_list = Memcache().getmem('lq_matchlist')
	first_match = match_list[0]
	strs ='[{"ball":"106925:周四001:[主胜_1.37]/106926:周四002:[主胜_2.14]","data":"106925:周四001:[主胜_1.37]/106926:周四002:[主胜_2.14]^2串1","tag":"jczq","times":5,"note":1,"money":10,"matchcount":2}]'
	bet = {
		"cart":quote(strs),
		"tag":'jczq',
		"lotteryid":lotteryid,
		"bonus":'NS44Ng=='
	}
	return bet

if __name__ == '__main__':
	print jc_bet_data(25)