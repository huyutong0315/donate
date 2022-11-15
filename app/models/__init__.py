from app.models.base import db


# 将json所有字段插入到对应表的对应字段中
def json2db(jsondata, table):
    with db.auto_commit():
        new_record = table()
        for k in jsondata:
            if jsondata is not None:
                setattr(new_record, k, jsondata[k])
        # 使用merge方法，存在则修改，不存在则新增，只查主键
        db.session.merge(new_record)
        db.session.commit()
    return new_record


def json2db_add(jsondata, table):
    new_record = table()
    for k in jsondata:
        if jsondata is not None:
            setattr(new_record, k, jsondata[k])
    db.session.add(new_record)
    db.session.flush()
    db.session.commit()
    return new_record
