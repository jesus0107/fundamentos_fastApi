#python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastApi
from fastapi import FastAPI, Body

app = FastAPI()


#------ MODELS ------
class Person(BaseModel):
    name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


#------ PATHs ------
@app.get("/")
def home():
    return {"Hello": "World"}

#Request and response body

@app.post("/person/new")
def create_person(person: Person = Body()):
    return person