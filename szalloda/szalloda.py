from abc import ABC, abstractmethod
from datetime import datetime

class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar):
        super().__init__(szobaszam, ar)

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar):
        super().__init__(szobaszam, ar)

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = {}
    
    def add_szoba(self, szoba):
        self.szobak.append(szoba)
    
    def foglal_szoba(self, szobaszam, datum):
        if datum < datetime.today().date():
            return "A választott dátum a múltban van."
        if szobaszam not in [szoba.szobaszam for szoba in self.szobak]:
            return "Nem létező szobaszám."
        if datum in self.foglalasok and szobaszam in self.foglalasok[datum]:
            return "A szoba már foglalt ezen a napon."
        self.foglalasok.setdefault(datum, []).append(szobaszam)
        return f"Foglalás rögzítve. Ár: {next(szoba.ar for szoba in self.szobak if szoba.szobaszam == szobaszam)}"
    
    def lemond_foglalas(self, szobaszam, datum):
        if datum not in self.foglalasok or szobaszam not in self.foglalasok[datum]:
            return "Nem létező foglalás."
        self.foglalasok[datum].remove(szobaszam)
        if not self.foglalasok[datum]:
            del self.foglalasok[datum]
        return "Foglalás lemondva."
    
    def listaz_foglalasok(self):
        if not self.foglalasok:
            return "Nincsenek foglalások."
        return "\n".join(f"{datum}: {szobak}" for datum, szobak in self.foglalasok.items())

class FelhasznaloiInterfesz:
    def __init__(self, szalloda):
        self.szalloda = szalloda
        self.folytat = True
    
    def indit(self):
        while self.folytat:
            print("Üdvözlünk a szállodában! Válaszd ki a műveletet:")
            print("1. Foglalás\n2. Lemondás\n3. Foglalások listázása\n4. Kilépés\n5. Program újrainditása")
            valasztas = input("Kérem válasszon egy opciót: ")
            if valasztas == "1":
                self.kezel_foglalas()
            elif valasztas == "2":
                self.kezel_lemondas()
            elif valasztas == "3":
                print(self.szalloda.listaz_foglalasok())
            elif valasztas == "4":
                self.folytat = False
            

    def kezel_foglalas(self):
        szobaszam = input("Szobaszám: ")
        datum = input("Dátum (YYYY-MM-DD): ")
        try:
            datum = datetime.strptime(datum, '%Y-%m-%d').date()
        except ValueError:
            print("Hibás dátumformátum.")
            return
        print(self.szalloda.foglal_szoba(szobaszam, datum))

    def kezel_lemondas(self):
        szobaszam = input("Szobaszám a lemondáshoz: ")
        datum = input("Dátum (YYYY-MM-DD) a lemondáshoz: ")
        try:
            datum = datetime.strptime(datum, '%Y-%m-%d').date()
        except ValueError:
            print("Hibás dátumformátum.")
            return
        print(self.szalloda.lemond_foglalas(szobaszam, datum))

if __name__ == "__main__":
    szalloda = Szalloda("Budapest Hotel")
    szalloda.add_szoba(EgyagyasSzoba("101", 10000))
    szalloda.add_szoba(KetagyasSzoba("102", 15000))
    szalloda.add_szoba(EgyagyasSzoba("103", 12000))

    felhasznaloi_interfesz = FelhasznaloiInterfesz(szalloda)
    felhasznaloi_interfesz.indit()