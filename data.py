from os.path import exists
import json

class Data:
    def __init__(self):
        if exists('./data.json'):
            self.data = json.load(open('./data.json'))
        else:
            self.data = {}

    def write(self):
        t = json.dumps(self.data, indent=4)
        with open('./data.json', 'w') as outfile:
            outfile.write(t)

    def find(self, kode):
        if not kode in self.data:
            return

        return self.data[kode]
    
    def insert(self, kode, value):
        if kode in self.data:
            return

        self.data[kode] = value
        self.write()
        return self.data[kode]

    def delete(self, kode):
        if not kode in self.data:
            return

        del self.data[kode]
        self.write()
        return
    
    def count(self, tipe):
        c = 0
        for karcis in self.data.keys():
            if karcis.startswith(tipe):
                c += 1

        return c
    
    def reset(self):
        self.data = {}
        self.write()
    
    def log(self, s):
        log = open('./data_log.csv', 'a')
        log.write(s + '\n')

data = Data()