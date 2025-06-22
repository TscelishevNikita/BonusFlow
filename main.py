from fastapi import FastAPI

from api.routers import router as bonus_flow_router

app = FastAPI()

app.include_router(bonus_flow_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
