from sqlinjection.InjectionIndex import InjectionControl
from XSSBug.XSSCheck import GetXSS
from ComIn.ComCheck import GetComIn
from File_Inclusion.LocalFileInclude import CheckLocalFileInclude


class BugScan:
    def __init__(self,url,reaidspool):
        self.url=url
        self.redispool=reaidspool

    def SQLBugScan(self):
        vulnerable, db, payload =InjectionControl(self.url)
        return vulnerable,db,payload

    def XSSBugScan(self):
        vulnerable, website, payload=GetXSS(self.url,self.redispool)
        return vulnerable, website, payload

    def ComInScan(self):
        vulnerable, website, payload=GetComIn(self.url)
        return vulnerable, website, payload

    def FileIncludeScan(self):
        vulnerable, website, payload=CheckLocalFileInclude(self.url)
        return vulnerable, website, payload

    def WebLogicScan(self):
        return None

    def POCScan(self):
        return None

if __name__=='__main__':
    # test=BugScan('http://testphp.vulnweb.com/listproducts.php?cat=1')
    # test=BugScan('http://leettime.net/xsslab1/chalg1.php?name=1')
    # print(test.SQLBugScan())
    test=BugScan('http://127.0.0.1/Cl0ud.php?page=1')
    print(test.FileIncludeScan())