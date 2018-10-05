# -*- coding: utf-8 -*-
'''
Created on 2018.08.01
@author: wuyou
'''
import datetime
import pytest
import pymysql
import pandas as pd
import itertools
import json
import copy
import re
import os
from lib.querySQL import querySQL
from dateutil import rrule
from lib.readWriteExcel import readWriteExcel
from lib.interface import interface
import time
from multiprocessing.dummy import  Pool as ThreadPool
sql = querySQL()
excel = readWriteExcel()
inf = interface()

#当前路径: \Real_Time_test\TestCase
casepath = os.path.dirname(__file__)
basepath = os.path.dirname(casepath)
config_excel = os.path.join(basepath + "\config\\","Configuration.xlsx")
config_sheet = 'env_config'
ratefile = os.path.join(casepath,"rates.txt")

class caculate2():
    def __init__(self):
        end = excel.get_excel_row_count(config_excel, config_sheet)
        configdict = excel.get_excel_name_value_dict(config_excel, config_sheet,'B','C','2',end)
        self.rate_url = configdict['rate_url']
        self.command_jl_hh = configdict['command_jl_hh']
        self.command_jl_gp = configdict['command_jl_gp']
        self.command_jl_zq = configdict['command_jl_zq']
        self.command_jl_zs = configdict['command_jl_zs']
        self.command_jl_QDII = configdict['command_jl_QDII']
        self.command_jl_fof = configdict['command_jl_fof']
        self.command_jl_hb = configdict['command_jl_hb']
        self.command_app = configdict['command_app']
        self.check_hh = configdict['check_hh']
        self.check_gp = configdict['check_gp']
        self.check_zq = configdict['check_zq']
        self.check_zs = configdict['check_zs']
        self.check_QDII = configdict['check_QDII']
        self.check_fof = configdict['check_fof']
        self.check_hb = configdict['check_hb']

        self.dateList = ['2013-07-18','2013-08-19','2013-09-18','2013-10-18',\
                         '2013-11-18','2013-12-18','2014-01-20','2014-02-18',\
                         '2014-03-18','2014-04-18','2014-05-19','2014-06-18',\
                         '2014-07-18','2014-08-18','2014-09-18','2014-10-20',\
                         '2014-11-18','2014-12-18','2015-01-19','2015-02-25',\
                         '2015-03-18','2015-04-20','2015-05-18','2015-06-18',\
                         '2015-07-20','2015-08-18','2015-09-18','2015-10-19',\
                         '2015-11-18','2015-12-18','2016-01-18','2016-02-18',\
                         '2016-03-18','2016-04-18','2016-05-18','2016-06-20',\
                         '2016-07-18','2016-08-18','2016-09-19','2016-10-18',\
                         '2016-11-18','2016-12-19','2017-01-18','2017-02-20',\
                         '2017-03-20','2017-04-18','2017-05-18','2017-06-19',\
                         '2017-07-18','2017-08-18','2017-09-18','2017-10-18',\
                         '2017-11-20','2017-12-18','2018-01-18','2018-02-22',\
                         '2018-03-19','2018-04-18','2018-05-18','2018-06-19',\
                         '2018-07-18','2018-08-20','2018-09-18','2018-10-18',\
                         '2018-11-19','2018-12-18']
    #将list里所有值相加
    def list_sum(self,list1):
        num = 0
        for value in list1:
            value = float(value)
            num = num + value
        return num

    #获取月份差值,过滤出5年，3年，2年，1年定投的时间
    def dateFilter(self,d1,year):
        # d1 = datetime.date(year = 2016,month=8,day=19)
        # year =2
        d2 = self.get18Time()
        if d1.day>18:
            if d1.month==12:
                newmonth = 1
                newyear = d1.year+1
            else:
                newmonth = d1.month+1
                newyear = d1.year
            dtmp =datetime.date( year = newyear, month = newmonth, day = 18)
        else:
            dtmp =datetime.date( year = d1.year, month = d1.month, day = 18)

        # dtmp = datetime.date(2017, 8, 26)
        # d2 = datetime.date(2018, 8, 10)
        # print(dtmp)
        # print(d2)
        months = rrule.rrule(rrule.MONTHLY,dtstart=dtmp,until=d2).count()
        # print("months:  "+str(months))
        if year==5:
            if months>=60:
                return(d1)
        elif year==3:
            if months>=36:
                return(d1)
        elif year==2:
            if months>=24:
                return(d1)
        elif year==1:
            if months>=12:
                return(d1)
        else:
            print('ERROR')

    def get18Time(self):
        #获取当月最近的18号，也就是开始时间
        now = datetime.datetime.now()
        if now.day>18:
            startday = datetime.date(year= now.year,month=now.month,day=18)
        else:
            if now.month == 1:
                yearnew = now.year-1
                monthnew = 12
            else:
                monthnew = now.month - 1
                yearnew = now.year
            startday = datetime.date(year= yearnew,month=monthnew,day=18)
        return(startday)

    #根据当前时间，和定投年限，获取到所有月份list（每月18号）
    def getmonths(self,year):
        times = int(year)*12
        #查看当前时间是否大于18，如果不大于18，取上月18号，作为开始时间。（注意考虑1月）

        now= datetime.datetime.now()
        # print("当前日期：    "+str(now))
        day = int(now.day)
        if day>=18:
            startday = datetime.date(year= now.year,month=now.month,day=18)
        else:
            if now.month == 1:
                yearnew = now.year-1
                monthnew = 12
            else:
                monthnew = now.month - 1
                yearnew = now.year
            startday = datetime.date(year= yearnew,month=monthnew,day=18)
        # print("获取收益率的起始日期："+str(startday))

        #以startday作为开始时间，向前取times个时间点，
        if str(startday) in self.dateList:
            index = self.dateList.index(str(startday))
            # print('起始日期所在的位置: '+str(index))
            monthlist = self.dateList[index+1-times:index+1]
            # print("将要获取收益率的所有日期：    "+str(monthlist))
        # for month in monthlist:
        #     datetime.datetime.strptime(month,"%Y-%m-%d")
        # print(monthlist)
        return(monthlist)

    def cal_realrate(self,ratelist):
        Nlist = []
        for i in ratelist:
            if i==ratelist[0]:
                N=1
            else:
                N=N*(1+i/10000)
            Nlist.append(N)
        return(Nlist)
    # def compareYearMonth(self,d1,d2):
    #     if d1.year == d2.year and d1.month==d2.month:
    #         return(d1)

    def getFrame(self,type):
        '''
        fnd_gen_info库和ana_fnd_nav_calc库 组合查询
        fund_code       ---基金code
        fundsname
        inner_code      ---inner code，表示基金唯一性
        estab_date      ---基金成立时间
        tradedate_min      ---最早交易时间
        tradedate_max     ---最近一次的交易时间
        FAC_UNIT_NET_MAX     ---最新的复权净值
        '''

        (server_jl,con_jl,serverport1) = sql.connectdb_jl()
        (server_app,con_app,serverport2) = sql.connectdb_app()
        #第一次过滤条件
        if type == "混合型":
            command_jl = self.command_jl_hh
            command_result = self.check_hh
        elif type=="股票型":
            command_jl = self.command_jl_gp
            command_result= self.check_gp
        elif type=="债券型":
            command_jl = self.command_jl_zq
            command_result= self.check_zq
        elif type=="指数型":
            command_jl = self.command_jl_zs
            command_result= self.check_zs
        elif type=="QDII":
            command_jl = self.command_jl_QDII
            command_result= self.check_QDII
        elif type=="fof":
            command_jl = self.command_jl_fof
            command_result= self.check_fof
        elif type=="货币型":
            command_jl = self.command_jl_hb
            command_result= self.check_hb

        #金牛过滤条件
        command_app=self.command_app
        #分块读取巨灵库里的第一次过滤内容
        d_jl_tmp=pd.read_sql(command_jl,con=con_jl,chunksize=10000)

        d_jl_list = []
        for d_jl_one in d_jl_tmp:
            d_jl_list.append(d_jl_one)
        d_jl = pd.concat(d_jl_list, ignore_index=True)
        print(d_jl.shape)
        #读取金牛库中的fund_code
        d_jn = pd.read_sql(command_app,con=con_app)
        print("d_jn: "+str(d_jn.shape))
        d_check = pd.read_sql(command_result,con=con_app)

        #基金和金牛过滤后的所有基金
        d_fundframe = pd.merge(d_jl, d_jn, how='inner', on=['fund_code'])
        print("和金牛过滤后的基金数: "+str(d_fundframe.shape))
        months5 = self.getmonths(5)
        months3 = self.getmonths(3)
        months2 = self.getmonths(2)
        months1 = self.getmonths(1)
        print("months5"+str(months5))
        print("months3"+str(months3))
        print("months2"+str(months2))
        print("months1"+str(months1))
        if type=="货币型":
            fund_codelist = d_fundframe['fund_code'].drop_duplicates().tolist()
            realratelist= []
            for fund_code in fund_codelist:
                unitlist = d_fundframe[d_fundframe['fund_code']==fund_code]['tenthou_unit_incm'].tolist()
                realratelist = realratelist+(self.cal_realrate(unitlist))

            d_fundframe['realrates']=realratelist
            d_fundframetmp=d_fundframe.sort_values('enddate',ascending=False)
            d_fundframeall = d_fundframetmp.groupby(d_fundframetmp['fund_code']).head(1)
            print('kkkkkkkkkkkkkkkkkkkkkk')
            print(d_fundframeall[d_fundframeall['fund_code']=='161622'][['estab_date','fund_code']])

            #5年定投的所有基金的60个月的18号的收益率
            d_fundframe5 = d_fundframeall[d_fundframeall['estab_date'].isin(d_fundframeall['estab_date'].apply(self.dateFilter,args=(5,)).tolist())]
            d_fundframe3 = d_fundframeall[d_fundframeall['estab_date'].isin(d_fundframeall['estab_date'].apply(self.dateFilter,args=(3,)).tolist())]
            d_fundframe2 = d_fundframeall[d_fundframeall['estab_date'].isin(d_fundframeall['estab_date'].apply(self.dateFilter,args=(2,)).tolist())]
            d_fundframe1 = d_fundframeall[d_fundframeall['estab_date'].isin(d_fundframeall['estab_date'].apply(self.dateFilter,args=(1,)).tolist())]


            rateFrame5 = d_fundframe[d_fundframe['enddate'].isin(months5)& d_fundframe['fund_code'].isin(d_fundframe5['fund_code'].tolist())]
            print(rateFrame5.shape)
            rateFrame3 = d_fundframe[d_fundframe['enddate'].isin(months3)& d_fundframe['fund_code'].isin(d_fundframe3['fund_code'].tolist())]
            print(rateFrame3.shape)
            rateFrame2 = d_fundframe[d_fundframe['enddate'].isin(months2)& d_fundframe['fund_code'].isin(d_fundframe2['fund_code'].tolist())]
            print(rateFrame2.shape)
            rateFrame1 = d_fundframe[d_fundframe['enddate'].isin(months1)& d_fundframe['fund_code'].isin(d_fundframe1['fund_code'].tolist())]
            print(rateFrame1.shape)

            #rateFrame1 = d_fundframe[d_fundframe['enddate'].isin(months1) &d_fundframe['estab_date'].isin(d_fundframe['estab_date'].apply(self.dateFilter,args=(1,)).tolist())]

        else:
            #过滤掉不满1年的基金，取出5,3,2,1定投的所有基金，
            # column有 fund_code，fundsname，inner_code，estab_date(基金成立时间)
            # tradedate_min(最早交易时间)，tradedate_max(最晚交易时间)
            # fac_unit_net_max(最新的复权净值)
            # d_fundframe5_tmp = d_fundframe[d_fundframe['tradedate_min'].isin(d_fundframe['tradedate_min'].apply(self.dateFilter,args=(5,)).tolist())]
            # print(d_fundframe5_tmp.shape[0])
            # d_fundframe5= d_fundframe5_tmp[d_fundframe5_tmp['estab_date'].isin(d_fundframe5_tmp['estab_date'].apply(self.dateFilter,args=(5,)).tolist())]
            # print(d_fundframe5.shape[0])

            d_fundframe5 = d_fundframe[d_fundframe['estab_date'].isin(d_fundframe['estab_date'].apply(self.dateFilter,args=(5,)).tolist())]

            print(d_fundframe5.shape)

            # d_fundframe3_tmp = d_fundframe[d_fundframe['tradedate_min'].isin(d_fundframe['tradedate_min'].apply(self.dateFilter,args=(3,)).tolist())]
            # print(d_fundframe3_tmp.shape[0])
            # d_fundframe3 = d_fundframe3_tmp[d_fundframe3_tmp['estab_date'].isin(d_fundframe3_tmp['estab_date'].apply(self.dateFilter,args=(3,)).tolist())]
            d_fundframe3 = d_fundframe[d_fundframe['estab_date'].isin(d_fundframe['estab_date'].apply(self.dateFilter,args=(3,)).tolist())]
            print(d_fundframe3.shape[0])
            print(d_fundframe3.shape)

            # d_fundframe2_tmp = d_fundframe[d_fundframe['tradedate_min'].isin(d_fundframe['tradedate_min'].apply(self.dateFilter,args=(2,)).tolist())]
            # print(d_fundframe2_tmp.shape[0])
            # d_fundframe2 = d_fundframe2_tmp[d_fundframe2_tmp['estab_date'].isin(d_fundframe2_tmp['estab_date'].apply(self.dateFilter,args=(2,)).tolist())]
            d_fundframe2 = d_fundframe[d_fundframe['estab_date'].isin(d_fundframe['estab_date'].apply(self.dateFilter,args=(2,)).tolist())]
            print(d_fundframe2.shape[0])

            # print(d_fundframe2.shape)
            # d_fundframe1_tmp = d_fundframe[d_fundframe['tradedate_min'].isin(d_fundframe['tradedate_min'].apply(self.dateFilter,args=(1,)).tolist())]
            # print(d_fundframe1_tmp.shape[0])
            # d_fundframe1 = d_fundframe1_tmp[d_fundframe1_tmp['estab_date'].isin(d_fundframe1_tmp['estab_date'].apply(self.dateFilter,args=(1,)).tolist())]
            d_fundframe1 = d_fundframe[d_fundframe['estab_date'].isin(d_fundframe['estab_date'].apply(self.dateFilter,args=(1,)).tolist())]
            print(d_fundframe1.shape[0])
            print(d_fundframe1.shape)

            #取出所有满足条件基金的fundcode和innercode
            fundlist = d_fundframe1['fund_code'].tolist()
            inner_code = d_fundframe1['inner_code'].tolist()

            #所有满足条件的基金在特定月份的所有收益率 过滤条件
            command_rate="SELECT fund_code,inner_code,fac_unit_net,tradedate FROM ana_fnd_nav_calc WHERE inner_code \
            in " + str(tuple(inner_code)) + " and tradedate in " + str(tuple(self.dateList))

            rateFrame=pd.read_sql(command_rate,con=con_jl)



            #5年定投的所有基金的60个月的18号的收益率
            rateFrame5 = rateFrame[rateFrame['tradedate'].isin(months5)\
                        &rateFrame['inner_code'].isin(d_fundframe5['inner_code'].tolist())]
            print(rateFrame5.shape)

            rateFrame3 = rateFrame[rateFrame['tradedate'].isin(months3)\
                        &rateFrame['inner_code'].isin(d_fundframe3['inner_code'].tolist())]
            print(rateFrame3.shape)

            rateFrame2 = rateFrame[rateFrame['tradedate'].isin(months2)\
                        &rateFrame['inner_code'].isin(d_fundframe2['inner_code'].tolist())]
            print(rateFrame2.shape)

            rateFrame1 = rateFrame[rateFrame['tradedate'].isin(months1)\
                        &rateFrame['inner_code'].isin(d_fundframe1['inner_code'].tolist())]
            print(rateFrame1.shape)
        #
        server_jl.stop()
        server_app.stop()
        con_jl.close()
        con_app.close()
        return(d_fundframe5,d_fundframe3,d_fundframe2,d_fundframe1,rateFrame5,rateFrame3,rateFrame2,rateFrame1,d_check)

    def get_rates(self):
        f = open(ratefile,'r')
        rates = f.readlines()
        #读取下来的json字符串需要将单引号改成双引号，才能解析成功
        ratedict = json.loads(rates[0].replace("'",'"'))
        return(ratedict)

    def compareDate(self,type,year):
        # 公式： 最新一个复权净值 * [1/（(1+申购费率）*第一次定投复权净值）+ 1/（(1+申购费率）*第二次定投复权净值）+
        #      1/（(1+申购费率）*第三次定投复权净值）+ ....]/定投次数  - 1
        #
        starttime = time.time()
        (fund5,fund3,fund2,fund1,rate5,rate3,rate2,rate1,check) = self.getFrame(type)
        shoprateDict = self.get_rates()

        if type=='货币型':
            if year==5:
                fund_codelist = fund5['fund_code'].drop_duplicates().tolist()
                rate = rate5
                fund = fund5
                ratename = 'rate_five'
            elif year==3:
                fund_codelist = fund3['fund_code'].drop_duplicates().tolist()
                rate = rate3
                fund = fund3
                ratename = 'rate_three'
            elif year==2:
                fund_codelist = fund2['fund_code'].drop_duplicates().tolist()
                rate = rate2
                fund = fund2
                ratename = 'rate_two'
            elif year==1:
                fund_codelist = fund1['fund_code'].drop_duplicates().tolist()
                rate = rate1
                fund = fund1
                ratename = 'rate_one'
            listtmp = []
            checknum = float(check[ratename].dropna().shape[0])
            checkcodelist = check[check[ratename].isin(check[ratename].dropna().tolist())]['fund_code'].tolist()
            checkcodelist.sort()
            print('check fundcode list: '+str(checkcodelist))
            print('checknum:    '+str(checknum))
            fund_codelist.sort()
            calnum=len(fund_codelist)
            print('cal fundcode list:   '+str(fund_codelist))
            print('calnum:   '+str(calnum))
            tmpdict={}
            tmpdict['fundnum']=[calnum,checknum]
            listtmp.append(tmpdict)

            for code in  fund_codelist:
                tmpdict = {}
                print('fund_code:   '+str(code))
                shoprate = shoprateDict[code]
                print('申购费率：    '+str(shoprate))
                rates = rate[rate['fund_code']==code]['realrates'].dropna().tolist()
                print('所有真实净值rates: '+str(rates))
                print(len(rates))
                newestRate = float(fund[fund['fund_code']==code]['realrates'])
                print("最新复权净值：  "+str(newestRate))
                tmp = 0
                for key in rates:
                    tmp = tmp+1/(( 1+float(shoprate) )*float(key))
                    # print(tmp,float(shoprate),float(key))
                print("sum: "+str(tmp))
                finallrate = newestRate*tmp/len(rates) -1

                tmpdict[code]=[]
                tmpdict[code].append(finallrate)
                if not check[check['fund_code']==code][ratename].empty:
                    tmpdict[code].append(float(check[check['fund_code']==code][ratename]))
                else:
                    tmpdict[code].append('null')
                listtmp.append(tmpdict)
                print('finallrate'+str(year)+":  "+str(finallrate))
        else:
            if year==5:
                fund_codelist = fund5['fund_code'].drop_duplicates().tolist()
                rate = rate5
                fund = fund5
                ratename = 'rate_five'
            elif year==3:
                fund_codelist = fund3['fund_code'].drop_duplicates().tolist()
                rate = rate3
                fund = fund3
                ratename = 'rate_three'
            elif year==2:
                fund_codelist = fund2['fund_code'].drop_duplicates().tolist()
                rate = rate2
                fund = fund2
                ratename = 'rate_two'
            elif year==1:
                fund_codelist = fund1['fund_code'].drop_duplicates().tolist()
                rate = rate1
                fund = fund1
                ratename = 'rate_one'

            listtmp = []
            checknum = float(check[ratename].dropna().shape[0])
            checkcodelist = check[check[ratename].isin(check[ratename].dropna().tolist())]['fund_code'].tolist()
            checkcodelist.sort()
            print('check fundcode list: '+str(checkcodelist))
            print('checknum:    '+str(checknum))
            fund_codelist.sort()
            calnum=len(fund_codelist)
            print('cal fundcode list:   '+str(fund_codelist))
            print('calnum:   '+str(calnum))
            tmpdict={}
            tmpdict['fundnum']=[calnum,checknum]
            listtmp.append(tmpdict)

            for code in  fund_codelist:
                #计算最终的收益率
                print("fund_code:   "+str(code))
                tmpdict = {}
                shoprate = shoprateDict[code]
                print('申购费率：    '+str(shoprate))
                rates = rate[rate['fund_code']==code]['fac_unit_net'].dropna().tolist()
                print('所有复权净值rates: '+str(rates))
                print(len(rates))

                newestRate = float(fund[fund['fund_code']==code]['fac_unit_net_max'].drop_duplicates())
                print("最新复权净值：  "+str(newestRate))
                tmp = 0
                for key in rates:
                    tmp = tmp+1/(( 1+float(shoprate) )*float(key))
                    # print(tmp,float(shoprate),float(key))
                print("sum: "+str(tmp))
                finallrate = newestRate*tmp/len(rates) -1
                #
                tmpdict[code]=[]
                tmpdict[code].append(finallrate)
                if not check[check['fund_code']==code][ratename].empty:
                    tmpdict[code].append(float(check[check['fund_code']==code][ratename]))
                else:
                    tmpdict[code].append('null')
                listtmp.append(tmpdict)
                print('finallrate'+str(year)+":  "+str(finallrate))

        print(str(year)+"年定投：   "+ str(listtmp))
        return(listtmp)

    def getCodefund(self,type,year):
        (fund5,fund3,fund2,fund1,rate5,rate3,rate2,rate1,check) = self.getFrame(type)
        codelist=['num']
        if year==5:
            codelist = codelist+fund5['fund_code'].drop_duplicates().tolist()
        elif year==3:
            codelist = codelist+ fund3['fund_code'].drop_duplicates().tolist()
        elif year==2:
            codelist = codelist+ fund2['fund_code'].drop_duplicates().tolist()
        elif year==1:
            codelist = codelist+ fund1['fund_code'].drop_duplicates().tolist()
        #codelist = codelist[0:3]
        return(codelist)



if __name__ == '__main__':
    starttime = time.time()
    cal = caculate2()
    #cal.dateFilter(2018,2)
    #cal.compareDate("债券型",3)
    # cal.compareDate("fof",1)
    #cal.compareDate("QDII",1)
    # cal.compareDate("货币型",3)
    # cal.compareDate("货币型",2)
    cal.compareDate("货币型",5)
    #cal.getFrame('货币型')

    #cal.cal_realrate()
    #cal.compareDate("指数型",5)
    #cal.compareDate("债券型",5)
    #cal.compareDate("股票型",5)
    #cal.get_rates()
    end = time.time()
    t = end - starttime

    print("总耗时：  "+str(t))