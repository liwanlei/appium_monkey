""" 
@author: lileilei
@file: run.py 
@time: 2018/5/6 17:32 
"""
import os
from common.log import LOG
from case.uimonkey import MonkeyClass
from common.execlog import run_adb_log
import multiprocessing
from common.Makecasenum import call_num
import click
from common.apktools import get_apkname, get_apk_lanchactivity

basepth = os.getcwd()


@click.group()
def cli():
    pass


@click.command()
def monkey():
    LOG.name = "基于Appium Monkey随机测试"
    testapk = get_apkname("/Users/lileilei/Desktop/testplan/pc_clicent_new/installapk/autohome.apk")
    testapklanchactivity = get_apk_lanchactivity(
        "/Users/lileilei/Desktop/testplan/pc_clicent_new/installapk/autohome.apk")
    path = os.path.join(os.path.join(os.getcwd(), 'testlog'), call_num)
    if os.path.exists(path) is False:
        os.mkdir(path)
    runlog = multiprocessing.Pool()
    runlog.apply_async(run_adb_log, ("RF8MC0GHRHR", path))
    monkey = MonkeyClass(dev="RF8MC0GHRHR", Testplatform='Android', port=4724,
                         andriod=True, packagename=testapk, call_num=call_num,
                         testapkactivity=testapklanchactivity, log=LOG
                         )
    monkey.run()
    monkey.makereport()
    runlog.close()
    runlog.terminate()


cli.add_command(monkey)

if __name__ == "__main__":
    cli()
