from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

fake_items_db = [
    Item(id=1, name="Laptop", description="Gaming laptop", price=999.99),
    Item(id=2, name="Mouse", description="Wireless mouse", price=29.99),
    Item(id=3, name="Keyboard", description="Mechanical keyboard", price=79.99),
]

# GET ejemplo
@router.get("/", response_model=List[Item])
async def read_items():
    return fake_items_db

# GET con id
@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int):
    item = next((item for item in fake_items_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# POST para crear
@router.post("/", response_model=Item)
async def create_item(item: Item):
    if any(existing_item.id == item.id for existing_item in fake_items_db):
        raise HTTPException(status_code=400, detail="Item ID already exists")
    
    fake_items_db.append(item)
    return item

# PUT para actualizar
@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id != item.id:
        raise HTTPException(status_code=400, detail="Item ID mismatch")
    
    for index, existing_item in enumerate(fake_items_db):
        if existing_item.id == item_id:
            fake_items_db[index] = item
            return item
    
    raise HTTPException(status_code=404, detail="Item not found")

# DELETE para eliminar
@router.delete("/{item_id}")
async def delete_item(item_id: int):
    for index, existing_item in enumerate(fake_items_db):
        if existing_item.id == item_id:
            deleted_item = fake_items_db.pop(index)
            return {"message": "Item deleted", "item": deleted_item}
    
    raise HTTPException(status_code=404, detail="Item not found")