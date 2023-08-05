from pydantic import BaseModel

class UserPostgres(BaseModel):
    first_name: str
    password: str
    email: str
    phone: str

# MongoDB Model
class UserProfile(BaseModel):
    profile_picture: str

# Combined Model
class UserRegistration(UserPostgres, UserProfile):
    full_name: str