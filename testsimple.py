# -*- coding: utf-8 -*-
"""
时间: 2019/9/27 16:22

作者: shichao

更改记录:

重要说明:参考连接 https://blog.csdn.net/luanpeng825485697/article/details/79459771
"""

import unittest

import fab

class testFab(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("这里是本类下所有具体测试用例执行前的准备工作，用于为全部的用例构建测试环境")

    @classmethod
    def tearDownClass(cls):
        print("这里是本类下所有具体测试用例执行后的清理工作，用于清理全部的用例结束后的环境")

    def setUp(self):
        print("这里是一个具体的测试用例执行前的准备工作，该方法用于为每一个测试用例构建测试环境")

    def tearDown(self):
        print("这里是一个具体的测试用例执行后的清理工作，该方法用于清理每一个测试用例结束后的环境")

    # 这是一个具体的测试用例
    # @unittest.skip('跳过')
    def test_fab(self):
        self.assertEquals(1,1)
        self.assertNotEquals(1, 2, '错误')

    # 这是另一个具体的测试用例
    def test_fab2(self):
        self.assertEquals(1, 1)
        self.skipTest('从这里跳过')
        self.assertNotEquals(1, 2, '错误')
        self.assertEquals(1, 2)


if __name__ == '__main__':
    # unittest.main(verbosity=2)
    suite = unittest.TestSuite()

    suite.addTest(testFab('test_fab'))
    suite.addTests([testFab('test_fab'),testFab('test_fab2')])
    suite.addTests(unittest.load_tests(unittest.TestLoader().loadTestsFromTestCase(testFab)))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

    # 将测试结果输出到测试报告中
    # with open('UnittestTextReport.txt', 'a') as f:
    #     runner = unittest.TextTestRunner(stream=f, verbosity=2)
    #     runner.run(suite)

    # 将测试结果输出到测试报告html中
    # https://github.com/626626cdllp/Test/blob/master/python-unittest/HTMLTestRunner.py
    # with open('HTMLReport.html', 'w') as f:
    #     runner = HTMLTestRunner(stream=f,
    #                             title='MathFunc Test Report',
    #                             description='generated by HTMLTestRunner.',
    #                             verbosity=2
    #                             )
    #     runner.run(suite)

