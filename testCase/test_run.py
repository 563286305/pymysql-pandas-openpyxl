# -*- coding: utf-8 -*-
'''
Created on 2018.08.08
@author: wuyou
'''

import os
import time
import allure
import pytest
from lib.calculate2 import caculate2
from lib.querySQL import querySQL
ca = caculate2()
sql = querySQL()

#class get_date():
#     def __init__(self,type):
#         # comlist5 = ca.compareDate5(type)
#         # comlist3 = ca.compareDate5(type)
#         # comlist2 = ca.compareDate5(type)
#         # comlist5 = ca.compareDate5(type)
#         (comlist5,comlist3,comlist2,comlist1) = ca.compareDate(type)
#         fundcode5list = [];fundcode3list = [];fundcode2list = [];fundcode1list = []
#         for i in comlist5:
#             for key in i:
#                 fundcode5list.append(key)
#         for i in comlist3:
#             for key in i:
#                 fundcode3list.append(key)
#         for i in comlist2:
#             for key in i:
#                 fundcode2list.append(key)
#         for i in comlist1:
#             for key in i:
#                 fundcode1list.append(key)
#         self.comlist5 = comlist5
#         self.comlist3 = comlist3
#         self.comlist2 = comlist2
#         self.comlist1 = comlist1
#         self.fundcode5list = fundcode5list
#         self.fundcode3list = fundcode3list
#         self.fundcode2list = fundcode2list
#         self.fundcode1list = fundcode1list
#
# @pytest.fixture(scope='module')
# def getFundRate(type):
#     return get_date(type)

