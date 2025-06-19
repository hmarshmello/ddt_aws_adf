# AWS to Azure Migration Mapping Tool

A web-based tool for generating comprehensive migration mapping documents for AWS Glue to Azure Data Factory migrations.

## Overview

This tool helps you plan and document your migration from AWS Glue to Azure Data Factory and Azure Databricks. By analyzing your AWS Glue job definitions and scripts, it generates a detailed mapping document that outlines how to implement equivalent functionality in Azure.

## Features

- Upload AWS Glue job configuration (JSON) and script (Python) files
- Analyze the AWS Glue job to understand its purpose, configuration, and logic
- Generate a comprehensive mapping report with Azure equivalents
- View the report in the browser with proper Markdown rendering
- Download the report for future reference

## Project Structure

```
aws-azure-migration-tool/
│
├── backend/                      # FastAPI backend
│   ├── app/
│   │   ├── main.py               # FastAPI application entry point
│   │   ├── api/                  # API endpoints
│   │   ├── core/                 # Core functionality
│   │   └── services/             # Business logic
│   ├── tests/                    # Backend tests
│   ├── requirements.txt          # Python dependencies
│   └── Dockerfile                # For containerization
│
├── frontend/                     # Vue.js frontend
│   ├── public/                   # Static assets
│   ├── src/                      # Vue components and logic
│   ├── package.json              # NPM dependencies
│   ├── vue.config.js             # Vue CLI configuration
│   └── Dockerfile                # For containerization
│
├── docker-compose.yml            # For running both services together
└── README.md                     # Project documentation
```

## Prerequisites

- Python 3.9+
- Node.js 16+
- Docker and Docker Compose (optional, for containerized deployment)

## Setup and Installation

### Option 1: Local Development

#### Backend Setup

1. Navigate to the backend directory:
   ```
   cd aws-azure-migration-tool/backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run the backend server:
   ```
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd aws-azure-migration-tool/frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the development server:
   ```
   npm run serve
   ```

4. Access the application at `http://localhost:8080`

### Option 2: Docker Deployment

1. Make sure Docker and Docker Compose are installed on your system.

2. **Navigate to the tool's directory:**
   ```bash
   cd aws-azure-migration-tool
   ```

3. **Create a symbolic link (or directory junction on Windows) named `ddt_aws_adf` inside this directory.** This link should point to the actual source code of your `ddt_aws_adf` Python package. Replace `C:\path\to\your\ddt_aws_adf_package_source` with the correct absolute path to your `ddt_aws_adf` package (e.g., `D:\ddt_aws_adf\src\ddt_aws_adf` if your main project is `ddt_aws_adf` and the package is in its `src` folder).

   *   **For Unix/MacOS (run from `aws-azure-migration-tool` directory):**
       ```bash
       # Example: ln -s ../src/ddt_aws_adf ddt_aws_adf 
       # OR using an absolute path:
       ln -s /absolute/path/to/your/ddt_aws_adf_package_source ddt_aws_adf
       ```

   *   **For Windows (Command Prompt - run as Administrator, from `aws-azure-migration-tool` directory):**
       ```cmd
       # Example: mklink /D ddt_aws_adf ..\src\ddt_aws_adf
       # OR using an absolute path (use backslashes):
       mklink /D ddt_aws_adf C:\path\to\your\ddt_aws_adf_package_source
       ```
       *(Note: For `mklink /D`, the link name comes first, then the target path.)*

   *   **For Windows (PowerShell - run from `aws-azure-migration-tool` directory):**
       ```powershell
       # Example: New-Item -ItemType Junction -Path .\ddt_aws_adf -Target ..\src\ddt_aws_adf
       # OR using an absolute path:
       New-Item -ItemType Junction -Path .\ddt_aws_adf -Target C:\path\to\your\ddt_aws_adf_package_source
       ```
       *(This creates a directory junction, which is similar to a symbolic link for directories and often doesn't require admin privileges.)*

   This step is crucial for the Docker container to find your `ddt_aws_adf` package, as specified in `docker-compose.yml`.

4. Build and start the containers (run from `aws-azure-migration-tool` directory):
   ```bash
   docker-compose up -d
   ```

5. Access the application at `http://localhost`

## Usage

1. Open the application in your web browser.
2. Upload your AWS Glue job configuration (JSON) file.
3. Upload your AWS Glue script (Python) file.
4. Click "Generate Migration Mapping" to process the files.
5. Review the generated mapping report.
6. Download the report for future reference.

## Development

### Backend API Endpoints

- `GET /`: Root endpoint, returns a welcome message
- `POST /api/generate-mapping`: Accepts AWS Glue configuration and script files, returns a mapping report

### Adding New Features

- Backend: Add new endpoints in `app/api/routes.py` and implement business logic in `app/services/`
- Frontend: Add new components in `src/components/` and views in `src/views/`

## License

[MIT License](LICENSE)
