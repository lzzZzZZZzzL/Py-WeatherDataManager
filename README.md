现代程序设计期末大实验要求：
使用Python语言编程开发一个简易的天气信息管理系统。
1）	应实现的基本功能包括：
	a)	数据管理：使用CSV文件管理天气数据，能够兼容从https://rp5.ru/下载的CSV文件，能够增加/删除某地区或某时间段内的天气数据。（CSV文件统一使用UTF-8编码）
	b)	天气信息查询：根据给定的地区、日期范围、气象参数（如：气温、气压、湿度、风向、降雨量等）等组合条件查询并展示天气信息。
	c)	天气信息统计：根据给定的地区、日期范围统计某气象参数的平均值、最小值、最大值等，通过图形展示该气象参数的变化情况（可使用折线图）及分布情况（可使用柱状图或饼状图	等）。
	d)	用户管理：设置管理员与普通用户两类账号。管理员能够修改天气数据，能够设置普通用户的权限（如限制某用户可查询的日期范围、气象参数等）。普通用户只能进行天气信息的查	询与统计。
2）	在实现基本功能的基础上，可加入若干进阶功能，包括但不限于：
	a)	天气信息比较：对比同一地区不同时间段、或不同地区同一时间段的气象信息。
	b)	自然语言查询：根据用户输入的问题返回相关结果。如回答“深圳市2021年12月的平均气温是？”、“广州市2023年9月1日出门要带伞吗？”等问题。
	c)	语音助手：选择某些基于python的语音识别工具，将其整合到系统中，通过语音命令查询天气信息。（参考：https://pypi.org/project/SpeechRecognition/；GitHub - 	llxlr/Speech-Recognition-With-Python: Speech Recognition With Python | python语音识别；https://anaconda.org/conda-forge/speechrecognition）。
	d)	天气预测：选择某些机器学习算法，通过历史数据预测未来的天气情况。
	e)	在线爬取数据：实现一个功能，可以自动地从https://rp5.ru/爬取某地区某时间段内的天气数据，并将其添加到已有的数据库内。
	f)	数据可视化工具：提供更多样的图形化工具，让用户可以自由选择和定制天气数据的展示方式，如热图、雷达图等。
	g)	图形界面：默认情况下通过命令行进行用户交互，可通过编程设计图形界面进行用户交互。




完成情况：实现了所有基本功能和进阶功能中的数据可视化工具，可以获取网站数据的下载链接，将下载的文件导入数据库，注册且登录后的用户可查询和统计数据库中的天气数据，也可以进行可视化；管理员还可以管理所有用户的权限和增加/删除数据库里的数据，其他功能也许假期有时间继续开发--------2024.12.26
