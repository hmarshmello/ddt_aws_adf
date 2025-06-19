from ddt_aws_adf.crew import DdtAwsAdf
from datetime import datetime
import os # Added for file operations
import traceback # Already imported below, but good to have at top if used widely

# Define output filenames (assuming they are created in the backend's current working directory)
NOTEBOOK_OUTPUT_FILENAME = "databricks_notebook.py"
MAPPING_REPORT_FILENAME = "mapping_report.md"

def _run_crew_and_get_outputs(inputs: dict) -> None:
    """
    Helper function to run the CrewAI process.
    This assumes kickoff() generates the necessary files.
    """
    print("--- MAPPING SERVICE (HELPER): _run_crew_and_get_outputs called ---")
    print(f"--- MAPPING SERVICE (HELPER): Inputs prepared for CrewAI ---")
    print(f"Input keys: {list(inputs.keys())}")
    # Avoid printing potentially very large glue_config/script
    # print(f"Inputs: {inputs}") 

    try:
        print("--- MAPPING SERVICE (HELPER): Calling DdtAwsAdf().crew().kickoff() ---")
        start_time = datetime.now()
        
        crew_instance = DdtAwsAdf().crew() 
        print("--- MAPPING SERVICE (HELPER): DdtAwsAdf().crew() initialized. Kicking off... ---")
        
        # We assume kickoff() will generate the files based on the tasks defined in crew.py
        # If kickoff() returns specific task outputs directly, this logic could be simpler.
        result = crew_instance.kickoff(inputs=inputs) 
        
        end_time = datetime.now()
        duration = end_time - start_time
        print(f"--- MAPPING SERVICE (HELPER): DdtAwsAdf().crew().kickoff() completed in {duration} ---")
        print(f"--- MAPPING SERVICE (HELPER): Result type from kickoff: {type(result)} ---")
        # We are now relying on files being created, so result.raw might not be the primary focus for all functions.
        if hasattr(result, "raw") and result.raw:
             print(f"--- MAPPING SERVICE (HELPER): Kickoff result.raw length: {len(result.raw)} ---")
        else:
             print("--- MAPPING SERVICE (HELPER): Kickoff result.raw is empty or not present. Relying on file outputs.")

    except Exception as e:
        print(f"--- MAPPING SERVICE (HELPER): ERROR during CrewAI kickoff: {str(e)} ---")
        traceback.print_exc()
        raise Exception(f"Error during CrewAI execution: {str(e)}")

def _read_output_file(filename: str) -> str:
    """Helper function to read an output file."""
    print(f"--- MAPPING SERVICE (HELPER): Attempting to read output file: {filename} ---")
    try:
        # Assuming files are created in the current working directory of the backend
        # For Docker, this would be /app
        # For local dev, this would be aws-azure-migration-tool/backend
        filepath = os.path.join(os.getcwd(), filename)
        print(f"--- MAPPING SERVICE (HELPER): Reading from absolute path: {filepath} ---")
        if not os.path.exists(filepath):
            print(f"--- MAPPING SERVICE (HELPER): ERROR - Output file not found: {filepath} ---")
            raise FileNotFoundError(f"Output file {filename} not found after CrewAI execution.")
            
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"--- MAPPING SERVICE (HELPER): Successfully read {len(content)} chars from {filename} ---")
        return content
    except FileNotFoundError:
        raise # Re-raise to be caught by the calling function
    except Exception as e:
        print(f"--- MAPPING SERVICE (HELPER): ERROR reading file {filename}: {str(e)} ---")
        traceback.print_exc()
        raise Exception(f"Error reading output file {filename}: {str(e)}")


def generate_mapping_report(glue_config: str, glue_script: str) -> str:
     # This function is now for the "Do All & Generate Report" button, 
     # which user indicated should show mapping_analyst output (mapping_report.md)
    print("--- MAPPING SERVICE: generate_mapping_report (for Do All button) called ---")
    inputs = {
        "topic": "AWS to Azure Migration", # This might need to be adjusted if tasks are specific
        "current_year": str(datetime.now().year),
        "aws_glue_job_definition": glue_config,
        "aws_python_script": glue_script,
    }
    print(f"Glue config length: {len(glue_config)} chars, Script length: {len(glue_script)} chars")
    
    _run_crew_and_get_outputs(inputs) # Run the crew, expecting it to generate files
    return _read_output_file(MAPPING_REPORT_FILENAME) # Return content of mapping_report.md

def get_adf_notebook_output(glue_config: str, glue_script: str) -> str:
    """
    Generates and returns the content of the ADF notebook (databricks_notebook.py).
    """
    print("--- MAPPING SERVICE: get_adf_notebook_output called ---")
    inputs = {
        "topic": "Generate ADF Notebook", # Topic might influence which tasks run, if crew is set up that way
        "current_year": str(datetime.now().year),
        "aws_glue_job_definition": glue_config,
        "aws_python_script": glue_script,
    }
    print(f"Glue config length: {len(glue_config)} chars, Script length: {len(glue_script)} chars")

    _run_crew_and_get_outputs(inputs) # Run the crew
    return _read_output_file(NOTEBOOK_OUTPUT_FILENAME) # Return content of databricks_notebook.py

def get_mapping_reference_output(glue_config: str, glue_script: str) -> str:
    """
    Generates and returns the content of the mapping reference (mapping_report.md).
    """
    print("--- MAPPING SERVICE: get_mapping_reference_output called ---")
    inputs = {
        "topic": "Generate Mapping Reference", # Topic might influence tasks
        "current_year": str(datetime.now().year),
        "aws_glue_job_definition": glue_config,
        "aws_python_script": glue_script,
    }
    print(f"Glue config length: {len(glue_config)} chars, Script length: {len(glue_script)} chars")
    
    _run_crew_and_get_outputs(inputs) # Run the crew
    return _read_output_file(MAPPING_REPORT_FILENAME) # Return content of mapping_report.md

# Old generate_mapping_report function body, for reference if needed, now refactored.
# The old function returned result.raw, which might be different from file contents.
# For now, all main report generation points to mapping_report.md as per user feedback.
'''
def generate_mapping_report_OLD(glue_config: str, glue_script: str) -> str:
    """
    Generate a migration mapping report using CrewAI.

    Args:
        glue_config: AWS Glue job configuration JSON as string
        glue_script: AWS Glue Python script as string

    Returns:
        Generated mapping report as markdown string
    """
    """
    Generate a migration mapping report using CrewAI.

    Args:
        glue_config: AWS Glue job configuration JSON as string
        glue_script: AWS Glue Python script as string

    Returns:
        Generated mapping report as markdown string
    """
    # This old body is now commented out and replaced by the new logic above.
    # The new generate_mapping_report calls _run_crew_and_get_outputs and then _read_output_file.
'''
