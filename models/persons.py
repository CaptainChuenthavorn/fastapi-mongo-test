# models class to convert mongodb object to json object with fastapi schema validation
def individual_serial(person)-> dict:
    return {
        "id": str(person["_id"]),
        "first_name": person["first_name"],
        "last_name": person["last_name"],
        "age": person["age"],
        "email": person["email"],
        "phone_number": person["phone_number"],
        "famous": person["famous"],
    }

def list_serial(persons)-> list:
    return [individual_serial(person) for person in persons]

def normalize_email(email: str)-> str:
    return email.lower()
