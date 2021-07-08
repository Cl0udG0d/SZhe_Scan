from app.utils.selfrequests import normalReq

class TargetMsg:
    def __init__(self,url):
        self.url=url
        self.domain=self.getDomain()
        self.target=self.getTarget()
        self.isDomain=self.checkDomain()
        self.rep=None

        return

    def getTarget(self):
        self.rep=normalReq(self.target)

    def getDomain(self):
        return

    def getResponse(self):

        return

    def getStatus(self):

        return

    def getTargetPort(self):
        return

    def getTargetSensitiveMsg(self):
        return

    def checkDomain(self):
        pass
