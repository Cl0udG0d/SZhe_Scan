from app.scan.self.vul.sqlinjection.InjectionIndex import InjectionControl
from app.scan.self.vul.XSSBug.XSSCheck import GetXSS
from app.scan.self.vul.ComIn.ComCheck import GetComIn
from app.scan.self.vul.File_Inclusion.LocalFileInclude import CheckLocalFileInclude
from app.scan.self.vul.POCScan import POCScan


class BugScan:
    def __init__(self, oldurl, url):
        self.url = url
        self.oldurl = oldurl

    def SQLBugScan(self):
        try:
            vulnerable, payload, bugdetail = InjectionControl(self.url)
            return vulnerable, payload, bugdetail
        except Exception as e:
            print(e)
            return False, None,None

    def XSSBugScan(self):
        try:
            vulnerable, payload, bugdetail = GetXSS(self.url)
            return vulnerable, payload, bugdetail
        except Exception as e:
            print(e)
            return False, None, None

    def ComInScan(self):
        try:
            vulnerable, payload, bugdetail = GetComIn(self.url)
            return vulnerable, payload, bugdetail
        except Exception as e:
            print(e)
            return False, None, None

    def FileIncludeScan(self):
        try:
            vulnerable, payload, bugdetail = CheckLocalFileInclude(self.url)
            return vulnerable, payload, bugdetail
        except Exception as e:
            print(e)
            return False, None, None

    def POCScan(self):
        try:
            POCScan.POCScanConsole(self.oldurl, self.url)
        except Exception as e:
            print(e)
            pass

if __name__ == '__main__':
    # test=BugScan('http://testphp.vulnweb.com/listproducts.php?cat=1')
    # test=BugScan('http://leettime.net/xsslab1/chalg1.php?name=1')
    # print(test.SQLBugScan())
    test = BugScan('http://127.0.0.1/Cl0ud.php?page=1')
    print(test.FileIncludeScan())
