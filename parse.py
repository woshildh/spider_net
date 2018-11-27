import re
from bs4 import BeautifulSoup

def get_url(html,filter_mode,root_domain):
	'''
	从html中提取出所有的有用的url并且返回url_list
	params:
		html:html
	returns:
		url_list
	'''
	b=BeautifulSoup(html,"lxml")
	a_list=b.find_all("a")
	url_list=[]
	for a in a_list:
		url=a.get("href")
		url_list.append(url)

	for i in range(len(url_list)):
		if not url_list[i]:
			url_list[i]="xxxx"
		url_list[i]=url_list[i].strip()
		if "http" not in url_list[i]:
			url_list[i]="http:"+url_list[i]
		if filter_mode and root_domain not in url_list[i]:
			url_list[i]="xxxx"
	url_list=set(url_list)
	while "xxxx" in url_list:
		url_list.remove("xxxx")
	url_list=list(url_list)

	return url_list

if __name__=="__main__":
	file=open("./p.html","r",encoding="utf-8").read()
	url_list=get_url(file)
	for url in url_list:
		if "http" not in url:
			print(url)

