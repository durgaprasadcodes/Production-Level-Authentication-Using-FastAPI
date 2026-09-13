from pydantic import BaseModel,EmailStr,field_validator,Field

class RegistrationSchema(BaseModel):
    name:str = Field(min_length=3,max_length=200)
    email:EmailStr 
    password:str = Field(min_length=8)
    
class LoginSchema(BaseModel):
    email:EmailStr
    password:str 
    
class GoogleUser(BaseModel):
    id:str
    name:str
    email:EmailStr
    google_id:str
    picture:str