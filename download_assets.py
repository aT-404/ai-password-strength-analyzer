import requests
import os

# --- IMPORTANT: REPLACE THESE URLS with the actual RAW file links from Hugging Face ---
ASSET_URLS = {
    "password_strength_model.joblib": "https://huggingface.co/datasets/aT-404/password-analyzer-assets/resolve/main/password_strength_model.joblib", 
    "model_features.joblib": "https://huggingface.co/datasets/aT-404/password-analyzer-assets/resolve/main/model_features.joblib",
    "password_data.csv": "https://huggingface.co/datasets/aT-404/password-analyzer-assets/resolve/main/password_data.csv"
}

def download_assets():
    print("Starting download of ML assets from Hugging Face...")
    for filename, url in ASSET_URLS.items():
        if url.startswith("PASTE_THE_RAW"):
            print(f"Skipping {filename}: URL not updated.")
            continue

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(filename, 'wb') as handle:
                for chunk in response.iter_content(chunk_size=8192):
                    handle.write(chunk)
            print(f"Successfully downloaded {filename}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {filename}: {e}")

if __name__ == '__main__':
    download_assets()