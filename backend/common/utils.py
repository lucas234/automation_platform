# coding=utf-8
# auther：Liul5
# date：9/17/2019 4:38 PM
# tools：PyCharm
# Python：3.7.3


def get_not_exist_fields(input_list, model):
    not_exist_fields = list(set(input_list).difference(set(model.__table__.columns.keys())))
    return not_exist_fields


def response(info=None, code=200):
    success = {"status": "success", "data": info}
    failure = {"status": "failure", "msg": info}
    if code == 200:
        return success
    else:
        return failure, code


def dump_datetime(_time):
    """Deserialize datetime object into string form for JSON processing."""
    if _time is None:
        return None
    return _time.strftime("%Y-%m-%d %H:%M:%S")


def sort_id(sort, model):
    if sort[0] == "-":
        return model.id.desc()
    else:
        return model.id.asc()
