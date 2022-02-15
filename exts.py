from flask_sqlalchemy import SQLAlchemy
#专门存放db，防止循环引用问题的出现

db=SQLAlchemy()