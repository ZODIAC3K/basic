from fastapi import FastAPI, Response, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.get(
    "/",
    responses={
        200: {"description": "Successful Response", "content": {"application/json": {"example": {"message": "Hello World"}}}},
        404: {"description": "Not Found", "content": {"application/json": {"example": {"error": "Not Found"}}}},
    },
)
def read_home():
    return {"message": "Hello World"}

class UserCreate(BaseModel):
    name: str

@app.post(
    "/users",
    responses={
        201: {"description": "User created successfully", "content": {"application/json": {"example": {"message": "John is created successfully"}}}},
        400: {"description": "Bad Request - Missing or invalid name", "content": {"application/json": {"example": {"error": "User name is required"}}}},
        422: {"description": "Validation Error", "content": {"application/json": {"example": {"error": "Invalid request format"}}}},
    },
)
async def create_user(user: UserCreate, response: Response):
    if user.name.strip() == "":
        response.status_code = 400
        return {"error": "User name is required"} 
    response.status_code = 201
    return {"message": f"{user.name} is created successfully"}

# Custom 404 Not Found Error
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Not Found"},
    )

# Custom 422 Validation Error Handler
@app.exception_handler(RequestValidationError)
async def custom_422_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid request format"},
    )