class Test_fund():
#     #######################################  混合型  ##########################################
#     # 混合型 + 5年定投
#     @allure.feature('混合型基金')
#     @allure.severity("critical")
#     @allure.story("五年定投")
#     @pytest.mark.parametrize("fund5dict",ca.compareDate("混合型",5),ids=ca.getCodefund("混合型",5))
#     #@pytest.mark.parametrize("fund5dict",getFundRate("混合型").comlist5,ids=getFundRate("混合型").fundcode5list)
#     def test_hh5_case(self,fund5dict):
#         for key in fund5dict:
#             fundcode = key
#             calresult = fund5dict[key][0]
#             exceptresult = fund5dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
#     # 混合型 + 3年定投
#     @allure.feature('混合型基金')
#     @allure.severity("critical")
#     @allure.story("三年定投")
#     @pytest.mark.parametrize("fund3dict",ca.compareDate("混合型",3),ids=ca.getCodefund("混合型",3))
#     def test_hh3_case(self,fund3dict):
#         for key in fund3dict:
#             fundcode = key
#             calresult = fund3dict[key][0]
#             exceptresult = fund3dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#     # 混合型 + 2年定投
#     @allure.feature('混合型基金')
#     @allure.severity("critical")
#     @allure.story("两年定投")
#     @pytest.mark.parametrize("fund2dict",ca.compareDate("混合型",2),ids=ca.getCodefund("混合型",2))
#     def test_hh2_case(self,fund2dict):
#         for key in fund2dict:
#             fundcode = key
#             calresult = fund2dict[key][0]
#             exceptresult = fund2dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#     # 混合型 + 1年定投
#     @allure.feature('混合型基金')
#     @allure.severity("critical")
#     @allure.story("一年定投")
#     @pytest.mark.parametrize("fund1dict",ca.compareDate("混合型",1),ids=ca.getCodefund("混合型",1))
#     def test_hh1_case(self,fund1dict):
#         for key in fund1dict:
#             fundcode = key
#             calresult = fund1dict[key][0]
#             exceptresult = fund1dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
#     #######################################  股票型  ##########################################
#     # 股票型 + 5年定投
#     @allure.feature('股票型基金')
#     @allure.severity("critical")
#     @allure.story("五年定投")
#     @pytest.mark.parametrize("fund5dict",ca.compareDate("股票型",5),ids=ca.getCodefund("股票型",5))
#     def test_gp5_case(self,fund5dict):
#         for key in fund5dict:
#             fundcode = key
#             calresult = fund5dict[key][0]
#             exceptresult = fund5dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
#     # 股票型 + 3年定投
#     @allure.feature('股票型基金')
#     @allure.severity("critical")
#     @allure.story("三年定投")
#     @pytest.mark.parametrize("fund3dict",ca.compareDate("股票型",3),ids=ca.getCodefund("股票型",3))
#     def test_gp3_case(self,fund3dict):
#         for key in fund3dict:
#             fundcode = key
#             calresult = fund3dict[key][0]
#             exceptresult = fund3dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
#     # 股票型 + 2年定投
#     @allure.feature('股票型基金')
#     @allure.severity("critical")
#     @allure.story("两年定投")
#     @pytest.mark.parametrize("fund2dict",ca.compareDate("股票型",2),ids=ca.getCodefund("股票型",2))
#     def test_gp2_case(self,fund2dict):
#         for key in fund2dict:
#             fundcode = key
#             calresult = fund2dict[key][0]
#             exceptresult = fund2dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
#     # 股票型 + 1年定投
#     @allure.feature('股票型基金')
#     @allure.severity("critical")
#     @allure.story("一年定投")
#     @pytest.mark.parametrize("fund1dict",ca.compareDate("股票型",1),ids=ca.getCodefund("股票型",1))
#     def test_gp1_case(self,fund1dict):
#         for key in fund1dict:
#             fundcode = key
#             calresult = fund1dict[key][0]
#             exceptresult = fund1dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
#
#  ########################################   债券型   ########################################
#     # 债券型 + 5年定投
#     @allure.feature('债券型基金')
#     @allure.severity("critical")
#     @allure.story("五年定投")
#     @pytest.mark.parametrize("fund5dict",ca.compareDate("债券型",5),ids=ca.getCodefund("债券型",5))
#     def test_zq5_case(self,fund5dict):
#         for key in fund5dict:
#             fundcode = key
#             calresult = fund5dict[key][0]
#             exceptresult = fund5dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
#     # 债券型 + 3年定投
#     @allure.feature('债券型基金')
#     @allure.severity("critical")
#     @allure.story("三年定投")
#     @pytest.mark.parametrize("fund3dict",ca.compareDate("债券型",3),ids=ca.getCodefund("债券型",3))
#     def test_zq3_case(self,fund3dict):
#         for key in fund3dict:
#             fundcode = key
#             calresult = fund3dict[key][0]
#             exceptresult = fund3dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
#     # 债券型 + 2年定投
#     @allure.feature('债券型基金')
#     @allure.severity("critical")
#     @allure.story("两年定投")
#     @pytest.mark.parametrize("fund2dict",ca.compareDate("债券型",2),ids=ca.getCodefund("债券型",2))
#     def test_zq2_case(self,fund2dict):
#         for key in fund2dict:
#             fundcode = key
#             calresult = fund2dict[key][0]
#             exceptresult = fund2dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
#     # 债券型 + 1年定投
#     @allure.feature('债券型基金')
#     @allure.severity("critical")
#     @allure.story("一年定投")
#     @pytest.mark.parametrize("fund1dict",ca.compareDate("债券型",1),ids=ca.getCodefund("债券型",1))
#     def test_zq1_case(self,fund1dict):
#         for key in fund1dict:
#             fundcode = key
#             calresult = fund1dict[key][0]
#             exceptresult = fund1dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
# ############################################  指数型  ##########################################
#     # 指数型 + 5年定投
#     @allure.feature('指数型基金')
#     @allure.severity("critical")
#     @allure.story("五年定投")
#     @pytest.mark.parametrize("fund5dict",ca.compareDate("指数型",5),ids=ca.getCodefund("指数型",5))
#     def test_zs5_case(self,fund5dict):
#         for key in fund5dict:
#             fundcode = key
#             calresult = fund5dict[key][0]
#             exceptresult = fund5dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
#     # 指数型 + 3年定投
#     @allure.feature('指数型基金')
#     @allure.severity("critical")
#     @allure.story("三年定投")
#     @pytest.mark.parametrize("fund3dict",ca.compareDate("指数型",3),ids=ca.getCodefund("指数型",3))
#     def test_zs3_case(self,fund3dict):
#         for key in fund3dict:
#             fundcode = key
#             calresult = fund3dict[key][0]
#             exceptresult = fund3dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
#     # 指数型 + 2年定投
#     @allure.feature('指数型基金')
#     @allure.severity("critical")
#     @allure.story("两年定投")
#     @pytest.mark.parametrize("fund2dict",ca.compareDate("指数型",2),ids=ca.getCodefund("指数型",2))
#     def test_zs2_case(self,fund2dict):
#         for key in fund2dict:
#             fundcode = key
#             calresult = fund2dict[key][0]
#             exceptresult = fund2dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
#     # 指数型 + 1年定投
#     @allure.feature('指数型基金')
#     @allure.severity("critical")
#     @allure.story("一年定投")
#     @pytest.mark.parametrize("fund1dict",ca.compareDate("指数型",1),ids=ca.getCodefund("指数型",1))
#     def test_zs1_case(self,fund1dict):
#         for key in fund1dict:
#             fundcode = key
#             calresult = fund1dict[key][0]
#             exceptresult = fund1dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
# ########################################   QDII   ###########################################
#     # QDII + 5年定投
#     @allure.feature('QDII基金')
#     @allure.severity("critical")
#     @allure.story("五年定投")
#     @pytest.mark.parametrize("fund5dict",ca.compareDate("QDII",5),ids=ca.getCodefund("QDII",5))
#     def test_QDII5_case(self,fund5dict):
#         for key in fund5dict:
#             fundcode = key
#             calresult = fund5dict[key][0]
#             exceptresult = fund5dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
#     # QDII + 3年定投
#     @allure.feature('QDII基金')
#     @allure.severity("critical")
#     @allure.story("三年定投")
#     @pytest.mark.parametrize("fund3dict",ca.compareDate("QDII",3),ids=ca.getCodefund("QDII",3))
#     def test_QDII3_case(self,fund3dict):
#         for key in fund3dict:
#             fundcode = key
#             calresult = fund3dict[key][0]
#             exceptresult = fund3dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
#     # QDII + 2年定投
#     @allure.feature('QDII基金')
#     @allure.severity("critical")
#     @allure.story("两年定投")
#     @pytest.mark.parametrize("fund2dict",ca.compareDate("QDII",2),ids=ca.getCodefund("QDII",2))
#     def test_QDII2_case(self,fund2dict):
#         for key in fund2dict:
#             fundcode = key
#             calresult = fund2dict[key][0]
#             exceptresult = fund2dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
#     # QDII + 1年定投
#     @allure.feature('QDII基金')
#     @allure.severity("critical")
#     @allure.story("一年定投")
#     @pytest.mark.parametrize("fund1dict",ca.compareDate("QDII",1),ids=ca.getCodefund("QDII",1))
#     def test_QDII1_case(self,fund1dict):
#         for key in fund1dict:
#             fundcode = key
#             calresult = fund1dict[key][0]
#             exceptresult = fund1dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02

 #####################################  货币型  ##############################################
    # 货币型 + 5年定投
    @allure.feature('货币型基金')
    @allure.severity("critical")
    @allure.story("五年定投")
    @pytest.mark.parametrize("fund5dict",ca.compareDate("货币型",5),ids=ca.getCodefund("货币型",5))
    def test_hb5_case(self,fund5dict):
        for key in fund5dict:
            fundcode = key
            calresult = fund5dict[key][0]
            exceptresult = fund5dict[key][1]
        with pytest.allure.step("测试步骤： 结果校验"):
             allure.attach('fundcode', str(fundcode))
             allure.attach('计算结果', str(calresult))
             allure.attach('期望结果', str(exceptresult))
             assert abs(calresult-exceptresult)<0.02
 #    # 货币型 + 3年定投
 #    @allure.feature('货币型基金')
 #    @allure.severity("critical")
 #    @allure.story("三年定投")
 #    @pytest.mark.parametrize("fund3dict",ca.compareDate("货币型",3),ids=ca.getCodefund("货币型",3))
 #    def test_hb3_case(self,fund3dict):
 #        for key in fund3dict:
 #            fundcode = key
 #            calresult = fund3dict[key][0]
 #            exceptresult = fund3dict[key][1]
 #        with pytest.allure.step("测试步骤： 结果校验"):
 #             allure.attach('fundcode', str(fundcode))
 #             allure.attach('计算结果', str(calresult))
 #             allure.attach('期望结果', str(exceptresult))
 #             assert abs(calresult-exceptresult)<0.02
 #    # 货币型 + 2年定投
 #    @allure.feature('货币型基金')
 #    @allure.severity("critical")
 #    @allure.story("两年定投")
 #    @pytest.mark.parametrize("fund2dict",ca.compareDate("货币型",2),ids=ca.getCodefund("货币型",2))
 #    def test_hb2_case(self,fund2dict):
 #        for key in fund2dict:
 #            fundcode = key
 #            calresult = fund2dict[key][0]
 #            exceptresult = fund2dict[key][1]
 #        with pytest.allure.step("测试步骤： 结果校验"):
 #             allure.attach('fundcode', str(fundcode))
 #             allure.attach('计算结果', str(calresult))
 #             allure.attach('期望结果', str(exceptresult))
 #             assert abs(calresult-exceptresult)<0.02
 #    # 货币型 + 1年定投
 #    @allure.feature('货币型基金')
 #    @allure.severity("critical")
 #    @allure.story("一年定投")
 #    @pytest.mark.parametrize("fund1dict",ca.compareDate("货币型",1),ids=ca.getCodefund("货币型",1))
 #    def test_hb1_case(self,fund1dict):
 #        for key in fund1dict:
 #            fundcode = key
 #            calresult = fund1dict[key][0]
 #            exceptresult = fund1dict[key][1]
 #        with pytest.allure.step("测试步骤： 结果校验"):
 #             allure.attach('fundcode', str(fundcode))
 #             allure.attach('计算结果', str(calresult))
 #             allure.attach('期望结果', str(exceptresult))
 #             assert abs(calresult-exceptresult)<0.02

