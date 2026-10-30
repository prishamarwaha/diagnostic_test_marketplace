
from fastapi import APIRouter, Query
from app.services.dataset_service import preprocess_dataset


router = APIRouter(
    prefix="/tests",
    tags=["Diagnostic Tests"]
)


# API 1: Get all available tests
@router.get("/")
def get_all_tests():

    centres, prices = preprocess_dataset()

    test_names = (
        prices["Test"]
        .dropna()
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    return {
        "total_tests": len(test_names),
        "tests": test_names
    }


# API 2: Compare prices for a particular test
@router.get("/{test_name}")
def get_test_prices(
    test_name: str,
    sort_order: str = Query(
        default="asc",
        description="Use asc for cheapest first or desc for most expensive first"
    )
):

    centres, prices = preprocess_dataset()

    filtered_prices = prices[
        prices["Test"].str.casefold() == test_name.strip().casefold()
    ].copy()

    if filtered_prices.empty:
        return {
            "message": "Test not found",
            "test": test_name,
            "total_centres": 0,
            "prices": []
        }

    # Validate sorting preference
    if sort_order.lower() not in ["asc", "desc"]:
        return {
            "message": "Invalid sort order. Use asc or desc."
        }

    # Sort by minimum test price
    filtered_prices = filtered_prices.sort_values(
        by="Min Price (₹)",
        ascending=(sort_order.lower() == "asc")
    )

    result = filtered_prices[
        [
            "Diagnostic Centre",
            "Area",
            "Test",
            "Min Price (₹)",
            "Max Price (₹)"
        ]
    ].to_dict(orient="records")

    return {
        "test": test_name,
        "sort_order": sort_order,
        "total_centres": len(result),
        "prices": result
    }
