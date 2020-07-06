from sqlinjection.InjectionIndex import InjectionControl
from XSSBug.XSSCheck import GetXSS
from ComIn.ComCheck import GetComIn
from File_Inclusion.LocalFileInclude import CheckLocalFileInclude
from POCScan import POCScan


class BugScan:
    def __init__(self, oldurl, url):
        self.url = url
        self.oldurl = oldurl

    def SQLBugScan(self):
        vulnerable, payload, bugdetail = InjectionControl(self.url)
        return vulnerable, payload, bugdetail

    def XSSBugScan(self):
        vulnerable, payload, bugdetail = GetXSS(self.url)
        return vulnerable, payload, bugdetail

    def ComInScan(self):
        vulnerable, payload, bugdetail = GetComIn(self.url)
        return vulnerable, payload, bugdetail

    def FileIncludeScan(self):
        vulnerable, payload, bugdetail = CheckLocalFileInclude(self.url)
        return vulnerable, payload, bugdetail

    def POCScan(self):
        POCScan.POCScanConsole(self.oldurl, self.url)


if __name__ == '__main__':
    # test=BugScan('http://testphp.vulnweb.com/listproducts.php?cat=1')
    # test=BugScan('http://leettime.net/xsslab1/chalg1.php?name=1')
    # print(test.SQLBugScan())
    test = BugScan('http://127.0.0.1/Cl0ud.php?page=1')
    print(test.FileIncludeScan())
