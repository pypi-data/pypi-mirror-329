# -*- coding: utf-8 -*-
import winreg
import win32com.client
import win32com.client.gencache
import win32process, win32api, win32gui

import time, os, math, basic_data
import pyperclip
import chardet
import pygetwindow as gw
import paho.mqtt.client as mqtt
import pywinauto

from unittest.mock import patch
with patch("ctypes.windll.user32.SetProcessDPIAware", autospec=True):
    import pyautogui

class pyclick:
	"""
	여러가지 사무용에 사용할 만한 메소드들을 만들어 놓은것이며,
	좀더 특이한 것은 youtil2로 만들어서 사용할 예정입니다

	2024-09-11 : 전체적으로 유사한것들을 변경함
	"""

	def __init__(self):
		self.vars = basic_data.basic_data().vars

	def all_infomation_for_handle_no(self, handle_no):
		"""
		핸들 번호로 열려있는 프로그램일 경우, 일반 정보들을 돌려주는것

		:param handle_no:
		:return:
		"""
		result = {}
		if handle_no is not None:
			hwnd_title = win32gui.GetWindowText(handle_no)
			# 윈도우 클래스명 (개발 시점에 적용된 고유값이라고 보면 됨)
			hwnd_class_name = win32gui.GetClassName(handle_no)

			# 사용자가 볼 수 있는지 있는지 여부 (보이면 1, 안보이면 0)
			# (최소화된 상태라도) 사용자가 볼 수 있는 창이면 이 값은 1 임
			hwnd_is_visible = win32gui.IsWindowVisible(handle_no)

			# 좌표 정보
			result["pxywh"] = win32gui.GetWindowRect(handle_no)
			result["px"] = result["pxyxy"][0] # 만약 hwnd_rect_x 값이 -32000 이면 최소화된 상태라고 보면 됨
			result["py"] = result["pxyxy"][1] # 만약 hwnd_rect_y 값이 -32000 이면 최소화된 상태라고 보면 됨
			result["w"] = result["pxyxy"][2]
			result["title"] = hwnd_title
			result["class_name"] = hwnd_class_name
			result["is_visible"] = str(hwnd_is_visible)
			result["h"] = result["pxyxy"][3]
			result["h"] = result["pxyxy"][3]
			result["h"] = result["pxyxy"][3]

			print(result)
		return result

	def cal_pixel_size_for_input_text_2(self, input_text, target_pixel, font_name="malgun.ttf", font_size=12, fill_char=" "):
		"""
		원하는 길이만큼 텍스트를 근처의 픽셀값으로 만드는것
		원래자료에 붙이는 문자의 픽셀값
		"""
		fill_px = self.cal_pixel_size_for_input_text_2(fill_char, font_size, font_name)[0]
		total_length =0
		for one_text in input_text:
			#한글자씩 필셀값을 계산해서 다 더한다
			one_length = self.cal_pixel_size_for_input_text_2(fill_char, font_size, font_name)[0]
			total_length = total_length + one_length

		# 원하는 길이만큼 부족한 것을 몇번 넣을지 게산하는것
		times = round((target_pixel - total_length)/fill_px)
		result = input_text + " "*times

		#최종적으로 넣은 텍스트의 길이를 한번더 구하는것
		length = self.cal_pixel_size_for_input_text_2(result, font_size, font_name)[0]

		#[최종변경문자, 총 길이, 몇번을 넣은건지]
		return [result, length, times]

	def check_input_action_key(self, input_value):
		"""
		키보드의 액션을 하기위해 사용해야할 용어를 확인하는 부분이다
		:param input_value:
		:return:
		"""
		input_value = str(input_value).lower()
		if input_value in self.vars["keyboard_action_list_all"]:
			result = input_value
		else:
			result = ""
		return result

	def click_mouse_with_type_times_interval(self, click_type="click", input_clicks=1, input_interval=0.25):
		"""

		:param click_type:
		:param input_clicks:
		:param input_interval:
		:return:
		"""
		pyautogui.click(button=click_type, clicks=input_clicks, interval=input_interval)

	def click_mouse_left_with_n_times(self, click_times = 1):
		"""
		왼쪽 마우스 버튼을 누르는 것

		:param click_times: 누르는 횟수
		:return:
		"""
		pyautogui.click(button="left", clicks= click_times)

	def click_mouse_left_down(self):
		"""
		왼쪽 마우스 버튼 눌른상태로 멈춤
		드리그등을 위한것
		"""
		pyautogui.mouseDown(button='left')

	def click_mouse_left_up(self):
		"""
		왼쪽 마우스 버튼 눌럿다 올린것
		"""
		pyautogui.mouseUp(button='left')

	def click_mouse_right_with_n_times(self, click_times = 1):
		"""
		오른쪽 마우스 클릭
		:param click_times:
		"""
		pyautogui.click(button="right", clicks=click_times)

	def click_mouse_right_down(self):
		"""
		오른쪽 마우스 눌름
		"""
		pyautogui.mouseDown(button='right')

	def click_mouse_right_up(self):
		"""
		오른쪽 마우스 올림
		:return:
		"""
		pyautogui.mouseUp(button='right')

	def copy(self):
		"""
		현재 선택된 것을 복사하기
		"""
		pyautogui.hotkey('ctrl', "c")

	def data_for_keyboard_action_list_short(self):
		"""
		키보드 액션의 종류들
		:return:
		"""
		result = self.vars["keyboard_action_list_short"]
		return result

	def data_for_keyboard_action_list(self):
		"""
		키보드 액션의 종류들
		:return:
		"""
		result = self.vars["keyboard_action_list_all"]
		return result

	def dclick_mouse(self):
		"""
		double click
		:return:
		"""
		pyautogui.click(button="left", clicks=2, interval=0.25)

	def dclick_mouse_left_with_interval(self, interval_time=0.25):
		"""
		왼쪽 마우스 더블 클릭
		:param interval_time: 클릭 시간 간격
		:return:
		"""
		pyautogui.click(button="left", clicks=2, interval=interval_time)

	def dclick_mouse_right_with_interval(self, interval_time=0.25):
		"""
		오른쪽 마우스 더블 클릭
		:param interval_time:클릭 시간 간격
		:return:
		"""
		pyautogui.click(button="right", clicks=2, interval=interval_time)

	def drag_mouse_from_pxy1_to_pxy2(self, pxy1, pxy2, drag_speed=0.5):
		"""
		마우스 드레그

		:param pxy1:
		:param pxy2:
		:param drag_speed:
		:return:
		"""
		pyautogui.moveTo(pxy1[0], pxy1[1])
		pyautogui.dragTo(pxy2[0], pxy2[1], drag_speed)

	def drag_mouse_to_pwh(self, phw, drag_speed=0.5):
		"""
		현재 마우스위치에서 상대적인 위치인 pxy로 이동
		상대적인 위치의 의미로 width 와 height 의 개념으로 pwh 를 사용 duration 은 드레그가 너무 빠를때 이동하는 시간을 설정하는 것이다

		:param phw:
		:param drag_speed: 드레그 속도
		"""
		pyautogui.drag(phw[0], phw[1], drag_speed)

	def drag_mouse_to_pxy(self, pxy, drag_speed=0.5):
		"""
		현재 마우스위치에서 절대위치인 머이로 이동	duration 은 드레그가 너무 빠를때 이동하는 시간을 설정하는 것이다

		:param pxy:
		:param drag_speed: 드레그 속도
		"""
		pyautogui.dragTo(pxy[0], pxy[1], drag_speed)

	def file_change_ecoding_type(self, path, filename, original_type="EUC-KR", new_type="UTF-8", new_filename=""):
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
			print(result['encoding'], filename)
			aaa.close()

			if result['encoding'] == original_type:
				print("화일의 인코딩은 ======> {}, 화일이름은 {} 입니다".format(original_type, filename))
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
			self.file_type_change(path, one_file, "EUC-KR", "UTF-8", "_changed")

	def focus_on(self, original_xy, move_xy=[10, 10]):
		"""
		많이 사용하는 마우스와 키보드의 기능을 다시 만들어 놓은 것이다

		:param original_xy:
		:param move_xy:
		:return:
		"""
		pyautogui.moveTo(original_xy[0] + move_xy[0], original_xy[1] + move_xy[1])
		pyautogui.mouseDown(button='left')

	def focus_to_window_by_title(self, window_title="Excel.Application"):
		"""

		:param window_title:
		:return:
		"""
		window = gw.getWindowsWithTitle(window_title)
		print()
		if window.isActive == False:
			try:
				pywinauto.application.Application().connect(handle=window._hWnd).top_window().set_focus()
			except:
				print('No permission')

	def focus_by_handle_no(self, handle_no):
		"""
		특정 윈도우 핸들을 포커스/포커싱 처리하기

		:param handle_no:
		:return:
		"""
		result = False
		if handle_no is not None:
			while True:
				win32gui.ShowWindow(handle_no, 9) # 최소화 되어있을 경우 복원
				win32gui.SetForegroundWindow(handle_no)
				if str(handle_no) == str(win32gui.GetForegroundWindow()):
					break
				else:
					time.sleep(1)
			result = True
		return result

	def get_information_for_monitor(self):
		"""

		:return:
		"""
		result = []
		monitor = win32api.EnumDisplayMonitors()
		result = list()

		for info in monitor:
			# 주 모니터와 서브 모니터 구분
			if info[2][0] == 0 and info[2][1] == 0:
				monitorType = "주모니터"
			else:
				monitorType = "서브모니터"

			result.append({'type': monitorType, '모니터의 영역(왼쪽위, 오른쪽아래)': info[2]})

		result.append({'총모니터갯수': len(monitor)})
		return result

	def get_information_for_mouse(self):
		"""
		[(PyHANDLE:65537, PyHANDLE:0, (0, 0, 1920, 1080)), (PyHANDLE:65539, PyHANDLE:0, (-1920, 1, 0, 1081))]
		1 : 모니터의 핸들값
		2 : unknown
		3 : 위치와 해상도, ( left, top, width, height )
		0, 0 이 주모니터
		left : - 일 경우 주 모니터 왼쪽에 위치, 모니터가 상하로 위치할 경우 top 의 +- 로 판단

		:return:
		"""
		result = []
		pxy = self.get_pxy_for_mouse()
		result.append({"마우스의 현재 위치":pxy})
		monitors = win32api.EnumDisplayMonitors()

		for info in monitors:
			# 주 모니터와 서브 모니터 구분
			if info[2][0] == 0 and info[2][1] == 0:
				monitorType = "주모니터"
			else:
				monitorType = "서브모니터"

			if info[2][0] <= pxy[0] <= info[2][2] and info[2][1] <= pxy[1] <= info[2][3]:
				result.append({"모니터에서의 위치":monitorType})
				break

		return result

	def get_monitor_size(self):
		"""
		모니터의 해상도를 읽어오는 것

		:return:
		"""
		result = pyautogui.size()
		return result

	def get_pos_for_mouse(self):
		# 현재 마우스의 위치를 읽어온다
		result = win32api.GetCursorPos()
		return result

	def get_pxy_for_mouse(self):
		"""
		마우스 위치
		:return:
		"""
		pxy = pyautogui.position()
		return [pxy.x, pxy.y]

	def get_pxy_for_mouse_rev1(self):
		"""
		현재 마우스의 위치를 읽어온다

		:return:
		"""
		result = win32api.GetCursorPos()
		return result

	def get_pxy_for_selected_image(self, input_file_name):
		"""
		화면에서 저장된 이미지랑 같은 위치를 찾아서 돌려주는 것

		:param input_file_name:
		:return:
		"""
		button5location = pyautogui.locateOnScreen(input_file_name)
		center = pyautogui.center(button5location)
		return center

	def get_rgb_for_pxy_in_monitor(self, input_pxy=""):
		"""
		입력으로 들어오는 pxy위치의 rgb값을 갖고온다
		만약 "" 이면, 현재 마우스가 위치한곳의 rgb를 갖고온다
		:param input_pxy:
		:return:
		"""
		if input_pxy:
			x, y = input_pxy
		else:
			x, y = pyautogui.position()
		r, g, b = pyautogui.pixel(x, y)
		return [r,g,b]

	def get_screen_size(self):
		"""
		화면 사이즈

		:return:
		"""
		px =  win32api.GetSystemMetrics(0)
		py =  win32api.GetSystemMetrics(1)
		return [px, py]

	def get_xy_for_mouse(self, ):
		"""
		많이 사용하는 마우스와 키보드의 기능을 다시 만들어 놓은 것이다

		:return:
		"""
		xy = pyautogui.position()
		return (xy.x, xy.y)

	def get_handle_by_patial_title(self, input_text):
		"""
		현재 열려져있는 프로그램들의 제목을 가지고 handle을 구하는 것이며
		전체 이름이 아닌 일부분만 같아도 돌려주도록 한다

		:param input_text:
		:return:
		"""
		result = None
		all_data = self.get_all_title_n_handle_for_opened_windows()
		for title, handle_no in all_data:
			if str(input_text).lower() in str(title).lower():
				return [title, handle_no]
		return result

	def get_title_n_handle_all_for_opened_windows(self):
		"""
		현재 열려져있는 프로그램들의 제목과 윈도우핸들값을 구하는 것

		:return:
		"""
		def callback(hwnd, hwnd_list: list):
			title = win32gui.GetWindowText(hwnd)
			if win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and title:
				hwnd_list.append((title, hwnd))
			return True
		output = []
		win32gui.EnumWindows(callback, output)
		return output

	def get_handle_for_focused_program(self):
		"""
		현재 제일 앞부분에 활성화된 프로그램의 핸들값을 주는 것

		:return:
		"""
		result = win32gui.GetForegroundWindow()
		return result

	def get_process_id_for_focused_program(self):
		"""
		현재 제일 앞부분에 활성화된 프로그램의 process 번호를 돌려주는 것

		:return:
		"""
		process_id = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
		print(process_id)
		return process_id

	def get_running_process_all(self):
		"""
		현재 윈도우 화면에 있는 프로세스 목록 리스트를 반환한다.
		리스트의 각 요소는 element 객체로 프로세스 id, 핸들값, 이름 등의 정보를 보유한다.

		:return:
		"""
		result = []
		procs = pywinauto.findwindows.find_elements()
		for proc in procs:
			result.append([proc, proc.process_id])
		return result

	def get_installed_program_id_all(self):
		"""
		현재 컴퓨터안에 설치된 모든 프로그램의 ID

		:return:
		"""
		result = []
		try:
			# 레지스트리 키 열기
			key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "")
			i = 0
			while True:
				try:
					# 레지스트리 키 열거
					subkey_name = winreg.EnumKey(key, i)
					i += 1
					# ProgID는 일반적으로 '.'을 포함하지 않음
					# #if '.' not in subkey_name:
					result.append(subkey_name)
				except OSError:
					break
		except Exception as e:
			print(f"Error: {e}")
		return result

	def is_com_accessible(self, prog_id):
		"""
		현재 열려있는 프로그램중에서 win32com의 가상 함수가 있는것을 확인하는 것

		:param prog_id:
		:return:
		"""
		try:
			# COM 객체 생성 시도
			app = win32com.client.GetActiveObject(prog_id)
			print("win32com 적용가능 => ", prog_id)
		except:
			return False

	def move_cursor(self, direction, press_times = 1):
		"""
		마우스커서를 기준으로 이동하는것

		:param direction:
		:param press_times:
		:return:
		"""
		for no in range(press_times):
			pyautogui.press(direction)

	def move_mouse_to_pos(self, xy_list):
		"""
		원하는 위치로 마우스를 이동시킨다

		:param xy:
		:return:
		"""
		pos = (xy_list[0], xy_list[1])
		win32api.SetCursorPos(pos)

	def move_mouse_to_pwh_as_delta(self, pwh):
		"""
		마우스의 위치를 이동시킨다

		:param pwh:
		:return:
		"""
		pyautogui.move(pwh[0], pwh[1])

	def move_mouse_to_pxy(self, pxy):
		"""
		마우스의 위치를 이동시킨다

		:param pxy:
		:return:
		"""
		pyautogui.moveTo(pxy[0], pxy[1])

	def move_mouse_xy_as_delta(self, x1, y1):
		"""
		move_mouse_xy
		현재있는 위치에서 x1, y1만큼 이동

		:param x1:
		:param y1:
		:return:
		"""
		pyautogui.move(x1, y1)

	def move_screen_by_scroll(self, input_no):
		"""
		현재 위치에서 상하로 스크롤하는 기능 #위로 올리는것은 +숫자，내리는것은 -숫자로 사용

		:param input_no:
		:return:
		"""
		pyautogui.scroll(input_no)

	def move_xy_by_degree_n_distance(self, degree, distance):
		"""
		move_degree_distance( degree="입력필요", distance="입력필요")
		현재 위치 x,y에서 30도로 20만큼 떨어진 거리의 위치를 돌려주는 것
		메뉴에서 제외

		:param degree:
		:param distance:
		:return:
		"""
		degree = degree * (3.141592 / 180)
		y = distance * math.cos(degree)
		x = distance * math.sin(degree)
		return [x, y]

	def mqtt_connect(self, client, userdata, flags, rc):
		"""
		connect_mqtt

		:param client:
		:param userdata:
		:param flags:
		:param rc:
		:return:
		"""
		if rc == 0:
			print("connected OK")
		else:
			print("Bad connection Returned code=", rc)

	def mqtt_receive_data(self, topic='halmoney/data001'):
		"""
		mqtt의 서버에서 자료받기

		:param topic:
		:return:
		"""
		self.topic = topic
		client = mqtt.Client()
		client.on_connect = self.on_connect
		client.on_disconnect = self.on_disconnect
		client.on_subscribe = self.on_subscribe
		client.on_message = self.on_message

		client.connect(self.broker, self.port, 60)
		client.subscribe(self.topic, 1)
		client.loop_forever()

	def mqtt_send_data(self, input_text="no message", topic='halmoney/data001'):
		"""

		:param input_text:
		:param topic:
		:return:
		"""
		self.topic = topic
		client = mqtt.Client()
		# 새로운 클라이언트 생성

		# 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
		client.on_connect = self.on_connect
		client.on_disconnect = self.on_disconnect
		client.on_publish = self.on_publish
		client.connect(self.broker, self.port)
		client.loop_start()

		client.publish(self.topic, str(input_text), self.qos)
		client.loop_stop()
		client.disconnect()

	def mqtt_start(self, broker="broker.hivemq.com", port=1883, qos=0):
		"""

		:param broker:
		:param port:
		:param qos:
		:return:
		"""
		self.broker = broker
		self.port = port
		self.qos = qos

	def paste(self):
		"""
		복사후 붙여넣기

		:return:
		"""
		pyautogui.hotkey('ctrl', "v")

	def paste_clipboard_data(self):
		"""
		클립보드에 저장된 텍스트를 붙여넣습니다.

		:return:
		"""
		pyperclip.paste()

	def paste_text_from_clipboard(self):
		"""
		클립보드에서 입력된 내용을 복사를 하는 것이다

		:return:
		"""
		result = pyperclip.paste()
		return result

	def popup_for_input(self, button_list):
		"""
		메세지박스의 버튼을 만드는 것

		:param button_list:
		:return:
		"""
		press_button_name = pyautogui.confirm('Enter option', buttons=['A', 'B', 'C'])
		return press_button_name

	def popup_for_input_with_password_style(self, input_text, input_title="", input_default_text =""):
		"""
		메세지박스 : 암호 입력용
		:param input_text:
		:param input_title:
		:param input_default_text:
		:return:
		"""
		a = pyautogui.password(text=input_text, title=input_title, default=input_default_text, mask='*')
		print(a)

	def popup_for_show_message(self):
		"""

		:return:
		"""
		pyautogui.alert(text='내용입니다', title='제목입니다', button='OK')

	def popup_for_show_message_box(self, input_text, input_title="", input_default_text =""):
		"""
		일반 메세지 박스

		:param input_text:
		:param input_title:
		:param input_default_text:
		:return:
		"""
		a = pyautogui.prompt(text=input_text, title=input_title, default=input_default_text)
		print(a)

	def press_key_down(self, one_key):
		"""
		어떤키의 키보드를 눌름

		:param one_key:
		:return:
		"""
		pyautogui.keyDown(one_key)

	def press_key_up(self, one_key):
		"""
		어떤키의 키보드를 눌렀다 땜

		:param one_key:
		:return:
		"""
		pyautogui.keyUp(one_key)

	def press_one_key(self, input_key="enter"):
		"""
		기본적인 키를 누르는 것을 설정하는 것이며
		기본값은 enter이다
		press의 의미는 down + up이다

		:param input_key:
		:return:
		"""
		pyautogui.press(input_key)

	def save(self):
		"""
		저장하기

		:return:
		"""
		pyautogui.hotkey('ctrl', "s")

	def screen_capture(self, file_name="D:Wtemp_101.jpg"):
		"""
		스크린 캡쳐를 해서, 화면을 저장하는 것

		:param file_name:
		:return:
		"""
		pyautogui.screenshot(file_name)
		return file_name

	def screen_capture_with_file_name_n_size(self, file_name, pxyxy):
		"""
		화면캡쳐를 지정한 크기에서 하는것

		:return:
		"""
		region_data = (pxyxy[0], pxyxy[1], pxyxy[2], pxyxy[3])
		im3 = pyautogui.screenshot(file_name, region=region_data)

	def screen_capture_for_full_screen(self, input_full_path=""):
		"""
		스크린샷

		:param input_full_path:
		:return:
		"""
		result = pyautogui.screenshot()
		if input_full_path:
			result.save(input_full_path)
		return result

	def screen_capture_with_pxywh(self, input_pxywh, input_full_path=""):
		"""
		스크린샷

		:param input_pxywh:
		:param input_full_path:
		:return:
		"""
		x,y,w,h  = input_pxywh
		result = pyautogui.screenshot(region=(x,y,w,h))
		if input_full_path:
			result.save(input_full_path)
		return result

	def scroll_screen_by_click_num(self, input_no):
		"""
		현재 위치에서 상하로 스크롤하는 기능 #위로 올리는것은 +숫자，내리는것은 -숫자로 사용

		:param input_no:
		:return:
		"""
		pyautogui.scroll(input_no)

	def scroll_mouse_down(self, input_click_count=10):
		"""
		scroll down 10 "clicks"

		:param input_click_count:
		:return:
		"""
		pyautogui.scroll(input_click_count*-1)

	def scroll_mouse_up(self, input_click_count=10):
		"""
		scroll up 10 "clicks"

		:param input_click_count:
		:return:
		"""
		pyautogui.scroll(input_click_count)

	def search_same_position_for_input_picture_in_monitor(self, input_file_path):
		"""
		화면에서 같은 그림의 위치 찾기

		:param input_file_path:
		:return:
		"""
		result = []
		for pos in pyautogui.locateAllOnScreen(input_file_path):
			result.append(pos)
		return result

	def search_same_position_for_input_picture_in_monitor_by_gray_scale(self, input_file_path):
		"""
		그레이 스케일로 변경해서 찾기

		:param input_file_path:
		:return:
		"""
		result = []
		for pos in pyautogui.locateAllOnScreen(input_file_path, grayscale=True):
			result.append(pos)
		return result

	def search_center_of_same_position_for_input_picture_in_monitor(self, input_picture):
		"""
		화면위에서 들어온 그림의 위치를 찾아서 중간 위치를 알려주는 것

		:param input_picture:
		:return:
		"""

		pxywh = pyautogui.locateOnScreen(input_picture)
		pxy = pyautogui.center(pxywh)
		result = [pxy[0], pxy[1]]
		return result

	def select_from_curent_cursor(self, direction, press_times):
		"""
		현재위치에서 왼쪽이나 오른쪽으로 몇개를 선택하는 것

		:param direction:
		:param press_times:
		:return:
		"""
		pyautogui.keyDown("shift")
		for one in range(press_times):
			self.press_key_down(direction)
		pyautogui.keyUp("shift")

	def type_hotkey_n_char(self, input_hotkey, input_key):
		"""
		pyautogui.hotkey('ctrl', 'c') ==> ctrl-c to copy

		:param input_hotkey:
		:param input_key:
		:return:
		"""
		pyautogui.hotkey(input_hotkey, input_key)

	def type_action_key(self, action='enter', times=1, input_interval=0.1):
		"""
		키타이핑

		:param action:
		:param times:
		:param input_interval:
		:return:
		"""
		pyautogui.press(action, presses=times, interval=input_interval)

	def type_letter(self, input_text):
		"""
		암호나 글자를 입력하는 데 사용하는것이다
		이것은 대부분 마우스를 원하는 위치에 옮기고, 클릭을 한번한후에 사용하는것이 대부분이다
		그저 글자를 타이핑 치는 것이다
		"""
		pyperclip.copy(input_text)
		pyautogui.hotkey("ctrl", "v")

	def type_delete_n_times(self, input_no = 1000):
		"""
		현재위치에서 자료를 지우는것
		최대 한줄의 자료를 다 지워서 x 의 위치가 변거나 textbox 안의 자료가 다지워져 위치이동이 없으면 종료

		:return:
		"""
		for no in range(0, int(input_no)):
			position = pyautogui.position()
			pxy_old = [position.x, position.y]
			pyautogui.press('delete')
			position = pyautogui.position()
			pxy_new = [position.x, position.y]
			if pxy_old == pxy_new or pxy_old[1] != pxy_new[1]:
				break

	def type_backspace_n_times(self, input_no = 10):
		"""
		현재위치에서 자료를 지우는것
		죄대 한줄의 자료를 다 지워서 x 의 위지가 변거나 textbox 안의 자료가 다지워져 위지이동이 없으면 종료

		:param input_no:
		:return:
		"""
		for no in range(0, input_no):
			pyautogui.press('backspace')
			time.sleep(0.2)

	def type_ctrl_n_char(self, input_char):
		"""
		ctrl + 키를 위한것

		:param input_text:
		:return:
		"""
		pyautogui.hotkey('ctrl', input_char)


	def type_arrow_key_with_n_times(self, input_char, n_times = 1, interval=None):
		"""
		방향키를 n번 누르는것


		:param input_char:
		:return:
		"""
		base_data = {"left":"left", "왼쪽":"left", "right":"right", "오른쪽":"right", "up":"up", "위":"up", "down":"down", "아래":"down", }
		checked_char = base_data[input_char]
		for num in range(n_times):
			if not interval:
				time.sleep(interval)
			pyautogui.press(checked_char)  # press the left arrow key


	def type_text_with_interval(self, input_text, input_interval=0.1):
		"""
		그저 글자를 타이핑 치는 것이다
		pyautogui.pressfenter', presses=3z interval=3) # enter 키를 3 초에 한번씩 세번 입력합니다.

		:param input_text:
		:param input_interval:
		:return:
		"""
		pyautogui.typewrite(input_text, interval=input_interval)

	def type_text_for_hangul(self, input_text):
		"""
		영문은 어떻게 하면 입력이 잘되는데, 한글이나 유니코드는 잘되지 않아 찾아보니 아래의 형태로 사용하시면 가능합니다
		pyautogui 가 unicode 는 입력이 안됩니다

		:param input_text:
		:return:
		"""
		pyperclip.copy(input_text)
		pyautogui.hotkey('ctrl', "v")

	def type_text_one_by_one(self, input_text):
		"""
		영문은 어떻게 하면 입력이 잘되는데, 한글이나 유니코드는 잘되지 않아 찾아보니 아래의 형태로 사용하시면 가능합니다
		어떤경우는 여러개는 않되어서 한개씩 들어가는 형태로 한다

		:param input_text:
		:return:
		"""
		for one_letter in input_text:
			pyperclip.copy(one_letter)
			pyautogui.hotkey("ctrl", "v")

	def write_text_at_cursor(self, input_text):
		"""
		암호나 글자를 입력하는 데 사용하는것이다
		이것은 대부분 마우스를 원하는 위치에 옮기고, 클릭을 한번한후에 사용하는것이 대부분이다
		그저 글자를 타이핑 치는 것이다
		"""
		time.sleep(1)
		pyperclip.copy(input_text)
		pyautogui.hotkey("ctrl", "v")

	def write_text_at_previous_window(self, input_text ="가나다라abcd$^&*", start_window_no=1, next_line = 0):
		"""
		바로전에 활성화 되었던 윈도우에 글씨 써넣기

		:param input_text:
		:param start_window_no:
		:param next_line:
		:return:
		"""
		window_list = []
		for index, one in enumerate(gw.getAllTitles()):
			if one:
				window_list.append(one)
		previous_window = gw.getWindowsWithTitle(window_list[start_window_no])[0]
		previous_window.activate()
		if next_line==1:
			self.type_text_for_hangul(input_text)
			pyautogui.press('enter')
		else:
			self.type_text_for_hangul(input_text)

