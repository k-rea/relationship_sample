import uvicorn

from app.main import app

if __name__ == "__main__":
    uvicorn.run(app=app, host="localhost", port=8000)
