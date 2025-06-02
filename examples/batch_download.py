"""
Batch download example for App Store Icon Hunter

This example shows how to search for multiple apps and download all their icons
"""

import asyncio
from app_store_icon_hunter.core.app_store import AppStoreAPI
from app_store_icon_hunter.core.google_play import GooglePlayAPI
from app_store_icon_hunter.core.downloader import IconDownloader


async def batch_download_example():
    """Example of batch downloading icons for multiple apps"""
    print("🚀 Batch Download Example")
    print("=" * 50)
    
    # Initialize APIs
    app_store = AppStoreAPI()
    google_play = GooglePlayAPI()
    downloader = IconDownloader("batch_download_icons")
    
    # Search terms to batch process
    search_terms = ["WhatsApp", "Telegram", "Signal"]
    all_apps = []
    
    # Collect apps from multiple searches
    for term in search_terms:
        print(f"🔍 Searching for '{term}'...")
        
        # Search App Store
        app_store_apps = app_store.search_apps(term, limit=3)
        all_apps.extend(app_store_apps[:1])  # Take first result
        
        # Search Google Play (if API key available)
        google_play_apps = google_play.search_apps(term, limit=3)
        all_apps.extend(google_play_apps[:1])  # Take first result
    
    if not all_apps:
        print("❌ No apps found")
        return
    
    print(f"\n📱 Found {len(all_apps)} apps total:")
    for app in all_apps:
        print(f"  - {app['name']} ({app['store']})")
    
    # Start batch download
    print(f"\n📥 Starting batch download...")
    result = await downloader.download_icons_async(
        all_apps, 
        sizes=[64, 128, 256],
        job_id="batch_example"
    )
    
    print(f"\n📊 Download Results:")
    print(f"Status: {result['status']}")
    print(f"Completed: {result['progress']}/{result['total']}")
    
    if result['status'] == 'completed':
        print(f"✅ Batch download completed!")
        if result.get('zip_path'):
            print(f"📦 ZIP file: {result['zip_path']}")
        
        print("\n✅ Successfully downloaded:")
        for app_name in result.get('completed_apps', []):
            print(f"  - {app_name}")
        
        if result.get('failed_apps'):
            print("\n❌ Failed downloads:")
            for failure in result['failed_apps']:
                print(f"  - {failure['app']}: {failure['error']}")
    else:
        print(f"❌ Batch download failed: {result.get('error_message', 'Unknown error')}")


if __name__ == "__main__":
    asyncio.run(batch_download_example())
