import uvicorn

def main_dev():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

def main_prod():
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
