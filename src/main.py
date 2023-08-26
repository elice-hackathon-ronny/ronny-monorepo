import uvicorn
from fastapi import FastAPI
from src.routes import user, debate, debug
from src.repository.mongo import database
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(user.router)
app.include_router(debate.router)
app.include_router(debug.router)


origins = [
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # cookie 포함 여부를 설정한다. 기본은 False
    allow_methods=["*"],    # 허용할 method를 설정할 수 있으며, 기본값은 'GET'이다.
    allow_headers=["*"],	# 허용할 http header 목록을 설정할 수 있으며 Content-Type, Accept, Accept-Language, Content-Language은 항상 허용된다.
)


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
