from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr

from src.database.models import UserRole


class ContactModel(BaseModel):
    """
    Model for creating or updating a contact.

    Attributes:
        name: contact's first name (minimum 2 characters, maximum 50 characters)
        surname: contact's last name (minimum 2 characters, maximum 50 characters)
        email: contact's email (minimum 7 characters, maximum 100 characters)
        phone: contact's phone number (minimum 7 characters, maximum 20 characters)
        birthday: contact's date of birth
        info: additional information about the contact (optional)
    """

    name: str = Field(min_length=2, max_length=50)
    surname: str = Field(min_length=2, max_length=50)
    email: EmailStr = Field(min_length=7, max_length=100)
    phone: str = Field(min_length=7, max_length=20)
    birthday: date
    info: Optional[str] = None


class ContactResponse(ContactModel):
    """
    Model for the response when retrieving a contact from the database.

    Attributes:
        id: unique identifier of the contact
        created_at: date and time of the contact's creation
        updated_at: date and time of the contact's last update (optional)
    """

    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    """
    Model for representing a user.

    Attributes:
        id: unique identifier of the user
        username: username of the user
        email: user's email
        avatar: URL to the user's avatar
        role: the user's role (e.g., administrator or user)
    """

    id: int
    username: str
    email: str
    avatar: str
    role: UserRole
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """
    Model for creating a new user.

    Attributes:
        username: username of the user
        email: user's email
        password: user's password (minimum 4 characters, maximum 128 characters)
        role: the user's role (e.g., administrator or user)
    """

    username: str
    email: str
    password: str = Field(min_length=4, max_length=128)
    role: UserRole


class Token(BaseModel):
    """
    Model for returning an access token.

    Attributes:
        access_token: access token
        token_type: token type (e.g., Bearer)
    """

    access_token: str
    token_type: str


class RequestEmail(BaseModel):
    """
    Model for requesting an email to reset the password.

    Attribute:
        email: user's email
    """

    email: EmailStr


class ResetPassword(BaseModel):
    """
    Model for resetting a password.

    Attributes:
        email: user's email
        password: new password for the user (minimum 4 characters, maximum 128 characters)
    """

    email: EmailStr
    password: str = Field(min_length=4, max_length=128, description="New password")
