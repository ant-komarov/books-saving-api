from fastapi import FastAPI
from router import router


app = FastAPI()

app.include_router(router)


@app.get("/")
def root() -> dict:
    return {"message": "Welcome to bookssaving api service"}
