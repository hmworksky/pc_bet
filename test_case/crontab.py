# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from tools import get_num_issue,Memcache,get_match
from requests import get
from bs4 import BeautifulSoup
from urllib import quote
from tools import logger
class InsertMemcache:
	def __init__(self):
		self.mem = Memcache()

	def update_issue(self):
		lotteryid_list = [51,52,53,54,200,201,202]
		for lotteryid in lotteryid_list:
			issue = get_num_issue(lotteryid)
			key = "issue_{}".format(lotteryid)
			self.mem.setmem(key,issue)
			logger(lotteryid,"写入缓存成功")
		return "success"
	def update_match(self):
		for matchinfo in ['zq','lq']:
			match_list = get_match(matchinfo)
			self.mem.setmem("{}_matchlist".format(matchinfo),match_list)
		return "success"
	#处理insert_matchinfo中投注串中针对不同彩种转化
	def win_str(self,lotteryid,datatype,win):
		if lotteryid == 32:
			tmp_dic = {'0': '1-5', '1': '6-10', '2': '11-15', '3': '16-20', '4': '21-25', '5': '26+'}
			if datatype.startswith('sfc_visiting'):
				winteam = '客胜'
			else:
				winteam = '主胜'
			inside_str = tmp_dic.get(datatype[-1])
			win = "{winteam}{inside_str}_{win}".format(**locals())
		if lotteryid == 33:
			if datatype == 'dx_visiting':
				winteam = u'大'
			else:
				winteam = u'小'
			win = "{winteam}_{win}".format(**locals())
		if lotteryid == 31:
			if datatype == 'rf_visiting':
				winteam = u'让分主负'
			else:
				winteam = u'让分主胜'
			win = "{winteam}_{win}".format(**locals())
		return win
	def insert_matchinfo(self,lotteryid):
		from data import jc_data
		if lotteryid in [20,21,22,23,25,26,2521]:
			lotterytype = 'jczq'
		else:
			lotterytype = 'jclq'
		match_url,cart,tag_info = jc_data(lotteryid)
		match_url = match_url.format(**locals())
		html = get(match_url).content
		tag = tag_info.get('tag')
		league_info = tag_info.get('leagueinfo')
		li = self.jc_bs4_for_list(html,tag,league_info)
		league_no1,numb1,data_type1,tmp_win1 = li[0]
		league_no2,numb2,data_type2,tmp_win2 = li[1]
		win1 = self.win_str(lotteryid,data_type1,tmp_win1)
		win2 = self.win_str(lotteryid, data_type2, tmp_win2)
		cart = cart.format(**locals()).replace('(', '{').replace(')', '}')
		bet_info = {
			"cart":quote(cart),
			"tag":'"{}"'.format(lotterytype),
			"lotteryid":lotteryid,
			"bonus":'NS44Ng=='
		}

		self.mem.setmem("bet_{}".format(lotteryid),bet_info)
		print bet_info.get("tag")
		return bet_info

	def jc_bs4_for_list(self,html,tag,league_info):
		soup = BeautifulSoup(html, 'lxml')
		tr = soup.find_all("td", class_=tag)
		li = []
		for i in tr:
			sp = BeautifulSoup(str(i), 'lxml')
			s = sp.find_all('a')
			for j in s:
				if j.get(league_info)  and int(j.get('numb')) > 10000:
					if j.string:
						tmp =(j.get(league_info), j.get('numb'),j.get('data-odd-type'),j.string)
					else:
						win = sp.find('a').find('span').string
						tmp = (j.get(league_info), j.get('numb'),j.get('data-odd-type'),win)
					li.append(tmp)
				else:
					return False
		tmp_dict ={}
		for i in li:
			_,x,_,_ = i
			tmp_dict[x] = i
		# 去除重复数据，拿取前2个足够
		li = tmp_dict.values()[:2]
		return li
if __name__ == '__main__':

	ins = InsertMemcache()
	print ins.insert_matchinfo(32)