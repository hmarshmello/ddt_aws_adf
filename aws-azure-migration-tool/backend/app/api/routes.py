from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.mapping_service import (
    generate_mapping_report, # For "Do All & Generate Report" button
    get_adf_notebook_output,
    get_mapping_reference_output
)

router = APIRouter()

@router.post("/generate-mapping") # This is for the "Do All & Generate Report" button
async def generate_overall_report( # Renamed function for clarity
    glue_config: UploadFile = File(...),
    glue_script: UploadFile = File(...)
):
    try:
        glue_config_content = await glue_config.read()
        glue_script_content = await glue_script.read()
        
        report_content = generate_mapping_report( # This service fn now reads mapping_report.md
            glue_config_content.decode("utf-8"),
            glue_script_content.decode("utf-8")
        )
        # For this endpoint, the report is expected to be markdown
        return {"success": True, "report": report_content, "type": "markdown"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-adf-notebook")
async def generate_adf_notebook_endpoint(
    glue_config: UploadFile = File(...),
    glue_script: UploadFile = File(...)
):
    try:
        glue_config_content = await glue_config.read()
        glue_script_content = await glue_script.read()
        
        notebook_content = get_adf_notebook_output(
            glue_config_content.decode("utf-8"),
            glue_script_content.decode("utf-8")
        )
        # The content is Python code, return as plain text or specific content type
        return {"success": True, "report": notebook_content, "type": "python"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-mapping-reference")
async def generate_mapping_reference_endpoint(
    glue_config: UploadFile = File(...),
    glue_script: UploadFile = File(...)
):
    try:
        glue_config_content = await glue_config.read()
        glue_script_content = await glue_script.read()
        
        reference_content = get_mapping_reference_output(
            glue_config_content.decode("utf-8"),
            glue_script_content.decode("utf-8")
        )
        # This content is markdown
        return {"success": True, "report": reference_content, "type": "markdown"}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
