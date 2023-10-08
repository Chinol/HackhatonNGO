from typing import Optional, List
from sqlmodel import Field, SQLModel, create_engine, Session
import json

json_file_path = 'C:\\Users\\marcz\\Desktop\\Hackaton2023\\HackhatonNGO\\database\\wynik.json'

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

class UserSQLModel(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    login: str  
    password: str

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)




def import_data():
    with open(json_file_path, "r", encoding="utf-8") as file:
        list = json.load(file)
        for dict in list:
            if dict["name"] != None:  
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

            #for klucz, wartosc in ngo_dict.items():
                #if "\ufffd" in wartosc:
                    #ngo_dict[klucz] = wartosc.replace("\ufffd", 'l')

            ngo = NGOSQLModel(**ngo_dict)
            with Session(engine) as session:
                session.add(ngo)
                session.commit()

            
