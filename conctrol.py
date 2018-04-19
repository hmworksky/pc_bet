# coding:utf-8
import unittest
import HTMLTestRunner
import sys
sys.path.append("\test_case")
from test_case import youdao


testunit = unittest.TestSuite()
testunit.addTest(unittest.makeSuite(baidu.BaiduTest))
testunit.addTest(unittest.makeSuite(youdao.Caipiao))
filename = "D:\\SOFTWARE\\study\\auto\\selenium\\test.html"
fp = file(filename,'wb')
runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title=u'多个测试集',description=u'执行情况：')
runner.run(testunit)


