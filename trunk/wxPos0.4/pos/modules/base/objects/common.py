
class Object:
    item = None
    all_items = None

    def getAll(self, refresh=False):
        if refresh or self.all_items is None:
            item_ids = self.dbGetAll()
            if self.all_items is not None:
                old_items_dict = dict(map(lambda item: (item.id, item), self.all_items))
                deleted_item_ids = filter(lambda _id: _id not in item_ids, old_items_dict.keys())
                for _id in deleted_item_ids:
                    self.all_items.remove(self.find(_id=_id))
                for _id in item_ids:
                    if _id in old_items_dict.keys():
                        item = old_items_dict[_id]
                        item.getData()
                    else:
                        self.all_items.append(self.item(_id))
            else:
                self.all_items = map(lambda _id: self.item(_id), item_ids)
        return self.all_items

    def find(self, list=False, _id=None, **kwargs):
        results = self.getAll()
        if _id is not None or len(kwargs)>0:
            matches = []
            if _id is not None:
                matches.append(lambda i: (i.id == _id))
            for key, val in kwargs.iteritems():
                matches.append(lambda i: (i.data[key] == val))
            for m in matches:
                results = filter(m, results)

        count = len(results)
        if list or count>1:
            return [r for r in results]
        elif count == 0:
            return None
        elif count == 1:
            return results[0]

    def add(self, **kwargs):
        args_items = filter(lambda (k, v): k in self.item.data_keys, kwargs.items())
        args = dict(args_items)
        data_items = map(lambda (k, v): (k, self.getDBData(k, v)), args_items)
        data = dict(data_items)
        _id = self.dbInsert(**data)
        if _id:
            i = self.item(_id)
            i.data.update(args)
            self.getAll(refresh=True)
            return i
        else:
            return None

    def getDBData(self, key, val):
        return val

class DataDict(dict):
    def __init__(self, obj):
        dict.__init__(self)
        self.obj = obj
        self.keys = obj.data_keys
    
    def __missing__(self, key):
        if key not in self.keys:
            raise KeyError, 'No data key %s' % (key,)
        else:
            self.obj.getData()
            if not self.has_key(key):
                raise KeyError, 'No data key %s' % (key,)
            else:
                return self[key]

    def copy(self):
        if len(self) == 0:
            self.obj.getData()
        return dict.copy(self)

class Item:
    data_keys = tuple()

    def getData(self):
        pass

    def __init__(self, _id):
        self.id = _id
        self.data = DataDict(self)

    def __eq__(self, el):
        try:
            return type(self) == type(el) and self.id == el.id
        except AttributeError:
            return False
    
    def __ne__(self, el):
        try:
            return type(self) != type(el) or self.id != el.id
        except AttributeError:
            return False

    def update(self, **kwargs):
        args_items = filter(lambda (k, v): k in self.data_keys, kwargs.items())
        args = dict(args_items)
        data_items = map(lambda (k, v): (k, self.obj.getDBData(k, v)), args_items)
        data = dict(data_items)
        success = self.obj.dbUpdate(self.id, **data)
        if success:
            self.data.update(args)
            self.obj.getAll(refresh=True)
            return True
        else:
            return False

    def delete(self):
        success = self.obj.dbDelete(self.id)
        if success:
            self.obj.getAll(refresh=True)
            return True
        else:
            return False

    def get(self, key):
        self.getData()
        return self.data[key]
