'''
下载页面并且保存html页面
'''
import requests
import parse

def download_save(url,proxies,headers,save_path,filter_mode,root_domain):
	'''
	params:
		url:要爬取的url
		ip:代理ip地址
		port:端口号
		save_path:保存的路径
	returns:
		status:状态，是否下载并且保存成功
		url_list:这个页面中的url_list
	'''
	try:
		if proxies:
			if "https" in url:
				proxies={"https":proxies}
			else:
				proxies={"http":proxies}
			req=requests.get(url,headers=headers,proxies=proxies)
		else:
			req=requests.get(url,headers=headers)
		if req.status_code==200:  #判断状态是否是200
			html=req.text
		else:
			return -1,[]

		with open(save_path,"w",encoding="utf-8") as file:
			file.write(html)
			url_list=parse.get_url(html,filter_mode,root_domain)
		return 1,url_list
	except:
		return -1,[]

