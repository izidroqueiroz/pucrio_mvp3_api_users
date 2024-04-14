from typing import Optional, List, Union
from model import Session, ToiGetUser
from pydantic import BaseModel
    

class ToiGetUserSchema(BaseModel):
    """ Defines how a new User to be inserted should be represented. 
    """
    firstname: str = "Fulano"
    lastname: str = "de Tal"
    email: str = "fulano@gmail.com"
    password: str = "1234"
    role: str = "user"


class ToiGetUserSearchSchema(BaseModel):
    """ Defines how the search will be done.
    """
    email: str = "fulano@gmail.com"


class ToiGetUsersListSchema(BaseModel):
    """ Defines how a Users List will be presented.
    """
    users:List[ToiGetUserSchema]

def show_users(users: List[ToiGetUser], session: Session):
    """ Returns a List of Users, using UserViewSchema.
    """
    result = []
    for user in users:
        result.append(show_user(user, session))
    
    session.close()

    return {"users": result}


class ToiGetUserViewSchema(BaseModel):
    """ Defines how a User will be showed
    """
    id: int = 1
    firstname: str = "Fulano"
    lastname: str = "de Tal"
    email: str = "fulano@gmail.com"
    password: str = "1234"
    role: str = "user"

class ToiGetUserDeleteSchema(BaseModel):
    """ Defines information to delete a user
    """
    message: str
    email: str

def show_user(user: ToiGetUser, session: Session):
    """ Shows User using UserViewSchema
    """
    result = [{
        "id": user.id,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
        "password": user.password,
        "role": user.role
    }]

    session.close()
    return {"user": result}

