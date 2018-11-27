import download,config,hidden,parse
import os
import spider

def main():
	'''
	进行爬取的主函数
	'''
	s=spider.Spider(config.start_url,num=config.num,
		max_layers=config.depth,succ_path=config.log_succ_path,
		fail_path=config.log_fail_path,save_path=config.root_save_path,
		time_out=config.time_out,filter_mode=config.filter_mode,
		root_domain=config.root_domain,use_daili=config.use_daili)
	s.start()
	s.run()
	print(len(s.has_url_set))

if __name__=="__main__":
	main()

