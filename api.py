from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio

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
    allow_origins=origins,
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

@app.get("/reviews/")
async def read_item():
    results = await conn.get_reviews()

    order_items = []
    if len(results) == 0:
        return {
            "count": 0,
            "results": [
                {
                    "id": None,
                    "surname": None,
                    "name": None,
                    "lastname": None,
                    "phone": None,
                    "email": None,
                    "review": None,
                }
            ],
        }
    for i in results:
        order_items.append(
            reviews(
                id=i[0],
                surname = i[1],
                name = i[2],
                lastname = i[3],
                phone=i[4],
                email=i[5],
                review=i[6],
            )
        )

    return {"count": len(results), "results": order_items}

@app.post("/reviews/")
async def create_review(review: add_reviews):
    result = await conn.post_reviews(review)
    return result


if __name__ == "__main__":

    conn = workwithbd()

    # asyncio.run(conn.check_connection())

    # asyncio.run(
    #     conn.post_goods(product_item(title="Карбонара", category_id=2, price=1500))
    # )

    uvicorn.run(app, host="0.0.0.0", port=9010)