#!/usr/bin/env python3
"""
Example script demonstrating how to use the App Store Icon Hunter API

This example shows how to:
1. Search for apps using the REST API
2. Start a download job
3. Monitor download progress
4. Download the completed ZIP file
"""

import requests
import time
import json

API_BASE_URL = "http://localhost:8000"

def search_apps(term, store="both", limit=5):
    """Search for apps using the API"""
    print(f"🔍 Searching for '{term}' in {store}...")
    
    response = requests.post(f"{API_BASE_URL}/search", json={
        "term": term,
        "store": store,
        "country": "us",
        "limit": limit
    })
    
    if response.status_code == 200:
        apps = response.json()
        print(f"✅ Found {len(apps)} apps")
        return apps
    else:
        print(f"❌ Search failed: {response.status_code}")
        return []

def start_download(apps, sizes=[128, 256, 512]):
    """Start downloading icons for selected apps"""
    print(f"📥 Starting download for {len(apps)} apps...")
    
    response = requests.post(f"{API_BASE_URL}/download", json={
        "apps": apps,
        "sizes": sizes,
        "format": "zip"
    })
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Download job started: {result['job_id']}")
        return result["job_id"]
    else:
        print(f"❌ Download failed: {response.status_code}")
        return None

def check_status(job_id):
    """Check the status of a download job"""
    response = requests.get(f"{API_BASE_URL}/status/{job_id}")
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Status check failed: {response.status_code}")
        return None

def download_file(job_id, filename="icons.zip"):
    """Download the completed zip file"""
    response = requests.get(f"{API_BASE_URL}/download/{job_id}")
    
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Downloaded {filename}")
        return True
    else:
        print(f"❌ Download failed: {response.status_code}")
        return False

def main():
    """Main example function"""
    print("🚀 App Store Icon Hunter API Example")
    print("=" * 50)
    
    # Search for apps
    apps = search_apps("Instagram", store="appstore", limit=3)
    
    if not apps:
        print("No apps found. Make sure the API server is running!")
        return
    
    # Display found apps
    print("\n📱 Found Apps:")
    for i, app in enumerate(apps, 1):
        print(f"{i}. {app['name']} ({app['store']}) - {app['price']}")
        if app.get('rating'):
            print(f"   ⭐ Rating: {app['rating']}/5")
    
    # Select first 2 apps for download
    selected_apps = apps[:2]
    print(f"\n🎯 Selected {len(selected_apps)} apps for download")
    
    # Start download
    job_id = start_download(selected_apps, sizes=[64, 128, 256])
    
    if not job_id:
        return
    
    # Monitor progress
    print("\n⏳ Monitoring download progress...")
    while True:
        status = check_status(job_id)
        if not status:
            break
        
        print(f"Status: {status['status']} - Progress: {status['progress']}/{status['total']}")
        
        if status['status'] == 'completed':
            print("✅ Download completed!")
            
            # Download the zip file
            if download_file(job_id, f"instagram_icons_{job_id[:8]}.zip"):
                print(f"🎉 Icons saved successfully!")
            break
        elif status['status'] == 'failed':
            print(f"❌ Download failed: {status.get('error_message', 'Unknown error')}")
            break
        
        time.sleep(2)  # Wait 2 seconds before checking again

def interactive_example():
    """Interactive example that prompts user for input"""
    print("🎮 Interactive App Icon Hunter")
    print("=" * 40)
    
    # Get search term from user
    search_term = input("Enter app name to search: ").strip()
    if not search_term:
        print("No search term provided!")
        return
    
    # Get store preference
    store = input("Store (appstore/googleplay/both) [both]: ").strip().lower()
    if store not in ['appstore', 'googleplay', 'both']:
        store = 'both'
    
    # Search for apps
    apps = search_apps(search_term, store=store, limit=10)
    
    if not apps:
        return
    
    # Display apps and let user select
    print("\n📱 Select apps to download:")
    for i, app in enumerate(apps, 1):
        print(f"{i}. {app['name']} ({app['store']}) - {app['price']}")
    
    # Get user selection
    try:
        selection = input("Enter numbers separated by commas (e.g., 1,3,5): ").strip()
        indices = [int(x.strip()) - 1 for x in selection.split(',')]
        selected_apps = [apps[i] for i in indices if 0 <= i < len(apps)]
        
        if not selected_apps:
            print("No valid apps selected!")
            return
        
        print(f"Selected {len(selected_apps)} apps")
        
        # Get icon sizes
        sizes_input = input("Icon sizes (64,128,256,512) [default]: ").strip()
        if sizes_input:
            sizes = [int(x.strip()) for x in sizes_input.split(',')]
        else:
            sizes = [64, 128, 256, 512]
        
        # Start download process
        job_id = start_download(selected_apps, sizes)
        
        if job_id:
            print("Download started! Check the API server for progress.")
            print(f"Job ID: {job_id}")
        
    except (ValueError, IndexError) as e:
        print(f"Invalid selection: {e}")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Run basic example")
    print("2. Run interactive example")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        main()
    elif choice == "2":
        interactive_example()
    else:
        print("Invalid choice. Running basic example...")
        main()