from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.routers import user, auth

app = FastAPI(title="Tripari's", version="1.0.0")

allow_origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://ttq186.xyz",
    "https://ttq186.xyz",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
