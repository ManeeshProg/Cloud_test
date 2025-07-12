import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_storage():
    """Set up Azure Storage container"""
    print("🔧 Setting up Azure Storage...")
    
    # Get connection string
    conn_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not conn_string:
        print("❌ AZURE_STORAGE_CONNECTION_STRING not found in .env file")
        return False
    
    try:
        # Create blob service client
        blob_service_client = BlobServiceClient.from_connection_string(conn_string)
        
        # Create container if it doesn't exist
        container_name = "attachment"
        container_client = blob_service_client.get_container_client(container_name)
        
        print(f"📦 Creating container '{container_name}'...")
        container_client.create_container()
        print(f"✅ Container '{container_name}' created successfully!")
        
        # List containers to verify
        containers = blob_service_client.list_containers()
        print("\n📋 Available containers:")
        for container in containers:
            print(f"   - {container.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

if __name__ == "__main__":
    setup_storage() 