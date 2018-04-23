# coding:utf-8
#pc端投注串，传入数字返回不同串
def pc_bet_form(type):
	bet_info = {
		#双色球单式
		10001:{'betnum':'040609172124-08$','betstr':'040609172124-08$01~1','lotteryid':200},
		#双色球复式
		10002:{'betnum':'01021112202530-10$','betstr':'01021112202530-10$02~7','lotteryid':200},
		#双色球胆拖
		10003:{'betnum':'(1316222833)0519-09$','betstr':'[1316222833]0519-09$03~2','lotteryid': 200},

		#3D直选单式
		10004:{'betnum':'1-6-9$','betstr':'1-6-9$1_1_1~1','lotteryid':201},
		#3D直选复式
		10005: {'betnum': '26-5-7$', 'betstr': '26-5-7$1_1_2~2', 'lotteryid': 201},
		#3D直选和值
		10006: {'betnum': None, 'betstr': '0$1_2~1', 'lotteryid': 201},
		#3D组三投注
		10007: {'betnum': None, 'betstr': '13$2_2~2', 'lotteryid': 201},
		#3D组六单式
		10008: {'betnum': None, 'betstr': '2-3-6$3_1~1', 'lotteryid': 201},
		#3D组六复式
		10009: {'betnum': None, 'betstr': '0268$3_2~4', 'lotteryid': 201},

		#七乐彩单式
		10010: {'betnum': '03070915212330$', 'betstr': '03070915212330$01~1', 'lotteryid': 202},
		#七乐彩复式
		10011: {'betnum': '0710131719222529$', 'betstr': '0710131719222529$02~8', 'lotteryid': 202},
		# 七乐彩胆拖
		10012: {'betnum': '(020423242630)0708$', 'betstr': '[020423242630]0708$03~2', 'lotteryid': 202},

		# 大乐透单式
		10013: {'betnum': '2425263235-0510$', 'betstr': '2425263235-0510$01~1', 'lotteryid': 51},
		# 大乐透复式
		10014: {'betnum': '0102081618-091012$', 'betstr': '0102081618-091012$02~3', 'lotteryid': 51},
		# 大乐透胆拖
		10015: {'betnum': '(09162431)2226-0312$', 'betstr': '[09162431]2226-0312$02~2', 'lotteryid': 51},

		# 七星彩单式
		10016: {'betnum': '0-7-4-5-8-4-8$', 'betstr': '0-7-4-5-8-4-8$01~1', 'lotteryid': 52},
		# 七星彩复式
		10017: {'betnum': '35-0-6-3-0-5-4$', 'betstr': '35-0-6-3-0-5-4$01~2', 'lotteryid': 52},

		# 排列五单式
		10018: {'betnum': '7-2-4-2-2$', 'betstr': '7-2-4-2-2$01~1', 'lotteryid': 53},
		# 排列五复式
		10019: {'betnum': '2-07-4-4-6$', 'betstr': '2-07-4-4-6$01~2', 'lotteryid': 53},

		# 排列三单式
		10020: {'betnum': '8-8-5$', 'betstr': '8-8-5$1_1~1', 'lotteryid': 54},
		# 排列三复式
		10021: {'betnum': '05-9-5$', 'betstr': '05-9-5$1_2~2', 'lotteryid': 54},
		# 排列三直选和值
		10022: {'betnum': '1$', 'betstr': '1$1_3~3', 'lotteryid': 54},
		# 排列三单式组合
		10023: {'betnum': '024$', 'betstr': '024$1_4~6', 'lotteryid': 54},
		# 排列三组三单式
		10024: {'betnum': '6-1-6$', 'betstr': '6-1-6$2_1~1', 'lotteryid': 54},
		# 排列三组三复式
		10025: {'betnum': '14$', 'betstr': '14$2_2~2', 'lotteryid': 54},
		# 排列三组六单式
		10026: {'betnum': '246$', 'betstr': '246$3_1~1', 'lotteryid': 54},
		# 排列三组六复式
		10027: {'betnum': '0135$', 'betstr': '0135$3_2~4', 'lotteryid': 54},
		# 排列三组选和值
		10028: {'betnum': '2$', 'betstr': '2$4_1~2', 'lotteryid': 54},
	}
	return bet_info.get(type)

