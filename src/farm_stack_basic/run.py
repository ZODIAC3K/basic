import uvicorn

def main_dev():
    uvicorn.run("src.farm_stack_basic.main:app", host="127.0.0.1", port=8000, reload=True)

def main_prod():
    uvicorn.run("src.farm_stack_basic.main:app", host="127.0.0.1", port=8000)
