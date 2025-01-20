from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio
import json
import logging

# from database import *
from database import *
import uvicorn

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:5500",
    "http://45.153.189.82:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# conn = workwithbd("localhost", "root", "", "mdk_bd")

class reviews(BaseModel):
    id: Optional[int] = None
    surname: Optional[str] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    review: Optional[str] = None

    class Config:
        from_attributes = True


class add_reviews(BaseModel):
    surname: Optional[str] = None
    name: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    review: Optional[str] = None

    class Config:
        from_attributes = True

# @app.get("/reviews/")
# async def read_item():
#     results = await conn.get_reviews()

#     order_items = []
#     if len(results) == 0:
#         return {
#             "count": 0,
#             "results": [
#                 {
#                     "id": None,
#                     "surname": None,
#                     "name": None,
#                     "lastname": None,
#                     "phone": None,
#                     "email": None,
#                     "review": None,
#                 }
#             ],
#         }
#     for i in results:
#         order_items.append(
#             reviews(
#                 id=i[0],
#                 surname = i[1],
#                 name = i[2],
#                 lastname = i[3],
#                 phone=i[4],
#                 email=i[5],
#                 review=i[6],
#             )
#         )

#     return {"count": len(results), "results": order_items}

# @app.post("/reviews/")
# async def create_review(review: add_reviews):
#     result = await conn.post_reviews(review)
#     return result

@app.post("/test")
async def test_endpoint(request: Request):
    # Получаем JSON-данные из запроса
    try:
        data = await request.json()
    except Exception as e:
        logging.error(f"Ошибка при получении JSON: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Логируем полученные данные
    logging.info(f"Получен запрос: {data}")

    # Проверяем тип запроса
    if data.get("type") == "confirmation":
        group_id = data.get("group_id")
        if group_id == 229078408:
            return {"response": "e3b4a4bc"}
        else:
            raise HTTPException(status_code=400, detail="Invalid group_id")
    else:
        raise HTTPException(status_code=400, detail="Invalid type")


if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=9010)