from fastapi import fastapi


@app.get("/")

def read_root():
    return {"Hello", "World"}