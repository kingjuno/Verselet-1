import pandas as pd
def init_room(l, s, gn, n):
    db = pd.read_csv('rooms.csv')
    db = db.append({'link': l, 'status': s, 'name': gn, 'n': n}, ignore_index=True)
    db.to_csv('rooms.csv', index=False)
    # return room.id


def delete_room(link):
    db=pd.read_csv('rooms.csv')
    db=db.drop(db[db['link']==link].index)
    db.to_csv('rooms.csv',index=False)

def get_room(link):
    global room_link, room_status, room_names

    inx = 0; db = pd.read_csv('rooms.csv')
    for i in db['link']:
        if i == link:
            room_link = i; room_status = db['status'][inx]; room_name = db['name'][inx]; room_names = db['n'][inx]
            return [["link", room_link], ["status", room_status], ['name', room_name], ["n", room_names]]
        else:
            inx += 1
