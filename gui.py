from tkinter import *
from typing import List
from kendaraan import Kendaraan, mobil, motor
from data import data

class PalangMasuk(Toplevel):
    def __init__(self, master, jenis:Kendaraan):
        super().__init__(master)

        self.title("Masuk")
        self.jenis = jenis

        self.geometry("220x50")
        self.varKode = StringVar(master)

        Button(self, text=f"Ambil Karcis {jenis.nama}", command=self.printTiket).pack()
        Entry(self, textvariable=self.varKode, state='readonly').pack()
    
    def printTiket(self):
        kode = self.jenis.masuk()
        if kode == None:
            self.varKode.set("Kapasitas penuh")
        else:
            self.varKode.set(kode)
        return 0

class PalangKeluar(Toplevel):
    def __init__(self, master, kendaraan:List[Kendaraan]):
        super().__init__(master)

        self.title("Keluar")
        self.geometry("220x200")

        self.kendaraan = {}
        for jenis in kendaraan:
            self.kendaraan[f"({jenis.tipe}) {jenis.nama}"] = jenis

        self.jenis = kendaraan[0]
        self.varJenis = StringVar(self, kendaraan[0].nama)
        self.varJenis.trace_add('write', self.gantiTipe)

        OptionMenu(self, self.varJenis, *[nama for nama in self.kendaraan.keys()]).pack()

        self.varKode = StringVar(self)
        self.varPlat = StringVar(self)

        Label(self, text="Nomor parkir: ").pack()
        self.inputParkir = Entry(self, textvariable=self.varKode)
        self.inputParkir.pack()

        Label(self, text="Plat nomor:").pack()
        Entry(self, textvariable=self.varPlat).pack()

        Button(self, command=self.keluar, text="Keluar").pack()
        Button(self, command=self.bayar, text="Bayar").pack()

        self.infoLabel = Label(self, text="")
        self.infoLabel.pack()

    def keluar(self):
        harga = self.jenis.keluar(self.jenis.tipe + "-" + self.varKode.get(), self.varPlat.get())
        if harga == None:
            self.info("Karcis tidak ditemukan")
        else:
            self.info(f"Rp{harga}")
    
    def bayar(self):
        self.info("")
        self.varKode.set("")
        self.varPlat.set("")
        self.inputParkir.focus()

    def gantiTipe(self, *_):
        self.jenis = self.kendaraan[self.varJenis.get()]

    def info(self, text):
        self.infoLabel.configure(text=text)

class Info(Frame):
    def __init__(self, master, jenis:Kendaraan):
        super().__init__(master)
        Label(self, text=jenis.nama).pack()

        self.jenis = jenis
        self.varKapasitas = StringVar()
        self.varPemasukan = StringVar()

        Label(self, text=f"Jumlah: ({jenis.kapasitas})").pack()
        Entry(self, textvariable=self.varKapasitas, state="readonly").pack()
        Label(self, text="Pemasukan").pack()
        Entry(self, textvariable=self.varPemasukan, state="readonly").pack()
    
    def refresh(self):
        k, p = self.jenis.info()
        self.varKapasitas.set(k)
        self.varPemasukan.set(p)
    
def GUI():
    root = Tk()
    root.title("Info")
    root.geometry("200x260")
    kendaraan = [motor, mobil]

    info = [Info(root, jenis) for jenis in kendaraan]
    for i in info:
        i.pack()
    
    def refreshInfo():
        for i in info:
            i.refresh()
    Button(root, text="Refresh", command=refreshInfo).pack()
    Button(root, text="Reset", command= lambda : data.reset()).pack()

    PalangKeluar(root, kendaraan)
    PalangKeluar(root, kendaraan)
    PalangMasuk(root, motor)
    PalangMasuk(root, mobil)

    root.mainloop()
