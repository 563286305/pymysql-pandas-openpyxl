# -*- coding: utf-8 -*-
'''
Created on 2018.01.24
@author: wuyou
'''

import pymysql
from sshtunnel import SSHTunnelForwarder
from lib.readWriteExcel import readWriteExcel
import sys
import os
import time

excel = readWriteExcel()
casepath = os.path.dirname(__file__)
basepath = os.path.dirname(casepath)
config_excel = os.path.join(basepath + "\config\\","Configuration.xlsx")
config_sheet = 'env_config'


class querySQL():

    def __init__(self):
        end = excel.get_excel_row_count(config_excel, config_sheet)
        configdict = excel.get_excel_name_value_dict(config_excel, config_sheet,'B','C','2',end)
        self.app_ssh_host = configdict['app_ssh_host']
        self.app_ssh_usr = configdict['app_ssh_usr']
        self.app_ssh_psw = configdict['app_ssh_psw']
        self.app_sql_addr = configdict['app_sql_addr']
        self.app_sql_usr = configdict['app_sql_usr']
        self.app_sql_psw = configdict['app_sql_psw']
        self.sql_port = configdict['sql_port']
        self.jlfundapp_db = configdict['jlfundapp_db']
        self.jl_ssh_host = configdict['jl_ssh_host']
        self.jl_ssh_usr = configdict['jl_ssh_usr']
        self.jl_ssh_psw = configdict['jl_ssh_psw']
        self.jl_sql_addr = configdict['jl_sql_addr']
        self.jl_sql_usr = configdict['jl_sql_usr']
        self.jl_sql_psw = configdict['jl_sql_psw']
        self.jl_jr_db = configdict['jl_jr_db']


    #巨灵测试库
    def connectdb_jl(self):
        server = SSHTunnelForwarder(
				(self.jl_ssh_host, 22),
				ssh_username = self.jl_ssh_usr,
				ssh_password = self.jl_ssh_psw,
				remote_bind_address=(self.jl_sql_addr, 3306))
        server.start()
        serverport = server.local_bind_port
        con = pymysql.connect(host='127.0.0.1',
#							   port=server.local_bind_port,
							   port=serverport,
							   user=self.jl_sql_usr,
							   passwd=self.jl_sql_psw,
		                       db=self.jl_jr_db,
							   charset='utf8')
        return server,con,serverport

    #app库
    def connectdb_app(self):
        server = SSHTunnelForwarder(
				(self.app_ssh_host, 22),
				ssh_username = self.app_ssh_usr,
				ssh_password = self.app_ssh_psw,
				remote_bind_address=(self.app_sql_addr, 3306))
        server.start()
        serverport = server.local_bind_port
        con = pymysql.connect(host='127.0.0.1',
#							   port=server.local_bind_port,
							   port=serverport,
							   user=self.app_sql_usr,
							   passwd=self.app_sql_psw,
		                       db=self.jlfundapp_db,
							   charset='utf8')
        return server,con,serverport



    def get_one_value(self,db,sqlcommand):
        cursor = db.cursor()
        # print("SQL语句：   "+str(sqlcommand))
        result = ()
        for i in range(30):
            #time.sleep(1)
            if len(result) == 0:
                try:
                    cursor.execute(sqlcommand)
                    result = cursor.fetchall()
                    print(result)
                except Exception as error:
                    print(error)
            else:
                # print("Check Sucessful ! ")
                break
        if len(result) != 0:
            result = str(result[0][0])
        else:
            result= 'empty'
        return result

    def run_sql_single_with_value(self, db, sqlcommand, value):
        cursor = db.cursor()
        test_sql = str(sqlcommand)
        print("SQL语句：   "+test_sql)
        value = [value]
        result = ()
        for i in range(30):
            time.sleep(2)
            if len(result)==0:
                try:
                    cursor.execute(test_sql, value)
                    result = cursor.fetchall()
                    print(result)
                except Exception as error:
                    print(error)
            else:
                print("Check Sucessful ! ")
                break
        if len(result)!=0:
            result = str(result[0][0])
        else:
            result = "empty"
        return result


    #sql查询，得到一个横行，取值，返回list
    def run_sql_single_with_value_return_list(self, db, sqlcommand, value):
        cursor = db.cursor()
        test_sql = str(sqlcommand)
        print("SQL语句：   "+test_sql)
        value = [value]

        resultlist = []
        result = ()
        for i in range(30):
            time.sleep(2)
            if len(result) == 0:
                try:
                    cursor.execute(test_sql, value)
                    result = cursor.fetchall()
                    print(result)
                except Exception as error:
                    print(error)
            else:
                print("Check Sucessful ! ")
                break
        if len(result) != 0:
            for i in range(len(result[0])):
                resultlist.append(str(result[0][i]))
        else:
            result = "empty"
            resultlist.append(result)
        return resultlist

    def get_sql_value(self, db, sqlcommand):
        cursor = db.cursor()
        sqlcommand = str(sqlcommand)
        result = ()
        for i in range(30):
            if len(result) == 0:
                try:
                    cursor.execute(sqlcommand)
                    result = cursor.fetchall()
                except Exception as error:
                    result = error

        return(result)

    #sql查询，得到一个竖列，取值，返回list。无value
    def sql_return_list(self, db, sqlcommand):
        cursor = db.cursor()
        test_sql = str(sqlcommand)
        resultlist = []
        result = ()
        for i in range(15):
            if len(result)==0:
                try:
                    cursor.execute(test_sql)
                    result = cursor.fetchall()
                except Exception as error:
                    print(error)
            else:
                try:
                    cursor.execute(test_sql)
                    time.sleep(1)
                    result = cursor.fetchall()
                    cursor.execute(test_sql)
                    time.sleep(1)
                    result = cursor.fetchall()
                    print(result)
                except Exception as error:
                    print(error)
                print("Check Sucessful ! ")
                break

        if len(result)!=0:
            for i in range(len(result)):
                resultlist.append(str(result[i][0]))
        else:
            result = "empty"
            resultlist.append(result)
        return resultlist

    #sql查询，得到一个竖列，取值，返回list
    def run_sql_single_with_value_return_list2(self, db, sqlcommand, value):
        cursor = db.cursor()
        test_sql = str(sqlcommand)
        print("SQL语句：   "+test_sql)
        value = [value]

        resultlist = []
        result = ()
        for i in range(15):
            time.sleep(1)
            if len(result)==0:
                try:
                    cursor.execute(test_sql, value)
                    result = cursor.fetchall()
