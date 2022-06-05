# -*- coding: utf-8 -*-
"""
====================================
@File Name ：uimonkey.py
@Time ： 2022/5/3 15:56
@Create by Author ： lileilei
====================================
"""
import time
from common.configuntil import Parse
from common.pictools import imagetovideo
from common.webdriverencapsulation import deriver_encapsulation
from common.unitil import *
from common.htmlreport import *
from common.unitil import getMobileInfo
from config import TestappActivity


class MonkeyClass(object):
    def __init__(self, dev, Testplatform, packagename, port, andriod, call_num,
                 testapkactivity,
                 store_activity=False, log=None):
        self.dev = dev
        self.Testplatform = Testplatform
        self.packagename = packagename
        self.port = port
        self.andriod = andriod
        self.call_num = call_num
        self.activity_dict = {}
        self.parseconfig = Parse(os.path.join(os.path.join(os.getcwd(), 'file'), 'config.yaml'))
        self.base = os.path.join(os.getcwd(), "testreport")
        self.call_num_path = os.path.join(self.base, self.call_num)
        if os.path.exists(self.call_num_path) is False:
            os.mkdir(self.call_num_path)
        self.runtime = self.parseconfig.get_run_time()
        self.isvideo = self.parseconfig.vido()
        self.path = os.path.join(self.call_num_path, self.dev)
        self.store_activity = store_activity
        self.activity = testapkactivity
        self.LOG = log

    def run(self):
        self.LOG.info("{}设备Monkey开始执行".format(self.dev))
        platform_version = getversion(self.dev)
        starttime = time.time()
        self.LOG.info("开始时间{}".format(str(starttime)))
        waittime = self.parseconfig.get_find_element_wait()
        if os.path.exists(self.path) is False:
            os.makedirs(self.path)
        deriverone = deriver_encapsulation(self.port, self.Testplatform, platform_version, self.dev
                                           , self.packagename, self.activity)
        allevent = self.parseconfig.getmonkeyConfig()
        self.LOG.info("支持事件{}".format(str(allevent.keys())))
        autologin = self.parseconfig.auto_loggin()
        run_is = self.checkout(allevent)

        get_find_element_timeout = self.parseconfig.get_find_element_timeout()
        if run_is is False:
            self.LOG.info("事件的比例不能满足100%要求，上限是100%的比例")
            return
        if autologin:
            self.LOG.info("开始执行登陆")
            self.login(deriverone, get_find_element_timeout)
        if self.andriod is False:
            allevent.delete('HOME_KEY_RATIO')
        title_X = 80
        title_Y = 80
        page = deriverone.get_wiow_size()
        width_wind = page['width']
        heigth_wind = page['height']
        canclick_width = width_wind - title_X
        canclick_heigth = heigth_wind - title_Y
        path = os.path.join(self.call_num_path, self.dev)
        if os.path.exists(path) is False:
            os.makedirs(path)
        time.sleep(2)
        self.LOG.info("任务执行需要执行：{} 分钟".format(str(self.runtime)))
        while True:
            '''
            每次事件出发 都执行下判断是否待测apk
            '''
            if checkPackeExit(self.dev, self.packagename, self.andriod) is False:
                deriverone.launch_app()
                time.sleep(10)
            endtime = time.time()
            if (endtime - starttime) > self.runtime * 60:
                self.LOG.info("任务运行{}时间，即将结束".format(str(self.runtime)))
                break
            x = random.randint(title_X, canclick_width)
            y = random.randint(title_Y, canclick_heigth)
            event = self.randoEvent(allevent)
            self.LOG.info("执行随机事件：%s" % str(event))
            if self.andriod:
                activity = deriverone.current_activity()
                self.activity_dict_update(event, activity, True)
            else:
                self.activity_dict_update(event, "", False)
            endx = random.randint(title_X, canclick_width)
            endy = random.randint(title_Y, canclick_heigth)
            if event == "SWIPE_RATIO":
                deriverone.take_screen(path)
                deriverone.swpape(x, y, endx, endy)
            elif event == "CLICK_RATIO":
                deriverone.take_screen(path)
                deriverone.click(x, y)

            elif event == 'RESTART_APP_RATIO':
                deriverone.take_screen(path)
                deriverone.close()
                deriverone.launch_app()

            elif event == 'LONG_PRESS_RATIO':
                deriverone.take_screen(path)
                deriverone.longcick(x, y)

            elif event == 'HOME_KEY_RATIO':
                deriverone.take_screen(path)
                perform_home(self.dev)
                deriverone.launch_app()

            elif event == 'BACK_KEY_RATIO':
                deriverone.take_screen(path)
                perform_back(self.dev)
                deriverone.take_screen(path)
            elif event == 'DOUBLE_TAP_RATIO':
                deriverone.take_screen(path)
                deriverone.doubletap(x, y)
            elif event == 'PINCH_RATIO':
                deriverone.take_screen(path)
                deriverone.pinch(x, y, endx, endy, False, heigth_wind, self.andriod)
            elif event == 'UNPINCH_RATIO':
                deriverone.take_screen(path)
                deriverone.pinch(x, y, endx, endy, True, heigth_wind, self.andriod)

            elif event == 'DRAG_RATIO':
                deriverone.take_screen(path)
                deriverone.draginde(x, y, endx, endy, self.andriod)
            elif event == 'AUTO_SOUND':
                deriverone.take_screen(path)
                perform_audio(self.dev)
            elif event == 'RELOVE_SCREEN':
                deriverone.take_screen(path)
                retonescreen(self.dev)
            time.sleep(int(waittime))
        self.LOG.info(self.activity_dict.__str__())

    def activity_dict_update(self, events: str, activity: str, android):
        if android is False:
            if events in self.activity_dict.keys():
                self.activity_dict[events] = self.activity_dict[events] + 1
            else:
                self.activity_dict[events] = 1
        else:
            if activity in self.activity_dict.keys():
                reslut = self.activity_dict[activity]
                if events in reslut.keys():
                    self.activity_dict[activity][events] = self.activity_dict[activity][events] + 1
                    return
                else:
                    self.activity_dict[activity][events] = 1
                    return
            self.activity_dict[activity] = {events: 1}
            return

    def login(self, deriver, get_find_element_timeout):
        '''
        执行登陆操作
        '''
        login = self.parseconfig.opearlogin()
        for item in login:
            element = deriver.find_ele('xpath', item['XPATH'], get_find_element_timeout)
            if item['ACTION'] == "input":
                element.clear()
                element.send_keys(item['VALUE'])
            elif item['ACTION'] == 'click':
                element.click()
            time.sleep(self.parseconfig.get_find_element_wait())

    def checkout(self, allevent: dict) -> bool:
        '''
        校验事件比例是否满足 ，暂定和大于100不行
        '''
        all_event = 0
        for value in allevent.values():
            all_event += int(value)
        if all_event > 100:
            return False
        else:
            return True

    def randoEvent(self, allevent: dict) -> str:
        '''
        随机产生事件，按照配置的比例去执行
        '''
        reslut = random.choices([key for key in allevent.keys()], weights=[value for value in allevent.values()], k=1)[
            0]
        return reslut

    def makereport(self):
        '''
        产生测试报告
        '''
        model, version, newKernel, serialno, brand, sdk, rom, rom_verison = getMobileInfo(self.dev)
        self.reslut = ""
        run_count = 0
        for key, value in self.activity_dict.items():
            self.reslut += "<p>activity {}".format(key)
            for keyevent, valueevent in value.items():
                run_count += valueevent
                self.reslut += " 事件：{} 操作：{} 次 ".format(str(keyevent), str(valueevent))
            self.reslut += "</p>"
        titles = title("基于Appium Monkey测试")
        conect = '''<div class="row " style="margin:60px">
                <div style='    margin-top: 5%;' >
                 <table class="table table-hover table-condensed table-bordered" style="word-wrap:break-word;">
            <tr > <td><strong>设备</strong></td><td>{}</td></tr>
        <td><strong>厂商</strong></td><td>{}</td></tr>
         
           <tr > <td><strong>系统版本</strong></td><td>{}</td></tr>
           <tr > <td><strong>测试apk</strong></td><td>{}</td></tr>
           <tr > <td><strong>启动activty：</strong></td><td>{}</td></tr>
           <tr >  <td><strong>测试时间：</strong></td><td>{}</td></tr>
            <tr >  <td><strong>一共操作：</strong></td><td>{} 次</td></tr>
            <tr >  <td><strong>事件详情：</strong></td><td>{}</td></tr>
                '''.format(self.dev, brand, rom,
                           self.packagename, TestappActivity, self.runtime, str(run_count), self.reslut)
        reslut = titles + conect
        end = '        </table></div></div></div>'
        reslut += end
        file = self.reportfile()
        with open(file, 'a+', encoding='utf-8') as f:
            f.write(reslut)
        if self.isvideo:
            self.video()

    def reportfile(self):
        self.repost_html = os.path.join(self.call_num_path, self.dev + ".html")
        return self.repost_html

    def video(self):
        for item in os.listdir(self.path):
            if os.path.isdir(item):
                path = os.path.join(self.path, item)
                runitem = os.path.join(self.call_num_path, item + "_crash.mp4")
                imagetovideo(path, runitem)
        run = os.path.join(self.call_num_path, self.dev + "_all.mp4")
        imagetovideo(self.path, run)
