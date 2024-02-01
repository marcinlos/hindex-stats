import hashlib
import json


class MemoryDatabase:
    def __init__(self):
        self.objects = {}
        self.refs = {}

    def write(self, data):
        key = hash_object(data)
        self.objects[key] = data
        return key

    def read(self, id):
        return self.objects[id]

    def write_ref(self, ref, key):
        self.refs[ref] = key

    def read_ref(self, ref):
        return self.refs[ref]

    def delete_ref(self, ref):
        del self.refs[ref]


def hash_object(data):
    json_object = json.dumps(data, sort_keys=True)
    text = json_object.encode("utf-8")
    return hashlib.sha256(text).hexdigest()
