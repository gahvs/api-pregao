from fastapi import FastAPI
import pregao.routes

app = FastAPI()

app.include_router(pregao.routes.router)

@app.get("/")
def root():
    return {
        "message": "API is running!"
    }