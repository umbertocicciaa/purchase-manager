from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_tables
from controller import PurchaseController

app = FastAPI(title="Purchase Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
create_tables()

# Purchase routes
app.post("/upload/")(PurchaseController.upload_purchase)
app.get("/search", response_model=list)(PurchaseController.search_purchases)
app.get("/purchase/{purchase_id}")(PurchaseController.get_purchase)
app.delete("/purchase/{purchase_id}")(PurchaseController.delete_purchase)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
