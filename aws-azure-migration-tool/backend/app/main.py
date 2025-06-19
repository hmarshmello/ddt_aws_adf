import sys
import os

# Add the parent directory of 'aws-azure-migration-tool' to the Python path
# This allows importing 'ddt_aws_adf' from the 'src' directory at the project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="AWS to Azure Migration Mapping Tool",
    description="Tool for mapping AWS Glue jobs to Azure Data Factory",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Vue.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "AWS to Azure Migration Mapping Tool API"}
