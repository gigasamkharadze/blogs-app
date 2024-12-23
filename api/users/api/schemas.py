from ninja import Schema
from typing import Optional

class TokenSchema(Schema):
    access_token: str
    token_type: str

class AuthSchema(Schema):
    username: str
    password: str

class RegisterSchema(Schema):
    username: str
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserUpdateSchema(Schema):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class PasswordChangeSchema(Schema):
    current_password: str
    new_password: str
    confirm_password: str

class PasswordResetRequestSchema(Schema):
    email: str

class PasswordResetConfirmSchema(Schema):
    token: str
    new_password: str
    confirm_password: str

class UserProfileSchema(Schema):
    id: int
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    profile_image: Optional[str]

class ErrorSchema(Schema):
    message: str

class SuccessSchema(Schema):
    message: str