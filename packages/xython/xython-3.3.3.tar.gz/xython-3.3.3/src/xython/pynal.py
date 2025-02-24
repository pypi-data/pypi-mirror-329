# -*- coding: utf-8 -*-
import re, time, calendar, arrow, datetime, string
import pywintypes
from korean_lunar_calendar import KoreanLunarCalendar
import jfinder, youtil, basic_data  # xython 모듈


class pynal():
	"""
	datetime의 객체는 local time을 기준으로 만듭니다

	datetime 객체를 기준으로 하여도 된다
	시간을 다루기 위한 모듈
	기본적으로 날짜의 변환이 필요한 경우는 utc 시간을 기준으로 변경하도록 하겠읍니다
	음력의 자료는 KoreanLunarCalendar모듈을 사용한다
	주일의 시작은 월요일이다

	dt_obj : datetime 객체
	timestamp : utc기준으로 1970년 1월1일부터 1초마다 숫자를 더해서 사용
	한 주의 시작 : '월'요일 부터
	utc : 1970.1.1을 1초로 시작
	datetime : 1900.1.1을 1초로 시작
	date 클래스의 isoformat() - YYYY-MM-DD의 형태를 말합니다

	"""

	def __init__(self):
		self.xyre = jfinder.jfinder()
		self.util = youtil.youtil()

		self.lunar_calendar = KoreanLunarCalendar()  # 음력
		self.vars = basic_data.basic_data().vars  # package안에서 공통적으로 사용되는 변수들

	def calculate_month_n_day_between_two_date(self, date1, date2, month_days=30):
		"""
		2날짜사이의 기간을 몇개월 몇일로 계산하는 것
		calculate_month_n_day_between_two_date("2024-10-01", "2024-08-15")

		:param date1:
		:param date2:
		:param month_days:
		:return:
		"""
		dt1 = self.change_any_text_time_to_dt_obj(date1)
		ts1 = self.change_dt_obj_to_utc(dt1)
		dt2 = self.change_any_text_time_to_dt_obj(date2)
		ts2 = self.change_dt_obj_to_utc(dt2)

		delta = int(ts1 - ts2)
		mon_ts = month_days * 24 * 60 * 60
		months = int(delta / mon_ts)
		days = int((delta - months * mon_ts) / (24 * 60 * 60))

		return [months, days]

	def calculate_overlap_sec_between_two_time(self, dt_obj_1, dt_obj_2, input_list):
		"""
		두시간 사이에 겹치는 시간을 초를 계산하는것

		:param dt_obj_1: datetime객체
		:param dt_obj_2: datetime객체
		:param input_list:
		:return:
		"""
		result = []
		check_data = self.overlap_area_for_two_dt_range(dt_obj_1, dt_obj_2)
		for one_list in input_list:
			base_sec_start = one_list[0] * 60 * 60 + one_list[1] * 60
			base_sec_end = one_list[2] * 60 * 60 + one_list[3] * 60
			overlap_area = self.intersect_two_time_range(base_sec_start, base_sec_end, check_data[0], check_data[1])
			result.append([overlap_area, one_list[4], one_list[5], one_list[6]])
		return result

	def chang_no_to_nth_eng(self, no):
		"""
		이것은 그날을 서수로 돌려주는 것입니다 ---> ['1ST']

		:param no:
		:return:
		"""
		data = ['1ST', '2ND', '3RD', '4TH', '5TH', '6TH', '7TH', '8TH', '9TH', '10TH', '11TH', '12TH', '13TH', '14TH',
				'15TH', '16TH', '17TH', '18TH', '19TH', '20TH', '21ST', '22ND', '23RD', '24TH', '25TH', '26TH', '27TH',
				'28TH', '29TH', '30TH', '31ST']
		return data[no - 1]

	def change_any_text_time_to_dt_obj(self, input_text_time):
		"""
		기존의 자료를 다른 형태러 만들어 본것
		어떤 문자열의 시간이 오더라도 datetime형으로 돌려주는것

		:param input_text_time: 문자열로된 시간
		:return:
		"""

		input_text_time = str(input_text_time)

		result = {}

		result["yea"] = 0
		result["mon"] = 0
		result["day"] = 0
		result["hou"] = 0
		result["min"] = 0
		result["sec"] = 0
		result["week"] = 0
		result["bellow_sec"] = 0
		result["utc_+-"] = 0
		result["utc_h"] = 0
		result["utc_m"] = 0

		# 전처리를 실시
		dt_string = (str(input_text_time).strip()).lower()
		dt_string = dt_string.replace("/", "-")
		dt_string = dt_string.replace("#", "-")

		ymd_sql = []

		# 아래의 자료 형태들을 인식하는 것이다
		# '2022-03-04'
		# '3/12/2018' => '3-12-2018'
		# '20220607'
		# "180919 015519"
		# 'Jun 28 2018 7:40AM',
		# 'Jun 28 2018 at 7:40AM',
		# 'September 18, 2017, 22:19:55',
		# 'Mon, 21 March, 2015',
		# 'Tuesday , 6th September, 2017 at 4:30pm'
		# '2023-09-09 00:00:00+00:00'
		# 'Sun, 05/12/1999, 12:30PM', => 'Sun, 05-12-1999, 12:30PM',
		# '2023-03-01T10:01:23.221000+09:00'

		# +00:00 을 찾아내는것
		dt_string = dt_string.strip()
		old_dt_string = dt_string
		resql_result = self.xyre.search_all_by_jf_sql("[+-:1~1][숫자:2~2]:[숫자:2~2]", dt_string)
		if resql_result:
			temp = resql_result[0][0].split(":")
			result["utc_+-"] = temp[0][0]
			result["utc_h"] = temp[0][1:3]
			result["utc_m"] = temp[1]
			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()
		if old_dt_string != "":
			pass
		# print("1) +00:00       의 형태 ====>", " 기존 => ", old_dt_string, " 변경 => ", dt_string, " 찾은것 => ",  resql_result)

		# "2022-03-04"
		# "3-12-2018"
		# "20220607"
		# "180919 015519"
		# 'Jun 28 2018 7:40AM',
		# 'Jun 28 2018 at 7:40AM',
		# 'September 18, 2017, 22:19:55',
		# 'Mon, 21 March, 2015',
		# 'Tuesday , 6th September, 2017 at 4:30pm'
		# "2023-09-09 00:00:00"
		# 'Sun, 05-12-1999, 12:30PM',
		# '2023-03-01T10:01:23.221000'

		# 7:40AM
		dt_string = dt_string.strip()
		old_dt_string = dt_string
		resql = "([숫자:1~2]):([숫자:1~2])[공백&apm:1~3]"
		resql_result = self.xyre.search_all_by_jf_sql(resql, dt_string)

		ampm = ""
		if resql_result:
			result["hou"] = resql_result[0][3][0]
			result["min"] = resql_result[0][3][1]
			searched_data = resql_result[0][0]
			if "am" in searched_data:
				ampm = "am"
				searched_data = searched_data.replace("am", "")
			if "pm" in searched_data:
				ampm = "pm"
				searched_data = searched_data.replace("pm", "")

			temp = searched_data.split(":")
			result["hou"] = str(temp[0]).strip()
			result["min"] = str(temp[1]).strip()

			if ampm == "pm" and int(result["hou"]) < 12:
				result["hou"] = int(result["hou"]) + 12
			elif ampm == "pm" and int(result["hou"]) == 12:
				result["hou"] = 0

			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()
		if old_dt_string != "":
			pass
		# print("2) 7:40AM       의 형태 ====>", " 기존 => ", old_dt_string, " 변경 => ", dt_string, " 찾은것 => ",  resql_result)

		# "2022-03-04"
		# "3-12-2018"
		# "20220607"
		# "180919 015519"
		# 'Jun 28 2018',
		# 'September 18, 2017, 22:19:55',
		# 'Mon, 21 March, 2015',
		# 'Tuesday , 6th September, 2017'
		# "2023-09-09 00:00:00"
		# 'Sun, 05-12-1999,'
		# '2023-03-01T10:01:23.221000'

		# 17:08:00
		dt_string = dt_string.strip()
		old_dt_string = dt_string
		resql_result = self.xyre.search_all_by_jf_sql("[숫자:2~2]:[숫자:2~2]:[숫자:2~2]", dt_string)

		if resql_result:
			temp = resql_result[0][0].split(":")
			result["hou"] = temp[0]
			result["min"] = temp[1]
			result["sec"] = temp[2]

			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.replace("at", "")
			dt_string = dt_string.strip()
		if old_dt_string != "":
			pass
		# print("3) 17:08:00     의 형태 ====>", " 기존 => ", old_dt_string, " 변경 => ", dt_string, " 찾은것 => ",  resql_result)

		# "2022-03-04"
		# "3-12-2018"
		# "20220607"
		# "180919 015519"
		# 'Jun 28 2018',
		# 'September 18, 2017,',
		# 'Mon, 21 March, 2015',
		# 'Tuesday , 6th September, 2017'
		# 'Sun, 05-12-1999,'
		# '2023-03-01T.221000'

		# 2022-03-04
		dt_string = dt_string.strip()
		old_dt_string = dt_string
		if self.xyre.search_all_by_jf_sql("[숫자:4~4]-[숫자:1~2]-[숫자:1~2]", dt_string):
			resql_result = self.xyre.search_all_by_jf_sql("[숫자:4~4]-[숫자:1~2]-[숫자:1~2]", dt_string)

			temp = resql_result[0][0].split("-")
			result["yea"] = temp[0]
			result["mon"] = temp[1]
			result["day"] = temp[2]

			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()
		if old_dt_string != "":
			pass
		# print("4) 2022-03-04   의 형태 ====>", " 기존 => ", old_dt_string, " 변경 => ", dt_string, " 찾은것 => ",  resql_result)

		# "3-12-2018"
		# "20220607"
		# "180919 015519"
		# 'Jun 28 2018',
		# 'September 18, 2017,',
		# 'Mon, 21 March, 2015',
		# 'Tuesday , 6th September, 2017'
		# 'Sun, 05-12-1999,'
		# 'T.221000'

		# 18/09/19 => 18-09-19
		dt_string = dt_string.strip()
		old_dt_string = dt_string
		resql_result = self.xyre.search_all_by_jf_sql("[숫자:1~2]-[숫자:1~2]-[숫자:1~4]", dt_string)
		if resql_result:
			temp = resql_result[0][0].split("-")
			result["yea"] = temp[2]
			result["mon"] = temp[1]
			result["day"] = temp[0]

			if int(temp[0]) > 12:
				result["mon"] = temp[1]
				result["day"] = temp[0]
			elif int(temp[1]) > 12:
				result["mon"] = temp[0]
				result["day"] = temp[1]

			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()
		if old_dt_string != "":
			pass
			# print("5) 18/09/19     의 형태 ====>", " 기존 => ", old_dt_string, " 변경 => ", dt_string, " 찾은것 => ",  resql_result)

			# "20220607"
			# "180919 015519"
			# 'Jun 28 2018',
			# 'September 18, 2017,',
			# 'Mon, 21 March, 2015',
			# 'Tuesday , 6th September, 2017'
			# 'Sun'

			# 20220607
			dt_string = dt_string.strip()
			old_dt_string = dt_string
			resql_result = self.xyre.search_all_by_jf_sql("(20|19)[숫자:6~6]", dt_string)
		if resql_result:
			result["yea"] = resql_result[0][0][0:4]
			result["mon"] = resql_result[0][0][4:6]
			result["day"] = resql_result[0][0][6:8]

			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()

		if old_dt_string != "":
			pass
		# print("6) 20220607     의 형태 ====>", " 기존 => ", old_dt_string, " 변경 => ", dt_string, " 찾은것 => ",  resql_result)

		# "180919 015519"
		# 'Jun 28 2018',
		# 'September 18, 2017,',
		# 'Mon, 21 March, 2015',
		# 'Tuesday , 6th September, 2017'
		# 'Sun'

		# Tuesday
		for one_week in self.vars["week_vs_enum"].keys():
			if one_week in dt_string:
				result["week"] = self.vars["week_vs_enum"][one_week]
				dt_string = dt_string.replace(one_week, "")
				dt_string = dt_string.strip()

		if old_dt_string != "":
			pass
		# print("7) Tuesday      의 형태 ====>", " 기존 => ", old_dt_string, " 변경 => ", dt_string, " 찾은것 => ",  resql_result)

		# "180919 015519"
		# 'Jun 28 2018',
		# 'September 18, 2017,',
		# ', 21 March, 2015',
		# ', 6th September, 2017'

		# "180919 015519"
		dt_string = dt_string.strip()
		old_dt_string = dt_string
		resql_result = self.xyre.search_all_by_jf_sql("[숫자:6~6][공백:1~1][숫자:6~6]", dt_string)
		if resql_result:
			result["day"] = resql_result[0][0][0:2]
			result["mon"] = resql_result[0][0][2:4]
			result["yea"] = resql_result[0][0][4:6]
			result["bellow_sec"] = resql_result[0][0][:-6]

			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()
		if old_dt_string != "":
			pass
		# print("8) 180919 015519의 형태 ====>", " 기존 => ", old_dt_string, " 변경 => ", dt_string, " 찾은것 => ",  resql_result)

		# 'Jun 28 2018',
		# 'September 18, 2017,',
		# ', 21 March, 2015',
		# ', 6th September, 2017'

		# Jun 28 2018 스타일 찾기
		dt_string = dt_string.strip()
		old_dt_string = dt_string
		resql_result = self.xyre.search_all_by_jf_sql("([영어:3~10])[공백&,.:0~3]([숫자:1~2])[공백&,.:1~3]([숫자:1~4])", dt_string)

		if resql_result:
			result["mon"] = self.vars["dic_mon_no"][resql_result[0][3][0]]
			result["day"] = resql_result[0][3][1]
			result["yea"] = resql_result[0][3][2]

			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()
		if old_dt_string != "":
			pass
		# print("9) Jun 28 2018  의 형태 ====>", " 기존 => ", old_dt_string, " 변경 => ", dt_string, " 찾은것 => ",  resql_result)

		# ', 21 March, 2015',
		# ', 6th September, 2017'
		#	'Tuesday , 6th September, 2017 at 4:30pm'

		# 6th September, 2017 스타일 찾기
		dt_string = dt_string.strip()
		old_dt_string = dt_string
		resql_result = self.xyre.search_all_by_jf_sql("[숫자:1~2][영어:0~3][공백&,:1~3][영어:3~9][공백&,:0~3][숫자:4~4]", dt_string)
		if resql_result:
			found_text = resql_result[0][0]

			bbb = self.xyre.search_all_by_jf_sql("[영어:3~9]", found_text)
			for num in self.vars["dic_no_mon"].keys():
				if bbb[0][0] in self.vars["dic_no_mon"][num]:
					result["mon"] = num
			found_text = found_text.replace(bbb[0][0], "")

			ccc = self.xyre.search_all_by_jf_sql("[숫자:4~4]", found_text)
			result["yea"] = ccc[0][0]
			found_text = found_text.replace(ccc[0][0], "")

			ddd = self.xyre.search_all_by_jf_sql("[숫자:1~2]", found_text)
			result["day"] = ddd[0][0]

			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()

		resql_result = self.xyre.search_all_by_jf_sql("\.[숫자:6~6]", dt_string)
		if resql_result:
			dt_string = dt_string.replace(resql_result[0][0], "")
			# .586525
			# 초단위 이하의 자료
			result["bellow_sec"] = resql_result[0][0]

		# 여태 걸린것주에 없는 4가지 숫자는 연도로 추측한다
		resql_result = self.xyre.search_all_by_jf_sql("[숫자:4~4]", dt_string)
		if resql_result:
			# print(resql_result)
			result["yea"] = int(resql_result[0][0])
			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()

		# 여태 걸린것 없는 2가지 숫자는 날짜로 추측한다
		resql_result = self.xyre.search_all_by_jf_sql("[숫자:2~2]", dt_string)
		if resql_result:
			result["day"] = resql_result[0][0]
			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()

		resql_result = self.xyre.search_all_by_jf_sql("pm[또는]am", dt_string)
		if resql_result:
			# print(resql_result)
			if resql_result[0][0] == "pm" and int(result["hou"]) <= 12:
				result["hou"] = int(result["hou"]) + 12
			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()
		if old_dt_string != "":
			pass
		# print("10)6th September, 2017의 형태 ====>", " 기존 => ", old_dt_string, " 변경 => ", dt_string, " 찾은것 => ",  resql_result)

		result["yea"] = int(result["yea"])
		result["mon"] = int(result["mon"])
		result["day"] = int(result["day"])
		result["hou"] = int(result["hou"])
		result["min"] = int(result["min"])
		result["sec"] = int(result["sec"])
		# print("전체 인쇄 => ", result["yea"], result["mon"], result["day"], result["hou"], result["min"], result["sec"])

		try:
			text_time = str(result["yea"]) + "-" + str(result["mon"]) + "-" + str(result["day"]) + " " + str(
				result["hou"]) + "-" + str(result["min"]) + "-" + str(result["sec"])
			# print("시간 문자 ==> ", text_time)
			if len(str(result["yea"])) == 2:
				result = datetime.datetime.strptime(text_time, "%y-%m-%d %H-%M-%S")
			elif len(str(result["yea"])) == 4:
				result = datetime.datetime.strptime(text_time, "%Y-%m-%d %H-%M-%S")
		except:
			result = "error"

		return result

	def change_anytime_to_dt_obj(self, input_text_time):
		"""
		어떤 형태의 시간관련 문자를 datetime객체로 만드는 것

		:param input_text_time:
		:return:
		"""
		result = self.check_input_time(input_text_time)
		return result

	def change_anytime_to_text_time_with_format(self, input_text_time, input_time_format='%Y-%m-%d'):
		"""
		입력시간을 입력된 형태로 바꾸는 것

		:param input_time_format:
		:param input_format:
		:return:
		"""
		dt_obj = self.check_input_time(input_text_time)
		result = time.strptime(dt_obj, input_time_format)
		return result

	def change_anytime_to_utc(self, input_time=""):
		"""
		어떤 시간이라도 utf형식의 시간으로 만들어 주는 것

		:param input_time:
		:return:
		"""

		result = ""
		if input_time == "":  # 만약 아무것도 넣지 않으면 localtime을 돌려준다
			result = time.localtime()
		elif type(input_time) == type([]) and len(input_time) == 3:  # [2023, 03, 14]의 형식일때
			result = self.change_ymd_list_to_utc(input_time)
		elif type("string") == type(input_time):  # 만약 입력형태가 문자열이면
			re_compiled = re.compile("\d+")
			temp = re.findall(re_compiled, input_time)
			if len(temp) == 3:  # "2023-03-14"의 형식일때
				ymd_list = temp
			elif len(temp) == 1:  # "230314"의 형식일때
				if len(temp[0]) == 5:  # "23314"의 형식일때
					ymd_list = [temp[0][:2], temp[0][2:3], temp[0][-2:]]
				elif len(temp[0]) == 6:
					ymd_list = [temp[0][:2], temp[0][2:4], temp[0][-2:]]
				elif len(temp[0]) == 8:  # "20230314"의 형식일때
					ymd_list = [temp[0][:4], temp[0][4:6], temp[0][-2:]]
			result = self.change_ymd_list_to_utc(ymd_list)
		else:
			result = time.localtime(input_time)
		return result

	def change_anytime_to_utftime(self, input_time=""):

		result = ""
		if input_time == "":  # 만약 아무것도 넣지 않으면 localtime을 돌려준다
			result = time.localtime()
		elif type(input_time) == type([]) and len(input_time) == 3:  # [2023, 03, 14]의 형식일때
			result = self.change_ymdlist_to_utftime(input_time)
		elif type("string") == type(input_time):  # 만약 입력형태가 문자열이면
			re_compiled = re.compile("\d+")
			temp = re.findall(re_compiled, input_time)
			if len(temp) == 3:  # "2023-03-14"의 형식일때
				ymd_list = temp
			elif len(temp) == 1:  # "230314"의 형식일때
				if len(temp[0]) == 5:  # "23314"의 형식일때
					ymd_list = [temp[0][:2], temp[0][2:3], temp[0][-2:]]
				elif len(temp[0]) == 6:
					ymd_list = [temp[0][:2], temp[0][2:4], temp[0][-2:]]
				elif len(temp[0]) == 8:  # "20230314"의 형식일때
					ymd_list = [temp[0][:4], temp[0][4:6], temp[0][-2:]]
			result = self.change_ymdlist_to_utftime(ymd_list)
		else:
			result = time.localtime(input_time)
		return result

	def change_anytime_to_ymd_list(self, anytime_style):
		"""
		어떤 시간을 2024-10-01처럼 만들어 주는 것
		문자형시간 => [년, 월, 일]

		:param input_text_time: 문자열로된 시간
		:return:
		"""
		dt_obj = self.check_input_time(anytime_style)
		result = self.get_ymd_list_for_dt_obj(dt_obj)
		return result

	def change_dic_time_to_dt_obj(self, input_dic):
		"""
		사전형식의 시간을 datetime객체로 만드는 것
		dic_time : {"yea":2024, "mon" : 2, "day":24, "hou":10, "min":33,"sec":45}와 같은 형식

		:param input_dic:
		:return:
		"""
		temp = self.make_dic_time(input_dic)
		text_time = str(temp["yea"]) + "-" + str(temp["mon"]) + "-" + str(temp["day"]) + "-" + str(
			temp["hou"]) + "-" + str(temp["min"]) + "-" + str(temp["sec"])
		dt_obj = datetime.datetime.strptime(text_time, "%Y-%m-%d-%H-%M-%S")
		return dt_obj

	def change_dt_obj_to_dic_time(self, input_dt_obj=""):
		"""
		datetime객체를 사전형식의 시간으로 바꾸는 것
		dic_time : {"yea":2024, "mon":2, "day":24, "hou":10, "min":33, "sec":45}와 같은 형식

		:param input_dt_obj: datetime객체
		:return:
		"""

		result = self.get_all_infomation_for_dt_obj(input_dt_obj)
		return result

	def change_dt_obj_to_hms_list(self, input_dt_obj=""):
		"""
		datetime객체 => [시, 분, 초]

		:param input_dt_obj: datetime객체
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		temp = input_dt_obj.strftime("%H-%M-%S")
		result = temp.split("-")
		return result

	def change_dt_obj_to_sec(self, input_dt_obj=""):
		"""
		시간 객체를 초로 나타내는 자료형으로 만드는 것
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		result = self.get_all_infomation_for_dt_obj(input_dt_obj)["sec"]
		return result

	def change_dt_obj_to_sec_set(self, input_dt_obj=""):
		"""
		시간 객체를 초로 나타내는 자료형으로 만드는 것

		:param input_dt_obj: datetime객체
		:return: [timestamp, 날짜에대한 초, 나머지초]
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		timestamp = self.get_dt_timestamp_for_dt_obj(input_dt_obj)
		day = int(timestamp / 86400)
		sec = int(timestamp) - day * 86400
		return [timestamp, day, sec]

	def change_dt_obj_to_text_time_with_format(self, input_dt_obj="", input_format="%Y-%m-%d %H:%M:%S"):
		"""
		입력형식으로 되어있는 시간자료를 dt객체로 인식하도록 만드는 것이다
		dt = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")

		:param input_dt_obj: datetime객체, 날짜 객체
		:param input_format:
		:return:
		"""

		input_dt_obj = self.check_dt_obj(input_dt_obj)
		input_format = self.check_time_format(input_format)
		result = input_dt_obj.strftime(input_format)
		return result

	def change_dt_obj_to_timestamp_from_1970(self, input_dt_obj=""):
		"""
		날짜객체 => timestamp로 만드는 것
		timestamp : utc기준으로 1970년 1월1일부터 1초마다 숫자를 더해서 사용
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		result = self.get_all_infomation_for_dt_obj(input_dt_obj)
		print("======> ", result)
		return result["timestamp"]

	def change_dt_obj_to_total_day(self, input_dt_obj=""):
		"""
		시간 객체를 날수로 계산
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		result = self.get_all_infomation_for_dt_obj(input_dt_obj)["day"]
		return result

	def change_dt_obj_to_utc(self, input_dt_obj=""):
		"""
		:param input_dt_obj: datetime객체, 날짜 객체
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		result = input_dt_obj.timestamp() - 32400
		return result

	def change_dt_obj_to_weekno(self, input_dt_obj=""):
		"""
		week_no : 1~7까지의 요일에 대한 숫자, 월요일은 0, 일요일은 6
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		result = input_dt_obj.strftime('%w')
		return result

	def change_dt_obj_to_xy_list(self, input_dt_obj=""):
		"""
		시간을 좌표로 만들어 주는것
		x좌표 : 년월일 (0 ~ 9999*365)
		y좌표 : 시분초 (0 ~ 24*60*60)

		:param input_dt_obj: datetime객체
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		sec_total = self.get_dt_timestamp_for_dt_obj(input_dt_obj)
		hms_list = self.change_dt_obj_to_hms_list(input_dt_obj)
		sec_hms = self.change_hms_list_to_sec(hms_list)
		sec_ymd = sec_total - sec_hms
		return [sec_ymd, sec_hms]

	def change_dt_obj_to_ymd_list(self, input_dt_obj=""):
		"""
		datetime객체 => [년, 월, 일]
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		result = self.get_all_infomation_for_dt_obj(input_dt_obj)["ymd_list"]
		return result

	def change_dt_obj_to_ymd_style_with_connect_char(self, input_dt_obj="", connect_str="-"):
		"""
		datetime는 utc local
		입력문자를 기준으로 yyyy-mm-dd이런 스타일로 만드는 것이다
		시간객체 => 년-월-일

		:param input_dt_obj: datetime객체, 날짜 객체
		:param connect_str: 연결할 문자
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		dic_time = self.change_dt_obj_to_dic_time(input_dt_obj)
		result = dic_time["yea"] + connect_str + dic_time["mon"] + connect_str + dic_time["day"]
		return result

	def change_dt_obj_to_ymdhms_list(self, input_dt_obj=""):
		"""
		datetime객체 => [년, 월, 일, 시, 분, 초]

		:param input_dt_obj: datetime객체
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		result = self.get_all_infomation_for_dt_obj(input_dt_obj)["ymdhms_list"]
		return result

	def change_dt_obj_to_yyyy_mm_dd(self, input_dt_obj=""):
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		temp = self.get_all_infomation_for_dt_obj(input_dt_obj)["ymd_list"]
		result = str(temp[0]) + "-" + str(temp[1]) + "-" + str(temp[2])
		return result

	def change_dt_obj_to_yyyy_mm_dd_ver1(self, input_dt_obj=""):
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		temp = self.get_all_infomation_for_dt_obj(input_dt_obj)["ymd_list"]
		result = str(temp[0]) + "_" + str(temp[1]) + "_" + str(temp[2])
		return result

	def change_formatted_text_time_to_dt_obj_with_format(self, input_text_time, input_format):
		"""
		datetime는 utc local
		formatted_text_time : 간 문자열과 문자열의 형식
		입력한 시간 문자열과 문자열의 형식을 넣어주면 datetime객체를 만들어 준다

		:param input_text_time: 문자열로된 시간
		:param input_format:
		:return:
		"""
		dt_obj = datetime.datetime.strftime(input_text_time, input_format)
		return dt_obj

	def change_formatted_text_to_hms_list(self, hms_list, end_text=["시", "분", "초"]):
		"""
		시분초의 리스트를 텍스트로 연결하는 것

		:param hms_list: [시, 분, 초]
		:param end_text:
		:return:
		"""
		result = f"{hms_list[0]:0> 2}{end_text[0]} {hms_list[1]:0> 2}{end_text[1]} {hms_list[2]:0> 2}{end_text[2]}"
		return result

	def change_hmd_list_to_sec(self, base_day, input_list=[0, 0, 1]):
		"""
		몇년 몇월 몇일을 초로 바꾸는 것
		입력형태 : [몇년, 몇월, 몇일]
		현재일자를 기준으로
		월은 30일 기준으로 계산한다
		기준날짜에서 계산을 하는 것이다
		"""
		total_sec = int(input_list[0]) * 60 * 60 * 24 * 365 + int(input_list[1]) * 60 * 60 * 24 * 30 + int(
			input_list[2]) * 60 * 60 * 24
		return total_sec

	def change_hms_list_to_float(self, hms_list, base="hou"):
		"""
		시간을 숫자로 만들어서 계산을 편하게 만들기 위해서 만들어 본것

		[1,1,30] (1시간 1분 30초) => 61.5
		분:정수부분
		초: 소숫점 아래

		:param hms_list: [시, 분, 초]
		:param base:
		:return:
		"""
		sec_1 = self.change_hms_list_to_sec(hms_list)
		if base == "day":
			result = sec_1 / (60 * 60 * 24)
		elif base == "hou":
			result = sec_1 / (60 * 60)
		elif base == "min":
			result = sec_1 / (60)
		else:
			result = sec_1
		return result

	def change_hms_list_to_sec(self, input_data=""):
		"""
		hmslist : [시, 분, 초]
		출력값 : 초, 입력값으로 온 시분초를 초로 계산한것
		"""
		total_sec = int(input_data[0]) * 3600 + int(input_data[1]) * 60 + int(input_data[2])
		return total_sec

	def change_hms_text_to_sec(self, input_data=""):
		"""
		input_data = "14:06:23" => 초로 변경

		:param input_data:
		:return:
		"""
		re_compile = re.compile("\d+")
		result = re_compile.findall(input_data)
		total_sec = int(result[0]) * 3600 + int(result[1]) * 60 + int(result[2])
		return total_sec

	def change_hour_to_hm_list(self, input_fh):
		"""
		5.5시간을 5시간 30분으로 바꿔주는 것

		:param input_fh:
		:return:
		"""
		big_hour = int(input_fh)
		small_hour = input_fh - int(input_fh)
		minute = int(60 * small_hour)
		return [big_hour, minute]

	def change_input_local_to_utc(self, local_time_zone=9):
		"""
		기본적으로 datetime은 utc와 같은것이라 보면 된다
		:return:
		"""
		KST = datetime.timezone(datetime.timedelta(hours=local_time_zone))
		dt = datetime.datetime.now(datetime.timezone.utc)
		utc_time = dt.replace(tzinfo=KST)
		utc_timestamp = utc_time.timestamp()
		return utc_timestamp

	def change_input_time_to_sec(self, input_data=""):
		"""
		input_data = "14:06:23"
		"""
		re_compile = re.compile("\d+")
		result = re_compile.findall(input_data)
		total_sec = int(result[0]) * 3600 + int(result[1]) * 60 + int(result[2])
		return total_sec

	def change_lunar_day_to_solar_day(self, input_ymd):
		"""
		음력 -> 양력으로 변환시 (음력은 윤달인지 아닌지에대한 기준이 필요하다)
		결과값 : [평달일때의 양력, 윤달일때의 양력]

		:param input_ymd:
		:return:
		"""
		self.lunar_calendar.setLunarDate(input_ymd[0], input_ymd[1], input_ymd[2], False)
		moon_day_1 = self.lunar_calendar.SolarIsoFormat()

		moon_day_2 = ""
		try:
			# 윤달이 없는 달이면, 평달의 날짜를 돌려준다
			self.lunar_calendar.setLunarDate(input_ymd[0], input_ymd[1], input_ymd[2], True)
			moon_day_2 = self.lunar_calendar.SolarIsoFormat()
		except:
			pass
		return [moon_day_1, moon_day_2]

	def change_lunar_day_to_solar_day_1(self, input_data):
		"""
		음력을 양력으로 만들어 주는것

		:param input_data:
		:return:
		"""
		result = []
		for one in input_data:
			if one[3] == "양":
				result.append(one)
			elif one[3] == "음":
				if one[2] == "말일":
					result.append(one)
					input_data[1] = self.check_lunar_last_day_for_lunar_ym_list([one[0], one[1:]])
					self.lunar_calendar.setLunarDate(one[0], input_data[0], input_data[1], False)
					moon_day_1 = self.lunar_calendar.SolarIsoFormat()
					ymd_list = moon_day_1.split("-")
					one = ymd_list + one[3:]
				for num in range(int(one[4])):
					self.lunar_calendar.setLunarDate(one[0], one[1] + num, one[2], False)
					moon_day_1 = self.lunar_calendar.SolarIsoFormat()
					ymd_list = moon_day_1.split("-")
					result.append(ymd_list + ["음", 1] + one[5:])
		return result

	def change_lunar_dt_obj_to_solar_dt_obj(self, input_dt_obj="", yoon_or_not=True):
		"""
		음력을 양력으로 만들어 주는것
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		ymd_list = self.get_ymd_list_for_dt_obj(input_dt_obj)
		self.lunar_calendar.setLunarDate(int(ymd_list[0]), int(ymd_list[1]), int(ymd_list[2]), yoon_or_not)
		result = self.change_any_text_time_to_dt_obj(self.lunar_calendar.SolarIsoFormat())
		return result

	def change_lunar_ymd_to_solar_ymd(self, input_ymd_list, yoon_or_not=True):
		"""
		음력을 양력으로 만들어 주는것

		:param input_ymd_list: [년, 월, 일]
		:param yoon_or_not:
		:return:
		"""
		self.lunar_calendar.setLunarDate(int(input_ymd_list[0]), int(input_ymd_list[1]), int(input_ymd_list[2]),
										 yoon_or_not)
		dt_obj = self.change_any_text_time_to_dt_obj(self.lunar_calendar.SolarIsoFormat())
		result = self.get_ymd_list_for_dt_obj(dt_obj)
		return result

	def change_lunar_ymd_to_solar_ymd_1(self, input_ymd_list, yoon_or_not=True):
		"""
		음력을 양력으로 바꿔주는 기능
		:param input_year:
		:return:
		"""
		lunar_calendar = KoreanLunarCalendar()
		lunar_calendar.setLunarDate(int(input_ymd_list[0]), int(input_ymd_list[1]), int(input_ymd_list[2]), yoon_or_not)

		result = lunar_calendar.SolarIsoFormat()
		if lunar_calendar.solarYear == 0:
			result = "error"
		return result

	def change_month_no_to_eng(self, month):
		"""
		이것은 월을 숫자로 받아서 문자로 돌려주는 것입니다 ---> ['MAR', 'MARCH']

		:param month:
		:return:
		"""
		month_short = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
		month_long = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER',
					  'NOVEMBER', 'DECEMBER']
		return [month_short[month - 1], month_long[month - 1]]

	def change_month_no_to_month_eng(self, month):
		"""
		이것은 월을 숫자로 받아서 문자로 돌려주는 것입니다 ---> ['MAR', 'MARCH']

		:param month:
		:return:
		"""
		month_long = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER',
					  'NOVEMBER', 'DECEMBER']
		return month_long[month - 1]

	def change_num_to_nth_eng_day(self, no):
		"""
		이것은 그날을 서수로 돌려주는 것입니다 ---> ['1ST']

		:param no:
		:return:
		"""
		data = ['1ST', '2ND', '3RD', '4TH', '5TH', '6TH', '7TH', '8TH', '9TH', '10TH', '11TH', '12TH', '13TH', '14TH',
				'15TH', '16TH', '17TH', '18TH', '19TH', '20TH', '21ST', '22ND', '23RD', '24TH', '25TH', '26TH', '27TH',
				'28TH', '29TH', '30TH', '31ST']
		return data[no - 1]

	def change_sec_time(self, input_data=""):
		"""
		추단위의 숫자를 넣으면 날, 시,분, 초로 만들어주는 것

		:param input_data:
		:return:
		"""
		# input_data = 123456
		step_1 = divmod(int(input_data), 60)
		step_2 = divmod(step_1[0], 60)
		final_result = [step_2[0], step_2[1], step_1[1]]
		return final_result

	def change_sec_to_day(self, input_sec):
		"""
		초를 날자로 계산해 주는것
		"""
		nalsu = int(input_sec) / (60 * 60 * 24)
		return nalsu

	def change_sec_to_dhms(self, input_data):
		"""
		초를 날자로 계산해 주는것
		입력값 : 1000초
		출력값 : 2일3시간10분30초
		dhms : day-hour-minute-sec
		"""
		nalsu = int(input_data) / (60 * 60 * 24)
		return nalsu

	def change_sec_to_dhms_list(self, input_sec=""):
		"""
		초 => [날, 시, 분, 초]
		1000초 => 2일3시간10분30초
		dhms : day-hour-minute-sec

		:param input_sec:
		:return:
		"""
		step_1 = divmod(int(input_sec), 60)
		step_2 = divmod(step_1[0], 60)
		day = int(input_sec) / (60 * 60 * 24)
		result = [day, step_2[0], step_2[1], step_1[1]]
		return result

	def change_sec_to_hms(self, input_data=""):
		"""
		초로 넘어온 자료를 기간으로 돌려주는 것
		입력값 : 123456
		"""
		step_1 = divmod(int(input_data), 60)
		step_2 = divmod(step_1[0], 60)
		final_result = [step_2[0], step_2[1], step_1[1]]
		return final_result

	def change_sec_to_hms_list(self, input_sec=""):
		"""
		초를 hour로 바꾸는 것
		input_data = 123456 => 3시간 25분 45초
		입력값 : 123456 => [시, 분, 초]
		:param input_data:
		:return:
		"""
		step_1 = divmod(int(input_sec), 60)
		step_2 = divmod(step_1[0], 60)
		final_result = [step_2[0], step_2[1], step_1[1]]
		return final_result

	def change_solar_dt_obj_to_lunar_dt_obj(self, input_dt_obj="", yoon_or_not=True):
		"""
		날짜 객체인데, 음력의 날짜 객체로 변경하는 것
		음력을 양력으로 만들어 주는것
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		ymd_list = self.get_ymd_list_for_dt_obj(input_dt_obj)
		self.lunar_calendar.setSolarDate(int(ymd_list[0]), int(ymd_list[1]), int(ymd_list[2]))
		result = self.change_any_text_time_to_dt_obj(self.lunar_calendar.LunarIsoFormat())
		return result

	def change_solar_ymd_list_to_lunar_ymd_list(self, input_ymd_list):
		"""
		양력 -> 음력으로 변환시
		결과값 : [음력, 윤달여부]

		:param input_ymd_list: [년, 월, 일]
		:return:
		"""
		self.lunar_calendar.setLunarDate(input_ymd_list[0], input_ymd_list[1], input_ymd_list[2], False)
		lunar_ymd = self.lunar_calendar.LunarIsoFormat()
		yoon_or_not = self.lunar_calendar.isIntercalation()

		return [lunar_ymd, yoon_or_not]

	def change_text_time_to_another_formatted_text_time(self, input_text_time, input_time_format):
		"""
		입력시간을 다른 형식으로 바꾸는 것

		:param input_time_format:
		:param input_format:
		:return:
		"""
		dt_obj = self.check_input_time(input_text_time)
		result = time.strptime(dt_obj, input_time_format)
		return result

	def change_text_time_to_dt_obj(self, input_text_time):
		result = self.check_input_time(input_text_time)
		return result

	def change_text_time_to_utc(self, input_text_time):
		"""
		utc의 timestamp로 변경하는 것

		:param input_text_time:
		:return:
		"""
		dt_obj = self.check_input_time(input_text_time)
		timestamp = self.change_dt_obj_to_utc(dt_obj)
		return timestamp

	def change_text_time_to_ymd_list(self, input_text_time):
		"""
		문자형시간 => [년, 월, 일]

		:param input_text_time: 문자열로된 시간
		:return:
		"""
		dt_obj = self.check_input_time(input_text_time)
		result = self.get_ymd_list_for_dt_obj(dt_obj)
		return result

	def change_time_to_sec(self, input_data=""):
		# input_data = "14:06:23"
		re_compile = re.compile("\d+")
		result = re_compile.findall(input_data)
		total_sec = int(result[0]) * 3600 + int(result[1]) * 60 + int(result[2])
		return total_sec

	def change_time_to_utftime(self, input_data=""):
		"""
		현재의시간을 돌려준다
		입력값이 ""이면 지금의 시간을 뜻한다
		시간형태 : 1648037614.4801838 (의미 : 2022-03-23T21:13:34.480183+09:00)
		"""
		localtime = self.change_anytime_to_utftime(input_data)
		atime = arrow.get(localtime)
		result = atime.timestamp()
		return result

	def change_timestamp_to_utc(self, input_timestamp):
		"""
		숫자형으로된 시간을 utc로 바꾸는 것
		utc : utc의 timestamp, utc시간숫자, 1640995200.0 또는 ""

		:param input_timestamp:
		:return:
		"""
		result = time.gmtime(input_timestamp)
		return result

	def change_utc_to_dt_obj(self, input_utc):
		"""
		utc : utc의 timestamp, utc시간숫자, 1640995200.0 또는 ""
		utc  : 1970년 1월 1일을 0밀리초로 계산한 것
		utc  : 1640995200.0 또는 "", 1648037614.4801838 (의미 : 2022-03-23T21  13:34.480183+09:00)
		datetime : 1900.1.1을 1초로 시작

		:param input_utc:
		:return:
		"""
		input_utc = self.check_input_utc(input_utc)

		dt_timestamp = input_utc + 1640995200
		dt_obj = self.change_anytime_to_dt_obj(dt_timestamp)
		return dt_obj

	def change_utc_to_end_of_day_for_month(self, input_utc=""):
		"""
		입력한 날짜나 시간의 마지막날을 게산하는것
		입력값 : 시간 또는 날짜
		출력값 : 그달의 마지막날
		"""
		input_utc = self.check_input_utc(input_utc)
		lt = self.change_anytime_to_utc(input_utc)
		result = time.strftime('%W', lt)
		return result

	def change_utc_to_text_time_as_format(self, input_utc, format_a):
		"""
		utc : utc의 timestamp, utc시간숫자, 1640995200.0 또는 ""

		:param input_utc:
		:param format_a:
		:return:
		"""
		input_utc = self.check_input_utc(input_utc)
		result = self.set_format_for_utc(format_a, input_utc)
		return result

	def change_utc_to_timedic(self, input_data=""):
		"""
		입력된 시간에 대한 왠만한 모든 형식의 날짜 표현을 사전형식으로 돌려준다
		"""
		lt = self.change_anytime_to_utc(input_data)

		# s는 short, e는 english, l은 long
		year_s = time.strftime('%y', lt)
		year = time.strftime('%Y', lt)

		mon = time.strftime('%m', lt)
		mon_e = time.strftime('%b', lt)
		mon_e_l = time.strftime('%B', lt)

		day = time.strftime('%d', lt)
		day_l = time.strftime('%j', lt)

		week_no = time.strftime('%w', lt)
		yearweekno = time.strftime('%W', lt)
		week_e = time.strftime('%a', lt)
		week_e_l = time.strftime('%A', lt)

		hour = time.strftime('%I', lt)
		hour_l = time.strftime('%H', lt)
		ampm = time.strftime('%p', lt)
		min = time.strftime('%M', lt)
		sec = time.strftime('%S', lt)
		result = {"year_s": year_s, "year": year,
				  "month": mon, "mon": mon, "mon_e": mon_e, "mon_e_l": mon_e_l,
				  "day": day, "day_l": day_l,
				  "hour": hour, "hour_l": hour_l,
				  "ampm": ampm,
				  "min": min, "minute": min,
				  "sec": sec, "second": sec,
				  "week_no": week_no, "week_e": week_e, "week_e_l": week_e_l, "yearweekno": yearweekno}
		return result

	def change_utc_to_ymd_dash(self, input_utc):
		"""
		utc : utc의 timestamp, utc시간숫자, 1640995200.0 또는 ""

		utc를 2023-2-2형태로 돌려주는 것

		:param input_utc: utc 시간객체
		:return:
		"""
		input_utc = self.check_input_utc(input_utc)
		result = time.strftime('%Y-%m-%d', input_utc)
		return result

	def change_utc_to_ymd_list(self, input_utc):
		"""
		utc : utc의 timestamp, utc시간숫자, 1640995200.0 또는 ""

		:param input_utc: utc 시간객체
		:return:
		"""
		input_utc = self.check_input_utc(input_utc)

		year = time.strftime('%Y', input_utc)
		month = time.strftime('%m', input_utc)
		day = time.strftime('%d', input_utc)
		result = [year, month, day]
		return result

	def change_utftime_to_day_list(self, input_data=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		일 -----> ['05']
		닞은숫자 -> 많은글자 순으로 정리
		"""
		utf_local_time = self.change_anytime_to_utftime(input_data)
		day = time.strftime('%d', utf_local_time)
		day_l = time.strftime('%j', utf_local_time)
		result = [day, day_l]
		return result

	def change_utftime_to_end_of_day_for_month(self, input_data=""):
		"""
		입력한 날짜나 시간의 마지막날을 게산하는것
		입력값 : 시간 또는 날짜
		출력값 : 그달의 마지막날
		"""
		lt = self.change_anytime_to_utftime(input_data)
		result = time.strftime('%W', lt)
		return result

	def change_utftime_to_hour_list(self, input_data=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		시 -----> ['10', '22']
		닞은숫자 -> 많은글자 순으로 정리
		"""
		utf_local_time = self.change_anytime_to_utftime(input_data)
		hour = time.strftime('%I', utf_local_time)
		hour_l = time.strftime('%H', utf_local_time)
		result = [hour, hour_l]
		return result

	def change_utftime_to_time_dic(self, input_data=""):
		"""
		입력된 시간에 대한 왠만한 모든 형식의 날짜 표현을 사전형식으로 돌려준다
		"""
		lt = self.change_anytime_to_utftime(input_data)

		# s는 short, e는 english, l은 long
		year_s = time.strftime('%y', lt)
		year = time.strftime('%Y', lt)

		mon = time.strftime('%m', lt)
		mon_e = time.strftime('%b', lt)
		mon_e_l = time.strftime('%B', lt)

		day = time.strftime('%d', lt)
		day_l = time.strftime('%j', lt)

		week_no = time.strftime('%w', lt)
		yearweek_no = time.strftime('%W', lt)
		week_e = time.strftime('%a', lt)
		week_e_l = time.strftime('%A', lt)

		hour = time.strftime('%I', lt)
		hour_l = time.strftime('%H', lt)
		ampm = time.strftime('%p', lt)
		min = time.strftime('%M', lt)
		sec = time.strftime('%S', lt)
		result = {"year_s": year_s, "year": year,
				  "month": mon, "mon": mon, "mon_e": mon_e, "mon_e_l": mon_e_l,
				  "day": day, "day_l": day_l,
				  "hour": hour, "hour_l": hour_l,
				  "ampm": ampm,
				  "min": min, "minute": min,
				  "sec": sec, "second": sec,
				  "week_no": week_no, "week_e": week_e, "week_e_l": week_e_l, "yearweek_no": yearweek_no}
		return result

	def change_yearweekno_to_ymd_list_for_monday(self, input_year, input_yearweekno):
		"""
		년도, 위크번호 ==> 그주의 월요일

		:param input_year:
		:param input_yearweekno:
		:return:
		"""
		text_time = f"{input_year}-{input_yearweekno}"
		dt_obj = datetime.datetime.strptime(text_time + '-1', "%Y-%W-%w")
		result = self.get_ymd_list_for_dt_obj(dt_obj)
		return result

	def change_ymd_list_to_dt_obj(self, input_ymd_list):
		"""

		:param input_text_time: 문자열로된 시간
		:return:
		"""
		dt_obj = self.check_input_time(input_ymd_list)
		return dt_obj

	def change_ymd_list_to_sec(self, input_list):
		"""
		[년, 월, 일] => 초

		:param input_list:
		:return:
		"""
		total_sec = int(input_list[0]) * self.vars["year_sec"] + int(input_list[1]) * self.vars["month_sec"] + int(
			input_list[2]) * self.vars["day_sec"]
		return total_sec

	def change_ymd_list_to_utc(self, input_list):
		"""
		입력 : [년, 월, 일]
		출력 : utc값
		"""
		atime = arrow.get(int(input_list[0]), int(input_list[1]), int(input_list[2]))
		result = atime.timestamp()
		return result

	def change_ymd_list_to_yearweekno(self, input_ymd_list=""):
		"""
		yearweekno : 1년에서 몇번째 주인지 아는것
		입력한날의 week 번호를	계산
		입력값 : 날짜

		:param input_date:
		:return:
		"""
		if input_ymd_list == "":
			today = self.get_yyyy_mm_dd_for_today()
			year, month, day = today.split("-")
			dt_obj = self.check_input_time([year, month, day])
		else:
			dt_obj = self.change_any_text_time_to_dt_obj(input_ymd_list)
		result = int(dt_obj.strftime("%W"))
		return result

	def change_ymdhms_list_to_dt_obj(self, input_ymdhms_list):
		"""
		[2023, 3, 1, 0, 0, 0] => datetime객체
		:param input_ymdhms_list:
		:return:
		"""
		dt_obj = ""
		temp = ""
		for one in input_ymdhms_list:
			temp = temp + str(one) + "-"
			dt_obj = datetime.datetime.strptime(temp[:-1], "%Y-%m-%d-%H-%M-%S")
		return dt_obj

	def change_ymdlist_to_utftime(self, input_list):
		"""
		입력 : [년, 월, 일]
		출력 : utc값
		"""
		atime = arrow.get(int(input_list[0]), int(input_list[1]), int(input_list[2]))
		result = atime.timestamp()
		return result

	def change_yyyy_mm_dd_to_dt_obj(self, input_iso_format="2023-03-01"):
		"""
		date 클래스의 isoformat()  : YYYY-MM-DD의 형식

		:param input_iso_format:
		:return:
		"""
		dt_obj = datetime.datetime.fromisoformat(input_iso_format)
		return dt_obj

	def check_datetime(self, input_data):
		"""

		:param input_data:
		:return:
		"""
		print(type(input_data), input_data)
		if isinstance(input_data, (list, tuple)):
			result = []
			for one in input_data:
				aa = self.check_datetime(one)
				result.append(aa)
				return result
		elif isinstance(input_data, (pywintypes.TimeType)):
			# print(type(input_data), input_data)
			temp = str(input_data).split("")
			if temp[1] == "0 군00:00+00:00":
				result = temp[0]
			else:
				aaa = temp[0] + "" + temp[1].split("+")[0]
				result = aaa
			return result
		elif isinstance(input_data, (float)):
			if 0 < input_data < 1:
				print("l 보다 작은 정수 =>", input_data)
				return input_data
			elif isinstance(input_data, set):
				return set(self.check_datetime(x) for x in input_data)
			else:
				# print(type(input_data), input__data)
				return input_data

	def check_day_or_not(self, input_list):
		"""
		입력된 자료들이 년을 나타내는 자료인지를 확인하는것

		:param input_list:
		:return:
		"""
		result = []
		alphabet = "abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz".upper()
		if type(input_list[0]) == type([]):
			changed_input_list = input_list
		else:
			changed_input_list = []
			for one in input_list:
				changed_input_list.append([one])

		for one_list in changed_input_list:
			if str(one_list[0])[0] in alphabet:
				# 알파벳으로 사용하는것은 월밖에 없다
				result.append(False)
			else:
				if len(str(one_list[0])) == 4:
					# 4개의 숫자는 년도를 나타내는 것
					result.append(False)
				elif len(one_list[0]) <= 2:
					result.append(True)

				if int(one_list[0]) > 31:
					# 31보다 크면, 년도이다
					result.append(False)
				else:
					# 12보다 크면, 월을 나타내는것이 아니다
					result.append(True)

		total_num = 0
		for one in result:
			total_num = total_num + one

		# 전체중에서 1보다 넘으면 년을 쓰인것으로 본다
		# 숫자가 2개이하인것과 12이상일때, 두번 True로 만들기때문에...
		if total_num / len(result) > 1:
			month_or_not = True
		else:
			month_or_not = False
		return month_or_not

	def check_dt_obj(self, input_dt_obj=""):
		"""
		datetime객체를 만드는 것
		:param input_dt_obj:
		:return:
		"""
		if not input_dt_obj:
			input_dt_obj = self.get_dt_obj_for_now()
		return input_dt_obj

	def check_holiday_on_year(self, input_year, input_data):
		"""
		입력받은 공휴일 자료중에서 양력으로 된것은 그대로 저장하고
		음력으로 된것을 양력 날짜로 바꾸는것

		:param input_year:
		:param input_data:
		:return:
		"""
		result = []
		if input_data[2] == "양":
			dt_obj = self.change_ymd_list_to_dt_obj([input_year, input_data[0], input_data[1]])
		elif input_data[2] == "음":
			if input_data[1] == "말일":
				input_data[1] = self.check_lunar_last_day_for_lunar_ym_list([input_year, input_data[0]])

			self.lunar_calendar.setLunarDate(input_year, input_data[0], input_data[1], False)
			dt_obj = self.change_any_text_time_to_dt_obj(self.lunar_calendar.SolarIsoFormat())

		week_no_7 = self.get_no_of_sunday_in_same_week_for_dt_obj(dt_obj)
		new_ymd_list = self.get_ymd_list_for_dt_obj(dt_obj)
		for index in range(int(input_data[3])):
			checked_ymd_list = self.check_ymd_list([new_ymd_list[0], new_ymd_list[1], int(new_ymd_list[2]) + index])
			result.append(
				[checked_ymd_list[0], checked_ymd_list[1], checked_ymd_list[2], divmod(int(week_no_7) + index, 7)[1],
				 input_data[-1]])
		return result

	def check_input_date(self, input_data):
		"""
		날짜형식이 들어오면 그것을 다시 확인하는것
		"""
		result = ""
		if type([]) == type(input_data):
			# 만약 입력형태가 리스트이면
			if len(input_data) == 3:
				result = input_data
		elif type("string") == type(input_data):
			# 만약 입력형태가 문자열이면
			re_compiled = re.compile("\d+")
			temp = re.findall(re_compiled, input_data)
			print(temp)
			if len(temp) == 3:
				result = temp
			elif len(temp) == 1:
				if len(temp[0]) == 6:
					result = [temp[0][:2], temp[0][2:4], temp[0][-2:]]
				elif len(temp[0]) == 8:
					result = [temp[0][:4], temp[0][4:6], temp[0][-2:]]
		return result

	def check_input_datetime(self, input_date=""):
		"""

		:param input_date:
		:return:
		"""
		months = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6, "JUL": 7, "AUG": 8, "SEP": 9,
				  "OCT": 10, "NOV": 11, "DEC": 12, "JANUARY": 1, "FEBRUARY": 2, "MARCH": 3, "APRIL": 4, "JUNE": 6,
				  "JULY": 7, "AUGUST": 8, "SEPTEMBER": 9, "OCTOBER": 10, "NOVEMBER": 11, "DECEMBER": 12}
		if input_date == "":
			# 아무것도 입력하지 않으 면 local time 으로 인식한다
			self.lt = time.localtime()
			self.year = int(time.strftime("%Y", self.lt))
			self.month = int(time.strftime("%m", self.lt))
			self.day = int(time.strftime("%d", self.lt))
			self.lt_utc = datetime.datetime(self.year, self.month, self.day).timestamp()

		elif type(input_date) == type(float(123.00)):
			# 실수일 경우는 localutc로 인식한다
			self.lt_utc = time.localtime(float(input_date))
			self.year = int(time.strftime("%Y", self.lt_utc))
			self.month = int(time.strftime("%m", self.lt_utc))
			self.day = int(time.strftime("%d", self.lt_utc))
		elif type(input_date) == type([]):
			# 리스트 형태의 경우 : [2022t 1f 3]
			if len(input_date) >= 3:
				self.year, self.month, self.day = int(input_date[0]), int(input_date[1]), int(input_date[2])
				self.jt_utc = datetime.datetime(self.year, self.month, self.day).timestamp()

		elif type("string") == type(input_date) or type(int(123)) == type(input_date):
			#  만약 입력형태가 문자열이면
			#  "202201Or", "22/mar/01","22mar01"
			input_date = str(input_date)
			re_compiled = re.compile("Wd+")
			temp = re.findall(re_compiled, input_date)
			re_str = re.compile("[a-zA-Z]+")

			temp_str = re.findall(re_str, input_date)
			if len(temp) == 3:
				self.year, self.month, self.day = [int(temp[0]), int(temp[1]), int(temp[2])]
			elif len(temp) == 1:
				if len(temp[0]) == 6:
					self.year, self.month, self.day = [int(temp[0][:2]), int(temp[0][2:4]), int(temp[0][-2:])]
			elif len(temp[0]) == 8:
				self.year, self.month, self.day = [int(temp[0][:4]), int(temp[0][4:6]), int(temp[0][-2:])]
			elif len(temp) == 2 and len(temp_str) == 1:
				if temp_str[0] in list(months.keys()):
					self.year, self.month, self.day = [int(temp[0]), int(months[str(temp_str[0]).upper()]),
													   int(temp[1])]
					self.lt_utc = datetime.datetime(self.year, self.month, self.day).timestamp()

	def check_input_time(self, input_text_time=""):
		"""
		어떤 형태가 들어오더라도 datetime으로 돌려주는 것

		:param input_text_time: 문자열로된 시간
		:return:
		"""
		if input_text_time == "":
			# 아무것도 입력하지 않으면 local time 으로 인식한다
			result = datetime.datetime.now()

		elif type(input_text_time) == type(datetime.datetime.now()):
			# 만약 datetime객체일때
			result = input_text_time
		elif type(input_text_time) == pywintypes.TimeType:
			# 만약 datetime 객체일때
			result = input_text_time

		elif type(input_text_time) == type(float(123.00)) or type(input_text_time) == type(int(123.00)):
			# timestamp로 인식
			result = datetime.datetime.fromtimestamp(input_text_time)

		elif type("string") == type(input_text_time):
			#  만약 입력형태가 문자열이면 : "202201O", "22/mar/01","22mar01"
			result = self.change_any_text_time_to_dt_obj(input_text_time)

		elif type(input_text_time) == type([]):
			# 리스트 형태의 경우
			if len(input_text_time) >= 3:
				self.year, self.month, self.day = int(input_text_time[0]), int(input_text_time[1]), int(
					input_text_time[2])
				result = datetime.datetime(self.year, self.month, self.day)
		else:
			result = datetime.datetime.now()
		return result

	def check_input_time_1(self, input_data=""):
		"""
		입력 : utc, 입력값이 시간일때
		출력 : localtime값, 1575142526.500323
		만약 입력값이 없으면 지금 시간의 localtime값을 돌려준다
		"""
		if input_data == "":
			result = time.localtime()
		elif type(input_data) == type([]) and len(input_data) == 3:
			result = self.change_ymd_list_to_utc(input_data)
		else:
			result = time.localtime(input_data)
		return result

	def check_input_time_char(self, time_char=""):
		"""

		:param time_char:
		:return:
		"""
		if time_char == "":
			result = time.localtime()
		else:
			result = time.localtime(time_char)
		return result

	def check_input_utc(self, input_utc=""):
		if input_utc == "":
			input_utc = self.get_utc_for_now()
		return input_utc

	def check_lunar_last_day_for_lunar_ym_list(self, input_ym_list):
		"""
		음력으로 말일을 찾는것

		:param input_ym_list: [년, 월]
		:return:
		"""
		result = 26
		for nun in range(27, 31):
			self.lunar_calendar.setLunarDate(input_ym_list[0], input_ym_list[1], nun, False)
			temp = self.lunar_calendar.SolarIsoFormat()
			ymd_list = temp.split("-")
			if int(ymd_list[2]) >= result:
				print("말일 찾기 ==> ", result)
				result = int(ymd_list[2])
			else:
				break
		return result

	def check_month_or_not(self, input_list):
		"""
		입력된 자료들이 월을 나타내는 자료인지를 확인하는것

		:param input_list:
		:return:
		"""
		result = []
		alphabet = "abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz".upper()
		if type(input_list[0]) == type([]):
			changed_input_list = input_list
		else:
			changed_input_list = []
			for one in input_list:
				changed_input_list.append([one])

		for one_list in changed_input_list:
			if str(one_list[0])[0] in alphabet:
				# 알파벳으로 사용하는것은 월밖에 없다
				result.append(True)
			else:
				if len(str(one_list[0])) == 4:
					# 4개의 숫자는 년도를 나타내는 것
					result.append(False)
				elif int(one_list[0]) > 31:
					# 31보다 크면, 년도이다
					result.append(False)
				elif int(one_list[0]) > 12 and int(one_list[0]) <= 31:
					# 12보다 크면, 월을 나타내는것이 아니다
					result.append(True)
		total_num = 0
		for one in result:
			total_num = total_num + one

		# 전체중에서 70%가 넘으면 월로쓰인것으로 본다
		if total_num / len(result) > 0.9:
			month_or_not = True
		else:
			month_or_not = False

		return month_or_not

	def check_next_day_of_holiday(self, holiday_list, input_list_2d):
		"""
		대체공휴일을 확인하는것
		일요일인것만, 리스트로 만들어 준다

		:param holiday_list:
		:param input_list_2d:
		:return:
		"""
		result = []
		if holiday_list == "all":
			for list_1d in input_list_2d:
				temp = []
				sunday = 0
				for one in list_1d:
					if one[3] == 0:    sunday = 1
					one[2] = int(one[2]) + sunday
					temp.append(one)
				result.append(temp)
		else:
			for list_1d in input_list_2d:
				temp = []
				if list_1d in holiday_list:
					sunday = 0
					for one in list_1d:
						if one[3] == 0:  # 일요일의 값인 0이 있다면...
							sunday = 1
						one[2] = int(one[2]) + sunday
						temp.append(one)
					result.append(temp)
				else:
					result.append(list_1d)

		return result

	def check_solar_day_for_last_day_of_lunar_ym_list(self, input_ym_list, yoon_or_not=True):
		"""
		음력으로 입력된 것중에 말일이라고 된것의 양력날짜를 구하는 것
		yoon_or_not : 윤달인지 아닌지에 대한 설정

		:param input_ym_list: [년, 월]
		:param yoon_or_not:
		:return:
		"""
		for num in range(27, 31):
			try:
				# 윤달이 아닌 날짜를 기준으로 확인
				self.lunar_calendar.setLunarDate(int(input_ym_list[0]), int(input_ym_list[1]), num, yoon_or_not)
				dt_obj = self.change_any_text_time_to_dt_obj(self.lunar_calendar.SolarIsoFormat())
				ymd_list = self.get_ymd_list_for_dt_obj(dt_obj)
			except:
				break
		return ymd_list

	def check_text_time_with_jf_sql(self, input_text_time, jf_sql):
		"""
		jf_sql = "[숫자:1~2](시간|시)[숫자:1~2](분)[숫자:0~2](초)[0~1]"

		:param input_text_time:
		:param jf_sql:
		:return:
		"""
		result = self.xyre.search_all_by_jf_sql(input_text_time, jf_sql)
		return result

	def check_time_format(self, input_text="년-월"):
		"""
		한글을 사용가능하도록 만들기 위한것
		:param input_text:
		:return:
		"""
		dic_data = {"년": "%Y", "월": "%m", "일": "%d", "시": "%H", "분": "%M", "초": "%S", }
		for one_key in dic_data.keys():
			input_text = input_text.replace(one_key, dic_data[one_key])
		return input_text

	def check_time_input_data(self, time_char=""):
		"""

		:param time_char:
		:return:
		"""
		self.time_char = time_char
		if self.time_char == "":
			lt = time.localtime()
		else:
			lt = time.localtime(self.time_char)
		return self.time_char

	def check_time_list2d(self, time_char=""):
		"""

		:param time_char:
		:return:
		"""
		self.time_char = time_char
		if self.time_char == "":
			lt = time.localtime()
		else:
			lt = time.localtime(self.time_char)
		return self.time_char

	def check_two_hms_list(self, hms_list_1, hms_list_2):
		"""
		기준시간을 기준으로 삼아서, 두번째 시간이 그것보다 앞인지 뒤인지를 나타내는것

		:param hms_list_1:
		:param hms_list_2:
		:return:
		"""
		sec_1 = self.change_hms_list_to_sec(hms_list_1)
		sec_2 = self.change_hms_list_to_sec(hms_list_2)
		if sec_1 >= sec_2:
			result = "기준시간 초과"
		else:
			result = "기준시간 이전"
		return result

	def check_type_for_time(self, input_value):
		"""

		:param input_value:
		:return:
		"""
		result = False
		if type(input_value) is pywintypes.TimeType:
			result = str(input_value)
		return result

	def check_year_or_not(self, input_list):
		"""
		입력된 자료들이 년을 나타내는 자료인지를 확인하는것

		:param input_list:
		:return:
		"""
		result = []
		alphabet = "abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz".upper()
		if type(input_list[0]) == type([]):
			changed_input_list = input_list
		else:
			changed_input_list = []
			for one in input_list:
				changed_input_list.append([one])

		for one_list in changed_input_list:
			if str(one_list[0])[0] in alphabet:
				# 알파벳으로 사용하는것은 월밖에 없다
				result.append(False)
			else:
				if len(str(one_list[0])) == 4:
					# 4개의 숫자는 년도를 나타내는 것
					result.append(True)
				elif int(one_list[0]) > 31:
					# 31보다 크면, 년도이다
					result.append(True)
				elif int(one_list[0]) > 12 and int(one_list[0]) <= 31:
					# 12보다 크면, 월을 나타내는것이 아니다
					result.append(False)
		total_num = 0
		for one in result:
			total_num = total_num + one

		# 전체중에서 70%가 넘으면 년을 쓰인것으로 본다
		if total_num / len(result) > 0.5:
			month_or_not = True
		else:
			month_or_not = False
		return month_or_not

	def check_ymd_list(self, input_ymd_list):
		"""
		YMD리스트로 들어온값이 월과 일을 넘는 숫자이면 이것을 고치는것
		[2000, 14, 33] ==> [2001, 3, 31]

		:param input_ymd_list: [년, 월, 일]
		:return:
		"""
		year = int(input_ymd_list[0])
		month = int(input_ymd_list[1])
		day = int(input_ymd_list[2])
		if month > 12:
			year = year + divmod(month, 12)[0]
			month = divmod(month, 12)[1]
			if month == 0:
				year = year - 1
				month = 12

		if day > 25:
			delta_day = day - 25
			dt_obj = self.change_ymd_list_to_dt_obj([year, month, 25])
			dt_obj = self.shift_day_for_dt_obj(dt_obj, delta_day)
		else:
			dt_obj = self.change_ymd_list_to_dt_obj([year, month, day])

		result = self.get_ymd_list_for_dt_obj(dt_obj)
		return result

	def check_ymd_list_1(self, year, one_list):
		"""
		윤년의 날짜가 많이 틀려질수가 있어서, 12월은 "말일"이라는 단어를 쓰기때문에 이런것들을 확인하는 기능임
		현재 년도의 음력값을 갖고온다

		:param year:
		:param one_list:
		:return:
		"""
		if one_list[1][2] == "음":
			# "말일"이라는 단어가 있다면, 음력의 말일을 찾아서 넣는것이다
			if one_list[1][1] == "말일":
				one_list[1][1] = self.get_last_day_of_yyyymm_for_lunar(year, one_list[1][0])

			# 음력의 날짜를 양력의 날짜로 변경
			result = self.change_lunar_ymd_to_solar_ymd([year, one_list[1][0], one_list[1][1]], True)
			if result == "error": pass

		if one_list[1][2] == "양":
			result = [year, one_list[1][0], one_list[1][1]]
		return result

	def combine_date_obj_and_time_obj(self, input_date_obj, input_time_obj):
		"""
		날짜객체와 시간객체를 하나로 만드는 것

		:param input_date_obj:
		:param input_time_obj:
		:return:
		"""
		dt_obj = datetime.datetime.combine(input_date_obj, input_time_obj)
		return dt_obj

	def data_for_time_zone(self):
		"""

		:return:
		"""
		local_name = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
		sec = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
		hour = int(sec / 3600) * -1
		return [hour, local_name]

	def data_national_holiday_in_year(self, input_ymd_list1, input_ymd_list2):
		"""
		입력한 해의 국정공휴일을 반환해 주는 것이다
		[공휴일지정 시작일, 공휴일지정 끝나는날],[공휴일 월, 일, 음/양, 몇일간 연속된것인지, 윤달여부, 공휴일의 이름]

		:param input_ymd_list1:
		:param input_ymd_list2:
		:return:
		"""

		holiday_list2d = self.vars["holiday_list"]

		# 전체적으로 사용되는 변수들
		result_sun = []
		end_ymd_list_moon = self.shift_day_for_ymd_list(input_ymd_list2, 62)
		base_start_no = int(input_ymd_list1[0]) * 10000 + int(input_ymd_list1[1]) * 100 + int(input_ymd_list1[2])
		base_end_no = int(input_ymd_list2[0]) * 10000 + int(input_ymd_list2[1]) * 100 + int(input_ymd_list2[2])

		# 양력의 자료에 대해서 구한것
		period_list_sun = self.split_period_as_year_basis(input_ymd_list1, input_ymd_list2)
		for start_ymd_list, end_ymd_list in period_list_sun:
			year = int(start_ymd_list[0])
			for one_holiday in holiday_list2d:
				# 위의 자료를 모두 확인해서, 입력한 년도와 관계있는것만 골라내는 것
				if one_holiday[1][2] == "양":
					holiday_no = year * 10000 + int(one_holiday[1][0]) * 100 + int(one_holiday[1][1])
					if base_start_no <= holiday_no and base_end_no >= holiday_no and one_holiday[0][0] <= holiday_no and \
							one_holiday[0][1] >= holiday_no:
						result_sun.append([year, int(one_holiday[1][0]), int(one_holiday[1][1])] + one_holiday[1])

		# 음력중 평달인것만 구한것
		# 음력을 변환했을때의 양력날짜는 양력의 날짜보다 클수가 없다. 그래서 음력의 기간을 다시 설정하는 것이다
		period_list_moon = self.split_period_as_year_basis(input_ymd_list1, end_ymd_list_moon)

		for start_ymd_list, end_ymd_list in period_list_moon:
			year = int(start_ymd_list[0])

			for one_holiday in holiday_list2d:
				# 위의 자료를 모두 확인해서, 입력한 년도와 관계있는것만 골라내는 것
				if one_holiday[1][2] == "음":
					if one_holiday[1][1] == "말일":
						ymd_list_moon = self.check_lunar_last_day_for_lunar_ym_list([year, one_holiday[1][0]])
					else:
						ymd_list_moon = [year, one_holiday[1][0], one_holiday[1][1]]

					self.lunar_calendar.setLunarDate(ymd_list_moon[0], ymd_list_moon[1], ymd_list_moon[2], True)

					ymd_list_sun = self.change_lunar_ymd_to_solar_ymd(ymd_list_moon)
					holiday_no = int(ymd_list_sun[0]) * 10000 + int(ymd_list_sun[1]) * 100 + int(ymd_list_sun[2])

					if base_start_no <= holiday_no and base_end_no >= holiday_no and one_holiday[0][0] <= holiday_no and \
							one_holiday[0][1] >= holiday_no:
						result_sun.append(ymd_list_sun + one_holiday[1])
		return result_sun

	def delay(self, input_sec):
		"""
		time.sleep를 실행시키는 것

		:param input_sec:
		:return:
		"""
		time.sleep(input_sec)

	def delta_two_anytime_result_as_day(self, input_date1, input_date2):
		"""
		두날짜의 빼기

		:param input_date1:
		:param input_date2:
		:return:
		"""
		dt_obj_1 = self.change_any_text_time_to_dt_obj(input_date1)
		dt_obj_2 = self.change_any_text_time_to_dt_obj(input_date2)

		result = abs((float(dt_obj_1.timestamp()) - float(dt_obj_2.timestamp())) / (60 * 60 * 24))
		return result

	def delta_two_date(self, date_1, date_2):
		"""
		두날짜의 시간을 빼는 것

		:param date_1:
		:param date_2:
		:return:
		"""
		result = self.minus_date1_date2(date_1, date_2)
		return result

	def delta_two_dt_obj_output_as_day(self, input_date1, input_date2):
		"""
		두날짜의 빼기
		날짜로 만 나타내는 것

		:param input_date1:
		:param input_date2:
		:return:
		"""
		dt_obj_1 = self.change_any_text_time_to_dt_obj(input_date1)
		dt_obj_2 = self.change_any_text_time_to_dt_obj(input_date2)

		result = abs((float(dt_obj_1.timestamp()) - float(dt_obj_2.timestamp())) / (60 * 60 * 24))
		return result

	def delta_two_hms_list(self, input_hms_1, input_hms_2):
		"""
		hms_list : [시, 분, 초]
		두 시간에 대한 차이를 hms 형태로 돌려주는 것

		:param input_hms_1:
		:param input_hms_2:
		:return:
		"""
		sec_1 = self.change_hms_list_to_sec(input_hms_1)
		sec_2 = self.change_hms_list_to_sec(input_hms_2)
		delta_sec = abs(int(sec_2 - sec_1))
		result = self.change_sec_to_hms_list(delta_sec)
		return result

	def delta_two_ymd_list(self, input_hms_list_1, input_hms_list_2):
		"""
		hms_list : [시, 분, 초]
		두 시간에 대한 차이를 hms 형태로 돌려주는 것

		:param input_hms_list_1:
		:param input_hms_list_2:
		:return:
		"""
		sec_1 = self.change_hms_list_to_sec(input_hms_list_1)
		sec_2 = self.change_hms_list_to_sec(input_hms_list_2)
		delta_sec = abs(int(sec_2 - sec_1))
		result = self.change_sec_to_hms_list(delta_sec)
		return result

	def differance_two_dt_obj(self, input_dt_obj_1, input_dt_obj_2):
		"""
		날짜의 차이

		:param input_dt_obj_1:
		:param input_dt_obj_2:
		:return:
		"""
		if input_dt_obj_1 > input_dt_obj_2:
			input_dt_obj_2, input_dt_obj_1 = input_dt_obj_1, input_dt_obj_2

		base_ymd_list = self.get_ymd_list_for_dt_obj(input_dt_obj_1)
		day_no_for_one_month_before = self.get_last_day_of_month_for_ym_list([base_ymd_list[0], base_ymd_list[1] - 1])
		ymd_list_2 = self.get_ymd_list_for_dt_obj(input_dt_obj_2)

		if base_ymd_list[2] - ymd_list_2[2] <= 0:
			base_ymd_list[2] = base_ymd_list[2] + day_no_for_one_month_before
			base_ymd_list[1] = base_ymd_list[1] - 1

	def get_1st_day_N_last_day_for_yms_list(self, input_ymslist):
		"""
		입력으로 들어온 날짜를 기준으로 그 월의 시작날짜와 끝날짜를 돌려주는 것

		:param input_ymslist:
		:return:
		"""
		date = datetime.datetime(year=input_ymslist[0], month=input_ymslist[1], day=1).date()
		monthrange = calendar.monthrange(date.year, date.month)
		first_day = calendar.monthrange(date.year, date.month)[0]
		last_day = calendar.monthrange(date.year, date.month)[1]
		return [date, monthrange, first_day, last_day]

	def get_1st_day_n_last_day_for_ym_list(self, input_ym_list):
		"""
		[2023, 05] => [(1,31), 1, 31]

		:param input_ym_list: [년, 월]
		:return:
		"""
		date = datetime.datetime(year=input_ym_list[0], month=input_ym_list[1], day=1).date()
		monthrange = calendar.monthrange(date.year, date.month)
		first_day = calendar.monthrange(date.year, date.month)[0]
		last_day = calendar.monthrange(date.year, date.month)[1]
		return [date, monthrange, first_day, last_day]

	def get_7_day_list_for_yearweekno(self, year, week_no):
		"""
		일요일부터 시작하는 7개의 날짜를 돌려준다
		"""
		str_datetime = f'{year} {week_no} 0'
		startdate = datetime.datetime.strptime(str_datetime, '%Y %W %w')
		dates = [startdate.strftime('%Y-%m-%d')]
		for i in range(1, 7):
			day = startdate + datetime.timedelta(days=i)
			dates.append(day.strftime('%Y-%m-%d'))
		return dates

	def get_all_day_list_for_year_month(self, input_year, input_month):
		"""
		년과 월을 주면, 한달의 리스트를 알아내는것
		월요일부터 시작

		:param input_year: 년
		:param input_month: 월
		:return:
		"""
		result = []
		week_no = []
		date_obj = datetime.datetime(year=input_year, month=input_month, day=1).date()
		first_day_wwek_no = calendar.monthrange(date_obj.year, date_obj.month)[0]
		last_day = calendar.monthrange(date_obj.year, date_obj.month)[1]
		if first_day_wwek_no == 0:
			pass
		else:
			for no in range(first_day_wwek_no):
				week_no.append("")
		for num in range(1, int(last_day) + 1):
			if len(week_no) == 7:
				result.append(week_no)
				week_no = [num]
			else:
				week_no.append(num)
		if week_no:
			result.append(week_no)
		return result

	def get_all_holiday_for_lunar_year(self, input_year):
		"""
		음력으로된 휴일
		:param input_year:
		:return:
		"""
		result = []
		for one_list in self.vars["lunar_holiday_list"]:
			if one_list[0][0] <= input_year and one_list[0][3] >= input_year:
				if one_list[1][1] == "말일":
					one_list[1][1] = self.get_last_day_of_yyyymm_for_lunar(input_year, one_list[1][0])

				# 음력의 날짜를 양력의 날짜로 변경
				solar_date = self.change_lunar_ymd_to_solar_ymd_1([input_year, one_list[1][0], one_list[1][1]], True)
				if solar_date == "0000-00-00" or solar_date == "error":
					pass
				else:
					year_2, month, day = str(solar_date).split("-")
					result.append([int(year_2), int(month), int(day), one_list[1][-1]])
		return result

	def get_all_holiday_for_solar_year(self, input_year):
		"""
		입력 년도의 양력의 휴일
		:param input_year:
		:return:
		"""

		result = []
		for one_list in self.vars["solar_holiday_list"]:
			if one_list[0][0] <= input_year and one_list[0][3] >= input_year:
				result.append([input_year, one_list[1][0], one_list[1][1], one_list[1][-1]])
		return result

	def get_all_holiday_list_between_two_day(self, ymd_list_1, ymd_list_2):
		"""
		두날짜 사이의 휴일을 갖고오는것
		단, 음력은 한국/일본/중국이 같이 만들어가기 때문에, 당년도를 제외한 미래의 날짜는 알수가 없다
		:param date_1:
		:param date_2:
		:return:
		"""
		result = []
		total_holiday_list = []
		for one_year in range(ymd_list_1[0], ymd_list_2[0] + 1):
			solar_ymd_list = self.get_all_holiday_for_solar_year(one_year)
			for one in solar_ymd_list:
				total_holiday_list.append(one)

		# 음력의 경우는 2년을 더하기 빼기해서 계산한다
		for one_year in range(ymd_list_1[0] - 2, ymd_list_2[0] + 2):
			lunar_ymd_list = self.get_all_holiday_for_lunar_year(one_year)
			for one in lunar_ymd_list:
				total_holiday_list.append(one)

		dt_obj_date_1 = self.change_ymd_list_to_dt_obj(ymd_list_1)
		dt_obj_date_2 = self.change_ymd_list_to_dt_obj(ymd_list_2)
		for one in total_holiday_list:
			aaa = self.change_ymd_list_to_dt_obj([one[0], one[1], one[2]])
			if dt_obj_date_1 <= aaa <= dt_obj_date_2:
				result.append(one)
		result.sort()
		return result

	def get_all_infomation_for_dt_obj(self, input_dt_obj=""):
		"""
		입력된 시간에 대한 왠만한 모든 형식의 날짜 표현을 사전형식으로 돌려준다

		:param input_dt_obj: datetime객체, 날짜 객체
		:return:
		"""
		if not input_dt_obj:
			input_dt_obj = self.get_dt_obj_for_now()
		elif type(input_dt_obj) == type(123.45):
			input_dt_obj = self.change_anytime_to_dt_obj(input_dt_obj)

		result = {}
		# s는 short, e는 english, l은 long
		result["year_s"] = input_dt_obj.strftime('%y')  # 22
		result["year"] = input_dt_obj.strftime('%Y')  # 2023
		result["yyyy"] = result["year"]

		result["mon"] = input_dt_obj.strftime('%m')  # 1
		result["mm"] = result["mon"]
		result["mon_eng_s"] = input_dt_obj.strftime('%b')  # jan
		result["mon_eng_l"] = input_dt_obj.strftime('%B')  # january
		result["mon_eng"] = input_dt_obj.strftime('%B')  # january

		result["day_s"] = input_dt_obj.strftime('%d')  # 1
		result["d"] = input_dt_obj.strftime('%d')  # 1
		result["day"] = input_dt_obj.strftime('%j')  # 01
		result["dd"] = result["d"]

		result["week"] = input_dt_obj.strftime('%w')  # 6
		result["weekno"] = input_dt_obj.strftime('%w')
		result["yearweek"] = input_dt_obj.strftime('%W')  # 34, 1년중에 몇번째 주인지
		result["yearweekno"] = input_dt_obj.strftime('%W')  # 34, 1년중에 몇번째 주인지
		result["week_eng_s"] = input_dt_obj.strftime('%a')  # mon
		result["week_eng_l"] = input_dt_obj.strftime('%A')  # monday
		result["week_eng"] = input_dt_obj.strftime('%A')  # monday

		result["hour_s"] = input_dt_obj.strftime('%I')  # 1
		result["hour"] = input_dt_obj.strftime('%H')  # 13

		result["ampm"] = input_dt_obj.strftime('%p')
		result["min"] = input_dt_obj.strftime('%M')
		result["sec"] = input_dt_obj.strftime('%S')

		result["dt_timestamp"] = input_dt_obj.timestamp()
		result["timestamp"] = input_dt_obj.timestamp()
		result["utc_timestamp"] = input_dt_obj.timestamp() - 1640995200

		result["요일"] = int(result["weekno"])
		result["ymd"] = input_dt_obj.strftime("%Y-%m-%d")
		result["ymdhms"] = input_dt_obj.strftime("%Y-%m-%d-%H-%M-%S")
		result["sec_total"] = int(result["timestamp"])
		result["day_total"] = int(result["timestamp"] / 86400)
		result["ymd_list"] = result["ymd"].split("-")
		result["ymdhms_list"] = result["ymdhms"].split("-")
		return result

	def get_all_time_list_for_now(self, time_char=""):
		"""
		현제의 시간을 모든 날짜를 나타내는 자료의 형태로 구분해서 돌려주는 것

		:param time_char:
		:return:
		"""
		self.time_char = time_char
		if self.time_char == "":
			lt = time.localtime()
		else:
			lt = time.localtime(self.time_char)
		self.year = self.make_two_digit(lt.tm_year)
		self.mon = self.make_two_digit(lt.tm_mon)
		self.day = self.make_two_digit(lt.tm_mday)
		self.hour = self.make_two_digit(lt.tm_hour)
		self.min = self.make_two_digit(lt.tm_min)
		self.sec = self.make_two_digit(lt.tm_sec)
		self.weekday = str(lt.tm_wday)
		self.yearday = str(lt.tm_yday)
		return [self.year, self.mon, self.day, self.hour, self.min, self.sec, self.weekday, self.yearday]

	def get_day_for_now(self, input_text_time):
		"""
		입력시간의 일자를 알려주는 것
		일 -----> '05'

		:param input_text_time:
		:return:
		"""
		dt_obj = self.check_input_time(input_text_time)
		return time.strftime('%d', dt_obj)

	def get_day_for_utc(self, input_text_time=""):
		"""
		입력값 : utc시간숫자, 1640995200.0 또는 ""
		일 -----> ['05']
		닞은숫자 -> 많은글자 순으로 정리

		:param input_text_time: 문자열로된 시간
		:return:
		"""
		dt_obj = self.check_input_time(input_text_time)
		day = time.strftime('%d', dt_obj)
		return day

	def get_day_set_for_input_time(self, time_char=time.localtime(time.time())):
		"""
		입력한 시간(없을 때는 지금시간)을 아래의 형태에 대해서 알려주는 것
		일 -----> ['05', '095']

		:param time_char:
		:return:
		"""
		return [time.strftime('%d', time_char), time.strftime('%j', time_char)]

	def get_day_set_for_now(self, time_char=time.localtime(time.time())):
		"""
		일 -----> ['05', '095']

		:param time_char:
		:return:
		"""
		return [time.strftime('%d', time_char), time.strftime('%j', time_char)]

	def get_day_set_for_utc(self, input_utc=""):
		"""
		utc : utc의 timestamp, utc시간숫자, 1640995200.0 또는 ""
		일 -----> ['05']
		닞은숫자 -> 많은글자 순으로 정리

		:param input_data:
		:return:
		"""
		dt_obj = self.check_input_time(input_utc)
		day = time.strftime('%d', dt_obj)
		day_l = time.strftime('%j', dt_obj)
		result = [day, day_l]
		return result

	def get_dic_time_for_dt_obj(self, input_dt_obj=""):
		"""
		datetime객체를 사전형식의 시간으로 바꾸는 것

		:param input_dt_obj: datetime객체
		:return:
		"""
		if not input_dt_obj:
			input_dt_obj = self.get_dt_obj_for_now()
		result = {}
		temp = input_dt_obj.strftime("%Y-%m-%d-%H-%M-%S")
		result["yea"], result["mon"], result["day"], result["hou"], result["min"], result["sec"] = temp.split("-")
		return result

	def get_dt_obj_by_date_obj_and_time_obj(self, input_dt_obj="", input_time_obj=""):
		"""

		:param input_dt_obj:
		:param input_time_obj:
		:return:
		"""
		if not input_dt_obj:
			input_dt_obj = self.get_dt_obj_for_now()
		dt_obj = self.combine_date_obj_and_time_obj(input_dt_obj, input_time_obj)
		return dt_obj

	def get_dt_obj_for_last_day_of_anytime(self, input_text_time):
		"""
		입력한 날의 월의 마지막 날짜를 계산
		입력받은 날자에서 월을 1나 늘린후 1일을 마이너스 한다
		0:2023-04-19 -> 2023-05-01 -> 2023-05-01 - 12 -> 2023-04-30

		:param input_text_time: 문자열로된 시간
		:return:
		"""
		dt_obj = self.check_input_time(input_text_time)
		if dt_obj.month == 12:
			year = dt_obj.year + 1
			month = 1
		else:
			year = dt_obj.year
			month = dt_obj.month + 1
		dt_obj_1 = datetime.datetime(year, month, 1)
		dt_obj_2 = dt_obj_1 + datetime.timedelta(days=-1)
		result = dt_obj_2.day
		return result

	def get_dt_obj_for_now(self):
		"""
		기본인 datetime 객체를 돌려주는 것은 별도로 표기하지 않는다
		날짜와 시간(datetime) -> 문자열로 : strftime
		날짜와 시간 형식의 문자열을 -> datetime으로 : strptime

		:return:
		"""
		dt_obj = datetime.datetime.now()
		return dt_obj

	def get_dt_obj_for_now_as_local_time_zone(self):
		"""
		utc시간이 아니고 현재 지역적인 시간으로 변경하는 것
		3.6버전이후에 나타나는 astimezone를 사용하면 알아서 적용되는 것이다
		"""
		dt_obj = datetime.datetime.now()
		changed_dt_obj = dt_obj.astimezone()
		return changed_dt_obj

	def get_dt_obj_for_today(self):
		"""
		날짜와 시간(datetime) -> 문자열로 : strftime
		날짜와 시간 형식의 문자열을 -> datetime으로 : strptime

		:return:
		"""
		dt_obj = datetime.datetime.now()
		return dt_obj

	def get_dt_timestamp_for_dt_obj(self, input_dt_obj=""):
		"""
		날짜객체 => timestamp로 만드는 것

		:param input_dt_obj: datetime객체
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		result = input_dt_obj.timestamp()
		return result

	def get_dt_timestamp_for_now(self):
		"""
		기본적으로 datetime은 utc와 같은것이라 보면 된다
		:return:
		"""

		dt = datetime.datetime.now(datetime.timezone.utc)
		dt_timestamp = dt.timestamp()
		return dt_timestamp

	def get_end_day_of_month_for_text_time(self, input_text_time):
		"""
		입력한 날의 월의 마지막 날짜를 계산
		입력받은 날자에서 월을 1나 늘린후 1일을 마이너스 한다
		예: 2023-04-19 -> 2023-05-01 -> 2023-05-01 - 1일 -> 2023-04-30

		:param input_text_time: 문자열로된 시간
		:return:
		"""
		dt_obj = self.check_input_time(input_text_time)
		if dt_obj.month == 12:
			year = dt_obj.year + 1
			month = 1
		else:
			year = dt_obj.year
			month = dt_obj.month + 1
		dt_obj_1 = datetime.datetime(year, month, 1)
		dt_obj_2 = dt_obj_1 + datetime.timedelta(days=-1)
		result = dt_obj_2.day
		return result

	def get_hms_list_for_dt_obj(self, input_dt_obj=""):
		"""
		datetime객체 => [시, 분, 초]

		:param input_dt_obj: datetime객체
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		temp = input_dt_obj.strftime("%H-%M-%S")
		result = temp.split("-")
		return result

	def get_hms_list_for_now(self):
		"""
		utc시간이 아니고 현재 지역적인 시간으로 변경하는 것
		3.6버전이후에 나타나는 astimezone를 사용하면 알아서 적용되는 것이다
		"""
		dt_obj = datetime.datetime.now()
		changed_dt_obj = dt_obj.astimezone()
		result = self.change_dt_obj_to_hms_list(changed_dt_obj)
		return result

	def get_holiday_list_between_day1_and_day2(self, input_anytime1, input_anytime2):
		"""
		날짜사이의 휴일의 리스트 얻기

		:param input_ymd_list1: [년, 월, 일]
		:param input_ymd_list2: [년, 월, 일]
		:return:
		"""

		dic_time_1 = self.get_all_infomation_for_dt_obj(input_anytime1)
		dic_time_2 = self.get_all_infomation_for_dt_obj(input_anytime2)

		start_day = int(dic_time_1["year"] + dic_time_1["mon"] + dic_time_1["day"])
		end_day = int(dic_time_2["year"] + dic_time_2["mon"] + dic_time_2["day"])

		result = []
		# self.vars["holiday_list"] = [[[20060101, 20061231], [9, 6, "양", 1, "", "임시공휴일"]],[[19880101, 19881231], [9, 17, "양", 1, "", "임시공휴일"]],....]
		for list1d in self.vars["holiday_list"]:
			if list1d[0][0] <= int(start_day) and list1d[0][1] >= int(end_day):
				if list1d[1][0] <= int(dic_time_1["mon"]) and list1d[1][0] <= int(dic_time_2["mon"]) and list1d[1][
					1] <= int(dic_time_1["day"]) and list1d[1][1] <= int(dic_time_2["day"]):
					temp_year = [str(list1d[0][0])[0:4]]
					result.append(temp_year + list1d[1])
		return result

	def get_holiday_list_for_year(self, input_year):
		"""
		특정년도의 휴일을 돌려 줍니다

		:param input_year: 년
		:return:
		"""
		result = []
		temp = []
		for year in [input_year - 1, input_year, input_year + 1]:
			aaa = self.data_national_holiday_in_year(year, year)
			for one in aaa:
				bbb = self.check_holiday_on_year(year, one)
				for one in bbb:
					temp.append(one)
			print(year, temp)

		for one in temp:
			if int(one[0]) == int(input_year):
				result.append(one)
		return result

	def get_hour_for_input_time(self, time_char=time.localtime(time.time())):
		"""
		입력한 시간(없을 때는 지금시간)을 아래의 형태에 대해서 알려주는 것
		시 -----> '10'

		:param time_char:
		:return:
		"""
		return time.strftime('%I', time_char)

	def get_hour_for_now(self):
		"""
		시 -----> '10'

		:param time_char:
		:return:
		"""
		time_char = time.localtime(time.time())
		return time.strftime('%I', time_char)

	def get_hour_set_for_input_time(self, time_char=time.localtime(time.time())):
		"""
		입력한 시간(없을 때는 지금시간)을 아래의 형태에 대해서 알려주는 것
		시 -----> ['10', '22', 'PM']

		:param time_char:
		:return:
		"""
		return [time.strftime('%I', time_char), time.strftime('%H', time_char), time.strftime('%p', time_char)]

	def get_hour_set_for_now(self):
		"""
		시 -----> ['10', '22', 'PM']

		:param time_char:
		:return:
		"""
		time_char = time.localtime(time.time())
		return [time.strftime('%I', time_char), time.strftime('%H', time_char), time.strftime('%p', time_char)]

	def get_hour_set_for_utc(self, input_utc):
		"""
		utc : utc의 timestamp, utc시간숫자, 1640995200.0 또는 ""
		시 -----> ['10', '22']

		:param input_utc: utc 시간객체
		:return:
		"""
		input_utc = self.check_input_utc(input_utc)

		hour = time.strftime('%I', input_utc)
		hour_l = time.strftime('%H', input_utc)
		result = [hour, hour_l]
		return result

	def get_last_day_for_ym_list(self, input_ym_list):
		"""
		양력날짜에서 월의 마지막날을 찾는것
		입력 : [2023, 05]
		출력 : [날짜객체, [1,31], 1, 31]

		:param input_ym_list: [년, 월]
		:return:
		"""
		date = datetime.datetime(year=input_ym_list[0], month=input_ym_list[1], day=1).date()
		monthrange = calendar.monthrange(date.year, date.month)
		last_day = calendar.monthrange(date.year, date.month)[1]
		return last_day

	def get_last_day_of_input_month(self, input_list=[2002, 3]):
		"""
		입력값 : datetime.date(2012, month, 1)
		결과값 : 원하는 년과 월의 마지막날을 알아내는것
		"""
		any_day = datetime.date(input_list[0], input_list[1], 1)
		next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
		result = next_month - datetime.timedelta(days=next_month.day)
		return result

	def get_last_day_of_month_for_ym_list_as_dt_obj(self, input_ym_list=[2002, 3]):
		"""
		입력월의 마지막날을 돌려준다


		:param input_ym_list: [년, 월]
		:return:
		"""
		any_day = datetime.date(input_ym_list[0], input_ym_list[1], 1)
		next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
		result = next_month - datetime.timedelta(days=next_month.day)
		return result

	def get_last_day_of_yyyymm_for_lunar(self, input_yyyy, input_mm):
		"""
		음력의 년도와 월을 주면, 마지막날을 돌려주는 것
		12월은 "말일"을 날짜를 확인하기 위한것

		:param input_yyyy:
		:param input_mm:
		:return:
		"""
		self.lunar_calendar.setLunarDate(int(input_yyyy), int(input_mm), 1, True)
		result = self.lunar_calendar.LUNAR_BIG_MONTH_DAY
		return result

	def get_max_year_for_datetime(self):
		"""
		datetime객체에서 사용가능한 최대의 년도를 알려주는 것
		:return:
		"""
		result = datetime.MAXYEAR
		return result

	def get_min_for_input_time(self, time_char=time.localtime(time.time())):
		"""
		입력한 시간(없을 때는 지금시간)을 아래의 형태에 대해서 알려주는 것
		분 -----> ['07']

		:param time_char:
		:return:
		"""
		return [time.strftime('%M', time_char)]

	def get_min_for_utc(self, input_utc):
		"""
		입력값 : utc시간숫자, 1640995200.0 또는 ""
		분 -----> ['07']
		닞은숫자 -> 많은글자 순으로 정리

		:param input_utc: utc 시간객체
		:return:
		"""
		input_utc = self.check_input_utc(input_utc)

		result = time.strftime('%M', input_utc)
		return result

	def get_min_from_utftime(self, input_data=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		분 -----> ['07']
		닞은숫자 -> 많은글자 순으로 정리
		"""
		utf_local_time = self.change_anytime_to_utftime(input_data)
		min = time.strftime('%M', utf_local_time)
		return min

	def get_minute_set_for_now(self, time_char=time.localtime(time.time())):
		"""
		분 -----> ['07']

		:param time_char:
		:return:
		"""
		return [time.strftime('%M', time_char)]

	def get_month_for_input_time(self, time_char=time.localtime(time.time())):
		"""
		입력한 시간(없을 때는 지금시간)을 아래의 형태에 대해서 알려주는 것
		월 -----> '04'
		"""

		result = time.strftime('%m', time_char)
		return result

	def get_month_range_for_ym_list(self, input_ym_list=[2002, 3]):
		"""
		입력월의 첫날과 끝날을 알려주는 것

		:param input_ym_list: [년, 월]
		:return:
		"""
		date = datetime.datetime(year=input_ym_list[0], month=input_ym_list[1], day=1).date()
		monthrange = calendar.monthrange(date.year, date.month)
		first_day = 1
		last_day = calendar.monthrange(date.year, date.month)[1]
		return [first_day, last_day]

	def get_month_set_for_input_time(self, time_char=time.localtime(time.time())):
		"""
		입력한 시간(없을 때는 지금시간)을 아래의 형태에 대해서 알려주는 것
		월 -----> ['04', 'Apr', 'April']

		:param time_char:
		:return:
		"""
		return [time.strftime('%m', time_char), time.strftime('%b', time_char), time.strftime('%B', time_char)]

	def get_month_set_for_now(self, time_char=time.localtime(time.time())):
		"""
		utc : utc의 timestamp, utc시간숫자, 1640995200.0 또는 ""

		월 -----> ['04', Apr, April]
		닞은숫자 -> 많은글자 순으로 정리

		:param input_utc: utc 시간객체
		:return:
		"""
		return [time.strftime('%m', time_char), time.strftime('%b', time_char), time.strftime('%B', time_char)]

	def get_month_set_for_utc(self, input_utc=""):
		"""
		utc : utc의 timestamp, utc시간숫자, 1640995200.0 또는 ""

		월 -----> ['04', Apr, April]
		닞은숫자 -> 많은글자 순으로 정리

		:param input_utc: utc 시간객체
		:return:
		"""
		input_utc = self.check_input_utc(input_utc)
		mon = time.strftime('%m', input_utc)
		mon_e = time.strftime('%b', input_utc)
		mon_e_l = time.strftime('%B', input_utc)
		result = [mon, mon_e, mon_e_l]
		return result

	def get_month_set_from_utftime(self, input_data=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		월 -----> ['04', Apr, April]
		닞은숫자 -> 많은글자 순으로 정리
		"""
		utf_local_time = self.change_anytime_to_utftime(input_data)
		mon = time.strftime('%m', utf_local_time)
		mon_e = time.strftime('%b', utf_local_time)
		mon_e_l = time.strftime('%B', utf_local_time)
		result = [mon, mon_e, mon_e_l]
		return result

	def get_no_of_sunday_in_same_week_for_dt_obj(self, input_dt_obj=""):
		"""
		날짜객체의 week_no_7을 알아내는것
		주의 7번째 요일인 일요일의 날짜를 돌려줍니다

		:param input_dt_obj: datetime객체, 날짜 객체
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		result = input_dt_obj.strftime('%w')  # 6
		return result

	def get_one_month_list_for_year_month(self, input_year, input_month):
		"""
		년과 월을 주면, 한달의 리스트를 알아내는것
		월요일부터 시작

		:param input_year:년
		:param input_month:월
		:return:
		"""
		result = []
		week_no = []
		date_obj = datetime.datetime(year=input_year, month=input_month, day=1).date()
		first_day_wwek_no = calendar.monthrange(date_obj.year, date_obj.month)[0]
		last_day = calendar.monthrange(date_obj.year, date_obj.month)[1]
		if first_day_wwek_no == 0:
			pass
		else:
			for no in range(first_day_wwek_no):
				week_no.append("")
		for num in range(1, int(last_day) + 1):
			if len(week_no) == 7:
				result.append(week_no)
				week_no = [num]
			else:
				week_no.append(num)
		if week_no:
			result.append(week_no)
		return result

	def get_sec_for_dt_obj(self, input_dt_obj=""):
		"""
		시간객체를 초로 나타내는 자료형으로 만드는 것

		:param input_dt_obj: datetime객체
		:return: [timestamp, 날짜에대한 초, 나머지초]
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		sec = time.strftime('%S', input_dt_obj)
		return sec

	def get_sec_for_input_time(self, input_text_time=""):
		"""

		:param input_text_time: 문자열로된 시간
		:return:
		"""
		dt_obj = self.check_input_time(input_text_time)
		sec = time.strftime('%S', dt_obj)
		return sec

	def get_sec_for_now(self):
		"""
		초 -----> ['48']

		:param time_char:
		:return:
		"""
		time_char = time.localtime(time.time())
		return time.strftime('%S', time_char)

	def get_sec_for_utc(self, input_utc=""):
		"""
		utc : utc의 timestamp, utc시간숫자, 1640995200.0 또는 ""

		초 -----> ['48']
		닞은숫자 -> 많은글자 순으로 정리

		:param input_utc: utc 시간객체
		:return:
		"""
		input_utc = self.check_input_utc(input_utc)
		result = time.strftime('%S', input_utc)
		return result

	def get_sec_set_from_utftime(self, input_data=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		초 -----> ['48']
		닞은숫자 -> 많은글자 순으로 정리
		"""
		utf_local_time = self.change_anytime_to_utftime(input_data)
		sec = time.strftime('%S', utf_local_time)
		result = [sec]
		return result

	def get_start_year_of_datetime(self):
		"""
		datetime객체의 최소한의 년도를 알려주는 것

		:return:
		"""
		result = datetime.MINYEAR
		return result

	def get_text_time_for_dt_obj_as_input_format(self, input_dt_obj="", input_format="%Y-%m-%d %H:%M:%S"):
		"""
		입력형식으로 되어있는 시간자료를 dt객체로 인식하도록 만드는 것이다
		dt = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")

		:param input_dt_obj: datetime객체, 날짜 객체
		:param input_format:
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		input_format = self.check_time_format(input_format)
		result = input_dt_obj.strftime(input_format)
		return result

	def get_today_set_for_input_time(self, time_char=time.localtime(time.time())):
		"""
		입력한 시간(없을 때는 지금시간)을 아래의 형태에 대해서 알려주는 것
		종합 -----> ['04/05/02', '22:07:48', '04/05/02 22:07:48','2002-04-05']
		040621 : 이름을 변경 (total -> today)

		:param time_char:
		:return:
		"""
		aaa = time_char.split(time.strftime('%c', time_char))
		total_dash = time.strftime('%Y', time_char) + "-" + time.strftime('%m', time_char) + "-" + time.strftime('%d',
																												 time_char)
		return [aaa[0], aaa[1], time.strftime('%c', time_char), total_dash]

	def get_today_set_for_input_time(self, time_char=time.localtime(time.time())):
		"""
		입력한 시간(없을 때는 지금시간)을 아래의 형태에 대해서 알려주는 것
		주 -----> ['5', '13', 'Fri', 'Friday']

		:param time_char:
		:return:
		"""
		return [time.strftime('%w', time_char), time.strftime('%W', time_char), time.strftime('%a', time_char),
				time.strftime('%A', time_char)]

	def get_today_set_for_now(self, time_char=time.localtime(time.time())):
		"""
		종합 -----> ['04/05/02', '22:07:48', '04/05/02 22:07:48','2002-04-05']
		040621 : 이름을 변경 (total -> today)

		:param time_char:
		:return:
		"""
		aaa = str(time.strftime('%c', time_char)).split()
		total_dash = time.strftime('%Y', time_char) + "-" + time.strftime('%m', time_char) + "-" + time.strftime('%d',
																												 time_char)
		return [aaa[0], aaa[1], time.strftime('%c', time_char), total_dash]

	def get_utc_for_now(self):
		"""
		기본적으로 datetime은 utc와 같은것이라 보면 된다
		:return:
		"""
		result = datetime.datetime.utcnow()
		return result

	def get_utck_for_now(self):
		"""
		지금시간을 utf-k기준으로 알려주는 것

		:return:
		"""

		result = time.localtime(time.time())
		return result

	def get_week_list_by_nth_week_later(self, n_week_later, base_date=""):
		"""
		어느날짜를 기준으로 n주후의 일주일의 날짜를 갖고오는것

		:param n_week_later:
		:param base_date:
		:return:
		"""
		dt_obt = self.check_input_time(base_date)
		dt_obj = self.shift_day_for_dt_obj(dt_obt, n_week_later * 7)

		week_list = self.get_week_list_for_dt_obj(dt_obt)
		return week_list

	def get_week_list_by_year_weekno(self, year, weekno):
		"""
		년도와 주번호를 넣으면, 주의 리스트를 돌려주는 것
		:param year:
		:param week:
		:return:
		"""
		# 주의 첫 번째 날(월요일)을 계산합니다.
		first_day_of_year = datetime.datetime(year, 1, 1)
		# self.change_yyyy_mm_dd_to_dt_obj()
		first_week_day = first_day_of_year - datetime.timedelta(days=first_day_of_year.isoweekday() % 7)
		start_of_week = first_week_day + datetime.timedelta(weeks=weekno - 1)
		# 이번 주의 7 일을 리스트에 저장합니다
		week_dates = [(start_of_week + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
		return week_dates

	def get_week_list_for_dt_obj(self, input_dt_obj=""):
		"""
		월요일부터 시작하는 7 개의 날짜를 돌려준다
		2023-07-24 : f'{year} {yearweekno} 0' => f'{year} {yearweekno} 1'

		:param year:
		:param yearweekno:
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		dic_data = self.get_all_infomation_for_dt_obj(input_dt_obj)
		str_datetime = f'{dic_data["year"]} {dic_data["yearweek"]} 1'  # 1은 월요일 이다

		# 문자열형태로 입력받아서, 시간객체로 만들어 주는것
		startdate = datetime.datetime.strptime(str_datetime, '%Y %W %w')
		dates = []
		for i in range(7):
			day = startdate + datetime.timedelta(days=i)
			dates.append(day.strftime("%Y-%m-%d"))
		return dates

	def get_week_list_for_this_week(self, input_text_time=""):
		"""
		이번주에 대한 날짜 리스트

		:param input_text_time:
		:return:
		"""
		dt_obj = self.check_input_time(input_text_time)
		# 오늘의 요일을 가져옵니다. (월요일=0, 일요일=6)
		today_weekday = dt_obj.weekday()
		# 일요일을 기준으로 이번 주의 시작 날짜를 계산합니다.
		# 일요일은 6이므로, 오늘의 요일에 1을 더한 후 7로 나눈 나머지를 빼줍니다.
		start_of_week = dt_obj - datetime.timedelta(days=(today_weekday + 1) % 7)
		# 이번 주의 7 일을 리스트에 저장합니다
		week_dates = [(start_of_week + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
		return week_dates

	def get_week_set_for_input_time(self, time_char=time.localtime(time.time())):
		"""
		주 -----> ['5', '13', 'Fri', 'Friday']
		"""
		return [time.strftime('%w', time_char), time.strftime('%W', time_char), time.strftime('%a', time_char),
				time.strftime('%A', time_char)]

	def get_week_set_for_now(self, time_char=time.localtime(time.time())):
		"""
		주 -----> ['5', '13', 'Fri', 'Friday']

		:param time_char:
		:return:
		"""
		return [time.strftime('%w', time_char), time.strftime('%W', time_char), time.strftime('%a', time_char),
				time.strftime('%A', time_char)]

	def get_week_set_for_utc(self, input_utc):
		"""
		utc : utc의 timestamp, utc시간숫자, 1640995200.0 또는 ""
		주 -----> ['5', '13', 'Fri', 'Friday']
		닞은숫자 -> 많은글자 순으로 정리

		:param input_utc: utc 시간객체
		:return:
		"""
		input_utc = self.check_input_utc(input_utc)

		week_no = time.strftime('%w', input_utc)
		yearweekno = time.strftime('%W', input_utc)
		week_e = time.strftime('%a', input_utc)
		week_e_l = time.strftime('%A', input_utc)
		result = [week_no, yearweekno, week_e, week_e_l]
		return result

	def get_week_set_from_utftime(self, input_data=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		주 -----> ['5', '13', 'Fri', 'Friday']
		닞은숫자 -> 많은글자 순으로 정리
		"""
		utf_local_time = self.change_anytime_to_utftime(input_data)
		week_no = time.strftime('%w', utf_local_time)
		yearweek_no = time.strftime('%W', utf_local_time)
		week_e = time.strftime('%a', utf_local_time)
		week_e_l = time.strftime('%A', utf_local_time)
		result = [week_no, yearweek_no, week_e, week_e_l]
		return result

	def get_weekno_for_1st_day_of_ym_list(self, input_ym_list):
		"""
		week_no : 1~7까지의 요일에 대한 숫자
		입력한 월의 1일이 무슨요일인지 알아 내는것
		[2023, 05] => 0, 월요일

		:param input_ym_list: [년, 월]
		:return:
		"""
		date = datetime.datetime(year=input_ym_list[0], month=input_ym_list[1], day=1).date()
		monthrange = calendar.monthrange(date.year, date.month)
		first_day = calendar.monthrange(date.year, date.month)[0]
		return first_day

	def get_weekno_from_utftime(self, input_data=""):
		"""
		시간이 들어온면
		입력값 : 년도, 위크번호
		한 주의 시작은 '월'요일 부터이다
		"""
		lt = self.change_anytime_to_utftime(input_data)
		result = time.strftime('%W', lt)
		return result

	def get_weekno_set_for_dt_obj(self, input_dt_obj=""):
		"""
		datetime는 utc local
		week_no : 1~7까지의 요일에 대한 숫자, 월요일은 0, 일요일은 6

		:param input_dt_obj: datetime객체, 날짜 객체
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		weekno = input_dt_obj.strftime('%w')
		result = [weekno, self.vars["week"][weekno], self.vars["요일"][weekno]]
		return result

	def get_year_for_input_time(self, time_char=time.localtime(time.time())):
		"""
		입력한 시간(없을 때는 지금시간)을 아래의 형태에 대해서 알려주는 것
		년 -----> ['2002']

		:param time_char:
		:return:
		"""
		return [time.strftime('%Y', time_char)]

	def get_year_for_now(self):
		"""
		년 -----> 2002
		"""
		time_char = time.localtime(time.time())
		return time.strftime('%Y', time_char)

	def get_year_for_utc(self, input_utc):
		"""
		utc : utc의 timestamp, utc시간숫자, 1640995200.0 또는 ""

		년 -----> ['22', '2022']
		닞은숫자 -> 많은글자 순으로 정리

		:param input_utc: utc 시간객체
		:return:
		"""
		input_utc = self.check_input_utc(input_utc)

		result = time.strftime('%Y', input_utc)
		return result

	def get_year_from_utftime(self, input_data=""):
		"""
		년 -----> '2022'
		닞은숫자 -> 많은글자 순으로 정리
		"""
		utf_local_time = self.change_anytime_to_utftime(input_data)
		year = time.strftime('%Y', utf_local_time)
		return year

	def get_year_set_for_input_time(self, time_char=time.localtime(time.time())):
		"""
		입력한 시간(없을 때는 지금시간)을 아래의 형태에 대해서 알려주는 것
		년 -----> ['02', '2002']

		:param time_char:
		:return:
		"""
		return [time.strftime('%y', time_char), time.strftime('%Y', time_char)]

	def get_yearweekno_for_dt_obj(self, input_dt_obj=""):
		"""
		dt객체에 대한 한해의 몇번째 주인지를 알아낸다

		:param input_dt_obj: datetime객체, 날짜 객체
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		year, week_number, weekday = input_dt_obj.isocalendar()
		return week_number

	def get_yearweekno_for_now(self):
		"""
		yearweekno : 1년에서 몇번째 주인지 아는것
		입력한날의 week 번호를	계산
		입력값 : 날짜

		:return:
		"""
		today = self.get_yyyy_mm_dd_for_now()
		year, month, day = today.split("-")
		dt_obj = self.check_input_time([year, month, day])
		result = int(dt_obj.strftime("%W"))
		return result

	def get_yearweekno_for_today(self):
		"""
		오늘 날짜의 weekno를 갖고온다
		:return:
		"""
		today = datetime.datetime.today()
		year, week_number, weekday = today.isocalendar()
		return week_number

	def get_yearweekno_for_utc(self, input_text_time=""):
		"""
		utc : utc의 timestamp, utc시간숫자, 1640995200.0 또는 ""

		시간이 들어온면
		입력값 : 년도, 위크번호
		한 주의 시작은 '월'요일 부터이다

		:param input_text_time: 문자열로된 시간
		:return:
		"""
		dt_obj = self.check_input_time(input_text_time)
		result = time.strftime('%W', dt_obj)  # 34, 1년중에 몇번째 주인지
		return result

	def get_yearweekno_for_ymd_list(self, input_date=""):
		"""
		입력한날의 week 번호를 계산
		입력값 : 날짜
		"""

		if input_date == "":
			today = self.get_yyyy_mm_dd_for_today()
			print(today)
			year, month, day = today.split("-")
			dt_obj = self.check_input_time([year, month, day])
		else:
			dt_obj = self.change_anytime_to_dt_obj(input_date)

		result = int(dt_obj.strftime('%W'))
		return result

	def get_ymd_dash_for_today(self):
		"""
		오늘 날짜를 yyyy-mm-dd형식으로 돌려준다
		지금의 날짜를 돌려준다
		입력값 : 없음
		출력값 : 2022-03-01,
		"""
		just_now = arrow.now()
		result = just_now.format("YYYY-MM-DD")
		return result

	def get_ymd_dash_for_utc(self, input_utc):
		"""
		utc를 2023-2-2형태로 돌려주는 것

		:param input_utc: utc 시간객체
		:return:
		"""
		input_utc = self.check_input_utc(input_utc)
		result = time.strftime('%Y-%m-%d', input_utc)
		return result

	def get_ymd_dash_from_utftime(self, input_data=""):
		"""
		utf시간을 YYYY-MM-DD 형태의 시간으로 바꾸는 것
		:param input_data:
		:return:
		"""
		lt = self.change_anytime_to_utftime(input_data)
		atime = arrow.get(lt)
		result = atime.format("YYYY-MM-DD")
		return result

	def get_ymd_list_for_dt_obj(self, input_dt_obj=""):
		"""
		datetime는 utc local
		datetime객체 => [년, 월, 일]

		:param input_dt_obj: datetime객체
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		temp = input_dt_obj.strftime("%Y-%m-%d")
		result = temp.split("-")
		return result

	def get_ymd_list_for_now_by_local(self):
		"""
		utc시간이 아니고 현재 지역적인 시간으로 변경하는 것
		3.6버전이후에 나타나는 astimezone를 사용하면 알아서 적용되는 것이다
		"""
		dt_obj = datetime.datetime.now()
		changed_dt_obj = dt_obj.astimezone()
		result = self.get_ymd_list_for_dt_obj(changed_dt_obj)
		return result

	def get_ymd_list_for_text_time(self, input_anytime):
		"""
		datetime는 utc local
		datetime객체 => [년, 월, 일]

		:param input_dt_obj: datetime객체
		:return:
		"""
		dt_obj = self.change_anytime_to_dt_obj(input_anytime)
		temp = dt_obj.strftime("%Y-%m-%d")
		result = temp.split("-")
		return result

	def get_ymd_list_for_utc(self, input_utc):
		"""

		:param input_utc: utc 시간객체
		:return:
		"""
		input_utc = self.check_input_utc(input_utc)
		year = time.strftime('%Y', input_utc)
		month = time.strftime('%m', input_utc)
		day = time.strftime('%d', input_utc)
		result = [year, month, day]
		return result

	def get_ymdhms_list_for_dt_obj(self, input_dt_obj=""):
		"""
		datetime는 utc local
		datetime객체 => [년, 월, 일, 시, 분, 초]

		:param input_dt_obj: datetime객체
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		temp = input_dt_obj.strftime("%Y-%m-%d-%H-%M-%S")
		result = temp.split("-")
		return result

	def get_ymdhms_list_for_now_by_local(self):
		"""
		지금시간을 ymdhms_list형태로 알려주는 것
		:return:
		"""
		dt_obj = datetime.datetime.now()
		changed_dt_obj = dt_obj.astimezone()
		result = self.get_ymdhms_list_for_dt_obj(changed_dt_obj)
		return result

	def get_yyyy_mm_dd_for_now(self):
		"""
		오늘 날짜를 yyyy-mm-dd형식으로 돌려준다
		지금의 날짜를 돌려준다
		입력값 : 없음
		출력값 : 2022-03-01,

		:return:
		"""
		dt_obj = self.check_input_time("")
		result = dt_obj.format("YYYY-MM-DD")
		# result = dt_obj.strftime("%Y-%m-%d")
		return result

	def get_yyyy_mm_dd_for_today(self):
		"""
		오늘날자를 yyyy-mm-dd형식으로 만들어주는 것

		:return:
		"""
		lt = time.localtime()
		self.year = self.make_two_digit(lt.tm_year)
		self.mon = self.make_two_digit(lt.tm_mon)
		self.day = self.make_two_digit(lt.tm_mday)
		total_dash = self.year + "-" + self.mon + "-" + self.day
		return total_dash

	def get_yyyymmdd_for_timestamp(self):
		"""
		화일이름으로 사용하는 목적으로 만드는 것입니다
		예를들어 : 20241101_2345678

		:return:
		"""

		timestamp = self.get_dt_timestamp()
		str_timestamp = str(timestamp * 1000000)[-8:-2]
		# print("====> ", timestamp, str(timestamp*1000000))
		dt_obj = datetime.datetime.now()
		temp = self.get_all_infomation_for_dt_obj(dt_obj)["ymd_list"]
		result = str(temp[0]) + str(temp[1]) + str(temp[2]) + "_" + str_timestamp

		return result

	def holiday_nation(self):
		"""
		휴일기준

		:return:
		"""
		self.holiday["common"] = ["0101", "0301", "0505", "0606", "0815", "1001", "1225", 1.3]
		self.holiday["company"] = ["0708"]

	def intersect_two_time_range(self, dt_obj_11, dt_obj_12, dt_obj_21, dt_obj_22):
		"""
		겼치는 시간 부분을 리스트로 돌려줌

		:param dt_obj_11:
		:param dt_obj_12:
		:param dt_obj_21:
		:param dt_obj_22:
		:return:
		"""

		start_1 = min(dt_obj_11, dt_obj_12)
		end_1 = max(dt_obj_11, dt_obj_12)
		start_2 = min(dt_obj_21, dt_obj_22)
		end_2 = max(dt_obj_21, dt_obj_22)
		if end_2 < start_1 or start_2 < end_1:
			# 겪치는 부분이 없는것
			result = False
		else:
			temp_1 = min(start_1, start_2)
			temp_2 = max(end_1, end_2)
			result = [temp_1, temp_2]
		return result

	def is_same_ymd_for_two_dt_obj(self, dt_obj_1, dt_obj_2):
		"""
		겼치는 시간 부분을 리스트로 돌려줌

		:param dt_obj_1:
		:param dt_obj_2:
		:return:
		"""
		ymd_list_1 = self.get_ymd_list_for_dt_obj(dt_obj_1)
		ymd_list_2 = self.get_ymd_list_for_dt_obj(dt_obj_2)
		result = False
		if ymd_list_1 == ymd_list_2:
			result = True
		return result

	def join_list_with_char(self, input_list, input_char):
		"""
		입력리스트자료를 연결문자를 이용해서 하나의 문자로 만들어 주는 것

		:param input_list:
		:param input_char:
		:return:
		"""
		result = ""
		for one in input_list[:-1]:
			result = result + str(one) + input_char
		result = result + str(input_list[-1])
		return result

	def make_dic_time(self, input_dic):
		"""
		ymdhms의 사전형식으로 만드는 것
		:param input_dic:
		:return:
		"""
		result = {"yea": 0, "mon": 0, "day": 0, "hou": 0, "min": 0, "sec": 0}
		result.update(input_dic)
		return result

	def make_text_style_from_two_hms_list(self, hms_list_1, hms_list_2):
		"""
		09:20 ~ 10:21로 나타내는 것

		:param hms_list_1: [시, 분, 초]
		:param hms_list_2: [시, 분, 초]
		:return:
		"""
		h_1, m_1, s_1 = hms_list_1
		h_2, m_2, s_2 = hms_list_2
		result = f"{h_1:0>2}:{m_1:0>2} ~ {h_2:0>2}:{m_2:0>2}"
		return result

	def make_time_list_between_2_hms_list_by_step(self, start_hms_list, end_hms_list, step=30):
		"""
		시작과 종료시간을 입력하면, 30분간격으로 시간목록을 자동으로 생성시키는것

		:param start_hms_list: [시, 분, 초]
		:param end_hms_list: [시, 분, 초]
		:param step:
		:return:
		"""
		result = []
		hour, min, sec = start_hms_list
		hour_end, min_end, sec_end = end_hms_list
		result.append([hour, min, sec])
		while 1:
			min = min + step
			over_min, min = divmod(min, 60)
			if over_min > 0:
				hour = hour + over_min
			hour = divmod(hour, 24)[1]
			if int(hour) * 60 + int(min) > int(hour_end) * 60 + int(min_end):
				break
			result.append([hour, min, sec])
		return result

	def make_time_list_by_step_with_start_end(self, start_hsm_list, end_hsm_list, step=30):
		"""
		시작과 종료시간을 입력하면, 30분간격으로 시간목록을 자동으로 생성시키는것

		:param start_hsm_list:
		:param end_hsm_list:
		:param step:
		:return:
		"""
		result = []
		hour, min, sec = start_hsm_list
		hour_end, min_end, sec_end = end_hsm_list
		result.append([hour, min, sec])
		while 1:
			min = min + step
			over_min, min = divmod(min, 60)
			if over_min > 0:
				hour = hour + over_min
			hour = divmod(hour, 24)[1]
			if int(hour) * 60 + int(min) > int(hour_end) * 60 + int(min_end):
				break
			result.append([hour, min, sec])
		return result

	def make_time_list_for_hms_list_by_step_cycle(self, start_hms_list, step=30, cycle=20):
		"""
		시작과 종료시간을 입력하면, 30분간격으로 시간목록을 자동으로 생성시키는것

		:param start_hms_list: [시, 분, 초]
		:param step:
		:param cycle:
		:return:
		"""
		result = []
		hour, min, sec = start_hms_list
		result.append([hour, min, sec])
		for one in range(cycle):
			min = min + step
			over_min, min = divmod(min, 60)
			if over_min > 0:
				hour = hour + over_min
			hour = divmod(hour, 24)[1]
			result.append([hour, min, sec])
		return result

	def make_time_list_from_start_time_by_min_step(self, start_hsm_list, step=30, cycle=20):
		"""
		pynal - 시작과 종료시간을 입력하면, 30분간격으로 시간목록을 자동으로 생성시키는것
		시작과 종료시간을 입력하면, 30분간격으로 시간목록을 자동으로 생성시키는것

		:param start_hsm_list:
		:param step:
		:param cycle:
		:return:
		"""
		result = []
		hour, min, sec = start_hsm_list
		result.append([hour, min, sec])
		for one in range(cycle):
			min = min + step
			over_min, min = divmod(min, 60)
			if over_min > 0:
				hour = hour + over_min
			hour = divmod(hour, 24)[1]
			result.append([hour, min, sec])
		return result

	def make_time_set_from_hms_list_by_step(self, start_hms_list, step=30, cycle=20):
		"""
		시작과 종료시간을 입력하면, 30분간격으로 시간목록을 자동으로 생성시키는것

		:param start_hms_list: [시, 분, 초]
		:param step:
		:param cycle:
		:return:
		"""
		result = []
		hour, min, sec = start_hms_list
		result.append([hour, min, sec])
		for one in range(cycle):
			min = min + step
			over_min, min = divmod(min, 60)
			if over_min > 0:
				hour = hour + over_min
			hour = divmod(hour, 24)[1]
			result.append([hour, min, sec])
		return result

	def make_two_digit(self, input_data):
		"""

		:param input_data:
		:return:
		"""
		input_data = str(input_data)
		if len(input_data) == 1:
			result = "0" + input_data
		else:
			result = input_data
		return result

	def minus_date0_date1(self, input_date1, input_date2):
		"""
		두날자의 빼기

		:param input_date1:
		:param input_date2:
		:return:
		"""
		result = self.minus_two_date(input_date1, input_date2)
		return result

	def minus_date1_date2(self, date_1, date_2):
		"""
		두날자의 빼기

		:param date_1:
		:param date_2:
		:return:
		"""
		time_big = self.check_datetime(date_1)
		time_small = self.check_datetime(date_2)
		if time_big.lt_utc > time_small.lt_utc:
			pass
		else:
			time_big, time_small = time_small, time_big
		time_big.last_day = self.get_month_range_for_ym_list(time_big.year, time_big.month)[3]
		time_small.last_day = self.get_month_range_for_ym_list(time_small.year, time_small.month)[3]

		delta_year = abs(time_big.year - time_small.year)
		delta_day = int(abs(time_big.lt_utc - time_small.lt_utc) / (24 * 60 * 60))
		# 실제 1 년의 차이는 365 일 5 시간 48 분 46초 + 0.5초이다 (2 년에 1 번씩 윤초를 실시》
		actual_delta_year = int(abs(time_big.lt_utc - time_small.lt_utc) / (31556926 + 0.5))
		delta_month = abs((time_big.year * 12 + time_big.month) - (time_small.year * 12 + time_small.month))
		if time_big.day > time_small.day:
			actual_delta_month = delta_month - 1
		else:
			actual_delta_month = delta_month
		actual_delta_day = delta_day
		return [delta_year, delta_month, delta_day, actual_delta_year, actual_delta_month, actual_delta_day]

	def minus_two_date(self, input_date1, input_date2):
		"""
		두날짜의 빼기

		:param input_date1:
		:param input_date2:
		:return:
		"""
		utc1 = self.change_any_text_time_to_dt_obj(input_date1)
		utc2 = self.change_any_text_time_to_dt_obj(input_date2)
		result = abs((float(utc1) - float(utc2)) / (60 * 60 * 24))
		return result

	def minus_two_dt_obj(self, input_dt1, input_dt2):
		"""
		두날짜의 빼기

		:param input_dt1:
		:param input_dt2:
		:return:
		"""

		yr_ct = 365 * 24 * 60 * 60  # 31536000
		day_ct = 24 * 60 * 60  # 86400
		hour_ct = 60 * 60  # 3600
		minute_ct = 60

		result = {}
		ccc = abs(input_dt1 - input_dt2)

		result["original"] = ccc
		result["total_seconds"] = total_sec = ccc.total_seconds()

		result["year"] = int(total_sec / yr_ct)
		changed_total_sec = total_sec - int(total_sec / yr_ct) * yr_ct

		result["day"] = int(changed_total_sec / day_ct)
		changed_total_sec = changed_total_sec - int(changed_total_sec / day_ct) * day_ct

		result["hour"] = int(changed_total_sec / hour_ct)
		changed_total_sec = changed_total_sec - int(changed_total_sec / hour_ct) * hour_ct

		result["minute"] = int(changed_total_sec / minute_ct)
		changed_total_sec = changed_total_sec - int(changed_total_sec / minute_ct) * minute_ct

		result["second"] = int(changed_total_sec)
		changed_total_sec = changed_total_sec - int(changed_total_sec)

		result["remain"] = changed_total_sec
		print(result)
		return result

	def minus_two_hms_list(self, hms_list_1, hms_list_2):
		"""
		2개의 시분초리스트를 빼기 한다

		:param hms_list_1: [시, 분, 초]
		:param hms_list_2: [시, 분, 초]
		:return:
		"""
		sec_1 = self.change_hms_list_to_sec(hms_list_1)
		sec_2 = self.change_hms_list_to_sec(hms_list_2)
		result = self.change_sec_to_dhms_list(abs(sec_1 - sec_2))
		return result

	def mix_ymd_list_and_connect_char(self, input_ymd_list, connect_char="-"):
		"""
		입력리스트자료를 연결문자를 이용해서 하나의 문자로 만들어 주는 것

		:param input_ymd_list:
		:param connect_char:
		:return:
		"""
		result = input_ymd_list[0] + connect_char + input_ymd_list[1] + connect_char + input_ymd_list[2]
		return result

	def multiple_two_hms_list(self, hms_list_1, hms_list_2, times=1):
		"""
		2기간 사이의 기간을 몇배를 곱하기로 내는것

		:param hms_list_1: [시, 분, 초]
		:param hms_list_2: [시, 분, 초]
		:param times:
		:return:
		"""
		sec_1 = self.change_hms_list_to_sec(hms_list_1)
		sec_2 = self.change_hms_list_to_sec(hms_list_2)
		result = self.change_sec_to_dhms_list(abs(sec_1 - sec_2) * times)
		return result

	def overlap_area_for_two_dt_range(self, dt_obj_11, dt_obj_12):
		"""
		겹치는 시간 부분을 리스트로 돌려줌

		:param dt_obj_11:
		:param dt_obj_12:
		:return:
		"""
		start_dt_obj = min(dt_obj_11, dt_obj_12)
		end_dt_obj = max(dt_obj_11, dt_obj_12)
		start_timestamp, start_day, start_sec = self.change_dt_obj_to_sec_set(start_dt_obj)
		end_timestamp, end_day, end_sec = self.change_dt_obj_to_sec_set(end_dt_obj)
		differ_day = end_day - start_day
		if start_day == end_day:
			result = [start_sec, end_sec, None, None, 0]
		else:
			result = [start_sec, 86400, 1, end_sec, differ_day]
		return result

	def overtime(self):
		"""
		[시작시간, 끝시간, 일당몇배]

		:return:
		"""
		self.ot["common"] = [["0000", "0500", 1], ["0505", "0606", 1.2]]
		self.ot["company"] = ["0708"]

	def plus_dt_obj_and_hms_list(self, input_dt_obj, hms_list_2):
		"""
		앞의시간에서 뒤의시간을 더하는데, -로 넣으면 뻘샘도 된다

		:param input_dt_obj:
		:param hms_list_2: [시, 분, 초]
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		sec_1 = self.get_dt_timestamp_for_dt_obj(input_dt_obj)
		sec_2 = self.change_hms_list_to_sec(hms_list_2)
		temp = sec_1 + sec_2
		result = self.change_sec_to_hms_list(temp)
		return result

	def plus_two_hms_list(self, hms_list_1, hms_list_2):
		"""
		앞의시간에서 뒤의시간을 더하는데, -로 넣으면 뻘샘도 된다

		:param hms_list_1: [시, 분, 초]
		:param hms_list_2: [시, 분, 초]
		:return:
		"""
		sec_1 = self.change_hms_list_to_sec(hms_list_1)
		sec_2 = self.change_hms_list_to_sec(hms_list_2)
		result = self.change_sec_to_hms_list(sec_1 + sec_2)
		return result

	def read_no_only(self, input_text):
		"""
		입력텍스트에서 숫자만 분리해서 만든다

		:param input_text:
		:return:
		"""

		result = []
		temp = ""
		for one in input_text:
			if one in "1234567890" and temp:
				temp = temp + one
			elif one in "1234567890" and not temp:
				temp = one
			elif not one in "1234567890" and temp:
				result.append(temp)
				temp = ""
			elif not one in "1234567890" and not temp:
				pass
		return result

	def read_today_value(self, time_char=time.localtime(time.time())):
		"""
		종합 -----> ['04/05/02', '22:07:48', '04/05/02 22:07:48','2002-04-05']
		040621 : 이름을 변경 (total -> today)
		"""
		aaa = str(time.strftime('%c', time_char)).split()
		total_dash = time.strftime('%Y', time_char) + "-" + time.strftime('%m', time_char) + "-" + time.strftime('%d', time_char)
		return [aaa[0], aaa[1], time.strftime('%c', time_char), total_dash]

	def replace_dt_obj_by_dic_time(self, dt_obj, input_dic):
		"""
		datetime.replace(year=self.year, month=self.month, day=self.day, hour=self.hour, minute=self.minute,
		second=self.second, microsecond=self.microsecond, tzinfo=self.tzinfo, fold=0)
		입력된 시간의 특정 단위를 바꿀수있다
		즉, 모든 년을 2002로 바꿀수도 있다는 것이다

		:param dt_obj: 날짜 객체
		:param input_dic:
		:return:
		"""
		new_dt_obj = dt_obj.replace(input_dic)
		return new_dt_obj

	def replace_holiday_for_sunday(self, input_data):
		"""
		대체공휴일의 날짜를 확인하는 것이다
		input_data : [2009, 5, 5, 5, 5, '양', 1, '', '어린이날']
		[시작일], [끝나는날],[월, 일, 음/양, 몇일간, 윤달여부],[요일 - 대체적용일], [설명]

		:param input_data:
		:return:
		"""
		holiday_replace = [
			[[19590327, 19601230], ["all"], [6], ["대체공휴일제도"]],  # 모든공휴일에 대해서 대체공휴일 적용(일요일)
			[[19890301, 19901130], ["all"], [6], ["대체공휴일제도"]],  # 모든공휴일에 대해서 대체공휴일 적용(일요일)

			[[20131105, 99991231], [12, "말일", "음", 1, "윤달"], [6], ["설날", "대체공휴일제도"]],
			[[20131105, 99991231], [1, 1, "음", 2, "평달"], [6], ["신정", "대체공휴일제도"]],
			[[20131105, 99991231], [5, 5, "양", 1, ""], [5, 6], ["어린이날", "대체공휴일제도"]],  # 토/일요일
			[[20131105, 99991231], [8, 14, "음", 3, "평달"], [6], ["추석", "대체공휴일제도"]],

			[[20210715, 99991231], [3, 1, "양", 1, ""], [6], ["31절", "대체공휴일제도"]],
			[[20210715, 99991231], [10, 3, "양", 1, ""], [6], ["개천절", "대체공휴일제도"]],
			[[20210715, 99991231], [10, 9, "양", 1, ""], [6], ["한글날", "대체공휴일제도"]],

			[[20230504, 99991231], [12, 25, "양", 1, ""], [6], ["기독탄신일", "대체공휴일제도"]],
			[[20230504, 99991231], [4, 8, "음", 1, "평달"], [6], ["부처님오신날", "대체공휴일제도"]],
		]

		result = []
		dt_obj = self.change_ymd_list_to_dt_obj(input_data[0:3])
		week_no_7 = self.get_weekno_set_for_dt_obj(dt_obj[0])
		day_no = int(input_data[0]) * 10000 + int(input_data[1]) * 100 + int(input_data[2])

		for list1d in holiday_replace:
			change_day = False
			if list1d[0][0] <= day_no and list1d[0][1] >= day_no:
				if list1d[1][0] == "all" and week_no_7 in list1d[3]:
					# 대체휴일적용대상임
					change_day = True
				elif input_data[-1] == list1d[-1][0] and week_no_7 in list1d[3]:
					change_day = True

			if change_day:
				# print("대체공휴일 적용 =====> ")
				new_dt_obj = dt_obj + datetime.timedelta(days=1)
				new_ymd_list = self.get_ymd_list_for_dt_obj(new_dt_obj)
				result = new_ymd_list + input_data[3:] + ["대체공휴일적용", ]

		return result

	def roundup_hms_list(self, hms_list, base="min", condition="무조건"):
		"""
		시분초를 기준으로 그 윗부분을 반올림하는 것

		:param hms_list: [시, 분, 초]
		:param base:
		:param condition:
		:return:
		"""
		if base == "min":
			if condition == "무조건" and (hms_list[1] > 0 or hms_list[2] > 0):
				hms_list[0] = hms_list[0] + 1
			elif condition == "무조건" and hms_list[1] == 0 and hms_list[2] == 0:
				pass
			elif condition != "무조건" and (hms_list[1] > 0 or hms_list[2] > 0):
				if hms_list[2] >= 30: hms_list[1] = hms_list[1] + 1
				if hms_list[1] >= 30: hms_list[0] = hms_list[0] + 1
			elif condition != "무조건" and hms_list[1] == 0 and hms_list[2] == 0:
				pass
			result = [hms_list[0], 0, 0]
		elif base == "sec":
			if condition == "무조건" and hms_list[2] > 0:
				mok, namuji = divmod(hms_list[1] + 1, 60)
				result = [hms_list[0] + mok, namuji, 0]
			elif condition == "무조건" and hms_list[2] == 0:
				result = [hms_list[0], hms_list[1], 0]
			elif condition != "무조건" and hms_list[2] > 0:
				if hms_list[2] > 30: hms_list[2] = hms_list[2] + 1
				mok, namuji = divmod(hms_list[2], 60)
				result = [hms_list[0] + mok, namuji, 0]
			elif condition != "무조건" and hms_list[2] == 0:
				result = [hms_list[0], hms_list[1], 0]
		else:
			result = "error"
		return result

	def run_at_special_time(self, input_hms_list):
		"""

		:param input_hms_list:
		:return:
		"""
		if type(input_hms_list) == type(123):
			dt_obj_1 = self.get_dt_obj_for_now_as_local_time_zone()
			dt_obj_2 = self.shift_sec_for_dt_obj(dt_obj_1, input_hms_list)
			checked_input_hms_list = self.util.change_all_list_element_to_int(self.change_dt_obj_to_hms_list(dt_obj_2))
		else:
			checked_input_hms_list = self.util.change_all_list_element_to_int(input_hms_list)

		while 1:
			ymdhms = self.util.change_all_list_element_to_int(self.get_ymdhms_for_now_by_local())
			if [ymdhms[3], ymdhms[4], ymdhms[5]] == checked_input_hms_list:
				return ymdhms
		return False

	def set_format_for_utc(self, input_utc, input_format):
		"""
		utc : utc의 timestamp, utc시간숫자, 1640995200.0 또는 ""

		:param input_utc: utc 시간객체
		:param input_format:
		:return:
		"""
		input_utc = self.check_input_utc(input_utc)
		result = time.strftime(input_format, input_utc)
		return result

	def shft_dt_obj_with_option(self, input_dt_obj, **option):
		"""
		datetime객체를 입력하는 형태에따라서 이동시키는 것

		:param input_dt_obj:
		:param option:
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)

		if "year" in option.keys(): input_dt_obj = self.shift_year_for_dt_obj(input_dt_obj, option["year"])

		if "mon" in option.keys(): input_dt_obj = self.shift_month_for_dt_obj(input_dt_obj, option["mon"])
		if "month" in option.keys(): input_dt_obj = self.shift_month_for_dt_obj(input_dt_obj, option["month"])

		if "day" in option.keys(): input_dt_obj = input_dt_obj + datetime.timedelta(days=int(option["day"]))
		if "hour" in option.keys(): input_dt_obj = input_dt_obj + datetime.timedelta(hours=int(option["hour"]))

		if "min" in option.keys(): input_dt_obj = input_dt_obj + datetime.timedelta(minutes=option["min"])
		if "minute" in option.keys(): input_dt_obj = input_dt_obj + datetime.timedelta(minutes=int(option["minute"]))

		if "sec" in option.keys(): input_dt_obj = input_dt_obj + datetime.timedelta(seconds=int(option["sec"]))
		if "second" in option.keys(): input_dt_obj = input_dt_obj + datetime.timedelta(seconds=int(option["second"]))

		return input_dt_obj

	def shift_day_for_dt_obj(self, dt_obj, input_no):
		"""
		날짜를 이동

		:param dt_obj: 날짜 객체
		:param input_no:
		:return:
		"""
		new_dt_obj = dt_obj + datetime.timedelta(days=input_no)
		return new_dt_obj

	def shift_day_for_ymd_list(self, input_ymd_list="", input_no=0):
		"""
		입력한 날짜리스트를 기준으로 날을 이동시키는것
		아무것도 입력하지 않으면 현재 시간
		입력값 : [2022, 03, 02]
		출력값 : 2022-01-01

		:param input_ymd_list: [년, 월, 일]
		:param input_no:
		:return:
		"""
		dt_obj = self.change_ymd_list_to_dt_obj(input_ymd_list)
		changed_dt_obj = dt_obj + datetime.timedelta(days=int(input_no))
		result = self.get_ymd_list_for_dt_obj(changed_dt_obj)
		return result

	def shift_hour_for_dt_obj(self, input_dt_obj="", input_no=0):
		"""
		시간을 이동

		:param dt_obj: 날짜 객체
		:param input_no:
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		new_dt_obj = input_dt_obj + datetime.timedelta(hours=input_no)
		return new_dt_obj

	def shift_min_for_dt_obj(self, input_dt_obj="", input_no=0):
		"""
		분을 이동

		:param dt_obj: 날짜 객체
		:param input_no:
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		new_dt_obj = input_dt_obj + datetime.timedelta(minutes=input_no)
		return new_dt_obj

	def shift_month_for_dt_obj(self, input_dt_obj, input_no):
		"""
		시간이동 : 입력시간에 대해서 n번째 월로 이동

		:param dt_obj: 날짜 객체
		:param input_no:
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		original_mon = input_dt_obj.month
		original_year = input_dt_obj.year

		delta_year, delta_month = divmod(input_no, 12)

		if original_mon <= delta_month * -1 and 0 > delta_month:
			original_mon = original_mon + 12
			original_year = original_year - 1

		new_month = original_mon + delta_month
		new_year = original_year + delta_year

		delta_year_1, delta_month_1 = divmod(new_month, 12)
		final_new_year = original_year + delta_year_1

		new_dt_obj = input_dt_obj.replace(year=final_new_year)
		new_dt_obj = new_dt_obj.replace(month=delta_month_1)
		return new_dt_obj

	def shift_month_for_text_time(self, input_text_time, input_no):
		"""
		기준날짜에서 몇번째 월로 이동시키는것

		:param input_text_time: 문자열로된 날짜나 시간
		:param input_no:
		:return:
		"""
		dt_obj = self.check_input_time(input_text_time)
		changed_dt_obj = self.shift_month_for_dt_obj(dt_obj, input_no)
		result = self.get_ymd_list_for_dt_obj(changed_dt_obj)
		return result

	def shift_month_for_ymd_list(self, input_ymd_list="", input_month=0):
		"""
		기준날짜에서 월을 이동시키는것

		:param input_ymd_list: 년월일의 리스트를 넣는다
		:param input_month: 월
		:return:
		"""
		dt_obj = self.check_input_time(input_ymd_list)
		changed_dt_obj = dt_obj.shift(months=int(input_month))
		result = self.get_ymd_list_for_dt_obj(changed_dt_obj)
		return result

	def shift_sec_for_dt_obj(self, input_dt_obj="", input_sec=""):
		"""
		날짜객체를 초단위로 이동시키는 것

		timedelta에서 사용가능한 것
			days	일
			seconds	초
			microseconds	마이크로 초
			milliseconds	밀리 초 (1밀리 초는 1000마이크로 초)
			minutes	분
			hours	시간
			weeks	주 (7일을 의미함)


		:param dt_obj: 날짜 객체
		:param input_no:
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		changed_dt_obj = input_dt_obj + datetime.timedelta(seconds=int(input_sec))
		return changed_dt_obj

	def shift_week_for_dt_obj(self, input_dt_obj, input_no):
		"""
		입력시간을 기준으로 n번째 주로 이동

		shift : 일부분만 변경
		move : 전체가 변경

		:param dt_obj: 날짜 객체
		:param input_no:
		:return:
		"""
		if not input_dt_obj:
			input_dt_obj = self.get_dt_obj_for_now()
		new_dt_obj = input_dt_obj + datetime.timedelta(days=input_no * 7)
		return new_dt_obj

	def shift_year_for_dt_obj(self, input_dt_obj="", input_year_no=""):
		"""
		입력시간을 기준으로 n번째 년으로 이동
		년도는 timedelta가 없어서 년도 자체랄 바꾸는 방법을 사용하는 것이다

		shift : 일부분만 변경
		move : 전체가 변경

		:param dt_obj: 날짜 객체
		:param input_year_no:
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		new_year = input_dt_obj.year + input_year_no
		new_dt_obj = input_dt_obj.replace(year=new_year)
		return new_dt_obj

	def shift_year_for_ymd_list(self, input_ymd_list="", input_year=0):
		"""
		기준날짜에서 년을 이동시키는것
		입력형태 : [2022, 3, 1]

		:param input_ymd_list: [년, 월, 일] [2022, 3, 1]
		:param input_year: 년
		:return:
		"""
		dt_obj = self.check_input_time(input_ymd_list)
		dt_obj_changed = dt_obj.shift(years=int(input_year))
		result = self.get_ymd_list_for_dt_obj(dt_obj_changed)
		return result

	def shift_ymd_list_for_ymd_list(self, ymd_list_1, ymd_list_2):
		"""
		ymd_list형식의 입력값을 3년 2개월 29일을 이동시킬때 사용하는것

		:param ymd_list_1: [년, 월, 일]
		:param ymd_list_2: [년, 월, 일]
		:return:
		"""
		dt_obj = self.change_ymd_list_to_dt_obj(ymd_list_1)
		changed_dt_obj = self.shift_day_for_dt_obj(dt_obj, ymd_list_2[2])
		changed_dt_obj = self.shift_month_for_dt_obj(changed_dt_obj, ymd_list_2[1])
		changed_dt_obj = self.shift_year_for_dt_obj(changed_dt_obj, ymd_list_2[0])
		result = self.get_ymd_list_for_dt_obj(changed_dt_obj)
		return result

	def shift_ymdhms_list_for_dt_obj(self, input_dt_obj="", input_ymdhms_list=""):
		"""
		날짜를 이동

		:param dt_obj: 날짜 객체
		:param input_no:
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		changed_dt_obj = self.shift_sec_for_dt_obj(input_dt_obj, input_ymdhms_list[0])
		changed_dt_obj = self.shift_min_for_dt_obj(changed_dt_obj, input_ymdhms_list[1])
		changed_dt_obj = self.shift_hour_for_dt_obj(changed_dt_obj, input_ymdhms_list[2])
		changed_dt_obj = self.shift_day_for_dt_obj(changed_dt_obj, input_ymdhms_list[3])
		changed_dt_obj = self.shift_month_for_dt_obj(changed_dt_obj, input_ymdhms_list[4])
		changed_dt_obj = self.shift_year_for_dt_obj(changed_dt_obj, input_ymdhms_list[5])
		return changed_dt_obj

	def split_dt_obj_by_dt_obj(self, start_dt_obj, end_dt_obj, split_dt_obj):
		"""
		어떤 날짜를 기준으로 둘로 나누는것
		기준시간에서 1조전의 기간으로 나누는 것이다

		:param start_dt_obj: datetime객체
		:param end_dt_obj: datetime객체
		:param split_dt_obj: datetime객체
		:return:
		"""
		result = False
		if start_dt_obj > split_dt_obj > end_dt_obj:
			new_end_dt_obj = self.shift_sec_for_dt_obj(split_dt_obj, -1)
			result = [start_dt_obj, new_end_dt_obj, end_dt_obj, split_dt_obj]
		return result

	def split_period_as_year_basis(self, input_ymd_list1, input_ymd_list2):
		"""
		날짜기간이 년이 다른경우 같은 year들로 리스트형태로 기간을 만들어 주는것
		입력값을 확인하는 것이다

		:param input_ymd_list1: [년, 월, 일]
		:param input_ymd_list2: [년, 월, 일]
		:return:
		"""
		dt_obj1 = self.check_input_time(input_ymd_list1)
		input_ymd_list1 = self.get_ymd_list_for_dt_obj(dt_obj1)

		dt_obj2 = self.check_input_time(input_ymd_list2)
		input_ymd_list2 = self.get_ymd_list_for_dt_obj(dt_obj2)

		# 2가지의 날짜가 들어오면, 1년단위로 시작과 끝의 날짜를 만들어 주는 것이다
		start_1 = int(input_ymd_list1[0]) * 10000 + int(input_ymd_list1[1]) * 100 + int(input_ymd_list1[2])
		end_1 = int(input_ymd_list2[0]) * 10000 + int(input_ymd_list2[1]) * 100 + int(input_ymd_list2[2])
		result = []

		# 날짜가 늦은것을 뒤로가게 만드는 것이다
		start_ymd = input_ymd_list1
		end_ymd = input_ymd_list2
		if start_1 > end_1:
			start_ymd = input_ymd_list2
			end_ymd = input_ymd_list1

		# 만약 년도가 같으면, 그대로 돌려준다
		if int(start_ymd[0]) == int(end_ymd[0]):
			result = [[start_ymd, end_ymd]]
		# 만약 1년의 차이만 나면, 아래와 같이 간단히 만든다
		elif int(end_ymd[0]) - int(start_ymd[0]) == 1:
			result = [
				[start_ymd, [start_ymd[0], 12, 31]],
				[[end_ymd[0], 1, 1], end_ymd],
			]
		# 2년이상이 발생을 할때 적용하는 것이다
		else:
			result = [[start_ymd, [start_ymd[0], 12, 31]], ]
			for year in range(int(start_ymd[0]) + 1, int(end_ymd[0])):
				result.append([[year, 1, 1], [year, 12, 31]])
			result.append([[end_ymd[0], 1, 1], end_ymd])
		return result

	def split_range_time_per_day(self, input_dt1, input_dt2):
		"""
		시간간격을 매일 날짜로 나누어진 리스트형태로 만든다

		:param input_dt1: datetime객체
		:param input_dt2: datetime객체
		:return:
		"""
		result = []
		ymd_list_1 = self.get_ymd_list_for_dt_obj(input_dt1)
		ymd_list_1_shft_1 = self.shift_day_for_ymd_list(ymd_list_1, 1)
		ymd_list_2 = self.get_ymd_list_for_dt_obj(input_dt2)
		sec_datas_1 = self.change_dt_obj_to_sec_set(input_dt1)
		sec_datas_2 = self.change_dt_obj_to_sec_set(input_dt2)
		week_no_1 = self.change_ymd_list_to_yearweekno(ymd_list_1)
		week_no_2 = self.change_ymd_list_to_yearweekno(ymd_list_2)
		if ymd_list_1 == ymd_list_2:
			# [e₩u=, [2023,2,22], 19340, 25430]
			temp = [week_no_1, ymd_list_1, sec_datas_1[2], sec_datas_2[2]]
			result.append([temp])
		elif ymd_list_1_shft_1 == ymd_list_2:
			temp_1 = [week_no_1, ymd_list_1, sec_datas_1[2], sec_datas_2[2]]
			temp_2 = [week_no_2, ymd_list_2, sec_datas_2[2], sec_datas_2[2]]
			result.append(temp_1)
			result.append(temp_2)
		else:
			temp_1 = [week_no_1, ymd_list_1, sec_datas_1[2], sec_datas_2[2]]
			result.append(temp_1)
			delta_day = self.delta_two_ymd_list(ymd_list_2, ymd_list_1)
			print(delta_day)
			for one in range(1, delta_day[2]):
				new_ymd_list = self.shift_day_for_ymd_list(ymd_list_1, one)
				week_no_3 = self.change_ymd_list_to_yearweekno(new_ymd_list)
				result.append([week_no_3, new_ymd_list, 1, 86400])
			temp_2 = [week_no_2, ymd_list_2, sec_datas_2[2], sec_datas_2[2]]
			result.append(temp_2)
		return result

	def terms(self):
		"""
		용어들에 대한 정의
		"""
		result = """
		윈도우시간 : 1601년 1월1일을 0으로하여 계산하는 윈도우의 시간
		엑셀 시간 : 1900년부터 시작하는 밀리초단위로 계산 (밀리초를 0단위로하여 계산), 기존에 더 유명했던 로터스의 시간과 맞추기위하여 적용
		리눅스  시간     : 1970년부터 시작하는 초단위를 기준 (초를 0단위로 계산, 소숫점이 있음)
		utc  : 1970년 1월 1일을 0밀리초로 계산한 것 
		utc  : 1640995200.0 또는 "", 1648037614.4801838 (의미 : 2022-03-23T21  13:34.480183+09:00)
		datetime : 1900.1.1을 1초로 시작

		datetime class : 1년 1월1일부터 날짜를 시작, 1년은 3600*24초로 계산
		ISO형식 : 2023-03-01T10:01:23.221000, 2023-03-01T10:01:23.221000+09:00, 2023-03-01

		text_time : 문자열 형식으로된 시간표현, 시간객체가 아닌 글자로 표현된 시간
		dic_time : 사전형식으로 된 시간표현
		dt_obj : 시간 객체

		ymd_list : [년, 월, 일], [2000, 01, 01]
		hms_list : [시, 분, 초]
		datelist    : [2000, 01, 01]
		ymdhms_list : [년, 월, 일, 시, 분, 초]
		intersect : 두시간이 곂치는 부분
		update : 시간의 일부를 바꾸는것
		shift : 시간의 일부를 이동시키는것, 현재의 값을 같은 형태에서 값을 이동시키는것
		isocalendar : [year, week, weekday]
		sec_datas : sec형식을 가진 여러개의 집합
		date : 2000-01-01
		time : 시간의 여러형태로 입력을 하면, 이에 맞도록 알아서 조정한다
		dhms : 2일3시간10분30초, day-hour-minute-sec
		move : 입력값에 더하거나 빼서 다른 값으로 바꾸는것, 입력값과 출력값이 다를때 (출력값을 입력의 형태로 바꾸면 값이 다른것)
		change     : 형태를 바꾼것
		read : 입력값을 원하는 형태로 변경해서 갖고오는것
		get  : 입력값에서 원하는 형태의 값을 갖고오는것
		utc class    : 1970년 1월1일부터 날짜를 시작
		week_no_7    : 요일에대한 번호 (0~7)
		yearweekno  : 1년의 주번호 (1~55)
		week_no     : yearweekno를 뜻함
		timestamp : utc시간으로 만들어 주는것
		"""
		return result

	def time_check_inputtime(self, time_char=""):
		"""
		입력시간을 확인하는 것

		:param time_char:
		:return:
		"""
		if time_char == "":
			result = time.localtime()
		else:
			result = time.localtime(time_char)
		return result

	def time_read_all(self, time_char=""):
		"""

		:param time_char:
		:return:
		"""

		if time_char == "":
			lt = time.localtime()
		else:
			lt = time.localtime(time_char)

		# s는 short, e는 english, l은 long
		year_s = time.strftime('%y', lt)
		year = time.strftime('%Y', lt)

		mon = time.strftime('%m', lt)
		mon_e = time.strftime('%b', lt)
		mon_e_l = time.strftime('%B', lt)

		day = time.strftime('%d', lt)
		day_l = time.strftime('%j', lt)

		week_no = time.strftime('%w', lt)
		yearweek_no = time.strftime('%W', lt)
		week_e = time.strftime('%a', lt)
		week_e_l = time.strftime('%A', lt)

		hour = time.strftime('%I', lt)
		hour_l = time.strftime('%H', lt)
		ampm = time.strftime('%p', lt)
		min = time.strftime('%M', lt)
		sec = time.strftime('%S', lt)
		result = {"year_s": year_s, "year": year,
				  "month": mon, "mon": mon, "mon_e": mon_e, "mon_e_l": mon_e_l,
				  "day": day, "day_l": day_l,
				  "hour": hour, "hour_l": hour_l,
				  "ampm": ampm,
				  "min": min, "minute": min,
				  "sec": sec, "second": sec,
				  "week_no": week_no, "week_e": week_e, "week_e_l": week_e_l, "yearweek_no": yearweek_no}
		return result

	def time_today(self):
		"""
		지금시간의 정보를 알려주는 것
		"""
		lt = time.localtime()
		year = time.strftime('%Y', lt)
		mon = time.strftime('%m', lt)
		day = time.strftime('%d', lt)

		result = str(year) + "-" + str(mon) + "-" + str(day)
		print(result)
		return result

	def today(self):
		"""

		:return:
		"""
		lt = time.localtime()
		self.year = self.make_2_digit(lt.tm_year)
		self.mon = self.make_2_digit(lt.tm_mon)
		self.day = self.make_2_digit(lt.tm_mday)
		total_dash = self.year + "-" + self.mon + "-" + self.day
		return total_dash

	def update_dt_obj_by_dic_time(self, input_dt_obj="", input_dic=""):
		"""
		사전형식의 값들을 이용하여, 기존 시간값을 바꾼다

		:param input_dt_obj: datetime객체
		:param input_dic:
		:return:
		"""
		input_dt_obj = self.check_dt_obj(input_dt_obj)
		dic_time = self.change_dt_obj_to_dic_time(input_dt_obj)
		dic_time.update(input_dic)
		result = self.change_dic_time_to_dt_obj(dic_time)
		return result


