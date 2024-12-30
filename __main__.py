import uvicorn

from app.db.db import auto_create_db

if __name__ == "__main__":
    auto_create_db()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
