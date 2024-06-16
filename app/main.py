from fastapi import FastAPI
from routers import pregao

app = FastAPI()

app.include_router(pregao.router)

@app.get("/")
def root():
    return {
        "message": "API is running!"
    }