'''
构建多线程爬取的类
'''
import threading
import download,hidden
import os,time
import queue

class Spider():
	'''
	构建spider类用于全网爬取
	'''
	def __init__(self,start_url,num=1000,max_layers=3,fail_path="./logs/fail.csv",
		succ_path="./logs/succeed.csv",save_path="./save/",time_out=1,
		use_daili=False,filter_mode=False,root_domain="baidu.com"):
		
		self.has_url_set=set() #已经爬取的url set
		self.url_queue=queue.Queue()  #一个队列
		self.start_url=start_url  #开始的url
		self.h=hidden.Hidden(page_num=2) #用于随机获取ip和port
		
		self.count=0  #已经爬取了多少个html页面
		self.num=num   #要求的html数

		self.max_layer=max_layers #最多允许爬取的最大的层次
		self.layer=0  #现在的层次

		self.fail_path=fail_path  #记录失败的文件路径
		self.succ_path=succ_path  #记录成功的文件路径

		self.save_path=save_path #保存html的最后的dir
		self.time_out=time_out

		self.use_daili=use_daili
		self.filter_mode=filter_mode
		self.root_domain=root_domain
	def start(self):
		#将初始url放入到队列中
		self.url_queue.put(self.start_url)
		self.url_queue.put("end")
	def run(self):
		while self.url_queue.qsize()>0 and (self.count<self.num) and (self.layer<self.max_layer):
			url=self.url_queue.get()

			if url=="end": #判断一个layer是否结束
				self.layer+=1
				print("Now {} th layer end,has scrapy {} html...".format(
					self.layer,self.count))
				self.url_queue.put("end")
				continue
			if url in self.has_url_set:
				continue
			#获取和保存html
			proxies=self.h.get_ip(use_daili=self.use_daili)
			header=self.h.get_header()
			file_name=os.path.join(self.save_path,"{}.html".format(self.count))
			
			status,new_url_list=download.download_save(url,proxies=proxies,headers=header,
					save_path=file_name,filter_mode=self.filter_mode,
					root_domain=self.root_domain)
			time.sleep(self.time_out)
			if status==1:
				self.log_succ(url,file_name)
				self.has_url_set.add(url)
				self._add_has_url_set_(new_url_list)
				self.count+=1
				if proxies:
					print("{} get succeed by {},there is {} url in url queue".
						format(url,proxies,self.url_queue.qsize()))
				else:
					print("{} get succeed by {},there is {} url in url queue".
						format(url,"self ip",self.url_queue.qsize()))
			else:
				self.log_fail(url)
				self.has_url_set.add(url)
			
	def log_succ(self,url,save_path):
		content=",".join([url,save_path])+"\n"
		with open(self.succ_path,"a",encoding="utf-8") as file:
			file.write(content)
	def log_fail(self,url):
		content=url+"\n"
		with open(self.fail_path,"a",encoding="utf-8") as file:
			file.write(content)

	def _add_has_url_set_(self,new_url_list):
		new_url_list=set(new_url_list)
		for new_url in new_url_list: #将新的url 添加到 self.url_queue
			if new_url not in self.has_url_set: 
				self.url_queue.put(new_url)


