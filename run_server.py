import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    print("🚀 Starting FastAPI server...")
    print("Make sure you have set up your .env file with Azure Storage credentials!")
    print("=" * 50)
    
    uvicorn.run(
        "endpoint:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 