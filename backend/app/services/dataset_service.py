
from pathlib import Path
import pandas as pd


# Locate the original Excel dataset
BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    BASE_DIR / "data" / "raw" /
    "vellore_diagnostic_centres.xlsx"
)


def load_dataset():

    """Load both sheets from the original Excel dataset."""

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATASET_PATH}"
        )

    centres = pd.read_excel(
        DATASET_PATH,
        sheet_name="Diagnostic Centres"
    )

    prices = pd.read_excel(
        DATASET_PATH,
        sheet_name="Test Price List"
    )

    return centres, prices


def get_dataset_summary():

    """Return basic information about our dataset."""

    centres, prices = load_dataset()

    return {
        "centre_records": len(centres),
        "unique_centre_names":
            centres["Diagnostic Centre"].nunique(),

        "price_records": len(prices),

        "unique_tests":
            prices["Test"].nunique(),

        "centre_columns":
            list(centres.columns),

        "price_columns":
            list(prices.columns),

        "missing_centre_values":
            centres.isnull().sum().to_dict(),

        "missing_price_values":
            prices.isnull().sum().to_dict()
    }

def preprocess_dataset():
    """
   Clean and prepare both datasets for API use.
    """

    # Step 1: Load the original datasets
    centres, prices = load_dataset()

    # Step 2: Create copies so original data remains unchanged
    centres = centres.copy()
    prices = prices.copy()

    # Step 3: Remove duplicate records
    centres = centres.drop_duplicates()
    prices = prices.drop_duplicates()

    # Step 4: Clean text columns in diagnostic centres
    centre_text_columns = [
        "Diagnostic Centre",
        "Area",
        "Full Address (Google Maps)",
        "Google Maps Link",
        "Services Provided",
        "Location Note"
    ]

    for column in centre_text_columns:
        centres[column] = (
            centres[column]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
        )

    # Step 5: Clean test price text columns
    price_text_columns = [
        "Diagnostic Centre",
        "Area",
        "Test"
    ]

    for column in price_text_columns:
        prices[column] = (
            prices[column]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
        )

    # Step 6: Convert coordinates into numeric values
    centres["Latitude"] = pd.to_numeric(
        centres["Latitude"], errors="coerce"
    )

    centres["Longitude"] = pd.to_numeric(
        centres["Longitude"], errors="coerce"
    )

    # Step 7: Convert test prices into numeric values
    prices["Min Price (₹)"] = pd.to_numeric(
        prices["Min Price (₹)"], errors="coerce"
    )

    prices["Max Price (₹)"] = pd.to_numeric(
        prices["Max Price (₹)"], errors="coerce"
    )

    # Step 8: Handle missing location notes
    centres["Location Note"] = centres["Location Note"].fillna(
        "Not provided"
    )

    # Step 9: Remove records without essential identifiers
    centres = centres.dropna(
        subset=["Diagnostic Centre"]
    )

    prices = prices.dropna(
        subset=[
            "Diagnostic Centre",
            "Test",
            "Min Price (₹)",
            "Max Price (₹)"
        ]
    )

    # Step 10: Reset row indexes
    centres = centres.reset_index(drop=True)
    prices = prices.reset_index(drop=True)

    return centres, prices
