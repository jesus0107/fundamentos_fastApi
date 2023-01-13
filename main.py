#python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastApi
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()


#------ MODELS ------
class Person(BaseModel):
    name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

class Location(BaseModel):
    postal_code: int
    city:  str
    country: str

#------ PATHs ------
@app.get("/")
def home():
    return {"Hello": "World"}


#Request and response body
@app.post("/person/new")
def create_person(person: Person = Body()):
    return person


#Validations query parameters
@app.get("/person/detail")
def get_person(
    name: Optional[str] = Query(
            None, 
            min_length=1, 
            max_length=50,
            title="Person name",
            description="This is the person name. Its between 1 and 50 characters"
        ),
    age: int = Query(
            title="Person age", 
            description="This is the person age. Its required"
        )
):
    return {
        "name": name,
        "age": age
    }


#Validations Path parameters
@app.get("/person/detail/{person_id}")
def get_person(
    person_id: int = Path(
            gt=0,
            title="Person id", 
            description="Id needed to acces the person"
        )
):
    return {person_id: "Its exists"} 


# Validaciones request Body
@app.put("/person/{person_id}")
def update_person(
        person_id: int = Path(
            gt=0,
            title="Person ID",
            description=" This is the person ID"
    ), 
        person: Person = Body(),
        location: Location = Body()
    ):
    results = person.dict()
    results.update(location.dict())
    return results