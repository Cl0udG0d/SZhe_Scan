from init import app,redispool
from exts import db
from models import POC,BugList,BugType
import core
import requests

def POCScanConsole(attackurl,url):
    allpoc=POC.query.all()
    try:
        with app.app_context():
            for poc in allpoc:
                rep = requests.get(url+poc.rule, headers=core.GetHeaders(),timeout=2)
                if rep.status_code!=404 and poc.expression in rep.text:
                    bugtype = BugType.query.filter(BugType.bugtype == poc.name).first()
                    bug = BugList(oldurl=attackurl, bugurl=url, bugtypeid=bugtype.id, payload=url+poc,
                                  bugdetail=rep.text)
                    db.session.add(bug)
                    db.session.commit()

    except Exception as e:
        print(e)
        pass
    return None