# AWS Glue to Azure Data Factory Migration: `sample-glue-etl-job`

## 1. Executive Summary

This document outlines the migration of the AWS Glue ETL job `sample-glue-etl-job` to Azure Data Factory. The primary purpose of this job is to extract, transform, and load data from an AWS Glue Data Catalog table to an S3 bucket in Parquet format. The migration involves re-implementing the Glue job's logic using Azure Databricks and orchestrating the execution through Azure Data Factory. Key technologies involved are AWS Glue, S3, Python, Spark, Azure Data Factory, Azure Databricks, and Azure Blob Storage. The main goal is to migrate this job to Azure with minimal code changes and to ensure the same functionality.

## 2. Assumptions and Decisions

- **Compute Environment:** We will use Azure Databricks as the compute engine for the transformation logic because it supports Spark and Python, allowing us to reuse much of the existing Glue script.
- **Data Storage:** S3 data will be accessed by Azure Databricks using the abfs connector. We will configure the Azure Databricks cluster to access the S3 bucket.
- **Orchestration:** Azure Data Factory will be used to orchestrate the Databricks notebook execution.
- **Authentication:** We will use Managed Identities for Azure resources to securely access data and services.
- **Parameterization:** Job parameters in AWS Glue will be passed as parameters to the Databricks notebook via Azure Data Factory.
- **Error Handling:** Error handling will be implemented in the Databricks notebook to ensure robust data processing. We will also configure retry policies in Azure Data Factory.
- **Logging and Monitoring:** Azure Monitor will be leveraged for monitoring the ADF pipeline and Databricks job execution.
- **Connection Migration:** The AWS Glue connection `my-jdbc-connection` requires a corresponding Azure Linked Service to be created. It may involve an Azure Key Vault Secret to store connection credentials. If this connection isn't used in the python script, it could be left out of the current migration.
- **Temporary Directory:** The `TempDir` parameter will be mapped to an Azure Blob Storage path for temporary storage during Spark processing.

## 3. Azure Data Factory Pipeline Definition

```json
{
  "name": "pl_etl_process_data",
  "properties": {
    "description": "Pipeline to execute Databricks notebook for data processing",
    "parameters": {
      "DATABASE_NAME": {
        "type": "string",
        "defaultValue": "sample_database"
      },
      "TABLE_NAME": {
        "type": "string",
        "defaultValue": "sample_table"
      },
      "OUTPUT_PATH": {
        "type": "string",
        "defaultValue": "abfs://my-container@my-storageaccount.dfs.core.windows.net/processed-data/"
      },
      "JOB_NAME":{
        "type": "string",
        "defaultValue": "sample-glue-etl-job"
      }
    },
    "activities": [
      {
        "name": "DatabricksNotebookActivity",
        "type": "DatabricksNotebook",
        "dependsOn": [],
        "userProperties": [],
        "typeProperties": {
          "notebookPath": "/Repos/my-repo/sample_glue_script",
          "baseParameters": {
            "DATABASE_NAME": {
              "value": "@pipeline().parameters.DATABASE_NAME",
              "type": "string"
            },
            "TABLE_NAME": {
              "value": "@pipeline().parameters.TABLE_NAME",
              "type": "string"
            },
            "OUTPUT_PATH": {
              "value": "@pipeline().parameters.OUTPUT_PATH",
              "type": "string"
            },
            "JOB_NAME": {
              "value": "@pipeline().parameters.JOB_NAME",
              "type": "string"
            }
          }
        },
        "linkedServiceName": {
          "referenceName": "ls_databricks",
          "type": "LinkedServiceReference"
        },
        "timeout": "1.00:00:00",
        "retry": 0,
        "retryIntervalInSeconds": 30,
        "concurrency": 1
      }
    ],
    "annotations": [],
    "lastPublishTime": "2024-01-01T00:00:00Z"
  }
}
```

## 4. Azure Linked Services

- **ls_azure_blob_storage:**  (For accessing temporary storage)
  - *Type:* Azure Blob Storage
  - *Authentication:* Managed Identity
  - *Account Selection Method:* From Azure subscription
  - *Subscription:* Your Azure Subscription
  - *Storage Account Name:* Your Storage Account Name