#传入数字与彩种对应关系
def num_for_lotteryid(lotterytype):
	lottery_title = {
		'200':[10001,10002,10003],
		'201':[10004,10005,10006,10007,10008,10009],
		'202':[10010,10011,10012],
		'51':[10013,10014,10015],
		'52':[10016,10017],
		'53':[10018,10019],
		'54':[10020,10021,10022,10023,10024,10025,10026,10027,10028],
		'jclq':[30,31,32,33,35],
		'jczq':[20,26,21,22,23,2521]
	}
	return lottery_title.get(lotterytype)

#pc端获取期号配置
def bet_url_xpath(lotteryid = 200):
	data = {
		200: {
			'url':"http://caipiao.1768.com/index.php?act=order_ssq&pid=200",
			'issue_xpath':'//*[@id="ssqHead"]/div[1]/div/div/p[1]/em[1]'},
		202:{
			'url':"http://caipiao.1768.com/index.php?act=order_qlc&pid=202",
			'issue_xpath':'//*[@id="qlcHead"]/div[1]/div/div/p[1]/em',
			 },
		201:{
			'url':"http://caipiao.1768.com/index.php?act=order_3d&pid=201",
			'issue_xpath':'/html/body/div[4]/div[1]/div[2]/div/div/p/font',
			},
		51: {
			'url':"http://caipiao.1768.com/index.php?act=order_dlt&pid=51",
			'issue_xpath':'//*[@id="ssqHead"]/div[1]/div/div/p[1]/em[1]',
			},
		52:{
			'url':"http://caipiao.1768.com/index.php?act=order_qxc&pid=52",
			'issue_xpath':'//*[@id="ssqHead"]/div[1]/div/div/p[1]/em[1]',
			},
		53:{
			'url':"http://caipiao.1768.com/index.php?act=order_pl5&pid=53",
			'issue_xpath':'/html/body/div[4]/div[1]/div[2]/div/div/p/font'
			},
		54:{
			'url':"http://caipiao.1768.com/index.php?act=order_pl3&pid=54",
			'issue_xpath':'/html/body/div[4]/div[1]/div[2]/div/div/p/font'
		}
	}
	return data.get(lotteryid).get('url'),data.get(lotteryid).get('issue_xpath')

#竞彩pc投注串
def jc_data(lotteryid):
	jc_bet_info ={
			'url':'http://caipiao.1768.com/index.php?act={lotterytype}&st=main&pid={lotteryid}',
			'cart':'[("ball":"{numb1}:{league_no1}:[{win1}]/{numb2}:{league_no2}:[{win2}]","data":"{numb1}:{league_no1}:[{win1}]/{numb2}:{league_no2}:[{win2}]^2串1","tag":"{lotterytype}","times":"1","note":1,"money":2,"matchcount":2)]',
			'cart_jclq':'[("ball":"{numb1}:{league_no1}:[{win1}]/{numb2}:{league_no2}:[{win2}]","data":"{numb1}:{league_no1}:[{win1}]/{numb2}:{league_no2}:[{win2}]^2串1","tag":"jclq","times":1,"note":1,"money":2,"matchcount":2)]',
			'tag_leagueinfo':{
				20:{
					'tag':'average-pv odds',
					'leagueinfo':'league_no_week'
				},
				26:{
					'tag':'average-pv odds',
					'leagueinfo':'league_no_week'
				},
				25:{
					'tag':'sf-odds odds',
					'leagueinfo':'league_no'
				},
				22:{
					'tag':'average-pv odds',
					'leagueinfo':'league_no_week'
				},
				23:{
					'tag':'average-pv odds',
					'leagueinfo': 'league_no_week'
				},
				2521:{
					'tag':'average-pv odds',
					'leagueinfo': 'league_no_week'
				},
				21:{
					'tag':'odds',
					'leagueinfo': 'league_no_week'
				},
				35:{
					'tag':'sf-visiting-odds odds',
					'leagueinfo': 'league_no'
				},
				30:{
					'tag':'odds',
					'leagueinfo': 'league_no'
				},
				31:{
					'tag':'odds',
					'leagueinfo': 'league_no'
				},
				33:{
					'tag':'odds',
					'leagueinfo': 'league_no'
				},
				32: {
					'tag': 'odds',
					'leagueinfo': 'league_no'
				}


			}
	}
	return jc_bet_info.get('url'),jc_bet_info.get('cart'),jc_bet_info.get('tag_leagueinfo').get(lotteryid)