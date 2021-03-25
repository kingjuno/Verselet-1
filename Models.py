import pandas as pd

def init_room(l, s, n, c):
    db = pd.read_csv('rooms.csv')
    db = db.append({'link': l, 'status': s, 'n': n, 'code': c}, ignore_index=True)
    db.to_csv('rooms.csv', index=False)
    # return room.id


def delete_room(link):
    inx = 0; db = pd.read_csv('rooms.csv')
    for i in db['link']:
        if i == link:
            pass # REMOVE ROOM HERE
        else: inx += 1


def get_room(link):
    global room_link, room_status, room_names, room_code

    inx = 0; db = pd.read_csv('rooms.csv')
    for i in db['link']:
        if i == link:
            room_link = i; room_status = db['status'][inx]; room_names = db['names'][inx]; room_code = db['code'][inx]
        else:
            inx += 1
    return {"link": room_link, "status": room_status, "names": room_names, "code": room_code}
