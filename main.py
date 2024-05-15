from fastapi import FastAPI,HTTPException,status
from typing import Union
from pydantic import BaseModel,EmailStr
from pymongo import MongoClient
from typing import List

conn=MongoClient("mongodb+srv://ritiksinghis20:hashpassword1199@cluster0.dydw4.mongodb.net")
db=conn["database1"]
collection=db["users"]

app=FastAPI()

class User(BaseModel):
    name:str
    email:EmailStr
    number:int | None =None
    orders:list | None =None

@app.get("/")
def home():
    return {"Hello":"User"}

@app.post("/users/",response_model=User)
async def create_user(user:User):
    existing=collection.find_one({"email":user.email})
    
    if existing:
        raise HTTPException(status_code=status.HTTP_226_IM_USED,detail="User already exists")

    highest_user = collection.find_one(sort=[("user_id", -1)])
    if highest_user:
        user_id=highest_user["user_id"]+1
    else:
        user_id=1
    
    user_dict=user.dict()        
    user_dict["user_id"]=user_id
    inserted=collection.insert_one(user_dict)
    user_dict["_id"] = str(inserted.inserted_id)

    return user_dict

@app.get("/users/", response_model=List[User])
async def read_items():
    users = list(collection.find())
    return [{**user, "_id": str(user["_id"])} for user in users]

# @app.get("/users/{user_id}", response_model=User)
# async def read_user(user_id: int):
#     user = collection.find_one({"user_id": user_id})
#     if user:
#         return {**user}
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.get("/users/{user_id}",response_model=User)
async def read_user(user_id: int):
    user = collection.find_one({"user_id": user_id})
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.put("/users/{user_id}",response_model=User)
async def update_user(user_id:int,user:User):
    user_dict=user.dict()
    updated = collection.update_one({"user_id":user_id},{"$set": user_dict})

    if updated:
        return user
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    
@app.delete("/users/{user_id}")
async def delete_user(user_id:int,user:User):
    todel=collection.find_one_and_delete({"user_id":user_id})
    if todel:
        return {"Deleted":user_id}
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")