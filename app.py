from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask import redirect
from flask import request


from model import Session, ToiGetUser
from schemas import *


info = Info(title="ToiGet Users API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# definindo tags
home_tag = Tag(name="Documentation", description="Swagger Documentation")
user_tag = Tag(name="ToiGet User", description="Insert, view and delete ToiGet users")


@app.get('/', tags=[home_tag])
def home():
    """ Redirects to /openapi/swagger - Swagger Documentation
    """
    return redirect('/openapi/swagger')


@app.post('/user', tags=[user_tag],
          responses={"200": ToiGetUserViewSchema, "409": ErrorSchema, "400": ErrorSchema, "422": ErrorSchema})
def add_user(form: ToiGetUserSchema):
    """ Insert a user

    Returns user.
    """

    user = ToiGetUser(
        firstname=form.firstname,
        lastname=form.lastname,
        email=form.email,
        password=form.password,
        role=form.role)

    try:
        session = Session()
        # add a user
        session.add(user)
        session.commit()
        return show_user(user, session), 200
    
    except IntegrityError as e:
        error_msg = ToiGetUser.User_Error(str(e.orig))
        return {"message": error_msg}, 409

    except Exception as e:
        # Unexpected error
        print(e)
        error_msg = "Unexpected error."
        return {"message": error_msg}, 400


@app.get('/users', tags=[user_tag],
         responses={"200": ToiGetUsersListSchema, "404": ErrorSchema})
def get_users():
    """ Get all users

    Returns a list of all users.
    """
    session = Session()
    users = session.query(ToiGetUser).all()

    if not users:
        # there is no users
        return {"users": []}, 200
    else:
        # returns users list
        users_list = []
        for user in users: 
            users_list.append(user)
        return show_users(users_list, session), 200

@app.get('/user', tags=[user_tag],
         responses={"200": ToiGetUserViewSchema, "404": ErrorSchema})
def get_user(query: ToiGetUserSearchSchema):
    """ Get a user using email

    Returns user
    """
    email = query.email

    session = Session()
    # get the user
    user = session.query(ToiGetUser).filter(ToiGetUser.email == email).first()

    if not user:
        # if user not found
        error_msg = "User not found."
        return {"message": error_msg}, 404
    else:
        # returns user
        return show_user(user, session), 200


@app.delete('/user', tags=[user_tag],
            responses={"200": ToiGetUserDeleteSchema, "404": ErrorSchema})
def del_user(query: ToiGetUserSearchSchema):
    """ Delete a user using email

    Returns delete confirmation
    """
    email = query.email

    session = Session()
    # delete a user
    user = session.query(ToiGetUser).filter(ToiGetUser.email == email).first()

    if not user:
        # if user not found
        error_msg = "User not found."
        return {"message": error_msg}, 404
    else:
        count = session.query(ToiGetUser).filter(ToiGetUser.id == user.id).delete()
        session.commit()

    session.close()

    if count:
        # returns delete confirmation
        return {"message": "User has been deleted.", "id": user.id}
    else:
        # if user not found
        error_msg = "User not found."
        return {"message": error_msg}, 404
