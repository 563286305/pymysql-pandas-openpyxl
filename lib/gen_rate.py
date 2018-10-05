# -*- coding: utf-8 -*-
'''
Created on 2018.08.13
@author: wuyou
'''
import os
import json
from lib.querySQL import querySQL
from lib.readWriteExcel import readWriteExcel
from lib.interface import interface
from multiprocessing.dummy import Pool as ThreadPool
excel = readWriteExcel()
sql = querySQL()
inf = interface()
casepath = os.path.dirname(__file__)
basepath = os.path.dirname(casepath)
config_excel = os.path.join(basepath + "\config\\","Configuration.xlsx")
config_sheet = 'env_config'
ratefile = os.path.join(casepath,"rates.txt")

class gen_rate():
    def __init__(self):
        end = excel.get_excel_row_count(config_excel, config_sheet)
        configdict = excel.get_excel_name_value_dict(config_excel, config_sheet,'B','C','2',end)
        self.rate_url = configdict['rate_url']

    def getFundCodes(self):
        (server_jl,con_jl,serverport1) = sql.connectdb_jl()
        (server_app,con_app,serverport2) = sql.connectdb_app()

        command1 = '''SELECT distinct(b.fund_code) as  fund_code
                    FROM fnd_gen_info b
                    where b.isvalid = 1
                    and b.fund_status = 1
                    AND b.INNER_CODE NOT IN
                        (SELECT rela_inner_code FROM fnd_rela_info
                            WHERE isvalid = 1
                            AND rela_type = 14)
                    AND (((fnd_type = 2 OR fnd_type = 4) AND INVST_QUAL !=1) OR  INVST_QUAL =1 )
                    '''
        command_jn=''' SELECT b.fundcode AS fund_code FROM jn_fnd_gen_info b
                WHERE b.valuagrstate = '1'
                AND (b.fundstate != 'a'
                AND b.fundstate != '9'
                AND b.fundstate != '3')
        '''
        fundCodeListtmp = sql.sql_return_list(con_jl, command1)
        print("fundCodeListtmp"+str(fundCodeListtmp))
        print(len(fundCodeListtmp))
        fundCodeListjn = sql.sql_return_list(con_app, command_jn)
        fundCodeList = []
        for key in fundCodeListtmp:
            if key in fundCodeListjn:
                fundCodeList.append(key)

        print('fundCodelist:    '+str(fundCodeList))
        print(len(fundCodeList))
        server_jl.stop()
        con_jl.close()
        server_app.stop()
        con_app.close()
        return(fundCodeList)

    #取申购费率
    def getRate(self,fund_code):
        data = {'SecCode':fund_code}
        # print('data:    '+str(data))
        #text = '{"status":0,"message":"完成","a":"申购费","b":"赎回费","frontList":[{"SdtUpdate":"\/Date(-62135596800000)\/","IFundFee":0,"IFundID":0,"StrSCode":null,"StrExpType":null,"StrChargeType":null,"MApplyLowerLimit":null,"MApplyUpperLimit":100.00000000000,"DFeeRatio":1.5000,"MAmount":null,"IHoldLowerLimit":null,"IHoldUpperLimit":null,"DBuyStart":null,"FundCode":null,"DManageFee":null,"DByManageFee":null},{"SdtUpdate":"\/Date(-62135596800000)\/","IFundFee":0,"IFundID":0,"StrSCode":null,"StrExpType":null,"StrChargeType":null,"MApplyLowerLimit":100.00000000000,"MApplyUpperLimit":300.00000000000,"DFeeRatio":1.0000,"MAmount":null,"IHoldLowerLimit":null,"IHoldUpperLimit":null,"DBuyStart":null,"FundCode":null,"DManageFee":null,"DByManageFee":null},{"SdtUpdate":"\/Date(-62135596800000)\/","IFundFee":0,"IFundID":0,"StrSCode":null,"StrExpType":null,"StrChargeType":null,"MApplyLowerLimit":300.00000000000,"MApplyUpperLimit":500.00000000000,"DFeeRatio":0.8000,"MAmount":null,"IHoldLowerLimit":null,"IHoldUpperLimit":null,"DBuyStart":null,"FundCode":null,"DManageFee":null,"DByManageFee":null},{"SdtUpdate":"\/Date(-62135596800000)\/","IFundFee":0,"IFundID":0,"StrSCode":null,"StrExpType":null,"StrChargeType":null,"MApplyLowerLimit":500.00000000000,"MApplyUpperLimit":null,"DFeeRatio":null,"MAmount":1000.0000,"IHoldLowerLimit":null,"IHoldUpperLimit":null,"DBuyStart":null,"FundCode":null,"DManageFee":null,"DByManageFee":null}],"backList":null,"outerList":[{"SdtUpdate":"\/Date(-62135596800000)\/","IFundFee":0,"IFundID":0,"StrSCode":null,"StrExpType":null,"StrChargeType":null,"MApplyLowerLimit":null,"MApplyUpperLimit":null,"DFeeRatio":1.5000,"MAmount":null,"IHoldLowerLimit":null,"IHoldUpperLimit":7,"DBuyStart":null,"FundCode":null,"DManageFee":null,"DByManageFee":null},{"SdtUpdate":"\/Date(-62135596800000)\/","IFundFee":0,"IFundID":0,"StrSCode":null,"StrExpType":null,"StrChargeType":null,"MApplyLowerLimit":null,"MApplyUpperLimit":null,"DFeeRatio":0.7500,"MAmount":null,"IHoldLowerLimit":7,"IHoldUpperLimit":30,"DBuyStart":null,"FundCode":null,"DManageFee":null,"DByManageFee":null},{"SdtUpdate":"\/Date(-62135596800000)\/","IFundFee":0,"IFundID":0,"StrSCode":null,"StrExpType":null,"StrChargeType":null,"MApplyLowerLimit":null,"MApplyUpperLimit":null,"DFeeRatio":0.5000,"MAmount":null,"IHoldLowerLimit":30,"IHoldUpperLimit":365,"DBuyStart":null,"FundCode":null,"DManageFee":null,"DByManageFee":null},{"SdtUpdate":"\/Date(-62135596800000)\/","IFundFee":0,"IFundID":0,"StrSCode":null,"StrExpType":null,"StrChargeType":null,"MApplyLowerLimit":null,"MApplyUpperLimit":null,"DFeeRatio":0.2500,"MAmount":null,"IHoldLowerLimit":365,"IHoldUpperLimit":730,"DBuyStart":null,"FundCode":null,"DManageFee":null,"DByManageFee":null},{"SdtUpdate":"\/Date(-62135596800000)\/","IFundFee":0,"IFundID":0,"StrSCode":null,"StrExpType":null,"StrChargeType":null,"MApplyLowerLimit":null,"MApplyUpperLimit":null,"DFeeRatio":0.0000,"MAmount":null,"IHoldLowerLimit":730,"IHoldUpperLimit":null,"DBuyStart":null,"FundCode":null,"DManageFee":null,"DByManageFee":null}]}'
        try:
            content = json.loads(inf.get_rate(self.rate_url,data))
        except Exception as error:
            print('fund_code:   '+str(fund_code) + "  "+ str(error))
            content = {}
        # print('content:     '+str(content))
        # print("fund_code for front:   "+str(fund_code))
        # print("frontlist:   "+str(content['frontList']))
        #content = json.loads(text)
        if not content or 'frontList' not in content or content['frontList'] == 'null' or not isinstance(content['frontList'],list):
            rate = 0
        else:
            frontList = content['frontList']
            tmp = 0
            for front in frontList:
                if 'DFeeRatio' in front:
                    if isinstance(front['DFeeRatio'],float):
                        if front['DFeeRatio'] > tmp:
                            tmp = front['DFeeRatio']
            rate = tmp*0.01*0.1
        print("shoprate:    "+str(rate))
        return (fund_code,rate)

    def getRates(self,fundCodeList):
        dict1 = {}
        p = ThreadPool(4)
        results = p.map(self.getRate,fundCodeList)
        for result in results:
            dict1[result[0]]=result[1]

        f= open(ratefile,'w+')
        f.write(str(dict1))
        f.close
        ratefile

if __name__ == '__main__':
    gen = gen_rate()
    codelist = gen.getFundCodes()
    gen.getRates(codelist)
