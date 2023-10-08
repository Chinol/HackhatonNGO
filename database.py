from typing import Optional, List
from sqlmodel import Field, SQLModel, create_engine, Session
import json
import sqlite3
import random

json_file_path = 'C:\\Users\\marcz\\Desktop\\Hackaton2023\\HackhatonNGO\\database\\wynik3.json'

DATABASE_URL = "C:/Users/marcz/Desktop/Hackaton2023/HackhatonNGO/database/db.sqlite3"
engine = create_engine(f'sqlite:///{DATABASE_URL}', echo=True)
session = Session(engine)

class NGOSQLModel(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default = None)
    miasto: Optional[str] = Field(default = None)
    street: Optional[str] = Field(default = None)
    krs: Optional[str] = Field(default = None)
    phone: Optional[str] = Field(default = None)
    op: Optional[str] = Field(default = None) 
    status: Optional[str] = Field(default = None)
    dzial: Optional[str] = Field(default = None)
    numer: Optional[str] = Field(default = None)
    logo: Optional[str] = Field(default = None)
    kategoria: Optional[str] = Field(default = None)

class UserSQLModel(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    login: str  
    password: str

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def add_column():
    conn = sqlite3.connect('database\\db.sqlite3')
    cursor = conn.cursor()

    # Wykonaj polecenie ALTER TABLE, aby dodać nową kolumnę
    cursor.execute('ALTER TABLE ngosqlmodel ADD COLUMN kategoria TEXT')

    # Zatwierdź zmiany
    conn.commit()

    # Zamknij połączenie z bazą danych
    conn.close()

def dodaj_logo():
    conn = sqlite3.connect('database\\db.sqlite3')
    cursor = conn.cursor()
    nazwa_do_wyszukania = 'Akademickie Stowarzyszenie Ambitni w Działaniu'
    cursor.execute('SELECT id FROM ngosqlmodel WHERE name = ?', (nazwa_do_wyszukania,))
    result = cursor.fetchone()

    if result:
        wpis_id = result[0]

        # Aktualizuj logo dla znalezionego wpisu
        nowa_sciezka_do_pliku = 'C:/Users/marcz/Desktop/Hackaton2023/HackhatonNGO/res/akademickie.jpg'
        cursor.execute('UPDATE ngosqlmodel SET logo = ? WHERE id = ?', (nowa_sciezka_do_pliku, wpis_id))
        conn.commit()
        print(f'Zaktualizowano logo dla wpisu o nazwie "{nazwa_do_wyszukania}"')

    else:
        print(f'Nie znaleziono wpisu o nazwie "{nazwa_do_wyszukania}"')

# Zamknij połączenie z bazą danych
    conn.close()

def wylosuj_kategorie():
    kategorie = ["ekologia", "humanitaryzm", "edukacja"]

# Pobierz wszystkie rekordy z tabeli NGOModel
    rekordy = session.query(NGOSQLModel).all()

    # Zaktualizuj pole "kategoria" dla każdego rekordu losową wartością
    for rekord in rekordy:
        rekord.kategoria = random.choice(kategorie)

    # Zatwierdź zmiany w bazie danych
    session.commit()

    # Zamknij sesję
    session.close()

def import_data():
    with open(json_file_path, "r", encoding="utf-8") as file:
        list = json.load(file)
        
        for dict in list:
            if dict["name"] != "":  
                ngo_dict = {
                        "name": dict["name"],
                        "miasto": dict["miasto"], 
                        "street": dict["street"], 
                        "krs": dict["krs"], 
                        "phone": dict["phone"], 
                        "op": dict["op"],  
                        "status": dict["status"], 
                        "dzial": dict["dzial"], 
                        "numer": dict["numer"] 
                    }

            ngo = NGOSQLModel(**ngo_dict)
            with Session(engine) as session:
                session.add(ngo)
                session.commit()