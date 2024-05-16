from fastapi import FastAPI,HTTPException,status,UploadFile
from typing import Union
from pydantic import BaseModel,EmailStr
from typing import List
from database.connection import collection,itemcollection
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add the URL of your frontend
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class User(BaseModel):
    name:str
    email:EmailStr
    number:int | None =None
    orders:list | None =None
    
class Item(BaseModel):
    name:str
    price:int
    description:str
    
class ItemUpload(Item):
    image: UploadFile |  None
    tags:List[str] = []


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
async def read_users():
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

@app.post("/items",response_model=Item)
async def add_item(item:Item):
    item_dict=item.dict()
    
    highest_item = itemcollection.find_one(sort=[("item_id", -1)])
    if highest_item:
        item_id=highest_item["item_id"]+1
    else:
        item_id=1000
    
    item_dict["item_id"]=item_id
    insert=itemcollection.insert_one(item_dict)
    item_dict["_id"] = str(insert.inserted_id)

    return item_dict

@app.get("/items",response_model=List[Item])
async def get_items():
    items = list(itemcollection.find())
    return items

@app.get("/items/{item_id}",response_model=Item)
async def get_item(item_id:int):
    item=itemcollection.find_one({"item_id":item_id})
    
    if item:
        return item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item Not Found")
    

@app.put("/items/{item_id}",response_model=Item)
async def update_item(item_id:int,item:Item):
    item_dict=item.dict()
    updated = itemcollection.update_one({"item_id":item_id},{"$set": item_dict})

    if updated:
        return item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item Not Found")

@app.delete("/items/{item_id}")
async def delete_item(item_id:int):
    todel=itemcollection.find_one_and_delete({"item_id":item_id})      
    if todel:
        return {"Deleted":item_id}
    
    else:
        raise HTTPException 