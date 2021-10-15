class VisitedTables(object):

    def __init__(self):
        self.data = 2000*[None]
        self.capacity = 2000
        self.size = 0

    def __getitem__(self, key):
        return self._bucket_getitem(key % self.capacity, key)

    def __setitem__(self, key, values):
        bucket_index = key % self.capacity
        self._bucket_setitem(bucket_index, key, values)

    def __contains__(self, item):
        if self.data[item%self.capacity]==None:
            return False
        else:
            if self.data[item%self.capacity][0]==item:
                return True
            return False

    def _bucket_getitem(self, index, key):
        if self.data[index] is None:
            raise KeyError('No elements with that index')
        else:
            if key==self.data[index][0]:
                return self.data[index][1][0]

    def _bucket_setitem(self, index, key, values):
        if self.data[index]==None:
            self.data[index]=[key,values]
            self.size += 1
        else:
            if self.data[index][1][1]>values[1]:
                self.data[index] = [key, values]

