import requests
import core


def gethtml(url):
    headers = core.GetHeaders()
    if not (url.startswith("http://") or url.startswith("https://")):
        url="http://"+url
    try:
        rep = requests.get(url,headers=headers,timeout=2)
        html = rep.text
    except Exception as e:
        #不管其返回的是错误，null，都将其页面放入html，留给check_waf计算相似度
        html = str(e)
        pass
    return html

if __name__ == '__main__':
    html = gethtml("http://testphp.vulnweb.com:80/listproducts.php?cat=1'")
    print(html)

