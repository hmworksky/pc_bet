# coding:utf-8
import unittest
import baidu,youdao
import HTMLTestRunner
testunit = unittest.TestSuite()
testunit.addTest(unittest.makeSuite(baidu.BaiduTest))
testunit.addTest(unittest.makeSuite(youdao.Caipiao))
filename = "D:\\SOFTWARE\\study\\auto\\selenium\\test.html"
fp = file(filename,'wb')
runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title=u'多个测试集',description=u'执行情况：')
runner.run(testunit)


