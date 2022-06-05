"""
@file: reportsuit.py 
@time: 2018/5/7 15:49 
"""
from common import BSTestRunner
import unittest, time, os
from common.log import LOG
from common.makecase import makecasefile


def report(casepath):
    makecasefile(casename='ui', desc='自动化测试平台自动生成', funtionname='test_ui')
    test_suit = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(casepath, pattern='*test.py', top_level_dir=None)
    for test in discover:
        for test_case in test:
            test_suit.addTest(test_case)
    now = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))
    path = os.getcwd()
    reportpath = os.path.join(path, "testreport")
    report_dir = os.path.join(reportpath, "%s.html" % now)
    LOG.info('测试报告路径为：%s' % report_dir)
    re_open = open(report_dir, 'wb')
    runner = BSTestRunner.BSTestRunner(stream=re_open, title=u'自动化测试平台自动生成', description=u'自动化测试结果')
    n = runner.run(test_suit)
    success = n.success_count
    faill = n.failure_count
    error = n.error_count
    return error, faill, success, report_dir
