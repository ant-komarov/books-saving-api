from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def root() -> dict:
    return {"message": "Welcome to bookssaving api service"}
