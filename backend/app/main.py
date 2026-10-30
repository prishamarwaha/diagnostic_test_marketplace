from fastapi import FastAPI

from app.routers import (
    centres,
    tests,
    prescription,
    terminology,
    document_checker,
    travel,
    journey,
    equipment_maintenance,
    staff_roster,
    capacity,
    invoice,
    cancellation,
    family,
    cost
)

app = FastAPI(
    title="MediSlot API",
    description="Diagnostic Test Marketplace Backend",
    version="1.0.0"
)

# Register all API routers
app.include_router(centres.router)
app.include_router(tests.router)
app.include_router(prescription.router)
app.include_router(terminology.router)
app.include_router(document_checker.router)
app.include_router(travel.router)
app.include_router(journey.router)
app.include_router(equipment_maintenance.router)
app.include_router(staff_roster.router)
app.include_router(capacity.router)
app.include_router(invoice.router)
app.include_router(cancellation.router)
app.include_router(family.router)
app.include_router(cost.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to MediSlot",
        "status": "Backend is running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}