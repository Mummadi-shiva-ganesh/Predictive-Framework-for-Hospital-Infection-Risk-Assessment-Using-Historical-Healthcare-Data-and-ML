"""
Download the Surgery Healthcare Dataset from Kaggle.

This script tries multiple methods to obtain the dataset:
1. Kaggle CLI (if credentials are configured)
2. opendatasets library (interactive credential prompt)
3. Manual download instructions

Dataset: https://www.kaggle.com/datasets/arunjangir245/surgery-healthcare-dataset
"""

import os
import sys
import shutil

DATASET_SLUG = "arunjangir245/surgery-healthcare-dataset"
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
TARGET_FILE = os.path.join(DATA_DIR, "dataset.csv")

def check_existing():
    """Check if dataset already exists."""
    if os.path.exists(TARGET_FILE):
        file_size = os.path.getsize(TARGET_FILE)
        if file_size > 100:  # More than 100 bytes (not empty/header-only)
            print(f"[OK] Dataset already exists at: {TARGET_FILE}")
            print(f"     File size: {file_size:,} bytes")
            return True
    return False

def try_kaggle_cli():
    """Try downloading via Kaggle CLI."""
    print("\n[METHOD 1] Trying Kaggle CLI...")
    try:
        import subprocess
        result = subprocess.run(
            ["kaggle", "datasets", "download", "-d", DATASET_SLUG, "-p", DATA_DIR, "--unzip"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            # Find the downloaded CSV
            for f in os.listdir(DATA_DIR):
                if f.endswith(".csv") and f != "dataset.csv":
                    src = os.path.join(DATA_DIR, f)
                    shutil.move(src, TARGET_FILE)
                    print(f"[OK] Downloaded and renamed to: {TARGET_FILE}")
                    return True
            # Check if dataset.csv was created directly
            if os.path.exists(TARGET_FILE):
                print(f"[OK] Downloaded to: {TARGET_FILE}")
                return True
        else:
            print(f"     Kaggle CLI failed: {result.stderr.strip()}")
    except FileNotFoundError:
        print("     Kaggle CLI not found.")
    except Exception as e:
        print(f"     Kaggle CLI error: {e}")
    return False

def try_opendatasets():
    """Try downloading via opendatasets (prompts for credentials)."""
    print("\n[METHOD 2] Trying opendatasets library...")
    try:
        import opendatasets as od
        url = f"https://www.kaggle.com/datasets/{DATASET_SLUG}"
        od.download(url, data_dir=DATA_DIR)
        
        # Find the downloaded CSV in the subdirectory
        download_dir = os.path.join(DATA_DIR, "surgery-healthcare-dataset")
        if os.path.isdir(download_dir):
            for f in os.listdir(download_dir):
                if f.endswith(".csv"):
                    src = os.path.join(download_dir, f)
                    shutil.move(src, TARGET_FILE)
                    shutil.rmtree(download_dir, ignore_errors=True)
                    print(f"[OK] Downloaded and moved to: {TARGET_FILE}")
                    return True
        # Check root data dir
        for f in os.listdir(DATA_DIR):
            if f.endswith(".csv") and f != "dataset.csv":
                src = os.path.join(DATA_DIR, f)
                shutil.move(src, TARGET_FILE)
                print(f"[OK] Downloaded and renamed to: {TARGET_FILE}")
                return True
    except Exception as e:
        print(f"     opendatasets error: {e}")
    return False

def print_manual_instructions():
    """Print manual download instructions."""
    print("\n" + "=" * 60)
    print("MANUAL DOWNLOAD REQUIRED")
    print("=" * 60)
    print()
    print("Neither automated method worked. Please download manually:")
    print()
    print("1. Open your browser and go to:")
    print(f"   https://www.kaggle.com/datasets/{DATASET_SLUG}")
    print()
    print("2. Click the 'Download' button (you may need to log in).")
    print()
    print("3. Extract the ZIP file.")
    print()
    print("4. Copy the CSV file to:")
    print(f"   {TARGET_FILE}")
    print()
    print("   If the CSV has a different name (e.g., surgery_healthcare_dataset.csv),")
    print("   rename it to 'dataset.csv'.")
    print()
    print("5. Then run the analysis script:")
    print("   python -m training.data_analysis")
    print("=" * 60)

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    print("Surgery Healthcare Dataset Downloader")
    print("=" * 40)
    print(f"Target: {TARGET_FILE}")
    
    # Check if already downloaded
    if check_existing():
        return True
    
    # Try automated methods
    if try_kaggle_cli():
        return True
    
    if try_opendatasets():
        return True
    
    # Fall back to manual instructions
    print_manual_instructions()
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
