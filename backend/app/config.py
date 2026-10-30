from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Dataset location
DATASET_PATH = BASE_DIR / "backend" / "data" / "raw" / "vellore_diagnostic_centres.xlsx"

# Application settings
APP_NAME = "Diagnostic Test Marketplace"
APP_VERSION = "1.0.0"