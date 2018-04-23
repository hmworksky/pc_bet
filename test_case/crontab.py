# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from tools import get_num_issue,Memcache
from requests import get
from bs4 import BeautifulSoup
from urllib import quote
from tools import logger
class InsertMemcache:
	def __init__(self):
		self.mem = Memcache()

	def number_issue(self):
		lotteryid_list = [51,52,53,54,200,201,202]
		for lotteryid in lotteryid_list:
			issue = get_num_issue(lotteryid)
			key = "issue_{}".format(lotteryid)
			self.mem.setmem(key,issue)
			logger(lotteryid,"{}在售期号写入缓存成功".format(lotteryid))
		return


	#处理insert_matchinfo中投注串中针对不同彩种转化
	def win_str(self,lotteryid,datatype,win,ins):
		jclq_match_type = {
				'dx_visiting':u'大','dx_home':u'小',
				'rf_visiting':u'让分主负','rf_home':u'让分主胜',
				'sf_visiting':u'主负','sf_home':u'主胜'
				}
		jczq_match_type={
				'sf_home':u'主胜','sf_ping':u'平','sf_fail':u'主负',
				'rq_sf_home':u'让球主胜','rq_sf_ping':u'让球平','rq_sf_fail':u'让球主负'
		}
		if lotteryid in [30,31,32,33,35]:
			if lotteryid == 32:
				tmp_dic = {'0': '1-5', '1': '6-10', '2': '11-15', '3': '16-20', '4': '21-25', '5': '26+'}
				
				if datatype.startswith('sfc_visiting'):
					winteam = '客胜'
				else:
					winteam = '主胜'
				inside_str = tmp_dic.get(datatype[-1])
				win = "{winteam}{inside_str}_{win}".format(**locals())
				return win
			winteam = jclq_match_type.get(datatype)
		else:
			if lotteryid ==21:
				winteam = ins
			elif lotteryid == 2521:
				if ins == '客不败':
					ins = '让球主负'
				elif ins == '主不败':
					ins = '让球主胜'
				elif ins =='客胜':
					ins = '主负'
				winteam = ins
				win ="{winteam}_{win}".format(**locals())
				return win
			elif lotteryid in (22,23):
				winteam = datatype
			winteam = jczq_match_type.get(datatype)
		win = "{winteam}_{win}".format(**locals())
		return win



	def jc_bs4_for_list(self,html,tag,league_info):
		'''
		@html实例,从页面获取的html内容
		@tag:从data文件jc_data中根据不同彩种获取不同标签
		@league_info:比赛名称，如<周五002>
		注：有些彩种的win信息拼接需要拿到ins信息，有些彩种没有ins信息，所以用‘-’代替占位
		'''
		try:
			soup = BeautifulSoup(html, 'lxml')
			tr = soup.find_all("td", class_=tag)
			li = []
			for i in tr:
				sp = BeautifulSoup(str(i), 'lxml')
				s = sp.find_all('a')
				for j in s:
					if j.get(league_info)  and int(j.get('numb')) > 10000:
						if j.string:
							#此处无ins信息，使用-占位
							tmp =(j.get(league_info), j.get('numb'),j.get('data-odd-type'),j.string,'-')
						else:
							win = sp.find('a').find('span').string
							ins = sp.find('a').find('ins').string
							tmp = (j.get(league_info), j.get('numb'),j.get('data-odd-type'),win,ins)
						li.append(tmp)
			tmp_dict ={}
			for i in li:
				_,x,_,_,_ = i
				tmp_dict[int(x)] = i
			# 去除重复数据，拿取前2个足够
			li= [x[1] for x in sorted(tmp_dict.items(),key = lambda s :s[0])[:2]]
		except Exception ,e:
			logger('bs4',e)
		return li

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
		self.mem.setmem("bs4_page_info_{}".format(lotteryid),li)
		league_no1,numb1,data_type1,tmp_win1,ins1 = li[0]
		league_no2,numb2,data_type2,tmp_win2,ins2 = li[1]
		win1 = self.win_str(lotteryid,data_type1,tmp_win1,ins1)
		win2 = self.win_str(lotteryid, data_type2, tmp_win2,ins2)
		cart = cart.format(**locals()).replace('(', '{').replace(')', '}')

		bet_info = {
			"cart":quote(cart),
			"tag":lotterytype,
			"lotteryid":lotteryid if lotteryid != 2521 else 25,
			"bonus":'NTY0MA=='
		}

		self.mem.setmem("bet_{}".format(lotteryid),bet_info)
		logger(lotteryid,"{}投注串写入缓存成功".format(lotteryid))
		return bet_info

	def run(self):
		from data import num_for_lotteryid
		self.number_issue()
		for jczq in num_for_lotteryid('jczq'):
			self.insert_matchinfo(jczq)
		for jclq in num_for_lotteryid('jclq'):
			self.insert_matchinfo(jclq)

if __name__ == '__main__':
	ins = InsertMemcache()
	ins.run()
