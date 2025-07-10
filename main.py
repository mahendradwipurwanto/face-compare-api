# app.py
from flask import Flask, request, jsonify
from deepface import DeepFace

app = Flask(__name__)

import os
import requests

def download_image(url, filename):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    # Ensure tmp directory exists (for local or GCP environments)
    tmp_dir = "/tmp"
    os.makedirs(tmp_dir, exist_ok=True)
    path = os.path.join(tmp_dir, filename)

    # Download the image with headers
    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        with open(path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded image to {path}")
        return path
    else:
        raise Exception(f"Failed to download image from URL: {url} (status code: {response.status_code})")



@app.route("/verify", methods=["POST"])
def verify():
    try:
        data = request.get_json()

        img1_url = data.get("img1_url")
        img2_url = data.get("img2_url")

        if not img1_url or not img2_url:
            return jsonify({"error": "Both img1_url and img2_url are required"}), 400

        img1_path = download_image(img1_url, "img1.jpg")
        img2_path = download_image(img2_url, "img2.jpg")

        result = DeepFace.verify(
            img1_path=img1_path,
            img2_path=img2_path,
            model_name="Facenet",
            enforce_detection=False
        )

        return jsonify({
            "matched": result["verified"],
            "distance": result["distance"],
            "threshold": result["threshold"],
            "model": result["model"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
