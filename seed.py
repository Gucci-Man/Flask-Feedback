"""Seed file to make sample data for db."""

from models import *
from app import *

# Create all tables
db.drop_all()
db.create_all()

robin = User.register("Robin", "batmansmells123", "robin@gmail.com", 'Dick', 'Grayson')
batman = User.register("Batman",'robinlaidanegg321', "batman@gmail.com", 'Bruce', 'Wayne')
catwoman = User.register("Catwoman", 'catwomanrules987', "catwoman@gmail.com", 'Selina', 'Kyle')

db.session.add_all([robin, batman, catwoman])
db.session.commit()

f1 = Feedback(title="Robin and Batman", content="Batman and Robin rules the world", username='Robin')
f2 = Feedback(title="Robin and Batman Again", content="Gotham is under their protection", username='Robin')
f3 = Feedback(title="The Dark Knight", content="I AM BATMAN", username='Batman')
f4 = Feedback(title="The Dark Knight Rises", content="No villian can beat Batman", username='Batman')
f5 = Feedback(title="The Catwoman", content="Catwoman teamed up with Batman makes for a dynamic duo", username='Catwoman')

db.session.add_all([f1, f2, f3, f4, f5])
db.session.commit()