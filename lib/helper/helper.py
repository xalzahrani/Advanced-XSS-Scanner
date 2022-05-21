'''
This project was developed by Abdullah as a senior project module.
'''
import requests, json
##### Warna ####### 
N = '\033[0m'
W = '\033[1;37m' 
B = '\033[1;34m' 
M = '\033[1;35m' 
R = '\033[1;31m' 
G = '\033[1;32m' 
Y = '\033[1;33m' 
C = '\033[1;36m' 
##### Styling ######
underline = "\033[4m"
##### Default ######
agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'} 
line="—————————————————" 
#####################
def session(proxies,headers,cookie):
	r=requests.Session()
	r.proxies=proxies
	r.headers=headers
	r.cookies.update(json.loads(cookie))
	return r

logo=G+"""
              _                               _  __   __ _____ _____ 
     /\      | |                             | | \ \ / // ____/ ____|
    /  \   __| |_   ____ _ _ __   ___ ___  __| |  \ V /| (___| (___  
   / /\ \ / _` \ \ / / _` | '_ \ / __/ _ \/ _` |   > <  \___ \\___ \ 
  / ____ \ (_| |\ V / (_| | | | | (_|  __/ (_| |  / . \ ____) |___) |
 /_/    \_\__,_| \_/ \__,_|_| |_|\___\___|\__,_| /_/ \_\_____/_____/ 
                                                                     
%s                                                                     
%s
<<<<<<< STARTING >>>>>>>
"""%(R+"{v0.1 Beta}"+G,underline+C+"https://github.com/xalzahrani/advanced-xss-scanner"+N+G)

##=======
"""%(R+"{v0.5 Final}"+G,underline+C+"https://github.com/xalzahrani/advanced-xss-scanner"+N+G)
	

"""
