from fastapi import FastAPI
from api.notmule import notmule
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notmule)



@app.get("/")
async def root():
    type = "hello"
    return {"message": "Hello World",
            "type": type}
