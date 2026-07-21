from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.v1.routes.chat import router as chat_router
from backend.app.api.v1.routes.upload import router as upload_router


app = FastAPI(
    title="AI EPC Project Intelligence Platform"
)


# Allow React frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router)
app.include_router(upload_router)