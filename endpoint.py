# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import StreamingResponse
from functions import VideoStorageService
import os

app = FastAPI()
storage = VideoStorageService()

@app.post("/videos/upload/")
async def upload_video(file: UploadFile = File(...)):
    if file.content_type.split('/')[0] != 'video':
        raise HTTPException(400, "Invalid file type")
    
    # Read file size properly
    file_content = await file.read()
    file_size = len(file_content)
    if file_size > 500 * 1024 * 1024:  # 500MB limit
        raise HTTPException(400, "File too large")
    
    try:
        # Create a new UploadFile-like object with the content
        from io import BytesIO
        file.file = BytesIO(file_content)
        file.file.seek(0)  # Reset position to beginning
        
        url = await storage.upload_video(file, file.filename, file.content_type)
        return {"url": url, "filename": file.filename, "size": file_size}
    except Exception as e:
        raise HTTPException(500, f"Upload failed: {e}")

@app.get("/videos/")
async def list_videos():
    """List all uploaded videos"""
    try:
        videos = await storage.list_videos()
        return {"videos": videos}
    except Exception as e:
        raise HTTPException(500, f"Failed to list videos: {e}")

@app.get("/videos/{blob_name}")
async def get_video(blob_name: str, use_sas: bool = Query(False, description="Use SAS URL for secure access")):
    """Get a specific video by blob name"""
    try:
        if use_sas:
            url = await storage.generate_sas_url(blob_name)
        else:
            url = await storage.get_video_url(blob_name)
        return {"url": url, "blob_name": blob_name}
    except Exception as e:
        raise HTTPException(500, f"Failed to get video: {e}")

@app.get("/videos/{blob_name}/stream")
async def stream_video(blob_name: str):
    """Stream a video directly from Azure Storage"""
    try:
        blob = storage.client.get_blob_client(container=storage.container, blob=blob_name)
        properties = await blob.get_blob_properties()
        
        # Get the blob data
        blob_data = await blob.download_blob()
        
        return StreamingResponse(
            blob_data.readall(),
            media_type=properties.content_settings.content_type,
            headers={"Content-Disposition": f"inline; filename={blob_name}"}
        )
    except Exception as e:
        raise HTTPException(500, f"Failed to stream video: {e}")
