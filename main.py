#python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field, EmailStr, HttpUrl

#FastApi
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, File, UploadFile

app = FastAPI()

#Enums
class HairColor(Enum):
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

#------ MODELS ------
class PersonBase(BaseModel):
    name: str = Field(min_length=1, max_length=50, example="Martha")
    last_name: str = Field(min_length=1, max_length=50, example="Patricia")
    age: int = Field(gt=17, lt=90, example="28")
    email: EmailStr = Field(example="martha@example.com")
    website_url: HttpUrl = Field(example="http://marthasite.com")
    hair_color: Optional[HairColor] = Field(default=None, example="brown")
    is_married: Optional[bool] = Field(default=None, example="True")

        # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Jesus",
    #             "last_name":  "Cruz",
    #             "age": 18,
    #             "email": "example@example.com",
    #             "website_url": "http://www.mysite.com",
    #             "hair_color": "black",
    #             "is_married": False
    #         }
    #     }

class Person(PersonBase):
    password: str = Field(min_length=8,  example="mypassword")


class PersonOut(PersonBase):
    pass

class LoginOut(BaseModel):
    username: str = Field(max_length=30, example="myusername")
    # password: str = Field(min_length=8)
    message = "Login Successfully"


class Location(BaseModel):
    postal_code: int = Field(gt=0)
    city:  str = Field(max_length=50)
    country: str = Field(max_length=50)

    class Config:
        schema_extra = {
            "example": {
                "postal_code": 12345,
                "city": "Guadalajara",
                "country": "Mexico"
            }
        }

#------ PATHs ------
@app.get(path="/", status_code=status.HTTP_200_OK, tags=["home"])
def home():
    return {"Hello": "World"}


#Request and response body
@app.post(
        path="/person/new", 
        response_model=PersonOut, 
        status_code=status.HTTP_201_CREATED,
        tags=["person"],
        summary="Create a new person in the app"
    )
def create_person(person: Person = Body()):
    """
    Create Person

    this path operation create a new person in the app and save the information in the database

    Parameters:
    - Request body parameter: 
        - ** person: Person ** -> A person model with first name, last name, age, hair color and marital status.

    Returns:
    - Person Model with first name, last name, age, hair color an marital status.
    """
    return person


#Validations query parameters
@app.get(path="/person/detail", status_code=status.HTTP_200_OK,tags=["person"], deprecated=True)
def get_person(
    name: Optional[str] = Query(
            None, 
            min_length=1, 
            max_length=50,
            title="Person name",
            description="This is the person name. Its between 1 and 50 characters",
            example="Jesus"
        ),
    age: int = Query(
            title="Person age", 
            description="This is the person age. Its required",
            example=23
        )
):
    return {
        "name": name,
        "age": age
    }


#Validations Path parameters
my_ids = [1,2,3,4,5]
@app.get(path="/person/detail/{person_id}", status_code=status.HTTP_200_OK, tags=["person"])
def get_person(
    person_id: int = Path(
            gt=0,
            title="Person id", 
            description="Id needed to acces the person",
            example=12
        )
):
    if person_id not in my_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Person not found"
        )

    return {person_id: "Its exists"} 


# Validaciones request Body
@app.put(path="/person/{person_id}", response_model=PersonOut, status_code=status.HTTP_200_OK,tags=["person"])
def update_person(
        person_id: int = Path(
            gt=0,
            title="Person ID",
            description=" This is the person ID",
            example=13
    ), 
        person: Person = Body(),
        location: Location = Body()
    ):
    results = person.dict()
    results.update(location.dict())
    return results

# ------ Form
@app.post(path="/login", status_code=status.HTTP_200_OK, response_model=LoginOut,tags=["person"])
def login( username: str = Form(), password: str = Form()):
    return LoginOut(username=username)

# ------ Cookies and headers parameters
@app.post(path="/contact", status_code=status.HTTP_200_OK, tags=["contact"])
def contact(
        first_name: str = Form(
            max_length=20, 
            min_length=3),
        last_name: str = Form(
            max_length=20, 
            min_length=3),
        email: EmailStr = Form(),
        message: str = Form(min_length=20),
        user_agent: Optional[str] = Header(default=None),
        ads: Optional[str] = Cookie(default=None)
    ):
    return user_agent


# ------------ files
@app.post(path="/upload-image", status_code=status.HTTP_200_OK,tags=["upload_files"])
def upload_image(image: UploadFile = File()):
    return {
        "file_name": image.filename,
        "content_type": image.content_type,
        "size": round(len(image.file.read())/1024, ndigits=2)
    }