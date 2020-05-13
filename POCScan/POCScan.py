from init import app,redispool
from exts import db
from models import POC,BugList
import core
import requests

def POCScanConsole(attackurl,url):
    allpoc=POC.query.all()
    with app.app_context():
        for poc in allpoc:
            try:
                rep = requests.get(url+poc.rule, headers=core.GetHeaders(),timeout=2)
                if rep.status_code!=404 and poc.expression in rep.text:
                    bug = BugList(oldurl=attackurl, bugurl=url, bugname=poc.name,buggrade=redispool.hget('bugtype', poc.name), payload=url+poc,
                                  bugdetail=rep.text)
                    db.session.add(bug)
            except Exception as e:
                print(e)
                pass
        db.session.commit()
    return None