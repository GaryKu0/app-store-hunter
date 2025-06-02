"""
Basic usage example for App Store Icon Hunter

This example demonstrates the basic CLI usage
"""

from app_store_icon_hunter.core.app_store import AppStoreAPI
from app_store_icon_hunter.core.downloader import IconDownloader
from app_store_icon_hunter.utils.helpers import format_app_name


def basic_search_example():
    """Basic search example using the core APIs directly"""
    print("🚀 Basic Search Example")
    print("=" * 50)
    
    # Initialize API
    app_store = AppStoreAPI()
    
    # Search for apps
    print("🔍 Searching for 'Instagram' in App Store...")
    apps = app_store.search_apps("Instagram", limit=5)
    
    if apps:
        print(f"\n📱 Found {len(apps)} apps:")
        for i, app in enumerate(apps, 1):
            name = format_app_name(app.get('name', 'Unknown'))
            price = app.get('price', 'Free')
            developer = app.get('developer', 'Unknown')
            print(f"{i}. {name} - {price} (by {developer})")
        
        # Download first app's icon
        first_app = apps[0]
        print(f"\n📥 Downloading icon for {first_app['name']}...")
        
        downloader = IconDownloader()
        files = downloader.download_icon_sync(
            first_app['icon_url'], 
            first_app['name'],
            sizes=[128, 256, 512]
        )
        
        if files:
            print(f"✅ Downloaded {len(files)} icon files:")
            for file_path in files:
                print(f"  - {file_path}")
        else:
            print("❌ Download failed")
    
    else:
        print("❌ No apps found")


if __name__ == "__main__":
    basic_search_example()
