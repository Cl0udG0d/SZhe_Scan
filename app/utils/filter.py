
def check2filter(targets):
    '''
    去重和规范化输入
    '''
    targets = targets.split()
    targetsSet=set()
    newTarget=list()
    for i, tempurl in enumerate(targets):

        url = tempurl[:-1] if tempurl.endswith("/") else tempurl
        url = url.replace("http://","") if url.startswith("http://") else url
        url =url.replace("https://","") if url.startswith("https://") else url

        url= url.split('/')[0] if "/" in url else url
        # url=url.split(':')[0] if ":" in url else url

        if url not in targetsSet:
            targetsSet.add(url)
            newTarget.append(url)

    return newTarget,len(newTarget)

def inputfilter(url):
    rep,rep1,rep2=None,None,None
    if url.endswith("/"):
        url=url[:-1]
    if not url.startswith("http://") and not url.startswith("https://"):
        attackurl1="http://"+url
        attackurl2="https://"+url
        try:
            rep1=requests.get(attackurl1, headers=core.GetHeaders(), timeout=10, verify=False)
        except Exception as e:
            pass
        try:
            rep2=requests.get(attackurl2, headers=core.GetHeaders(), timeout=10, verify=False)
        except Exception as e:
            pass
        if rep1:
            return url,attackurl1,rep1
        elif rep2:
            return url,attackurl2,rep2
        else:
            print("None data")
            try:
                count=redispool.hget('targetscan', 'waitcount')
                if 'str' in str(type(count)):
                    waitcount=int(count)-1
                    redispool.hset("targetscan", "waitcount", str(waitcount))
                else:
                    redispool.hset("targetscan", "waitcount", "0")
                redispool.hdel("targetscan", "nowscan")
            except Exception as e:
                print(e)
                pass
            return None,None,None
    if "http://" in url or "https://" in url:
        attackurl=url
        try:
            rep=requests.get(attackurl, headers=core.GetHeaders(), timeout=10, verify=False)
        except:
            pass
        if rep:
            if "http://" in url:
                return url.replace("http://",""),attackurl,rep
            else:
                return url.replace("https://",""),attackurl,rep
        else:
            print("{}访问超时".format(attackurl))
            return None,None,None



