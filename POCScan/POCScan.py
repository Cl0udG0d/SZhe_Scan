from Init import app,redispool
from exts import db
from models import POC,BugList
import core
import requests

def POCScanConsole(attackurl,url):
    try:
        allpoc=POC.query.all()
        with app.app_context():
            for poc in allpoc:
                rep = requests.get(url+poc.rule, headers=core.GetHeaders(),timeout=2)
                if rep.status_code!=404 and poc.expression in rep.text:
                    bug = BugList(oldurl=attackurl, bugurl=url, bugname=poc.name,buggrade=redispool.hget('bugtype', poc.name), payload=url+poc,
                                      bugdetail=rep.text)
                    redispool.pfadd(redispool.hget('bugtype', poc.name), url)
                    redispool.pfadd(poc.name, url)
                    db.session.add(bug)
            db.session.commit()
    except Exception as e:
        print(e)
        pass
