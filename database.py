from typing import Optional, List
from sqlmodel import Field, SQLModel, create_engine, Session, select
from sqlalchemy import ARRAY, String, Column
import pandas as pd 
import pypyodbc

excel = 'C:\\Users\\marcz\\Desktop\\Hackaton2023Płock\\HackhatonNGO\\database\\NGO.xlsx'

DATABASE_URL = "C:/Users/marcz/Desktop/Hackaton2023Płock/HackhatonNGO/database/db.sqlite3"
engine = create_engine(f'sqlite:///{DATABASE_URL}', echo=True)
session = Session(engine)

Base = declarative_base()

class NGOSQLModel(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default = None)
    city: Optional[str] = Field(default = None)
    street: Optional[str] = Field(default = None)
    krs: Optional[str] = Field(default = None)
    phone: Optional[str] = Field(default = None)
    op: Optional[str] = Field(default = None) 
    status: Optional[str] = Field(default = None)
    dzial: Optional[str] = Field(default = None)
    number: Optional[str] = Field(default = None)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)




def import_data():
# 6. Utwórz sesję SQLModel
    with Session(engine) as session:
    # 7. Wczytaj dane z pliku XLSX przy użyciu Pandas
        excel_file = pd.read_excel(excel, sheet_name='Zarejestrowane organizacje',skiprows=1,usecols="B:J")

        for _, row in excel_file.iterrows():
            data = SQLModel(**row.to_dict())
            session.add(data)
            session.commit()
            '''
            ngo_data = {
                "name": row.get("Nazwa"),
                "city": row.get("Miejscowość"),
                "street": row.get("Ulica"),
                "krs": row.get("KRS"),
                "phone": row.get("Telefon"),
                "op": row.get("Osobowa upoważniona"),
                "status": row.get("Forma prawna"),
                "dzial": row.get("Wiodący zakres działania"),
                "number": row.get("Zakres numer")
            }
    # {'fail', 'replace', 'append'}
            #df_data.to_sql('ngosqlmodel', engine, if_exists='append', index=False)
            '''

            


create_db_and_tables()
import_data()