from fastapi import FastAPI
from routers.webhook_router import webhook_router

app = FastAPI()

app.include_router(webhook_router.router)
