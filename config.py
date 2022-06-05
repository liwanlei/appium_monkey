""" 
@author: lileilei
@file: config.py 
@time: 2018/5/6 17:32 
"""
TESTPLANURL='http://127.0.0.1:8000/gettask/'#平台的获取用例
CreatRepoet='http://127.0.0.1:8000/greatreport/'#创建测试报告
SendxingUrl='http://127.0.0.1:8000/sendxing/'#创建性能
GetYilaiUrl='http://127.0.0.1:8000/yilaicase/'
TestreportUrl='http://127.0.0.1:8000/testreport/'
xinengreportUlr='http://127.0.0.1:8000/xingneng/'
Dingtalk_title='UI自动化测试执行结果汇报'
DINGTALK_URL='https://oapi.dingtalk.com/robot/?access_token=0189f3ef3d878cca3084038d8c8d3506565e7b411f578b5a8252edbf49abe81d'#钉钉机器人whook
usetype='project' #配置task或project
usertoken='d6f82c64df3dc34921d79e5f22e5d43a'#平台上面已经有的用户的token，后台会校验
taskname='学生app安卓'#平台上的task名称或project名称
tes_event='appios版本47环境'#平台上project的测试环境,task类型这里无需配置
Testplatform='Android'#测试的设备的系统
TestplatformVersion='4.4.2'#测试的系统版本
TestappActivity='com.qihoo.browser.launcher.LauncherActivity'#测试的app
TestappPackage='com.qihoo.browser'#测试app启动类
Testdevicesname='127.0.0.1:62001'#devices name
TestandroidDeviceReadyTimeout='30'
TestunicodeKeyboard=True
TestresetKeyboard=True
