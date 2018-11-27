'''
1.完成获取代理ip和端口号的任务
2.构造一组随机的headers
'''
import requests
from bs4 import BeautifulSoup
import random
import time

class Hidden(object):
	'''
	一个用于隐藏自身身份的类
	'''
	def __init__(self,url_path="http://www.xicidaili.com/nn/",page_num=1):
		self.url_path=url_path
		self.page_num=page_num
		self.proxies=[]
		self.get_ip_list()
	def get_ip_list(self):
		for i in range(self.page_num):
			url=self.url_path+str(i+1)
			head= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
			req=requests.get(url, headers=head)
			if req.status_code==200:
				html=req.text
				b=BeautifulSoup(html,"lxml")
				item_list=b.find_all(name="tr",attrs={"class":"odd"})
				for it in item_list:
					ip=it.find_all("td")[1].text
					port=it.find_all("td")[2].text
					t=ip+":"+port
					self.proxies.append(t)
			else:
				print("There is no response for request...")
			time.sleep(3)
		print("Get {} ip".format(len(self.proxies)))
	def get_ip(self,use_daili=True):
		if use_daili:
			ip=self.proxies[random.randint(0,len(self.proxies)-1)]
		else:
			ip=False
		return ip
	def get_header(self):
		ua_list = [
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
			"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
			"Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
			"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
			"",
		]
		accept_list=[
			"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
			"*/*"
		]
		accept_encoding_list=[
			"gzip, deflate",
			"gzip, deflate, br"
		]
		headers={"User-Agent":ua_list[random.randint(0,len(ua_list)-1)],
			"Accept":accept_list[random.randint(0,len(accept_list)-1)],
			"Accept-Encoding":accept_encoding_list[random.randint(0,len(accept_encoding_list)-1)],
			"Accept-Language":"zh-CN,zh;q=0.8"}
		return headers


if __name__=="__main__":
	h=Hidden(page_num=2)
	head=h.get_header()
	print(head)

