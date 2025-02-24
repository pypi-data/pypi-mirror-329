# -*- coding: utf-8 -*-
import csv, difflib, bisect, filecmp, random
import shutil, pickle, inspect, string, glob, math
import chardet, pyautogui
import re, os, collections
import zipfile, sys
import itertools
import pyperclip
from datetime import datetime

import jfinder, scolor, pynal, basic_data  # xython 모듈
import win32con, win32com, win32gui, win32api  # pywin32의 모듈


class youtil():
	"""
	2025-10-24 : anydb를 youtil과 통합함

	여러가지 사무용에 사용할 만한 메소드들을 만들어 놓은것이며,
	좀더 특이한 것은 youtil2로 만들어서 사용할 예정입니다

	2024-09-08 : 전체적으로 손을 봄

	database를 사용하기 쉽게 만든것
	table, df의 자료는 [제일 첫컬럼에 컬럼이름을 넣는다]
	list_db의 형태 : [[y_name-1, y_name_2.....],[[a1, a2, a3...], [b1, b2, b3...], ]]

	list_db : series형태로된 리스트의 묶음, 일반 list_2d와는 가로세로가 반대로 되어있다
	"""

	def __init__(self, db_name=""):
		self.xre = jfinder.jfinder()
		self.xcolor = scolor.scolor()
		self.vars = basic_data.basic_data().vars

		# 가끔 사용하다보면, css를 좀더 쉽게 사용했으면 할때가 있다
		self.db_name = db_name
		self.table_name = ""

	def _check_border_data(self, input_list):
		"""
		선에대한 속성중에서 자주사용하는 것에대해서 정의를 해놓고
		편하게 사용이 가능하도록 만든 것이다
		"""
		result = {}
		for value in input_list:
			if type(value) == type(123):
				result["thickness"] = str(value) + "px"
			elif value in ["solid", "dot"]:
				result["style"] = value
			else:
				try:
					rgbint = self.xcolor.change_scolor_to_hex(value)
					result["color"] = rgbint
				except:
					pass
		return result

	def _check_border_outline_data(self, input_dic):
		"""
		외관선에대한 자료를 확인해 주는 것
		"""
		result = ""
		if "position" in input_dic.keys():
			if input_dic["position"] == "bottom":
				result = result + "border-bottom :"
		if "thickness" in input_dic.keys():
			result = result + "border-width : " + self.change_list_to_padding_value(input_dic["thickness"]) + "; "
		if "style" in input_dic.keys():
			result = result + "border-style : " + input_dic["style"] + "; "
		if "color" in input_dic.keys():
			result = result + "border-color : " + input_dic["color"] + "; "
		if "radius" in input_dic.keys():
			result = result + "border-radius : " + self.change_list_to_padding_value(input_dic["radius"]) + "; "
		return result

	def _check_cell_data(self, *input_list):
		"""
		_check로 시작되는 메소드는 일반적으로 내부적으로 사용하는 편한 용어를 공식적인 단어로 변경해주는 역활을 하는 것이다
		예를들어 bold는 '진하게'로도 사용가능해서, 이것을 다시 공식적인 bold로 만들어 주는 것이다

		백그라운드에대한 속성중에서 자주사용하는 것에대해서 정의를 해놓고
		편하게 사용이 가능하도록 만든 것이다
		"""
		result = {}
		for value in input_list:
			if type(value) == type(123.0) and value <= 1:
				result["opacity"] = value
			elif value in ["bold", "진하게"]:
				result["bold"] = True
			elif value in ["밑줄", "underline"]:
				result["underline"] = True
			elif value in ["italic", "이탈릭채", "기울게", "이탈릭"]:
				result["foitalic"] = True
			elif self.xre.is_match("[시작][영어:3~8][숫자:2~2][끝]", value):
				try:
					rgbint = self.xcolor.change_scolor_to_rgbint(value)
					result["bgcolor"] = rgbint
				except:
					pass
		return result

	def _check_cell_line_data(self, *input_list):
		"""
		엑셀의 셀 라인에 대한 색이나 특성을 지정하기 위한것
		"""
		result = {"thickness": False,
				  "alpha": False,
				  "style": False,
				  "color": False,
				  "area": False,
				  }

		for value in input_list:
			if value in self.vars["check_line_thickness"].keys():
				result["thickness"] = self.vars["check_line_thickness"][value]
			elif type(value) == type(0.123):
				result["alpha"] = value
			elif value in self.vars["check_line_style"].keys():
				result["style"] = self.vars["check_line_style"][value]
			elif value in self.vars["check_line_position"].keys():
				result["position"] = self.vars["check_line_position"][value]
			elif self.xre.is_match("[시작][영어:3~8][숫자:2~2][끝]", value):
				try:
					rgbint = self.xcolor.change_scolor_to_rgbint(value)
					result["color"] = rgbint
				except:
					pass
		return result

	def _check_font_data(self, *input_list):
		"""
		폰트 관련된 자료가 들어가있는 자료를 폰트에 사용되는 공식적인 용어로 바꾸어서 사전으로 만든것

		:param input_list:
		:return:
		"""
		result = {"size": False,
				  "alpha": False,
				  "bold": False,
				  "underline": False,
				  "strikethrough": False,
				  "align_h": False,
				  "align_v": False,
				  "superscript": False,
				  "subscript": False,
				  "italic": False,
				  "color": False,
				  }

		for value in input_list:
			if type(value) == type(123):
				result["size"] = value
			elif type(value) == type(0.123):
				result["alpha"] = value
			elif value in ["bold", "진하게"]:
				result["bold"] = True
			elif value in ["밑줄", "underline"]:
				result["underline"] = True
			elif value in ["strikethrough", "취소", "취소선", "strike"]:
				result["strikethrough"] = True
			elif value in ["수평정렬", "수평", "align_h"]:
				result["align_h"] = True
			elif value in ["수직정렬", "수직", "align_v"]:
				result["align_v"] = True
			elif value in ["윗첨자", "superscript"]:
				result["superscript"] = True
			elif value in ["아래첨자", "subscript"]:
				result["subscript"] = True
			elif value in ["italic", "이탈릭채", "기울게", "이탈릭"]:
				result["italic"] = True
			elif self.xre.is_match("[시작][영어:3~8][숫자:2~2][끝]", value):
				try:
					rgbint = self.xcolor.change_scolor_to_rgbint(value)
					result["color"] = rgbint
				except:
					pass
		return result

	def add_list_2d_in_list_2d(self, input_base_list_2d, input_sub_list_2d):
		"""
		2차원의 자료에 다른 2차원의 자료를 제목을 기준으로 붙이기
		새로운것을 붙일때는 기존의 값은 빈것을 넣는다
		yx의 순서로 자료가 입력되어야 함

		:param input_base_list_2d:
		:param input_sub_list_2d:
		:return:
		"""

		blank_list = []
		for one in range(1, len(input_base_list_2d[0])):
			blank_list.append("")

		blank_list2 = []
		for one in range(1, len(input_sub_list_2d[0])):
			blank_list2.append("")

		total_len = len(input_base_list_2d[0]) + len(input_sub_list_2d[0]) - 1

		for no1, value1 in enumerate(input_sub_list_2d):
			found = False
			if value1 == None: value1 = ""

			for no2, value2 in enumerate(input_base_list_2d):
				if value2 == None: value2 = ""
				if value1[0] == value2[0]:
					input_base_list_2d[no2].extend(value1[1:])
					found = True

			if not found:
				input_base_list_2d.append(blank_list.extend(value1[1:]))

		for no, list_1d in enumerate(input_base_list_2d):
			if len(list_1d) < total_len:
				input_base_list_2d[no].extend(blank_list2)
		return input_base_list_2d

	def add_text_for_all_filename_in_folder(self, input_folder, input_text="aaa_", front_or_end="front"):
		"""
		폴더안의 모든 파일이름에 텍스트를 앞이나 뒤에 추가하는 것

		:param input_folder:
		:param input_text:
		:param front_or_end:
		:return:
		"""
		all_filename = self.get_all_filename_in_folder(input_folder)
		for one_filename in all_filename:
			changed_filename = input_text
			if front_or_end == "front":
				changed_filename = input_text + one_filename
			elif front_or_end == "end":
				changed_filename = one_filename + input_text
			else:
				pass

			full_path_old = input_folder + "\\" + one_filename
			full_path_new = input_folder + "\\" + changed_filename
			self.change_filename(full_path_old, full_path_new)

	def append_text_for_list_2d_at_left(self, input_l2d, input_text):
		"""
		단, 모든 내부자료는 텍스트여야 한다

		:param input_l2d:
		:param input_text:
		:return:
		"""
		result = []
		for l1d in input_l2d:
			temp=[]
			for one_value in l1d:
				temp.append(str(input_text) + str(one_value))
			result.append(temp)
		return result

	def append_text_for_list_2d_at_right(self, input_l2d, input_text):
		"""
		단, 모든 내부자료는 텍스트여야 한다

		:param input_l2d:
		:param input_text:
		:return:
		"""
		result = []
		for l1d in input_l2d:
			temp = []
			for one_value in l1d:
				temp.append(str(one_value)+str(input_text))
			result.append(temp)
		return result
	def append_value_for_all_list_1d_in_list_2d(self, input_list_2d, input_value):
		"""
		같은 항목으로 되어있는 자료를 제일 처음의 자료를 기준으로 합치는것
		2차원 리스트의 모든 자료끝에 값 추가하기
		2차원 리스트의 모든 자료끝에 값 추가하기
		모든 기존값에 입력되는 값을 추가하는것
		[[1],[2],[3]] ==> [[1,77],[2,77],[3,77]]

		:param input_list_2d:
		:param input_value:
		:return:
		"""
		result = []
		for list_1d in input_list_2d:
			result.append(list_1d.append(input_value))
		return result

	def arrange_min(self, input_data):
		"""
		계산용자료

		xyxy의 영역자료가 들어오면, 작은것부터 정렬하는것

		:param input_data:
		:return:
		"""
		x1, y1, x2, y2 = input_data
		if x1 > x2:
			new_x1 = x2
			new_x2 = x1
		else:
			new_x1 = x1
			new_x2 = x2

		if y1 > y2:
			new_y1 = y2
			new_y2 = y1
		else:
			new_y1 = y1
			new_y2 = y2
		return [new_x1, new_y1, new_x2, new_y2]

	def cal_basic_information_for_numbered_list_1d(self, list_1d):
		"""
		모든자료를 더해서 [total, eval, len(data), max(data), min(data)]를 돌려주는 것

		:param data:
		:return:
		"""
		total = 0
		for a in list_1d:
			total = total + a
		eval = total / len(list_1d)
		return [total, eval, len(list_1d), max(list_1d), min(list_1d)]

	def cal_center_for_any_many_cxy(self, input_cxy_list, value1=0, value2=0, total_len=0):
		"""
		재귀함수를 사용해서 리스트로 들어오는 좌표의 [x의합, y의합, 총갯수]의 형태로 돌려주는것
		리스트는 1차원이던 다차원이던 상관없이 계산된다

		:param input_cxy_list:
		:param value1:
		:param value2:
		:param total_len:
		:return:
		"""
		for one_cxy in input_cxy_list:
			if type(one_cxy[0]) == type([]):
				value1, value2, total_len = self.cal_center_for_any_many_cxy(one_cxy, value1, value2, total_len)
			else:
				value1 = value1 + one_cxy[0]
				value2 = value2 + one_cxy[1]
				total_len = total_len + 1
		return [value1, value2, total_len]

	def cal_container(self, path):
		"""
		폴더안의 크기를 돌려주는 것

		:param path:
		:return:
		"""
		total_size = 0
		for dirpath, dirnames, filenames in os.walk(path):
			for f in filenames:
				fp = os.path.join(dirpath, f)
				total_size += os.path.getsize(fp)
		return total_size

	def cal_degree_for_hms(self, input_dt_obj=""):
		"""
		현재의 시간을 각도로 만드는 방법

		:param input_dt_obj:
		:return:
		"""
		xytime = pynal.pynal()
		if input_dt_obj != "":
			now_dt_obj = input_dt_obj
		else:
			now_dt_obj = xytime.get_dt_obj_for_now()
		hour, min, sec = xytime.get_hms_list_for_dt_obj(now_dt_obj)
		hour, min, sec = int(hour), int(min), int(sec)

		# 시간 : 1시간은 30도의 각도임, 1분은 0.5도를 더해주어야함
		if int(hour) > 12:
			degree_hour = int(((12 - hour) / 12) * 360 + min * 0.5)
		else:
			degree_hour = int(((hour / 12) * 360) + min * 0.5)

		degree_min = int((min / 60) * 360)
		degree_sec = int((sec / 60) * 360)
		return [degree_hour, degree_min, degree_sec]

	def cal_no_to_mok_list(self, input_list, my_no):
		"""
		머릿글 기호를 쉽게 사용할수있도록 만들기 위해서 필한 함수
		어떤 리스트 형태로 되어있는 자료를 숯자에 맞는 형식으로 만들어 주는것

		:param input_list:
		:param my_no:
		:return:
		"""
		final_text = ""
		base_no = len(input_list)
		result = []
		if base_no > my_no:
			result = [my_no - 1]
		else:
			while True:
				mok, namuji = divmod(my_no, base_no)
				result.insert(0, namuji - 1)
				if mok < base_no:
					result.insert(0, mok - 1)
					break
				else:
					my_no = mok

		for index in result:
			final_text = final_text + input_list[index]
		return final_text

	def cal_range_address(self, son, mother):
		"""
		계산용자료

		두 영역이 겹쳐지는 영역을 게산하는것
		:param son:
		:param mother:
		:return:
		"""
		if len(son) == 2: son = son + son
		if len(mother) == 2: mother = mother + mother

		x1, y1, x2, y2 = self.arrange_min(son)
		x3, y3, x4, y4 = self.arrange_min(mother)

		## case1 오른쪽, 왼쪽, 위, 아래으로 벗어나 있는 경우
		if x2 < x3 or x1 > x4 or y2 < y3 or y1 > y4:
			kyo = [0, 0, 0, 0]
		else:
			cross_area = [max(x1, x3), max(y1, y3), min(x2, x4), min(y2, y4)]
			x_long_with_cross_area = [max(x1, x3), mother[1], min(x2, x4), mother[3]]
			y_long_with_cross_area = [mother[0], max(y1, y3), mother[2], min(y2, y4)]

		return [cross_area, x_long_with_cross_area, y_long_with_cross_area]

	def cal_xy_degree_distance(self, degree, length):
		"""
		각도와 길이를 주면 새로운 x, y주소를 계산해 준다
		위치는 0,0의 위치에서 계산을 하는 것이다

		:param degree:
		:param length:
		:return:
		"""
		degree = degree * 3.141592 / 180
		x = length * math.cos(degree)
		y = length * math.sin(degree)
		return [x, y]

	def change_10digit_number_to_base_letter_digit_number(self, input_no, show_letter="가나다라마바사아자차카타파하"):
		"""
		10진수값을 내가원하는 형식으로 변경하는것
		기본형을 예로들면 14진수이면서, 표현된,모양은 "0123456789abcd"가
		아니고 "가나다라마바사아자차카타파하"로 표현되는것

		:param input_no:
		:param show_letter:
		:return:
		"""
		digit_number = int(len(show_letter))
		q, r = divmod(input_no, digit_number)
		if q == 0:
			return show_letter[r]
		else:
			return self.change_10digit_number_to_base_letter_digit_number(q) + show_letter[r]

	def change_10digit_number_to_n_digit_number(self, input_no, digit_number=10):
		"""
		10진수값을 34진수까지의 진수형태로 변환
		진수값을 바꾸면 다른 진수형태로 변경된다

		:param input_no:
		:param digit_number:
		:return:
		"""
		base_letter = "0123456789abcdefghijklmnopqrstuvwxyz"
		q, r = divmod(input_no, digit_number)
		if q == 0:
			return base_letter[r]
		else:
			return self.change_10digit_number_to_n_digit_number(q, digit_number) + base_letter[r]

	def change_2_list_to_dic(self, key_list, value_list):
		"""
		두개의 리스트를 받으면 사전으로 만들어 주는 코드

		:param key_list:
		:param value_list:
		:return:
		"""
		result = dict(zip(key_list, value_list))
		return result

	def change_List_3d_to_list_1d_by_grouping_count(self, input_List_3d, index_no=4):
		"""
		index번호를 기준으로 그룹화를 만드는 것

		:param input_List_3d:
		:param index_no:
		:return:
		"""
		result = []
		for input_list_2d in input_List_3d:
			sorted_input_list_2d = self.sort_list_2d_by_index(input_list_2d, index_no)
			grouped_List_3d = self.change_list_2d_to_list_1d_group_by_no(sorted_input_list_2d, index_no)
			result = result + grouped_List_3d
		return result

	def change_all_value_in_list_1d_as_capital(self, input_list_1d):
		"""
		1차원리스트의 모든 요소를 대문자로 만드는 것

		:param input_list_1d:
		:return:
		"""
		for a in range(len(input_list_1d)):
			try:
				input_list_1d[a] = (input_list_1d[a]).capitalize()
			except:
				pass
		return input_list_1d

	def change_all_value_in_list_1d_as_int(self, input_list_1d):
		"""
		1차원리스트의 모든 요소를 정수로 만드는 것

		:param input_list:
		:return:
		"""
		result = []
		for one in input_list_1d:
			result.append(int(one))
		return result

	def change_all_value_in_list_1d_as_lower(self, input_list_1d):
		"""
		1차원리스트의 모든 요소를 소문자로 만드는 것

		:param input_list:
		:return:
		"""
		for a in range(len(input_list_1d)):
			try:
				input_list_1d[a] = (input_list_1d[a]).lower()
			except:
				pass
		return input_list_1d

	def change_all_value_in_list_1d_as_upper(self, input_list_1d):
		"""
		1차원자료의 모든 내용물을 대문자로 만들어 주는 것이다

		:param input_list:
		:return:
		"""
		for a in range(len(input_list_1d)):
			try:
				input_list_1d[a] = (input_list_1d[a]).upper()
			except:
				pass
		return input_list_1d

	def change_all_value_to_list_1d_as_same_max_len_for_mixed_list(self, input_list="", xy=""):
		"""
		입력값이 1차원과 2차원의 자료가 섞여 일을때
		2차원의 자료형태로 모두 같은 크기로 만들어 주는것

		:param input_list:
		:param xy:
		:return:
		"""
		temp_result = []
		x_len, y_len = xy
		list1_max_len = len(input_list)
		list2_max_len = y_len
		count = int(list1_max_len / x_len)

		# 2차원자료중 가장 큰것을 계산한다
		for one_value in input_list:
			if type(one_value) == type([]):
				list2_max_len = max(list2_max_len, len(one_value))

		for one_value in input_list:
			temp_list = one_value
			# 모든 항목을 리스트형태로 만든다
			if type(one_value) != type([]):
				temp_list = [one_value]

			# 최대길이에 맞도록 적은것은 ""으로 갯수를 채운다
			if list2_max_len - len(temp_list) > 0:
				temp_list.extend([""] * (list2_max_len - len(temp_list)))
			temp_result.append(temp_list)

		result = []
		for no in range(count):
			start = no * x_len
			end = start + x_len
			result.append(temp_result[start:end])

		return result

	def change_alpha_to_jamo(self, input_alpha_list):
		"""
		알파벳으로 바꾼 자음과 모음을 다시 자음과 모음으로 바꾸는 것

		:param input_alpha_list:
		:return:
		"""
		changed_value = input_alpha_list
		data_set = self.vars["eng_vs_jamo_list"]
		for one_list in data_set:
			for one_data in one_list:
				changed_value = changed_value.replace(one_data[0], one_data[1])
		result = changed_value.split("_")[:-1]
		# 자모를 한글로 만드는 방법
		return result

	def change_alpha_to_korean(self, input_alpha_list):
		"""
		한글을 자음과 모음으로 분리해서, 알파벳으로 변경하는 것
		알파벳으로 바꾸면, 영문의 문자열 다루는 것을 사용할수도 있을것 같아 만들어 보았으며
		동시에 자음과 모음을 한번에 바꿀수있게 되는 것이다
		박 ==> ["ㅂ", "ㅏ", "ㄱ"] => "abc"
		이렇게 자음과 모음으로 구분된영어단어로 바뀌는 것이다
		자음과모음의 연결로도 가능하는데, 문제는 받침이 없는 경우와 space의 구분이 어렵다는 것이다

		:param input_alpha_list:
		:return:
		"""
		changed_value = input_alpha_list
		data_set = [
			[['sox', 'ㅙ'], ['ugx', 'ㅞ'], ],
			[['ox', 'ㅐ'], ['px', 'ㅒ'], ['gx', 'ㅔ'], ['rx', 'ㅖ'], ['so', 'ㅘ'], ['sx', 'ㅚ'], ['wx', 'ㅢ'], ['ug', 'ㅝ'],
			 ['ux', 'ㅟ'], ],
			[['a', 'ㄱ'], ['b', 'ㄴ'], ['c', 'ㄷ'], ['d', 'ㄹ'], ['e', 'ㅁ'], ['f', 'ㅂ'], ['g', 'ㅅ'], ['h', 'ㅇ'], ['i', 'ㅈ'],
			 ['j', 'ㅊ'], ['k', 'ㅋ'], ['l', 'ㅌ'], ['m', 'ㅍ'], ['n', 'ㅎ']],
			[['aa', 'ㄲ'], ['cc', 'ㄸ'], ['ff', 'ㅃ'], ['gg', 'ㅆ'], ['ii', 'ㅉ'], ['ag', 'ㄳ'], ['bi', 'ㄵ'], ['bn', 'ㄶ'],
			 ['da', 'ㄺ'], ['de', 'ㄻ'], ['df', 'ㄼ'], ['dg', 'ㄽ'], ['dl', 'ㄾ'], ['dm', 'ㄿ'], ['dn', 'ㅀ'], ['fg', 'ㅄ'], ],
			[['o', 'ㅏ'], ['p', 'ㅑ'], ['q', 'ㅓ'], ['r', 'ㅕ'], ['s', 'ㅗ'], ['t', 'ㅛ'], ['u', 'ㅜ'], ['v', 'ㅠ'], ['w', 'ㅡ'],
			 ['x', 'ㅣ'], ],
			[['z', '_']],
		]
		for one_list in data_set:
			for one_data in one_list:
				changed_value = changed_value.replace(one_data[0], one_data[1])
		result = changed_value.split("_")[:-1]
		return result


	def change_any_data_to_list(self, input_any_data):
		"""
		자료안의 모든것을 list로 변경

		:param input_any_data:
		:return:
		"""
		if isinstance(input_any_data, (list, tuple)):
			return [self.change_any_data_to_list(x) for x in input_any_data]
		elif isinstance(input_any_data, set):
			return set(self.change_any_data_to_list(x) for x in input_any_data)
		else:
			return input_any_data

	def change_any_data_to_list_2d(self, input_data):
		"""
			어떤 자료형이 오더라도 2차원의 리스트로 만들어 주는 것
			제일 중요한 부분이 리스트의 2차원으로 만들어주는 것이다
			youtil로 이동
			"""
		if type(input_data) == type([]) or type(input_data) == type(()):
			if type(input_data[0]) == type([]) or type(input_data[0]) == type(()):
				result = input_data
			else:
				result = [input_data]
		elif type(input_data) == type("123") or type(input_data) == type(123):
			result = [[input_data]]
		else:
			result = input_data

		revise_result = []
		for list_1 in result:
			temp = []
			for one in list_1:
				if one:
					pass
				elif type(one) == type(None) or one == [] or one == ():
					one = None
				elif type(one) == type([]) or type(one) == type(()):
					one = str(one)
				else:
					one = ""
				temp.append(one)
			revise_result.append(list(temp))

		return revise_result

	def change_base_letter_digit_number_to_10digit_number(self, input_no, show_letter="가나다라마바사아자차카타파하"):
		"""
		입력형식의 값을 10진수값으로 변경하는것
		10진수값을 내가원하는 형식으로 변경하는것
		기본형을 예로들면 14진수이면서, "가나다라마바사아자차카타파하"로 표현되는것

		:param input_no:
		:param show_letter:
		:return:
		"""
		new_dic = {}
		for no, one_value in enumerate(show_letter):
			new_dic[one_value] = no

		total = 0
		checked_no = reversed(input_no)
		for no, one in enumerate(checked_no):
			total = total + len(show_letter) ** (no) * new_dic[one]
		return total

	def change_binary_to_int(self, bits):
		"""
		이진수를 정수로 변환시키는 것

		:param bits:
		:return:
		"""
		return int(bits, 2)

	def change_binary_to_string(self, bits):
		"""
		이진수를 문자로 변환시키는 것

		:param bits:
		:return:
		"""
		return ''.join([chr(int(i, 2)) for i in bits])

	def change_char_to_num(self, input_char="입력필요"):
		"""
		문자열 주소를 숫자로 바꿔주는 것 ( b -> 2 )
		문자가 오던 숫자가 오던 숫자로 변경하는 것이다
		주소를 바꿔주는 것이다

		:param input_value: 입력 text
		"""
		aaa = re.compile("^[a-zA-Z]+$")  # 처음부터 끝가지 알파벳일때
		result_str = aaa.findall(str(input_char))

		bbb = re.compile("^[0-9]+$")  # 처음부터 끝가지 숫자일때
		result_num = bbb.findall(str(input_char))

		if result_str != []:  # 입력자료가 문자열 일때
			no = 0
			result = 0
			for one in input_char.lower()[::-1]:
				num = string.ascii_lowercase.index(one) + 1
				result = result + 26 ** no * num
				no = no + 1
		elif result_num != []:  # 입력자료가 숫자 일때
			result = int(input_char)
		else:
			result = "error"
		return result

	def change_csv_file_to_dic(self, filename):
		"""
		사전형자료를 key 와 value 쌍으로 연속해서 만든 문자열형태로 CSV 파일로 저장한 텍스트화일을
		다시 사전형으로 만드는 것

		:param filename:
		:return:
		"""
		result = []

		temp = self.read_csv_text_file_as_list_1d(filename)

		for no in range(int(len(temp) / 2)):
			key_data = temp[no * 2]
			value_data = temp[no * 2 + 1]
			result[key_data] = value_data
		return result

	def change_df_to_list(self, df_obj):
		"""
		df자료를 커럼과 값을 기준으로 나누어서 결과를 돌려주는 것이다

		:param df_obj:
		:return:
		"""
		result = []
		col_list = df_obj.columns.values.tolist()
		value_list = df_obj.values.tolist()
		return [col_list, value_list]

	def change_dic_to_list(self, input_dic, parent_key=[]):
		"""
		사전을 아래와같이 만들어 주는것
		[[['a', 'b', 'c'], 'value1'], [['a', 'b', 'd'], 'value2'], [['a', 'e', 'f'], 'value3']]

		:param d:
		:param parent_key:
		:return:
		"""
		result = []
		for k, v in input_dic.items():
			result.append([k, v])
		return result

	def change_dic_to_text_decoration(self, option_dic):
		"""
		모양을 나타내는 부분
		사전형태
		"""
		css = ""
		all_keys = list(option_dic.keys())
		if "size" in option_dic.keys():
			temp = self.check_pixel(option_dic["size"])
			css = css + "font-size: " + temp + ";"
		if "align" in all_keys: css = css + "font-align: " + option_dic["align"] + ";"
		if "bold" in all_keys: css = css + "font-weight:bold;"
		if "color" in all_keys: css = css + "color: " + option_dic["color"] + ";"
		if "collapse" in all_keys: css = css + "borser-collapse: " + option_dic["collapse"] + ";"
		if "background" in all_keys: css = css + "background-color: " + option_dic["background"] + ";"
		if "width" in all_keys: css = css + "width: " + self.check_pixel(option_dic["width"]) + ";"
		if "padding" in all_keys: css = css + "padding: " + option_dic["padding"] + ";"
		if "border" in all_keys: css = css + self._check_border_outline_data(option_dic["border"])
		return css

	def change_encoding_type_for_file(self, path, filename, original_type="EUC-KR", new_type="UTF-8", new_filename=""):
		"""
		텍스트가 안 읽혀져서 확인해보니 인코딩이 달라서 안되어져서
		이것으로 전체를 변경하기위해 만듦

		:param path:
		:param filename:
		:param original_type:
		:param new_type:
		:param new_filename:
		:return:
		"""
		full_path = path + "\\" + filename
		full_path_changed = path + "\\" + new_filename + filename
		try:
			aaa = open(full_path, 'rb')
			result = chardet.detect(aaa.read())
			# print(result['encoding'], filename)
			aaa.close()

			if result['encoding'] == original_type:
				# print("화일의 인코딩은 ======> {}, 화일이름은 {} 입니다".format(original_type, filename))
				aaa = open(full_path, "r", encoding=original_type)
				file_read = aaa.readlines()
				aaa.close()

				new_file = open(full_path_changed, mode='w', encoding=new_type)
				for one in file_read:
					new_file.write(one)
				new_file.close()
		except:
			print("화일이 읽히지 않아요=====>", filename)

		path = "C:\Python39-32\Lib\site-packages\myez_xl\myez_xl_test_codes"
		file_lists = os.listdir(path)
		for one_file in file_lists:
			self.change_encoding_type_for_file(path, one_file, "EUC-KR", "UTF-8", "_changed")

	def change_filename(self, old_path, new_path):
		"""
		화일이름 변경

		:param old_path:
		:param new_path:
		:return:
		"""
		old_path = self.check_file_path(old_path)
		new_path = self.check_file_path(new_path)
		os.rename(old_path, new_path)

	def change_float_to_formatted_text(self, input_value, big_digit, small_digit, fill_empty=" ", align="right", comma1000=True):
		"""
		f-string처럼 실수를 원하는 형태로 변경하는것

		:param input_value:
		:param big_digit:
		:param small_digit:
		:param fill_empty:
		:param align:
		:param comma1000:
		:return:
		"""
		if comma1000:
			changed_input_value = f"{round(float(input_value), small_digit):,}"
		else:
			changed_input_value = str(round(float(input_value), small_digit))

		repeat_no = big_digit - len(changed_input_value)

		repeat_char = fill_empty * (repeat_no)
		repeat_char_start = fill_empty * int(repeat_no / 2)
		repeat_char_end = fill_empty * int(repeat_no - int(repeat_no / 2))

		if align == "left":
			result = changed_input_value + repeat_char
		elif align == "right":
			result = repeat_char + changed_input_value
		elif align == "middle":
			result = repeat_char_start + changed_input_value + repeat_char_end
		else:
			result = repeat_char + changed_input_value
		return result

	def change_folder_name(self, old_path, new_path):
		"""
		폴더이름 변경

		:param old_path:
		:param new_path:
		:return:
		"""
		os.rename(old_path, new_path)

	def change_int_to_formatted_text(self, input_value, big_digit, fill_empty=" ", align="right", comma1000=True):
		"""
		f-string처럼 숫자를 원하는 형태로 변경하는것

		:param input_value:
		:param big_digit:
		:param fill_empty:
		:param align:
		:param comma1000:
		:return:
		"""

		if comma1000:
			changed_input_value = f"{input_value:,}"
		else:
			changed_input_value = str(input_value)

		repeat_no = big_digit - len(changed_input_value)

		repeat_char = fill_empty * (repeat_no)
		repeat_char_start = fill_empty * int(repeat_no / 2)
		repeat_char_end = fill_empty * int(repeat_no - int(repeat_no / 2))

		if align == "left":
			result = changed_input_value + repeat_char
		elif align == "right":
			result = repeat_char + changed_input_value
		elif align == "middle":
			result = repeat_char_start + changed_input_value + repeat_char_end
		else:
			result = repeat_char + changed_input_value
		return result

	def change_int_to_text_with_zerofill_style(self, input_num, total_len, fill_char="0"):
		"""
		정수를 자릿수를 맞추는 행위를 위해서 0을 앞에 추가하는것

		:param input_num:
		:param total_len:
		:param fill_char:
		:return:
		"""
		result = str(input_num).rjust(total_len, fill_char)
		return result

	def change_jamo_to_alpha(self, input_jamo_list):
		"""
		한글의 자음과 모음의 한글자를 알파벳으로 바꾸는것

		:param input_jamo_list:
		:return:
		"""
		result = ""
		for one_list in input_jamo_list:
			for jamo in one_list:
				eng_one = self.var["jamo_vs_eng"][jamo]
				result = result + eng_one
			result = result + "z"
		return result

	def change_jamo_to_korean(self, input_jamo_list):
		"""
		한글의 자음과 모음을 한글의 글자로 바꾸는것

		:param input_jamo_list:
		:return:
		"""
		result = ""
		for one_list in input_jamo_list:
			for jamo in one_list:
				eng_one = self.var["jamo_vs_eng"][jamo]
				result = result + eng_one
			result = result + "z"
		return result

	def change_jaum_to_xy_list_with_size(self, size=[1, 2], input_text="ㄱ"):
		"""
		자음을 넣고, 엑셀에 나타나는 xy사이즈를 계산하는것

		:param size:
		:param input_text:
		:return:
		"""
		x, y = size
		# x, y는 글자의 크기
		ja_01 = [["ㄱ"], [1, 1, 1, y], [1, y, x, y]]
		ja_02 = [["ㄴ"], [1, 1, x, 1], [x, 1, x, y]]
		ja_03 = [["ㄷ"], [1, y, 1, 1], [1, 1, x, 1], [x, 1, x, y]]
		ja_04 = [["ㄹ"], [1, 1, 1, y], [1, y, 0.5 * x, y], [0.5 * x, y, 0.5 * x, 1], [0.5 * x, 1, x, 1], [x, 1, x, y]]
		ja_05 = [["ㅁ"], [1, 1, 1, y], [1, y, x, y], [x, y, x, 1], [x, 1, 1, 1]]
		ja_06 = [["ㅂ"], [1, 1, x, 1], [x, 1, x, y], [x, y, 1, y], [0.5 * x, 1, 0.5 * x, y]]
		ja_07 = [["ㅅ"], [1, 0.5 * y, 0.3 * x, 0.5 * y], [0.3 * x, 0.5 * y, x, 1], [0.3 * x, 0.5 * y, x, y]]
		ja_08 = [["ㅇ"], [0.8 * x, 0.2 * y, 0.8 * x, 0.8 * y], [0.8 * x, 0.8 * y, 0.6 * x, y, ""],
				 [0.6 * x, y, 0.2 * x, y], [0.2 * x, y, 1, 0.8 * y, "/"], [1, 0.8 * y, 1, 0.2 * y],
				 [1, 0.2 * y, 0.2 * x, 1, ""], [0.2 * x, 1, 0.6 * x, 1], [0.6 * x, 1, 0.8 * x, 0.2 * y, "/"]]
		ja_09 = [["ㅈ"], [1, 1, 1, y], [1, 0.5 * y, 0.5 * x, 0.5 * y], [0.5 * x, 0.5 * y, x, 1, "/"],
				 [0.5 * x, 0.5 * y, x, y, ""]]
		ja_10 = [["ㅊ"], [0.2 * x, 0.5 * y, 1, 0.5 * y], [0.2 * x, 1, 0.2 * x, y], [0.2 * x, 0.5 * y, 0.4 * x, 0.5 * y],
				 [1, 0.5 * y, 0.5 * x, 0.5 * y], [0.5 * x, 0.5 * y, x, 1], [0.5 * x, 0.5 * y, x, y, ""]]
		ja_11 = [["ㅋ"], [1, 1, 1, y], [1, y, x, y], [0.5 * x, 1, 0.5 * x, y]]
		ja_12 = [["ㅌ"], [1, y, 1, 1], [1, 1, x, 1], [x, 1, x, y], [0.5 * x, 1, 0.5 * x, y]]
		ja_13 = [["ㅍ"], [1, 1, 1, y], [x, 1, x, y], [1, 0.2 * y, x, 0.2 * y], [1, 0.8 * y, x, 0.8 * y]]
		ja_14 = [["ㅎ"], [1, 0.5 * y, 0.2 * x, 0.5 * y], [0.2 * x, 1, 0.2 * x, y], [0.4 * x, 0.3 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, 0.6 * x, y], [0.6 * x, y, 0.8 * x, y], [0.8 * x, y, x, 0.8 * y],
				 [x, 0.8 * y, x, 0.3 * y], [x, 0.3 * y, 0.8 * x, 1], [0.8 * x, 1, 0.6 * x, 1],
				 [0.6 * x, 1, 0.4 * x, 0.3 * y]]
		ja_31 = [["ㄲ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], ]
		ja_32 = [["ㄸ"], [1, 1, 1, 0.4 * y], [1, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y],
				 [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], ]
		ja_33 = [["ㅃ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [x, 0.4 * y, 1, 0.4 * y], [0.5 * x, 1, 0.5 * x, 0.4 * y],
				 [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], [x, y, 1, y], [0.5 * x, 0.7 * y, 0.5 * x, y], ]
		ja_34 = [["ㅆ"], [1, 0.3 * y, 0.4 * x, 0.3 * y], [0.4 * x, 0.3 * y, x, 1], [0.4 * x, 0.3 * y, x, 0.5 * y],
				 [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_35 = [["ㅉ"], [1, 1, 1, 0.5 * y], [1, 0.3 * y, 0.4 * x, 0.3 * y], [0.4 * x, 0.3 * y, x, 1],
				 [0.4 * x, 0.3 * y, x, 0.5 * y], [1, 0.6 * y, 1, y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_36 = [["ㄳ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, x, 0.4 * y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_37 = [["ㄵ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.6 * y, 1, y], [1, 0.8 * y, 0.4 * x, 0.8 * y],
				 [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]
		ja_38 = [["ㄶ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [0.1 * x, 0.8 * y, 1, 0.8 * y],
				 [0.2 * x, 0.6 * y, 0.2 * x, y], [0.4 * x, 0.7 * y, 0.4 * x, 0.9 * y], [0.4 * x, 0.9 * y, 0.6 * x, y],
				 [0.6 * x, y, x, 0.9 * y], [x, 0.9 * y, x, 0.7 * y], [x, 0.7 * y, 0.8 * x, 0.6 * y],
				 [0.8 * x, 0.6 * y, 0.6 * x, 0.6 * y], [0.6 * x, 0.6 * y, 0.4 * x, 0.7 * y]]
		ja_39 = [["ㄺ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], ]
		ja_40 = [["ㄻ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, y, x, y], [x, y, x, 0.7 * y],
				 [x, 0.7 * y, 1, 0.7 * y], ]
		ja_41 = [["ㄼ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, x, 0.7 * y], [x, 0.7 * y, x, y], [x, y, 1, y],
				 [0.5 * x, 0.7 * y, 0.5 * x, y], ]
		ja_42 = [["ㄽ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y],
				 [0.4 * x, 0.8 * y, x, y], ]
		ja_43 = [["ㄾ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.7 * y, 1, y], [1, 0.7 * y, x, 0.7 * y],
				 [x, 0.7 * y, x, y], [0.5 * x, 0.7 * y, 0.5 * x, y], ]
		ja_44 = [["ㄿ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [1, 0.6 * y, 1, y], [x, 0.6 * y, x, y],
				 [1, 0.7 * y, x, 0.7 * y], [1, 0.9 * y, x, 0.9 * y], ]
		ja_45 = [["ㅀ"], [1, 1, 1, 0.4 * y], [1, 0.4 * y, 0.5 * x, 0.4 * y], [0.5 * x, 0.4 * y, 0.5 * x, 1],
				 [0.5 * x, 1, x, 1], [x, 1, x, 0.4 * y], [0.1 * x, 0.8 * y, 1, 0.8 * y], [0.2 * x, 0.6 * y, 0.2 * x, y],
				 [0.4 * x, 0.7 * y, 0.4 * x, 0.9 * y], [0.4 * x, 0.9 * y, 0.6 * x, y], [0.6 * x, y, x, 0.9 * y],
				 [x, 0.9 * y, x, 0.7 * y], [x, 0.7 * y, 0.8 * x, 0.6 * y], [0.8 * x, 0.6 * y, 0.6 * x, 0.6 * y],
				 [0.6 * x, 0.6 * y, 0.4 * x, 0.7 * y]]
		ja_46 = [["ㅄ"], [1, 1, x, 1], [x, 1, x, 0.4 * y], [x, 0.4 * y, 1, 0.4 * y], [0.5 * x, 1, 0.5 * x, 0.4 * y],
				 [1, 0.8 * y, 0.4 * x, 0.8 * y], [0.4 * x, 0.8 * y, x, 0.6 * y], [0.4 * x, 0.8 * y, x, y], ]

		jamo1_dic = {"ㄱ": ja_01, "ㄴ": ja_02, "ㄷ": ja_03, "ㄹ": ja_04, "ㅁ": ja_05,
					 "ㅂ": ja_06, "ㅅ": ja_07, "ㅇ": ja_08, "ㅈ": ja_09, "ㅊ": ja_10,
					 "ㅋ": ja_11, "ㅌ": ja_12, "ㅍ": ja_13, "ㅎ": ja_14,
					 "ㄲ": ja_31, "ㄸ": ja_32, "ㅃ": ja_33, "ㅆ": ja_34, "ㅉ": ja_35,
					 "ㄳ": ja_36, "ㄵ": ja_37, "ㄶ": ja_38, "ㄺ": ja_39, "ㄻ": ja_40,
					 "ㄼ": ja_41, "ㄽ": ja_42, "ㄾ": ja_43, "ㄿ": ja_44, "ㅀ": ja_45, "ㅄ": ja_46,
					 }

		result = jamo1_dic[input_text]
		return result

	def change_key_list_n_value_list_to_dic(self, key_list, value_list):
		"""
		두개의 리스트를 받으면 사전으로 만들어 주는 코드

		:param key_list:
		:param value_list:
		:return:
		"""
		result = dict(zip(key_list, value_list))
		return result

	def change_korean_to_alpha(self, input_han):
		"""
		한글을 자음과 모음으로 분리해서, 알파벳으로 변경하는 것

		:param input_han:
		:return:
		"""
		aa = self.change_korean_to_jamo(input_han)
		result = self.change_jamo_to_korean(aa)
		return result

	def change_korean_to_jamo(self, text):
		"""
		한글자의 한글을 자음과 모음으로 구분해 주는것

		:param text:
		:return:
		"""
		one_byte_data = text.encode("utf-8")
		print(one_byte_data)
		value_sum = 0
		char_type = ""

		if str(text) in "0123456789":
			char_type = "숫자"

		compile_1 = re.compile("\d+")
		no = compile_1.findall(text)

		try:
			no_1 = int(one_byte_data[0])
			no_2 = int(one_byte_data[1])
			no_3 = int(one_byte_data[2])
			new_no_1 = (no_1 - 234) * 64 * 64
			new_no_2 = (no_2 - 128) * 64
			new_no_3 = (no_3 - 128)
			value_sum = new_no_1 + new_no_2 + new_no_3

			if value_sum >= -28367 and value_sum <= -28338:
				char_type = "ja_only"
			if value_sum >= -28337 and value_sum <= -28317:
				char_type = "mo_only"

			print(chr(new_no_1), new_no_2, new_no_3)
		except:
			char_type = "no_han"
			# 이것은 영어나 숫자, 특수문자라는 뜻이다
			no_1 = one_byte_data
			no_2 = ""
			no_3 = ""

		return [char_type, text]

	def change_list_1d_to_dic(self, input_list_1d):
		"""
		1차원리스트 자료를 사전으로 만드는 것

		:param input_list_1d:
		:return:
		"""
		result = {}
		index = 0
		for one in input_list_1d:
			if not one in result.keys():
				result[one] = index
				index = index + 1
		return result

	def change_list_1d_to_dic_value_as_count_of_same_data(self, input_list):
		"""
		입력한 자료를 1차원자료로 간주하고, 값은 사전의 키로 만들어서 같은것이 잇으면 숫자를 증가시켜서 값을 만든다
		["1","2","2","3","4","4","4"] => {"1":1, "2":2, "3":1, "4":3}

		:param input_text:
		"""
		result = {}
		for one_letter in input_list:
			if one_letter in list(result.keys()):
				result[one_letter] = result[one_letter] + 1
			else:
				result[one_letter] = 1
		return result

	def change_list_1d_to_dic_with_serial_no(self, input_list_1d):
		"""
		1차원리스트자료를 넣으면, 값:번호 형식의 사전을 만들어주는것
		예 : ['가', '나', '다'] =>['가' :1, '나':2, '다':3]

		:param input_list_1d:
		:return:
		"""
		result = []
		for index, one in enumerate(input_list_1d):
			result[one] = index + 1
		return result

	def change_list_1d_to_list_2d(self, input_data):
		"""
		1차원리스트를 2차원으로 만들어 주는 것

		:param input_data:
		:return:
		"""
		result = self.change_list_1d_to_list_2d_as_yline_style(input_data)
		return result

	def change_list_1d_to_list_2d_as_yline_style(self, input_data):
		"""
		1차원의 리스트가 오면 2차원으로 만들어주는 것
		"""
		result = []
		if len(input_data) > 0:
			if type(input_data[0]) != type([]):
				for one in input_data:
					result.append([one, ])
		return result

	def change_list_1d_to_list_2d_by_step(self, input_list_1d, step_no):
		"""
		1차원으로 들어온 자료를 갯수에 맞도록  분리해서 2차원의 자료로 만들어 주는것

		:param input_list_1d:
		:param step_no:
		:return:
		"""
		result = []
		for partial_list in input_list_1d[::step_no]:
			result.append(partial_list)
		return result

	def change_list_1d_to_list_2d_group_by_step(self, input_list_1d, input_no):
		"""
		[1,2,3,4,5,6,7,8] =>[[1,2,3],[4,5,6],[7,8]]

		입력된 1차원 자료를 no갯수만큼씩 묶어서 2차원으로 만드는 것

		:param input_list_1d:
		:param input_no:
		:return:
		"""
		result = []
		if len(input_list_1d) <= input_no:
			result = [input_list_1d]
		else:
			mok, namuji = divmod(len(input_list_1d), input_no)
			for num in range(mok):
				result.append(input_list_1d[num * input_no:(num + 1) * input_no])
			if namuji:
				result.append(input_list_1d[-1 * namuji:])
		return result

	def change_list_1d_to_list_2d_group_by_total_len(self, input_list_1d, step_no):
		"""
		12개의 리스트를
		입력 - [ [1,2,3,4,5,6,7,8,9,10,11,12], 4]를 받으면 총 4개의 묶읆으로 순서를 섞어서 만들어 주는것 => [[1,5,9],  [2,6,10],  [3,7,11],  [4,8,12]] 로 만들어 주는것

		:param input_list_1d:
		:param step_no:
		:return:
		"""
		count_no = int(len(input_list_1d) / step_no)
		group_no = divmod(len(input_list_1d), int(step_no))[0]
		namuji = len(input_list_1d) - step_no * group_no
		result = []

		for no in range(count_no):
			temp = input_list_1d[no * count_no: no * count_no + count_no]
			result.append(temp)
		if namuji > 0:
			result.append(input_list_1d[-namuji:])
		return result

	def change_list_1d_to_text_with_chain_word(self, input_list_1d, chain_word=" ,"):
		"""
		리스트 자료들을 중간문자를 추가하여 하나의 문자열로 만드는 것,
		리스트 자료들을 중간에 문자를 추가하여 한줄의 문자로 만드는 것
		["aa", "bb","ccc"] => “aa, bbb, ccc”

		:param input_list_1d:
		:param chain_word:
		"""
		new_list = []
		for one in input_list_1d:
			new_list.append(str(one))

		result = chain_word.join(new_list)
		return result

	def change_list_2d_as_xy_to_yx(self, input_list_2d):
		"""
		입력자료의 xy를 yx로 바꿔서 입력하는 것

		:param input_list_2d:
		:return:
		"""
		result = []
		for y in range(len(input_list_2d[0])):
			temp = []
			for x in range(len(input_list_2d)):
				temp.append(input_list_2d[x][y])
			result.append(temp)
		return result

	def change_list_2d_n_first_line_to_dic(self, input_list_2d):
		"""
		2차원리스트의 1번째 요소를 키로해서, 사전형식의 자료로 만든것

		:param input_list_2d:
		:return:
		"""
		result = {}
		for one in input_list_2d[0]:
			result[one] = []
		for ix, list_1d in enumerate(input_list_2d[1:]):
			for index, one in enumerate(list_1d):
				short_title = input_list_2d[0][index]
				result[short_title].append(one)
		return result

	def change_list_2d_n_list_1d_to_dic(self, input_list_2d, title_list_1d):
		"""
		2차원리스트와 제목을 연결해서 사전을 만드는 것

		:param input_list_2d:
		:param title_list_1d:
		:return:
		"""
		result = []
		if len(input_list_2d[0]) == len(title_list_1d):
			# 입력하는 자료와 제목의 갯수가 같이야 하는것을 확인
			for one in input_list_2d:
				one_dic = {}
				for no in range(len(title_list_1d)):
					one_dic[title_list_1d[no]] = one[no]
				result.append(one_dic)
		else:
			result = False
		return result

	def change_list_2d_n_title_list_to_json_file(self, input_list_2d, title_list):
		"""
		엑셀자료를 json으로 만들기
		단, 엑셀자료의 첫줄은 제목이있어야한다. 만약, 없는 option을 선택하면 1번부터 숫자로 만들어 진다
		이 제목이 key로 사용된다

		결과 : [json화일, 제목리스트]

		:param sheet_name:
		:param xyxy:
		:param json_filename:
		:param no_title:
		:return:
		"""
		all_text = "[\n"
		for list_1d in input_list_2d:
			all_text = all_text + "{"
			for index, value in enumerate(list_1d):
				# 숫자인것은 '을 붙이지 않는다
				if type(value) == type(123) or type(value) == type(123.4):
					all_text = all_text + '"' + title_list[index] + '":' + str(value) + ", "
				else:
					key = str(title_list[index]).replace("'", "")
					value = str(value).replace("'", "")
					all_text = all_text + '"' + key + '": "' + value + '", '
			all_text = all_text[:-2] + "}," + " \n"
		all_text = all_text[:-3] + "]"
		return all_text

	def change_list_2d_n_titles_to_list_1dic(self, input_list_2d, title_list_1d):
		"""
		2차원리스트와 제목을 연결해서 사전을 만드는 것

		:param input_list_2d:
		:param title_list_1d:
		:return:
		"""
		result = self.change_list_2d_n_list_1d_to_dic(input_list_2d, title_list_1d)
		return result

	def change_list_2d_over_to_list_2d(self, input_list_2d_over):
		"""
		2 차원자료가 넘어가는것은 콤마(,)로 연결한 하나의 자료로 만드는 것
		2 차원의 자료중에서 정규표현식에서 여러 개를 찾은 경우에, 하나의 자료로 만들어 주는 기능

		:param input_list_2d_over:
		:return:
		"""
		for x, list_1d in enumerate(input_list_2d_over):
			for y, value in enumerate(list_1d):
				temp = ""
				if value and len(value) > 1:
					for one in value:
						temp = temp + str(one) + ","
					input_list_2d_over[x][y] = temp[:-1]

	def change_list_2d_to_differnet_xy_size(self, xy_list, resize=[1, 1]):
		"""
		리스트의 크기를 다시 설정하는 것
		메뉴에서 제외

		:param xy_list:
		:param resize:
		:return:
		"""
		result = []
		# 자료의 x갯수를 요청한것과 비교
		if len(xy_list) < resize[0] or resize[0] == 0:
			pass
		else:
			xy_list = xy_list[:resize[0]]
		# 자료의 y갯수를 요청한것과 비교
		for x_list in xy_list:
			if len(x_list) < resize[1] or resize[1] == 0:
				pass
			else:
				x_list = xy_list[:resize[0]]
			result.append(x_list)
		return result

	def change_list_2d_to_html_table(self, style, title_list, input_list_2d):
		"""
		2차원 자료를 html형식의 table로 마드는 것

		:param style:
		:param title_list:
		:param input_list_2d:
		:return:
		"""
		import pywintypes
		table_style_id = ""
		if style != "":
			table_style_id = " id=" + '""+style+'""
		table_html = "<table" + table_style_id + ">Wn"

		for one in title_list:
			table_html = table_html + f"<th> (one)</th>"
		for list_1d in input_list_2d:
			table_html = table_html + "<tr>"
			for value in list_1d:
				if value == None:
					value = ""
				if isinstance(value, pywintypes.TimeType):
					value = str(value)[:10]
				table_html = table_html + f"<td>(value)</td>"
			table_html = table_html + "</tr>"
		table_html = table_html + "</table>"

	def change_list_2d_to_list_1d(self, input_data):
		"""
		항목 : ['항목1', '기본값1', '설명', {'입력형태1':'설명1', '입력형태2':'설명1',.... }]
		결과 ['항목1', '기본값1', '설명', '입력형태1:설명1', '입력형태2:설명1',.... }]
		위 형태의 자료를 한줄로 만들기위해 자료를 변경한다

		:param input_data:
		:return:
		"""
		result = []
		for one_data in input_data:
			if type(one_data) == type({}):
				for key in list(one_data.Keys()):
					value = str(key) + " : " + str(one_data[key])
					result.append(value)
			elif type(one_data) == type(()) or type(one_data) == type([]) or type(one_data) == type(set()):
				for value in one_data:
					result.append(value)
			else:
				result.append(one_data)
		return result

	def change_list_2d_to_list_1d_group_by_no(self, input_list_2d, index_no=4):
		"""
		index번호를 기준으로 그룹화를 만드는 것

		:param input_list_2d:
		:param index_no:
		:return:
		"""
		result = []
		print(input_list_2d)
		sorted_input_list_2d = self.sort_list_2d_by_index(input_list_2d, index_no)
		print(sorted_input_list_2d)
		check_value = sorted_input_list_2d[0][index_no]
		temp = []
		for one_list in sorted_input_list_2d:
			if one_list[index_no] == check_value:
				temp.append(one_list)
			else:
				result.append(temp)
				temp = [one_list]
				check_value = one_list[index_no]
		if temp:
			result.append(temp)
		return result

	def change_list_2d_to_list_2d_as_same_len(self, input_list_2d="입력필요"):
		"""
		2차원 리스트의 최대 길이로 같게 만드는 것
		가끔 자료의 갯수가 달라서 생기는 문제가 발생할 가능성이 있는것을 맞추는것
		추가할때는 ""를 맞는갯수를 채워넣는다
		메뉴에서 제외

		:param input_list_2d: 2차원의 리스트형
		:return:
		"""
		input_text = None
		max_num = max(map(lambda x: len(x), input_list_2d))
		result = []
		for one in input_list_2d:
			one_len = len(one)
			if max_num == one_len:
				result.append(one)
			else:
				one.extend([input_text] * (max_num - one_len))
				result.append(one)
		return result

	def change_list_2d_to_list_2d_as_same_max_count_of_list_1d(self, input_data):
		# 가변적인 2차원배열을 같은 크기로 만들어 준다
		result = []
		max_len = max(len(row) for row in input_data)
		for list_x in input_data:
			temp = list_x
			for no in range(len(list_x), max_len):
				temp.append("")
			result.append(temp)
		return result

	def change_list_2d_to_set(self, input_list_2d):
		"""
		list_2d자료를 set형으로 바꾸는 것
		input_list = [["변경전자료1", "변경후자료2"], ["변경전자료11", "변경후자료22"], ]

		:param input_list_2d:
		:return:
		"""
		result = set()
		for list_1d in input_list_2d:
			for one in list_1d:
				if one != None and one != "":
					result.add(one)
		return result

	def change_list_2d_to_text(self, input_list_2d, input_len):
		"""
		2차원리스트의 자료들을 정렬해서 텍스트로 만드는 것

		:param input_list_2d: 2차원 형태의 리스트
		:param input_len:
		:return:
		"""
		result_text = ""
		result = []
		len_list = {}
		for index, one in enumerate(input_list_2d[0]):
			len_list[index] = 0

		for list_1d in input_list_2d:
			for index, one in enumerate(list_1d):
				len_list[index] = max(len(str(one)), len_list[index])

		for list_1d in input_list_2d:
			temp = ""
			for index, one in enumerate(list_1d):
				len_list[index] = max(len(str(one)), len_list[index])

		for list_1d in input_list_2d:
			temp = ""
			for index, one in enumerate(list_1d):
				temp = temp + self.make_text_basic(str(one), len_list[index] + input_len)
			result_text = result_text + temp + '\n'
		return result_text

	def change_list_2d_to_text_with_chain_word(self, input_list_2d, chain_word=""):
		"""
		2차원 리스트를 연결문자를 이용해서 만드는것

		:param input_list_2d:
		:param chain_word:
		:return:
		"""
		temp_text = ""
		for one_list in input_list_2d:
			for one_item in one_list:
				temp_text = temp_text + one_item + chain_word
		return temp_text

	def change_list_3d_to_list_1d_by_group_count(self, input_list_3d, index_no=4):
		"""
		index번호를 기준으로 그룹화를 만드는 것

		:param input_list_3d:
		:param index_no:
		:return:
		"""
		result = []
		for input_list_2d in input_list_3d:
			sorted_list_2d = self.sort_list_2d_by_index(input_list_2d, index_no)
			grouped_list_3d = self.change_list_2d_to_list_1d_group_by_no(sorted_list_2d, index_no)
			result = result + grouped_list_3d
		return result

	def change_list_to_padding_value(self, *input_list):
		"""
		보통 margin을 나타내는 속성은 [1 2 3 4]와같은 형태를 사용한다
		입력으로 들어오는 리스트를  => [top, right, bottom, left]로 바꿔주는 것이다

	   """
		result = ""
		if len(input_list) == 1:
			result = input_list[0] + " " + input_list[0] + " " + input_list[0] + " " + input_list[0]
		elif len(input_list) == 2:
			result = input_list[0] + " " + input_list[1] + " " + input_list[0] + " " + input_list[1]
		elif len(input_list) == 3:
			result = input_list[0] + input_list[1] + " " + input_list[2] + " " + input_list[1]
		elif len(input_list) == 4:
			result = input_list
		return result

	def change_mixed_list_to_list_2d_by_step(self, input_list="", xy=""):
		"""
		입력값이 1차원과 2차원의 자료가 섞여 있을때
		2차원의 자료형태로 모두 같은 크기로 만들어 주는것

		:param input_list:
		:param xy:
		:return:
		"""
		temp_result = []
		x_len, y_len = xy
		list1_max_len = len(input_list)
		list2_max_len = y_len
		count = int(list1_max_len / x_len)

		# 2차원자료중 가장 큰것을 계산한다
		for one_value in input_list:
			if type(one_value) == type([]):
				list2_max_len = max(list2_max_len, len(one_value))

		for one_value in input_list:
			temp_list = one_value
			# 모든 항목을 리스트형태로 만든다
			if type(one_value) != type([]):
				temp_list = [one_value]

			# 최대길이에 맞도록 적은것은 ""으로 갯수를 채운다
			if list2_max_len - len(temp_list) > 0:
				temp_list.extend([""] * (list2_max_len - len(temp_list)))
			temp_result.append(temp_list)

		result = []
		for no in range(count):
			start = no * x_len
			end = start + x_len
			result.append(temp_result[start:end])

		return result

	def change_n_digit_number_to_10digit_number(self, input_no, input_digit_number=10):
		"""
		입력형식의 값을 10진수값으로 변경하는것
		n진수 : n-digit-number

		:param input_no:
		:param input_digit_number:
		:return:
		"""
		original_letter = "0123456789abcdefghijklmnopqrstuvwxyz"
		base_letter = original_letter[0:input_digit_number]
		new_dic = {}
		for no, one_value in enumerate(base_letter):
			new_dic[one_value] = no
		total = 0
		checked_no = reversed(input_no)
		for no, one in enumerate(checked_no):
			total = total + len(base_letter) ** (no) * new_dic[one]
		return total

	def change_nth_depth_value_for_dic(self, i_dic, target_depth, i_key, i_value, current_depth=1):
		"""
		사전자료의 n번째 깊이의 값을 바꾸는 것


		:param i_dic:
		:param target_depth:
		:param i_key:
		:param i_value:
		:param current_depth:
		:return:
		"""
		if current_depth == target_depth + 1:
			for key in list(i_dic.keys()):
				if key == i_key:
					i_dic[key] = i_value
		else:
			for key, value in i_dic.items():
				if isinstance(value, dict):
					self.change_nth_depth_value_for_dic(value, target_depth, i_key, i_value, current_depth + 1)

	def change_num_to_char(self, input_data="입력필요"):
		"""
		숫자를 문자로 바꿔주는 것
		2 -> b

		:param input_data: 입력숫자
		"""
		re_com = re.compile(r"([0-9]+)")
		result_num = re_com.match(str(input_data))

		if result_num:
			base_num = int(input_data)
			result_01 = ''
			result = []
			while base_num > 0:
				div = base_num // 26
				mod = base_num % 26
				if mod == 0:
					mod = 26
					div = div - 1
				base_num = div
				result.append(mod)
			for one_data in result:
				result_01 = string.ascii_lowercase[one_data - 1] + result_01
			final_result = result_01
		else:
			final_result = input_data
		return final_result

	def change_num_to_formated_num_as_price_style(self, input_price):
		"""
		백만원단위, 천만원단위, 억단위로 구분

		:param input_price:
		"""
		input_price = int(input_price)
		if input_price > 100000000:
			result = str('{:.If}'.format(input_price / 100000000)) + "억원"
		elif input_price > 10000000:
			result = str('{: .0f}'.format(input_price / 1000000)) + "백만원"
		elif input_price > 1000000:
			result = str('{:.If}'.format(input_price / 1000000)) + "백만원"
		return result

	def change_num_to_num_with_1000comma(self, input_no):
		"""
		입력된 숫자를 1000단위로 콤마를 넣는것

		:param input_no:
		:return:
		"""
		temp = str(input_no).split(".")
		total_len = len(temp[0])
		result = ""
		for num in range(total_len):
			one_num = temp[0][- num - 1]
			if num % 3 == 2:
				result = "," + one_num + result
			else:
				result = one_num + result
		if len(temp) > 1:
			result = result + "." + str(temp[1])
		return result

	def change_num_to_roman_num(self, num):
		"""
		로마 숫자와 그에 대응하는 정수 값의 리스트

		:param num:
		:return:
		"""
		val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
		syb = ["M", "CM", "D", "CD"  "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
		i = 0
		roman_num = ""
		while num > 0:
			for _ in range(num // val[i]):
				roman_num += syb[i]
				num -= val[i]
				i += 1
		return roman_num

	def change_num_to_tel_style(self, input_value):
		"""
		전화번호나 핸드폰 번호 스타일을 바꿔주는것
		전화번호를 21345678 =>02-134-5678 로 변경하는 것

		:param input_value:
		:return:
		"""
		result = input_value
		value = str(int(input_value))
		if len(value) == 8 and value[0] == "2":
			# 22345678 => 02-234-5678
			result = "0" + value[0:1] + "-" + value[1:4] + "-" + value[4:]
		elif len(value) == 9:
			if value[0:2] == "2":
				# 223456789 => 02-2345-6789
				result = "0" + value[0:1] + "-" + value[1:5] + "-" + value[5:]
			elif value[0:2] == "11":
				# 113456789 => 011-345-6789
				result = "0" + value[0:2] + "-" + value[2:5] + "-" + value[5:]
			else:
				# 523456789 => 052-345-6789
				result = "0" + value[0:2] + "-" + value[2:5] + "-" + value[5:]
		elif len(value) == 10:
			# 5234567890 => 052-3456-7890
			# 1034567890 => 010-3456-7890
			result = "0" + value[0:2] + "-" + value[2:6] + "-" + value[6:]
		return result

	def change_one_korean_to_jamo(self, input_one_char):
		"""
		초성, 중성, 종성 리스트

		:param input_one_char:
		:return:
		"""
		choseong_list = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]  # 19 글자
		jungseong_list = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]  # 21 글자
		jongseong_list = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]  # 28 글자, 없는것 포함

		"""
		한글의 자음과 모음을 분리
		"""
		result = []
		one_byte_data = input_one_char.encode("utf-8")
		# print("one_byte_data", one_byte_data)
		new_no_1 = (int(one_byte_data[0]) - 234) * 64 * 64
		new_no_2 = (int(one_byte_data[1]) - 128) * 64
		new_no_3 = (int(one_byte_data[2]) - 128)
		# 유니코드의 번호로 바꾼다
		# 한글의 경우는 44032번째부터 순서대로 표시되어있다
		value = new_no_1 + new_no_2 + new_no_3 - 3072

		# print("value", value)
		chosung = choseong_list[divmod(value, 588)[0]]  # 초성
		joongsung = jungseong_list[divmod(divmod(value, 588)[1], 28)[0]]  # 중성
		jongsung = jongseong_list[divmod(divmod(value, 588)[1], 28)[1]]  # 종성
		result = [chosung, joongsung, jongsung]
		return result

	def change_python_file_to_sorted_by_def(self, filename):
		"""
			python으로만든 화일을 읽어서 def를 기준으로 정렬해서 돌려주는 것
			1. 프린트해서 나타냄
			2. 화일로 정렬된것을 만듦
			3. 리스트형태로 돌려주는것
			"""
		file_pointer = open(filename, 'r', encoding='utf-8')  # 텍스트 읽어오기
		file_list = file_pointer.readlines()  # 한번에 다 읽기

		all_text = ""
		temp = []
		result = {}
		title = "000"
		for one_line_text in file_list:
			# def로 시작이 되는지 알아 내는것
			if str(one_line_text).strip()[0:3] == "def" and str(one_line_text).strip()[-1] == ":":
				result[title] = temp  # def나오기 전까지의 자료를 저장합니다
				temp = []
				title = str(one_line_text).strip()  # 사전의 key를 def의 이름으로 만드는 것이다
			temp.append(one_line_text)
		result[title] = temp

		#sorted_keys = list(result.keys())
		#sorted_keys.sort()  # key인 제목을 기준으로 정렬을 하도록 만든것
		#write_file = open("output_output_33.txt", 'w', encoding='utf-8')  # 텍스트 읽어오기

		#for one_key in sorted_keys:
		#	for one_line in result[one_key]:
		#		one_line = one_line.replace("\n", "")
		#		print(one_line)  # 별도로 화일로 만들지 않고, 터미널에 나타나는것을 복사해서 사용하는 방법으로 만듦
		#		all_text = all_text + one_line
		#		write_file.write(one_line + "\n")
		#write_file.close()
		return result


	def change_re_group_by_step(self, all_data, initial_group, step):
		"""
		기존에 그룹화되어있는것을 기준으로, 최대갯수가 step의 갯수만큼 되도록 다시 그룹화 하는것이다

		:param all_data:
		:param initial_group:
		:param step:
		:return:
		"""
		result = []
		for list_1d in initial_group:
			if len(list_1d) > step:
				repeat_no = int((len(list_1d) + step - 1) / step)
				for no in range(repeat_no - 1):
					result.append(list_1d[no * step:(no + 1) * step])
				result.append(list_1d[(repeat_no - 1) * step:])
			else:
				result.append(list_1d)

		remain_all_data = all_data
		for list_1d in initial_group:
			for one_value in list_1d:
				remain_all_data.remove(one_value)
		result.append(remain_all_data)
		return result

	def change_size_for_list_2d(self, input_list_2d, x_start, y_start, x_len, y_len):
		"""
		2차원 리스트의 사이즈를 변경하는 것
		2차원안의 1차원자료를 몇개씩 줄여서 새롭게 2차원자료를 만드는 것이다

		:param input_list_2d:
		:param x_start:
		:param y_start:
		:param x_len:
		:param y_len:
		:return:
		"""
		result = []
		if len(input_list_2d) >= x_start + x_len and len(input_list_2d[0]) >= y_start + y_len:
			changed_list_2d = input_list_2d[x_start:x_start + x_len - 1]
			for list_1d in changed_list_2d:
				result.append(list_1d[y_start:y_start + y_len - 1])
		return result

	def change_text_repeater_to_css_repeater(self, input_text):
		"""
		[3, "2n+1", "nth-child(3)","nth-child(3~5)", "t(2n+1)", "c(2n+1)"]
		위와같은 형태로 입력을 하면, css에서 사용가능한 공식적인 형태로 변경을 해주는 것이다
		3 : 3번째것만 적용
		2n+1 : 1번에서부터 시작하며, 매 2번째마다
		nth-child(3) : 3번째것
		nth-child(3~5) : 3~5번째것
		t(2n+1) : 테이블에대한것으로, 1번에서부터 시작하며, 매 2번째마다 가로줄을
		c(2n+1) : 테이블에대한것으로, 1번에서부터 시작하며, 매 2번째마다 세로줄을
		"""
		result = ""
		input_text = str(input_text)
		# "nth-child(3~5)"
		if "(" in input_text and "~" in input_text:
			head, num = input_text.split("(")
			head, num = head[:-1], num[:-1]
			start, end = str(num).split("~")

			temp1 = self.check_text_repeater_option("+" + str(start))
			temp2 = self.check_text_repeater_option("-" + str(end))
			if input_text.startswith("nth-child") or input_text.startswith("c"):
				result = "nth-child(" + temp1 + "):" + "nth-child(" + temp2 + ")"
			elif input_text.startswith("nth-of-type") or input_text.startswith("t"):
				result = "nth-of-type(" + temp1 + "):" + "nth-of-type(" + temp2 + ")"

		# ["nth-child(3)", "t(2n+1)", "c(2n+1)"]
		elif "(" in input_text and not "~" in input_text:
			head, num = input_text.split("(")
			num = num[:-1]

			try:
				start = int(num)
				if start == 0:
					result = "first-child"
				elif start == -1:
					result = "last-child"
				elif start < -1:
					result = "nth-last-child(" + str(int(start * -1)) + ")"
				elif start > 0:
					if input_text.startswith("nth-child") or input_text.startswith("c"):
						result = "nth-child(" + num + ")"
					elif str(input_text).startswith("nth-of-type") or input_text.startswith("t"):
						result = "nth-of-type(" + num + ")"

			except:
				if input_text.startswith("only-child"):
					result = "only-child"
				elif input_text.startswith("empty"):
					result = "empty"
				elif input_text.startswith("nth-child") or input_text.startswith("c"):
					result = "nth-child(" + num + ")"
				elif str(input_text).startswith("nth-of-type") or input_text.startswith("t"):
					result = "nth-of-type(" + num + ")"

		# [3, "2n+1"]
		elif not "(" in input_text and not "~" in input_text:
			result = "nth-child(" + input_text + ")"
		return result

	def change_text_to_binary_list(self, st):
		"""
		문자열을 바이너리 리스트로 만드는것

		:param st:
		:return:
		"""
		result = [bin(ord(i))[2:].zfill(8) for i in st]
		return result

	def change_text_to_list_1d_by_step(self, input_data, input_list):
		"""
		입력문자를 숫자만큼씨 짤라서 리스트로 만드는 것

		:param input_data:
		:param input_list:
		:return:
		"""
		result = []
		total_len = 0
		start_no = 0
		for no in range(len(input_list)):
			if no != 0:
				start_no = total_len
			end_len = input_list[no]
			result.append(input_data[start_no:start_no + end_len])
			total_len = total_len + end_len
		return result

	def change_text_to_text_by_fstring_format(self, input_value, big_digit, fill_empty=" ", align="right"):
		"""
		f-string처럼 문자를 원하는 형태로 변경하는것

		:param input_value:
		:param big_digit:
		:param fill_empty:
		:param align:
		:return:
		"""
		changed_input_value = str(input_value)
		repeat_no = big_digit - len(changed_input_value)

		repeat_char = fill_empty * (repeat_no)
		repeat_char_start = fill_empty * int(repeat_no / 2)
		repeat_char_end = fill_empty * int(repeat_no - int(repeat_no / 2))

		if align == "left":
			result = changed_input_value + repeat_char
		elif align == "right":
			result = repeat_char + changed_input_value
		elif align == "middle":
			result = repeat_char_start + changed_input_value + repeat_char_end
		else:
			result = repeat_char + changed_input_value
		return result

	def change_tuple_2d_to_list_2d(self, input_tuple_2d):
		"""
		2차원의 듀플을 2차원 리스트로 만드는 것

		:param sheet_name: 시트이름 (""은 활성화된 시트이름을 뜻함)
		:param xyxy: [1,1,2,2], 가로세로셀영역 (""은 현재 선택영역을 뜻함)
		:return:
		"""
		result = []
		for x in range(len(input_tuple_2d)):
			temp = []
			for y in range(len(input_tuple_2d[0])):
				value = input_tuple_2d[x][y]
				if value:
					pass
				else:
					value = ""
				temp.append(value)
			result.append(temp)
		return result

	def change_tuple_to_list(self, input_data):
		"""
		듀플을 리스트로 변경하는 것

		:param input_data:
		:return:
		"""
		if isinstance(input_data, (list, tuple)):
			return [self.change_tuple_to_list(x) for x in input_data]
		elif isinstance(input_data, set):
			return set(self.change_tuple_to_list(x) for x in input_data)
		else:
			return input_data

	def change_tuple_to_list_2d(self, input_tuple_2d):
		"""
		튜플의 2차원자료를 리스트 2차로 만드는 것

		:param input_tuple_2d:
		:return:
		"""
		list_2d = list(input_tuple_2d)
		for x in range(len(list_2d)):
			list_2d[x] = list(list_2d[x])
		return list_2d

	def change_two_list_1d_to_list_2d_group_by_same_xy_data(self, input_list_1, input_list_2):
		"""
		두개의 리스트를 서로 묶어서, 새로운 리스트를 만드는 것
		[1,2,3], ["a","b","c"] ==> [[1, "a"],[2,"b"],[3,"c"]]

		:param input_list_1:
		:param input_list_2:
		:return:
		"""
		result = []
		for x, y in zip(input_list_1, input_list_2):
			result.append(x + y)
		return result

	def change_two_list_2d_to_one_list_2d_with_same_len(self, input_list_2d_1, input_list_2d_2):
		"""
		선택한 영역이 2개를 서로 같은것을 기준으로 묶을려고하는것이다
		제일앞의 한줄이 같은것이다
		만약 묶을려고 할때 자료가 없을때는 그 기준자료만큼 빈자료를 넣어서 다음자료를 추가하는 것이다

		:param input_list_2d_1:
		:param input_list_2d_2:
		:return:
		"""
		no_of_list_2d_1 = len(input_list_2d_1[0]) - 1
		no_of_list_2d_2 = len(input_list_2d_2[0]) - 1
		empty_list_2d_1 = [""] * no_of_list_2d_1
		empty_list_2d_2 = [""] * no_of_list_2d_2
		# 리스트형태로는 코드가 더 길어질것으로 보여서 입력자료를 사전으로 변경 한것
		temp_dic = {}
		for one in input_list_2d_1:
			temp_dic[one[0]] = one[1:]
		checked_list = []
		# 기준이 되는 자료에 항목이 있을때
		for one in input_list_2d_2:
			if one[0] in temp_dic.keys():
				temp_dic[one[0]] = list(temp_dic[one[0]]) + list(one[1:])
			else:
				temp_dic[one[0]] = empty_list_2d_1 + list(one[1:])
			checked_list.append(one[0])
		# 기준자료에 항목이 없는것에 대한것
		for one in temp_dic.keys():
			if not one in checked_list:
				temp_dic[one] = list(temp_dic[one]) + empty_list_2d_2
		# 사전형식을 리스트로 다시 만드는것
		result = []
		for one in temp_dic:
			result.append([one] + list(temp_dic[one]))
		return result

	def change_two_list_to_dic(self, key_list, value_list):
		# 두개의 리스트를 받으면 사전으로 만들어 주는 코드
		result = dict(zip(key_list, value_list))
		return result

	def change_waste_data(self, original_data):
		"""
		숫자와 문자만 남기는것
		보통 데이터베이스의 컬럼명을 사용할때, 문제가 안생기도록 하기위하여 적용하는 것이다
		"""
		result = []
		for one_data in original_data:
			temp = ""
			for one in one_data:
				if str(one) in ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
					temp = temp + str(one)
			result.append(temp)
		return result

	def change_xylist_to_yxlist(self, input_list_2d="입력필요"):
		"""
		trans_list( input_list_2d="입력필요")
		2차원자료를 행과열을 바꿔서 만드는것
		단, 길이가 같아야 한다

		:param input_list_2d: 2차원 형태의 리스트
		:return:
		"""
		checked_list_2d = self.change_list_2d_to_list_2d_as_same_len(input_list_2d)
		result = [list(x) for x in zip(*checked_list_2d)]
		return result

	def check_data_type_for_data(self, input_data):
		"""
		입력된 자료형을 확인하는것

		:param input_data: 입력자료
		"""
		if input_data == None or input_data == [] or input_data == ():
			result = "none"

		elif type(input_data) == type([]):
			if type(input_data[0]) == type([]):
				# 2차원의 자료이므로 입력값 그대로를 돌려준다
				result = "list_2d_list"
			elif type(input_data[0]) == type(()):
				result = "list_tuple"
			else:
				result = "list_1d"
		elif type(input_data) == type(()):
			if type(input_data[0]) == type([]):
				# 2차원의 자료이므로 입력값 그대로를 돌려준다
				result = "tuple_list"
			elif type(input_data[0]) == type(()):
				result = "tuple_tuple"
			else:
				result = "tuple1d"
		elif type(input_data) == type(123):
			result = "int"
		elif type(input_data) == type("123"):
			result = "string"
		return result

	def check_data_types_for_list_2d(self, input_list_2d):
		return self.filter_list_2d_for_int_n_str(input_list_2d)

	def check_file_path(self, file):
		"""
		입력자료가 폴더를 갖고있지 않으면 현재 폴더를 포함해서 돌려준다

		:param file:
		:return:
		"""
		if len(file.split(".")) > 1:
			result = file
		else:
			cur_dir = self.get_current_path()
			result = cur_dir + "\\" + file
		return result

	def check_font_data(self, input_list):
		result = {}
		for value in input_list:
			if type(value) == type(123):
				result["size"] = value
			elif value in ["bold", "진하게"]:
				result["bold"] = True
			elif value in ["밑줄", "underline"]:
				result["underline"] = True
			elif value in ["italic", "이탈릭채", "기울게", "이탈릭"]:
				result["italic"] = True
			else:
				try:
					rgbint = self.xcolor.change_scolor_to_rgbint(value)
					result["color"] = rgbint
				except:
					pass
		return result

	def check_josa(self, front_word, input_josa):
		"""
		끝글자가 모음일때와 자음일때를 구별해서 사용
		앞의 글자에 따라서 맞는 조사를 선택하는 것

		:param front_word:
		:param input_josa:
		:return:
		"""
		result = False
		base_word_set = [["은", "는"], ["이", "가"], ["을", "를"], ["과", "와"], ["으로", "로"]]
		moum_tf = 0
		one_char = str(front_word).strip([-1])
		temp = self.xre.is_match("[한글:1~]", one_char)
		if temp:
			aaa = self.change_one_korean_to_jamo(one_char)
			if aaa[0][2]:
				moum_tf = 1
			for list_1d in base_word_set:
				if input_josa in list_1d:
					result = list_1d[moum_tf]
					break
		else:
			result = False
		return result


	def check_list_1d(self, input_data):
		"""
		입력으로 드러온자료가 리스트인지를 확인하는것
		만약 아니면, 1차원리스트로 만들어주는것

		:param input_data:
		:return:
		"""
		if type(input_data) == type([]):
			result = input_data
		else:
			result = [input_data]
		return result

	def check_list_as_col_name(self, input_list):
		"""
		입력형태 : 제목리스트, 2차원 값리스트형
		출력형태 : dataframe로 바꾼것

		:param input_list:
		:return:
		"""
		result = []
		if input_list == "":
			if type(input_list[0]) != type([]):
				for one in input_list:
					result.append([one, ])
		return result

	def check_min_result(self, input_dic, except_key=[]):
		"""
		갯수가 제일 적은 것을 찾는 것
		입력된 사전을 기준으로 사전의 키가 except_key는 제외하고,
		사전의 value에서 가장 작은 갯수의 key를 찾는 것이다

		:param input_dic:
		:param except_key:
		:return:
		"""
		selected_key = ""
		temp_count = 999
		for key_value in input_dic.keys():
			if not key_value in except_key:
				if len(input_dic[key_value]) < temp_count:
					temp_count = len(input_dic[key_value])
					selected_key = key_value
		return selected_key

	def check_one_address(self, input_text=""):
		"""
		입력된 1개의 주소를 문자인지, 숫자인지
		숫자로 변경하는 것이다

		:param input_text: 입력 text
		"""
		re_com_1 = re.compile("^[a-zA-Z]+$")  # 처음부터 끝가지 알파벳일때
		result_str = re_com_1.findall(str(input_text))

		re_com_2 = re.compile("^[0-9]+$")  # 처음부터 끝가지 숫자일때
		result_num = re_com_2.findall(str(input_text))

		if result_num == [] and result_str != []:
			address_type = "string"
			no = 0
			address_int = 0
			for one in input_text.lower()[::-1]:
				num = string.ascii_lowercase.index(one) + 1
				address_int = address_int + 26 ** no * num
				no = no + 1
		elif result_str == [] and result_num != []:
			address_type = "num"
			address_int = int(input_text)
		else:
			address_int = "error"
			address_type = "error"
		return [address_int, address_type, input_text]

	def check_pixel(self, input_value):
		"""
		px단위가 없는것은 집어 넣는 것이다
		"""
		if type(input_value) == type(123):
			result = str(input_value) + "px"
		elif type(input_value) == type("abc") and input_value.endswith("px"):
			result = input_value
		else:
			result = str(input_value) + "px"
		return result

	def check_range_for_df(self, input_df):
		"""


		:param input_df:
		:return:
		"""
		self.manual["clipboard_paste"] = {
			"분류1": "pandas, dataframe",
			"설명": "df에 들어가는 입력값을 확인하는 것",
			"입력요소": "input_df(dataframe)",
			"기타설명": "내부적으로 사용하는것"
		}
		temp = []
		for one in input_df:
			if ":" in one:
				pass
			elif "~" in one:
				one = one.replace("~", ":")
			elif "all" in one:
				one = one.replace("all", ":")
			else:
				changed_one = one.split(",")
				temp_1 = []
				for item in changed_one:
					temp_1.append(int(item))
				one = temp_1
			temp.append(one)
		return temp

	def check_same_position(self, input_list_2d, list_1d):
		"""
		여러 엑셀의 자료에서 같은 부분을 찾기위해 만든 것이다
		같은 형태를 가진 엑셀화일들을 더하기 위해서는 같은 사이즈를 가져야 하는데, 어떤 경우들은
		사용하다가 틀려지는 부분들이 잇어서, 이것을 확인하기 위해서 만든 것이다

		들어온 자료중에서, 처음으로 list_1d와같은 위치를 돌려준다

		:param input_list_2d: 보통 used_range의 자료를 갖고 옮
		:param list_1d: 제일 처음의 몇개의 자료 ["","제목"]
		:return:
		"""
		result = ""
		repeat_no = len(input_list_2d[0]) - len(list_1d) + 1
		x = -1
		for list_1d in input_list_2d:
			x = x + 1
			y = -1
			for no in range(repeat_no):
				y = y + 1
				if list_1d[no:no + len(list_1d)] == list_1d:
					return [x, y]
		return result

	def check_selector_basic(self, input_list_1d):
		"""
		*** 사용되지 않음

		제일 앞의것을 리스트형태로 변경
		"""
		if type(input_list_1d) != type([]):
			input_list_1d = [input_list_1d]

		# print(input_list_1d)
		result = ""

		for one in input_list_1d:
			one = str(one).strip()
			if one in ["전체", "all", "*"]:
				result = result + "*" + " "
			elif one.startswith("class"):
				front, end = one.split("(")
				result = result + "." + end[:-1] + " "
			elif one.startswith("id"):
				front, end = one.split("(")
				result = result + "#" + end[:-1] + " "
			elif one.startswith("tag"):
				# tag(p), tag(p, class(aaa)), class(aaa)
				front, end = one.split("(")
				result = result + end[:-1] + " "
			else:
				result = result + one + " "
		result = result[:-1]
		return result

	def check_start_with_list(self, base_data, input_list):
		result = True
		for one in input_list:
			if base_data.startswith(one):
				result = False
				break
		return result

	def check_text_encoding_data(self, text, encoding_type):
		"""
		입력자료의 인코딩을 확인하는 것

		:param text:
		:param encoding_type:
		:return:
		"""
		byte_data = text.encode(encoding_type)
		hex_data_as_str = " ".os.path.join("{0}".format(hex(c)) for c in byte_data)
		int_data_as_str = " ".os.path.join("{0}".format(int(c)) for c in byte_data)

		print("\"" + text + "\" 전체 문자 길이: {0}".format(len(text)))
		print("\"" + text + "\" 전체 문자를 표현하는 데 사용한 바이트 수: {0} 바이트".format(len(byte_data)))
		print("\"" + text + "\" 16진수 값: {0}".format(hex_data_as_str))
		print("\"" + text + "\" 10진수 값: {0}".format(int_data_as_str))
		# 사용법 : text_encoding_data("Hello", "utf-8")
		return int_data_as_str

	def check_text_outline(self, input_text):
		"""
		글자의 외곽선을 그리기
		입력으로 들어온 텍스트를 분리 => 3가지 종류로 확인 => 다시 올바른 text로 만듦
		temp = ["1", "solid", "; "]
		"""
		temp = [" ", " ", "; "]

		input_list = input_text.split()
		input_list_1 = list(input_list)
		for one in input_list:
			aaa = self.xre.search_all_by_jf_sql("[숫자:1~][단어(px):0~1]", one)
			if aaa:
				temp[0] = aaa[0][0]
				input_list_1.remove(one)

			if one in self.vars["line_style_dic"].keys():
				temp[1] = self.vars["line_style_dic"][one]
				input_list_1.remove(one)

		if input_list_1:
			temp[2] = input_list_1[0] + "; "

		result = self.change_list_1d_to_text_with_chain_word(temp, " ")
		return result

	def check_text_repeater_option(self, input_text):
		"""

		"""
		is_num = self.xre.is_number_only(input_text)

		if is_num:
			result = input_text
		elif input_text == "even":
			result = "2n"
		elif input_text == "odd":
			result = "2n+1"
		elif input_text.startswith("+"):
			result = "n+" + input_text[1:]
		elif input_text.startswith("-"):
			result = "-n+" + input_text[1:]
		elif "n" in input_text:
			result = input_text
		else:
			result = False
		return result

	def check_title_or_col_name(self, temp_title):
		"""
		각 제목으로 들어가는 글자에 대해서 변경해야 하는것을 변경하는 것이다
		입력형태 :
		출력형태 :
		"""
		for temp_01 in [[" ", "_"], ["(", "_"], [")", "_"], ["/", "_per_"], ["%", ""], ["'", ""], ['"', ""], ["$", ""],
						["__", "_"], ["__", "_"], ["\\", ""], [".", ""]]:
			temp_title = temp_title.replace(temp_01[0], temp_01[1])
		if temp_title[-1] == "_": temp_title = temp_title[:-2]
		return temp_title

	def check_unique_y_in_list_1d(self, data1, data2):
		"""
		고유한 컬럼만 골라낸다
		"""
		result = []
		columns = self.read_y_names(data1)
		update_data2 = self.change_waste_data(data2)
		for temp_3 in update_data2:
			if not temp_3.lower() in columns:
				result.append(temp_3)
		return result

	def chenge_text_id_to_css_id(self, input_text):
		"""
		id(아이디번호) => #아이디번호
		위와같이 바꿔주는것, 여러개가 있으면 여러개를 바꿔줌
		"""
		searched_list = self.xre.search_all_by_jf_sql("id\([영어&,_&공백:1~]\)", input_text)
		if searched_list:
			found_text = searched_list[0][0][3:-1]
			temp = self.xre.replace_with_jf_sql("[,&공백:1~]", ", .", found_text)
			temp1 = "#" + temp
			result = input_text.replace(input_text[searched_list[0][1]:searched_list[0][2]], temp1)
		else:
			result = input_text
		return result

	def chenge_text_selector_to_css_selector(self, input_text=""):
		"""
		class(클래스이름) => .클래스이름
		위와같이 바꿔주는것, 여러개가 있으면 여러개를 바꿔줌
		"""
		searched_list = self.xre.search_all_by_jf_sql("class\([영어&,_&공백:1~]\)", input_text)
		if searched_list:
			found_text = searched_list[0][0][6:-1]
			temp = self.xre.replace_with_jf_sql("[,&공백:1~]", ", .", found_text)
			temp1 = "." + temp
			temp2 = input_text.replace(input_text[searched_list[0][1]:searched_list[0][2]], temp1)
			result = self.chenge_text_id_to_css_id(temp2)
		else:
			result = input_text
		return result

	def combine_two_list_1d_as_list_2d_group_by_same_xy_data(self, input_list_1, input_list_2):
		"""
		두개의 리스트를 서로 묶어서, 새로운 리스트를 만드는 것
		[1,2,3], ["a","b","c"] ==> [[1, "a"],[2,"b"],[3,"c"]]

		:param input_list_1:
		:param input_list_2:
		:return:
		"""
		result = []
		for x, y in zip(input_list_1, input_list_2):
			result.append(x + y)
		return result

	def combine_two_list_1d_as_list_2dn(self, input_list_2d_1, input_list_2d_2):
		"""
		선택한 영역이 2개를 서로 같은것을 기준으로 묶을려고하는것이다
		제일앞의 한줄이 같은것이다
		만약 묶을려고 할때 자료가 없을때는 그 기준자료만큼 빈자료를 넣어서 다음자료를 추가하는 것이다

		:param input_list_2d_1:
		:param input_list_2d_2:
		:return:
		"""
		no_of_list_2d_1 = len(input_list_2d_1[0]) - 1
		no_of_list_2d_2 = len(input_list_2d_2[0]) - 1
		empty_list_2d_1 = [""] * no_of_list_2d_1
		empty_list_2d_2 = [""] * no_of_list_2d_2
		# 리스트형태로는 코드가 더 길어질것으로 보여서 입력자료를 사전으로 변경 한것
		temp_dic = {}
		for one in input_list_2d_1:
			temp_dic[one[0]] = one[1:]
		checked_list = []
		# 기준이 되는 자료에 항목이 있을때
		for one in input_list_2d_2:
			if one[0] in temp_dic.keys():
				temp_dic[one[0]] = list(temp_dic[one[0]]) + list(one[1:])
			else:
				temp_dic[one[0]] = empty_list_2d_1 + list(one[1:])
			checked_list.append(one[0])
		# 기준자료에 항목이 없는것에 대한것
		for one in temp_dic.keys():
			if not one in checked_list:
				temp_dic[one] = list(temp_dic[one]) + empty_list_2d_2
		# 사전형식을 리스트로 다시 만드는것
		result = []
		for one in temp_dic:
			result.append([one] + list(temp_dic[one]))
		return result

	def compare_two_value_in_list(self, raw_data, req_num, project_name, vendor_name, nal):
		"""
		위아래 비교
		회사에서 사용하는 inq용 화일은 두줄로 구성이 된다
		한줄은 client가 요청한 스팩이며
		나머지 한줄은 vendor가 deviation사항으로 만든 스팩이다
		이두가지의 스팩을 하나로 만드는 것이다
		즉, 두줄에서 아래의 글씨가 있고 그것이 0, None가 아니면 위의것과 치환되는 것이다
		그런후 이위의 자료들만 따로 모아서 돌려주는 것이다
		"""
		self.data = list(raw_data)
		self.data_set = []
		self.data_set_final = []

		for a in range(0, len(self.data), 2):
			for b in range(len(self.data[1])):
				if not (self.data[a + 1][b] == self.data[a][b]) and self.data[a + 1][
					b] != None and self.data[a + 1][b] != 0:
					self.data_set.append(self.data[a + 1][b])
				else:
					self.data_set.append(self.data[a][b])
			self.data_set.append(req_num)
			self.data_set.append(project_name)
			self.data_set.append(vendor_name)
			self.data_set.append(nal)
			self.data_set_final.append(self.data_set)
			self.data_set = []
		return self.data_set_final

	def concate_jfinder_result(self, input_list_2d, chain_word=": "):
		"""
		jfinder에서 찾은 여러개의 자료를 하나의 텍스트로 만들어서 연결하는것
		jfinder에서 찾은 여러개의 자료 : [[찾은글자, 찾은 시작 위치, 끝위치 번호, [그룹1, 그룹2], ....]

		2차원자료로 오는것을 연결되는 문자로 연결해 주는것

		:param input_list_2d:
		:param chain_word:
		:return:
		"""
		result = ""
		if input_list_2d:  # 1
			for list_1d in input_list_2d:
				result = result + list_1d[0] + chain_word
			result = result[:-1 * len(chain_word)]
		return result

	def copy_file(self, old_path, new_path, meta=""):
		"""
		화일복사

		:param old_path:
		:param new_path:
		:param meta:
		:return:
		"""
		old_path = self.check_file_path(old_path)
		new_path = self.check_file_path(new_path)
		if meta == "":
			shutil.copy(old_path, new_path)
		else:
			shutil.copy2(old_path, new_path)

	def copy_file_with_meta(self, old_path, new_path):
		"""
		화일복사

		:param old_path:
		:param new_path:
		:return:
		"""
		old_path = self.check_file_path(old_path)
		new_path = self.check_file_path(new_path)
		shutil.copy2(old_path, new_path)

	def copy_folder(self, old_path, new_path):
		"""
		폴더복사

		:param old_path:
		:param new_path:
		:return:
		"""
		shutil.copytree(old_path, new_path)

	def copy_to_clipboard(self, input_text):
		"""

		:param input_text:
		:return:
		"""
		pyperclip.copy(input_text)

	def count_all_value_element_for_dic(self, input_dic):
		"""
		dic안의 value들의 전체 갯수를 계산해서 돌려주는 것

		:param input_dic:
		:return:
		"""
		result = 0
		for one in input_dic.keys():
			result = result + len(input_dic[one])
		return result

	def count_element_for_list_2d(self, input_list_2d):
		"""
		1차원이나 2차원의 리스트가 들어오면,
		값들이 몇번 나왔는지를 계산하는것

		:param input_list_2d:
		:return:
		"""

		result = {}
		if type(input_list_2d[0]) != type([]) and type(input_list_2d[0]) != type(()):
			input_list_2d = [input_list_2d]
		for x in range(len(input_list_2d)):
			for y in range(len(input_list_2d[x])):
				one_value = input_list_2d[x][y]
				if one_value == "" or one_value == None:
					pass
				else:
					if one_value in list(result.keys()):
						result[one_value] = result[one_value] + 1
					else:
						result[one_value] = 1
		return result

	def count_function_num_in_python_file(self, python_file_list, path=""):
		"""
			원하는 python화일안에 몇개의 def로 정의된 메소드가 있는지 확인하는 것이다

			:param python_file_list:
			:param path:
			:return:
			"""
		result = []
		num = 0
		for one in python_file_list:
			aaa = self.change_python_file_to_sorted_by_def(path + one)
			num = num + len(aaa)
			result.append([one, len(aaa)])
		result.append(["총갯수는 ===>", num])
		return result


	def count_method_for_python_file(self, python_file_list, path=""):
		"""
		원하는 python화일안에 몇개의 def로 정의된 메소드가 있는지 확인하는 것이다

		:param python_file_list:
		:param path:
		:return:
		"""
		result = []
		num = 0
		for one in python_file_list:
			aaa = self.sort_python_file_by_def(path + one)
			num = num + len(aaa)
			result.append([one, len(aaa)])
		result.append(["총갯수는 ===>", num])
		return result

	def count_same_value_for_ordered_list(self, input_list):
		"""
		2개이상 반복되는것중 높은 갯수 기준으로 돌려주는것

		:param input_list:
		:return:
		"""
		result_dic = {}
		# 리스트안의 자료가 몇번나오는지 갯수를 센후에
		# 1번이상의 자료만 남기고 다 삭제하는것
		for one in input_list:
			if one in result_dic.keys():
				result_dic[one] = result_dic[one] + 1
			else:
				result_dic[one] = 1

		# 1번이상의 자료만 남기고 다 삭제하는것
		for one in list(result_dic.keys()):
			if result_dic[one] == 1:
				del result_dic[one]

		# 사전자료를 2차원리스트로 만든것
		new_list = []
		for key, val in result_dic.items():
			new_list.append([key, val])

		# 사전자료를 2차원리스트로 만든것을 역순으로 정렬한것
		new_list = sorted(new_list, key=lambda x: x[1], reverse=True)
		return new_list

	def delete_all_explanation_for_python_file(self, input_text):
		"""
		넘어온 python화일 에서 주석으로 사용되는 것들을 지우는것

		:param input_text:
		:return:
		"""
		input_text = re.sub(re.compile(r"[\s]*#.*[\n]"), "\n", input_text)
		input_text = re.sub(re.compile(r"[\s]*''',*?'''", re.DOTALL | re.MULTILINE), "", input_text)
		input_text = re.sub(re.compile(r'[\s]*""".*?"""', re.DOTALL | re.MULTILINE), "", input_text)
		input_text = re.sub(re.compile(r"[\n][\s]*?[\n]"), "\n", input_text)
		return input_text

	def delete_continious_same_value_for_list_1d(self, input_list):
		"""
		연속된 같은 자료만 지우는 것

		:param input_list:
		:return:
		"""
		result = []
		for no in range(len(input_list) - 1):
			if input_list[no] == input_list[no + 1]:
				pass
			else:
				result.append(input_list[no])
		return result

	def delete_continious_same_value_for_list_2d_by_multi_yline(self, list_2d, y_list):
		"""
		2 차원리스트의 자료중에서, 1,3 번이 동시에 연속적으로 같은 것은 삭제

		:param list_2d:
		:param y_list:
		:return:
		"""
		if type(y_list) != type([]):
			y_list = [y_list]
		result = []
		old_line = None
		for ix, list_1d in enumerate(list_2d):
			current_line = ""
			for index in y_list:
				current_line = current_line + str(list_1d[index])
				if ix == 0:
					result.append(list(list_1d))
					old_line = current_line
				else:
					if old_line == current_line:
						print(list(list_1d), "===-> 같음")
					else:
						result.append(list(list_1d))
						old_line = current_line
						print(list(list_1d))
		return result

	def delete_dic_db_1d_with_partial(self, i_dic, i_key=[1, 2, 3]):
		"""
		아래와같은 1차원의 형태로 가능한 database를 만들어 보자
		이것은 엑셀과같은 고유한 셀이나 다른곳의 값을 넣고 뺄때 편할것 같다

		:param i_dic:
		:param i_key:
		:return:
		"""
		len_a = len(i_key)
		checked_i_key = list(i_key)
		for one_key in i_dic.keys():
			if list(one_key)[0:len_a] == checked_i_key:
				del i_dic[one_key]

	def delete_each_value_of_list_1d_in_list_2d_by_index_list(self, input_list_2d, no_list):
		"""
		입력형태 : 2차원리스트, [2,5,7]
		2차원자료의 각 1차원자료의 index번호에 따라서 값을 없애는것

		[2,5,7]라인을 없래라는 뜻이라면,
		[[1,2,3,4,5,6,7,8], [1,2,3,4,5,6,7,8],] => [[1,2,4,5,7], [1,2,4,5,7]]

		:param input_list_2d:
		:param no_list:
		:return:
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list_2d)):
				del input_list_2d[x][one]
		return input_list_2d

	def delete_empty_column_for_df(self, df_obj):
		"""
		dataframe의 빈열을 삭제
		제목이 있는 경우에만 해야 문제가 없을것이다
		"""
		nan_value = float("NaN")
		df_obj.replace(0, nan_value, inplace=True)
		df_obj.replace("", nan_value, inplace=True)
		df_obj.dropna(how="all", axis=1, inplace=True)
		return df_obj

	def delete_empty_folder_in_path(self, old_dir):
		"""
		폴더삭제
		폴더안에 자료가 없어야 삭제

		:param old_dir:
		:return:
		"""
		os.rmdir(old_dir)

	def delete_empty_line_in_list_2d(self, input_list_2d):
		"""
		가로나 세로열을 기준으로 값이 없는것을 삭제하기
		입력으로 들어온 2차원의 자료중에서, 가로행이 완전히 빈것을 삭제하는 기능

		:param input_list_2d: 2차원 형태의 리스트
		:return:
		"""
		base_no = len(input_list_2d[0])
		result = []
		for list_1d in input_list_2d:
			check_no = 0
			for value in list_1d:
				if value in [[], (), "", None]:
					check_no = check_no + 1
			if check_no != base_no:
				result.append(list_1d)
		return result

	def delete_empty_value_in_list(self, input_list, condition=["", None, [], ()]):
		"""
		넘어온 리스트 형태의 자료중 조건에 맞는것이 있으면 제거하는 것
		입력형태 : ["aaa", "", None, "", "bbb"], [["aaa", "", None, "", "bbb"],"werw", 31231, [], ["aaa", "", None, "", "bbb"]]
		출력형태 : ["aaa", "bbb"], [['aaa', 'bbb'], 'werw', 31231, [], ['aaa', 'bbb']]

		:param input_list:
		:param condition:
		:return:
		"""
		for x in range(len(input_list) - 1, -1, -1):
			if input_list[x] in condition:
				del (input_list[x])
			else:
				if type(input_list[x]) == type([]):
					for y in range(len(input_list[x]) - 1, -1, -1):
						if input_list[x][y] in condition:
							del (input_list[x][y])
				else:
					if input_list[x] in condition:
						del (input_list[x])
		return input_list

	def delete_empty_value_in_list_2d(self, input_list_2d):
		"""
		가로나 세로열을 기준으로 값이 없는것을 삭제하기
		입력으로 들어온 2차원의 자료중에서, 가로행이 완전히 빈것을 삭제하는 기능

		:param input_list_2d: 2차원 형태의 리스트
		:return: 없음
		"""
		base_no = len(input_list_2d[0])
		result = []
		for list_1d in input_list_2d:
			check_no = 0
			for value in list_1d:
				if value in [[], (), "", None]:
					check_no = check_no + 1
			if check_no != base_no:
				result.append(list_1d)
		return result

	def delete_empty_xline_and_yline_in_list_2d(self, input_list_2d):
		"""
		2차원자료에서 전체가 빈 가로줄과 세로줄의 자료를 삭제하는 것

		:param input_list_2d:
		:return:
		"""
		temp_result = []
		for list_1d in input_list_2d:
			for value in list_1d:
				if value:
					temp_result.append(list_1d)
					break
		r_temp_result = self.change_xylist_to_yxlist(temp_result)
		temp_result_2 = []
		for list_1d in r_temp_result:
			for value in list_1d:
				if value:
					temp_result_2.append(list_1d)
					break
		result = self.change_xylist_to_yxlist(temp_result_2)
		return result

	def delete_empty_xline_in_list_2d(self, input_list_2d):
		"""
		가로나 세로열을 기준으로 값이 없는것을 삭제하기
		입력으로 들어온 2차원의 자료중에서, 가로행이 완전히 빈것을 삭제하는 기능

		:param input_list_2d: 2차원 형태의 리스트
		:return:
		"""
		base_no = len(input_list_2d[0])
		result = []
		for list_1d in input_list_2d:
			check_no = 0
			for value in list_1d:
				if value:
					break
				else:
					check_no = base_no + 1
			if check_no != base_no:
				result.append(list_1d)
		return result

	def delete_empty_yline_in_list_2d(self, input_list_2d):
		"""
		입력으로 들어온 2차원의 자료중에서, 세로행이 처음부터 끝까지 빈Y열을 삭제하는 기능

		:param input_list_2d: 2차원 형태의 리스트
		:return:
		"""
		changed_list_2d = self.change_xylist_to_yxlist(input_list_2d)
		temp = self.delete_empty_line_in_list_2d(changed_list_2d)
		result = self.change_xylist_to_yxlist(temp)
		return result

	def delete_even_element_in_list_1d(self, data):
		"""
		홀수의 자료만 삭제

		:param data:
		:return:
		"""
		result = []
		for no in range(len(data)):
			if divmod(no, 2)[1] != 1:
				result.append(data[no])
		return result

	def delete_file(self, old_path):
		"""
		화일삭제

		:param old_path:
		:return:
		"""
		old_path = self.check_file_path(old_path)
		os.remove(old_path)

	def delete_folder(self, old_dir, empty="no"):
		"""
		폴더삭제
		폴더안에 자료가 있어도 삭제
		"""
		if empty == "no":
			shutil.rmtree(old_dir)
		else:
			os.rmdir(old_dir)

	def delete_line_in_list_2d_by_index_list(self, input_list_2d, no_list):
		"""
		2차원자료를 기준으로 index번호를 기준으로 삭제하는것
		어찌보면 1차원 리스트와 같은것이다
		입력형태 : 2차원리스트, [2,5,7]

		:param input_list_2d:
		:param no_list:
		:return:
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list_2d)):
				del input_list_2d[x][one]
		return input_list_2d

	def delete_list_1d_in_list_2d_by_step(self, input_list, step, start=0):
		"""
		원하는 순서째의 자료를 ""으로 만드는것

		:param input_list:
		:param step:
		:param start:
		:return:
		"""
		flag_no = 0
		for num in range(start, len(input_list)):
			flag_no = flag_no + 1
			if flag_no == step:
				input_list[num] = ""
				flag_no = 0
		return input_list

	def delete_no_meaning_words_in_list(self, input_list, change_word_dic):
		"""
		의미없는 단어를 삭제하는것

		:param input_list:
		:param change_word_dic:
		:return:
		"""
		sql_1 = "[시작][숫자&특수문자:1~][끝]"  # 숫자만있는것을 삭제
		sql_2 = "[시작][숫자:1:5][영어&한글:1:1][끝]"  # 1223개 와 같은것 삭제
		sql_3 = "[시작][한글:1~][끝]"  #
		sql_4 = "[\(][문자:1~][\)]"  # 괄호안의 글자삭제

		result = []
		for one in input_list:
			one = str(one).strip()
			if self.xre.match(sql_3, one):
				if one in list(change_word_dic.keys()):
					print("발견 ==> 바꿀문자", one)
					one = change_word_dic[one]

			if self.xre.match(sql_4, one):
				print("발견 ==> (문자)  : ", one)
				one = self.xre.delete_with_jf_sql(sql_4, one)
				print("------------->", one)

			if len(one) <= 1:
				one = ""
			elif self.xre.match(sql_1, one):
				print("발견 ==> 숫자만", one)
				one = ""
			elif self.xre.match(sql_2, one):
				print("발견 ==> 숫자+1글자", one)
				one = ""

			if one != "":
				result.append(one)

			result_unique = list(set(result))
		return result_unique

	def delete_odd_element_in_list_1d(self, data):
		"""
		짝수의 자료만 삭제

		:param data:
		:return:
		"""
		result = []
		for no in range(len(data)):
			if divmod(no, 2)[1] != 0:
				result.append(data[no])
		return result

	def delete_over_2_continious_empty_line_in_file(self, filename):
		"""
		화일을 읽어 내려가다가 2줄이상의 띄어쓰기가 된것을 하나만 남기는것

		:param filename:
		:return:
		"""
		f = open(filename, 'r', encoding='UTF8')
		lines = f.readlines()
		num = 0
		result = ""
		for one_line in lines:
			if one_line == "\n":
				num = num + 1
				if num == 1:
					result = result + str(one_line)
				elif num > 1:
					# print("2줄발견")
					pass
			else:
				num = 0
				result = result + str(one_line)
		print(result)
		return result

	def delete_partial_same_list_1d_in_list_2d_by_range(self, input_list_2d, start_index=0, end_index=None):
		"""
		입력받은 2d자료형에서
		같은것을 삭제하는데, 일부영역으로 같은것을 판단, 전체를 삭제한다

		:param input_list_2d:
		:param input_no:
		:return:
		"""

		is_same = []
		result = []
		for one in input_list_2d:
			partial_list = one[start_index:end_index]
			if partial_list in is_same:
				pass
			else:
				is_same.append(partial_list)
				result.append(one)
		return result

	def delete_same_list_1d_in_list_2d_when_same_at_index(self, input_list_2d, base_index):
		"""
		2차원의 자료를 기준으로 각 1차원자료의 n번째 값이 같으면 제외하고 고유한것만 돌려주는 것이다

		2차원자료중에서 몇번째의 자료가 같은 것만 삭제하는것

		:param input_list_2d: 2차원 형태의 리스트
		:param base_index:
		:return:
		"""
		waste_letters = [" ", ',', '.', '"', "'", ',', '?', '-']
		result = []
		only_one = set()
		for one_list in input_list_2d:
			new_value = str(one_list[base_index])
			for one in waste_letters:
				new_value = new_value.replace(one, "")

			if new_value in only_one:
				print("같은것 찾음")
			else:
				result.append(one_list)
				only_one.add(new_value)
		return result

	def delete_same_value_in_list(self, input_datas, status=0):
		"""
		1차원리스트안의 원소중에 고유한것만 남기고 삭제하는 것

		:param input_datas:
		:param status:
		:return:
		"""
		if status == 0:
			result = []
			# 계속해서 pop으로 하나씩 없애므로 하나도 없으면 그만 실행한다
			while len(input_datas) != 0:
				gijun = input_datas.pop()
				sjpark = 0
				result.append(gijun)
				for num in range(len(input_datas)):
					if input_datas[int(num)] == []:  # 빈자료일때는 그냥 통과한다
						pass
					if input_datas[int(num)] == gijun:  # 자료가 같은것이 있으면 []으로 변경한다
						sjpark = sjpark + 1
						input_datas[int(num)] = []
			else:
				# 중복된것중에서 아무것도없는 []마저 없애는 것이다. 위의 only_one을 이용하여 사용한다
				# 같은것중에서 하나만 남기고 나머지는 []으로 고친다
				# 이것은 연속된 자료만 기준으로 삭제를 하는 것입니다
				# 만약 연속이 되지않은 같은자료는 삭제가 되지를 않읍니다
				result = list(set(input_datas))
				for a in range(len(result) - 1, 0, -1):
					if result[a] == []:
						del result[int(a)]
		return result

	def delete_same_value_in_list_2d_limit_no(self, input_list_2d, input_no=2):
		"""
		입력받은 2d자료형에서
		뒤에서 몇번째의 자료를 제외하고 같은 자료를 입력받은것엣 지우기

		:param input_list_2d:
		:param input_no:
		:return:
		"""
		is_same = []
		result = []
		for one in input_list_2d:
			if one[:-input_no] in is_same:
				pass
			# print(one)
			else:
				is_same.append(one[:-input_no])
				result.append(one)
		return result

	def delete_set_item_as_same_list_data(self, input_set, input_list):
		"""
		list의 항목으로 들어간것을 하나씩 꺼내어서
		set안에 같은것이 있으면 지운다

		:param input_set:
		:param input_list:
		:return:
		"""
		for one in input_list:
			input_set.remove(one)
		return input_set

	def delete_special_char_in_text_except_num_n_eng(self, original_data):
		return self.change_waste_data(original_data)

	def delete_sub_tree_for_dic_by_key(self, i_dic, target_key, depth, current_depth=1):
		"""
		키값을 기준으로 n차원의 자료를 삭제하는것

		:param i_dic:
		:param target_key:
		:param depth:
		:param current_depth:
		:return:
		"""
		if current_depth == depth:
			if target_key in i_dic:
				del i_dic[target_key]
		else:
			for key, value in list(i_dic.items()):
				if isinstance(value, dict):
					self.delete_sub_tree_for_dic_by_key(value, target_key, depth, current_depth + 1)
					if not value:
						del i_dic[key]
		return i_dic

	def delete_sub_tree_for_dic_by_value(self, i_dic, target_value, depth, current_depth=1):
		"""
		사전형식에서 깊이가 n-depth아래에있는 입력값을 삭제하는 것

		:param i_dic:
		:param target_value:
		:param depth:
		:param current_depth:
		:return:
		"""
		if current_depth == depth:
			keys_to_delete = [key for key, value in i_dic.items() if value == target_value]
			for key in keys_to_delete:
				del i_dic[key]
		else:
			for key, value in list(i_dic.items()):
				if isinstance(value, dict):
					self.delete_sub_tree_for_dic_by_value(value, target_value, depth, current_depth + 1)
					if not value:
						del i_dic[key]
		return i_dic

	def delete_text_between_bracket_and_bracket(self, input_text):
		"""
		입력텍스트에서 괄호안의 모든 문자를 지우는것

		:param input_text:
		:return:
		"""
		re_basic = '\([^)]*\)'
		new_value = re.sub(re_basic, '', input_text)
		return new_value

	def delete_value_in_dic_db_by_below_n_depth(self, main_dic, i_depth_list):
		"""
		사전형 db에서 모든 n번째 깊이 이하의 모든 입력값을 삭제하는 것

		:param main_dic:
		:param i_depth_list:
		:return:
		"""
		i_dic = main_dic[0]
		if len(i_depth_list) > 1:
			for index, one_value in enumerate(i_depth_list[:-1]):
				checked_key = str(index + 1) + "_" + str(one_value)
				i_dic = i_dic[checked_key][1]

		checked_key1 = str(len(i_depth_list)) + "_" + str(i_depth_list[-1])
		del i_dic[checked_key1]

	def delete_waste_data_for_list(self, original_data):
		return self.change_waste_data(original_data)

	def delete_waste_data_in_data_except_number_eng(self, original_data):
		return self.change_waste_data(original_data)

	def delete_xline_for_list_2d_by_index_list(self, input_list_2d, no_list):
		"""
		입력형태 : 2차원리스트, [2,5,7]
		메뉴에서 제외

		:param input_list_2d: list type 2dimension, 2차원의 리스트형
		:param no_list:
		:return:
		"""
		no_list.sort()
		no_list.reverse()  # 뒤에서부터 삭제를 해야 문제가 발생하지 않는다
		for one in no_list:
			for x in range(len(input_list_2d)):
				del input_list_2d[x][one]
		return input_list_2d

	def dialog_for_file(self):
		"""
		일반적인 메세지박스를 만드는 것이다

		:return:
		"""
		result = win32gui.GetOpenFileNameW(DefExt="*.*")
		return result

	def dialog_for_file_with_image_type(self, file_type=""):
		"""
		일반적인 이미지를 불러오는 메세지박스를 나타낸다

		:return:
		"""
		if file_type == "":
			filter = "Picture Files \*.*"
		else:
			filter = "Picture Files \0*.jp*;*.gif;*.bmp;*.png\0Text files\0*.txt\0"
		# filter = "Picture Files (*.jp*; *.gif; *.bmp; *.png),*.xls"
		result = win32gui.GetOpenFileNameW(InitialDir=os.environ["temp"],
										   Filter=filter,
										   Flags=win32con.OFN_ALLOWMULTISELECT | win32con.OFN_EXPLORER,
										   File="somefilename", DefExt="py",
										   Title="GetOpenFileNameW",
										   FilterIndex=0)

		# print(result)
		return result

	def dialog_for_folder_name(self):
		"""
		일반적인 메세지박스를 만드는 것이다

		:return:
		"""

		shell = win32com.client.Dispatch("WScript.Shell")

		# 폴더 선택 대화 상자 열기
		# folder_path = shell.SpecialFolders("Desktop")  # 초기 디렉토리를 바탕화면으로 설정
		# folder = shell.Folder(folder_path)
		# folder_id_list = folder.self.Persist()

		# 폴더 선택 대화 상자 옵션 설정 (필요에 따라 추가)
		# 예: BIF_RETURNONLYFSDIRS (파일 시스템 디렉토리만 반환)
		#      BIF_NEWDIALOGSTYLE (새로운 스타일의 대화 상자)

		# 폴더 선택 대화 상자 띄우기
		result = shell.BrowseForFolder(0, "폴더 선택", 0)

		return result

	def dialog_for_general_with_time(self, input_text, second, title="www.xython.co.kr"):
		"""
		몇초후에 팝업창이 자동으로 사라지는것

		:param input_text: 팝업창에 나타나는 문구
		:param second: 팝업창이 존재하는 초
		"""
		shell = win32com.client.Dispatch('WScript.Shell')
		intReturn = shell.Popup(input_text, second, title)

	def dialog_for_messagebox(self, input_text="입력필요", input_title="xython.co.kr"):
		"""
		사용하기 편하게 이름을 바꿈
		original : write_value_in_messagebox

		:param input_text:
		:param input_title:
		:return:
		"""
		win32api.MessageBox(0, input_text, input_title, 16)

	def dialog_for_messagebox_with_time(self, input_text, second, title="www.xython.co.kr"):
		"""
		몇초후에 팝업창이 자동으로 사라지는것

		:param input_text: 팝업창에 나타나는 문구
		:param second: 팝업창이 존재하는 초
		"""
		shell = win32com.client.Dispatch('WScript.Shell')
		intReturn = shell.Popup(input_text, second, title)

	def diff_list1_list2(self, input_list1, input_list2):
		"""
		두개의 리스트에서 디의 자료를 삭제하는것

		:param input_list1:
		:param input_list2:
		:return:
		"""
		for one in input_list2:
			try:
				input_list1.remove(one)
			except:
				pass

		result = input_list1
		return result

	def draw_get_diagonal_xy(self, xyxy=[5, 9, 12, 21]):
		"""
		좌표와 대각선의 방향을 입력받으면, 대각선에 해당하는 셀을 돌려주는것
		좌표를 낮은것 부터 정렬하기이한것 [3, 4, 1, 2] => [1, 2, 3, 4]
		"""
		result = []
		if xyxy[0] > xyxy[2]:
			x1, y1, x2, y2 = xyxy[2], xyxy[3], xyxy[0], xyxy[1]
		else:
			x1, y1, x2, y2 = xyxy

		x_height = abs(x2 - x1) + 1
		y_width = abs(y2 - y1) + 1
		step = x_height / y_width
		temp = 0

		if x1 <= x2 and y1 <= y2:
			# \형태의 대각선
			for y in range(1, y_width + 1):
				x = y * step
				if int(x) >= 1:
					final_x = int(x) + x1 - 1
					final_y = int(y) + y1 - 1
					if temp != final_x:
						result.append([final_x, final_y])
						temp = final_x
		else:
			for y in range(y_width, 0, -1):
				x = x_height - y * step

				final_x = int(x) + x1
				final_y = int(y) + y1 - y_width
				temp_no = int(x)

				if temp != final_x:
					temp = final_x
					result.append([final_x, final_y])
		return result

	def draw_triangle(self, xyxy, per=100, reverse=1, size=100):
		"""
		직각삼각형
		정삼각형에서 오른쪽이나 왼쪽으로 얼마나 더 간것인지
		100이나 -100이면 직삼각형이다
		사각형은 왼쪽위에서 오른쪽 아래로 만들어 진다

		:param xyxy:
		:param per:
		:param reverse:
		:param size:
		:return:
		"""
		x1, y1, x2, y2 = xyxy
		width = x2 - x1
		height = y2 - y1
		lt = [x1, y1]  # left top
		lb = [x2, y1]  # left bottom
		rt = [x1, y2]  # right top
		rb = [x2, y2]  # right bottom
		tm = [x1, int(y1 + width / 2)]  # 윗쪽의 중간
		lm = [int(x1 + height / 2), y1]  # 윗쪽의 중간
		rm = [int(x1 + height / 2), y1]  # 윗쪽의 중간
		bm = [x2, int(y1 + width / 2)]  # 윗쪽의 중간
		center = [int(x1 + width / 2), int(y1 + height / 2)]

		result = [lb, rb, rt]
		return result

	def euclidean_distance(self, point1, point2):
		"""
		n차원 공간에서 두 점 사이의 유클리드 거리를 계산합니다

		:param point1: 첫 번째 점 (리스트 또는 튜플)
		:param point2: 두 번째 점 (리스트 또는 튜플)
		:return: 두 점 사이의 유클리드 거리
		"""
		if len(point1) != len(point2):
			raise ValueError("두 점은 같은 차원이어야 합니다.")
		distance = math.sqrt(sum((p - q) * 2 for p, q in zip(point1, point2)))
		return distance

	def filter_3_list_with_3_order_no(self, i_list_2d, i_no_list):
		"""
		입력되는 2차원자료에서, 원하는 순서번째의 자료만 갖고오는 것
		bbb = pick_3_list_with_3_order_no(aaa, [5,3,2])
		:param i_list_2d:
		:param i_no_list:
		:return:
		"""
		result = []
		for no in i_no_list:
			result.append(i_list_2d[no - 1])
		return result

	def filter_element_for_list_1d_by_start_with_input_value(self, base_data, input_list):
		"""
		1차원 리스트중 입력으로 들어온 값으로 시작하는 요소들만 골라내는 것
		:param base_data:
		:param input_list:
		:return:
		"""
		result = True
		for one in input_list:
			if base_data.startswith(one):
				result = False
				break
		return result

	def filter_gtlt_style_for_list_2d(self, input_list_2d, line_no=2, condition=[[2, "<"], ["<=", 4]]):
		"""
		2차원자료에서 크고작은 조건으로 골라내는것

		:param input_list_2d:
		:param line_no:
		:param condition:
		:return:
		"""
		result = []
		if "<" in condition or "<=" in condition or ">" in condition or ">=" in condition:
			if len(condition) == 3:
				if condition[0] == "value":
					for list_1d in input_list_2d:
						exec(f"if {list_1d[line_no - 1]} {condition[1]} {condition[2]}: result.append({list_1d})")
				elif condition[2] == "value":
					for list_1d in input_list_2d:
						exec(f"if {condition[0]} {condition[1]} {list_1d[line_no - 1]}: result.append({list_1d})")
			elif len(condition) == 5:
				for list_1d in input_list_2d:
					aaa = f"if {condition[0]} {condition[1]} {list_1d[line_no - 1]} {condition[3]} {condition[4]}: result.append({list_1d})"
					# print(aaa)
					exec(aaa)
			else:
				for list_1d in input_list_2d:
					if list_1d[line_no - 1] in condition:
						result.append(list_1d)

		return result

	def filter_index_element_in_list_1d_for_list_2d(self, input_list_2d, input_no_list):
		"""
		input_no_list.sort()
		input_no_list.reverse()

		:param input_list_2d:
		:param input_no_list:
		:return:
		"""
		for before, after in input_no_list:
			for no in range(len(input_list_2d)):
				value1 = input_list_2d[no][before]
				value2 = input_list_2d[no][after]
				input_list_2d[no][before] = value2
				input_list_2d[no][after] = value1
		return input_list_2d

	def filter_int_for_list(self, input_list):
		"""
		입력리스트중에 정수만 골라내는 것

		:param input_list:
		"""
		input_list = self.change_list_2d_to_list_1d(input_list)
		result = False
		for one in input_list:
			if type(123) == type(one):
				result = one
				break
		return result

	def filter_int_for_list_1d(self, input_list):
		return self.filter_int_for_list(input_list)

	def filter_list_1d_by_string(self, input_list, input_text):
		"""
		리스트로 들어온 자료들을 한번에 분리해서 2차원리스트로 만드는 것

		:param input_list:
		:param input_text:
		:return:
		"""

		result = []
		for one_value in input_list:
			temp_result = str(one_value).split(input_text)
			result.append(temp_result)
		return result

	def filter_list_1d_for_list_2d_when_same_value_in_nth_position(self, input_list_2d, input_position, input_value):
		"""
		입력으로 들어온 2차원 자료에서, 특정 위치의 특정값인것만 갖고오기

		:param input_list_2d:
		:param input_position:
		:param input_value:
		:return:
		"""
		result = []
		for list_1d in input_list_2d:
			if list_1d[input_position] == input_value:
				result.append(list_1d)
		return result

	def filter_list_1d_for_same_data_with_option(self, i_list_1d, i_text, i_position="", all_or_part="part"):
		"""
		리스트의 어떤 자료에서, 글자가 포함된 것을 삭제하는 기능
		1차원 리스트의 자료중에서 , 입력으로 들어오는 자료와 부분이 같은 경우나 전체가 같은 경우를 구분한다
		기본적으로 영문으로 입력하는 값은 앞의 3글자만 입력하여도 가능하도록 만든다

		:param i_list_1d:
		:param i_text:
		:param i_position:
		:param all_or_part:
		:return:
		"""
		result = []
		if all_or_part == "all":
			for one in i_list_1d:
				if not one == i_text:
					result.append(one)
		elif i_position in ["right", "오른쪽", "끝", "end", "rig"]:
			for one in i_list_1d:
				if not str(one).endswith(i_text):
					result.append(one)
		elif i_position in ["left", "왼쪽", "시작", "start", "lef", "sta"]:
			for one in i_list_1d:
				if not str(one).startswith(i_text):
					result.append(one)
		elif i_position in ["", "중간", "middle", "mid", "부분", "partial", "par"]:
			for one in i_list_1d:
				if not i_text in one:
					result.append(one)
		else:
			# 맞는것이 없으면 partial 로 간주 한다
			for one in i_list_1d:
				if not i_text in one:
					result.append(one)
		return result

	def filter_list_2d_by_same_value_in_ylines(self, list_2d, y_no_list_1d, input_value_list_1d):
		"""
		list_2d의 n번째 줄의 값이 input_value인것만 찾아내는 것
		:param list_2d:
		:param y_no:
		:param input_value:
		:return:
		"""
		result = []
		len_gijun = len(input_value_list_1d)
		for list_1d in list_2d:
			check_no = 0
			for index, y_no in enumerate(y_no_list_1d):
				if list_1d[y_no - 1] == input_value_list_1d[index]:
					check_no = check_no + 1
			if check_no == len_gijun:
				result.append(list_1d)
		return result

	def filter_list_2d_by_value_in_yline(self, list_2d, y_no, input_value):
		"""
		list_2d의 n번째 줄의 값이 input_value인것만 찾아내는 것
		:param list_2d:
		:param y_no:
		:param input_value:
		:return:
		"""
		result = self.filter_list_2d_by_same_value_in_ylines(list_2d, [y_no], [input_value])
		return result

	def filter_list_2d_for_condition(self, input_list_2d, condition=[[2, 0]]):
		"""
		입력으로 들어온 자료에서
		condition에 있는 조건의 값들만 필터링하는것	[[2번째열, 자료있음], [(6번째열, 자료없음]...]

		:param input_list_2d:
		:param condition:
		:return:
		"""
		result = []
		count_no = len(condition)
		for list_1d in input_list_2d:
			temp = 0
			for one in condition:
				if not one[1] and not list_1d[one[0]]:
					temp = temp + 1
				elif one[1] and list_1d[one[0]]:
					temp = temp + 1
			if temp == count_no:
				result.append(list_1d)
		return result

	def filter_list_2d_for_int_n_str(self, input_list_2d):
		"""
		입력된 2차원자료를 프린트가 가능한 형태로 만든다
		숫자와 문자를 제외하고는 모드 None으로 만드는 것
		"""
		result = []
		for x, list_1d in enumerate(input_list_2d):
			t_list = []
			for y, value in enumerate(list_1d):
				temp = self.check_data_type_for_data(value)
				# print(temp, value)
				if temp in ["int", "string"]:
					t_list.append(value)
				else:
					t_list.append(None)
			result.append(t_list)
		print(result)
		return result

	def filter_list_2d_for_not_empty_value_by_index(self, input_list_2d, index_no=4):
		"""
		index 번호의 Y열의 값이 빈것이 아닌것만 돌려주는 것

		:param input_list_2d:
		:param index_no:
		:return:
		"""
		result = []
		others = []
		for index, one in enumerate(input_list_2d):
			if one[index_no]:
				result.append(one)
			else:
				others.append(one)
		return [result, others]

	def filter_list_2d_for_same_data(self, input_list_2d, input_position, input_value):
		"""
		입력으로 들어온 2차원 자료에서, 특정 위치의 특정값인것만 갖고오기

		:param input_list_2d:
		:param input_position:
		:param input_value:
		:return:
		"""
		result = []
		for list_1d in input_list_2d:
			if list_1d[input_position] == input_value:
				result.append(list_1d)
		return result

	def filter_list_2d_for_same_data_02(self, input_list_2d, same_line=[1, 4]):
		"""
		입력으로 들어온 자료에서
		맨처음의 자료와 같은것만 골라내기

		:param input_list_2d:
		:param same_line:
		:return:
		"""
		result = [input_list_2d[0]]
		count_no = len(same_line)
		for list_1d in input_list_2d[1:]:
			temp = 0
			for no in same_line:
				if input_list_2d[0][no - 1] == list_1d[no - 1]:
					temp = temp + 1
				else:
					break
			if temp == count_no:
				result.append(list_1d)
		return result

	def filter_list_2d_for_same_with_first_line_and_yline(self, input_list_2d, same_line=[1, 4]):
		"""
		입력으로 들어온 자료에서
		맨처음의 자료와 같은것만 골라내기

		:param input_list_2d:
		:param same_line:
		:return:
		"""
		result = [input_list_2d[0]]
		count_no = len(same_line)
		for list_1d in input_list_2d[1:]:
			temp = 0
			for no in same_line:
				if input_list_2d[0][no - 1] == list_1d[no - 1]:
					temp = temp + 1
				else:
					break
			if temp == count_no:
				result.append(list_1d)
		return result

	def filter_list_2d_for_same_with_yline_and_value(self, input_list_2d, input_y_no, input_value):
		"""

		:param input_list_2d:
		:param input_y_no:
		:param input_value:
		:return:
		"""
		result = []
		for list_1d in input_list_2d:
			if list_1d[input_y_no - 1] == input_value:
				result.append(list_1d)
		return result

	def filter_list_2d_for_unique_data(self, input_2dlist):
		"""
		입력된 값중에서 고유한 값만을 골라내는것

		:param input_2dlist:
		:return:
		"""
		result = set()
		if type(input_2dlist[0]) != type([]):
			input_2dlist = [input_2dlist]
		for x in range(len(input_2dlist)):
			for y in range(len(input_2dlist[x])):
				value = input_2dlist[x][y]
				if value == "" or value == None:
					pass
				else:
					result.add(value)
		return list(result)

	def filter_list_2d_for_yline_no_and_value(self, input_list_2d, input_position, input_value):
		"""
		입력으로 들어온 2차원 자료에서, 특정 위치의 특정값인것만 갖고오기

		:param input_list_2d:
		:param input_position:
		:param input_value:
		:return:
		"""
		result = []
		for list_1d in input_list_2d:
			if list_1d[input_position - 1] == input_value:
				result.append(list_1d)
		return result

	def filter_list_2d_to_another_list_2d_by_step(self, input_list_2d, index_no=4):
		"""
		2차원자료를 다 1차원으로 만든후, 다시 입력된 갯수만큼씩 묶어서 2차원으로 만든것

		:param input_list_2d: 2차원 형태의 리스트
		:param index_no:
		:return:
		"""
		result = []
		sorted_list_2d = self.sort_list_2d_by_index(input_list_2d, index_no)
		check_value = sorted_list_2d[0][index_no]
		temp = []
		for one_list in sorted_list_2d:
			if one_list[index_no] == check_value:
				temp.append(one_list)
			else:
				result.append(temp)
				temp = [one_list]
				check_value = one_list[index_no]
		if temp:
			result.append(temp)
		return result

	def filter_list_by_py_range_style(self, input_list, input_text=""):
		"""
		python의 list에사용하는 방법을 좀더 다르게 사용해도 될것같아서 해본다
		이 번호들은 통일성을 위해 index를 기본으로 한다
		1) 1:2:3
		2) ::3
		4) :5:2n+1
		"""
		step = None
		start = None
		end = None
		step_1 = None
		step_2 = None
		temp_1 = input_text.split(":")

		if len(temp_1) == 1:
			pass
		elif len(temp_1) == 2:
			start, end = temp_1
		elif len(temp_1) == 3:
			start, end, step = temp_1
			if "n" in step:
				step_1, step_2 = str(step).split("n")
				step_1 = int(step_1)
				if step_2:
					step_2 = int(step_2)
		num = 0
		result = []
		for index in range(start, end):
			if step_2:
				if divmod(num, step_1)[1] == step_2:
					result.append(input_list[index])
			elif step_1:
				if divmod(num, step_1)[1] == 0:
					result.append(input_list[index])
			num = num + 1
		return result

	def filter_list_for_index_list(self, input_list, position_list):
		"""
		리스트로 넘오온 자료를 원하는 열만 추출하는것

		:param input_list:
		:param position_list:
		:return:
		"""
		result = []
		for one_list in input_list:
			temp = []
			for one in position_list:
				temp.append(one_list[one - 1])
			result.append(temp)
		return result

	def filter_list_for_unique_value(self, input_datas, status=0):
		"""
		중복된 리스트의 자료를 없애는 것이다. 같은것중에서 하나만 남기고 나머지는 []으로 고친다
		"""
		if status == 0:
			result = []
			# 계속해서 pop으로 하나씩 없애므로 하나도 없으면 그만 실행한다
			while len(input_datas) != 0:
				gijun = input_datas.pop()
				sjpark = 0
				result.append(gijun)
				for num in range(len(input_datas)):
					if input_datas[int(num)] == []:  # 빈자료일때는 그냥 통과한다
						pass
					if input_datas[int(num)] == gijun:  # 자료가 같은것이 있으면 []으로 변경한다
						sjpark = sjpark + 1
						input_datas[int(num)] = []
		else:
			# 중복된것중에서 아무것도없는 []마저 없애는 것이다. 위의 only_one을 이용하여 사용한다
			# 같은것중에서 하나만 남기고 나머지는 []으로 고친다
			# 이것은 연속된 자료만 기준으로 삭제를 하는 것입니다
			# 만약 연속이 되지않은 같은자료는 삭제가 되지를 않읍니다
			result = list(self.get_unique_data_in_list_1d(input_datas))
			for a in range(len(result) - 1, 0, -1):
				if result[a] == []:
					del result[int(a)]
		return result

	def filter_max_data(self):
		"""
		자료중에서 가장 큰값이나 작은값을 찾아내는것

		그것을 기준으로 찾아서 자료를 넣어주는 기능

		:return:
		"""
		a = 111
		return a

	def filter_name_and_title_in_text(self, input_name):
		"""
		이름과 직함이 같이 있는 입력값을 이름과 직함으로 분리하는 것

		:param input_name:
		:return:
		"""
		name = ""
		title = ""
		title_list = ["부장", "이사", "프로", "사원", "대리", "과장", "사장", "차장", "대표", "대표이사", "전무", "전무이사", "공장장"]
		input_name = input_name.strip()  # 공백을 없애는 것
		if len(input_name) > 3:
			for one in title_list:
				title_len = len(one)
				if input_name[-title_len:] == one:
					name = input_name[:-title_len]
					title = input_name[-title_len:]
					break
		return [name, title]

	def filter_not_empty_value_in_list_2d_by_index(self, input_list_2d, index_no=4):
		"""
			index 번호의 Y열의 값이 빈것이 아닌것만 돌려주는 것
			"""
		result = []
		for index, one in enumerate(input_list_2d):
			if one[index_no]:
				result.append(one)
		return result

	def filter_same_element_for_two_list_1d(self, list_mother, list_son):
		"""
		두개의 리스트를 비교해서 같은것을 찾는 것이다

		:param list_mother:
		:param list_son:
		:return:
		"""
		result = list_mother
		for one in range(len(list_son)):
			found = 0
			for two in range(len(list_mother)):
				if list_son[one][0] == list_mother[two][0]:
					found = 1
			if found == 0:
				result.append(list_son[one])
				print("새로운것 발견 ===>")
		return result

	def filter_same_value_between_two_list_1d(self, input_list_1d_1, input_list_1d_2):
		"""
		기준값에서 1 차원의 같은 값을 찾는 것이다

		:param input_list_1d_1:
		:param input_list_1d_2:
		:return:
		"""
		result = []
		for one in input_list_1d_1:
			if one in input_list_1d_2:
				result.append(one)
		return result

	def filter_same_value_for_two_list_1d(self, input_list_1, input_list_2):
		"""

		:param input_list_1:
		:param input_list_2:
		:return:
		"""
		checked_list_1d_1 = self.get_unique_data_in_list_1d(input_list_1)
		checked_list_1d_2 = self.get_unique_data_in_list_1d(input_list_2)
		# print(checked_list_1d_1)
		result = []
		for one_data in checked_list_1d_1:
			if one_data in checked_list_1d_2:
				result.append(one_data)
		return result

	def filter_same_value_in_list_2d(self, input_list_1d_1, input_list_1d_2):
		"""
		2차원의 자료안에서 입력값이 같은것을 찾아내기
		:param input_list_1d_1:
		:param input_list_1d_2:
		:return:
		"""
		result = []
		for one in input_list_1d_1:
			if one in input_list_1d_2:
				result.append(one)
		return result

	def filter_similality_for_list_1d_with_two_words(self, input_list_1d, base_num=0.6):
		"""
		입력된 자료에서 유사도를 검사해서 기본설정값보다 높은 값들의 자료만 갖고옮

		:param input_list_1d:
		:param base_num:
		:return:
		"""
		result = []
		num = 0
		for one in input_list_1d:
			for two in input_list_1d[num:]:
				ratio = difflib.SequenceMatcher(None, one, two).ratio()
				if ratio >= base_num and ratio != 1.0:
					# print(one, two, " : 유사도는 = = >", ratio)
					result.append([ratio, one, two, ])
		num = num + 1
		return result

	def filter_str_for_list_1d(self, input_list):
		"""
		문자형 자료만 추출하는것

		:param input_list:
		:return:
		"""
		result = []
		for one_data in input_list:
			if type("abc") == type(one_data):
				result.append(one_data)
		return result

	def filter_text_for_eng(self, input_text):
		"""
		단어중에 나와있는 영어만 분리하는기능
		"""
		re_compile = re.compile(r"([a-zA-Z]+)")
		result = re_compile.findall(input_text)
		new_result = []
		for dim1_data in result:
			for dim2_data in dim1_data:
				new_result.append(dim2_data)
		return new_result

	def filter_text_for_num(self, input_text):
		"""
		단어중에 나와있는 숫자만 분리하는기능
		"""
		re_compile = re.compile(r"([0-9]+)")
		result = re_compile.findall(input_text)
		new_result = []
		for dim1_data in result:
			for dim2_data in dim1_data:
				new_result.append(dim2_data)
		return new_result

	def filter_unique_col_name_compare_table_col_name(self, table_name, data2):
		"""
		고유한 컬럼만 골라낸다

		:param table_name:
		:param data2:
		:return:
		"""
		result = []
		columns = self.get_all_filename_in_folder(table_name)
		update_data2 = self.delete_waste_data_in_data_except_number_eng(data2)
		for temp_3 in update_data2:
			if not temp_3.lower() in columns:
				result.append(temp_3)
		return result

	def filter_unique_data_for_list_1d(self, input_data):
		"""
		리스트의 값중 고유한것만 골라내기
		"""
		temp = set()
		for one in input_data:
			temp.add(one)
		result = list(temp)
		return result

	def filter_unique_data_for_list_1d_02(self, input_datas, status=0):
		"""
		중복된 리스트의 자료를 없애는 것이다. 같은것중에서 하나만 남기고 나머지는 []으로 고친다
		"""
		if status == 0:
			result = []
			# 계속해서 pop으로 하나씩 없애므로 하나도 없으면 그만 실행한다
			while len(input_datas) != 0:
				gijun = input_datas.pop()
				sjpark = 0
				result.append(gijun)
				for num in range(len(input_datas)):
					if input_datas[int(num)] == []:  # 빈자료일때는 그냥 통과한다
						pass
					if input_datas[int(num)] == gijun:  # 자료가 같은것이 있으면 []으로 변경한다
						sjpark = sjpark + 1
						input_datas[int(num)] = []
		else:
			# 중복된것중에서 아무것도없는 []마저 없애는 것이다. 위의 only_one을 이용하여 사용한다
			# 같은것중에서 하나만 남기고 나머지는 []으로 고친다
			# 이것은 연속된 자료만 기준으로 삭제를 하는 것입니다
			# 만약 연속이 되지않은 같은자료는 삭제가 되지를 않읍니다
			result = list(self.get_unique_data_in_list_1d(input_datas))

			for a in range(len(result) - 1, 0, -1):
				if result[a] == []:
					del result[int(a)]
		return result

	def filter_unique_element_for_list_1d(self, input_data):
		"""
		리스트의 값중 고유한것만 골라내기

		:param input_data:
		:return:
		"""
		temp = set()
		for one in input_data:
			temp.add(one)
		result = list(temp)
		return result

	def filter_unique_element_for_list_2d(self, input_list_2d):
		"""
		입력된 값중에서 고유한 값만을 골라내는것

		:param input_list_2d:
		:return:
		"""
		result = set()
		if type(input_list_2d[0]) != type([]):
			input_list_2d = [input_list_2d]
		for x in range(len(input_list_2d)):
			for y in range(len(input_list_2d[x])):
				value = input_list_2d[x][y]
				if value == "" or value == None:
					pass
				else:
					result.add(value)
		return list(result)

	def filter_yline_set_at_list_2d(self, input_list_2d, input_y_index_list):
		"""
		2차원리스트에서, [1,3,5]번째의 값만 필터링해서 새로운 2차원리스트자료로 만드는 것

		:param input_list_2d:
		:param list_1d:
		:return:
		"""
		result = []
		for list_1d in input_list_2d:
			temp = []
			for y_index in input_y_index_list:
				temp.append(list_1d[y_index])
			result.append(temp)
		return result

	def find_filename_in_folder(self, directory, target_filename):
		"""
		입력디렉토리안의 모든 화일중에서 원하는 화일이름이 들어있는 화일을 찾는 것

		:param directory:
		:param target_filename:
		:return:
		"""
		matching_files = []
		for root, dirs, files in os.walk(directory):
			for file in files:
				if file == target_filename:
					file_path = os.path.join(root, file)
					creation_time = os.path.getctime(file_path)
					creation_date = datetime.fromtimestamp(creation_time).strftime('%y%m%d')
					matching_files.append([root, creation_date, file])
		return matching_files

	def find_more_elements(self, list1, list2):
		"""
		두개의 리스트에서, 작은것을 기준으로 큰것중에 어느부분이 더 있고, 위치는 어디인지를 알려주는 것
		이것의 사용목적은 워드에서 영역안의 글자를 읽어오는데, 3가지의 경우가 잇어서, 어떤것이 어떤 부분이 다른것들과 차이가 나는지를
		확인하기위해서 만든것이다

		:param list1:
		:param list2:
		:return:
		"""

		counter1 = collections.Counter(list1)
		counter2 = collections.Counter(list2)
		if len(counter1) < len(counter2):
			smaller_counter = counter1
			larger_counter = counter2
			smaller_list = list1
			larger_list = list2
		else:
			smaller_counter = counter2
			larger_counter = counter1
			smaller_list = list2
			larger_list = list1
		more_elements = []
		for element in larger_counter:
			if element not in smaller_counter or larger_counter[element] > smaller_counter[element]:
				more_elements.append(element)
		result = []
		for element in more_elements:
			positions = [i for i, x in enumerate(larger_list) if x == element]
			result.append((element, positions))
		return result

	def find_near_value(self, sorted_list, input_no):
		"""
		정렬된 자료를 기준자료로하여, 입력된 자료에서 가장 가까운 값 기준자료를 찾아주는 코드
		양쪽이 같은 크기만큼 떨어진 경우는 작은 값을 우선으로 표현합니다

		사용할 곳 : 색에 대해서 전체를 사용하지 않고, index개념으로 사용하는 색에 대해서,  index를 rgbint값으로 바꾸던지
		decimal로 바꿔서 그중에 가까운것을 찾는 것
		RGB값에 대해서 가장 가까운 rgbint값을 찾는 것입니다

		:param sorted_list: 정렬된 2차원 자료들
		:param input_no:
		:return:
		"""
		pos = bisect.bisect_left(sorted_list, input_no)
		# 가장 가까운 값을 찾기 위해 양쪽 값을 비교합니다
		if pos == 0:
			result = sorted_list[0]
		elif pos == len(sorted_list):
			result = sorted_list[-1]
		elif abs(sorted_list[pos] - input_no) < abs(input_no - sorted_list[pos - 1]):
			result = sorted_list[pos]
		else:
			result = sorted_list[pos - 1]
		return result

	def find_one_line_by_value_in_y_line(self, list_2d, check_value, y_line_no=1):
		"""

		:param list_2d:
		:param check_value:
		:param y_line_no:
		:return:
		"""
		for list_1d in list_2d:
			if list_1d[y_line_no] == check_value:
				return list_1d

	def find_text_between_brackets(self, input_text):
		"""
		괄호안의 글자를 추출해서 알려주는 것이며, 다중 괄호도 가능하게 만든 것이다
		"""
		stack = []
		result = []
		num_left = 0
		num_right = 0

		changed_start = 0
		for i, char in enumerate(input_text):
			if char == '(':
				num_left = num_left + 1
				stack.append(i)
				if num_left == 1:
					start = i
			elif char == ')':
				num_right = num_right + 1
				end = i
				if num_left == num_right and num_left != 0:
					selector = input_text[changed_start:start]
					if selector.strip().startswith(","):
						selector = selector[1:].strip()
					result.append([selector, input_text[start + 1:end], input_text])
					changed_start = end + 1
					if self.find_text_between_brackets(input_text[start + 1:end]):
						temp = self.find_text_between_brackets(input_text[start + 1:end])
						result.append(temp)
					stack.pop()
					num_left = num_left - 1
					num_right = num_right - 1
		return result

	def float_range(self, start, end, step):
		"""
		실수형으로 가능한 range 형태
		"""
		value = start
		while value <= end:
			yield value
			value = step + value

	def get_all_doc_of_method_name_for_object(self, input_object):
		"""
		객체를 주면 메소드의 help를 돌려 주는것

		:param input_object:
		:return:
		"""
		result = {}
		for method_name in dir(input_object):
			temp = []
			# 이중언더 메소드는 제외시키는것
			if not method_name.startswith('__'):
				try:
					temp.append(method_name)
					temp.append(getattr(input_object, method_name).__doc__)
				except:
					pass
			result[method_name] = temp
		return result

	def get_all_excel_file_name_in_folder(self, directory="./"):
		result = self.get_all_filename_in_folder_by_extension_name(directory, ["xls", "xlsx", "xlsm", "xla"])
		return result


	def get_all_excel_filename_in_folder(self, directory="./"):
		result = self.get_filename_in_folder_by_extention_name(directory, [".xls", ".xlsx", ".xlsm", ".xla"])
		return result

	def get_all_file_information_in_folder(self, directory="./"):
		"""
		폴더안의 파일을 이름, 작성한날, 크기, 총경로를 리스트로 만들어서 주는것

		:param directory:
		:return:
		"""
		result = []
		all_files = os.scandir(directory)
		for one in all_files:
			info = one.stat()
			try:
				if one.is_dir():
					temp = self.get_all_filename_in_folder_with_all_properties(directory + "\\" + one.name)
					result.extend(temp)
				else:
					result.append([one.name, info.st_mtime, info.st_size, one.path])
			except:
				pass
		return result

	def get_all_file_information_in_folder_except_sub_folder(self, directory="./"):
		"""
		폴더안의 파일을 이름, 작성한날, 크기, 총경로를 리스트로 만들어서 주는것

		:param directory:
		:return:
		"""
		result = []
		all_files = os.scandir(directory)
		for one in all_files:
			info = one.stat()
			try:
				if one.is_dir():
					pass
				else:
					result.append([one.name, info.st_mtime, info.st_size, one.path])
			except:
				pass
		return result

	def get_all_file_information_in_folder_with_sub_folder_as_dic_style(self, directory="./"):
		"""
		같은 화일일때 삭제를 하기위하여 같은 화일을 찾아내는 것이다
		플더안의 파일을 이름, 작성한날, 크기, 총경로를 사전으로 만들어 주며,
		사전의 key 는 이름_작성한날_크기 의 형태로 만들고, 값은 [이름, 작성한날, 크기, 총경로]]으로  만든다
		만약 같은 key 를 발견하면 값에 추가를 한다

		:param directory:
		:return:
		"""
		result = {}
		all_files = os.scandir(directory)
		for one in all_files:
			info = one.stat()
			try:
				if one.is_dir():
					temp = self.get_all_file_information_in_folder_with_sub_folder_as_dic_style(directory + "/" + one.name)
					for one_key in temp.keys():
						if one_key in result.keys():
							result[one_key].append(temp[one_key])
						else:
							result[one_key] = [temp[one_key]]
				else:
					key_value = str(one.name) + "_" + str(info.st_mtime) + "" + str(info.st_size)
					one_value = [one.name, info.st_mtime, info.st_size, one.path]
					if key_value in result.keys():
						result[key_value].append(one_value)
					else:
						result[key_value] = [one_value]
			except:
				pass
		return result

	def get_all_file_n_folder_name_in_folder(self, directory):
		"""
		폴더 안의 화일을 읽어오는것

		:param directory:
		:return:
		"""
		result = []
		filenames = os.listdir(directory)
		for filename in filenames:
			full_filename = os.path.join(directory, filename)
			result.append(filename)
		return result

	def get_all_filename_in_folder(self, directory, option_full_filename=False):
		"""
		tree에서 폴더를 클릭하면 안의 화일을 읽어오는것

		:param directory:
		:return:
		"""
		result = []

		file_list = glob.glob(directory)

		filenames = os.listdir(directory)
		for filename in filenames:
			if option_full_filename:
				full_filename = os.path.join(directory, filename)
				result.append(full_filename)
			else:
				result.append(filename)
		return result

	def get_all_filename_in_folder_by_extension_name(self, directory="./", all_extension_name="pickle"):
		"""
		확장자이름으로 어떤 폴더안의 모든 화일이름을 갖고오는 것

		:param directory:
		:param filter:
		:return:
		"""
		result = []
		all_files = os.listdir(directory)
		if type(all_extension_name) != type([]):
			all_extension_name = [all_extension_name]

		for extension_name in all_extension_name:
			if extension_name == "*" or extension_name == "":
				extension_name = ""
				result = all_files
			else:
				extension_name = "." + extension_name
				for x in all_files:
					if x.endswith(extension_name):
						result.append(x)
		return result

	def get_all_filename_in_folder_by_first_underbar(self, input_folder):
		"""
		어떤 폴더안의 화일이름을 2단계의 메뉴로 만들어주는 코드
		화일이름을 기준으로 _로 나누어서 2단계의 메뉴을 만드는데 사용
		aaa_bbb_ccc => ["aaa", "bbb_ccc"]
		"""

		filenames = self.get_all_filename_in_folder(input_folder)
		result = {}

		for one_file in filenames:
			splited_filename = str(one_file).split("_")

			if len(splited_filename) == 1:
				result[splited_filename[0]] = ""
			else:
				result[one_file] = [splited_filename[0]], one_file[len(splited_filename[0]) + 1:]
		return result

	def get_all_filename_in_folder_save_as_pickle(self, directory="./", filter="pickle"):
		"""
		pickle로 만든 자료를 저장하는것
		"""
		result = []
		all_files = os.listdir(directory)
		if filter == "*" or filter == "":
			filter = ""
			result = all_files
		else:
			filter = "." + filter
			for x in all_files:
				if x.endswith(filter):
					result.append(x)
		return result

	def get_all_filename_in_folder_with_all_properties(self, directory="./"):
		"""
		폴더안의 파일을 이름, 작성한날, 크기, 총경로를 리스트로 만들어서 주는것

		:param directory:
		:return:
		"""
		result = []
		all_files = os.scandir(directory)
		for one in all_files:
			info = one.stat()
			try:
				if one.is_dir():
					#	print(directory+,,\\"+one.name)
					temp = self.get_all_filename_in_folder_with_all_properties(directory + "\\" + one.name)
					result.extend(temp)
				else:
					# result.append(one)
					result.append([one.name, info.st_mtime, info.st_size, one.path])
			except:
				pass
		return result

	def get_all_filename_in_folder_with_all_properties_except_sub_folder(self, directory="./"):
		"""
		폴더안의 파일을 이름, 작성한날, 크기, 총경로를 리스트로 만들어서 주는것

		:param directory:
		:return:
		"""
		result = []
		all_files = os.scandir(directory)
		for one in all_files:
			info = one.stat()
			try:
				if not one.is_dir():
					result.append([one.name, info.st_mtime, info.st_size, one.path])
			except:
				pass
		return result

	def get_all_filename_in_folder_with_sub_folder(self, input_path, filename):
		"""
		입력 폴더안의 서브폴더를 포함한 곳에서 화일을 경로및 수정일자를 포함해서 돌려주는것
		"""
		xytime = pynal.pynal()

		result = []
		for root, sub_folder, files in os.walk(input_path):
			for item in files:
				if filename == item:
					file_path = root + '/' + filename
					created = os.path.getctime(file_path)
					modified = os.path.getmtime(file_path)
					dt_obj = xytime.change_anytime_to_dt_obj(modified)
					aaa = xytime.change_dt_obj_to_ymd_list(dt_obj)

					result.append([filename, root, str(aaa[0]) + str(aaa[1]) + str(aaa[2])])
		return result

	def get_all_filename_n_folder_name_in_path(self, directory):
		"""
		폴더 안의 화일을 읽어오는것

		:param directory:
		:return:
		"""
		result = []
		filenames = os.listdir(directory)
		for filename in filenames:
			full_filename = os.path.join(directory, filename)
			result.append(filename)
		return result

	def get_all_folder_name_in_path(self, directory="./"):
		"""
		폴더안의 파일을 리스트로 만들어서 주는것
		"""
		result = []
		all_file_n_folder = os.scandir(directory)
		for one in all_file_n_folder:
			if one.is_dir():
				result.append(one.name)
		return result

	def get_all_mathod_name_n_source_code_for_object_as_dic(self, input_object):
		"""
		입력객체에 대해서, 메소드를 기준으로 소스코드를 읽어오는것

		:param input_object:
		"""
		result = {}
		method_object = ""
		for object_method in dir(input_object):
			if not object_method.startswith("_"):
				try:
					exec(f"method_object = {input_object}.{object_method}")
					ddd = inspect.getsource(method_object)
					result[object_method] = ddd
				except:
					pass
		return result

	def get_all_method_code_by_method_name(self, str_method_name):
		"""
		메소드의 코드를 읽어오는것
		문자로 넣을수있도록 만든 것이다

		:param str_method_name:
		:return:
		"""
		# method_name = eval(str_method_name)
		code_text = inspect.getsource(str_method_name)
		return code_text

	def get_all_method_name_for_object(self, input_object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다
		"""
		result = []
		for object_method in dir(input_object):
			result.append(object_method)
		return result

	def get_all_method_name_for_object_except_dunder_methods(self, input_object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다
		던더메소드는 제외시킨 것이다

		:param input_object:
		:return:
		"""
		result = []
		for object_method in dir(input_object):
			if object_method.startswith("__"):
				pass
			else:
				result.append(object_method)

		return result

	def get_all_method_name_for_object_except_dunder_methods_with_prefix(self, input_object, start_text):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다

		:param object:
		:return:
		"""
		# all_method_name = self.get_all_method_name_with_argument_for_object(input_object)
		# print(all_method_name)

		all_method_name1 = self.get_all_method_name_with_argument_for_object(input_object)
		# print(all_method_name1)

		result = []
		for obj_method in all_method_name1:
			# print(obj_method)
			if obj_method.startswith("__"):
				pass
			else:
				result.append(start_text + obj_method)
		return result

	def get_all_method_name_for_object_except_dunder_methods_with_prefix_as_dic(self, input_object, start_text):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다

		:param object:
		:return:
		"""

		all_method_name1 = self.get_all_method_name_n_argument_for_object_as_dic(input_object)

		result = []
		for obj_method in all_method_name1:
			if obj_method.startswith("__"):
				pass
			else:
				result.append(start_text + obj_method)
		return result

	def get_all_method_name_for_python_file(self, filename):
		"""
		py로만든 화일을 읽어서 def를 기준으로 분리하는 것

		:param filename:
		:return:
		"""
		file_pointer = open(filename, 'r', encoding='utf-8')
		result = {}
		filejist = file_pointer.readlines()
		key_value = "_aa_bb_cc_"
		temp = []
		for ori_value in filejist:
			one_value = str(ori_value).replace(" ", "")
			one_value = str(one_value).replace("\t", "")
			if one_value[0:3] == "def":
				# print(key_value)
				result[key_value] = temp
				temp = []
			key_value = "_aa_bb_cc_" + str(ori_value)
		else:
			temp.append(ori_value)
		result[key_value] = temp
		aaa = list(result.keys())
		aaa.sort()
		for one in aaa:
			update_one = one.replace("_aa_bb_cc_", "")
			update_one = update_one.replace("\n", "")
			# print(update_one)
			for one_1 in result[one]:
				one_1 = one_1.replace("\n", "")

	def get_all_method_name_n_argument_for_object_as_dic(self, object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다
		"""
		result = {}
		for obj_method in dir(object):
			try:
				method_data = inspect.signature(getattr(object, obj_method))
				dic_fun_var = {}
				if not obj_method.startswith("__"):
					for one in method_data.parameters:
						value_default = method_data.parameters[one].default
						value_data = str(method_data.parameters[one])
						if value_default == inspect._empty:
							dic_fun_var[value_data] = None
						else:
							value_key, value_value = value_data.split("=")
							dic_fun_var[value_key] = value_value
						result[obj_method] = dic_fun_var
			except:
				pass
		return result

	def get_all_method_name_n_argument_for_object_except_dunder_methods_as_dic(self, object):
		"""
		객체를 넣으면 객체의 메소드와 그 메소드의 parameter를 갖고오는 것

		:param object:
		:return:
		"""
		result = {}
		for one_method_name in dir(object):
			try:
				(sig, local_vars) = inspect.signature(getattr(object, one_method_name)), locals()
				if not one_method_name.startswith("_"):
					args = {}
					for a in sig.parameters.keys():
						args[a] = sig.parameters[a]
					result[one_method_name] = args
			except:
				pass
		return result

	def get_all_method_name_n_doc_for_object_as_dic(self, input_object):
		"""
		객체를 주면 메소드의 help를 돌려 주는것

		:param input_object:
		:return:
		"""
		result = {}
		for method_name in dir(input_object):
			temp = []
			# 이중언더 메소드는 제외시키는것
			if not method_name.startswith('__'):
				try:
					temp.append(method_name)
					temp.append(getattr(input_object, method_name).__doc__)
				except:
					pass
			result[method_name] = temp
		return result

	def get_all_method_name_with_argument_for_input_object(self, object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다
		{"메소드이름":{"변수1":"기본값1", "변수2":"기본값2".....}......}
		:param object:
		:return:
		"""
		result = {}
		for method_name in dir(object):
			try:
				method_data = inspect.signature(getattr(object, method_name))
				# (sheet_name='', xyxy='', value='입력필요')이런형태로 결과값이 넘어온다

				one_method_data = {}
				# __로 시작되는 던더메소드를 제외하는것
				if not method_name.startswith("_"):
					for one in method_data.parameters:

						# 인자의 기본값이 있는지를 확인하는 것
						para_name = one
						para_value = method_data.parameters[one].default

						# 기본값이 없으면 None으로 하고
						if para_value == inspect._empty:
							para_value = None
						else:
							if para_value == "''" or para_value == '""':
								para_value = ''
							# 변수값중 ''가 들어간것이 없어져서, 아래의 것을 주석처리를 함
							one_method_data[para_name] = para_value

				result[method_name] = one_method_data

			except:
				pass
		return result

	def get_all_method_name_with_argument_for_object(self, object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다
		{"메소드이름":{"변수1":"기본값1", "변수2":"기본값2".....}......}
		:param object:
		:return:
		"""
		result = {}
		for method_name in dir(object):
			try:
				method_data = inspect.signature(getattr(object, method_name))
				# (sheet_name='', xyxy='', value='입력필요')이런형태로 결과값이 넘어온다

				one_method_data = {}
				# __로 시작되는 던더메소드를 제외하는것
				if not method_name.startswith("_"):
					for one in method_data.parameters:

						# 인자의 기본값이 있는지를 확인하는 것
						para_name = one
						para_value = method_data.parameters[one].default

						# 기본값이 없으면 None으로 하고
						if para_value == inspect._empty:
							para_value = None
						else:
							if para_value == "''" or para_value == '""':
								para_value = ''
							# 변수값중 ''가 들어간것이 없어져서, 아래의 것을 주석처리를 함
							one_method_data[para_name] = para_value

				result[method_name] = one_method_data

			except:
				pass
		return result

	def get_all_method_name_with_argument_for_object_except_dunder_methods(self, object):
		# 객체를 넣으면 객체의 메소드와 그 메소드의 parameter를 갖고오는 것
		result = {}
		for one_method_name in dir(object):
			try:
				(sig, local_vars) = inspect.signature(getattr(object, one_method_name)), locals()
				if not one_method_name.startswith("_"):
					args = {}
					for a in sig.parameters.keys():
						args[a] = sig.parameters[a]
					result[one_method_name] = args
			except:
				pass
		return result

	def get_all_properties_for_object(self, object):
		"""
		원하는 객체를 넣으면, 객체의 함수와 각 함수의 인자를 사전형식으로 돌려준다

		:param object:
		"""
		result = []
		for att in dir(object):
			result.append(att)
		return result

	def get_all_properties_for_object_except_dunder_method(self, object):
		"""
		입력으로 들어오는 객체에 대해서 던더메소드를 제외하고 모든 속성을 찾는 것

		:param object:
		:return:
		"""
		result = []
		for i in inspect.getmembers(object):
			if not i[0].startswith('_'):
				if not inspect.ismethod(i[1]):
					result.append(i)
		return result

	def get_arguments_of_method_name_for_object(self, object, method_name):
		"""
		입력으로 들어오는 객체와 메소드를 기준으로 그 메소드의 인수를 갖고오는 것

		:param object:
		:param method_name:
		:return:
		"""
		result = inspect.signature(getattr(object, method_name))
		return result

	def get_biff_record(self):
		"""

		:return:
		"""
		height = self.height
		options = 0x00
		if self.bold:
			options |= 0x01
			self._weight = 0x02BC
		if self.italic:
			options |= 0x02
		if self.underline != self.UNDERLINE_NONE:
			options |= 0x04
		if self.struck_out:
			options |= 0x08
		if self.outline:
			options |= 0x010
		if self.shadow:
			options |= 0x020
		colour_index = self.colour_index
		weight = self._weight
		escapement = self.escapement
		underline = self.underline
		family = self.family
		charset = self.charset
		name = self.name

	def get_char_type_for_one_char(self, text):
		"""
		한글자의 글자 형태를 알아오는것

		:param text:
		:return:
		"""
		one_byte_data = text.encode("utf-8")
		value_sum = 0
		char_type = ""

		if str(text) in "0123456789":
			char_type = "숫자"

		compile_1 = re.compile("\d+")
		no = compile_1.findall(text)

		try:
			no_1 = int(one_byte_data[0])
			no_2 = int(one_byte_data[1])
			no_3 = int(one_byte_data[2])
			new_no_1 = (no_1 - 234) * 64 * 64
			new_no_2 = (no_2 - 128) * 64
			new_no_3 = (no_3 - 128)
			value_sum = new_no_1 + new_no_2 + new_no_3

			if value_sum >= -28367 and value_sum <= -28338:
				char_type = "ja_only"
			if value_sum >= -28337 and value_sum <= -28317:
				char_type = "mo_only"

		except:
			char_type = "no_han"
			# 이것은 영어나 숫자, 특수문자라는 뜻이다
			no_1 = one_byte_data
			no_2 = ""
			no_3 = ""
		# char_type : 글자의 형태, 숫자, 한글

		return [char_type, text]

	def get_cho_sung_for_korean(self, input_kor):
		"""
		초성의 글자만 갖고오는것

		:param input_kor:
		:return:
		"""
		result = []
		for one in input_kor:
			try:
				aa = self.change_korean_to_jamo(one)
				result.append(aa[0][0])
			except:
				pass
		return result

	def get_code_for_python_file(self, filename):
		"""
		입력으로 들어오는 화일의 코드를 갖고오는 것

		:param filename:
		:return:
		"""
		temp_list = []
		result = []
		f = open(filename, 'r', encoding='UTF8')
		lines = f.readlines()

		for line in lines:
			c_line = line.strip()
			c_line = c_line.replace("\n", "")
			if c_line and c_line[0:3] == "def" and temp_list != [] and c_line[-1] == ":":
				result.append(temp_list)
				temp_list = []
			temp_list.append(line)
		result.append(temp_list)
		f.close()
		return result

	def get_computer_name(self):
		"""
		win32api 를 사용하는 방법

		:return:
		"""
		print(win32api.GetComputerName())
		print(win32api.GetLocalTime())
		print(win32api.GetCursorPos())
		print(win32api.GetSystemDirectory())
		print(win32api.GetDiskFreeSpace())
		print(win32api.GetSystemFileCacheSize())
		print(win32api.GlobalMemoryStatus())
		print(win32api.GetSystemDirectory())
		print(win32api.GetSystemDirectory())
		print(win32api.GetSystemDirectory())
		print(win32api.GetSystemDirectory())

	def get_current_mouse_pxy(self):
		"""
		현재 마우스의 위치를 돌려조는 것

		다른방법
		xy = pyautogui.position()
		return (xy.x, xy.y)

		:return:
		"""
		# 현재 마우스의 위치를 읽어온다
		result = win32api.GetCursorPos()
		return result

	def get_current_path(self):
		"""
		현재의 경로를 돌려주는것
		"""
		result = os.getcwd()
		return result

	def get_cursor_pxy(self):
		"""
		커서의 위치를 갖고오는 것
		:return:
		"""
		pos = win32api.GetCursorPos()

	def get_data_type_for_input_data(self, input_data):
		return self.check_data_type_for_data(input_data)

	def get_degree_for_xy(self, xy):
		"""
		좌표를 주면, 좌표에대한 각도를 계산해 주는 것

		:param xy:
		:return:
		"""
		pi = 3.1415926535
		result = math.atan2(xy[1], xy[0]) * 180 / pi
		return result

	def get_diagonal_xy(self, xyxy=[5, 9, 12, 21]):
		"""
		좌표와 대각선의 방향을 입력받으면, 대각선에 해당하는 셀을 돌려주는것
		좌표를 낮은것 부터 정렬하기이한것 [3, 4, 1, 2] => [1, 2, 3, 4]
		"""
		result = []
		if xyxy[0] > xyxy[2]:
			x1, y1, x2, y2 = xyxy[2], xyxy[3], xyxy[0], xyxy[1]
		else:
			x1, y1, x2, y2 = xyxy

		x_height = abs(x2 - x1) + 1
		y_width = abs(y2 - y1) + 1
		step = x_height / y_width
		temp = 0

		if x1 <= x2 and y1 <= y2:
			# \형태의 대각선
			for y in range(1, y_width + 1):
				x = y * step
				if int(x) >= 1:
					final_x = int(x) + x1 - 1
					final_y = int(y) + y1 - 1
					if temp != final_x:
						result.append([final_x, final_y])
						temp = final_x
		else:
			for y in range(y_width, 0, -1):
				x = x_height - y * step

				final_x = int(x) + x1
				final_y = int(y) + y1 - y_width
				temp_no = int(x)

				if temp != final_x:
					temp = final_x
					result.append([final_x, final_y])
		return result

	def get_differnet_key_n_value_in_two_dic(self, mother_dic, child_dic):
		"""
		두 사전의 내용중에서 다른것을

		:param mother_dic:
		:param child_dic:
		:return:
		"""
		mother_keys_list = mother_dic.keys()
		child_keys_list = child_dic.keys0
		result_unique_key = []
		result_same_key_differ_value = []
		for one_key in mother_keys_list:
			if one_key in child_keys_list:
				if mother_dic[one_key] == child_dic[one_key]:
					pass
				else:
					result_same_key_differ_value.append(one_key)
			else:
				result_unique_key.append(one_key)
		return [result_unique_key, result_same_key_differ_value]

	def get_directory_portion_only_from_filename(self, input_file=""):
		"""
		입력으로 들어온 화일의 총 이름에서 디렉토리 부분만 추출하는 것
		:param input_file:
		:return:
		"""
		drive, path_and_file = os.path.splitdrive(input_file)
		path, file = os.path.split(input_file)
		result = [path, file]
		return result

	def get_doc_for_method_name_with_object(self, object, method_name):
		"""

		:param object:
		:param method_name:
		:return:
		"""

		try:
			result = getattr(object, method_name).__doc__
		except:
			result = ""

		return result

	def get_encoding_type_in_system(self, ):
		"""
		기본적인 시스템에서의 인코딩을 읽어온다
		#print("시스템의 기본적인 입력시의 인코딩 ====> ", system_in_basic_incoding)
		#print("시스템의 기본적인 출력시의 인코딩 ====> ", system_out_basic_incoding)
		"""
		system_in_basic_incoding = sys.stdin.encoding
		system_out_basic_incoding = sys.stdout.encoding

	def get_eng_vs_num_for_input_text(self, data):
		"""
		단어중에 나와있는 숫자, 영어를 분리하는기능

		:param data:
		:return:
		"""
		re_compile = re.compile(r"([a-zA-Z]+)([0-9]+)")
		result = re_compile.findall(data)
		new_result = []
		for dim1_data in result:
			for dim2_data in dim1_data:
				new_result.append(dim2_data)
		return new_result

	def get_eng_vs_num_in_text(self, data):
		"""
		단어중에 나와있는 숫자, 영어를 분리하는기능

		:param data:
		:return:
		"""
		re_compile = re.compile(r"([a-zA-Z]+)([0-9]+)")
		result = re_compile.findall(data)
		new_result = []
		for dim1_data in result:
			for dim2_data in dim1_data:
				new_result.append(dim2_data)
		return new_result

	def get_file_as_2_types(self, file_full_name):
		"""
		입력으로 들어오는 화일이름을 기준으로 2가지 형태로 돌려주는 것
		1. 모든 줄을 리스트형태로 돌려주는 것
		2. 일반 텍스트로 읽어오는 것

		:param file_full_name:
		:return:
		"""
		file_object = open(file_full_name, "r", encoding="UTF-8")
		file_as_list = file_object.readlines()
		file_object.close()
		one_file = ""
		for one in file_as_list:
			one_file = one_file + one
		return [file_as_list, one_file]

	def get_file_as_list_1d(self, file_full_name):
		"""
		화일을 리스트형태와 text형태로 2개로 돌려준다

		:param file_full_name:
		:return:
		"""
		file_object = open(file_full_name, "r", encoding="UTF-8")
		file_as_list = file_object.readlines()
		file_object.close()
		return file_as_list

	def get_file_as_two_types(self, file_full_name):
		"""

		:param file_full_name:
		:return:
		"""
		file_object = open(file_full_name, "r", encoding="UTF-8")
		file_as_list = file_object.readlines()
		file_object.close()
		one_file = ""
		for one in file_as_list:
			one_file = one_file + one
		return [file_as_list, one_file]

	def get_file_for_filename(self, filename):
		"""
		화일을 읽어오는 것

		:param filename:
		:return:
		"""
		try:
			f = open(filename, 'r', encoding='UTF-8')
			result = f.readlines()
			f.close()
		except:
			f = open(filename, 'r')
			result = f.readlines()
			f.close()
		return result

	def get_filename_in_folder_by_extention_name(self, directory="./", extention_name_list_1d=[".xls", ".xlsx", ".xlsm", ".xla"]):
		all_files = self.get_all_filename_in_folder(directory)
		result = []
		for one_file in all_files:
			if one_file.endswith(tuple(extention_name_list_1d)):
				result.append(os.path.join(directory, one_file))
		return result

	def get_folder_name_in_path_as_dic_type(self, path):
		"""
		결로를 입력하면, 그결로안의 폴더이름들을 사전형식으로 돌려주는 것

		:param path:
		:return:
		"""
		folder_dict = {}
		for item in os.listdir(path):
			item_path = os.path.join(path, item)
			if os.path.isdir(item_path):
				# 보안때문에 접근이 거부된 화일들을 읽으려할때 어러나는것을 방지하기 위해
				try:
					folder_dict[item] = self.folder_to_dict(item_path)
				except:
					pass
			else:
				folder_dict[item] = None
		return folder_dict

	def get_font_list_for_window(self):
		"""
		윈도우에서 설치된 font리스트를 갖고온다

		:return:
		"""
		font_names = []
		hdc = win32gui.GetDC(None)
		win32gui.EnumFontFamilies(hdc, None, self.callback, font_names)
		# print("\n".join(font_names))
		win32gui.ReleaseDC(hdc, None)
		return font_names

	def get_information_for_folder(self, path):
		"""
		폴더안의 크기를 돌려주는 것

		:param path:
		:return:
		"""
		total_size = 0
		for dirpath, dirnames, filenames in os.walk(path):
			for f in filenames:
				fp = os.path.join(dirpath, f)
				total_size += os.path.getsize(fp)
			return total_size

	def get_information_for_input_object(self, obj, level=0, max_level=2):
		# 입력으로오는 객체의 속성, 함수, 클래스 이름을 갖고오는 것
		if level > max_level:
			return
		indent = "     " * level
		print(f" {indent}{obj.__class__, __name__}:")

		# dir0 함수를 사용하여 객체의 속성과 메서드를 나열

		attributes = dir(obj)
		for attr in attributes:
			if not attr.startswith("_"):
				try:
					sub_obj = getattr(obj, attr)
					if inspect.ismethod(sub_obj) or inspect.isfunction(sub_obj):
						print(f"{indent}  Method: {attr}()")
					elif inspect.isclass(sub_obj):
						print(f"{indent} Class: {attr}")
						self.get_information_for_input_object(sub_obj, level + 1, max_level)
					else:
						print(f"{indent} Attribute: {attr}")
				except Exception as e:
					print(f"{indent} {attr} (Error: (e])")

	def get_key_for_dic_as_min_len_value(self, input_dic, except_key=[]):
		"""
		갯수가 제일 적은 것을 찾는 것
		입력된 사전을 기준으로 사전의 키가 except_key는 제외하고,
		사전의 value에서 가장 작은 갯수의 key를 찾는 것이다

		:param input_dic:
		:param except_key:
		:return:
		"""
		selected_key = ""
		temp_count = 999
		for key_value in input_dic.keys():
			if not key_value in except_key:
				if len(input_dic[key_value]) < temp_count:
					temp_count = len(input_dic[key_value])
					selected_key = key_value
		return selected_key

	def get_list_1d_with_float_range(self, start, end, step):
		"""
		실수형으로 가능한 range 형태

		:param start:
		:param end:
		:param step:
		:return:
		"""
		result = []
		value = start
		while value <= end:
			yield value
			value = step + value
			result.append(value)
		return result

	def get_max_len_for_list_2d(self, list_2d_data):
		"""
		2차원 배열의 제일 큰 갯수를 확인한다
		#an_array = [[1, 2], [3, 4, 5]]
		#print("2차배열 요소의 최대 갯수는 ==>", check_list_maxsize(an_array))
		"""
		max_length = max(len(row) for row in list_2d_data)
		return max_length

	def get_method_code(self, str_method_name):
		"""
		메소드의 코드를 읽어오는것
		문자로 넣을수있도록 만든 것이다

		:param str_method_name:
		:return:
		"""

		method_name = eval(str_method_name)
		code_text = inspect.getsource(method_name)
		return code_text

	def get_monitor_size(self):
		"""모니터의 해상도를 읽어오는 것"""
		result = pyautogui.size()
		return result



	def get_nos_in_list_2d_by_same_xline(self, input_2dlist=""):
		"""
		2dlist의 자료의 형태로 된것중에서
		위에서 부터 같은것을 삭제 한다
		0,3,5의 3개가 같은것이라면 제일 앞의 1개는 제외하고 [3,5]를 돌려준다
		"""

		all_datas = input_2dlist
		total_len = len(all_datas)
		same_nos = []
		for no in range(total_len):
			if no in same_nos:
				pass
			else:
				one_list = all_datas[no]
				# print(one_list)
				for num in range(no + 1, total_len):
					if num in same_nos:
						pass
					else:
						if one_list == all_datas[num]:
							same_nos.append(num)
		return same_nos

	def get_not_empty_value_in_list_2d_by_index(self, input_list_2d, index_no=4):
		"""
		index 번호의 Y열의 값이 빈것이 아닌것만 돌려주는 것

		:param input_list_2d:
		:param index_no:
		:return:
		"""
		result = []
		for index, one in enumerate(input_list_2d):
			if one[index_no]:
				result.append(one)
		return result

	def get_one_line_having_input_word_in_file(self, filename="pcell.py", input_text="menu_dic["):
		"""
		화일안에서 원하는 단어가 들어간 줄을 리스트로 만들어서 돌려주는것
		메뉴를 만들 목적으로 한것

		:param filename:
		:param input_text:
		:return:
		"""
		aa = open(filename, 'r', encoding="UTF-8")
		result = []
		for one in aa.readlines():
			if input_text in str(one).strip():
				# print(str(one).strip())
				result.append(str(one).strip())
		return result

	def get_parameter_datas_for_method_name_in_object(self, input_object, input_method_name):
		"""
		입력으로 드어오는 객체의 메소드에 대하여 파라미터들의 정보를 돌려주는 것
		출력형태 : [사전형의 기본자료형식, ==> {sheet_name:'',xyxy: [1, 1, 7, 7], xy: [3, 3])}
			       문자열의 입력변수형태,  ==> "(sheet_name='', xyxy=[1, 1, 7, 7], xy=[3, 3])"
			       사전형의 자료         ==>  {sheet_name:"sheet_name = ''",xyxy: "xyxy = [1, 1, 7, 7]", xy: "xy=[3, 3]")}
			       ]
		"""
		result = []
		dic_param_vs_default_value = {}
		meta_data = getattr(input_object, input_method_name)

		# result.append(ddd)
		basic_method_data = inspect.signature(meta_data)
		for one in basic_method_data.parameters:
			parameter_name = basic_method_data.parameters[one].name
			parameter_defalt_value = basic_method_data.parameters[one].default
			if parameter_defalt_value == inspect._empty:
				parameter_defalt_value = None
			dic_param_vs_default_value[parameter_name] = parameter_defalt_value
		result.append(dic_param_vs_default_value)
		result.append(str(basic_method_data))
		result.append(basic_method_data.parameters)
		result.append(meta_data.__doc__)

		return result

	def get_pickle_filenames_in_folder(self, directory="./", filter="pickle"):
		"""
		pickle로 만든 자료를 저장하는것
		"""
		result = []
		all_files = os.listdir(directory)
		if filter == "*" or filter == "":
			filter = ""
			result = all_files
		else:
			filter = "." + filter
			for x in all_files:
				if x.endswith(filter):
					result.append(x)
		return result

	def get_random_number(self, digit=2, total_no=1):
		"""
		입력으로들어오는 것을 랜덤하여 갯수만큼 자료를 만드는것

		:param digit:
		:param total_no:
		:return:
		"""
		result = []
		for no in range(total_no):
			temp = ""
			for one in range(digit):
				number = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
				temp = temp + str(number)
			result.append(temp)
		return result

	def get_same_value_for_list_2d_by_index_list(self, input_lisd2d_1, input_lisd2d_2, index_list=[1, 2]):
		"""
		2 차원의 자료들이 서로 같은것을 삭제하는 것인데,
		모두 같은것이 아니고, 일부분이 같은것을
		골라내는 기능을 만든 것이다

		:param input_lisd2d_1:
		:param input_lisd2d_2:
		:param index_list:
		:return:
		"""
		semi_result_1 = {}
		for num, value in enumerate(input_lisd2d_1):
			temp_1 = []
			for one in index_list:
				temp_1.append(value[one])
				semi_result_1[num] = [temp_1, value]
		semi_result_2 = {}
		for num, value in enumerate(input_lisd2d_2):
			temp_2 = []
			for one in index_list:
				temp_2.append(value[one])
				semi_result_2[num] = [temp_2, value]
		result = []
		for key, value in semi_result_1.items():
			for key2, value2 in semi_result_2.items():
				if value[0] == value2[0]:
					if value[1] in result:
						pass
					else:
						result.append(value[1])
		return list(result)

	def get_serial_list_for_eng(self, start_serial, count):
		"""
		입력한 영문글자를 원하는 갯수만큼 증가시킨것을 리스트로 돌려주는 것

		:param start_serial:
		:param count:
		:return:
		"""
		result = []
		current_serial = start_serial
		for _ in range(count):
			result.append(current_serial)
			current_serial = self.increment_serial(current_serial)
		return result

	def get_serial_no_in_text(self, input_data, input_list):
		"""

		:param input_data:
		:param input_list:
		:return:
		"""
		result = []
		total_len = 0
		start_no = 0
		for no in range(len(input_list)):
			if no != 0:
				start_no = total_len
			end_len = input_list[no]
			result.append(input_data[start_no:start_no + end_len])
			total_len = total_len + end_len
		return result

	def get_similar_word_in_list_1d_with_input_value(self, basic_list, input_value):
		"""
		앞에서부터 가장 많이 같은 글자가 있는 자료를 돌려준다

		:param basic_list:
		:param input_value:
		:return:
		"""
		result_no = 0
		result_value = ""
		# 공백이 없도록 만든다, 가끔 공백을 2개를 넣거나 하는경우가 있어서 넣은것이다
		checked_value = str(input_value).replace(" ", "")
		# 비교할것중에 작은것을 기준으로 한글짜식 비교하기 위해 길이를 계산한것
		a_len = len(input_value)

		# 폴더의 자료를 하나씩 돌려서 비교한다
		for one_word in basic_list:
			temp_no = 0
			# 공백이 없도록 만든다, 가끔 공백을 2개를 넣거나 하는경우가 있어서 넣은것이다
			checked_one_word = str(one_word).replace(" ", "")
			b_len = len(checked_one_word)
			min_len = min(a_len, b_len)

			# 길이만큼 하나씩 비교를 한다
			for index in range(min_len):
				# 만약 위치마다 한글짜식 비교해서 계속 같은것이 나오면 갯수를 더한다
				if checked_value[index] == checked_one_word[index]:
					temp_no = temp_no + 1
				else:
					# 만약 다른 글자가 나타나면, 제일 긴것인지를 확인한후, 다음 단어로 넘어가도록 한다
					if temp_no > result_no:
						result_no = temp_no
						result_value = one_word
					# print("앞에서부터 같은 갯수 ==> ", temp_no, checked_one_word)
					break
		return result_value

	def get_similarity_for_2_word(self, a, b):
		"""
		두개의 유사도를 측정
		:return:
		"""
		return difflib.SequenceMatcher(None, a, b).ratio()

	def get_size_for_list_2d(self, input_list_2d):
		"""
		입력값으로 온것의 크기를 돌려주는것

		:param input_list_2d:
		:return:
		"""
		len_x = len(input_list_2d)
		len_y = len(input_list_2d[0])
		return [len_x, len_y]

	def get_unique_col_name_compare_table_col_name(self, table_name, data2):
		"""
		고유한 컬럼만 골라낸다

		:param table_name:
		:param data2:
		:return:
		"""
		result = []
		columns = self.get_all_filename_in_folder(table_name)
		update_data2 = self.delete_special_char_in_text_except_num_n_eng(data2)
		for temp_3 in update_data2:
			if not temp_3.lower() in columns:
				result.append(temp_3)
		return result

	def get_unique_data_in_list_1d(self, input_data):
		"""
		리스트의 값중 고유한것만 골라내기

		:param input_data:
		:return:
		"""
		temp = set()
		for one in input_data:
			temp.add(one)
		result = list(temp)
		return result

	def get_unique_element_between_two_list_1d(self, list_1d_a, list_1d_b):
		"""
		두개 리스트중에서，앞과 동일한것만 삭제하기 위한 것
		앞의 리스트에서 뒤에 갈은것만 삭제하는것
		예 : [1,2,3,4,5] - [3,4,5,6,7] ==> [1,2]
		"""
		result = [x for x in list_1d_a if x not in list_1d_b]
		return result

	def get_unique_method_name_between_two_python_file(self, file_a, file_b):
		"""
		두 파이썬 화일중에서 다른 함수만 갖고오는것

		:param file_a:
		:param file_b:
		:return:
		"""
		a_file = self.sort_python_file_by_def(file_a)
		b_file = self.sort_python_file_by_def(file_b)
		a_file_keys = a_file.keys()
		b_file_keys = b_file.keys()
		unique_a = []
		for one_key in a_file_keys:
			if not one_key in b_file_keys:
				unique_a.append([a_file_keys])
		return unique_a

	def get_unique_value_for_list_2d(self, input_list_2d):
		"""
		입력으로 들어온 자료들을 단어별로 구분하기위해서 만든것이며
		/,&-등의 문자는 없앨려고 하는것이다
		"""

		list_1d = []
		for one in input_list_2d:
			list_1d.extend(one)
		temp_result = []
		for one in list_1d:
			one = str(one).lower()
			one = one.replace("/", " ")
			one = one.replace(",", " ")
			one = one.replace("&", " ")
			one = one.replace("-", " ")
			temp_result.extend(one.split(" "))
		result = list(set(temp_result))
		return result

	def get_window_font_list(self):
		"""
		윈도우에서 설치된 font리스트를 갖고온다

		:return:
		"""
		result = []
		hdc = win32gui.GetDC(None)
		win32gui.EnumFontFamilies(hdc, None, self.callback, result)
		win32gui.ReleaseDC(hdc, None)
		return result

	def get_xy_for_nth_label_printing(self, serial_no, start_xy, size_xy, y_line):
		"""
		한줄의 자료를 라벨로 만드는 경우를 생각할때, 몇번째 자료가 어디부분에서 시작이 되는지를 계산하는 것
		n번째 프린트하는 자료의 시작점을 돌려주는 것이다

		:param serial_no: 몇번째로 출력될 것인지를 아는 것
		:param start_xy: 1번째의 자료가 시작되는 부분
		:param size_xy: 한줄의 자료가 출력되는 크기
		:param y_line: 한페이지에 몇줄로 출력할지를 설정하는 것
		:return:
		"""
		mok, namuji = divmod(serial_no, y_line)
		new_start_x = start_xy[0] + mok * size_xy[0]
		new_start_y = start_xy[1] + namuji * size_xy[1]
		return [new_start_x, new_start_y]

	def get_xy_list_for_moum_on_base_size(self, size=[1, 2], input_data="ㅏ"):
		"""
		모음을 엑셀에 나타내기 위한 좌표를 주는 것이다
		x, y는 글자의 크기

		:param size:
		:param input_data:
		:return:
		"""
		x, y = size
		mo_01 = [["ㅏ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.8 * y]]
		mo_02 = [["ㅑ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.8 * y],
				 [0.6 * x, 0.6 * y, 0.6 * x, 0.8 * y]]
		mo_03 = [["ㅓ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y]]
		mo_04 = [["ㅕ"], [1, 0.6 * y, x, 0.6 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y],
				 [0.6 * x, 0.4 * y, 0.6 * x, 0.6 * y]]
		mo_10 = [["ㅣ"], [1, 0.6 * y, x, 0.6 * y]]
		mo_05 = [["ㅗ"], [x, 1, x, y],
				 [x, 0.5 * y, 0.8 * x, 0.5 * y]]
		mo_06 = [["ㅛ"], [x, 1, x, y],
				 [x, 0.3 * y, 0.8 * x, 0.3 * y],
				 [x, 0.7 * y, 0.8 * x, 0.7 * y]]
		mo_07 = [["ㅜ"], [1, 1, 1, y],
				 [1, 0.5 * y, 0.5 * x, 0.5 * y]]
		mo_08 = [["ㅠ"], [1, 1, 1, y],
				 [1, 0.3 * y, 0.8 * x, 0.3 * y],
				 [1, 0.7 * y, 0.8 * x, 0.7 * y]]
		mo_09 = [["ㅡ"], [0.5 * x, 1, 0.5 * x, y]]

		mo_21 = [["ㅐ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.8 * y]]
		mo_22 = [["ㅒ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.6 * y, 0.4 * x, 0.6 * y],
				 [0.6 * x, 0.8 * y, 0.6 * x, 0.8 * y]]
		mo_23 = [["ㅔ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y]]
		mo_24 = [["ㅖ"], [1, 0.6 * y, x, 0.6 * y],
				 [1, 0.8 * y, x, 0.8 * y],
				 [0.4 * x, 0.4 * y, 0.4 * x, 0.6 * y],
				 [0.6 * x, 0.4 * y, 0.6 * x, 0.6 * y]]

		jamo2_dic = {
			"ㅏ": mo_01, "ㅑ": mo_02, "ㅓ": mo_03, "ㅕ": mo_04, "ㅗ": mo_05,
			"ㅛ": mo_06, "ㅜ": mo_07, "ㅠ": mo_08, "ㅡ": mo_09, "ㅣ": mo_10,
			"ㅐ": mo_21, "ㅒ": mo_22, "ㅔ": mo_23, "ㅖ": mo_24,
		}
		result = jamo2_dic[input_data]
		return result

	def get_xy_size_for_list_2d(self, input_list_2d):
		"""
		입력값으로 온것의 크기를 돌려주는것

		:param input_list_2d: 2차원 형태의 리스트
		:return:
		"""
		len_x = len(input_list_2d)
		len_y = len(input_list_2d[0])
		return [len_x, len_y]

	def group_list_2d_by_index(self, input_list_2d, index_no=4):
		"""
		index번호를 기준으로 그룹화를 만드는 것

		:param input_list_2d:
		:param index_no:
		:return:
		"""
		result = []
		# print(input_list_2d)

		sorted_input_list_2d = self.sort_list_2d_by_index(input_list_2d, index_no)
		# print(sorted_input_list_2d)

		check_value = sorted_input_list_2d[0][index_no]
		temp = []
		for one_list in sorted_input_list_2d:
			if one_list[index_no] == check_value:
				temp.append(one_list)
			else:
				result.append(temp)
				temp = [one_list]

				check_value = one_list[index_no]
		if temp:
			result.append(temp)
		return result

	def group_list_3d_by_index(self, input_list_3d, index_no=4):
		"""
		3차원의 자료를 2차원기준으로 index_no만큼씩 그룹화 하는것

		:param input_list_3d:
		:param index_no:
		:return:
		"""
		result = []
		for input_list_2d in input_list_3d:
			sorted_input_list_2d = self.sort_list_2d_by_index(input_list_2d, index_no)
			grouped_list_3d = self.group_list_2d_by_index(sorted_input_list_2d, index_no)
			result = result + grouped_list_3d
		return result

	def increment_serial(self, serial):
		"""
		입력으로 들어오는 영문자를 1단계 높은 글자로 바꿔주는 것

		:param serial:
		:return:
		"""
		serial_list = list(serial)
		length = len(serial_list)
		for i in range(length - 1, -1, -1):
			if serial_list[i] == 'Z':
				serial_list[i] = 'A'
			else:
				serial_list[i] = chr(ord(serial_list[i]) + 1)
				break
		return ''.join(serial_list)

	def insert_data_for_list_1d_by_index(self, data, num=1, input_data=[]):
		"""
		리스트에 일정한 간격으로 자료삽입

		:param data:
		:param num:
		:param input_data:
		:return:
		"""
		total_num = len(data)
		dd = 0
		for a in range(len(data)):
			if a % num == 0 and a != 0:
				if total_num != a:
					data.insert(dd, input_data)
					dd = dd + 1
			dd = dd + 1
		return data

	def insert_dic_db_1d(self, i_dic, i_key=[1, 2, 3], value=""):
		"""
		아래와같은 1차원의 형태로 가능한 database를 만들어 보자
		만약 만약 1,2,3이 있다고 가정하면, 1,2,3보다 큰 모든 값을 +1하여야 한다

		:param i_dic:
		:param i_key:
		:param value:
		:return:
		"""
		len_a = len(i_key)
		checked_i_key = list(i_key)
		for one_key in i_dic.keys():
			if list(one_key)[0:len_a] == checked_i_key:
				del i_dic[one_key]

	def insert_input_data_in_list_1d_by_step(self, input_list, insert_value, step):
		"""
		기존자료에 n번째마다 자료를 추가하는 기능
		raw_data = ['qweqw','qweqweqw','rterert','gdgdfgd',23,534534,'박상진']
		added_data = "new_data"
		step=3, 각 3번째 마다 자료를 추가한다면
		"""
		var_1, var_2 = divmod(len(input_list), int(step))
		for num in range(var_1, 0, -1):
			input_list.insert(num * int(step) - var_2 + 1, insert_value)
		return input_list

	def insert_into_3d_dict(self, main_dic, input_key_list, value):
		"""

		:param main_dic:
		:param input_key_list:
		:param value:
		:return:
		"""
		current_level = main_dic
		for key in input_key_list[:-1]:
			if key not in current_level:
				current_level[key] = {}
			current_level = current_level[key]

		# 마지막 키에 값을 삽입
		last_key = input_key_list[-1]
		current_level[last_key] = value
		return main_dic

	def insert_line_in_list(self, data, num=1, input_data=[]):
		"""
		리스트에 일정한 간격으로 자료삽입

		:param data:
		:param num:
		:param input_data:
		:return:
		"""
		total_num = len(data)
		dd = 0
		for a in range(len(data)):
			if a % num == 0 and a != 0:
				if total_num != a:
					data.insert(dd, input_data)
					dd = dd + 1
			dd = dd + 1
		return data

	def insert_serial_value_at_begin_for_list_2d(self, input_list_2d, start_no=1, special_char=""):
		"""
		엑셀의 제일 앞세로열에 특이한 번호를 넣고싶은 경우가 있다
		이때, 사용하기 위한 목적으로 만들었다.

		2 차원값의 값의 제일 처음값에만 순서가있는 값을 넣기
		값의 맨앞에 1), 2), 3)과같은 순서의 값을 넣고 싶을때

		:param input_list_2d: 2차원 형태의 리스트
		:param start_no:
		:param special_char:
		:return:
		"""
		for x in range(len(input_list_2d)):
			if not start_no == "":
				add_value = str(start_no + x) + special_char
			else:
				add_value = special_char
			input_list_2d[x][0] = add_value + input_list_2d[x][0]
		return input_list_2d

	def insert_text_nth_position(self, main_text, input_no, input_text):
		"""
		문자의 n번째에 우리가 원하는 문자를 집어 넣는 것
		:param main_text:
		:param input_no:
		:param input_text:
		:return:
		"""
		if len(main_text) > input_no:
			result = str(main_text)[:input_no] + input_text + str(main_text)[input_no:]
		else:
			result = main_text
		return result

	def insert_value_1000comma(self, input_num):
		"""
		입력된 숫자를 1000단위로 콤마를 넣는것
		"""
		temp = str(input_num).split(".")
		total_len = len(temp[0])
		result = ""
		for num in range(total_len):
			one_num = temp[0][- num - 1]
			if num % 3 == 2:
				result = "," + one_num + result
			else:
				result = one_num + result
		if len(temp) > 1:
			result = result + "." + str(temp[1])
		return result

	def insert_value_a_each_list_1d_for_list_2d_by_index_list(self, input_list_2d, index_list, input_value=""):
		"""
		입력형태 : 2차원리스트, [2,5,7]

		:param input_list_2d:
		:param no_list:
		:return:
		"""
		index_list.sort()
		index_list.reverse()
		for one in index_list:
			for x in range(len(input_list_2d)):
				input_list_2d[x].insert(int(one), input_value)
		return input_list_2d

	def insert_value_for_list_1d_by_step(self, input_datas, num=1, input_data=[]):
		"""
		입력으로 온 리스트자료의 n번째마다 값을 넣는 것

		:param input_datas:
		:param num:
		:param input_data:
		:return:
		"""
		total_num = len(input_datas)
		dd = 0
		for a in range(len(input_datas)):
			if a % num == 0 and a != 0:
				if total_num != a:
					input_datas.insert(dd, input_data)
					dd = dd + 1
			dd = dd + 1
		return input_datas

	def is_file_in_folder(self, path, filename):
		"""
		입력폴더안의 화일인가?

		:param path: path
		:param filename: filename
		:return:
		"""
		result = ""
		if path == "":
			path = "C:/Users/Administrator/Documents"
		filename_all = self.get_all_filename_in_folder(path)
		if filename in filename_all:
			result = True
		return result

	def is_num_only(self, input_text):
		"""
		소슷점까지는 포함한것이다

		:param input_text:
		:return:
		"""
		result = False
		temp = re.match("^[0-9.]+$", input_text)
		if temp: result = True

		return result

	def is_number(self, input_data):
		"""
		들어온 자료가 맞는지 확인하는것

		:param input_data:
		:return:
		"""
		temp = self.is_number_only(input_data)
		if temp:
			result = True
		else:
			result = False
		return result

	def is_number_only(self, input_text):
		"""
		소슷점까지는 포함한것이다

		:param input_text:
		:return:
		"""
		result = False
		temp = re.match("^[0-9.]+$", input_text)
		if temp: result = True

		return result

	def is_title_names(self, input_list):
		"""
		입력으로 들어온 1 차원 리스트자료가 컬럼이름으로 사용되는것인지 아닌지 확인하는것

		:param input_list:
		:return:
		"""
		result = 1
		result_empty = 0
		result_date_int = 0
		for one_value in input_list:
			if one_value == None or one_value == "":
				result_empty = result_empty + 1
			if type(one_value) == type(1):
				result_date_int = result_date_int + 1
			if result_empty > 0 or result_date_int > 0:
				result = 0
		return result

	def list_compare_two_value(self, raw_data, req_num, project_name, vendor_name, nal):
		"""
		위아래 비교
		회사에서 사용하는 inq용 화일은 두줄로 구성이 된다
		한줄은 client가 요청한 스팩이며
		나머지 한줄은 vendor가 deviation사항으로 만든 스팩이다
		이두가지의 스팩을 하나로 만드는 것이다
		즉, 두줄에서 아래의 글씨가 있고 그것이 0, None가 아니면 위의것과 치환되는 것이다
		그런후 이위의 자료들만 따로 모아서 돌려주는 것이다
		"""
		self.data = list(raw_data)
		self.data_set = []
		self.data_set_final = []

		for self.a in range(0, len(self.data), 2):
			for self.b in range(len(self.data[1])):
				if not (self.data[self.a + 1][self.b] == self.data[self.a][self.b]) and self.data[self.a + 1][
					self.b] != None and self.data[self.a + 1][self.b] != 0:
					self.data_set.append(self.data[self.a + 1][self.b])
				else:
					self.data_set.append(self.data[self.a][self.b])
			self.data_set.append(req_num)
			self.data_set.append(project_name)
			self.data_set.append(vendor_name)
			self.data_set.append(nal)
			self.data_set_final.append(self.data_set)
			self.data_set = []
		return self.data_set_final

	def list_sum(self, input_list):
		"""
		넘어온 여러줄의 리스트자료를 기준으로
		각 y행마다 자료가 있는지 확인해서,
		최대한 자료가 많이 들어가도록 각 x 라인을 채워서 한줄을 만든다

		:param input_list:
		:return:
		"""
		result = []
		x_no = len(input_list)
		y_no = len(input_list[0])
		for y in range(y_no):
			temp = ""
			for x in range(x_no):
				one_value = input_list[x][y]
				if one_value != "" and one_value != None:
					temp = one_value
			result.append(temp)
		# print(result)
		return result

	def make_2_digit(self, input_data):
		"""
		0을 포함한 2자리숫자로 원하는 리스트를 만들어주는 것

		:param input_data:
		:return:
		"""
		input_data = str(input_data)
		if len(input_data) == 1:
			result = "0" + input_data
		else:
			result = input_data
		return result

	def make_3_menu_for_folder(self, input_folder):
		"""
		어떤 폴더안의 화일이름을 3단계의 메뉴로 만들어주는 코드
		"""
		all_filenames = self.get_all_filename_in_folder(input_folder)
		result = {}

		for one_filename in all_filenames:
			splited_filename = str(one_filename).split("_")
			count_x = len(splited_filename)
			temp = []
			len_x = 0
			if count_x == 1:
				len_x = len(splited_filename[0])
				temp.append(splited_filename[0])
				temp.append("")
				temp.append("")
			elif count_x == 2:
				len_x = len(splited_filename[0]) + len(splited_filename[1])
				temp.append(splited_filename[0])
				temp.append(splited_filename[1])
				temp.append("")
			elif count_x > 2:
				len_x = len(splited_filename[0]) + len(splited_filename[1])
				temp.append(splited_filename[0])
				temp.append(splited_filename[1])
				temp.append(one_filename[len_x + 2:])

			for index, one in enumerate(temp):
				if not temp[0] in list(result.keys()):
					result[temp[0]] = {}

				if not temp[1] in list(result[temp[0]].keys()):
					result[temp[0]][temp[1]] = {}

				if not temp[2] in list(result[temp[0]][temp[1]].keys()):
					result[temp[0]][temp[1]][temp[2]] = ""
		return result

	def make_3_menu_for_folder_ver2(self, input_folder):
		""" 어떤폴더안의 화일이름을 3단계의 메뉴로 만들어주는 코드"""
		all_filenames = self.get_all_filename_in_folder(input_folder)
		result = {}

		for one_filename in all_filenames:
			splited_filename = str(one_filename).split("_")
			count_x = len(splited_filename)
			temp = []
			len_x = 0
			if count_x == 1:
				len_x = len(splited_filename[0])
				temp.append(splited_filename[0])
				temp.append("")
				temp.append("")
			elif count_x == 2:
				len_x = len(splited_filename[0]) + len(splited_filename[1])
				temp.append(splited_filename[0])
				temp.append(splited_filename[1])
				temp.append("")
			elif count_x > 2:
				len_x = len(splited_filename[0]) + len(splited_filename[1])
				temp.append(splited_filename[0])
				temp.append(splited_filename[1])
				temp.append(one_filename[len_x + 2:])

			for index, one in enumerate(temp):
				if not temp[0] in list(result.keys()):
					result[temp[0]] = {}

				if not temp[1] in list(result[temp[0]].keys()):
					result[temp[0]][temp[1]] = {}

				if not temp[2] in list(result[temp[0]][temp[1]].keys()):
					result[temp[0]][temp[1]][temp[2]] = ""
		return result

	def make_char_set(self, upper_eng="", lower_eng="", num="", special="", others=""):
		"""
		어떤 문자의 조합까지 넣을것인지 확인하는 것

		:param upper_eng:
		:param lower_eng:
		:param num:
		:param special:
		:param others:
		:return:
		"""
		check_char = []
		if upper_eng:    check_char.extend(list(string.ascii_uppercase))
		if lower_eng: check_char.extend(list(string.ascii_lowercase))
		if num: check_char.extend(list(string.digits))
		if special: check_char.extend("!@#$%^*_-")
		if others: check_char.extend(others)
		return check_char

	def make_comma_string(self, input_list):
		# 리스트를 주면, 콤마로 연결한 문자열을 만들어주는것
		result = ""
		for one_item in input_list:
			if one_item == "":
				pass
			else:
				result += str(one_item) + ", "
		return result[:-2]

	def make_dic_2d(self, main_dic, input_key_1, input_key_2, input_value_2):
		"""
		2차원자료를 만드는것

		:param main_dic:
		:param input_key_1:
		:param input_key_2:
		:param input_value_2:
		:return:
		"""
		if type(main_dic[input_key_1]) != type({}):
			main_dic[input_key_1] = {}

		main_dic[input_key_1][input_key_2] = input_value_2
		return main_dic

	def make_dic_for_two_list(self, key_list, value_list):
		"""
		두개의 리스트를 받으면 사전으로 만들어 주는 코드

		:param key_list:
		:param value_list:
		:return:
		"""
		result = dict(zip(key_list, value_list))
		return result

	def make_dic_with_count(self, input_text):
		"""
		갯수만큼의 문자열을 사전으로 만드는 것

		:param input_text:
		:return:
		"""
		input_text = input_text.replace(" ", "")
		input_text = input_text.upper()
		result = {}
		for one_letter in input_text:
			if one_letter in list(result.keys()):
				result[one_letter] = result[one_letter] + 1
			else:
				result[one_letter] = 1
		return result

	def make_easy_css(self, selector, style):
		"""
		기본이되는 메소드로, 이것을 통해서 css를 만드는 것이다
		"""
		text_selector = self.maker_for_selector_n_repeater_n_attr(selector)
		dic_1 = self.maker_for_decoration(style)
		text_decoration = self.change_dic_to_text_decoration(dic_1)
		return text_selector + "{" + text_decoration + "}"

	def make_file_for_input_text(self, filename, input_text):
		"""
		텍스트자료를 화일로 저장하는것
		"""
		new_file = open(filename, "r", encoding="UTF-8")
		for one in input_text:
			new_file.write(one)

	def make_file_with_text(self, file_full_name, source_data):
		"""
		텍스트자료를 화일로 저장하는것
		"""
		new_file = open(file_full_name, "w", encoding="UTF-8")
		for one in source_data:
			new_file.write(one)

	def make_folder(self, input_folder_name):
		"""
		폴더 만들기

		:param input_folder_name:
		:return:
		"""
		try:
			os.mkdir(input_folder_name)
		except:
			pass

	def make_html_inline_text(self, input_text, bold, size, color):
		"""
		입력문자에 진하게, 색상, 크기를 html으로 적용하기 위하여 만든 것
		:param input_text:
		:param bold:
		:param size:
		:param color:
		:return:
		"""
		text_style: str = '<p style= "'
		aaa = ""
		if bold:
			if text_style != '<p style= "': aaa = ';'
			text_style = text_style + aaa + "font-weight: bold"
		if size:
			if text_style != '<p style= "': aaa = ';'
			text_style = text_style + aaa + "font-size: " + str(size) + "px"
		if color:
			if text_style != '<p style= "': aaa = ';'
			text_style = text_style + aaa + "color: " + str(color)
		text_style = text_style + '">' + input_text + "</p>"
		result = text_style
		return result

	def make_html_table(self, table_title_list, table_value_list):
		"""
		** youtil에 추가하여야 할것

		html용으로 사용되는 table을 만드는 것
		:param table_title_list:
		:param table_value_list:
		:return:
		"""
		body_top = """
            수고합니다<br>
            <br>
            구매 요청건에 대하여 아래와 같이 TBE요청합니다"<br>
            <br>
            """

		body_tail = """
            <br>
            -----------------------------------------------------------------------------------<br>
            abc컴퍼니 / def수석<br>

            """

		table_style = """
            <html>
            <style>
            body {
                  font-family:'Malgun Gothic';
                  font-size:10pt;
                }
            table {
                width: 70%;
                padding: 11px;
                font-family:'Malgun Gothic';
                font-size:10pt;
              }
              tr, td {
                border-bottom: 1px solid #444444;
                padding: 3px;
                text-align: center;
              }
              tr, th {
                padding: 13px;
                background-color: #bbdefb;
              }
              td {
                background-color: #e3f2fd;
              }
                </style>
                <body>"""

		temp = table_style + body_top + "<table>"

		temp = temp + "<tr>"
		for x in range(len(table_title_list)):
			temp = temp + "<th>" + str(table_title_list[x]) + "</th>"
		temp = temp + "</tr>"

		for x in range(len(table_value_list)):
			temp = temp + "<tr>"
			for y in range(len(table_value_list[0])):
				temp = temp + "<td>" + str(table_value_list[x][y]) + "<br></td>"
			temp = temp + "</tr>"
		temp = temp + "</table>" + body_tail + "</body></html>"
		return temp

	def make_int_list_with_option(self, start_no=1, end_no=1000, step=1, qty=100, random_tf=False, unique_tf=True):
		"""
		make : 어디에서 기본 자료를 갖고오지 않는 경우
		정수형으로 구성된 리스트 자료를 쉽게 만들어주는 함수
		갯수가 잘못 입력되었을때를 대비 하는것

		:param start_no:
		:param end_no:
		:param step:
		:param qty: 몇개를 리스트로 만들것인지
		:param random_tf: 랜덤한 자료를 만들것인지, 끝의 tf는 true_falfe를 나타내는 뜻입니다
		:param unique_tf: 고유한것이만일지, 같은 값도 반복이 가능한지를 선택하는것, 끝의 tf는 true_falfe를 나타내는 뜻입니다
		:return:
		"""

		if qty == False or int((end_no - start_no) / step) < qty:
			qty = int((end_no - start_no) / step)
		# 고유한 자료들만 하는경우와 중복이 가능한 경우를 나눠서 적용

		if random_tf:
			if unique_tf:
				temp = list(range(start_no, end_no, step))
				random.shuffle(temp)
				result = temp[:qty]
			else:
				result = []
				for _ in range(qty):
					result.append(random.randrange(start_no, end_no, step))
		else:
			temp = list(range(start_no, end_no, step))
			result = temp[:qty]
		return result

	def make_korean_char(self, input_list):
		"""
		유니코드 한글 시작점

		:param input_list:
		:return:
		"""
		base_code = 0xAC00
		# 초성, 중성, 종성 리스트
		choseong_list = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]  # 19 글자
		jungseong_list = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]  # 21 글자
		jongseong_list = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]  # 28 글자, 없는것 포함

		# 초성, 중성, 종성의 인덱스 찾기
		choseong_index = choseong_list.index(input_list[0])
		jungseong_index = jungseong_list.index(input_list[1])
		jongseong_index = jongseong_list.index(input_list[2])
		# 유니코드 계산
		korean_code = base_code + (choseong_index * 21 * 28) + (jungseong_index * 28) + jongseong_index
		# 유니코드 문자로 변환
		korean_char = chr(korean_code)
		return korean_char

	def make_list_2d_same_len(self, input_data):
		"""
		길이가 다른 2dlist의 내부 값들을 길이가 같게 만들어주는 것이다
		가변적인 2차원배열을 최대크기로 모두 같이 만들어 준다
		"""
		result = []
		max_len = max(len(row) for row in input_data)
		for list_x in input_data:
			temp = list_x
			for no in range(len(list_x), max_len):
				temp.append("")
			result.append(temp)
		return result

	def make_list_for_same_repeat_no(self, input_data, line_no):
		"""
		넘어온 자료중 line_no번째의 연속된 자료가 같은 갯수를 세어서 리스트형태로 돌려주는것

		:param input_data:
		:param line_no:
		:return:
		"""
		result = []
		num = 1
		for no in range(len(input_data) - 1):
			if input_data[no][line_no] == input_data[no + 1][line_no]:
				# 위와 아래의 Item이 같은것일때
				num = num + 1
			else:
				result.append(num)
				num = 1
		# print(result)
		return result

	def make_list_on_re_compile(self, re_txt, filename):
		"""
		텍스트화일을 읽어서 re에 맞도록 한것을 리스트로 만드는 것이다
		함수인 def를 기준으로 저장을 하며, [[공백을없앤자료, 원래자료, 시작줄번호].....]

		:param re_txt:
		:param filename:
		:return:
		"""
		re_com = re.compile(re_txt)
		f = open(filename, 'r', encoding='UTF8')
		lines = f.readlines()
		num = 0
		temp = ""
		temp_original = ""
		result = []
		for one_line in lines:
			aaa = re.findall(re_com, str(one_line))
			original_line = one_line
			changed_line = one_line.replace(" ", "")
			changed_line = changed_line.replace("\n", "")

			if aaa:
				result.append([temp, temp_original, num])
				temp = changed_line
				temp_original = original_line
			# print("발견", num)
			else:
				temp = temp + changed_line
				temp_original = temp_original + one_line
		return result

	def make_menu_for_folder(self, input_folder):
		"""
		어떤 폴더안의 화일이름을 2단계의 메뉴로 만들어주는 코드
		"""

		all_filenames = self.get_all_filename_in_folder(input_folder)
		result = {}

		for one_filename in all_filenames:
			splited_filename = str(one_filename).split("_")
			if splited_filename[0] in result.keys():
				result[splited_filename[0]].append(one_filename)
			else:
				result[splited_filename[0]] = [one_filename]
		return result

	def make_menu_for_input_object(self, input_object, except_startwith=["__", "xlapp", "xlbook", "check_", "type_", "data_"]):
		"""
		총 3가지의 결과값을 돌려준다
		1. dic["각메소드이름"] = {'1st':"", '2nd':"", '3rd':"", "method_name", "params":, "doc":"~~~" }
		어떤 객체가 오면 메소드를 3단계의 메뉴로 만들어주는 코드
		메소드이름을 나누는 기준은 _를 기준으로 한다
		만약 3단계 이하의 분리가 되면 나머지는 공백으로 만든다
		"""

		menu = {}
		tree_menu = {}
		all_method_name_list = {}

		# {"메소드이름":{"변수1":"기본값1", "변수2":"기본값2".....}......}
		self.object_dic = self.get_all_method_name_with_argument_for_input_object(input_object)

		for one_method_name in self.object_dic.keys():
			if self.check_start_with_list(one_method_name, except_startwith):

				splited_method_name = str(one_method_name).split("_")

				temp = {'1st': "", '2nd': "", '3rd': "", }
				temp['method_name'] = one_method_name
				temp['params'] = self.object_dic[one_method_name]
				temp['doc'] = self.get_doc_for_method_name_with_object(input_object, one_method_name)

				temp['1st'] = splited_method_name[0]

				if len(splited_method_name) == 2:
					temp['2nd'] = splited_method_name[1]
					temp['3rd'] = ""
				elif len(splited_method_name) > 2:
					temp['2nd'] = splited_method_name[1]
					temp['3rd'] = one_method_name[len(splited_method_name[0]) + len(splited_method_name[1]) + 2:]
				menu[one_method_name] = temp

				# tree형식으로 메뉴를 만들기 위한것
				if not temp["1st"] in tree_menu.keys():
					tree_menu[temp["1st"]] = {}

				if not temp["2nd"] in tree_menu[temp["1st"]].keys():
					tree_menu[temp["1st"]][temp["2nd"]] = {}

				if not temp["3rd"] in tree_menu[temp["1st"]][temp["2nd"]].keys():
					tree_menu[temp["1st"]][temp["2nd"]][temp["3rd"]] = ""

				all_method_name_list[temp["1st"] + temp["2nd"] + temp["3rd"]] = one_method_name
		# 제목을 기준으로 찾을수있도록 만든것

		return [menu, tree_menu, all_method_name_list]

	def make_menu_for_object(self, input_object, except_startwith=["__", "xlapp", "xlbook", "check_", "type_", "data_"]):
		"""
		총 3가지의 결과값을 돌려준다
		1. dic["각메소드이름"] = {'1st':"", '2nd':"", '3rd':"", "method_name", "params":, "doc":"~~~" }
		어떤 객체가 오면 메소드를 3단계의 메뉴로 만들어주는 코드
		메소드이름을 나누는 기준은 _를 기준으로 한다
		만약 3단계 이하의 분리가 되면 나머지는 공백으로 만든다
		"""

		menu = {}
		tree_menu = {}
		all_method_name_list = {}

		# {"메소드이름":{"변수1":"기본값1", "변수2":"기본값2".....}......}
		self.object_dic = self.get_all_method_name_n_argument_for_object_as_dic(input_object)

		for one_method_name in self.object_dic.keys():
			if self.check_start_with_list(one_method_name, except_startwith):

				splited_method_name = str(one_method_name).split("_")

				temp = {'1st': "", '2nd': "", '3rd': "", }
				temp['method_name'] = one_method_name
				temp['params'] = self.object_dic[one_method_name]
				temp['doc'] = self.get_doc_for_method_name_with_object(input_object, one_method_name)

				temp['1st'] = splited_method_name[0]

				if len(splited_method_name) == 2:
					temp['2nd'] = splited_method_name[1]
					temp['3rd'] = ""
				elif len(splited_method_name) > 2:
					temp['2nd'] = splited_method_name[1]
					temp['3rd'] = one_method_name[len(splited_method_name[0]) + len(splited_method_name[1]) + 2:]
				menu[one_method_name] = temp

				# tree형식으로 메뉴를 만들기 위한것
				if not temp["1st"] in tree_menu.keys():
					tree_menu[temp["1st"]] = {}

				if not temp["2nd"] in tree_menu[temp["1st"]].keys():
					tree_menu[temp["1st"]][temp["2nd"]] = {}

				if not temp["3rd"] in tree_menu[temp["1st"]][temp["2nd"]].keys():
					tree_menu[temp["1st"]][temp["2nd"]][temp["3rd"]] = ""

				all_method_name_list[temp["1st"] + temp["2nd"] + temp["3rd"]] = one_method_name
		# 제목을 기준으로 찾을수있도록 만든것

		return [menu, tree_menu, all_method_name_list]

	def make_menu_set_for_object(self, input_object, except_startwith=["__", "xlapp", "xlbook", "check_", "type_", "data_"]):
		"""
		총 3가지의 결과값을 돌려준다
		1. dic["각메소드이름"] = {'1st':"", '2nd':"", '3rd':"", "method_name", "params":, "doc":"~~~" }
		어떤 객체가 오면 메소드를 3단계의 메뉴로 만들어주는 코드
		메소드이름을 나누는 기준은 _를 기준으로 한다
		만약 3단계 이하의 분리가 되면 나머지는 공백으로 만든다

		메뉴에서 1번째것을 누르면, 나머지것이 나오도록 만들기 위해 teee형식으로 만든 것이다
		"""

		menu = {}
		tree_menu = {}
		all_method_name_list = {}

		# 입력 객체에 대해서 메소드이름과 인수를 사전형으로 만드는 것
		# {"메소드이름":{"변수1":"기본값1", "변수2":"기본값2".....}......}
		self.object_dic = self.get_all_method_name_with_argument_for_object(input_object)

		# 메소드의 이름을 하나씩 넣은후에, _를 기준으로 3단계로 만드는 것
		for one_method_name in self.object_dic.keys():
			if self.check_start_with_list(one_method_name, except_startwith):

				splited_method_name = str(one_method_name).split("_")

				temp = {'1st': "", '2nd': "", '3rd': "", }
				temp['method_name'] = one_method_name
				temp['params'] = self.object_dic[one_method_name]
				temp['doc'] = self.get_doc_for_method_name_with_object(input_object, one_method_name)

				temp['1st'] = splited_method_name[0]

				if len(splited_method_name) == 2:
					temp['2nd'] = splited_method_name[1]
					temp['3rd'] = ""
				elif len(splited_method_name) > 2:
					temp['2nd'] = splited_method_name[1]
					temp['3rd'] = one_method_name[len(splited_method_name[0]) + len(splited_method_name[1]) + 2:]
				menu[one_method_name] = temp

				# tree형식으로 메뉴를 만들기 위한것
				if not temp["1st"] in tree_menu.keys():
					tree_menu[temp["1st"]] = {}

				if not temp["2nd"] in tree_menu[temp["1st"]].keys():
					tree_menu[temp["1st"]][temp["2nd"]] = {}

				if not temp["3rd"] in tree_menu[temp["1st"]][temp["2nd"]].keys():
					tree_menu[temp["1st"]][temp["2nd"]][temp["3rd"]] = ""

				all_method_name_list[temp["1st"] + temp["2nd"] + temp["3rd"]] = one_method_name
		# 제목을 기준으로 찾을수있도록 만든것
		return [menu, tree_menu, all_method_name_list]

	def make_multi_line_text_for_list_1d(self, input_list_1d):
		"""
		1 차원리스트의 자료를 줄바꿈기호를 넣어서 여러줄로 되는 텍스트로 바꿔주는 것

		:param input_list_1d:
		:return:
		"""
		result = ""
		for one in input_list_1d:
			result = result + str(one).strip() + chr(13)
		return result

	def make_multi_line_text_for_one_text_by_chars(self, input_text, input_chars=", "):
		"""
		한줄의 텍스트를 원하는 문자를 기준으로 나누어서, 여러줄의 텍스트로 만들어 주는것

		:param input_text:
		:param input_chars:
		:return:
		"""
		input_list_1d = input_text.split(input_chars)
		result = ""
		for one in input_list_1d:
			result = result + str(one).strip() + chr(13)
		return result

	def make_name_list(self, input_no=5):
		"""
		입력한 갯수만큼 이름의 갯수를 만들어 주는것

		:param input_no:
		:return:
		"""
		sung = "김이박최정강조윤장"
		name = "가나다라마바사아자차카"
		last = "진원일이삼사오구원송국한"
		if input_no > len(sung) * len(name) * len(last) / 2:
			result = []
			pass
		else:
			total_name = set()
			num = 0
			while True:
				one_sung = random.choice(sung)
				one_name = random.choice(name)
				one_last = random.choice(last)
				new_name = one_sung + one_name + one_last
				total_name.add(new_name)
				num = num + 1
				if len(total_name) == input_no:
					# print(input_no, num)
					break
			result = list(total_name)
		return result

	def make_one_text_with_special_char_for_list_1d(self, input_list_1d, input_char=", "):
		"""
		1 차원리스트의 모든 자료를 원하는 글자를 붙여서 1개의 텍스트로 만들어 주는것
		각요소들의 앞뒤공백을 없애준다

		:param input_list_1d:
		:param input_char:
		:return:
		"""
		result = ""
		for one in input_list_1d:
			result = result + str(one).strip() + input_char
		return result

	def make_random_list(self, input_list, input_limit, input_times=1):
		"""
		입력된 자료를 랜덤으로 리스트를 만드는 것

		:param input_list:
		:param input_limit:
		:param input_times:
		:return:
		"""
		result_set = []
		# if len(input_list) == 2:
		#	input_list = list(range(input_list[0], input_list[1]))
		for no in range(input_times):
			result = []
			for num in range(input_limit):
				dd = random.choice(input_list)
				result.append(dd)
				input_list.remove(dd)
			result_set.append(result)
		return result_set

	def make_random_list_for_input_list(self, input_list, input_limit, input_times=1):
		"""
		입력된 자료를 랜덤으로 리스트를 만드는 것

		:param input_list:
		:param input_limit:
		:param input_times:
		:return:
		"""
		result_set = []
		# if len(input_list) == 2:
		#	input_list = list(range(input_list[0], input_list[1]))
		for no in range(input_times):
			result = []
			for num in range(input_limit):
				dd = random.choice(input_list)
				result.append(dd)
				input_list.remove(dd)
			result_set.append(result)
		return result_set

	def make_same_len_for_list_2d(self, input_list_2d):
		"""
		change_list_to_samelen_list( input_list_2d)
		2차원 리스트의 최대 길이로 같게 만드는 것
		가끔 자료의 갯수가 달라서 생기는 문제가 발생할 가능성이 있는것을 맞추는것
		추가할때는 ""를 맞는갯수를 채워넣는다
		"""
		input_text = None
		max_num = max(map(lambda x: len(x), input_list_2d))
		result = []
		for one in input_list_2d:
			one_len = len(one)
			if max_num == one_len:
				result.append(one)
			else:
				one.extend([input_text] * (max_num - one_len))
				result.append(one)
		return result

	def make_serial_no_from_start_no(self, start_no=1, style="####"):
		"""
		1000으로 시작되는 연속된 번호를 만드는 것이다

		:param start_no:
		:param style:
		:return:
		"""
		length = len(style)
		value = 10 ** (length - 1) + start_no
		return value

	def make_table_sample_for_int_01(self, xlen, ylen, xtitle, ytitle, data_style=100):
		"""
		샘플을 만들어주는 것
		숫자가 들어간 2차원테이블형식의 자료를 만들어 주는 것

		:param xlen:
		:param ylen:
		:param xtitle:
		:param ytitle:
		:param data_style:
		:return:
		"""
		xtitle_list = self.make_title_with_num(xtitle, "_", xlen)
		xtitle_list.insert(0, "")
		ytitle_list = self.make_title_with_num(ytitle, "_", ylen + 1)
		result = []
		result.append(xtitle_list)
		for ix, one in enumerate(range(xlen)):
			temp = [ytitle_list[ix]]
			for two in range(ylen):
				temp.append(int(random.random() * data_style))
			result.append(temp)
		return result

	def make_team_with_condition(self, all_data, not_same_group, level, step):
		"""
		무엇인가를 하다보면, 조편성을 해야하는 경우가 있는데, 이때, 여러 조건들을 만족해야만 하는
		가 생긴다
		즉, 팀장들은 분리를 해야한다던지
		부장과 과장은 같이 안들어가게 해야 한다던지
		이렇게 조건에 맞는 조를 편성하는것을 한번 만들어 보았다

		:param all_data: 원본자료, 조를 짜는 자료들
		:param not_same_group: 서로 같은 그룹에 있으면 않되는 자료들, 서로 같은 그룹에 들어가면 않되는 것
		:param level: 사원그룹, 대리그룹, 과장그룹과 같은 그런 형태의 집단들로 가능하면 서로 섞이도록
		:param step: 최종 그룹의 갯수
		:return:
		"""
		# 해당하지 않는것을 제일 마지막의 자료에 넣는다
		# 전체자료중에서, level로 묶여진것을
		changed_level = self.change_re_group_by_step(all_data, level, step)
		# print(changed_level)
		# 그룹no만큼 그룹을 만든다
		result = {}
		for no in range(step):
			result[no] = []
		# 몇번을 반복해서 계산할것인지를 나타낸다
		repeat_no, namuji = divmod(len(all_data), step)
		if namuji != 0: repeat_no = repeat_no + 1
		# 서로있으면 않되는 모든 2가지의 경우의 수를 만들어서 확인하는데 사용한다
		combi = []
		for one_group in not_same_group:
			aaa = list(itertools.permutations(one_group, 2))
			combi.extend(aaa)
			n = 0
			for list_1d in changed_level:
				randomed_list_1d = self.make_random_list(list_1d, len(list_1d))[0]
				finished = ""
				for one_value in randomed_list_1d:
					temp = []
					finished = ""
					for num in range(step):
						if finished == "ok":
							pass
						else:
							min_group_no = self.check_min_result(result, temp)
							error_found = False
							for one_item in combi:
								if (one_item[0] in result[min_group_no] or one_item[1] in result[min_group_no]) and (
										one_item[0] == one_value or one_item[1] == one_value):
									error_found = True
							if error_found:
								temp.append(min_group_no)
							else:
								result[min_group_no].append(one_value)
								finished = "ok"
		return result

	def make_text_basic(self, input_value, total_len):
		"""
		f-string처럼 문자를 변경하는것

		:param input_value:
		:param total_len:
		:return:
		"""
		result = ""
		if type(input_value) == type(123.45):
			result = self.make_text_for_float(input_value, total_len, 2, " ", "right", True)
		elif type(input_value) == type(123):
			result = self.make_text_for_integer(input_value, total_len, " ", "right", True)
		elif type(input_value) == type("123.45"):
			result = self.make_text_for_string(input_value, total_len, " ", "right")
		return result

	def make_text_file_for_input_text(self, file_full_name, input_text):
		"""
		텍스트자료를 화일로 저장하는것

		:param file_full_name:
		:param input_text:
		:return:
		"""
		new_file = open(file_full_name, "w", encoding="UTF-8")
		for one_line in input_text:
			new_file.write(one_line)

	def make_text_file_for_text_data(self, file_full_name, input_text):
		"""
		텍스트자료를 화일로 저장하는것

		:param file_full_name:
		:param input_text:
		:return:
		"""
		new_file = open(file_full_name, "w", encoding="UTF-8")
		for one_line in input_text:
			new_file.write(one_line)

	def make_text_for_float(self, input_value, big_digit, small_digit, fill_empty=" ", align="right", comma1000=True):
		"""
		f-string처럼 실수를 원하는 형태로 변경하는것

		:param input_value:
		:param big_digit:
		:param small_digit:
		:param fill_empty:
		:param align:
		:param comma1000:
		:return:
		"""
		if comma1000:
			changed_value = f"{round(float(input_value), small_digit):,}"
		else:
			changed_value = str(round(float(input_value), small_digit))

		repeat_no = big_digit - len(changed_value)

		repeat_char = fill_empty * (repeat_no)
		repeat_char_start = fill_empty * int(repeat_no / 2)
		repeat_char_end = fill_empty * int(repeat_no - int(repeat_no / 2))

		if align == "left":
			result = changed_value + repeat_char
		elif align == "right":
			result = repeat_char + changed_value
		elif align == "middle":
			result = repeat_char_start + changed_value + repeat_char_end
		else:
			result = repeat_char + changed_value
		return result

	def make_text_for_integer(self, input_value, big_digit, fill_empty=" ", align="right", comma1000=True):
		"""
		f-string처럼 숫자를 원하는 형태로 변경하는것

		:param input_value:
		:param big_digit:
		:param fill_empty:
		:param align:
		:param comma1000:
		:return:
		"""

		if comma1000:
			changed_value = f"{input_value:,}"
		else:
			changed_value = str(input_value)

		repeat_no = big_digit - len(changed_value)

		repeat_char = fill_empty * (repeat_no)
		repeat_char_start = fill_empty * int(repeat_no / 2)
		repeat_char_end = fill_empty * int(repeat_no - int(repeat_no / 2))

		if align == "left":
			result = changed_value + repeat_char
		elif align == "right":
			result = repeat_char + changed_value
		elif align == "middle":
			result = repeat_char_start + changed_value + repeat_char_end
		else:
			result = repeat_char + changed_value
		return result

	def make_text_for_list_1d(self, input_list_2d, input_len):
		"""
		1차원리스트의 자료들을 정렬해서 텍스트로 만드는 것

		:param input_list_2d:
		:param input_len:
		:return:
		"""
		result_text = ""
		result = []
		len_list = {}
		for index, one in enumerate(input_list_2d[0]):
			len_list[index] = 0

		for list_1d in input_list_2d:
			for index, one in enumerate(list_1d):
				len_list[index] = max(len(str(one)), len_list[index])

		for list_1d in input_list_2d:
			temp = ""
			for index, one in enumerate(list_1d):
				len_list[index] = max(len(str(one)), len_list[index])

		# print(len_list)

		for list_1d in input_list_2d:
			temp = ""
			for index, one in enumerate(list_1d):
				temp = temp + self.make_text_basic(one, len_list[index] + input_len)

			result_text = result_text + temp + '\n'
		return result_text

	def make_text_for_string(self, input_value, big_digit, fill_empty=" ", align="right"):
		"""
		f-string처럼 문자를 원하는 형태로 변경하는것

		:param input_value:
		:param big_digit:
		:param fill_empty:
		:param align:
		:return:
		"""
		changed_value = str(input_value)
		repeat_no = big_digit - len(changed_value)

		repeat_char = fill_empty * (repeat_no)
		repeat_char_start = fill_empty * int(repeat_no / 2)
		repeat_char_end = fill_empty * int(repeat_no - int(repeat_no / 2))

		if align == "left":
			result = changed_value + repeat_char
		elif align == "right":
			result = repeat_char + changed_value
		elif align == "middle":
			result = repeat_char_start + changed_value + repeat_char_end
		else:
			result = repeat_char + changed_value
		return result

	def make_text_list_from_int(self, start_no=1, end_no=1000, step=1, qty=100, same_len=0, start_char="", random_tf=False, unique_tf=False):
		"""
		make : 어디에서 기본 자료를 갖고오지 않는 경우
		뒤에 숫자가 붙은 형태의 컬럼 제목을 위한 리스트형태로 만드는 것
		예  : ["title_002","title_003","title_004","title_005"]
		Databse용 table 의 각 y열의 제목을 만들어주는 것같은 리스트를 만들어주는것
		1. 앞에 접두어를 붙일것인지
		2. 뒤에붙는 숫자의 길이를 같게 만들것인지 (100 => 0100, 12 => 0012)

		:param start_no:
		:param end_no:
		:param step:
		:param qty:
		:param same_len:
		:param start_char:
		:param random_tf:
		:param unique_tf:
		:return:
		"""

		if same_len:
			if len(str(end_no)) > same_len:
				same_len = len(str(end_no))
			if qty == False or int((end_no - start_no) / step) < qty:
				qty = int((end_no - start_no) / step)

		# 고유한 자료들만 하는경우와 중복이 가능한 경우를 나눠서 적용
		result = []
		if random_tf:
			if unique_tf:
				temp = list(range(start_no, end_no, step))
				random.shuffle(temp)
				for one_value in temp[:qty]:
					result.append(start_char + (same_len - len(str(one_value))) * "0" + str(one_value))
			else:
				temp = list(range(start_no, end_no, step))
				random.shuffle(temp)
				for _ in range(qty):
					one_value = random.choice(temp)
					result.append(start_char + (same_len - len(str(one_value))) * "0" + str(one_value))
		else:
			temp = list(range(start_no, end_no, step))
			for one_value in temp[:qty]:
				result.append(start_char + (same_len - len(str(one_value))) * "0" + str(one_value))
		return result

	def make_title_with_num(self, title="제목 ", connect_char="_", xlen=6):
		"""
		예제를 만들때, 제목 부분을 쉽게 만드릭 위해서 만든 것입니다

		:param title:
		:param connect_char:
		:param xlen:
		:return:
		"""
		result = []

		if title:
			title = "제목"
		for num in range(1, xlen + 1):
			result.append(title + connect_char + str(num))
		return result

	def make_unique_words(self, input_list_2d):
		"""
		입력으로 들어온 자료들을 단어별로 구분하기위해서 만든것이며 /,&-등의 문자는 없앨려고 하는것이다
		"""
		list_1d = []
		for one in input_list_2d:
			list_1d.extend(one)
		temp_result = []
		for one in list_1d:
			one = str(one).lower()
			one = one.replace("/", "")
			one = one.replace(",", "")
			one = one.replace("&", "")
			one = one.replace("_", "")
			temp_result.extend(one.split(""))
		result = list(set(temp_result))
		return result

	def make_zip_file(self, zip_name_path, new_path_all):
		"""
		화일들을 zip으로 압축하는것

		:param zip_name_path:
		:param new_path_all:
		:return:
		"""
		with zipfile.ZipFile(zip_name_path, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
			for one in new_path_all:
				new_zip.write(one)
		new_zip.close()

	def maker_for_decoration(self, input_list_1d):
		"""
		폰트와 백그라운드, 라인의 속성값을 리스트형태로 3개를 받으면 각자 알아서
		사전형식으로 css에서 사용가능한 것으로 바꿔주는 것이다
		"""
		result_dic = {}
		if input_list_1d[0]:
			result_dic.update(self._check_font_data(input_list_1d[0]))
		if len(input_list_1d) > 1:
			result_dic.update(self._check_background_data(input_list_1d[1]))
		if len(input_list_1d) > 2:
			result_dic["border"] = self._check_border_data(input_list_1d[2])
		return result_dic

	def maker_for_selector_n_repeater_n_attr(self, i_list_1d):
		"""
		selector는 너무 다양해서, 가능하면 3부분으로 분리
		제일 앞의것을 리스트형태로 변경
		selector_1 = ["p~h1", "nth-child(3)", "[herf='_blank']"]
		"""
		result = self.chenge_text_selector_to_css_selector(i_list_1d[0])
		# print(self.find_text_between_brackets(i_list_1d[0]))

		if i_list_1d[1]:
			if type(i_list_1d[1]) != type([]):
				i_list_1d[1] = [i_list_1d[1]]
			if len(i_list_1d[1]) == 1:
				result = result + "::" + self.change_text_repeater_to_css_repeater(str(i_list_1d[1][0]))
			elif len(i_list_1d[1]) == 2:
				result = result + ":" + self.change_text_repeater_to_css_repeater(
					str(i_list_1d[1][0])) + ":" + self.change_text_repeater_to_css_repeater(str(i_list_1d[1][0]))
			elif len(i_list_1d[1]) == 3:
				result = result + ":" + self.change_text_repeater_to_css_repeater(
					str(i_list_1d[1][0])) + ":" + self.change_text_repeater_to_css_repeater(
					str(i_list_1d[1][1])) + ":" + self.change_text_repeater_to_css_repeater(str(i_list_1d[1][2]))

		if len(i_list_1d) > 2:
			# print(i_list_1d)
			result = result + str(i_list_1d[2])
		return result

	def mix_data(self, list1, list1_index, list2, list2_index):
		"""
		입력받은 2개의 자료를 하나로 합치는 것이며, 같은 자료의 위치를 알려주는 것이다
		만약 같은 자료가 없는 것은 무시한다

		:param list1:
		:param list1_index:
		:param list2:
		:param list2_index:
		:return:
		"""
		list1_dic = {}
		for one_line in list1:
			list1_dic[one_line[list1_index]] = one_line
		result = []
		for one_line in list2:
			if one_line[list2_index] in list1_dic.keys():
				temp = list1_dic[one_line[list2_index]]
				temp.extend(one_line)
				result.append(temp)
		return result

	def mix_two_dic_data(self, dic_1, dic_2):
		"""
		자료를 합쳐주는 기능
		입력한 자료의 테이블제목이 a, d, e라고 하고 다른 테이블의 자료가 a, b라고 할때
		1. 두개 화일의 제목을 먼저 하나로 만든다
		2. 각 테이블의 자료를 사전형식으로 바꾼다
		3. 하나씩 돌아가면서, 자료를 정렬한다

		:param dic_1:
		:param dic_2:
		:return:
		"""
		result = []
		title_list = list(dic_1.keys())
		title_list_2 = list(dic_2.keys())
		for one in title_list_2:
			if not one in title_list:
				title_list.append(one)
		result.append(title_list)

		for index in range(len(dic_1[title_list[0]])):
			temp = []
			for one_title in title_list:
				if one_title in dic_1.keys():
					temp.append(dic_1[one_title][index])
				else:
					temp.append(None)
				result.append(temp)

		for index in range(len(dic_2[title_list_2[0]])):
			temp = []
		for one_title in title_list:
			if one_title in dic_2.keys():
				temp.append(dic_2[one_title][index])
			else:
				temp.append(None)
			result.append(temp)
		return result

	def mix_two_list_2d(self, input_list_1, input_list_2):
		"""
		두개의 리스트를 서로 묶어서, 새로운 리스트를 만드는 것
		[1,2,3], ["a","b","c"] ==> [[1, "a"],[2,"b"],[3,"c"]]

		:param input_list_1:
		:param input_list_2:
		:return:
		"""
		result = []
		for x, y in zip(input_list_1, input_list_2):
			result.append(x + y)
		return result

	def mix_two_list_2d_by_title_name(self, input_base_list_2d, input_sub_list_2d):
		"""
		2차원의 자료에 다른 2차원의 자료를 제목을 기준으로 붙이기
		새로운것을 붙일때는 기존의 값은 빈것을 넣는다
		yx의 순서로 자료가 입력되어야 함

		:param input_base_list_2d:
		:param input_sub_list_2d:
		:return:
		"""

		blank_list = []
		for one in range(1, len(input_base_list_2d[0])):
			blank_list.append("")

		blank_list2 = []
		for one in range(1, len(input_sub_list_2d[0])):
			blank_list2.append("")

		total_len = len(input_base_list_2d[0]) + len(input_sub_list_2d[0]) - 1

		for no1, value1 in enumerate(input_sub_list_2d):
			found = False
			if value1 == None: value1 = ""

			for no2, value2 in enumerate(input_base_list_2d):
				if value2 == None: value2 = ""
				if value1[0] == value2[0]:
					input_base_list_2d[no2].extend(value1[1:])
					found = True

			if not found:
				input_base_list_2d.append(blank_list.extend(value1[1:]))

		for no, list_1d in enumerate(input_base_list_2d):
			if len(list_1d) < total_len:
				input_base_list_2d[no].extend(blank_list2)
		return input_base_list_2d

	def mix_two_list_as_beside(self, input_list_2d_1, input_list_2d_2):
		"""
		맨앞의 자료가 같다는 가정에서 하는것
		제목부분은 고유한 자료여야 한다
		자료가 없거나 값이 없을때 붙이는 빈자료를 위해 만든것

		:param input_list_2d_1:
		:param input_list_2d_2:
		:return:
		"""
		no_of_list_2d_1 = len(input_list_2d_1[0]) - 1
		no_of_list_2d_2 = len(input_list_2d_2[0]) - 1
		empty_list_2d_1 = [""] * no_of_list_2d_1
		empty_list_2d_2 = [""] * no_of_list_2d_2
		# 리스트형태로는 코드가 더 길어질것으로 보여서 입력자료를 사전으로 변경 한것
		temp_dic = {}
		for one in input_list_2d_1:
			temp_dic[one[0]] = one[1:]
		checked_list = []
		# 기준이 되는 자료에 항목이 있을때
		for one in input_list_2d_2:
			if one[0] in temp_dic.keys():
				temp_dic[one[0]] = list(temp_dic[one[0]]) + list(one[1:])
			else:
				temp_dic[one[0]] = empty_list_2d_1 + list(one[1:])
			checked_list.append(one[0])
		# 기준자료에 항목이 없는것에 대한것
		for one in temp_dic.keys():
			if not one in checked_list:
				temp_dic[one] = list(temp_dic[one]) + empty_list_2d_2
		# 사전형식을 리스트로 다시 만드는것
		result = []
		for one in temp_dic:
			result.append([one] + list(temp_dic[one]))
		return result

	def mouse_click(self, x, y):
		"""
		좌표로 이동해서 마우스 왼쪽을 클릭
		mouse_click(300, 300)

		:param x:
		:param y:
		:return:
		"""
		win32api.SetCursorPos((x, y))
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

	def move_degree_distance(self, degree="입력필요", distance="입력필요"):
		"""
		move_degree_distance( degree="입력필요", distance="입력필요")
		현재 위치 x,y에서 30도로 20만큼 떨어진 거리의 위치를 돌려주는 것
		메뉴에서 제외

		:param degree:
		:param distance:
		:return:
		"""
		degree = degree * 3.141592 / 180
		y = distance * math.cos(degree)
		x = distance * math.sin(degree)
		return [x, y]

	def move_element_for_list_2d_by_index(self, input_list_2d, input_no_list):
		"""
		입력형태 : 2차원리스트, [[옮길것, 옮기고싶은자리].....]

		:param input_list_2d:
		:param input_no_list:
		:return:
		"""
		ori_no_dic = {}
		for one in range(len(input_list_2d[0])):
			ori_no_dic[one] = one
		for before, after in input_no_list:
			new_before = ori_no_dic[before]
			new_after = ori_no_dic[after]

			for no in range(len(input_list_2d)):
				if new_before < new_after:
					new_after = after - 1
				value = input_list_2d[no][new_before]
				del input_list_2d[no][new_before]
				input_list_2d[no].insert(int(new_after), value)
		return input_list_2d

	def move_file(self, old_file, new_file):
		"""
		화일을 이동시키는것
		"""
		old_file = self.check_file(old_file)
		shutil.move(old_file, new_file)

	def move_folder(self, old_dir, new_dir):
		"""
		폴더를 이동시키는것
		"""
		shutil.move(old_dir, new_dir)

	def new_dic(self, old_dic, key_list, value):
		"""
		어떤 사전형식의 자료를 넣으면 알아서 분리해 주는것
		dim : 1차원자료인지 아닌지처럼, 몇차원으로 만드는 것
		그차원에서 key값과 value값
		"""
		temp = ""
		icount = len(key_list) - 1
		for index, one_key in enumerate(key_list):
			temp = temp + f"[{one_key}]"
			if icount == index:
				try:
					exec(f"old_dic{temp}=one_key")
				except:
					exec(f"old_dic{temp}=one_key")
			else:
				try:
					exec(f"old_dic{temp}=one_key")
				except:
					exec(f"old_dic{temp}=one_key")
		return old_dic

	def open_pdf_file(self, filename):
		"""
		pdf화일을 여는 것

		:param filename:
		:return:
		"""
		import os
		os.startfile(filename)

	def paste_with_condition(self, range_obj, value=False, memo=False, line=False, width=False, formular=False,
							 format=False, numformat=False, condition_format=False):
		"""
		붙여넣기

		:param range_obj:
		:param value:
		:param memo:
		:param line:
		:param width:
		:param formular:
		:param format:
		:param numformat:
		:param condition_format:
		:return:
		"""
		if value: range_obj.PasteSpecial(-4163)
		if line: range_obj.PasteSpecial(7)
		if width: range_obj.PasteSpecial(8)
		if formular: range_obj.PasteSpecial(-4123)
		if format: range_obj.PasteSpecial(-4122)
		if numformat: range_obj.PasteSpecial(12)
		if condition_format: range_obj.PasteSpecial(14)
		if memo: range_obj.PasteSpecial(-4144)

	def paste_clipboard(self, ):
		"""
		클립보드의 내용을 붙여넣기하는 것

		:return:
		"""
		result = pyperclip.paste()
		return result

	def pick_3_list_with_3_ordering_no(self, i_list_2d, i_no_list):
		"""
		입력되는 2차원자료에서, 원하는 순서번째의 자료만 갖고오는 것
		bbb = pick_3_list_with_3_ordering_no(aaa, [5,3,2])
		:param i_list_2d:
		:param i_no_list:
		:return:
		"""
		result = []
		for no in i_no_list:
			result.append(i_list_2d[no - 1])
		return result

	def pick_category_data_for_list_2d(self, input_list_2d, list_no):
		"""
		2차원자료의 리스트에서 y줄번호를 입력하면, 그줄의 고유한 값들만 돌려주는것
		제목이나 카테고리를 만들려고 한다

		:param input_list_2d:
		:param list_no:
		:return:
		"""
		result = []
		for no in list_no:
			temp = set([])
			for list_1d in input_list_2d:
				if list_1d[no]:
					temp.add(list_1d[no])
			result.append(list(temp))
		return result

	def pick_data_for_int_n_str_for_list_2d(self, input_list_2d):
		return self.filter_list_2d_for_int_n_str(input_list_2d)

	def pick_int_datas_at_input_list(self, input_list):
		"""
		입력리스트중에 정수만 골라내는 것

		:param input_list:
		"""
		result = False
		for one in input_list:
			if type(123) == type(one):
				result = one
				break
		return result

	def pick_nea_element_from_list_1d_as_random_n_duplicate(self, input_list_1d, qty, random_tf=True, unique_tf=True):
		"""
		입력으로 들어오는 리스트자료를 변경 => 그안에서 qty만큼 골라내는데, 랜덤하게 할것인지 중복이 가능하게 할것인지를 적선택해서 하는 것

		:param input_list_1d: 입력으로 들어오는 1차원의 리스트 자료
		:param qty: 몇개를 리스트로 만들것인지
		:param random_tf:
		:param unique_tf:
		:return:
		"""
		if len(input_list_1d) < qty:
			qty = len(input_list_1d)
		if random_tf:
			random.shuffle(input_list_1d)
		if unique_tf:
			result = input_list_1d[:qty]
		else:
			result = []
			for _ in range(qty):
				result.append(random.choice(input_list_1d))
		return result

	def pick_str_data(self, input_list):
		"""
		문자형 자료만 추출하는것

		:param input_list:
		:return:
		"""
		result = set()
		temp_list = []
		for one_data in input_list:
			temp = self.pick_str_data_only(one_data, temp_list)
			result.update(temp)

	def pick_str_data_only(self, one_value, result=[]):
		"""
		문자형 자료만 골라내는 것

		:param one_value:
		:param result:
		:return:
		"""
		if type(one_value) == type(None):
			pass
		elif type(one_value) == type([]):
			for one in one_value:
				self.pick_str_data_only(one, result)
		elif type(one_value) == type(()):
			for one in one_value:
				self.pick_str_data_only(one, result)
		elif type(one_value) == type("abc"):
			result.append(one_value)
		elif type(one_value) == type(123):
			pass
		elif type(one_value) == type(123.45):
			pass
		elif type(one_value) == type(True) or type(one_value) == type(False):
			pass
		return result

	def pick_unique_col_name_compare_table_col_name(self, table_name, data2):
		"""
		고유한 컬럼만 골라낸다

		:param table_name:
		:param data2:
		:return:
		"""
		result = []
		columns = self.get_all_filename_in_folder(table_name)
		update_data2 = self.delete_waste_data_in_input_data_except_num_eng(data2)
		for temp_3 in update_data2:
			if not temp_3.lower() in columns:
				result.append(temp_3)
		return result

	def pick_ylines_at_list_2d(self, input_list_2d, list_1d):
		"""
		2차원의 자료를 [1,3,5]의 형태로 필터링해서 새로운 2차원자료를 만드는 것

		:param input_list_2d:
		:param list_1d:
		:return:
		"""
		result = []
		for one_list in input_list_2d:
			temp = []
			for index in list_1d:
				temp.append(one_list[index])
				result.append(temp)
		return result

	def plus_two_list(self, input_list_1, input_list_2):
		"""
		두개의 리스트를 각 우치에따라서 더하기

		:param input_list_1:
		:param input_list_2:
		:return:
		"""
		result = []
		for x, y in zip(input_list_1, input_list_2):
			result.append(x + y)
		return result

	def plus_two_list_with_same_len(self, input_list_2d_1, input_list_2d_2):
		"""
		선택한 영역이 2개를 서로 같은것을 기준으로 묶을려고하는것이다
		제일앞의 한즐이 같은것이다
		만약 묶을려고 할때 자료가 없을때는 그 기준자료만큼 빈자료를 넣어서 다음자료를 추가하는 것이다

		:param input_list_2d_1:
		:param input_list_2d_2:
		:return:
		"""
		no_of_list_2d_1 = len(input_list_2d_1[0]) - 1
		no_of_list_2d_2 = len(input_list_2d_2[1]) - 1
		empty_list_2d_1 = [""] * no_of_list_2d_1
		empty_list_2d_2 = [""] * no_of_list_2d_2
		# 리스트형태로는 코드가 더 길어질것으로 보여서 입력자료를 사전으로 변경 한것
		temp_dic = {}
		for one in input_list_2d_1:
			temp_dic[one[0]] = one[1:]
		checked_list = []
		# 기준이 되는 자료에 항목이 있을때
		for one in input_list_2d_2:
			if one[0] in temp_dic.keys():
				temp_dic[one[0]] = list(temp_dic[one[0]]) + list(one[1:])
			else:
				temp_dic[one[0]] = empty_list_2d_1 + list(one[1:])
			checked_list.append(one[0])
		# 기준자료에 항목이 없는것에 대한것
		for one in temp_dic.keys():
			if not one in checked_list:
				temp_dic[one] = list(temp_dic[one]) + empty_list_2d_2
		# 사전형식을 리스트로 다시 만드는것
		result = []
		for one in temp_dic:
			result.append([one] + list(temp_dic[one]))
		return result

	def popup_notification(self, input_text, second):
		"""
		몇초후에 팝업창이 자동으로 사라지는것

		:param input_text:
		:param second:
		:return:
		"""
		shell = win32com.client.Dispatch('WScript.Shell')
		intReturn = shell.Popup(input_text, second)

	def pre_treatment(self, input_list_2d):
		"""
		자료의 전처리
		자료들중에 변경을 할 자료들을 처리한다

		:param input_list_2d:
		:return:
		"""
		unique_data = collections.Counter()
		for data_1d in input_list_2d:
			value = str(data_1d[0])
			for new_word in [["(주)", ""], ["주식회사", ""], ["(유)", ""], ["유한회사", " "]]:
				value = value.replace(new_word[0], new_word[1])
				value = value.lower()
			unique_data.update([value])
			result = list(unique_data.keys())
		return result

	def print_2d(self, *input_list):
		"""
		2차원 리스트자료를 한줄씩 프린틓주는 것

		:param input_list:
		:return:
		"""

		for input_2d in input_list:
			if type(input_2d) == type([]):
				print("[")
				for one in input_2d:
					print(one, ",")
				print("]")
			elif type(input_2d) == type(()):
				print("(")
				for one in input_2d:
					print(one, ",")
				print(")")
			else:
				print(input_2d)

	def print_by_step(self, input_list_2d, input_step):
		"""
		입력한 자료를 원하는 갯수만큼씩 프린트하는 방법이다
		개당은 짧은데, 하나씩 하면 짧아서 몇개씩

		:param input_list_2d:
		:param input_step:
		:return:
		"""
		print("[")
		for one in range(0, len(input_list_2d), input_step):
			print(str(input_list_2d[one:one + input_step])[1:-1] + ",")
		print("]")

	def print_dic_one_by_one(self, dct):
		"""
		사전형식의 자료를 하나씩 한줄로 사전형식으로 나타나도록 하는것

		:param dct:
		:return:
		"""
		for key, value in dct.items():
			if type(key) == type("string"): key = "'" + key + "'"
			if type(value) == type("string"): value = "'" + value + "'"

	def print_list_one_by_one(self, list_2d):
		"""
		2차원자료를 한줄씩 나타나도록 하는것

		:param list_2d:
		:return:
		"""

		if type(list_2d[0]) == type([]):
			print("[")
			for index, one in enumerate(list_2d):
				print("{}".format(one))
			print("]")

	def print_one_by_one(self, input_list):
		"""
		리스트를 하나씩 출력하는것

		:param input_list:
		:return:
		"""
		for one in input_list:
			print(one)

	def random_set(self, digit=2, total_no=1, letters="가나다라마바사아자차카타파하"):
		"""
		입력으로들어오는 것을 랜덤하여 갯수만큼 자료를 만드는것

		:param digit:
		:param total_no:
		:param letters:
		:return:
		"""
		result = []
		for no in range(total_no):
			temp = ""
			for one in range(digit):
				number = random.choice(letters)
				temp = temp + str(number)
			result.append(temp)
		return result

	def random_set_for_number(self, digit=2, total_no=1):
		"""
		입력으로들어오는 것을 랜덤하여 갯수만큼 자료를 만드는것

		:param digit:
		:param total_no:
		:return:
		"""
		result = []
		for no in range(total_no):
			temp = ""
			for one in range(digit):
				num = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
				temp = temp + str(num)
			result.append(temp)
		return result

	def read_all_filename_in_folder(self, directory):
		"""폴더 안의 화일을 읽어오는것 메뉴에서 제외
		:param
		directory:
		"""
		result = []

		try:
			filenames = os.listdir(str(directory))
		except:
			filenames = os.listdir(str(directory).replace("\\", "/"))
		for filename in filenames:
			full_filename = os.path.join(directory, filename)
			result.append(filename)
		return result

	def read_any_encoding_text_as_list(self, i_path):
		"""
		어떤 텍스트라도 읽어오기
		text 자료를 읽어오기
		어떤 텍스트형태라도 읽어오기
		default = ANSI
		osv 는 utf-8 로만하면 에러가 나기도 함, uTF-8-sig
		UTF-16

		:param i_path:
		:return:
		"""
		result = []
		encoding_set = ["utf-8", "ansi", "UTE-8-sig", "utf-16", ]
		for a_coding in encoding_set:
			try:
				f = open(i_path, 'r', encoding=a_coding)
				while True:
					line = f.readline()
					if not line: break
					result.append(line)
				f.close()
				if result != []:
					print(a_coding, result)
					return result
			except:
				pass

	def read_code_for_python_file(self, filename):
		"""
		py로 만들어진 화일을 불러온다

		:param filename:
		:return:
		"""
		temp_list = []
		result = []

		try:
			f = open(filename, mode='r', encoding='cp949')
			lines = f.readlines()
		finally:
			f = open(filename, mode='r', encoding='utf-8')
			lines = f.readlines()
			print(lines)

		original = lines
		lines = list(map(lambda s: s.strip(), lines))
		start_no = 0
		for no in range(len(lines)):
			print(filename, no)
			line = lines[no]

			changed_line = line.strip()
			changed_line = changed_line.replace("\n", "")
			if changed_line[0:3] == "def" and temp_list != []:
				print("처음은 ===> ", start_no)
				print("끝은 ===> ", no)
				temp_list.insert(0, [start_no, no])
				result.append(temp_list)
				start_no = no
				# print(temp_list)
				temp_list = []
			if changed_line != "" and changed_line[0] != "#":
				temp_list.append(changed_line)
		f.close()
		return [result, original]

	def read_csv_text_file_as_list_1d(self, filename, seperate_by=","):
		"""
		seperate_by = \t, ' ', '+'

		:param filename:
		:return:
		"""

		encoding_set = ["utf-8", "ansi", "UTE-8-sig", "utf-16", ]
		result = []
		for a_coding in encoding_set:
			try:
				with open(filename, 'r', encoding=a_coding) as file:
					reader = csv.reader(file, delimiter=seperate_by)
					for row in reader:
						result.append(row)
				return result
			except:
				pass

	def read_df_by_name(self, df_obj, x, y):
		"""
		열이나 행의 이름으로 pandas의 dataframe의 일부를 불러오는 것이다
		이것은 리스트를 기본으로 사용한다
		list_x=["가"~"다"] ===> "가"~"다"열
		list_x=["가","나","다","4"] ===> 가,나,다, 4 열
		x=""또는 "all" ===> 전부
		"""

		temp = []
		for one in [x, y]:
			if ":" in one[0]:
				changed_one = one[0]
			elif "~" in one[0]:
				ed_one = one[0].split("~")
				changed_one = "'" + str(ed_one[0]) + "'" + ":" + "'" + str(ed_one[1]) + "'"

			elif "all" in one[0]:
				changed_one = one[0].replace("all", ":")
			else:
				changed_one = one
			temp.append(changed_one)
		# 이것중에 self를 사용하지 않으면 오류가 발생한다
		print(temp)
		exec("self.result = df_obj.loc[{}, {}]".format(temp[0], temp[1]))
		return self.result

	def read_df_by_no(self, df_obj, x, y):
		"""
		dataframe객체를 x,y번호를 기준으로 읽어오는 것

		:param df_obj:
		:param x:
		:param y:
		:return:
		"""
		example = """
			숫자번호로 pandas의 dataframe의 일부를 불러오는 것
			단, 모든것을 문자로 넣어주어야 한다
			x=["1:2", "1~2"] ===> 1, 2열
			x=["1,2,3,4"] ===> 1,2,3,4열
			x=[1,2,3,4]  ===> 1,2,3,4열
			x=""또는 "all" ===> 전부
			"""

		self.manual["df_read_byno"] = {
			"분류1": "pandas, dataframe",
			"설명": "pandas의 dataframe의 자료의 일부를 쉽게 갖고오도록 만든것",
			"입력요소": "df_obj, x, y",
			"기타설명": example
		}
		x_list = self.df_check_range(x)
		y_list = self.df_check_range(y)
		exec("self.result = df_obj.iloc[{}, {}]".format(x_list, y_list))
		return self.result

	def read_df_by_xy(self, df_obj, xy=[0, 0]):
		"""
		위치를 기준으로 값을 읽어오는 것이다
		숫자를 넣으면 된다
		"""
		result = df_obj.iat[int(xy[0]), int(xy[1])]
		return result

	def read_doc_in_each_object_method_name(self, object):
		"""
		객체를 주면 메소드의 help를 돌려 주는것
		"""
		result = {}
		for one in dir(object):
			temp = []
			if not one.startswith('__'):
				try:
					temp.append(one)
					# print(one)
					temp.append(getattr(object, one).__doc__)
				# print(getattr(obgect, one).__doc__)
				except:
					pass
			result[one] = temp
		return result

	def read_file(self, filename):
		result = self.read_file_as_text(filename)
		return result

	def read_file_as_list_1d(self, file_full_name):
		"""
		화일을 리스트형태와 text형태로 2개로 돌려준다

		:param file_full_name:
		:return:
		"""
		file_object = open(file_full_name, "r", encoding="UTF-8")
		file_as_list = file_object.readlines()
		file_object.close()
		return file_as_list

	def read_file_as_text(self, filename):
		"""
		화일을 읽어오는 것

		:param filename:
		:return:
		"""
		try:
			f = open(filename, 'r', encoding='UTF-8')
			result = f.readlines()
			f.close()
		except:
			f = open(filename, 'r')
			result = f.readlines()
			f.close()
		return result

	def read_folder_filename_only_pickle(self, directory="./", filter="pickle"):
		"""
		pickle로 만든 자료를 저장하는것
		"""
		result = []
		all_files = os.listdir(directory)
		if filter == "*" or filter == "":
			filter = ""
			result = all_files
		else:
			filter = "." + filter
			for x in all_files:
				if x.endswith(filter):
					result.append(x)
		return result

	def read_method_code_by_method_name(self, str_method_name):
		"""
		메소드의 코드를 읽어오는것
		문자로 넣을수있도록 만든 것이다

		:param str_method_name:
		:return:
		"""
		# method_name = eval(str_method_name)
		code_text = inspect.getsource(str_method_name)
		return code_text

	def read_pickle_file(self, i_full_filename):
		"""

		:param path_n_name:
		:return:
		"""
		with open(i_full_filename, "rb") as fr:
			result = pickle.load(fr)
		return result

	def read_pickle_filenames_in_folder(self, directory="./", filter="pickle"):
		"""
		pickle로 만든 자료를 저장하는것
		"""
		result = []
		all_files = os.listdir(directory)
		if filter == "*" or filter == "":
			filter = ""
			result = all_files
		else:
			filter = "." + filter
			for x in all_files:
				if x.endswith(filter):
					result.append(x)
		return result

	def read_pxy_for_mouse(self):
		"""
		마우스의 위치를 pxcel값으로 읽어오는 것

		:return:
		"""
		position = pyautogui.position()
		return [position.x, position.y]

	def read_screen_size(self):
		"""
		화면 사이즈를

		:return:
		"""
		result = win32api.GetSystemMetrics()
		return result

	def read_size_for_list_2d(self, input_list_2d):
		"""
		입력값으로 온것의 크기를 돌려주는것

		:param input_list_2d:
		:return:
		"""
		len_x = len(input_list_2d)
		len_y = len(input_list_2d[0])
		return [len_x, len_y]

	def read_system_current_path(self, path=""):
		"""
		현재의 경로를 돌려주는것

		:param path:
		:return:
		"""
		result = os.getcwd()
		return result

	def read_system_encodeing_type(self, ):
		"""
		기본적인 시스템에서의 인코딩을 읽어온다
		"""
		system_in_basic_incoding = sys.stdin.encoding
		system_out_basic_incoding = sys.stdout.encoding
		print("시스템의 기본적인 입력시의 인코딩 ====> ", system_in_basic_incoding)
		print("시스템의 기본적인 출력시의 인코딩 ====> ", system_out_basic_incoding)

	def read_text_file_as_list(self, i_path):
		"""
		어떤 텍스트라도 읽어오기
		text 자료를 읽어오기
		어떤 텍스트형태라도 읽어오기
		default = ANSI
		osv 는 utf-8 로만하면 에러가 나기도 함, uTF-8-sig
		UTF-16

		:param i_path:
		:return:
		"""
		result = []
		encoding_set = ["utf-8", "ansi", "UTE-8-sig", "utf-16", ]
		for a_coding in encoding_set:
			try:
				f = open(i_path, 'r', encoding=a_coding)
				while True:
					line = f.readline()
					if not line: break
					result.append(line)
				f.close()
				if result != []:
					print(a_coding, result)
					return result
			except:
				pass

	def read_text_file_as_list_1d(self, filename):
		encoding_set = ["utf-8", "ansi", "UTE-8-sig", "utf-16", ]
		for a_coding in encoding_set:
			try:
				f = open(filename, 'r', encoding=a_coding)
				lines = f.readlines()
				f.close()
				return lines
			except:
				pass

	def read_text_file_as_one_text(self, filename):
		result = ""
		list_1d = self.read_text_file_as_list_1d(filename)
		for one_line in list_1d:
			result = result + one_line
		return result

	def regroup_for_old_group_as_new_step(self, all_data, initial_group, step):
		"""
		기존에 그룹화되어있는것을 기준으로, 최대갯수가 step의 갯수만큼 되도록 다시 그룹화 하는것이다

		:param all_data:
		:param initial_group:
		:param step:
		:return:
		"""
		result = []
		for list_1d in initial_group:
			if len(list_1d) > step:
				repeat_no = int((len(list_1d) + step - 1) / step)
				for no in range(repeat_no - 1):
					result.append(list_1d[no * step:(no + 1) * step])
				result.append(list_1d[(repeat_no - 1) * step:])
			else:
				result.append(list_1d)
		remain_all_data = all_data
		for list_1d in initial_group:
			for one_value in list_1d:
				remain_all_data.remove(one_value)
		result.append(remain_all_data)
		return result

	def remain_list_unique_value(self, input_datas, status=0):
		"""
		중복된 리스트의 자료를 없애는 것이다. 같은것중에서 하나만 남기고 나머지는 []으로 고친다

		:param input_datas:
		:param status:
		:return:
		"""
		if status == 0:
			result = []
			# 계속해서 pop으로 하나씩 없애므로 하나도 없으면 그만 실행한다
			while len(input_datas) != 0:
				gijun = input_datas.pop()
				sjpark = 0
				result.append(gijun)
				for num in range(len(input_datas)):
					if input_datas[int(num)] == []:  # 빈자료일때는 그냥 통과한다
						pass
					if input_datas[int(num)] == gijun:  # 자료가 같은것이 있으면 []으로 변경한다
						sjpark = sjpark + 1
						input_datas[int(num)] = []
		else:
			# 중복된것중에서 아무것도없는 []마저 없애는 것이다. 위의 only_one을 이용하여 사용한다
			# 같은것중에서 하나만 남기고 나머지는 []으로 고친다
			# 이것은 연속된 자료만 기준으로 삭제를 하는 것입니다
			# 만약 연속이 되지않은 같은자료는 삭제가 되지를 않읍니다
			result = list(self.remain_list_unique_value(input_datas))
			for a in range(len(result) - 1, 0, -1):
				if result[a] == []:
					del result[int(a)]
		return result

	def remove_duplicate_files(self, reference_folder, parent_folder):
		"""
		같은 화일을 삭제하는 것

		:param reference_folder:
		:param parent_folder:
		:return:
		"""
		# parent folder 내의 모든 하위 폴더를 탐색
		for root, dirs, _ in os.walk(parent_folder):
			for dir in dirs:
				target_folder = os.path.join(root, dir)
				# target folder 내의 파일을 기준 폴더와 비교
				for sub_root, _, files in os.walk(target_folder):
					for file in files:
						target_file_path = os.path.join(sub_root, file)
						reference_file_path = os.path.join(reference_folder, os.path.relpath(target_file_path, target_folder))
						# 기준 폴더에 동일한 파일이 있는지 확인하고, 파일 내용이 동일한지 비교
						if os.path.exists(reference_file_path) and filecmp.cmp(reference_file_path, target_file_path, shallow=False):
							print(f"Removing duplicate file: {target_file_path}")
							os.remove(target_file_path)

	def remove_elements_of_list_1d_for_list_2d_by_index_list(self, input_list_2d, no_list):
		"""
		2차원 자료에서
		원하는 순서들의 자료를 삭제하는 것
		입력형태 : 2차원리스트, [2,5,7]

		:param input_list_2d:
		:param no_list:
		:return:
		"""
		no_list.sort()
		no_list.reverse()
		for one in no_list:
			for x in range(len(input_list_2d)):
				del input_list_2d[x][one]
		return input_list_2d

	def remove_empty_folders_including_sub_folders(self, input_full_path):
		"""
		모든 하위 폴더를 순회하면서 빈 폴더들만 삭제하는 코드
		주어진 경로의 모든 하위 폴더를 탐색

		:param input_full_path:
		:return:
		"""
		for root, dirs, files in os.walk(input_full_path, topdown=False):
			for dir in dirs:
				dir_path = os.path.join(root, dir)  # 폴더가 비어있는지 확인
				if not os.listdir(dir_path):
					print(f"Removing empty folder: {dir_path}")
					os.rmdir(dir_path)

	def replace_elements_as_space_for_list_1d_by_step(self, input_list, step, start=0):
		"""
		1차원의 자료중에서 원하는 순서째의 자료를 ""으로 만드는것
		"""
		if start != 0:
			result = input_list[0:start]
		else:
			result = []

		for num in range(start, len(input_list)):
			temp_value = input_list[num]
			if divmod(num, step)[1] == 0:
				temp_value = ""
			result.append(temp_value)

		return result

	def replace_list_1d_element_as_space_by_step(self, input_list, step, start=0):
		"""
		1차원의 자료중에서 원하는 순서째의 자료를 ""으로 만드는것
		"""
		if start != 0:
			result = input_list[0:start]
		else:
			result = []

		for num in range(start, len(input_list)):
			temp_value = input_list[num]
			if divmod(num, step)[1] == 0:
				temp_value = ""
			result.append(temp_value)

		return result

	def replace_many_times_with_jf_sql(self, jf_sql_list, replace_word_list, input_text):
		"""
		하나의 값을 여러 sql로 계속 값을 변경하는 것

		:param jf_sql_list:
		:param replace_word_list:
		:param input_text:
		:return:
		"""
		re_sql_list = []
		for one in jf_sql_list:
			re_sql_list.append(self.xre.inder(one))
			for index, one_re_sql in enumerate(re_sql_list):
				input_text = re.sub(one_re_sql, replace_word_list[index], input_text, flags=re.MULTILINE)
		return input_text

	def replace_text_between_a_and_b(self, input_text, start_no, end_no, replace_text):
		"""
		텍스트문장에서 번호를 기준으로 a번호에서 b번호까지의 글자를 바꾸는것으로
		번호를 기준으로 바꾸는 기능을 만든것이다
		보통 어떤 단어나 문장을 바꾸는것은 있어도, 번호를 기준으로 바꾸는것은 없어서, 만든것이며
		정규표현식에서 찾은것이 숫자로 되어있어서 그것을 이용하기 위해 만든 것이다

		:param input_text:
		:param start_no:
		:param end_no:
		:param replace_text:
		:return:
		"""
		front = input_text[:start_no]
		end = input_text[end_no:]
		result = front + replace_text + end
		return result

	def replace_text_word(self, input_text, before_text, after_text):
		"""
		폰트와 글자를 주면, 필셀의 크기를 돌려준다
		"""
		result = input_text.replace(before_text, after_text)
		return result

	def replace_value_for_list_1d_by_step(self, input_list, input_text, step, start=0):
		"""
		1차원의 자료중에서 원하는 순서째의 자료를 원하는 값으로 바꾸는 것

		:param input_list:
		:param step:
		:param start:
		:return:
		"""
		if start != 0:
			result = input_list[0:start]
		else:
			result = []

		for num in range(start, len(input_list)):
			temp_value = input_list[num]
			if divmod(num, step)[1] == 0:
				temp_value = input_text
			result.append(temp_value)
		return result

	def reset_for_input_setup(self, input_setup_dic=""):
		"""
		들어오는 사전형식의 모든 값을 None로 설정하는 것
		보통 설정을 위해 사용하는 것의 모든 값을 삭제하는 것이다
		input_setup_dic의 형태는 아래의 형식을 따릅니다
		self.vars["setup"]["line"]={}
		self.vars["setup"]["line"]["color"] = "red"
		self.vars["setup"]["line"]["thickness"] = "thin"
		단, 그안의 key값을 삭제하지는 않는다

		:param input_setup_dic:
		:return:
		"""
		top_key = input_setup_dic.keys()[0]
		for one_key in input_setup_dic[top_key].keys():
			input_setup_dic[top_key][one_key] = None

	def reset_with_default_for_input_setup(self, input_setup_dic, default_value_dic=""):
		"""
		들어오는 사전형식의 모든값을 None로 설정하는 것
		보통 설정을 위해 사용하는 것의 모든 값을 삭제하는 것이다
		만약 default값을 먼저 설정해 놓고 싶으면
		self.vars["default"]["line"] = {"color":"red", "thickness":"thin"} 이렇게 먼저 해놓으면된다

		:param input_setup_dic:
		:return:
		"""
		self.reset_for_input_setup(input_setup_dic)
		if not default_value_dic:
			default_value_dic = self.vars["default"][default_value_dic.keys()[0]]

		top_key = input_setup_dic.keys()[0]
		for one_key in default_value_dic.keys():
			input_setup_dic[top_key][one_key] = default_value_dic[one_key]

	def resize_list(self, xy_list, resize=[1, 1]):
		"""
		리스트의 크기를 다시 설정하는 것
		"""
		result = []
		# 자료의 x갯수를 요청한것과 비교
		if len(xy_list) < resize[0] or resize[0] == 0:
			pass
		else:
			xy_list = xy_list[:resize[0]]
		# 자료의 y갯수를 요청한것과 비교
		for x_list in xy_list:
			if len(x_list) < resize[1] or resize[1] == 0:
				pass
			else:
				x_list = xy_list[:resize[0]]
			result.append(x_list)
		return result

	def resize_list_1(self, input_list="", xy=""):
		"""
		입력으로 들어온 자료를 2차원으로 만든후
		xy로 넘어온 자료를 기준으로 만드는 것이다
		사이즈의 크기에 따라서 들어온 자료를 만든다
		"""
		result = []
		x_len, y_len = xy
		list1_max_len = len(input_list)
		list2_max_len = 0

		# 최대의 길이를 구한다
		for one_value in input_list:
			if type(one_value) == type([]):
				if list2_max_len < len(one_value):
					list2_max_len = len(one_value)

		for one_value in input_list:
			temp_list = []
			# 모든 항목을 리스트형태로 만든다
			if type(one_value) != type(one_value):
				temp_list = temp_list.append(one_value)
			else:
				temp_list = one_value

			# 최대길이에 맞도록 적은것은 ""으로 갯수를 채운다
			if list2_max_len - len(temp_list) > 0:
				for no in range(list2_max_len - len(temp_list)):
					temp_list.append("")
			result.append(temp_list)

		if xy != "":
			# x갯수를 정리한다
			if x_len < len(result):
				changed_result_2 = result[0:x_len]
			# y갯수를 정리한다
			changed_result_3 = []
			if y_len < len(changed_result_2[0]):
				for one_list in changed_result_2:
					changed_result_3.append(one_list[0:y_len])
			else:
				changed_result_3 = changed_result_2
			result = changed_result_3

		return result

	def resize_list_1d_to_list_2d_by_step(self, all_data, initial_group, step):
		"""
		기존에 그룹화되어있는것을 기준으로, 최대갯수가 step의 갯수만큼 되도록 다시 그룹화 하는것이다

		:param all_data:
		:param initial_group:
		:param step:
		:return:
		"""
		result = []
		for list_1d in initial_group:
			if len(list_1d) > step:
				repeat_no = int((len(list_1d) + step - 1) / step)
				for no in range(repeat_no - 1):
					result.append(list_1d[no * step:(no + 1) * step])
				result.append(list_1d[(repeat_no - 1) * step:])
			else:
				result.append(list_1d)
		remain_all_data = all_data
		for list_1d in initial_group:
			for one_value in list_1d:
				remain_all_data.remove(one_value)
		result.append(remain_all_data)
		return result

	def resize_list_2d(self, input_list_2d, x_start, y_start, x_len, y_len):
			"""
			2	차원	리스트의	사이즈를	변경하는	것	2	차원안의	1차원자료를	몇개씩	줄여서	새롭게	2차원자료를	만드는	것이다

			:param 	input_list_2d:
			:param	x_start:
			:param	y_start:
			:param	x_len:
			:param	y_len:
			:return:
			"""
			result = []
			if len(input_list_2d) >= x_start + x_len and len(input_list_2d[0]) >= y_start + y_len:
				changed_list_2d = input_list_2d[x_start:x_start + x_len - 1]
				for list_1d in changed_list_2d:
					result.append(list_1d[y_start:y_start + y_len - 1])
			return result

	def resize_list_2d(self, input_list_2d, x_start, y_start, x_len, y_len):
		"""
		2차원 리스트의 사이즈를 변경하는 것
		2차원안의 1차원자료를 몇개씩 줄여서 새롭게 2차원자료를 만드는 것이다

		:param input_list_2d:
		:param x_start:
		:param y_start:
		:param x_len:
		:param y_len:
		:return:
		"""
		result = []
		if len(input_list_2d) >= x_start + x_len and len(input_list_2d[0]) >= y_start + y_len:
			changed_list_2d = input_list_2d[x_start:x_start + x_len - 1]
			for list_1d in changed_list_2d:
				result.append(list_1d[y_start:y_start + y_len - 1])
		return result

	def resize_list_2d_by_xy_step(self, xy_list, resize=[1, 1]):
		"""
		리스트의 크기를 다시 설정하는 것
		메뉴에서 제외

		:param xy_list:
		:param resize:
		:return:
		"""
		result = []
		# 자료의 x갯수를 요청한것과 비교
		if len(xy_list) < resize[0] or resize[0] == 0:
			pass
		else:
			xy_list = xy_list[:resize[0]]
		# 자료의 y갯수를 요청한것과 비교
		for x_list in xy_list:
			if len(x_list) < resize[1] or resize[1] == 0:
				pass
			else:
				x_list = xy_list[:resize[0]]
			result.append(x_list)
		return result

	def reverse_int(self, input_int):
		"""
		숫자를 문자로 바꾼후, 뒤집은다음에 다시 숫자로 만드는 것
		문자열을 앞뒤를 바꿔서 반대로 만들어 주는 것

		:param input_text:
		:return:
		"""
		input_text = str(input_int)
		text2list = list(input_text)
		text2list.reverse()
		result = "".join(text2list)
		result = int(result)
		return result

	def reverse_text(self, input_text):
		"""
		문자열을 앞뒤를 바꿔서 반대로 만들어 주는 것

		:param input_text:
		:return:
		"""
		text2list = list(input_text)
		text2list.reverse()
		result = "".join(text2list)
		return result

	def rotate_xy_by_degree(self, xy, degree):
		"""
		좌표를 각도를 넣어서 회전하는 좌표를 주는 것

		:param xy:
		:param degree:
		:return:
		"""
		rad = degree * (math.pi / 180.0)
		x2 = round(math.cos(rad) * xy[0] - math.sin(rad) * xy[1])
		y2 = round(math.sin(rad) * xy[0] + math.cos(rad) * xy[1])
		return [x2, y2]

	def run_file(self, file_full_path):
		"""
		원하는 화일을 open하는 것

		:param filename:
		"""
		os.startfile(file_full_path)

	def run_notepad_and_paste(self):
		"""
		노트패드를 실행시키고
		붙여넣기를 실행시키는 것이다
		노트패드는 com인터페이스가 없다
		"""
		shell = win32com.client.Dispatch("WScript.Shell")
		shell.Run("notepad")
		shell.AppActivate("notepad")
		shell.SendKeys("^v", 0)

	def run_python_file(self, filename):

		encoding_set = ["utf-8", "ansi", "UTE-8-sig", "utf-16", ]
		for a_coding in encoding_set:
			try:
				f = open(filename, 'r', encoding=a_coding)
				lines = f.readlines()
				f.close()
				exec(lines)
			except:
				pass

	def sample_pre_treatment(self, input_list_2d):
		"""
		자료의 전처리
		자료들중에 변경을 할 자료들을 처리한다

		:param input_list_2d:
		:return:
		"""
		unique_data = collections.Counter()
		for data_1d in input_list_2d:
			value = str(data_1d[0])
			for new_word in [["(주)", ""], ["주식회사", ""], ["(유)", ""], ["유한회사", " "]]:
				value = value.replace(new_word[0], new_word[1])
				value = value.lower()
			unique_data.update([value])
			result = list(unique_data.keys())
		return result

	def save_dic_1d_as_csv_text_file_by_key_value_pair(self, filename, input_dic):
		"""
		사전형자료를 key와 value쌍으로 연속해서 만든 문자열형태로 CSV 파일로 저장하는것

		:param filename:
		:param input_dic:
		:return:
		"""
		list_2d = input_dic.items()
		with open(filename, "w", new_line='', encoding="utf-8") as file:
			writer = csv.writer(file)
			writer.writerows(list_2d)

	def save_file_as_pickle(self, input_data="", path_n_name=""):
		"""
		피클로 객체를 저장하는것
		"""
		if ":" in path_n_name:
			full_filename = path_n_name
		else:
			full_filename = "./" + path_n_name
		with open(str(full_filename) + ".pickle", "wb") as fr:
			pickle.dump(input_data, fr)

	def save_list_2d_as_csv_text_file(self, filename, list_2d):
		"""
		2차원 리스트자료를 CSV 파일로 만드는 것

		:param filename:
		:param list_2d:
		:return:
		"""
		with open(filename, "w", new_line='', encoding="utf-8") as file:
			writer = csv.writer(file)
			writer.writerows(list_2d)

	def save_pickle(self, input_object="", filename="", path="D:\\"):
		"""
		자료를 pickle 로 저장하는것

		:param input_object:
		:param filename:
		:param path: 경로
		:return:
		"""
		if not "." in filename:
			filename = filename + ".pickle"
		with open(path + filename, "wb") as fr:
			pickle.dump(input_object, fr)

	def save_text_file(self, file_full_name, input_text):
		"""
		텍스트자료를 화일로 저장하는것

		:param file_full_name:
		:param input_text:
		:return:
		"""
		new_file = open(file_full_name, "w", encoding="UTF-8")
		for one_line in input_text:
			new_file.write(one_line)

	def screen_capture(self, filename="D:Wtemp_101.jpg"):
		"""
		스크린 캡쳐를 해서, 화면을 저장하는 것

		:param filename:
		:return:
		"""
		pyautogui.screenshot(filename)
		return filename

	def screen_scroll(self, input_no):
		"""
		현재 위치에서 상하로 스크롤하는 기능 #위로 올리는것은 +숫자，내리는것은 -숫자로 사용
		"""
		pyautogui.scroll(input_no)

	def search_eng_in_text(self, input_text):
		"""
		단어중에 나와있는 영어만 분리하는기능
		"""
		re_compile = re.compile(r"([a-zA-Z]+)")
		result = re_compile.findall(input_text)
		new_result = []
		for dim1_data in result:
			for dim2_data in dim1_data:
				new_result.append(dim2_data)
		return new_result

	def search_num_in_text(self, input_text):
		"""
		단어중에 나와있는 숫자만 분리하는기능
		"""
		re_compile = re.compile(r"([0-9]+)")
		result = re_compile.findall(input_text)
		new_result = []
		for dim1_data in result:
			for dim2_data in dim1_data:
				new_result.append(dim2_data)
		return new_result

	def select_list_1d_unique_y(self, data1, data2):
		"""
		고유한 컬럼만 골라낸다
		"""
		result = []
		columns = self.read_y_names(data1)
		update_data2 = self.delete_waste_data_for_list(data2)

		for temp_3 in update_data2:
			if not temp_3.lower() in columns:
				result.append(temp_3)
		return result

	def seperate_num_char(self, raw_data):
		"""
		2005년 12월 9일 추가
		문자와숫자를 분리해서 리스트로 돌려주는 것이다
		123wer -> ['123','wer']
		분류라는 의미 -> seperate를 사용하고, 어떤것들을 분리할지를 언급한다 (숫자, 문자)

		:param raw_data:
		:return:
		"""
		temp = ""
		result = []
		int_temp = ""
		datas = str(raw_data)
		for num in range(len(datas)):
			if num == 0:
				temp = str(datas[num])
			else:
				try:
					fore_var = int(datas[num])
					fore_var_status = "integer"
				except:
					fore_var = datas[num]
					fore_var_status = "string"
				try:
					back_var = int(datas[num - 1])
					back_var_status = "integer"
				except:
					back_var = datas[num - 1]
					back_var_status = "string"

				if fore_var_status == back_var_status:
					temp = temp + datas[num]
				else:
					result.append(temp)
					temp = datas[num]
		if len(temp) > 0:
			result.append(temp)
		return result

	def set_cursor_pos(self):
		"""
		커서의 옮기는 것
		:return:
		"""
		pos = (200, 200)
		win32api.SetCursorPos(pos)

	def set_limitation_for_mouse(self, xyxy_list):
		"""
		(left, top, right, bottom) 영역으로 마우스 커서 제한하기
		win32api.ClipCursor((200, 200, 700, 700))

		마우스 커서 제한 해제하기
		win32api.ClipCursor((0, 0, 0, 0))
		win32api.ClipCursor()

		:return:
		"""
		win32api.ClipCursor(xyxy_list)

	def shift_two_element_position_for_list_2d_by_two_index(self, input_list_2d, input_no_list):
		"""
		2차원 리스트의 자료에서 각 라인별 2개의 위치를 바꾼는것
		change_position_for_list_2d_by_two_index([[1,2,3], [4,5,6]], [0,2])
		[[1,2,3], [4,5,6]] ==> [[3,2,1], [6,5,4]]

		:param input_list_2d: list type 2dimension, 2차원의 리스트형
		:param input_no_list:
		:return:
		"""
		for before, after in input_no_list:
			for no in range(len(input_list_2d)):
				value1 = input_list_2d[no][before]
				value2 = input_list_2d[no][after]
				input_list_2d[no][before] = value2
				input_list_2d[no][after] = value1
		return input_list_2d

	def similar(self, a, b):
		"""
		유사성을 계산해서 갖고오는 것

		:param a:
		:param b:
		:return:
		"""
		return difflib.SequenceMatcher(None, a, b).ratio()

	def similar_test_with_two_words(self, input_list_1d, base_num=0.6):
		"""
		입력된 자료에서 유사도를 검사해서 기본설정값보다 높은 값들의 자료만 갖고옮

		:param input_list_1d:
		:param base_num:
		:return:
		"""
		result = []
		num = 0
		for one in input_list_1d:
			for two in input_list_1d[num:]:
				ratio = difflib.SequenceMatcher(None, one, two).ratio()
				if ratio >= base_num and ratio != 1.0:
					print(one, two, " : 유사도는 = = >", ratio)
					result.append([ratio, one, two, ])
		num = num + 1
		return result

	def sort_List_3d_by_index(self, input_List_3d, index_no=0):
		"""
		2차원 자료를 갖고있는 리스트
		번호를 넣으면, 정렬한 자료를 돌려주는 것
		"""

		result = []
		for input_list_2d in input_List_3d:
			if len(input_list_2d) == 1:
				result.append(input_list_2d)
			else:
				sorted_list_2d = self.sort_list_2d_by_index(input_list_2d, index_no)
				result.append(sorted_list_2d)
		return result

	def sort_list(self, input_data):
		"""
		aa = [[111, 'abc'], [222, 222],['333', 333], ['777', 'sjpark'], ['aaa', 123],['zzz', 'sang'], ['jjj', 987], ['ppp', 'park']]
		정렬하는 방법입니다
		"""
		result = []
		for one_data in input_data:
			for one in one_data:
				result.append(one.sort())
		return result

	def sort_list_1d(self, input_list_1d):
		"""
		1차원 리스트를 정렬하는 것

		:param input_list_1d:
		:return:
		"""

		str_temp = []
		int_temp = []
		for one in input_list_1d:
			if type(one) == type("str"):
				str_temp.append(one)
			else:
				int_temp.append(one)

		result_int = sorted(int_temp)
		result_str = sorted(str_temp)
		result = result_int + result_str
		return result

	def sort_list_1d_by_element_len(self, input_list):
		"""
		일반적인 정렬이 아니고,	문자의 길이에 따라서 정렬
		:param input_list:
		:return:
		"""
		input_list.sort(key=lambda x: len(str(x)))
		return input_list

	def sort_list_1d_by_index_list(self, source, sort_index):
		"""
		sort_index는 정렬되는 순서
		[1,-2,3] ==> 1,2,3으로 정렬을 하는데, 2번째는 역순으로 정렬한다

		:param source:
		:param sort_index:
		:return:
		"""
		temp = ""
		for one in sort_index:
			if "-" in str(one):
				temp = temp + ("-x[%s], " % (abs(one)))
			else:
				temp = temp + ("x[%s], " % (one))

		lam = ("lambda x : (%s)" % temp[:-2])

		result = sorted(source, key=eval(lam))
		return result

	def sort_list_2d(self, input_list_2d):
		"""
		2차원 리스트를 정렬하는 것

		:param input_list_2d:
		:return:
		"""
		result = self.sort_list_2d_by_index(input_list_2d, 0)
		return result

	def sort_list_2d_by_index(self, input_list_2d, index_no):
		"""
		입력 :  리스트자료
		리스트자료를 몇번째 순서를 기준으로 정렬하는것
		숫자와 문자가 같이 섞여 있어도, 정렬이 가능
		aa = [[111, 'abc'], [222, 222],['333', 333], ['777', 'sjpark'], ['aaa', 123],['zzz', 'sang'], ['jjj', 987], ['ppp', 'park']]
		value=sort_list(리스트자료, 정렬기준번호)

		:param input_list_2d:
		:param index_no:
		:return:
		"""
		print("========>", input_list_2d)
		none_temp = []
		str_temp = []
		int_temp = []

		for list_1d in input_list_2d:

			if type(list_1d[index_no]) == type(None):
				none_temp.append(list_1d)
			elif type(list_1d[index_no]) == type("str"):
				str_temp.append(list_1d)
			else:
				int_temp.append(list_1d)

		result_int = sorted(int_temp, key=lambda x: x[index_no])
		result_str = sorted(str_temp, key=lambda x: x[index_no])
		result = none_temp + result_int + result_str
		return result

	def sort_list_2d_by_yy_list(self, input_data, input_list=[0, 2, 3]):
		"""
		# Halmoney)util의 부분중에 하나를 변경
		2차원리스트를 몇번째를 기준으로 정렬하는것
		음수를 사용하면, 역으로 되는것을 적용시킴
		"""
		text = ""
		for one in input_list:
			if one >= 0:
				text = text + "row[" + str(one * -1) + "],"
			else:
				text = text + "-row[" + str(one * -1) + "],"  # <=이부분을 변경
		text = text[:-1]
		exec("global sorted_list_2d; sorted_list_2d = sorted(input_data, key=lambda row: (%s))" % text)
		global sorted_list_2d
		return sorted_list_2d

	def sort_list_3d_by_index(self, input_list_3d, index_no=0):
		"""
		3차원자료를 정렬하는것

		:param input_list_3d:
		:param index_no:
		:return:
		"""
		result = []
		for input_list_2d in input_list_3d:
			if len(input_list_2d) == 1:
				result.append(input_list_2d)
			else:
				sorted_list_2d = self.sort_list_2d_by_index(input_list_2d, index_no)
				result.append(sorted_list_2d)
		return result

	def sort_list_by_index(self, input_list, index_no=0):
		"""
		입력 :  리스트자료
		리스트자료를 몇번째 순서를 기준으로 정렬하는것
		aa = [[111, 'abc'], [222, 222],['333', 333], ['777', 'sjpark'], ['aaa', 123],['zzz', 'sang'], ['jjj', 987], ['ppp', 'park']]
		value=sort_list(리스트자료, 정렬기준번호)
		"""
		result_before = [(i[index_no], i) for i in input_list]
		result_before.sort()
		result = [i[1] for i in result_before]
		return result

	def sort_mixed_list_1d(self, input_list_1d):
		"""
		1, 2차원의 자료가 섞여서 저장된 자료를 정렬하는 것

		:param input_list_1d:
		:return:
		"""
		int_list = sorted([i for i in input_list_1d if type(i) is float or type(i) is int])
		str_list = sorted([i for i in input_list_1d if type(i) is str])
		return int_list + str_list

	def sort_python_file_by_def(self, filename):
		"""
		python으로만든 화일을 읽어서 def를 기준으로 정렬해서 돌려주는 것
		1. 프린트해서 나타냄
		2. 화일로 정렬된것을 만듦
		3. 리스트형태로 돌려주는것

		:param filename:
		:return:
		"""
		file_pointer = open(filename, 'r', encoding='utf-8')  # 텍스트 읽어오기
		file_list = file_pointer.readlines()  # 한번에 다 읽기

		all_text = ""
		temp = []
		result = {}
		title = "000"
		for one_line_text in file_list:
			# def로 시작이 되는지 알아 내는것
			if str(one_line_text).strip()[0:3] == "def" and str(one_line_text).strip()[-1] == ":":
				result[title] = temp  # def나오기 전까지의 자료를 저장합니다
				temp = []
				title = str(one_line_text).strip()  # 사전의 key를 def의 이름으로 만드는 것이다
			temp.append(one_line_text)
		result[title] = temp

		sorted_keys = list(result.keys())
		sorted_keys.sort()  # key인 제목을 기준으로 정렬을 하도록 만든것
		write_file = open("output_output_33.txt", 'w', encoding='utf-8')  # 텍스트 읽어오기

		for one_key in sorted_keys:
			for one_line in result[one_key]:
				one_line = one_line.replace("\n", "")
				# print(one_line)  # 별도로 화일로 만들지 않고, 터미널에 나타나는것을 복사해서 사용하는 방법으로 만듦
				all_text = all_text + one_line
				write_file.write(one_line + "\n")
		write_file.close()
		return result

	def sort_value(self, a, b=0):
		"""
		정렬하는 것

		:param a:
		:param b:
		:return:
		"""
		result_before = [(i[b], i) for i in a]
		result_before.sort()
		result = [i[1] for i in result_before]
		return result

	def sound_beep(self, sec=1000, hz=500):
		"""
		beep 음을 내는 것
		메뉴에서 제외

		:param sec:
		:param hz:
		:return:
		"""
		win32api.Beep(hz, sec)

	def split_all_list_1d_to_list_2d_by_input_text(self, input_list, input_text):
		"""
		리스트로 들어온 자료들을 한번에 분리해서 2차원리스트로 만드는 것

		:param input_list:
		:param input_text:
		:return:
		"""

		result = []
		for one_value in input_list:
			temp_result = str(one_value).split(input_text)
			result.append(temp_result)
		return result

	def split_as_num_list(self, input_list_1d, num_list_1d):
		"""
		넘어온 자료를 원하는 숫자만큼씩 자르는것
		입력값 : "ㅁㄴㅇㄹㄴㅇㄹㄴㅇㄹㄴㅇㄹㄴㄹ"
		분리기준 = [2,4,5]
		결과값 :["ㅁㄴ", "ㅇㄹㄴㅇ", "ㄹㄴㅇㄹㄴ", "ㅇㄹㄴㄹ"]

		:param input_list_1d:
		:param num_list_1d:
		:return:
		"""
		result = []

		for one_text in input_list_1d:
			temp = []
			text_len = len(one_text)
			remain_text = one_text
			for x in num_list_1d:
				if x <= len(remain_text):
					temp.append(remain_text[0:x])
					remain_text = remain_text[x:]
				elif len(remain_text):
					temp.append(remain_text)
					break
			result.append(temp)
		return result

	def split_data_by_new_line_char(self, input_text, num):
		"""
		문자열을 새로운줄, tab으로 구분해서 분리한다

		:param input_text:
		:param num:
		:return:
		"""
		result = []
		temp_list = str(input_text).split("\n")
		for one_value_1 in temp_list:
			temp = []
			tab_list = str(one_value_1).split("\t")
			for one_value_2 in tab_list:
				temp.append(one_value_2)
			result.append(temp)

		return result

	def split_directory(self, input_file=""):
		"""
		입력으로 들어온 화일의 총 이름에서 디렉토리 부분만 추출하는 것
		:param input_file:
		:return:
		"""
		drive, path_and_file = os.path.splitdrive(input_file)
		path, file = os.path.split(input_file)
		result = [path, file]
		return result

	def split_double_moum(self, double_moum):
		"""
		이중모음을 분리시키는것

		:param double_moum:
		:return:
		"""
		result = self.split_double_moum(double_moum)
		return result

	def split_double_moum_to_two_simple_moum(self, double_moum):
		"""
		이중모음을 단모음으로 바꿔주는것

		:param double_moum:
		:return:
		"""
		mo2_dic = {"ㅘ": ["ㅗ", "ㅏ"], "ㅙ": ["ㅗ", "ㅐ"], "ㅚ": ["ㅗ", "ㅣ"], "ㅝ": ["ㅜ", "ㅓ"], "ㅞ": ["ㅜ", "ㅔ"], "ㅟ": ["ㅜ", "ㅣ"],
				   "ㅢ": ["ㅡ", "ㅣ"], }
		result = mo2_dic[double_moum]
		return result

	def split_file_path_by_path_and_name(self, input_value=""):
		"""
		입력값을 경로와 이름으로 분리

		:param input_value:
		:return:
		"""
		filename = ""
		path = ""
		input_value = input_value.replace("/", "\\")
		temp_1 = input_value.split("\\")
		if "." in temp_1[-1]:
			filename = temp_1[-1]
		if len(temp_1) > 1 and "\\" in temp_1[:len(temp_1[-1])]:
			path = input_value[:len(temp_1[-1])]
		result = [filename, path]
		return result

	def split_filename_by_path_n_filename(self, filename=""):
		"""
		화일 이름을 경로와 이름으로 구분하는 것이다
		메뉴에서 제외

		:param filename:
		:return:
		"""
		path = ""
		changed_filename = filename.replace("\\", "/")
		split_list = changed_filename.split("/")
		filename_only = split_list[-1]
		if len(changed_filename) == len(filename_only):
			path = ""
		else:
			path = changed_filename[:len(filename_only)]

		return [path, filename_only]

	def split_korean_to_cho_sung_list(self, input_text):
		""" 한글자의 한글을 자음과 모음으로 구분해 주는것"""

		first_letter = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
		# 19 글자
		second_letter = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]  # 21 글자
		third_letter = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]  # 28 글자, 없는것 포함

		result = []
		input_text = str(input_text)
		for one_text in input_text:
			if self.xre.is_match("[한글:1~1]", one_text):
				one_byte_data = one_text.encode("utf-8")

				new_no_1 = (int(one_byte_data[0]) - 234) * 64 * 64
				new_no_2 = (int(one_byte_data[1]) - 128) * 64
				new_no_3 = (int(one_byte_data[2]) - 128)

				value = new_no_1 + new_no_2 + new_no_3 - 3072

				chosung = first_letter[divmod(value, 588)[0]]  # 초성
				#joongsung = second_letter[divmod(divmod(value, 588)[1], 28)[0]]  # 중성
				#jongsung = third_letter[divmod(divmod(value, 588)[1], 28)[1]]  # 종성
				result.append(chosung)
			else:
				result.append(None)
		return result
	def split_korean_to_jamo_list(self, input_text):
		""" 한글자의 한글을 자음과 모음으로 구분해 주는것"""

		first_letter = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
		# 19 글자
		second_letter = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]  # 21 글자
		third_letter = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]  # 28 글자, 없는것 포함

		result = []
		input_text = str(input_text)
		for one_text in input_text:
			if self.xre.is_match("[한글:1~1]", one_text):
				one_byte_data = one_text.encode("utf-8")

				new_no_1 = (int(one_byte_data[0]) - 234) * 64 * 64
				new_no_2 = (int(one_byte_data[1]) - 128) * 64
				new_no_3 = (int(one_byte_data[2]) - 128)

				value = new_no_1 + new_no_2 + new_no_3 - 3072

				temp_num_1 = divmod(value, 588)  # 초성이 몇번째 자리인지를 알아내는것
				temp_num_2 = divmod(divmod(value, 588)[1], 28)  # 중성과 종성의 자릿수를 알아내는것것

				chosung = first_letter[divmod(value, 588)[0]]  # 초성
				joongsung = second_letter[divmod(divmod(value, 588)[1], 28)[0]]  # 중성
				jongsung = third_letter[divmod(divmod(value, 588)[1], 28)[1]]  # 종성
				temp = [chosung, joongsung, jongsung]
				result.append(temp)
			else:
				result.append(None)
		return result



	def split_list_1d_for_list_2d_by_max_count(self, all_data, initial_group, step):
		"""
		기존에 그룹화되어있는것을 기준으로, 최대갯수가 step의 갯수만큼 되도록 다시 그룹화 하는것이다

		:param all_data:
		:param initial_group:
		:param step:
		:return:
		"""
		result = []
		for list_1d in initial_group:
			if len(list_1d) > step:
				repeat_no = int((len(list_1d) + step - 1) / step)
				for no in range(repeat_no - 1):
					result.append(list_1d[no * step:(no + 1) * step])
				result.append(list_1d[(repeat_no - 1) * step:])
			else:
				result.append(list_1d)
		remain_all_data = all_data
		for list_1d in initial_group:
			for one_value in list_1d:
				remain_all_data.remove(one_value)
		result.append(remain_all_data)
		return result

	def split_list_2d_as_none_data(self, input_list_2d, int_flag_value_at_2d):
		"""
		2번째 자료가 같은것만 묶는다
		예 : [[1,2,3,"",5], [1,2,13,4,16], [0,0,0,4,7], [1,3,5,"",9], [1,3,5,"",10]]
		4번째것을 기준으로 한다면
		결과 : [[1,2,3,"",5], [1,3,5,"",9], [1,3,5,"",10]]
		위와같은 형태로 만들어 주는 것이다

		:param input_list_2d:
		:param int_flag_value_at_2d:
		:return:
		"""

		result = []
		for list_1d in input_list_2d:
			# print(list_1d)
			if list_1d[int_flag_value_at_2d - 1] == "" or list_1d[int_flag_value_at_2d - 1] == None:
				result.append(list_1d)
		return result

	def split_list_2d_by_multi_words(self, all_list_2d, split_words=["o", "3", "bc", "1", "4577"]):
		"""
		1) 분리단어들을 큰것부터 정렬해야, 작은것도 가능하기 때문에 정리하는부분이다
		2) 먼저 분리할 단어들을 빠꾸기를 이용하여, 특수한 분자로 바꾸고, 맨마지막에 분리를 하는 방식을 사용한것이다

		:param all_list_2d:
		:param split_words:
		:return:
		"""
		split_words.sort()  # 1
		split_words.reverse()
		result = []
		for list_1d in all_list_2d:
			temp_2 = []
			for one_value in list_1d:
				one_value = str(one_value)
				for one_split_word in split_words:  # 2
					one_value = one_value.replace(one_split_word, "_#_#%0_")
				temp_2.append(one_value.split("_#_#%0_"))
			result.append(temp_2)
		return result

	def split_list_as_same_data(self, input_list, empty=11, same_column=[1, 3, 5]):
		"""
		읽어온 자료에서 끝나지 않은 자료만 걸러낸후, 같은 내용의 자료를 묶는것
		다음에 다른곳에도 사용이 가능할것 같아 함수로 만듦

		:param input_list:
		:param empty:
		:param same_column:
		:return:
		"""

		result = {}
		for one_list in input_list:
			# 넘어온 자료중 11번째 자료가 비어있다면 끝나지 않은것으로 판다.
			if one_list[empty - 1] == None or one_list[empty - 1] == "":
				# 같은것의 기준인 same_column안의 리스트 자료를 다 합쳐서 같은것은 같은 항목으로 견적요청한것으로 판단한다
				basic_data = ""
				for no in same_column:
					basic_data = basic_data + str(one_list[no - 1])

				# 기존에 같은 이름의 자료가 있으면, 하나더 추가한다(2차원리스트)
				if result:
					if basic_data in result.keys():
						value = result[basic_data]
						value.append(one_list)
						result[basic_data] = value
					else:
						result[basic_data] = [one_list]
				else:
					result[basic_data] = [one_list]

		# 3차원리스트 형태로 결과값을 돌려준다
		return result.values()

	def split_method_and_delete_empty_line(self, filename):
		"""
		화일의 메소드를 기준으로 나누면서 동시에 빈라인은 삭제하는것
		"""
		def_list = []
		result = []
		total_code = ""
		total = ""
		# 화일을 읽어온다
		f = open(filename, 'r', encoding='UTF8')
		original_lines = f.readlines()
		f.close()
		print(len(original_lines))
		num = 1
		temp = ""
		exp_start = ""
		exp_end = ""
		exp_mid = ""
		for one_line in original_lines:
			total = total + one_line
			changed_one_line = one_line.strip()
			if changed_one_line == "":
				one_line = ""
			elif changed_one_line[0] == "#":
				one_line = ""
			elif changed_one_line[0:3] == "def":
				def_list.append(temp)
				temp = one_line
			elif '"""' in changed_one_line:
				if changed_one_line[0:3] == '"""':
					exp_end = "no"
					exp_start = "yes"
					one_line = ""
				elif changed_one_line[:-3] == '"""':
					if exp_mid == "yes":
						exp_mid = "no"
					else:
						exp_end = "yes"
						exp_start = "no"
						one_line = ""
				else:
					if exp_mid == "yes":
						exp_mid = "no"
					else:
						exp_mid = "yes"

				num = num + 1

			if exp_start == "yes" and exp_end == "no":
				one_line = ""

			temp = temp + one_line
			total_code = total_code + one_line
		print(num)

		return [def_list, total_code, total]

	def split_num_n_char_for_mixed_text(self, raw_data):
		"""
		문자와숫자를 분리해서 리스트로 돌려주는 것이다
		123wer -> ['123','wer']
		"""
		temp = ""
		int_temp = ""
		result = []
		datas = str(raw_data)
		for num in range(len(datas)):
			if num == 0:
				temp = str(datas[num])
			else:
				try:
					fore_var = int(datas[num])
					fore_var_status = "integer"
				except:
					fore_var = datas[num]
					fore_var_status = "string"
				try:
					back_var = int(datas[num - 1])
					back_var_status = "integer"
				except:
					back_var = datas[num - 1]
					back_var_status = "string"

				if fore_var_status == back_var_status:
					temp = temp + datas[num]
				else:
					result.append(temp)
					temp = datas[num]
		if len(temp) > 0:
			result.append(temp)
		return result

	def split_operator(self, input_value):
		"""


		:param input_value:
		:return:
		"""
		result = []
		input_value = str(input_value)
		oper = ""
		short_value = ""
		for index in range(len(input_value)):
			if input_value[index] in ["<", ">", "="]:
				if oper == "":
					oper = oper + input_value[index]
					result.append(short_value)
					short_value = ""
				else:
					oper = oper + input_value[index]
			else:
				if oper != "":
					result.append(oper)
					short_value = short_value + input_value[index]
					oper = ""
				else:
					short_value = short_value + input_value[index]
		if short_value:
			result.append(short_value)
		return result

	def split_path_by_n_name(self, input_value=""):
		"""
		입력값을 경로와 이름으로 분리
		"""
		filename = ""
		path = ""
		input_value = input_value.replace("/", "\\")
		temp_1 = input_value.split("\\")
		if "." in temp_1[-1]:
			filename = temp_1[-1]
		if len(temp_1) > 1 and "\\" in temp_1[:len(temp_1[-1])]:
			path = input_value[:len(temp_1[-1])]
		result = [filename, path]
		return result

	def split_py_file_to_list_1d_by_def(self, filename, input_code_dic={}):
		"""
		python으로만든 화일을 읽어서 def를 기준으로 분리하는것
		결과 : {"메소드이름":["1번째 코드", "2번째 코드"]}
		"""

		for a_coding in ["utf-8", "ansi", "UTE-8-sig", "utf-16"]:
			try:
				f = open(filename, 'r', encoding=a_coding)
				file_list = f.readlines()
				f.close()
			except:
				pass

		result = input_code_dic
		start = 0
		code_text = ""
		for one_line_text in file_list:
			# def로 시작이 되는지 알아 내는것
			strip_text = str(one_line_text).strip()

			if strip_text[0:3] == "def" and strip_text[-1] == ":":
				method_name = strip_text.split("(")[0]
				if start == 0:
					code_text = one_line_text
					start = 1
				else:
					if method_name in result.keys():
						if code_text in result[method_name]:
							# print("found ", method_name)
							pass
						else:
							result[method_name] = [code_text]
					else:
						result[method_name] = [code_text]
					code_text = one_line_text
			else:
				code_text = code_text + one_line_text

		return result

	def split_selection_text_to_list_1d_by_each_paragraph(self, input_text):
		"""
		워드의 선택영역을 줄바꿈을 기준으로 1차원리스트로 만들어 주는것

		:param input_text:
		:return:
		"""
		result = input_text.split(chr(13))
		return result

	def split_text_by_chars(self, input_text, input_chars=","):
		"""
		어떤 글자를 원하는 문자로 나눠서 1차원자료로 만들어 주는것

		:param input_text:
		:param input_chars:
		:return:
		"""
		result = input_text.split(input_chars)
		return result

	def split_text_by_new_line_tab(self, input_text, num):
		"""
		문자열을 새로운줄, tab으로 구분해서 분리한다

		:param input_text:
		:param num:
		:return:
		"""
		result = []
		temp_list = str(input_text).split("\n")
		for one_value_1 in temp_list:
			temp = []
			tab_list = str(one_value_1).split("\t")
			for one_value_2 in tab_list:
				temp.append(one_value_2)
			result.append(temp)

		return result

	def split_text_by_step(self, input_text, num):
		"""
		문자열을 몇개씩 숫자만큼 분리하기
		'123456' => '12','34','56'

		:param input_text:
		:param num:
		:return:
		"""
		input_text = str(input_text)
		result = []
		for i in range(0, len(input_text), num):
			result.append(input_text[i:i + num])
		return result

	def split_text_for_csv_file(self, input_text):
		"""
		csv 형식의 자료를 읽어오는 것
		""로 들러쌓인것은 숫자나 문자이며, 아닌것은 전부 문자이다

		:param input_text:
		:return:
		"""
		result = []
		temp = ""
		num = 0
		my_type = ""
		for no in range(len(input_text)):
			one_char = input_text[no]
			if one_char == '"' and num == 0:
				my_type = "type_2"
			if one_char == '"': num = num + 1
			if one_char == ',':
				if divmod(num, 2)[1] == 0 and my_type == "type_2":
					temp = temp.replace(",", "")
					try:
						temp = int(temp[1:-1])
					except:
						temp = float(temp[1:-1])
					result.append(temp)
					temp = ""
					num = 0
					my_type = ""
				elif my_type == "":
					result.append(temp)
					temp = ""
					num = 0
				else:
					temp = temp + one_char
			else:
				temp = temp + one_char
		return result

	def split_text_to_list_1d_as_len_set(self, input_list_1d, num_list_1d):
		"""
		넘어온 자료를 원하는 숫자만큼씩 자르는것
		입력값 : "ㅁㄴㅇㄹㄴㅇㄹㄴㅇㄹㄴㅇㄹㄴㄹ"
		분리기준 = [2,4,5]
		결과값 :["ㅁㄴ", "ㅇㄹㄴㅇ", "ㄹㄴㅇㄹㄴ", "ㅇㄹㄴㄹ"]

		:param input_list_1d:
		:param num_list_1d:
		:return:
		"""
		result = []

		for one_text in input_list_1d:
			temp = []
			text_len = len(one_text)
			remain_text = one_text
			for x in num_list_1d:
				if x <= len(remain_text):
					temp.append(remain_text[0:x])
					remain_text = remain_text[x:]
				elif len(remain_text):
					temp.append(remain_text)
					break
			result.append(temp)
		return result

	def split_text_to_list_1d_by_base_word(self, input_list_1d, base_words):
		"""
		문장으로 된것을 의미있는 단어들로 분리하는 것

		:param input_list_1d:
		:param base_words:
		:return:
		"""
		aaa = collections.Counter()
		for one in input_list_1d:
			value = str(one).lower().strip()
			if len(value) == 1 or value == None or value == " ":
				pass
			else:
				for l1 in base_words:
					value = value.replace(l1[0], l1[1])
				value = value.replace(",", " ")
				value = value.replace("(", " ")
				value = value.replace(")", " ")
				value = value.replace("  ", " ")
				value = value.replace("  ", " ")
				values = value.split(" ")
				aaa.update(values)
		return aaa

	def split_unique(self, raw_data, delete_or_blank=0):
		"""
		이것은 똑같은 자료가 있으면 그자료를 맨처음의 것만을 남기고 없애는 것이다
		이것을 클래스로 만들어 본다

		:param raw_data:
		:param delete_or_blank:
		:return:
		"""

		before = list(raw_data)
		blank = []
		for dd in range(len(before[0])):
			blank = blank.append('')

		for a in range(len(before) - 1):
			gijun_data = before[a]

			for b in range(a + 1, len(before)):
				cmp_data = before[b]

				result = self.cmp(gijun_data, cmp_data)
				if result == 0:
					before[b] = blank
		return before

	def split_value_as_num_char(self, raw_data):
		"""
		문자와숫자를 분리해서 리스트로 돌려주는 것이다 123
		wer -> ['123', 'wer']
		"""
		temp = ""
		int_temp = ""
		result = []
		datas = str(raw_data)
		for num in range(len(datas)):
			if num == 0:
				temp = str(datas[num])
			else:
				try:
					fore_var = int(datas[num])
					fore_var_status = "integer"
				except:
					fore_var = datas[num]
					fore_var_status = "string"
				try:
					back_var = int(datas[num - 1])
					back_var_status = "integer"
				except:
					back_var = datas[num - 1]
					back_var_status = "string"

				if fore_var_status == back_var_status:
					temp = temp + datas[num]
				else:
					result.append(temp)
					temp = datas[num]
		if len(temp) > 0:
			result.append(temp)
		return result

	def splitter(self, n, s):
		"""
		문자열을 몇개씩 숫자만큼 분리하기
		['123456'] => ['12','34','56']

		:param n:
		:param s:
		:return:
		"""
		result = []
		for i in range(0, len(s), n):
			result.append("".join(s[i:i + n]))
		return result

	def string_to_binary_list(self, st):
		"""

		:param st:
		:return:
		"""
		result = [bin(ord(i))[2:].zfill(8) for i in st]
		return result

	def sum_list(self, input_list):
		"""
		넘어온 여러줄의 리스트자료를 기준으로
		각 y행마다 자료가 있는지 확인해서,
		최대한 자료가 많이 들어가도록 각 x 라인을 채워서 한줄을 만든다

		:param input_list:
		:return:
		"""
		result = []
		x_no = len(input_list)
		y_no = len(input_list[0])
		for y in range(y_no):
			temp = ""
			for x in range(x_no):
				one_value = input_list[x][y]
				if one_value != "" and one_value != None:
					temp = one_value
			result.append(temp)
		# print(result)
		return result

	def sum_two_list_2d_with_each_same_position(self, list_2d_1, list_2d_2):
		"""
		같은 사이즈의 2차원 자료를 같은 위치의 값을 더하는것
		이것은 여러 엑셀화일의 같은 형태의 자료들을 더하기 위해서 사용하는 목적이다

		:param list_2d_1:
		:param list_2d_2:
		:return:
		"""
		for x in range(len(list_2d_1)):
			for y in range(len(list_2d_1[0])):
				try:
					list_2d_1[x][y] = list_2d_1[x][y] + list_2d_2[x][y]
				except:
					list_2d_1[x][y] = str(list_2d_1[x][y]) + str(list_2d_2[x][y])
		return list_2d_1

	def swap(self, a, b):
		"""
		a,b를 바꾸는 함수이다

		:param a:
		:param b:
		:return:
		"""
		t = a
		a = b
		b = t
		return [a, b]

	def switch_2_value_of_list_1d_for_list_2d(self, input_list_2d, input_no_list):
		"""
		2차원 리스트의 자료에서 각 라인별 2개의 위치를 바꾼는것
		change_position_for_list_2d_by_2_index([[1,2,3], [4,5,6]], [0,2])
		[[1,2,3], [4,5,6]] ==> [[3,2,1], [6,5,4]]
		메뉴에서 제외

		:param input_list_2d: list type 2dimension, 2차원의 리스트형
		:param input_no_list:
		:return:
		"""
		for before, after in input_no_list:
			for no in range(len(input_list_2d)):
				value1 = input_list_2d[no][before]
				value2 = input_list_2d[no][after]
				input_list_2d[no][before] = value2
				input_list_2d[no][after] = value1
		return input_list_2d

	def switch_every_two_data_for_list_1d(self, input_data):
		"""
		input_data : [a, b, c, d]
		result : [b, a, d, c]
		두개의 자료들에 대해서만 자리를 바꾸는 것이다

		:param input_data:
		:return:
		"""
		result = []
		for one_data in range(int(len(input_data) / 2)):
			result.append(input_data[one_data * 2 + 1])
			result.append(input_data[one_data * 2])
		return result

	def switch_list_2d_based_on_index(self, input_list_2d, input_no_list):
		"""
		2차원의 각 1차원자료들의 index번호를 기준으로 앞뒤를 바꾸는 것
		[[1,2,3,4,5], [5,6,7,8,9]] ==> [[3,4,5, 1,2], [7,8,9, 5,6]]
		input_no_list.sort()
		input_no_list.reverse()

		:param input_list_2d: 2차원 형태의 리스트
		:param input_no_list:
		:return:
		"""
		for before, after in input_no_list:
			for no in range(len(input_list_2d)):
				value1 = input_list_2d[no][before]
				value2 = input_list_2d[no][after]
				input_list_2d[no][before] = value2
				input_list_2d[no][after] = value1
		return input_list_2d

	def switch_one_value_by_special_char(self, input_value, input_char="="):
		"""
		입력된 값에 특정한 문자가 있으면, 그것을 기준으로 앞뒤를 바꾸는 것
		"aaa=bbb" => "bbb=aaa"

		:param input_char:
		"""
		one_list = str(input_value).split(input_char)
		if len(one_list) == 2:
			result = one_list[1] + input_char + one_list[0]
		else:
			result = input_value
		return result

	def switch_two_data(self, a, b):
		"""
		a,b를 바꾸는 함수이다

		:param a:
		:param b:
		:return:
		"""
		t = a
		a = b
		b = t
		return [a, b]

	def switch_value_by_2_position_no_in_list_2d(self, input_list_2d, input_no_list):
		"""
		2차원 리스트의 자료에서 각 라인별 2개의 위치를 바꾼는것
		change_position_for_list_2d_by_2_index([[1,2,3], [4,5,6]], [0,2])
		[[1,2,3], [4,5,6]] ==> [[3,2,1], [6,5,4]]

		:param input_list_2d: 2차원의 리스트형 자료
		:param input_no_list:
		"""
		for before, after in input_no_list:
			for no in range(len(input_list_2d)):
				value1 = input_list_2d[no][before]
				value2 = input_list_2d[no][after]
				input_list_2d[no][before] = value2
				input_list_2d[no][after] = value1
		return input_list_2d

	def terms(self):
		"""
		용어정리 : 아래와같은 형태로 용어를 사용한다
		:return:
		"""

		result = """
			pxy : 커서의 픽셀 좌표
			pwh: 넓이, 높이의 길이를 픽셀단위로 나타낸것
			mouse_click = mouse_down + mouse_up film
			date	 : 2000-01-01
			datelist : [2000, 01, 01]
			ymdlist : [2000, 01, 01]
			time	 : 시간의 여러형태로 입력을 하면, 이에 맞도록 알아서 조정한다
			dhms	 : 2일3시간10분30초, day-hour-minute-sec
			hmslist  : [시, 분, 초]
			utc  : 1640995200.0 또는 "", 1648037614.4801838 (의미 : 2022-03-23T21:13:34.480183+09:00)
			move	 : 입력값에 더하거나 빼서 다른 값으로 바꾸는것, 입력값과 출력값이 다를때 (출력값을 입력의 형태로 바꾸면 값이 다른것)
			change   : 형태를 바꾼것
			read	 : 입력값을 원하는 형태로 변경해서 갖고오는것
			get	  : 입력값에서 원하는 형태의 값을 갖고오는것
			shift	: 현재의 값을 같은 형태에서 값을 이동시키는것
			index : 0부터 시작되는 번호들
			no : 1부터 시작되는 번호들
		"""
		return result

	def trans_list(self, input_list_2d="입력필요"):
		"""
		trans_list( input_list_2d="입력필요")
		2차원자료를 행과열을 바꿔서 만드는것
		단, 길이가 같아야 한다
		입력형태 :
		출력형태 :
		"""
		checked_input_list_2d = self.make_list_2d_same_len(input_list_2d)
		result = [list(x) for x in zip(*checked_input_list_2d)]
		return result

	def trans_list_2d(self, input_list_2d):
		result = self.change_list_2d_as_xy_to_yx(input_list_2d)
		return result

	def trans_list_2d_from_xy_to_yx(self, input_list):
		"""
		리스트값의 x,y를 바꾸는것
		"""
		result = zip(*input_list)
		return result

	def tri_1(self, xyxy, per=100, reverse=1, size=100):
		"""
		삼각형을 만드는것
		"""
		x1, y1, x2, y2 = xyxy
		width = x2 - x1
		height = y2 - y1
		lt = [x1, y1]  # left top
		lb = [x2, y1]  # left bottom
		rt = [x1, y1]  # right top
		rb = [x2, y2]  # right bottom
		tm = [x1, int(y1 + width / 2)]  # 윗쪽의 중간
		lm = [int(x1 + height / 2), y1]  # 윗쪽의 중간
		rm = [int(x1 + height / 2), y1]  # 윗쪽의 중간
		bm = [x2, int(y1 + width / 2)]  # 윗쪽의 중간
		center = [int(x1 + width / 2), int(y1 + height / 2)]

		# 정삼각형
		# 정삼각형에서 오른쪽이나 왼쪽으로 얼마나 더 간것인지
		# 100이나 -100이면 직삼각형이다

		# 사각형은 왼쪽위에서 오른쪽 아래로 만들어 진다

		result = [lb, rb, tm]
		return result

	def update_set_by_list_2d(self, input_set, input_list_2d):
		"""
		input_list = [["변경전자료1", "변경후자료2"], ["변경전자료11", "변경후자료22"], ]

		:param input_set:
		:param input_list_2d:
		:return:
		"""
		for list_1d in input_list_2d:
			input_set.discard(list_1d[0])
			input_set.add(list_1d[1])
		return input_set

	def window_font_list(self):
		"""
		윈도우에서 설치된 font리스트를 갖고온다

		:return:
		"""
		font_names = []
		hdc = win32gui.GetDC(None)
		win32gui.EnumFontFamilies(hdc, None, self.callback, font_names)
		# print("\n".join(font_names))
		win32gui.ReleaseDC(hdc, None)
		return font_names

	def write_dic_db_1d(self, i_dic, i_key, i_value):
		"""
		아래와같은 1차원의 형태로 가능한 database를 만들어 보자
		이것은 엑셀과같은 고유한 셀이나 다른곳의 값을 넣고 뺄때 편할것 같다

		:param i_dic:
		:param i_key:
		:param i_value:
		:return:
		"""
		i_key = tuple(i_key)
		i_dic[i_key] = i_value

	def write_key_value_at_nth_dimension(self, d, key, value, target_depth, current_depth=1):
		# 다차원 사전에서 모든 n번째 차원에 키와 값을 설정하는 함수.
		if current_depth == target_depth:
			for k in d.keys():
				if isinstance(d[k], dict):
					d[k][key] = value
		else:
			for k, sub_dict in d.items():
				if isinstance(sub_dict, dict):
					self.write_key_value_at_nth_dimension(sub_dict, key, value, target_depth, current_depth + 1)

	def write_value_at_nth_dimension(self, d, keys, value):
		"""
		['a', 'b', 'd'], 'new_value' 이런 형태의 값을 넣는것

		:param d:
		:param keys:
		:param value:
		:return:
		"""
		current_dict = d
		for key in keys[:-1]:
			if key not in current_dict:
				current_dict[key] = {}
			current_dict = current_dict[key]
		current_dict[keys[-1]] = value

	def xyprint(self, input_value, limit_no=20):
		"""
		print할때 너무 많은 글자가 나오면 않되기 때문에 글자수를 줄여주면서 끝에 ~~을 넣어서 프린트해주는 기능이다

		:param input_value:
		:param limit_no:
		:return:
		"""
		if type(input_value) == type([]):
			result = []
			for one in input_value:
				if len(str(one)) > limit_no:
					result.append(str(one))[:limit_no] + str("~~")
		elif type(input_value) == type({}):
			result = {}
			for one in input_value.keys():
				if len(str(input_value[one])) > limit_no:
					result[one] = str(input_value[one])[:limit_no] + str("~~")
		elif type(input_value) == type("abc"):
			if len(input_value) > limit_no:
				result = input_value[:limit_no] + str("~~")
		else:
			result = input_value
		return result

