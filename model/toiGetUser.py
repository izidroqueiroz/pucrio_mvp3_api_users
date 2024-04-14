from sqlalchemy import Column, String, Integer, DateTime, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class ToiGetUser(Base):
    __tablename__ = 'user'
    __table_args__ = (
        UniqueConstraint('email', name='email'),
        CheckConstraint("role IN ('admin','user')", name='check_role'),
    )

    id = Column("pk_user", Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(256))
    password = Column(String(50))
    # role: 'admin' or 'user'
    role = Column(String(10))
    insertDate = Column(DateTime, default=datetime.now())

    def __init__(self, firstname:str, lastname:str, 
                 email:str, password:str, role:str,
                 insertDate:Union[DateTime, None] = None):
        """
        Insert a User

        Arguments:
            firstname: first name of the user
            lastname: last name of the user
            email: email of the user
            password: password of the user
            role: role of the user ('admin' or 'user')
            insertDate: insert date of the user
        """
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.role = role

        # if not informed, it will be the current date
        if insertDate:
            self.insertDate = insertDate

    def User_Error(error_type:str): 
        if error_type == "UNIQUE constraint failed: user.email":
            error_msg = "User already exists with this email."
        elif error_type == "CHECK constraint failed: check_role":
            error_msg = "Role must be 'admin' or 'user'."
        else:
            error_msg = "Unexpected error : " + error_type
        return error_msg

