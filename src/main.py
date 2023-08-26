import uvicorn
from fastapi import FastAPI
from src.routes import user, debate
from src.repository.mongo import database


app = FastAPI()
app.include_router(user.router)
app.include_router(debate.router)

@app.on_event("startup")
def connect_mongodb():
    database.connect()


@app.on_event("shutdown")
def close_mongodb():
    database.close()


@app.get("/hello")
def hello():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)