from abc import ABC, abstractmethod
from tkinter import Tk, Label, Button, Entry, StringVar, Frame, OptionMenu, messagebox
import datetime


# Szoba osztályok
class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

    @abstractmethod
    def leiras(self):
        pass


class EgyagyasSzoba(Szoba):
    def leiras(self):
        return f"Egyágyas szoba, szobaszám: {self.szobaszam}, ár: {self.ar} Ft"


class KetagyasSzoba(Szoba):
    def leiras(self):
        return f"Kétágyas szoba, szobaszám: {self.szobaszam}, ár: {self.ar} Ft"


# Szálloda osztály
class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = {}
        self.foglalasok = {}

    def szoba_hozzaadas(self, szoba):
        self.szobak[szoba.szobaszam] = szoba

    def foglalas(self, szobaszam, datum):
        if datum < datetime.datetime.now().date():
            raise ValueError("A múltba nem lehet szobát foglalni. Válasszon másik dátumot.")
        if szobaszam in self.foglalasok and datum in self.foglalasok[szobaszam]:
            raise ValueError("A szoba ezen a napon már foglalt. Válasszon másik dátumot.")
        if szobaszam not in self.szobak:
            raise ValueError("A megadott szobaszám nem létezik a szállodában.")
        self.foglalasok.setdefault(szobaszam, []).append(datum)
        return self.szobak[szobaszam].ar

    def foglalas_torles(self, szobaszam, datum):
        if szobaszam in self.foglalasok and datum in self.foglalasok[szobaszam]:
            self.foglalasok[szobaszam].remove(datum)
            if not self.foglalasok[szobaszam]:
                del self.foglalasok[szobaszam]
        else:
            raise ValueError("A megadott foglalás nem található. Ellenőrizze a szobaszámot és a dátumot.")

    def foglalasok_listazasa(self):
        return [(szobaszam, datum) for szobaszam, datums in self.foglalasok.items() for datum in datums]


# GUI megvalósítása
class SzallodaApp:
    def __init__(self, master):
        self.master = master
        master.title("Szálloda Foglalási Rendszer")

        # Háttérszín
        master.geometry("400x300")


        # Szálloda létrehozása és szobák hozzáadása
        self.szalloda = Szalloda("Best Hotel******")
        self.szalloda.szoba_hozzaadas(EgyagyasSzoba(101, 15000))
        self.szalloda.szoba_hozzaadas(KetagyasSzoba(102, 20000))
        self.szalloda.szoba_hozzaadas(EgyagyasSzoba(103, 18000))

        # Kezdő foglalások hozzáadása
        try:
            self.szalloda.foglalas(101, datetime.date(2024, 5, 10))
            self.szalloda.foglalas(102, datetime.date(2024, 5, 11))
            self.szalloda.foglalas(103, datetime.date(2024, 5, 12))
            self.szalloda.foglalas(101, datetime.date(2024, 5, 13))
            self.szalloda.foglalas(102, datetime.date(2024, 5, 14))
        except ValueError as e:
            messagebox.showerror("Hiba", str(e))

        # Widgetek elhelyezése egy közös keretben
        self.control_frame = Frame(master)
        self.control_frame.pack(pady=10)

        self.datum_var = StringVar(master)
        self.datum_label = Label(self.control_frame, text="Dátum (éééé-hh-nn):")
        self.datum_entry = Entry(self.control_frame, textvariable=self.datum_var)

        self.szoba_var = StringVar(master)
        self.szoba_var.set(list(self.szalloda.szobak.keys())[0])
        self.szoba_menu = OptionMenu(self.control_frame, self.szoba_var, *self.szalloda.szobak.keys())

        self.foglalas_button = Button(self.control_frame, text="Foglalás", command=self.foglalas)
        self.lemondas_button = Button(self.control_frame, text="Lemondás", command=self.lemondas)
        self.listazas_button = Button(self.control_frame, text="Listázás", command=self.listazas)

        # Kilépés gomb elkülönített keretben
        self.exit_frame = Frame(master)
        self.exit_frame.pack(pady=20)
        self.kilepes_button = Button(self.exit_frame, text="Kilépés", command=master.quit)
        self.kilepes_button.pack()

        # Widgetek elhelyezése a vezérlő keretben
        self.datum_label.pack()
        self.datum_entry.pack()
        self.szoba_menu.pack()
        self.foglalas_button.pack(side="left", padx=5, pady=5)
        self.lemondas_button.pack(side="left", padx=5, pady=5)
        self.listazas_button.pack(side="left", padx=5, pady=5)

    def foglalas(self):
        datum = self.datum_var.get()
        try:
            parsed_datum = datetime.datetime.strptime(datum, "%Y-%m-%d").date()
            ar = self.szalloda.foglalas(int(self.szoba_var.get()), parsed_datum)
            messagebox.showinfo("Foglalás", f"Foglalás sikeres. Ár: {ar} Ft")
        except ValueError as e:
            if "does not match format" in str(e):
                messagebox.showerror("Hiba", "A dátum formátuma helytelen. Kérjük, használja az éééé-hh-nn formátumot.")
            else:
                messagebox.showerror("Hiba", str(e))

    def lemondas(self):
        datum = self.datum_var.get()
        try:
            parsed_datum = datetime.datetime.strptime(datum, "%Y-%m-%d").date()
            self.szalloda.foglalas_torles(int(self.szoba_var.get()), parsed_datum)
            messagebox.showinfo("Lemondás", "Foglalás sikeresen törölve.")
        except ValueError as e:
            if "does not match format" in str(e):
                messagebox.showerror("Hiba", "A dátum formátuma helytelen. Kérjük, használja az éééé-hh-nn formátumot.")
            else:
                messagebox.showerror("Hiba", str(e))

    def listazas(self):
        foglalasok = self.szalloda.foglalasok_listazasa()
        foglalasok_str = "\n".join(f"{szobaszam} dátum: {datum}" for szobaszam, datum in foglalasok)
        messagebox.showinfo("Foglalások listája", foglalasok_str)


# A GUI alkalmazás indítása
root = Tk()
app = SzallodaApp(root)
root.mainloop()
