
#Python
from typing import Optional#=> trae un tipo de dato para crear tipado estático
from enum import Enum
from  jwt_manager import create_token, validate_token



#Pydantic => crear  modelos de las entidades
from pydantic import BaseModel
from pydantic import Field#import in order to validate models
from pydantic import EmailStr   
#from pydantic import SecretStr




#FastAPI
from fastapi import FastAPI
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from fastapi import Body,Query,Path, Form,Header,Cookie,UploadFile,File,Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer 
from fastapi.encoders import jsonable_encoder

#from SQL Alchemy and Modules
from  config.database import session, engine, Base
from models.movie import Movie as MovieModel

#From middlewares
from middle.ware.error_handler import ErrorHandler

#from routers

from routers.movie import movie_router






app=FastAPI()
app.title='My applicationi with FastApi'
#app.version('0.0.1')
# Indicating what middleware to use  across the entire application
app.add_middleware(ErrorHandler)
app.include_router(movie_router)


# creates the actual database file
Base.metadata.create_all(bind=engine)

#Models
##Class to validate tokens
class JWTBearer(HTTPBearer):
    
    async def __call__(self,request:Request):
        auth=await super().__call__(Request)
        validate_token(auth.credentials)
        if  data['email']!='admin@gmail.com':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Credenciales son invalidas')


class HairColor(Enum):
    white="white"
    brown='brown'
    black='black'
    blonde='blonde'
    red='red'


class User(BaseModel):
    email:str
    password:str
    
    
    
class Person(BaseModel):#validation is made 
    first_name:str=Field(
        ...,
        min_length=1,
        max_length=50,
                
        )
    password:str=Field(
        ...,
        min_length=8,
        )
    
    last_name:str=Field(
        ...,
        min_length=1,
        max_length=50,
    )   
    age:int=Field(
        ...,
        gt=0,
        le=115
        )
    hair_color:Optional[HairColor]=Field(default=None)
    is_married:Optional[bool]=Field(default=None)
    
        
    class Config:#Creando ejemplos de Request Body automáticos para probarlos, así no tiene que ponerlos en la documentación a cada rato
        schema_extra={
            "example":{
                'first_name':'Facundo',
                'last_name':'García Martoni',
                'age':21,
                'hair_color':'blond',
                'is_married':False
            }
    
            
            
        }
    
    
class Location(BaseModel):
    city:str
    state:str
    country:str


class PersonOut(BaseModel):
    pass
    
class LoginOut(BaseModel):
    username:str=Field(...,max_length=20,example='miguel')
    message:str=Field(default=' Login Successfully')
    
    
    
    

@app.get(path='/',
         status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def home():
    """
    ##Título de la función:Home
    ##Descripción de la función
    ##Parametros de la función:
    #Resultados que devuelve el path operation function
    
    """
    return {"Hello":'World'}

#Request and response body



@app.post(
    path='/person/new',
    response_model=PersonOut,
    status_code=status.HTTP_202_ACCEPTED,
    tags=['Persons'],
    summary='Create person in the app')

def create_person(person:Person=Body(...)):
    """
    Create Person
    This path creates a person in the app  and save  the information in the database

    Parameters:
    -Requests body Parameter:
        -**person:Person**-> A person model with 1st name, lastname, age, hair color and marital status.
        
    Returns a person model with 1stname, last lanem , age, hair color and marital status
    
    """
    db=Session()
    new_movie=MovieModel(**movie.dict())  # I can add each attribute as title=movie.title or as **movie.dict()
    db.add(new_movie)
    db.commit()
    return person

#validaciones query parameters
@app.get(path='person/detail',
         tags=['Persons'],
         deprecated=True)
def show_person(
    name:Optional[str]=Query(
        None,
        min_length=1,
        max_length=50),
        title='Person Name',
        description="This is the person name. It's between 1 and 50 characters",
        example='Rocío'):

    age:str=Query(
        ...,
        title='Person Age',
        description='This is the person age, it is required',
        example=25,
        
        )
    
    return{name:age}



#Validaciones: Path Parameters
persons=[1,2,3,4,5]


@app.get(
    path='/person/detail/{person_id}',
         tags=['Persons'])
def show_person(
    person_id:int=Path
    (...,
     gt=0,
     title="Person Id",
     description='This is the person id, it is required'
     )
    
    
):
    if person_id not in persons:
        raise  HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exit")
    return {person_id:'it exists!'}


@app.put('/person/{person_id}', tags=['Persons'])
def update_person(
    person_id:int=Path(
        ...,
        title='Person ID',
        description='This is the person ID',
        gt=0
          
    ),
    person:Person = Body(...),
    location: Location =Body(...)
        
    
):
    results=person.dict()
    results.updated(location.dict())
    return results
    #return person
    
#forms


@app.post('/login', tags=['Persons'],
response_model=LoginOut,
status_code=status.HTTP_200_OK
)
def login(username:str=Form(...), password:str=Form(...)):
    return LoginOut(username=username)


#Cookies and Headers Parameters

@app.post('/contact', 
          status_code=status.HTTP_200_OK, tags=['Interactions']
          )
def contact(
    first_name:str=Form(
        
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1),
    email:EmailStr=Form(...),
    message:str=Form(
        ...,
        min_length=20),
    user_agent:Optional[str]=Header(default=None),
    ads:Optional[str]=Cookie(default=None)
):
    return user_agent


@app.post('/post-image', tags=['Interactions'])
def post_image(image:UploadFile=File(...)):
    return{
        "Filename":image.filename,
        "Format":image.content_type,
        "Size(kb)":round(len(image.file.read())/1024,ndigits=2)
    }
    
    
    
#login
@app.post('/login', tags=['Auth'])
def login(user:User):
    if user.email=='admin@gmail.com' and user.password=='admin':
        token =create_token(user.dict())
        return JSONResponse(status_code=2000, content=token)   