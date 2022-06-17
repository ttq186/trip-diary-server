from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings

from api.v1.routers import (
    user,
    auth,
    trip,
    trip_like,
    location,
    trip_comment,
    location_file,
    checklist_item,
)

app = FastAPI(title="Tripari's", version="1.0.0", root_path=settings.ROOT_PATH)

allow_origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://triparis.work",
    "https://triparis.work",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(trip.router)
app.include_router(location.router)
app.include_router(location_file.router)
app.include_router(checklist_item.router)
app.include_router(trip_like.router)
app.include_router(trip_comment.router)
