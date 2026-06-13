"""Small FastAPI application used in the Jenkins CI/CD workshop."""

from fastapi import FastAPI, HTTPException

from app.logic import calculate_gross

app = FastAPI(title="Python CI Demo", version="1.0.0")


@app.get("/")
def root() -> dict:
    return {"message": "Welcome to the Python CI/CD demo"}


@app.get("/health")
def health() -> dict:
    """Endpoint for the post-deploy smoke test."""
    return {"status": "ok"}


@app.get("/vat")
def vat(net: float, rate: float = 23.0) -> dict:
    """Returns the gross amount for the given net amount and VAT rate."""
    try:
        gross = calculate_gross(net, rate)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"net": net, "rate": rate, "gross": gross}