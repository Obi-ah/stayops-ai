from fastapi import FastAPI

app = FastAPI(title="StayOps AI", description="AI-powered serviced apartment booking operations", version= "1.0")


@app.get("/")
def home():
    return {"message": "Welcome to StayOps AI!",
            "status": "running"}

    