- **ls_databricks:** (For connecting to the Databricks workspace)
  - *Type:* Azure Databricks
  - *Authentication:* Managed Identity
  - *Existing cluster ID:*  Your Databricks Cluster ID
  - *Workspace URL:* Your Databricks Workspace URL

- **ls_s3:** (Placeholder for S3 connection, will configure within Databricks)
  - *Type:* Amazon S3 (This is a placeholder, configure access within Databricks cluster)
  - Authentication: IAM Role (Configure within Databricks cluster)
    * Access Key and Secret Key (Not recommended, use IAM roles instead within databricks)

- **ls_jdbc:** (Placeholder for `my-jdbc-connection`)
    * Type: Azure SQL Database/Synapse Analytics/etc. (Based on the type of the original JDBC connection)
    * Authentication: Managed Identity/SQL Authentication (Using Azure Key Vault for storing credentials is recommended)
    * Server: Your Server Name
    * Database: Your Database Name

## 5. Azure Datasets

Since the data source is the AWS Glue Data Catalog and the target is S3 (accessed through Databricks), explicit Azure Datasets are not strictly required. The data source and target paths will be defined within the Databricks notebook using parameters.

## 6. Azure Databricks Notebook

```python
# Databricks notebook code
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import SparkSession

# COMMAND ----------

# Get the parameters passed from ADF
DATABASE_NAME = dbutils.widgets.get("DATABASE_NAME")
TABLE_NAME = dbutils.widgets.get("TABLE_NAME")
OUTPUT_PATH = dbutils.widgets.get("OUTPUT_PATH")
JOB_NAME = dbutils.widgets.get("JOB_NAME")


# Initialize Spark and Glue context
spark = SparkSession.builder.appName(JOB_NAME).getOrCreate()
glueContext = GlueContext(spark.sparkContext)
job = Job(glueContext)
job.init(JOB_NAME, {})

# Configure access to S3 bucket
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", "<YOUR_ACCESS_KEY>")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "<YOUR_SECRET_KEY>")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.amazonaws.com")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")


# Read data from Glue Data Catalog
try:
  df = glueContext.create_dynamic_frame.from_catalog(database = DATABASE_NAME, table_name = TABLE_NAME, transformation_ctx = "data_source").toDF()

  # Perform transformations (Example: dropping a column)
  df = df.drop("some_column_to_drop")

  # Write data to Azure Blob Storage in Parquet format
  df.write.mode("overwrite").parquet(OUTPUT_PATH)

  job.commit()

except Exception as e:
  print(f"Job failed: {e}")
  job.commit()
  raise e
```

**Changes Needed:**

- Replace `create_dynamic_frame.from_catalog` with reading data directly using Spark, potentially leveraging the `ls_jdbc` Linked Service in ADF to get connection information if the source data comes from a JDBC connection in Glue.
- Replace S3 path in the dataframe with Azure Blob Storage paths (ABFS).
- The AWS Glue specific imports might need to be adjusted based on how the data source is to be accessed in Azure
- Handle any library dependencies differences between the Glue environment and the Databricks cluster by installing the necessary libraries to the Databricks cluster.
- Add proper error handling and logging (using Databricks utilities).
- Replace AWS Glue Job bookmark functionality with custom logic if needed.
- Remove `awsglue` library-specific operations, use standard PySpark equivalents instead.

## 7. Mapping Table

