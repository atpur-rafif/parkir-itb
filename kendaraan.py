from datetime import datetime
import math
import random
from typing import TypedDict
from data import data

def generateTiket():
    return ''.join(random.choice('0123456789ABCDEF') for _ in range(4))

def getLocalTime():
    return datetime.now().isoformat()

class Config(TypedDict):
    nama: str
    tipe: str
    kapasitas: str


class Kendaraan:
    pemasukan = 0
    jumlah = 0

    def __init__(self, config:Config):
        self.nama = config['nama']
        self.tipe = config['tipe']
        self.kapasitas = config['kapasitas'] 
        self.jumlah = data.count(self.tipe)

        if 'harga' in config:
            self.harga = config['harga']

        return
    
    def harga(self, *_):
        return 0
    
    def info(self):
        self.jumlah = data.count(self.tipe)
        return self.jumlah, self.pemasukan
    
    def masuk(self):
        if self.jumlah >= self.kapasitas:
            return

        self.jumlah += 1
        kode = generateTiket()
        while data.find(self.tipe + '-' + kode) != None:
            kode = generateTiket()
        data.insert(self.tipe + '-' + kode, getLocalTime())
        return kode

    def keluar(self, kode, plat):
        mulai = data.find(kode)
        if mulai == None:
            return

        harga = self.harga(mulai, getLocalTime())
        data.log(kode + ',' + plat + ',' + str(harga))
        data.delete(kode)
        self.jumlah -= 1
        self.pemasukan += harga
        return harga
        
def hitungHargaMobil(mulai, selesai):
    seconds = (datetime.fromisoformat(selesai) - datetime.fromisoformat(mulai)).seconds
    harga = 0
    if seconds / (24 * 3600) >= 1:
        harga = 30000
    else:
        harga = min(math.ceil(seconds / 3600), 10000) * 2000

    return harga

mobil = Kendaraan({
    'nama'      : 'Mobil',
    'tipe'      : 'A',
    'kapasitas' : 90,
    'harga'     : hitungHargaMobil
})

def hitungHargaMotor(mulai, selesai):
    return 2000

motor = Kendaraan({
    'nama'      : 'Motor',
    'tipe'      : 'C',
    'kapasitas' : 400,
    'harga'     : hitungHargaMotor
})