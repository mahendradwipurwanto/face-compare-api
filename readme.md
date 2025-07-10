# DeepFace Face Verification API

A lightweight Flask API to compare two faces using [DeepFace](https://github.com/serengil/deepface) and `Facenet` model. Accepts image **URLs** via a JSON POST request and returns similarity results.

## 📦 Features

- Face comparison using DeepFace (`Facenet`)
- Accepts image URLs (not uploads)
- Returns match result and distance
- Ready for Docker or local use

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/mahendradwipurwanto/face-compare-api.git
cd face-compare-api
