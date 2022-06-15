from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .OAuth import Generate_Access_Token, get_current
from .utils import Hashing_Password, verify_password
from .models import Data_Table
from . import models
from .database import engine, get_db
from .schemas import User_Request, User_Response
from fastapi.security import OAuth2PasswordBearer


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def Hello_World():
    return "Hello World!"


@app.post("/create_user", response_model=User_Response)
def Create_User(request: User_Request, db: Session = Depends(get_db)):
    request.password = Hashing_Password(request.password)
    user = Data_Table(**request.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/get_all_users", response_model=List[User_Response])
def Get_All_Feed(db: Session = Depends(get_db), current_user=Depends(get_current)):
    Existing_Users = db.query(Data_Table).all()
    return Existing_Users


@app.get("/get_one_user/{id}", response_model=User_Response)
def Get_One_User(id: int, db: Session = Depends(get_db)):
    Particular_User = db.query(Data_Table).filter(id == Data_Table.id)
    User = Particular_User.first()
    if not User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id:{id} does not exists",
        )

    return Particular_User


@app.delete("/delete_user/{id}")
def Delete_User(
    id: int, db: Session = Depends(get_db), current_user=Depends(get_current)
):
    User = db.query(Data_Table).filter(id == Data_Table.id)
    User.delete()
    db.commit()
    return "deleted successfully"


@app.put("/update_user/{id}", response_model=User_Response)
def Update_Username(
    id: int,
    request: User_Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current),
):
    User = db.query(Data_Table).filter(id == Data_Table.id)
    Update_User = User.first()
    request.password = Hashing_Password(request.password)
    User.update(request.dict())
    db.commit()
    db.refresh(Update_User)
    return Update_User


@app.post("/login")
def Authentication_User(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    User = db.query(Data_Table).filter(request.username == Data_Table.email)
    User_One = User.first()
    if not User:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials"
        )
    if not verify_password(request.password, User_One.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid credentials"
        )
    token = Generate_Access_Token({"id": User_One.id})
    return {"access_token": token, "token_type": "bearer"}