#                    result = cursor.fetchmany(50)
                except Exception as error:
                    print(error)
            else:
                try:
                    cursor.execute(test_sql, value)
                    time.sleep(1)
                    result = cursor.fetchall()
                    cursor.execute(test_sql, value)
                    time.sleep(1)
                    result = cursor.fetchall()
#                    result = cursor.fetchmany(50)
                    print(result)
                except Exception as error:
                    print(error)

                print("Check Sucessful ! ")
                break
        if len(result)!=0:
            for i in range(len(result)):
                resultlist.append(str(result[i][0]))
        else:
            result = "empty"
            resultlist.append(result)
        return resultlist


if __name__ == '__main__':
    run = querySQL()
    # (server1,con1,serverport1) = run.connectdb_jl()
    (server2,con2,serverport2) = run.connectdb_app()

    # command = "SELECT a.FUND_CODE,b.valuagrstate FROM jljr.fnd_gen_info \
    # a INNER JOIN jlfundapp.jn_fnd_gen_info b ON a.fund_code = b.fundcode \
    # and a.FUND_CODE = '000251'"
    # command1 = "SELECT b.fund_code,b.fundsname,b.inner_code, b.estab_date\
    # FROM fnd_gen_info b \
    # WHERE \
    #     b.fund_status = 1 \
    #     AND b.isvalid = 1 \
    #     AND b.INNER_CODE NOT IN \
    #         (SELECT	rela_inner_code \
    #             FROM fnd_rela_info \
    #             WHERE isvalid = 1 \
    #             AND rela_type = 14) \
    #             AND (fnd_type = 2 or fnd_type = 4) \
    #             and (invst_type = 3 and INVST_QUAL !=1 and invst_style != 5)"
    #
    # command2 = "SELECT b.fundcode from jlfundapp.jn_fnd_gen_info b WHERE \
    # b.valuagrstate = '1' and (b.fundstate != 'a' or b.fundstate != '9' or b.fundstate != '3')"
    # cur1 = con1.cursor()
    # cur1.execute(command1)
    # result1 = cur1.fetchall()
    # result1 =list(result1)
    # print(result1)
    # print(len(result1))
    #
    # cur2 = con2.cursor()
    # cur2.execute(command2)
    # result2 = cur2.fetchall()
    # print(result2)
    # print(len(result2))
    # for key in result1:
    #     if key[1] not in result2:
    #         result1.remove(key)
    # print("new result" + str(result1))
    # print(len(result1))
    #
    # server1.stop()
    # server2.stop()
    # con1.close()
    # con2.close()


