# API Documentation

## App Store Icon Hunter REST API

The REST API provides programmatic access to search and download app icons.

## Base URL

```
http://localhost:8000
```

## Endpoints

### GET `/`
Root endpoint with API information.

**Response:**
```json
{
  "name": "App Store Icon Hunter API",
  "version": "2.0.0",
  "description": "Search apps and download icons from App Store and Google Play",
  "endpoints": {
    "search": "/search",
    "download": "/download",
    "status": "/status/{job_id}",
    "download_file": "/download/{job_id}",
    "docs": "/docs"
  }
}
```

### POST `/search`
Search for apps in App Store and/or Google Play Store.

**Request Body:**
```json
{
  "term": "Instagram",
  "store": "both",
  "country": "us", 
  "limit": 10
}
```

**Parameters:**
- `term` (string, required): Search term
- `store` (string): Store to search - `appstore`, `googleplay`, or `both` (default: `both`)
- `country` (string): Country code (default: `us`)
- `limit` (integer): Maximum results per store (default: 10, max: 50)

**Response:**
```json
[
  {
    "name": "Instagram",
    "bundle_id": "com.burbn.instagram",
    "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple123/v4/...",
    "store": "appstore",
    "price": "Free",
    "rating": 4.5,
    "description": "Instagram is a simple way to capture and share...",
    "developer": "Instagram, Inc.",
    "category": "Photo & Video",
    "url": "https://apps.apple.com/app/instagram/id389801252"
  }
]
```

### POST `/download`
Start downloading icons for selected apps.

**Request Body:**
```json
{
  "apps": [
    {
      "name": "Instagram",
      "bundle_id": "com.burbn.instagram", 
      "icon_url": "https://is1-ssl.mzstatic.com/image/thumb/Purple123/v4/...",
      "store": "appstore"
    }
  ],
  "sizes": [64, 128, 256, 512],
  "format": "zip"
}
```

**Parameters:**
- `apps` (array, required): List of app objects to download
- `sizes` (array): Icon sizes to generate (default: [64, 128, 256, 512])
- `format` (string): Download format - currently only `zip` supported

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "started",
  "message": "Download started for 1 apps"
}
```

### GET `/status/{job_id}`
Get the status of a download job.

**Parameters:**
- `job_id` (string): The ID of the download job

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 1,
  "total": 1,
  "completed_apps": ["Instagram"],
  "failed_apps": [],
  "download_url": null,
  "error_message": null
}
```

**Status Values:**
- `pending`: Job is queued
- `running`: Job is actively downloading
- `completed`: Job finished successfully
- `failed`: Job failed with errors

### GET `/download/{job_id}`
Download the completed ZIP file for a job.

**Parameters:**
- `job_id` (string): The ID of the completed download job

**Response:**
- ZIP file download (binary)
- Filename: `icons_{job_id}.zip`

### GET `/jobs`
List all download jobs and their status.

**Response:**
```json
{
  "jobs": {
    "550e8400-e29b-41d4-a716-446655440000": {
      "job_id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "completed",
      "progress": "1/1",
      "completed_apps": 1,
      "failed_apps": 0
    }
  }
}
```

### DELETE `/jobs/{job_id}`
Clean up a completed job and its files.

**Parameters:**
- `job_id` (string): The ID of the job to clean up

**Response:**
```json
{
  "message": "Job 550e8400-e29b-41d4-a716-446655440000 cleaned up"
}
```

### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "App Store Icon Hunter API",
  "version": "2.0.0"
}
```

## Error Responses

All endpoints return appropriate HTTP status codes and error messages:

**400 Bad Request:**
```json
{
  "detail": "Invalid store name"
}
```

**404 Not Found:**
```json
{
  "detail": "Job not found"  
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Search failed"
}
```

## Example Usage

### Python with requests

```python
import requests
import time

# Search for apps
response = requests.post("http://localhost:8000/search", json={
    "term": "Instagram",
    "store": "appstore",
    "limit": 3
})
apps = response.json()

# Start download
response = requests.post("http://localhost:8000/download", json={
    "apps": apps[:2],  # Download first 2 apps
    "sizes": [128, 256, 512]
})
job = response.json()
job_id = job["job_id"]

# Monitor progress
while True:
    response = requests.get(f"http://localhost:8000/status/{job_id}")
    status = response.json()
    
    print(f"Status: {status['status']} - {status['progress']}/{status['total']}")
    
    if status['status'] == 'completed':
        # Download ZIP file
        response = requests.get(f"http://localhost:8000/download/{job_id}")
        with open("icons.zip", "wb") as f:
            f.write(response.content)
        print("Download complete!")
        break
    elif status['status'] == 'failed':
        print(f"Download failed: {status['error_message']}")
        break
    
    time.sleep(2)
```

### cURL

```bash
# Search for apps
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"term": "Instagram", "store": "appstore", "limit": 5}'

# Start download (replace with actual app data)
curl -X POST "http://localhost:8000/download" \
  -H "Content-Type: application/json" \
  -d '{"apps": [...], "sizes": [64, 128, 256]}'

# Check status
curl "http://localhost:8000/status/{job_id}"

# Download ZIP file
curl -O "http://localhost:8000/download/{job_id}"
```

## Rate Limiting

Currently no rate limiting is implemented, but consider implementing rate limiting for production use.

## Authentication

Currently no authentication is required, but consider adding API keys for production deployments.

## Running the API Server

```bash
# Install dependencies
pip install app-store-icon-hunter

# Run the server
uvicorn app_store_icon_hunter.api.main:app --host 0.0.0.0 --port 8000

# Or run directly
python -m app_store_icon_hunter.api.main
```

The API documentation is also available at `/docs` (Swagger UI) and `/redoc` when the server is running.
