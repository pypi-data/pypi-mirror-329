# -*- coding: utf-8 -*-
import folium
from folium import plugins
import json
import webbrowser
import os, math
import scolor, jfinder, youtil, basic_data
from folium.features import DivIcon
import basic_data_for_xymap

class xy_map:
	def __init__(self):
		"""
		지도를 좀더 쉽게 만들어주는 기능을 위해서 만든 것입니다
		기본적으로 folium을 사용합니다
		
		모든 공통정보는 vars를 통해서 전해지도록 한다
		"""
		self.color = scolor.scolor()
		self.xyre = jfinder.jfinder()
		self.util = youtil.youtil()
		self.vars = basic_data.basic_data().vars
		self.main_map = None
		self.all_cxy = basic_data_for_xymap.basic_data().vars
		self.cxy = None #cxy의 c는 coordinate의 약어임
		self.vars={
			"zoom_control" : True,
			"scrollWheelZoom" : True,
			"dragging" : True,
			"basic_cxy":[36.7835555121117, 126.99992340628],
			"location":[37.388738, 126.967983],
			"width":"100%",
			"height": "100%",
			"min_zoom": 0,
			"max_zoom": 18,
			"zoom_start": 10,
			"tiles": "OpenStreetMap",
			"prefer_canvas": False,
			"control_scale": False,
			"no_touch": False,
			"font_size": "1rem",
			"attr": None,
			"crs": "EPSG3857",
			"min_lat": None,
			"max_lat": None,
			"min_lon": None,
			"max_lon": None,

		}
		self.vars.update(self.vars)
		
		self.vars["color_type"] = ['lightred', 'gray', 'lightgreen', 'pink', 'lightblue', 'beige', 'black', 'darkgreen', 'darkblue',
						  'lightgray', 'green', 'white', 'red', 'blue', 'orange', 'darkred', 'purple', 'cadetblue',
						  'darkpurple']
		self.vars["icon_type"] = ["cloud", "info-sign", "star", "bookmark", "flag", ]
		self.vars["tile_style"] = ["OpenStreetMap", "Cartodb Positron", "Cartodb dark_matter"]


	def _check_l2d(self, input_value):
		"""
		_로 시작되는 것은 공통자료로도 사용가능한 것입니다

		2차원 자료를 확인하는 것
		cxy의 자료는 2차원료를 기본으로 사용하며,
		그래서 자료를 확인해서 1차원으로 들어오는 자료를 2차로 만드는 것이다
		1. 리스트가아닌 다른 자료형일때
		2. 1차원일때
		
		:param input_cxy_list:
		:return:
		"""
		if type(input_value) == type(()):
			input_value = list(input_value)

		if type(input_value) == type([]):
			if type(input_value[0]) == type([]) or type(input_value[0]) == type(()) :
				pass
			else:
				input_value = [input_value]
		else:
			input_value = [[input_value]]

		return input_value

	def cal_circle_size(self, input_value = 123, min_v=1, max_v=200, min_s=1, max_s=20):
		"""
		원의 크기를 자료의 형태에 따라서 정해주는 것
		원의 사이즈를 데이터의 크기에 따라서 다르게 할려고 하는 것이다
		자료에따라서 원의 크기를 다르게 만들고 싶을때 사용한다

		:param input_value:
		:param min_v:
		:param max_v:
		:param min_s:
		:param max_s:
		:return:
		"""
		min_size = min_s
		max_size = max_s
		min_value = min_v
		max_value = max_v
		if min_value > input_value:
			result  = min_size
		elif max_value < input_value:
			result = max_size
		else:
			result = (max_value - min_value +1) / (max_size - min_size +1)
		return result

	def change_date_data_to_time_line_style(self, input_l2d):
		"""
		plugin중 timeline을 만들때 사용하는 자료의 형태로 바꿔주는 것

				lines = [
			{
				"coordinates": [
					[139.76451516151428, 35.68159659061569],
					[139.75964426994324, 35.682590062684206],
				],
				"dates": ["2017-06-02T00:00:00", "2017-06-02T00:10:00"],
				"color": "red",
			},
			{
				"coordinates": [
					[139.7575843334198, 35.679505030038506],
					[139.76337790489197, 35.678040905014065],
				],
				"dates": ["2017-06-02T00:20:00", "2017-06-02T00:30:00"],
				"color": "green",
				"weight": 15,
			},
		]

		:param input_l2d:
		:return:
		"""
		result = []
		# l1d = [cxy1[0], cxy1[1], cxy2[0], cxy2[1], date1, date2, color, thickness]
		for l1d in input_l2d:
			temp_dic = {}
			temp_dic["coordinates"] = [[l1d[0], l1d[1]],[l1d[2], l1d[3]]]
			temp_dic["dates"] = [l1d[4], l1d[5]]
			temp_dic["color"] = l1d[6]
			temp_dic["weight"] = l1d[7]
			result.append(temp_dic)
		return result

	def change_scolor_to_text_rgb(self, input_scolor):
		"""
		scolor값을 "rgb(255, 0, 0)"의 형식으로 바꾸는 것
		folium의 rgb값의 형식은 이런식으로 넣어주어야 한다

		:param input_scolor:
		:return:
		"""
		rgb_list = self.color.change_scolor_to_rgb(input_scolor)
		result = "rgb(" + str(rgb_list[0]) + "," + str(rgb_list[1]) + "," + str(rgb_list[2]) + ")"
		return result

	def check_xy_data(self, input_list_1, input_list_2):
		"""
		선을 그리는 좌표를 알아서 확인해주는 기능
		folium에서 선을 그리는 것은 x는 x의 자료들만
		y는 y들만의 좌표로만 나타내는 것이다


		:param input_list_1:
		:param input_list_2:
		:return:
		"""
		result_1 = []
		result_2 = []

		if type(input_list_1[0]) == type([]):
			# 2차원의 자료이다
			for list_1d in input_list_1:
				result_1.append(list_1d[0])
				result_2.append(list_1d[1])
		else:
			result_1 = input_list_1
			result_2 = input_list_2

		return [result_1, result_2]

	def data_for_color_type(self):
		"""
		folium에서 사용가능한 색깔의 종류

		:return:
		"""
		result = self.vars["color_type"]
		return result

	def data_for_icon_type(self):
		"""
		folium에서 사용가능한 icon형태에 대한 자료

		:return:
		"""
		result = self.vars["icon_type"]
		return result

	def data_tile_style_all(self):
		"""
		folium은 지도를 나타낼때, 타일이라는 형식을 사용한다
		그래서 어떤 타일의 형식이 가능한지를 알려주는 것이다

		기본적인 설정값은 맨앞의 자료로 정한다

		:return:
		"""
		result = self.vars["tile_style"]
		return result

	def draw_polygon(self, input_map_obj, input_cxy_list):
		"""
		다각형의 닫힌 도형을 만드는 것이다

		:param input_map_obj: 다각형을 그릴 그림 객체
		:param input_cxy_list: 다각형으로 그릴 좌표들
		:return:
		"""
		if not input_map_obj: input_map_obj = self.main_map


		folium.PolyLine(
			locations=input_cxy_list,
			tooltip='Polygon',
			fill=True,
		).add_to(input_map_obj)

	def draw_arrow_marker(self, input_cxy_list, angle_list=[]):
		"""
		마커의 종류중에 화살표 방향을 표시할수있는 마커
		그래서, 좌표용 리스트와 별개로, 좌표의갯수만큼 화살표의 각도를 나타낼수도 있다

		:param input_cxy_list:
		:param icon_no:
		:param tooltip_text:
		:return:
		"""
		kw = {"prefix": "fa", "color": "green", "icon": "arrow-up"}
		input_cxy_list = self._check_l2d(input_cxy_list)
		default_angle = 90
		if type(angle_list) != type([]):
			angle_list = [angle_list]

		if len(input_cxy_list) > len(angle_list):
			for one in range(len(input_cxy_list) - len(angle_list)):
				angle_list.append(default_angle)

		for index, one_cxy in enumerate(input_cxy_list):
			folium.Marker(location=one_cxy, icon=folium.Icon(angle=angle_list[index], **kw)).add_to(self.main_map)

	def draw_choropleth(self, input_title, input_geo, input_df, col_name_for_geo, col_name_for_data, input_property="동"):
		"""
		columns = (지도 데이터와 매핑할 데이터, 시각화 하고려는 데이터)
		등치 지역도는 데이터 값에 따라 행정 구역에 색상이 지정되거나 음영 처리되는 주제별 지도입니다
		choropleth : 행정구역별 구분되는 지도

		:param input_geo:
		:param input_data:
		:param input_columns:
		:return:
		"""
		self.main_map = folium.Choropleth(
			geo_data=input_geo,
			data=input_df,
			columns=[col_name_for_geo, col_name_for_data],
			key_on='feature.properties.'+input_property,
			fill_color='BuPu',
			legend_name=input_title,
		).add_to(self.main_map)

	def draw_choropleth_at_map(self, geo_data, table_data, bar_title):
		"""
		Choropleth 레이어를 만들고, 맵에 추가합니다.

		:param geo_data:
		:param table_data:
		:param bar_title:
		:return:
		"""
		self.main_map = self.make_main_map_object("", 8)
		folium.Choropleth(
			geo_data=geo_data,
			data=table_data,
			columns=('name', 'code'),
			key_on='feature.properties.name',
			fill_color='BuPu',
			legend_name=bar_title,
		).add_to(self.main_map)

	def draw_circle(self, input_cxy_list, input_size_meter, popup_text=None, line_scolor=None, fill_scolor=None):
		"""
		원 그리기
		1개의 자료만 와도 2차원리스트로 만들어 준다

		:param input_cxy_list: 원을 만들고 싶은 좌표, 원의 중심점 좌표
		:param input_size_meter: 원의 크기
		:param popup_text: 원의 팝업시 나타나는 글자
		:param line_scolor: 선의 색
		:param fill_scolor: 배경색
		:return:
		"""
		if line_scolor: line_scolor = self.change_scolor_to_text_rgb(line_scolor)
		if fill_scolor: fill_scolor = self.change_scolor_to_text_rgb(fill_scolor)

		input_cxy_list = self._check_l2d(input_cxy_list)

		for index, one_cxy in enumerate(input_cxy_list):
			folium.CircleMarker(
				location=one_cxy,
				radius=input_size_meter,  # 점의 크기
				popup=popup_text,
				color=line_scolor,
				fill=True,
				fill_color=fill_scolor,
			).add_to(self.main_map)

	def draw_colorline(self, input_cxy_list, input_scolor_list):
		"""
		색을 입히면서 만드는 라인
		:return:
		"""

		folium.ColorLine(
			positions=input_cxy_list,
			colors=input_scolor_list,
			colormap=["y", "orange", "r"],
			weight=10,
		).add_to(self.main_map)

	def draw_custom_marker(self, input_cxy, icon_image_path, shadow_image_path=None, tooltip_text=None):
		"""
		사용자가 만든 마커를 넣는 것

		:param input_cxy:
		:param icon_image_path:
		:param shadow_image_path:
		:param tooltip_text:
		:return:
		"""
		icon_image = icon_image_path
		my_icon = folium.CustomIcon(
			icon_image,
			icon_size=(38, 38),
			icon_anchor=(22, 94),
			shadow_image=shadow_image_path,
			shadow_size=(50, 64),
			shadow_anchor=(4, 62),
			popup_anchor=(-3, -76),
		)

		folium.Marker(location=input_cxy, icon=my_icon, tooltip=tooltip_text).add_to(self.main_map)


	def draw_heatmap(self, input_cxy_list, circle_size=500):
		"""
		서로 가까이 점이잇으면, 색이 진하게 되는 것입니다
		히트 맵 레이어 생성

		:param input_cxy_list:
		:param circle_size:
		:return:
		"""
		input_cxy_list = self._check_l2d(input_cxy_list)

		folium.plugins.HeatMap(input_cxy_list,
						#min_opacity=0.2,
						radius=circle_size,
						blur=50,
						max_zoom=1).add_to(self.main_map)

	def draw_heatmap_withtime(self, heat_data, circle_size = 40, total_date2=None):
		"""
		자료는 frame개념으로 보여준다
		1개의 프레임은 1개의 자료의 묶음이다
		즉, 시간으로 나타내는 부분이 아닌것이다, 만약 시간별로 나타내고싶다면, 자료 자체를 일정한 간격으로 만들면 됩니다

		data 파라미터는 파이썬 리스트 자료형만 인식

		HeatMapWithTime 은 특정지역의 시간에 따른 변화를 나타내는 역할을 하기 때문에, 공간과 시간, 이렇게 두 가지 축이 필요하다.

		lat_lng_by_hour = [
			[[37.56071136, 126.91485473, 0.3]],  # 0
			[[37.56071136, 126.91485473, 0.4]],  # 1
			[[37.56071136, 126.91485473, 0.5]],  # 2
			[[37.56071136, 126.91485473, 0.6]],  # 3
			[[37.56071136, 126.91485473, 0.1]],  # 4 ]

		lat_lng_by_hour[0] 은 0번째 시간의 모든 점들을 담고 있으며,
		lat_lng_by_hour[0][1] 은 0번째 시간의 점 중, 첫 번째 점을 나타낸다.
		lat_lng_by_hour[0][1][0] 은 0번째 시간의 점 중, 첫 번째 점의 위도를 나타낸다.

		:param heat_data:
		:param total_date2:
		:return:
		"""

		folium.plugins.HeatMapWithTime(heat_data, radius=circle_size,index=total_date2).add_to(self.main_map)

	def draw_json_data(self, input_map_obj, json_data, input_name):
		"""
		json자료를 지도위에 그리는 것

		:param input_map_obj:
		:param json_data:
		:param input_name:
		:return:
		"""
		if not input_map_obj: input_map_obj = self.main_map


		folium.GeoJson(
			json_data,
			name=input_name
		).add_to(input_map_obj)

	def draw_json_file(self, input_json_file='skorea_municipalities_geo_simple.json'):
		"""
		json화일로 그리기

		:param input_json_file:
		:return:
		"""
		# input_json_file = "skorea_municipalities_geo_simple.json" #시단위

		with open(input_json_file, mode='rt', encoding='utf-8') as f:
			geo = json.loads(f.read())
			f.close()
		folium.GeoJson(geo, name='seoul_provinces').add_to(self.main_map)

	def draw_line(self, input_cxy_list, input_scolor, thickness_1to10=5, tooltip=None, opacity_oto1=1):
		"""
		input으로 시작하는 인수는 꼭 입력해야하는것이고, 아닌 것은 앞에 붙이지 않거나 다른 용어를 사용한다

		:param input_cxy_list:
		:param input_scolor:
		:param thickness_1to10:
		:param tooltip:
		:param opacity_oto1:
		:return:
		"""
		input_cxy_list = self._check_l2d(input_cxy_list)
		if input_scolor: input_scolor = self.change_scolor_to_text_rgb(input_scolor)

		folium.PolyLine(
			locations=input_cxy_list,
			color=input_scolor,
			weight=thickness_1to10,
			opacity=opacity_oto1,
			tooltip=tooltip
		).add_to(self.main_map)

	def draw_marker(self, input_cxy_list, tooltip_text=None, setup_draggable_tf=False):
		"""
		좌표에 마커를 만드는 것

		:param input_cxy_list:
		:param tooltip_text:
		:param setup_draggable_tf:
		:return:
		"""
		input_cxy_list = self._check_l2d(input_cxy_list)

		for index, one_cxy in enumerate(input_cxy_list):
			folium.Marker(location=one_cxy, tooltip=tooltip_text, draggable=setup_draggable_tf).add_to(self.main_map)


	def draw_marker_with_icon_type(self, input_cxy_list, icon_no=1, tooltip_text=None):
		"""
		마커에 표시하는 아이콘을 선택할수가 있다

		icon의 색은 hex도 가능하다.
		fm = folium.Map(location=(44,3), tiles="Stamen Terrain")
		folium.Marker(
				location=(44,3.2),
				popup="data1",
				icon=folium.Icon(color='#8000ff',icon_color='#4df3ce', icon="star", prefix="fa"),
			).add_to(fm)
		fm

		:param input_cxy_list:
		:param icon_no:
		:param tooltip_text:
		:return:
		"""

		input_cxy_list = self._check_l2d(input_cxy_list)

		for index, one_cxy in enumerate(input_cxy_list):
			folium.Marker(location=one_cxy, icon=folium.Icon(color='red', icon=self.vars["icon_type"][icon_no - 1]),
						  tooltip=tooltip_text).add_to(self.main_map)

	def draw_marker_with_serial_no(self, input_cxy_list, start_no=1):
		"""
		한줄이 아닌 여러 줄을 연결할때, 각 줄의 끝부분에 번호로된 마커를 넣는 방법
		시작 번호를 지정할수가 있다

		:param input_cxy_list:
		:param start_no:
		:return:
		"""
		input_cxy_list = self._check_l2d(input_cxy_list)

		for index, one_cxy in enumerate(input_cxy_list):
			new_no = start_no + index
			folium.Marker(
				location=one_cxy,
				icon=plugins.BeautifyIcon(icon="arrow-down", icon_shape="circle", border_width=2, number=new_no,
										  tooltip=new_no),
			).add_to(self.main_map)

	def draw_polyline_with_time_period(self, input_l2d=""):
		"""
		다각형자료를 시간때별로 변하는 지도를 만드는 것

		:param input_l2d:
		:return:
		"""
		# Lon, Lat order.
		lines = self.change_date_data_to_time_line_style(input_l2d)

		features = [
			{
				"type": "Feature",
				"geometry": {
					"type": "LineString",
					"coordinates": line["coordinates"],
				},
				"properties": {
					"times": line["dates"],
					"style": {
						"color": line["color"],
						"weight": line["weight"] if "weight" in line else 5,
					},
				},
			}
			for line in lines
		]

		folium.plugins.TimestampedGeoJson(
			{
				"type": "FeatureCollection",
				"features": features,
			},
			period="PT1M",
			add_last_point=True,
		).add_to(self.main_map)

	def draw_rectangle(self, input_map_obj, input_cxy_list):
		"""
		사각형 그리기

		:param input_map_obj:
		:param input_cxy_list:
		:return:
		"""
		if not input_map_obj: input_map_obj = self.main_map
		input_cxy_list = self._check_l2d(input_cxy_list)

		folium.PolyLine(
			locations=input_cxy_list,
			tooltip='Rectangle'
		).add_to(input_map_obj)

	def get_360_out_side(self, input_xy_list, base_xy):
		"""
		모든 xy리스자료중에서 기준좌표를 기준으로하여 360도로 가장 먼 좌표들만 만드는 것

		:param input_xy_list:
		:param base_xy:
		:return:
		"""
		input_xy_list = self._check_l2d(input_xy_list)


		pi = 3.1415926535
		result = {}
		x0, y0 = base_xy
		for old_xy in input_xy_list:
			one_xy = [float(old_xy[0]),float(old_xy[1])]
			x, y = one_xy
			#print(base_xy, one_xy)
			degree = int(math.atan2(x0-x, y0-y) * 180 / pi)
			a = (x0 - x)
			b = (y0 - y)
			distance = math.sqrt((a * a) + (b * b))

			if degree in result.keys():
				if result[degree][0] < distance:
					result[degree] = [distance, x, y]
			else:
				result[degree] = [distance, x, y]
		return result

	def insert_plugin_for_click_marker(self):
		"""
		화면을 클릭하면 마커가 만들어지는 것
		교육용으로 사용가능 한 방법으로 보인다
		:return:
		"""
		self.main_map.add_child(folium.ClickForMarker())

	def insert_plugin_for_filter(self, input_data):
		"""
		menu group와같이 비슷한 형태로 사용되는것으로, filter라는 개념으로 사용합니다

		:param input_data:
		:return:
		"""

		unique_data = set()
		for i, cxy in enumerate(input_data):
			folium.Marker(
				cxy,
				tags=[input_data[i][2]]
			).add_to(self.main_map)
			unique_data.add(input_data[i][2])

		folium.plugins.TagFilterButton(list(unique_data)).add_to(self.main_map)

	def insert_plugin_for_minimap(self):
		"""
		화면에 미니지도를 넣는것
		:return:
		"""
		minimap = plugins.MiniMap()
		self.main_map.add_child(minimap)

	def insert_plugin_for_mouse_position(self):
		"""
		마우스의 위치를 알려주는 것을 넣는 것
		:return:
		"""
		folium.plugins.MousePosition().add_to(self.main_map)

	def insert_plugin_for_my_position(self):
		"""
		나의 위치를 알려주는 것을 넣는 것
		:return:
		"""
		folium.plugins.LocateControl().add_to(self.main_map)

	def make_basic_data_set(self, input_lists):
		"""
		읽어오고 싶은 자료들을 자료의 형태에 따라서 만들어야 한다

		:param input_lists:
		:return:
		"""
		result = []
		for one_data in input_lists:
			temp_dic = {}
			temp_dic["address_full"] = one_data[9]
			temp_dic["address_middle"] = one_data[8]
			temp_dic["address_top"] = one_data[7]
			temp_dic["water_element"] = one_data[6]
			temp_dic["temp"] = one_data[5]
			temp_dic["ph"] = one_data[4]
			temp_dic["water_type"] = one_data[3]

			# 아래의 자료는 기본적으로 folium에서 사용되는 형태이다
			temp_dic["title"] = str(one_data[3]) + "<br>" + str(one_data[4]) + "<br>" + str(one_data[5]) + "<br>" + str(
				one_data[6]) + "<br>" + str(one_data[7]) + "<br>" + str(one_data[8]) + "<br>" + str(one_data[9])
			temp_dic["xy"] = [one_data[2], one_data[1]]
			temp_dic["pop_text"] = one_data[8]
			temp_dic["html"] = one_data[8] + "<br>" + temp_dic["title"]
			temp_dic["iframe"] = folium.IFrame(html=temp_dic["html"], width=300, height=200)
			result.append(temp_dic)
		return result

	def make_main_map_object(self, input_cxy, zoom_no):
		"""
		지도의 중앙지점과 줌의 정도를 설정한다
		우리나라의 중앙일것같은 온양온천을 기준으로 표시

		:param input_cxy:
		:param zoom_no:
		:return:
		"""
		input_cxy = self.vars["basic_cxy"](input_cxy)
		self.main_map = folium.Map(
			location=input_cxy,
			zoom_start=zoom_no,
			# width=750,
			# height=500,
			# tiles='Stamen Toner' #타일의 종류를 설정하는 것이다
		)
		return self.main_map

	def draw_marker_by_cxy_tooltip_menu(self, cxy, tool_tip, menu):
		if type(cxy) == type("abc"):
			cxy = self.change_address_to_cxy(cxy)
		folium.Marker(
			location=cxy,
			tooltip = tool_tip,
			tags=[menu],
		).add_to(self.main_map)

		folium.plugins.TagFilterButton(menu).add_to(self.main_map)

	def draw_marker_with_list_2d_as_cxy_tooltip_menu(self, input_l2d):
		"""
		input_l2d =  [[cxy, tool_tip, menu]....]
		만약 cxy대신에 주소가 들어가면 그분은 자동으로 변경이 되도록 한다

		1개씩 자료를 마커로 만들면, 필터로 나타나는 것이 여러개 나타나므로, 한번에 모든 자료를 넣어야 합니다

		자료의 정확성을 위해 다음의 기능을 추가하였읍니다
		- 만약 메뉴부분을 넣지 않으면 그냥 빈문자열을 넣는다
		- 만약 cxy가 아닌 일반 주소가 들어가면, cxy로 변경하는 기능도 추가하였읍니다
		- 만약 1개의 자료만 온다면, 그것은 어떤 의미가 있는지 모르므로, 잘못된 자료로 인식해서, 그냥 넘어가도록 합니다

		"""
		unique_data = set()
		for i, l1d in enumerate(input_l2d):
			if len(l1d) == 2:
				l1d.append("")
			unique_data.add(l1d[2])

		icon_dic = {}
		icon_count = len(self.vars["color_type"])
		for index, one in enumerate(list(unique_data)):
			icon_dic[one] = self.vars["color_type"][divmod(index, icon_count)[1]]

		for i, l1d in enumerate(input_l2d):
			if len(l1d) == 1:
				pass
			else:
				if type(l1d[0]) == type("abc"):
					l1d[0] = self.change_address_to_cxy(l1d[0])
				folium.Marker(
					location=l1d[0],
					tooltip = l1d[1],
					tags=[l1d[2]],
					icon=folium.Icon(color=icon_dic[l1d[2]])
				).add_to(self.main_map)

		folium.plugins.TagFilterButton(list(unique_data)).add_to(self.main_map)

	def draw_marker_with_list_2d_as_cx_cy_tooltip_menu(self, input_l2d):
		"""
		엑셀의 자료를 갖고올때, 쉽게 사용가능하도록 만드는 것이다

		input_l2d =  [[cx, cy, tool_tip, menu]....]
		만약 cxy대신에 주소가 들어가면 그분은 자동으로 변경이 되도록 한다

		1개씩 자료를 마커로 만들면, 필터로 나타나는 것이 여러개 나타나므로, 한번에 모든 자료를 넣어야 합니다

		자료의 정확성을 위해 다음의 기능을 추가하였읍니다
		- 만약 메뉴부분을 넣지 않으면 그냥 빈문자열을 넣는다
		- 만약 cxy가 아닌 일반 주소가 들어가면, cxy로 변경하는 기능도 추가하였읍니다
		- 만약 1개의 자료만 온다면, 그것은 어떤 의미가 있는지 모르므로, 잘못된 자료로 인식해서, 그냥 넘어가도록 합니다

		"""
		input_l2d = self.util.change_any_data_type_to_list_2d(input_l2d)

		unique_data = set()
		#자료가 맞는지를 확인하는 것, 틀리면 고치는 것
		for i, l1d in enumerate(input_l2d):
			unique_data.add(l1d[3])

		icon_dic = {}
		icon_count = len(self.vars["color_type"])
		for index, one in enumerate(list(unique_data)):
			icon_dic[one] = self.vars["color_type"][divmod(index, icon_count)[1]]

		for i, l1d in enumerate(input_l2d):
			if type(l1d[0]) == type("abc"):
				cxy_new = self.change_address_to_cxy(l1d[0])
				l1d[0] = cxy_new[0]
				l1d[1] = cxy_new[1]

			folium.Marker(
				location=[l1d[0],l1d[1]] ,
				tooltip = l1d[2],
				tags=[l1d[3]],
				icon=folium.Icon(color=icon_dic[l1d[3]])
			).add_to(self.main_map)

		folium.plugins.TagFilterButton(list(unique_data)).add_to(self.main_map)


	def make_menu_with_main_n_sub_menu(self, input_lists, main_n_sub, icon_n_color):
		"""
		input_lists = [
			['37.55440684521157', '127.12937429453059','food_land','방이 샤브샤브','맛나는데 여자들이 더 좋아해요'],
			['37.1834787433397','128.466953597959','food_land','미탄집','메밀전병'],
			['37.2079513137108','128.986557255629','food_land','구와우순두부','순두부'],
			]

		# 메인 메뉴와 서브메뉴를 정의한다
		main_n_sub = [['육해공군', 'food_land', 'food_sea', 'food_sky'], ["카페를 한눈에", 'cafe', 'food_etc','etc']]
		# 서브메뉴에 보일 아이콘과 색을 정의한다
		icon_n_color = {'food_land': ['lightred', 'cloud'], 'food_sea': ['gray', 'info-sign'], 'food_sky': ['lightgreen', 'star'], 'cafe': ['gray', 'info-sign'], 'food_etc': ['lightgreen', 'star'], 'etc': ['pink', 'bookmark']}

		:param input_lists:
		:param main_n_sub:
		:param icon_n_color:
		:return:
		"""
		menu_dic = {}
		sub_menu_dic = {}
		for ix, one_list in enumerate(main_n_sub):
			exec(f"main_menu_{ix} = folium.FeatureGroup(name='{one_list[0]}')")
			exec(f"self.main_map.add_child(main_menu_{ix})")
			exec(f"menu_dic['{one_list[0]}'] = main_menu_{ix}")

			for iy, sub_menu in enumerate(one_list[1:]):
				exec(f"sub_menu_{iy} = plugins.FeatureGroupSubGroup(main_menu_{ix}, '{sub_menu}')")
				exec(f"self.main_map.add_child(sub_menu_{iy})")
				exec(f"sub_menu_dic['{sub_menu}'] = sub_menu_{iy}")

		# 만약 icon_n_color에 아무런 값도 없을때 만들어 지는 것
		if not icon_n_color:
			icon_type = self.data_for_icon_type()
			color_type = self.data_for_color_type()
			icon_color = {}
			for ix, one_list in enumerate(main_n_sub):
				for iy, sub_menu in enumerate(one_list[1:]):
					icon_color[sub_menu] = [color_type[ix + iy], icon_type[ix + iy]]
			print(icon_color)

		folium.LayerControl(collapsed=False).add_to(self.main_map)
		for one_data in input_lists:
			folium.Marker(
				location=[one_data[0], one_data[1]],
				popup=one_data[2],
				icon=folium.Icon(color=icon_n_color[one_data[2]][0], icon=icon_n_color[one_data[2]][1]),
				tooltip=one_data[3],
			).add_to(sub_menu_dic[one_data[2]])

	def make_sub_menu_group(self, top_menu_title, category_location, input_title, all_data_set):
		"""
		서브 메뉴를 만드는 것
		오른쪽의 선택하는 그룹에 나타나게 할것인지를 설정하는 것이다

		:param top_menu_title:
		:param category_location:
		:param input_title:
		:param all_data_set:
		:return:
		"""
		self.main_map = self.make_main_map_object("", 8)
		dic_sub_menus = {}
		fg_name = folium.FeatureGroup(name=top_menu_title)
		self.main_map.add_child(fg_name)

		for num in range(len(category_location)):
			sun_menu_name = category_location[num]
			aaa = plugins.FeatureGroupSubGroup(fg_name, sun_menu_name, show=True)
			self.main_map.add_child(aaa)
			dic_sub_menus[sun_menu_name] = aaa

			for one_dic in all_data_set:
				if one_dic[input_title] in list(dic_sub_menus.keys()):
					folium.Marker(
						location=one_dic["xy"],
						popup=folium.Popup(one_dic["iframe"]),
						icon=folium.Icon(icon_size=(25)),  # 아이콘을 설정한 것이다
						tooltip=one_dic["title"],
					).add_to(dic_sub_menus[one_dic[input_title]])

	def make_top_menu_group(self, top_menu_name):
		"""
		탑메뉴를 만드는 것

		:param top_menu:
		:return:
		"""
		self.main_map = self.make_main_map_object("", 8)
		top_menu_obj = folium.FeatureGroup(name=top_menu_name)
		self.main_map.add_child(top_menu_name)
		return [top_menu_obj, self.main_map]

	def make_unique_list(self, input_lists, input_no):
		"""
		리스트의 자료중에서 고유한것들만 돌려주는 것

		:param input_lists:
		:param input_no:
		:return:
		"""
		result = set()
		for one in input_lists:
			result.add(one[input_no])
		return list(result)

	def new_map(self, start_cxy="", zoom_no=8, **input_dic):
		"""
		지도의 중앙지점과 줌의 정도를 설정한다
		우리나라의 중앙일것 같은 온양온천을 기준으로 표시

		:param start_cxy:
		:param zoom_no:
		:param input_dic:
		:return:
		"""

		if not start_cxy:
			start_cxy =[37.388738, 126.967983]

		self.vars.update(input_dic)
		self.vars["location"] = start_cxy
		self.vars["zoom_start"] = zoom_no

		self.main_map = folium.Map(
			zoom_control = self.vars["zoom_control"],
			scrollWheelZoom = self.vars["scrollWheelZoom"],
			dragging = self.vars["dragging"],
			location= self.vars["location"],
			width= self.vars["width"],
			height= self.vars["height"],
			min_zoom= self.vars["min_zoom"],
			max_zoom= self.vars["max_zoom"],
			zoom_start= self.vars["zoom_start"],
			tiles= self.vars["tiles"],
			prefer_canvas= self.vars["prefer_canvas"],
			control_scale= self.vars["control_scale"],
			no_touch= self.vars["no_touch"],
			font_size= self.vars["font_size"],
			attr= self.vars["attr"],
			crs= self.vars["crs"],
			min_lat = None,
			max_lat = None,
			min_lon = None,
			max_lon = None,
		)

		return self.main_map

	def new_map_as_empty(self, start_cxy="", zoom_no=8, **input_dic):
		"""
		지도없이 좌표에 표시만 하기
		지도의 중앙지점과 춤의 정도를 설정한다
		우리나라의 중앙일것같은 온양은천을 기준으로 표시

		:param start_cxy:
		:param zoom_no:
		:param input_dic:
		:return:
		"""

		#self.main_map = folium.Map( location=start_cxy, zoom_start=zoom_no, tiles=None)
		self.vars["tiles"] = None
		self.new_map(start_cxy, zoom_no, **input_dic)

	def print_by_step(self, input_list, input_step):
		"""
		입력한 자료를 원하는 갯수만큼씩 프린트하는 방법이다
		개당은 짧은데, 하나씩 하면 짧아서 몇개씩

		:param input_list2d:
		:param input_step:
		:return:
		"""
		print("[")
		for one in range(0, len(input_list), input_step):
			print(str(input_list[one:one + input_step])[1:-1] + ",")
		print("]")

	def read_json_data(self, file_path):
		"""
		json자료를 읽어오는 것
		:param file_path:
		:return:
		"""
		with open(file_path, mode='rt', encoding='utf-8') as f:
			result = json.loads(f.read())
			f.close()
		return result

	def setup_dragging_for_map_by_0or1(self, input_tf=False):
		"""
		드래그를 가능하게 할것인지 : 키거나 끄는 설정

		:param input_tf:
		:return:
		"""
		self.vars["dragging"] = input_tf

	def setup_map_height(self, input_no):
		"""
		화면의 크기(높이)를 설정

		:param input_no:
		:return:
		"""
		self.vars["width"] = input_no

	def setup_scroll_wheel_zoom_by_0or1(self, input_tf = False):
		"""
		마우스 스크롤 : 키거나 끄는 설정

		:param input_tf:
		:return:
		"""
		self.vars["scrollWheelZoom"] = input_tf

	def setup_show_cxy_by_click(self):
		"""
		클릭하면 좌표를 표시하는 기능
		:return:
		"""
		self.main_map.add_child(folium.LatLngPopup())

	def setup_map_width(self, input_no):
		"""
		화면의 크기(넓이)를 설정

		:param input_no:
		:return:
		"""
		self.vars["width"] = input_no

	def setup_onoff_for_zoom_by_0or1(self, input_tf = False):
		"""
		줌 : 키거나 끄는 설정

		:param input_tf:
		:return:
		"""
		self.vars["zoom_control"] = input_tf

	def setup_zoom_start_by_0to18(self, input_no=8):
		"""
		맨처음 보이는 지도의 줌상태를 설정하는 것

		:param input_no:
		:return:
		"""
		self.vars["zoom_start"] = input_no

	def show_map(self, input_file_name="xymap_sample.html"):
		"""
		사전을 보여주는 메소드

		:param input_file_name:
		:return:
		"""
		if not input_file_name.endswith(".html"): input_file_name = input_file_name + ".html"
		self.main_map.save(input_file_name)
		webbrowser.open('file://' + os.path.abspath(input_file_name))

	def write_text_with_box_in_map(self, input_cxy="", input_text=""):
		"""
		사각형안에 글씨쓰기

		:param input_text:
		:param input_cxy:
		:return:
		"""
		input_cxy = self.vars["basic_cxy"](input_cxy)
		folium.map.Marker(input_cxy,
						  icon = DivIcon(
						  icon_size=(150, 50), icon_anchor=(0,0),
						  html = f"""<div style="display: flex; justify-content: center; align items: center; border: 2px solid blue; background-color: lightblue; 
						  padding: 10px;p style="margin: 0;">{input_text}</p></div>""",) ).add_to(self.main_map)

	def write_text_with_circle_in_map(self, input_cxy="", input_text="123"):
		"""
		원안에 글자를 쓰도록 만든것
		사각형의 형태가 기본이라, 너무 많이 쓰면 원을 조금 넘어간다

		:param input_cxy:
		:param input_text:
		:return:
		"""
		input_cxy = self.vars["basic_cxy"](input_cxy)
		folium.map.Marker(input_cxy, icon=DivIcon(
							icon_size=(50, 50),
							icon_anchor=(0, 0),
							html=f"""<div style="display: flex; border-radius: 50%; justify-content: center; align items: center; border: 2px solid blue; background-color: lightblue; 
						padding: 10px;p style="margin: 0;">{input_text}</p></div>""", )).add_to(self.main_map)



	def change_address_to_cxy(self, input_address=""):
		"""
		일반 주소를 좌표로 만들어 주는것
		그러나 주소가 너무 짧으면 찾기가 어려우므로 찾은것이 3개이하가 되면, 문제가 있는 주소로 생각해야 한다

		기번 좌표의 형태 : [22218, '인천광역시', '', '중구', '', '송월동3가', 37.478114, 126.620739, '인천광역시 중구 송월동3가'],

		:param input_address:
		:return:
		"""

		fix_list = [["부산시", "부산광역시"],["인천시","인천광역시"],[ "대구시", "대구광역시"],[ "대전시", "대전광역시"],
					["광주시","광주광역시"],["울산시","울산광역시"],[ "세종시", "세종특별자치시"],["서울시","서울특별시"],
					["강원특별자치도","강원도"],["전북특별자치도","전라북도"], ["제주도","제주특별자치도"],
					["충남", "충천남도"],["충북", "충청북도"],["전북", "전라북도"],["전남", "전라남도"],["경남", "경상남도"],["경북", "경상북도"],
					]
		for one in fix_list:
			input_address = input_address.replace(one[0], one[1])
		all_address_l1d = input_address.strip().split(" ")
		#print(all_address_l1d)
		all_found_cxy_l2d = self.all_cxy

		for address_part in all_address_l1d[::-1]:
			temp = []
			# print("확인할 갯수는 => ", len(all_found_cxy_l2d), address_part)
			found_num = self.xyre.search_all_with_jf_sql("[숫자:1~]", address_part)

			for l1d in all_found_cxy_l2d:
				if address_part in l1d[8]:
					temp.append(l1d)

			# 만약 찾은값이 없고, 혹시 중간에 숫자가 있을때
			# 다시한번 숫자부터 뒷부분을 제거하고 찾는 것
			if temp == [] and found_num:
				#print(found_num, address_part[0:found_num[0][1]])
				for l1d in all_found_cxy_l2d:
					if address_part[0:found_num[0][1]] in l1d[8]:
						temp.append(l1d)
			all_found_cxy_l2d = temp

		# 만약 찾은것이 여러개일때는 제일 처음의 것을 사용하도록 하자
		#print(all_found_cxy_l2d)
		if len(all_found_cxy_l2d) > 1:
			all_found_cxy_l2d = all_found_cxy_l2d[0]
		return all_found_cxy_l2d[6:8]

	def draw_marker_for_text_address(self, text_address):
		cxy = self.change_address_to_cxy(text_address)
		self.draw_marker(cxy)

	def draw_marker_for_text_address_with_tool_tip(self, text_address, tool_tip):
		cxy = self.change_address_to_cxy(text_address)
		self.draw_marker(cxy, tool_tip)



	def manual_for_words(self):
		result="""
		cxy : coordinate xy의 뜻으로 지도좌표를 뜻한다
		
		"""
		return result