#  ##########################################  fof  #############################################
#     # fof + 5年定投
#     @allure.feature('fof基金')
#     @allure.severity("critical")
#     @allure.story("五年定投")
#     @pytest.mark.parametrize("fund5dict",ca.compareDate("fof",5),ids=ca.getCodefund("fof",5))
#     def test_fof5_case(self,fund5dict):
#         for key in fund5dict:
#             fundcode = key
#             calresult = fund5dict[key][0]
#             exceptresult = fund5dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#     # fof + 3年定投
#     @allure.feature('fof基金')
#     @allure.severity("critical")
#     @allure.story("三年定投")
#     @pytest.mark.parametrize("fund3dict",ca.compareDate("fof",3),ids=ca.getCodefund("fof",3))
#     def test_fof3_case(self,fund3dict):
#         for key in fund3dict:
#             fundcode = key
#             calresult = fund3dict[key][0]
#             exceptresult = fund3dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
#     # fof + 2年定投
#     @allure.feature('fof基金')
#     @allure.severity("critical")
#     @allure.story("两年定投")
#     @pytest.mark.parametrize("fund2dict",ca.compareDate("fof",2),ids=ca.getCodefund("fof",2))
#     def test_fof2_case(self,fund2dict):
#         for key in fund2dict:
#             fundcode = key
#             calresult = fund2dict[key][0]
#             exceptresult = fund2dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02
#
#     #  fof + 1 年定投
#     @allure.feature('fof基金')
#     @allure.severity("critical")
#     @allure.story("一年定投")
#     @pytest.mark.parametrize("fund1dict",ca.compareDate("fof",1),ids=ca.getCodefund("fof",1))
#     def test_fof1_case(self,fund1dict):
#         for key in fund1dict:
#             fundcode = key
#             calresult = fund1dict[key][0]
#             exceptresult = fund1dict[key][1]
#         with pytest.allure.step("测试步骤： 结果校验"):
#              allure.attach('fundcode', str(fundcode))
#              allure.attach('计算结果', str(calresult))
#              allure.attach('期望结果', str(exceptresult))
#              assert abs(calresult-exceptresult)<0.02


if __name__ == '__main__':
    pytest.main()
