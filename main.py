from fastapi import FastAPI, Response, Depends
from typing import Union, List
from models import NGOPydanticModel, NGOUserPydanticModel
from database import NGOSQLModel, engine, create_db_and_tables, UserSQLModel
from sqlmodel import Session, select
import sqlite3


app = FastAPI()

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()
    print("Aplikacja wystartowała")

def get_session():
    with Session(engine) as session:
        yield session

#Strona Powitalna
@app.get('/')
def hello_world():
    return 'To jest stronka z NGO i jest spoko. Można tu posprawdzać jakie są fajne NGO'

#Wyplucie wszystkim rekordów z bazy
@app.get('/NGO/', response_model=List[NGOPydanticModel])
def get_items(session: Session = Depends(get_session)):
    stmt = select(NGOSQLModel)
    result = session.exec(stmt).all()
    return result

#Wydobycie jednego itemu z bazy
@app.get('/NGO/{item_id}', response_model=Union[NGOPydanticModel, str])
def get_item_by_id(item_id: int, respone: Response, session: Session = Depends(get_session)):
    item = session.get(NGOSQLModel, item_id)
    if item is None:
        Response.status_code = 404
        return "Item not found"
    return item 

@app.get('/NGO/search/{search_text}')
def get_item_by_name(search_text: str, respone: Response, session: Session = Depends(get_session)):

    connection = sqlite3.connect('database\\db.sqlite3')
    cursor = connection.cursor()
    
    cursor.execute(f"""SELECT * FROM ngosqlmodel 
                   WHERE name LIKE '%{search_text}%'
                    OR miasto LIKE '%{search_text}%'
                    OR street LIKE '%{search_text}%'
                    OR krs LIKE '%{search_text}%'
                    OR phone LIKE '%{search_text}%'
                    OR op LIKE '%{search_text}%'
                    OR status LIKE '%{search_text}%'
                    OR dzial LIKE '%{search_text}%'
                    OR numer LIKE '%{search_text}%'
                """)
    
    search = cursor.fetchall()
    
    new_dict = {}
    final_list = [] 
    for item in search:
        final_list.append(dict({'name': item[1], 'miasto': item[2], 'street': item[3], 'krs': item[4], 'phone': item[5], 'op': item[6], 'status': item[7], 'dzial': item[8], 'numer': item[9]}))
    return final_list


#Dodaj nowy zabytek
@app.post('/NGO/', response_model=NGOPydanticModel, status_code=201)
def create_item(item: NGOSQLModel, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

#Update zabytku
@app.put('/NGO/{item_id}', response_model=Union[NGOPydanticModel, str])
def update_item(item_id: int, updated_item: NGOPydanticModel, respone: Response, session: Session = Depends(get_session) ):
    
    item = session.get(NGOSQLModel, item_id)

    if item is None:
        Response.status_code = 404
        return "Item not found"
    
    item_dict = updated_item.model_dump(exclude_unset = True)

    for key, val in item_dict.items():
        setattr(item, key, val)
    
    session.add(item)
    session.commit()
    session.refresh(item)

    return item 

#Usuń zabytek
@app.delete('/NGO/{item_id}')
def delete_item(item_id: int, respone: Response, session: Session = Depends(get_session)):
    item = session.get(NGOSQLModel, item_id)

    if item is None:
        Response.status_code = 404
        return "Item not found"

    session.delete(item)
    session.commit()
    return Response(status_code=200 )

#Create User
@app.post('/user-create/', response_model=NGOUserPydanticModel, status_code=201)
def user_create(item: UserSQLModel, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

#Login User
@app.get('/user-login/', response_model=str)
def get_items(login: str, passw: str, session: Session = Depends(get_session)):
    stmt = select(UserSQLModel).where(UserSQLModel.login == login).where(UserSQLModel.password == str)
    result = session.exec(stmt)
    if result is None:
        return "Uzytkownik nie zostal znaleziony"

    return f"Hej uzyszkodnik {login} zostal zalogowany"

@app.get('/image')
def get_image():
    text = str('C:/Users/marcz/Desktop/Hackaton2023/HackhatonNGO/res/jp.png') 
    return text 