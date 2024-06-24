#create schema define the API that FastAPI uses to interact with the database.
from pydantic import BaseModel, Field, EmailStr
# phone data validation
# from pydantic_extra_types.phone_numbers import PhoneNumber
class Person(BaseModel):
    first_name: str = Field(...,min_length=2,max_length=100, title="First Name", description="First name of the person")
    last_name: str = Field(...,min_length=2,max_length=100, title="Last Name", description="Last name of the person")
    age: int = Field(...,gt=0,lt=150, title="Age", description="Age of the person")
    email: EmailStr = Field(..., title="Email", description="Email of the person")
    # phone_number: PhoneNumber = Field(..., title="Phone Number", description="Phone number of the person")
    phone_number: str = Field(..., title="Phone Number", description="Phone number of the person")
    famous: bool = Field(default=False, title="Famous", description="Is the person famous?")

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "age": 30,
                "email": "JohnDoe@gmail.com",
                "phone_number": "1234567890",
                "famous": False,
            }
        }