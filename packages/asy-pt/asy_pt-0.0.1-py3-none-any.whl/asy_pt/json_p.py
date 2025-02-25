# -*- coding: utf-8 -*-
# @Time    : 2024/12/25 14:36
# @Author  : xuwei
# @FileName: json_p.py
# @Software: PyCharm

import json


##datetime.datetime is not JSON serializable 报错问题解决
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):

        from datetime import date
        import datetime

        if obj != obj:
            return None
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        # elif isinstance(obj, numpy.integer):
        #     return int(obj)
        # elif isinstance(obj, numpy.floating):
        #     return float(obj)
        # elif isinstance(obj, numpy.ndarray):
        #     return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj)
        # elif isinstance(obj, bson.ObjectId):
        #     return str(obj)
        return json.JSONEncoder.default(self, obj)


def dump_json(data):
    return json.dumps(data, ensure_ascii=False, cls=CJsonEncoder)


def load_json(data):
    return json.loads(data)
