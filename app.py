from fastapi import FastAPI

app = FastAPI()


@app.get("/{id}")
async def root(id: int):
    print(type(id))
    return {"message": "Hello World"}