| AWS Glue Configuration          | Azure Equivalent                                       | Notes                                                                                                                                                   |
|---------------------------------|--------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `job_name`                      | ADF Pipeline Name, Databricks Notebook Name            | Use ADF naming conventions (e.g., `pl_etl_process_data`). Use descriptive name for notebook in Databricks.                                             |
| `job_type`                      | Azure Databricks Notebook Activity                    | Designate the activity type in ADF.                                                                                                                    |
| `script_location`               | Databricks Notebook Path                               | Specify the path to the Databricks notebook within the Databricks workspace (e.g., `/Repos/my-repo/sample_glue_script`).                                  |
| `script_language`               | Databricks Notebook Language (Python)                 | Ensure the Databricks cluster is configured to support the required language.                                                                           |
| `glue_version`                  | Databricks Runtime Version                             | Choose a Databricks runtime that is compatible with the Spark version used in the Glue job.                                                               |
| `role`                          | Managed Identity for ADF and Databricks                | Grant the ADF Managed Identity appropriate permissions to access Azure Blob Storage and Databricks. Grant Databricks Managed Identity permissions to access Storage and other resources.  |
| `max_concurrent_runs`           | ADF Pipeline Concurrency                               | Set the `concurrency` property of the ADF pipeline.                                                                                                   |
| `max_retries`                   | ADF Activity Retry                                     | Configure the `retry` and `retryIntervalInSeconds` properties of the Databricks Notebook activity in ADF.                                                 |
| `timeout`                       | ADF Activity Timeout                                   | Set the `timeout` property of the Databricks Notebook activity in ADF. Convert seconds to ADF timeout format (e.g., `1.00:00:00` for 2880 seconds).     |
| `max_capacity` / `number_of_workers` / `worker_type` | Databricks Cluster Configuration                 | Configure the Databricks cluster with appropriate worker types and autoscaling settings to match the Glue job's capacity.                  |
| `connections`                   | Azure Linked Services                                    | Create corresponding Azure Linked Services for the connections. Consider using Azure Key Vault to store connection strings.                                  |
| `tags`                          | ADF Pipeline Annotations                               | Use annotations in ADF to store metadata or tags for the pipeline.                                                                                    |
| `default_arguments` (`--job-language`, `--job-bookmark-option`, etc.) | Databricks Notebook Parameters                           | Pass these as parameters to the Databricks notebook using the `baseParameters` property of the Databricks Notebook activity in ADF.                   |
| `data_source`                   | Spark Data Source (within Databricks notebook)          | Use Spark to read data from the data source. If the data source is JDBC, configure the connection using the Azure Linked Service.                                                       |
| `data_target`                   | Spark Data Target (within Databricks notebook)          | Use Spark to write data to the desired destination (e.g., Azure Blob Storage in Parquet format).                                                                 |
| `python_script_details`         | Databricks Notebook Code                               | Replicate the transformation logic in the Databricks notebook using Spark and Python.                                                                    |
| S3 Bucket Access | Databricks Cluster configuration and Secrets  |  Configure the Databricks cluster to have the appropriate IAM role or configure spark to use secrets to connect to S3. |
| Glue Catalog | Spark Metastore or External Hive Metastore | If using Glue Catalog, replace the catalog with Spark's Metastore capability and use it. |
| TempDir | Azure Blob Storage Path | Map the temp directory to Azure Blob Storage and ensure the Databricks cluster has permission to it. |

## 8. Post-Migration Considerations

- **Testing:**
  - Perform end-to-end testing to ensure data integrity and accuracy.
  - Compare the output of the Azure Data Factory pipeline with the output of the original AWS Glue job.
  - Test different data volumes and scenarios to validate performance and scalability.
- **Performance Tuning:**
  - Monitor the performance of the Databricks cluster and adjust the cluster size and configuration as needed.
  - Optimize the Spark code in the Databricks notebook for performance.
  - Consider using Delta Lake for improved performance and reliability.
- **Cost Optimization:**
  - Right-size the Databricks cluster to match the workload requirements.
  - Leverage Azure Spot Instances for cost savings.
  - Monitor ADF pipeline execution costs and identify opportunities for optimization.
- **Monitoring and Alerting:**
  - Configure Azure Monitor to monitor the ADF pipeline and Databricks job execution.
  - Set up alerts for failures, performance degradation, and other critical events.
  - Implement logging in the Databricks notebook to capture detailed information about job execution.
- **Security:**
  - Regularly review and update security configurations.
  - Use Azure Key Vault to store sensitive information such as database credentials and access keys.
  - Implement network security measures to protect data in transit and at rest.
- **Dependencies:**
  - Manage any new dependencies introduced during migration of this job.
  - Keep track of library and package versions.
