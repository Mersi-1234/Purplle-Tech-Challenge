from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Store Intelligence API Running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/stores/{store_id}/metrics")
def metrics(store_id: str):
    return {
        "store_id": store_id,
        "visitors": 0,
        "conversion_rate": 0
    }