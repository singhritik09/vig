from fastapi import FastAPI, HTTPException, status, UploadFile
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from database.connection import collection, itemcollection
from fastapi.middleware.cors import CORSMiddleware
import socket

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class User(BaseModel):
    name: str
    email: EmailStr
    number: Optional[int] = None
    orders: Optional[List[str]] = None

class Item(BaseModel):
    name: str
    price: int
    description: str

class ItemUpload(Item):
    image: Optional[UploadFile] = None
    tags: List[str] = []

def fetchDetails():
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)
    return str(hostname), str(host_ip)


@app.get("/")
def home_page():
    hostname,host_ip=fetchDetails()
    return {"Hello": "User", "hostname": hostname, "host_ip": host_ip}

@app.post("/users/", response_model=User)
async def create_user(user: User):
    existing = collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    user_dict = user.dict()
    highest_user = collection.find_one(sort=[("user_id", -1)])
    user_id = highest_user["user_id"] + 1 if highest_user else 1
    user_dict["user_id"] = user_id

    inserted = collection.insert_one(user_dict)
    user_dict["_id"] = str(inserted.inserted_id)

    return user_dict

@app.get("/users/", response_model=List[User])
async def read_users():
    users = list(collection.find())
    return [{**user, "_id": str(user["_id"])} for user in users]

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: str):
    user = collection.find_one({"_id": user_id})
    if user:
        return {**user, "_id": str(user["_id"])}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: User):
    user_dict = user.dict()
    updated = collection.update_one({"_id": user_id}, {"$set": user_dict})

    if updated.modified_count:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    deleted = collection.delete_one({"_id": user_id})
    if deleted.deleted_count:
        return {"Deleted": user_id}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.post("/items", response_model=ItemUpload)
async def add_item(item: ItemUpload):
    item_dict = item.dict()

    highest_item = itemcollection.find_one(sort=[("item_id", -1)])
    item_id = highest_item["item_id"] + 1 if highest_item else 1000
    item_dict["item_id"] = item_id

    insert = itemcollection.insert_one(item_dict)
    item_dict["_id"] = str(insert.inserted_id)

    return item_dict

@app.get("/items", response_model=List[Item])
async def get_items():
    items = list(itemcollection.find())
    return items

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = itemcollection.find_one({"item_id": item_id})
    if item:
        return item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    item_dict = item.dict()
    updated = itemcollection.update_one({"item_id": item_id}, {"$set": item_dict})

    if updated.modified_count:
        return item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    deleted = itemcollection.delete_one({"item_id": item_id})
    if deleted.deleted_count:
        return {"Deleted": item_id}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@app.on_event("startup")
async def startup():
    # Initialization code if needed
    pass

@app.on_event("shutdown")
async def shutdown():
    # Cleanup code if needed
    pass
