#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from ddt_aws_adf.crew import DdtAwsAdf

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew.
    """
    # Prompt user for file paths
    glue_config_path = input("Enter the path to your AWS Glue configuration file: ")
    glue_script_path = input("Enter the path to your AWS Glue script file: ")

    # Read file contents
    with open(glue_config_path, "r") as f:
        glue_config = f.read()
    with open(glue_script_path, "r") as f:
        glue_script = f.read()

    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year),
        "aws_glue_job_definition": glue_config,
        "aws_python_script": glue_script,
    }

    try:
        result = DdtAwsAdf().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

        # Print the result
        print("\n\n=== FINAL REPORT ===\n\n")
        print(result.raw)

        print("\n\nReport has been saved to output/report.md")


if __name__ == "__main__":
    run()

# def train():
#    """
#    Train the crew for a given number of iterations.
#    """
#    inputs = {
#        "topic": "AI LLMs",
#        'current_year': str(datetime.now().year)
#    }
#    try:
#        DdtAwsAdf().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
#
#    except Exception as e:
#        raise Exception(f"An error occurred while training the crew: {e}")
#
# def replay():
#    """
#    Replay the crew execution from a specific task.
#    """
#    try:
#        DdtAwsAdf().crew().replay(task_id=sys.argv[1])
#
#    except Exception as e:
#        raise Exception(f"An error occurred while replaying the crew: {e}")
#
# def test():
#    """
#    Test the crew execution and returns the results.
#    """
#    inputs = {
#        "topic": "AI LLMs",
#        "current_year": str(datetime.now().year)
#    }
#
#    try:
#        DdtAwsAdf().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
#
#    except Exception as e:
#        raise Exception(f"An error occurred while testing the crew: {e}")
#
