from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Room(db.Model):
    id     = db.Column(db.Integer  , primary_key=True)
    link   = db.Column(db.String(8), unique=True, nullable=False) # the part of the link after rooms/
    status = db.Column(db.String )
    names  = db.Column(db.String)
    code= db.Column(db.String)
    def __repr__(self):
        return f"<Room {self.id}:{self.link}>"
def init_room(link,status,names,code):
    room= Room(link=link,status=status,names=names,code=code)
    db.session.add(room)
    db.session.commit()
    return room.id

def delete_room(link):
    room=Room.query.filter_by(link=link).first()
    db.session.delete(room)
    db.session.commit()


def get_room(link):
    room=Room.query.filter_by(link=link).first()
    if room is None:
        return "NO SUCH ROOM"
    return {"link":room.link, "status":room.status,"names":room.names,"code":room.code}
def update_room(link, status="",names="",code=""):
    """
    link is required to identify the room 
    insert new values for current room can change anything besides the link
    e.g to change only the names write update_room("somelink",names="some new names")
    """
    room = Room.query.filter_by(link=link).first()
    if status != "":
        room.status=status
    if names != "":
        room.names=names
    if code != "":
        room.code=code