# -*- coding: utf-8 -*-
'''
Created on 2018.04.25
@author: wuyou
'''

import requests
import json

class interface():
	#申购费率查询接口:
	def get_rate(self,url,data):
		try:
			headers = {'Content-Type': 'application/json;charset=UTF-8'}
			result = requests.post(url,data=json.dumps(data),headers=headers)
			# print("查询结果：")
			# print(result.text)
			return str(result.text)
		except Exception as error:
			print(url + " : Check rate failed! ")
			print("data:	"+ str(data))
			result = 'false'
			return result

	#删除实时缓存数据
	def del_realtime_cache(self,url,data):
		try:
			headers = {'Content-Type': 'application/json;charset=UTF-8'}
			result = requests.post(url,data=json.dumps(data), headers=headers)
			print("删除缓存结果: " + str(result))
		except Exception as error:
			print(url + " : Add realtime cache failed! ")
			print("删除缓存结果: " + str(error))
			result = 'false'
		return result

	#推实时的缓存接口
	def add_realtime_cache(self,url,data):
		try:
			headers = {'Content-Type': 'application/json;charset=UTF-8'}
			result = requests.post(url,data=json.dumps(data), headers=headers)
			print("推送缓存结果: " + str(result))
		except Exception as error:
			print(url + " : Add realtime cache failed! ")
			print("推送缓存结果: " + str(error))
			result = 'false'
		return result

	#实时反欺诈接口
	def inf_realtime(self,url,data):
		try:
			headers = {'Content-Type': 'application/json;charset=UTF-8'}
			result = requests.post(url,data=json.dumps(data), headers=headers)
			print("实时反欺诈接口返回值: " + str(result.content))
			return str(result.content)
		except Exception as error:
			print(url + " : Trager realtime interface failed! ")
			print("实时反欺诈接口返回值: " + error)
			result = 'false'
			return result


if __name__ == '__main__':
	url = 'http://data.jnlc.com:80/app/home/getFeeApplyOrRedemption'
	#SecCode用基金的fundcode
	#data = {'SecCode':'110025'}
	data = {'SecCode':'510050'}

	inf = interface()
	#inf.inf_realtime(requesturl,requestdict)
	#inf.add_realtime_cache(cacheurl,cachedict)
	result = inf.get_rate(url,data)
	print(str(result))
