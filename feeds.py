import os

import users
from db import db


def create_feed(secret, title, description):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO feeds (secret, title, description, user_id, created_at) " \
          "VALUES (:secret, :title, :description, :user_id, NOW())"
    db.session.execute(
        sql,
        {
            "secret": secret,
            "title": title,
            "description": description,
            "user_id": user_id,
        },
    )
    db.session.commit()
    return True


def delete_feed(secret):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "SELECT * FROM feeds WHERE secret=:secret"
    feed = db.session.execute(sql, {"secret": secret}).fetchone()
    if user_id != feed["user_id"]:
        return False

    sql = "SELECT * FROM items WHERE feed_id=:feed_id"
    items = db.session.execute(sql, {"feed_id": feed["id"]}).fetchall()

    for item in items:
        if os.path.exists(item["path"]):
            os.remove(item["path"])

    sql = "DELETE from items WHERE feed_id=:feed_id"
    db.session.execute(sql, {"feed_id": feed["id"]})
    db.session.commit()
    sql = "DELETE from feeds WHERE id=:id"
    db.session.execute(sql, {"id": feed["id"]})
    db.session.commit()
    return True


def get_feed(secret):
    sql = "SELECT * FROM feeds WHERE secret=:secret"
    result = db.session.execute(sql, {"secret": secret})
    return result.fetchone()


def get_feeds():
    sql = "SELECT * FROM feeds WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id": users.user_id()})
    return result.fetchall()


def get_items(secret):
    sql = "SELECT I.id as id, I.description as description, I.path as path, I.created_at as created_at, I.user_id as user_id  " \
          "FROM items I, feeds F WHERE I.feed_id=F.id AND F.secret=:secret ORDER BY I.created_at DESC"
    result = db.session.execute(sql, {"secret": secret})
    return result.fetchall()


def create_item(secret, path, description):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "SELECT id FROM feeds WHERE secret=:secret"
    result = db.session.execute(sql, {"secret": secret})
    feed = result.fetchone()
    if feed == None:
        return False
    sql = "INSERT INTO items (feed_id, path, description, user_id, created_at) " \
          "VALUES (:feed_id, :path, :description, :user_id, NOW())"
    db.session.execute(
        sql,
        {
            "feed_id": feed[0],
            "path": path,
            "description": description,
            "user_id": user_id,
        },
    )
    db.session.commit()
    return True


def delete_item(secret, id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "SELECT id, user_id FROM feeds WHERE secret=:secret"
    result = db.session.execute(sql, {"secret": secret})
    feed = result.fetchone()
    if feed == None:
        return False
    sql = "SELECT id, user_id, path FROM items WHERE feed_id=:feed_id AND id=:id"
    result = db.session.execute(sql, {"feed_id": feed[0], "id": id})
    item = result.fetchone()
    if feed["user_id"] != user_id and item["user_id"] != user_id:
        return False
    if os.path.exists(item["path"]):
        os.remove(item["path"])
    sql = "DELETE FROM items WHERE feed_id=:feed_id AND id=:id"
    db.session.execute(sql, {"feed_id": feed[0], "id": id})
    db.session.commit()
    return True


def get_votes(item_id):
    sql = "SELECT id FROM votes WHERE feed_id=:feed_id AND item_id=:item_id"
    result = db.session.execute(sql, {"secret": secret})
    return result.fetchall()


def vote_item(secret, item_id):
    user_id = users.user_id()
    sql = "SELECT id FROM items I, feeds F WHERE I.feed_id=F.id AND F.secret=:secret"
    result = db.session.execute(sql, {"secret": secret, "id": item_id})
    item = result.fetchone()
    if user_id == 0 or item == None:
        return False
    sql = "SELECT id FROM votes WHERE feed_id=:feed_id AND item_id=:item_id AND user_id=:user_id"
    result = db.session.execute(
        sql, {"feed_id": feed_id, "item_id": item_id, "user_id": user_id}
    )
    vote = result.fetchone()
    if vote == None:
        sql = "INSERT INTO votes (feed_id, item_id, user_id) VALUES (:content, :user_id, NOW())"
    else:
        sql = "DELETE FROM votes WHERE feed=:feed_id AND item_id=:item_id AND user_id=:user_id"
    db.session.execute(
        sql, {"feed_id": feed_id, "item_id": item_id, "user_id": user_id}
    )
    db.session.commit()
    return True
