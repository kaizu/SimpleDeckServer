from manager import DeckManager, SpotNotFoundError, OperationError
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI()
manager = DeckManager(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])

class MoveRequest(BaseModel):
    from_spot: str
    to_spot: str

@app.post("/move")
def move_item(req: MoveRequest):
    try:
        manager.move_item(req.from_spot, req.to_spot)
        return {"status": "ok"}
    except SpotNotFoundError as e:
        raise HTTPException("move error")

class Item(BaseModel):
    uuid: uuid.UUID
    item_type: str

@app.put("/put_item/{spot_name}/")
def put_item(spot_name: str, item: Item):
    print("put_item", spot_name, item)
    try:
        manager.put_item(spot_name, item.model_dump())
        return {"status": "ok"}
    except OperationError as e:
        raise HTTPException(status_code = e.code)

@app.delete("/delete/{spot_name}")
def trash_item(spot_name: str):
    try:
        ret = manager.trash_item(spot_name)
        if ret == True:
            return {"status": "ok"}
        else:
            raise HTTPException(status_code=404, detail = str(f"No item in {spot_name}"))
    except SpotNotFoundError as e:
        raise HTTPException(status_code = 404, detail = str(f"Spot {spot_name} not found"))

@app.get("/state")
def get_state():
    return manager.get_all_spot_status()
