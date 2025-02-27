"""
This is a basic FastAPI application.
"""

from fastapi import FastAPI, Request

app = FastAPI(title="Fram Stack Basic", description="This is a basic FastAPI application.")

@app.get("/")
def read_home():
    return {"message": "Hello World"}

@app.post("/users")
async def create_user(request: Request):
    data = await request.json() # json is a dictionary in python and its automatically parsed in fastapi but not in django
    userName = data.get("name")  # .get() is safer than data["name"] because it doesn't raise an error if the key doesn't exist so we need to check if userName is None
    if userName is None:
        return {"message": "User name is required"}
    return {"message": f"User created: {userName}"}
