from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from router import router


app = FastAPI()

app.include_router(router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def root() -> dict:
    return {"message": "Welcome to bookssaving api service"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
