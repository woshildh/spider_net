import spider
import flask
from flask import Flask,make_response,jsonify,send_file,request
from flask_cors import *

app=Flask(__name__)
CORS(app, supports_credentials=True)

#设置ip和port
SERVER_HOST="localhost"
SERVER_PORT=5555

@app.route("/")
def index():
	return send_file("static/index.html")

@app.route("/images/<file_name>")
def req_images(file_name):
	return send_file("static/images/{}".format(file_name))

@app.route("/css/<file_name>")
def req_css(file_name):
	return send_file("static/css/{}".format(file_name))

@app.route("/run",methods=['GET', 'POST'])
def run_spider():
	if request.method=="POST":
		params=get_values(request)
		print("get a request,params is as follows:")
		for key in params.keys():
			print("{} : {}".format(key,params[key]))
		s=spider.Spider(start_url=params["start_url"],
			num=params["num"],max_layers=params["depth"],
			use_daili=params["use_daili"],time_out=params["time_out"],
			filter_mode=params["filter_mode"],
			root_domain=params["root_domain"])
		s.start()
		s.run()

		#返回的内容
		content={"download_num":len(s.has_url_set),
		"layer":s.layer}
		res=make_response(jsonify(content))
		res.headers['Access-Control-Allow-Origin'] = "*"
		return  res 

def get_values(request):
	'''
	从request中提取出7个参数
	'''
	params={}
	params["start_url"]=request.values.get("start_url")
	if request.values.get("use_daili")=="True":
		params["use_daili"]=True
	else:
		params["use_daili"]=False
	
	if request.values.get("filter_mode")=="True":
		params["filter_mode"]=True
	else:
		params["filter_mode"]=False

	params["root_domain"]=request.values.get("root_domain")
	params["num"]=int(request.values.get("num"))
	params["depth"]=int(request.values.get("depth"))
	params["time_out"]=float(request.values.get("time_out"))

	return params

if __name__=="__main__":
	app.run(host=SERVER_HOST,port=SERVER_PORT,debug=True)

