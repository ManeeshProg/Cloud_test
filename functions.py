import os, uuid
from azure.storage.blob.aio import BlobServiceClient
from azure.storage.blob import ContentSettings, StandardBlobTier, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

class VideoStorageService:
    def __init__(self):
        conn = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if not conn:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is required")
        self.client = BlobServiceClient.from_connection_string(conn)
        self.container = "attachment"

    async def upload_video(self, file, filename, content_type) -> str:
        ext = filename.split('.')[-1].lower()
        blob_name = f"{uuid.uuid4()}.{ext}"
        blob = self.client.get_blob_client(container=self.container, blob=blob_name)
        settings = ContentSettings(content_type=content_type)
        data = await file.read()
        await blob.upload_blob(data, overwrite=True, content_settings=settings, standard_blob_tier=StandardBlobTier.HOT)
        return blob.url

    async def get_video_url(self, blob_name: str) -> str:
        """Get a direct URL to the video blob"""
        blob = self.client.get_blob_client(container=self.container, blob=blob_name)
        return blob.url

    async def generate_sas_url(self, blob_name: str, expiry_hours: int = 1) -> str:
        """Generate a SAS URL for secure access to the video"""
        account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
        account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
        
        if not account_name or not account_key:
            raise ValueError("AZURE_STORAGE_ACCOUNT_NAME and AZURE_STORAGE_ACCOUNT_KEY are required for SAS URL generation")
        
        blob = self.client.get_blob_client(container=self.container, blob=blob_name)
        sas = generate_blob_sas(
            account_name, self.container, blob_name,
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=expiry_hours)
        )
        return f"{blob.url}?{sas}"

    async def list_videos(self):
        """List all videos in the container"""
        videos = []
        async for blob in self.client.get_container_client(self.container).list_blobs():
            videos.append({
                "name": blob.name,
                "size": blob.size,
                "created": blob.creation_time.isoformat() if hasattr(blob, 'creation_time') else None,
                "url": await self.get_video_url(blob.name)
            })
        return videos
