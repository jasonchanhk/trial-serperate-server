from core import db
from core.models.user import Useraccount



db.drop_all()


db.create_all()

l = Useraccount(username="Start", password="First", email="1@email.com")
db.session.add(l)
db.session.commit()
