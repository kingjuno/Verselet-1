from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(8), unique=True, nullable=False) # the part of the link after rooms/
    users= db.Column(db.String(80), nullable=False) #list of users in room converted to string

    def __repr__(self):
        return f"<Room {self.id}:{self.link}>"
