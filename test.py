from app.utils.baseMsg import GetBaseMessage
import requests

def main():
    rep=requests.get('https://www.cnblogs.com/Cl0ud')
    basemsg = GetBaseMessage('www.cnblogs.com', 'https://www.cnblogs.com/Cl0ud', rep)
    print(basemsg.GetFinger())
    return

if __name__ == '__main__':
    main()