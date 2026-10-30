
from fastapi import APIRouter, Query
import json
import math

from app.services.dataset_service import preprocess_dataset


# Create Diagnostic Centres API router
router = APIRouter(
    prefix="/centres",
    tags=["Diagnostic Centres"]
)


# API 1: Get all diagnostic centres
@router.get("/")
def get_all_centres():

    centres, prices = preprocess_dataset()

    result = json.loads(
        centres.to_json(
            orient="records",
            force_ascii=False
        )
    )

    return {
        "total_centres": len(result),
        "centres": result
    }


# API 2: Search diagnostic centres by name or area
@router.get("/search")
def search_centres(
    name: str | None = Query(default=None),
    area: str | None = Query(default=None)
):

    centres, prices = preprocess_dataset()

    filtered = centres.copy()

    # Filter by diagnostic centre name
    if name:
        filtered = filtered[
            filtered["Diagnostic Centre"].str.contains(
                name,
                case=False,
                na=False
            )
        ]

    # Filter by area
    if area:
        filtered = filtered[
            filtered["Area"].str.contains(
                area,
                case=False,
                na=False
            )
        ]

    result = json.loads(
        filtered.to_json(
            orient="records",
            force_ascii=False
        )
    )

    return {
        "total_results": len(result),
        "centres": result
    }


# API 3: Find nearby diagnostic centres
@router.get("/nearby")
def get_nearby_centres(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
    radius_km: float = Query(default=10, gt=0)
):

    centres, prices = preprocess_dataset()

    # Remove centres without valid coordinates
    filtered = centres.dropna(
        subset=["Latitude", "Longitude"]
    ).copy()

    # Calculate geographical distance using Haversine formula
    def calculate_distance(lat1, lon1, lat2, lon2):

        earth_radius = 6371

        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1)
            * math.cos(lat2)
            * math.sin(dlon / 2) ** 2
        )

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )

        return earth_radius * c

    # Calculate distance for each diagnostic centre
    filtered["Distance (km)"] = filtered.apply(
        lambda row: calculate_distance(
            latitude,
            longitude,
            row["Latitude"],
            row["Longitude"]
        ),
        axis=1
    )

    # Filter centres within the requested radius
    filtered = filtered[
        filtered["Distance (km)"] <= radius_km
    ]

    # Sort centres from nearest to farthest
    filtered = filtered.sort_values(
        by="Distance (km)"
    )

    result = json.loads(
        filtered.to_json(
            orient="records",
            force_ascii=False
        )
    )

    return {
        "search_radius_km": radius_km,
        "total_nearby_centres": len(result),
        "centres": result
    }


# API 4: Get all tests offered by a diagnostic centre
@router.get("/{centre_name}/tests")
def get_centre_tests(centre_name: str):

    centres, prices = preprocess_dataset()

    # Find matching diagnostic centre
    filtered = prices[
        prices["Diagnostic Centre"].str.casefold()
        == centre_name.strip().casefold()
    ]

    # Handle unavailable centre or missing test records
    if filtered.empty:
        return {
            "message": "No tests found for this diagnostic centre",
            "centre": centre_name,
            "total_tests": 0,
            "tests": []
        }

    # Extract test names and prices
    result = filtered[
        [
            "Test",
            "Min Price (₹)",
            "Max Price (₹)"
        ]
    ].to_dict(orient="records")

    return {
        "centre": centre_name,
        "total_tests": len(result),
        "tests": result
    }


