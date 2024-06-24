# Create FASTAPI CRUD with mongodb
from fastapi import FastAPI, HTTPException,APIRouter
from schema.schema import Person
from models.persons import individual_serial, list_serial, normalize_email
from config.database import collection_name
from bson import ObjectId
from bson import json_util
import json

router = APIRouter()

#POST Request Method 3 case 1.happycase checkschema validation 2. duplicate required field check with mongodb database 3. errorcase checkschema validation
@router.post("/persons",status_code=201)
async def create_person(person: Person):
    # Check if person schema is valid
    if not person.model_validate(person.model_dump()):
        raise HTTPException(status_code=400, detail="Invalid person schema")
    # Check if required fields are not duplicate in the database
    if collection_name.find_one({"email": person.email}) or collection_name.find_one({"phone_number": person.phone_number}):
        raise HTTPException(status_code=400, detail="Email or Phone Number already exists")
    # Insert the person into the database
    person_data = person.model_dump()
    person_id = collection_name.insert_one(person_data).inserted_id
    person_data = json.loads(json_util.dumps(person_data))
    # return 201 created status code and body that include the person_id and person body
    return {"status": 201, "message": "Person created", "person": person_data}

#GET Request Method 3 case 1.happycase get all person data 2. errorcase get all person data
@router.get("/persons")
def get_all_person():
    # Get all person data from the database
    all_person = collection_name.find()
    # Check if there are any person data in the database
    if all_person:
        all_person = list_serial(all_person)
        # return {"status": 200, "message": "All person data", "person": all_person}
        return all_person
    #return 404 not found status code and body that include the message
    raise HTTPException(status_code=404, detail="No person data found")

#DELETE METHOD
@router.delete("/persons/{person_id}")
def delete_person(person_id: str):
    # Check if the person_id is valid
    if not ObjectId.is_valid(person_id):
        raise HTTPException(status_code=400, detail="Invalid person_id")
    # Check if the person_id exists in the database
    person = collection_name.find_one({"_id": ObjectId(person_id)})
    if person:
        # Delete the person from the database
        collection_name.delete_one({"_id": ObjectId(person_id)})
        #return 200 ok status code and body that include the message
        return {"status": 200, "message": "Person deleted"}
    #return 404 not found status code and body that include the message
    raise HTTPException(status_code=404, detail="Person not found")

#PUT METHOD
@router.put("/persons/{person_id}")
def update_person(person_id: str, person: Person):
    # Check if the person_id is valid
    if not ObjectId.is_valid(person_id):
        raise HTTPException(status_code=400, detail="Invalid person_id")
    # Check if person schema is valid
    if not person.model_validate(person.model_dump()):
        raise HTTPException(status_code=400, detail="Invalid person schema")
    # Check if the person_id exists in the database
    person_data = collection_name.find_one({"_id": ObjectId(person_id)})
    if person_data:
        # Check if the email or phone_number already exists in the database
        if collection_name.find_one({"email": person.email}) or collection_name.find_one({"phone_number": person.phone_number}):
            raise HTTPException(status_code=400, detail="Email or Phone Number already exists")
        # Update the person in the database
        collection_name.update_one({"_id": ObjectId(person_id)}, {"$set": person.model_dump()})
        #return 200 ok status code and body that include the message
        return {"status": 200, "message": "Person updated"}
    #return 404 not found status code and body that include the message
    raise HTTPException(status_code=404, detail="Person not found")