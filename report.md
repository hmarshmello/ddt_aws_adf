# AWS Glue to Azure Data Factory Migration Guide

## 1. Executive Summary

This document outlines the migration of an AWS Glue ETL job, named `sample-glue-etl-job`, to Azure Data Factory (ADF). The Glue job is a Spark-based ETL process that reads data from the AWS Glue Data Catalog, transforms it, and writes it to Amazon S3 in Parquet format. The primary business purpose is data transformation and loading for analytical purposes. The migration strategy involves replicating the functionality of the Glue job using Azure Data Factory, Azure Databricks, and Azure Data Lake Storage (ADLS) Gen2. The source environment utilizes AWS Glue, S3, and the Glue Data Catalog, while the target environment leverages Azure Data Factory, Azure Databricks, Azure Data Lake Storage Gen2, and Azure Synapse Analytics (optional for target data warehouse).

## 2. Assumptions and Decisions

*   **Assumption:** Access to both AWS and Azure environments is pre-configured with appropriate permissions.
*   **Decision:** Utilize Azure Databricks for Spark-based data transformation due to its compatibility with PySpark, the same engine used in AWS Glue.
*   **Decision:** Migrate data stored in S3 to Azure Data Lake Storage Gen2 (ADLS Gen2) for optimized storage and performance in Azure.
*   **Decision:** Employ Azure Key Vault for securely storing and managing secrets, such as connection strings and access keys.
*   **Decision:** Use Managed Identities for Azure resources to simplify authentication and authorization.
*   **Challenge:** Translating AWS Glue Data Catalog to Azure Data Lake Storage Gen2 and external tables in Azure Synapse Analytics or Azure Data Lake Analytics. This will be handled by creating external tables pointing to the data in ADLS Gen2.
*   **Challenge:** AWS Glue uses a specific set of libraries. Ensuring equivalent libraries are available/imported into the Azure Databricks environment. This can be handled by creating init scripts or installing required packages in the Databricks cluster.

## 3. Azure Data Factory Pipeline Definition

Pipeline Name: `pl_etl_sampleGlueJob_migrate`

Description: Migrated pipeline from AWS Glue job 'sample-glue-etl-job'.

Parameters:

*   `databaseName` (String): Name of the source database (default: `sample_database`).
*   `tableName` (String): Name of the source table (default: `sample_table`).
*   `outputPath` (String): Output path in ADLS Gen2 (default: `abfss://<container>@<storageAccount>.dfs.core.windows.net/processed-data/`).
*   `jdbcConnectionName` (String): Name of the JDBC connection.

Activities:

1.  **Activity Name:** `GetMetadata_SourceData`
    *   **Type:** Get Metadata
    *   **Description:** Get metadata of the source data in ADLS Gen2 to validate the data exists
    *   **Dataset:** `ds_adls_source`
    *   **Field List:** `exists`
    *   **Settings**:
        *   `Format`: `Parquet`
        *   `Compression type`: `None`

2.  **Activity Name:** `DatabricksNotebook_TransformData`
    *   **Type:** Databricks Notebook
    *   **Description:** Executes the Databricks notebook for data transformation.
    *   **Linked Service:** `ls_databricks`
    *   **Settings:**
        *   **Notebook path:** `/Repos/<user>/<repo>/sample_glue_script`
        *   **Base Parameters:**
            *   `databaseName`: `@pipeline().parameters.databaseName`
            *   `tableName`: `@pipeline().parameters.tableName`
            *   `outputPath`: `@pipeline().parameters.outputPath`
            *   `jdbcConnectionName`: `@pipeline().parameters.jdbcConnectionName`

3.  **Activity Name:** `CopyData_TargetStorage` (Optional, if writing to a different format or location after Databricks)
    *   **Type:** Copy Data
    *   **Description:** Copies the transformed data from the Databricks output location to the final target location.
    *   **Source Dataset:** `ds_adls_transformed`
    *   **Sink Dataset:** `ds_adls_target`
    *    **Copy Settings:**
          *   `Data Integration Unit`: `Auto`
          *   `Enable Staging`: `false`

Settings mapped from AWS Glue:

*   **Timeout:** 2880 seconds (map to Activity Timeout in ADF - 48 hours).
*   **Retry:** 0 (map to Activity Retry in ADF).
*   **Concurrency:** MaxConcurrentRuns = 1 (handled at pipeline level with Trigger settings or manual scheduling).

## 4. Azure Linked Services

*   `ls_adls_source`: Linked Service to Azure Data Lake Storage Gen2 (Source).
    *   **Authentication:** Managed Identity
    *   **Account selection method:** From Azure subscription
    *   **URL:** `abfss://<container>@<storageAccount>.dfs.core.windows.net`
*   `ls_adls_target`: Linked Service to Azure Data Lake Storage Gen2 (Target).
    *   **Authentication:** Managed Identity
    *   **Account selection method:** From Azure subscription
    *   **URL:** `abfss://<container>@<storageAccount>.dfs.core.windows.net`
*   `ls_databricks`: Linked Service to Azure Databricks.
    *   **Authentication:** Managed Identity
    *   **Existing cluster id`: `<cluster-id>`
    *   **Workspace URL:** `https://<databricks-instance>.azuredatabricks.net`
*   `ls_jdbc`: (Placeholder) Linked Service to the JDBC connection (my-jdbc-connection), if used in Databricks.
    *   **Authentication:** Azure Key Vault (store credentials securely).
    *   **Connection String:** Stored in Azure Key Vault.

## 5. Azure Datasets

*   `ds_adls_source`: Dataset for source data in ADLS Gen2.
    *   **Linked Service:** `ls_adls_source`
    *   **File path:** `@dataset().SourcePath`
    *   **Format:** Parquet
    *   **Schema:** (Define the schema if known, otherwise, can be schema on read)

*   `ds_adls_transformed`: Dataset representing the transformed data outputted by the Databricks notebook in ADLS Gen2.
    *   **Linked Service:** `ls_adls_target`
    *   **File path:** `@dataset().OutputPath`
    *   **Format:** Parquet
    *   **Parameters:**
        *   `OutputPath` (String): Path to the transformed data.

*   `ds_adls_target`: Dataset for the final target location in ADLS Gen2.
    *   **Linked Service:** `ls_adls_target`
    *   **File path:** `@pipeline().parameters.outputPath`
    *   **Format:** Parquet

## 6. Azure Databricks Notebook

The Python script from AWS Glue ( `s3://my-glue-scripts/sample_glue_script.py`) needs to be adapted to run in Azure Databricks.

Key changes:

*   Replace AWS Glue specific libraries (e.g., `awsglue.transforms`, `awsglue.utils`) with their PySpark equivalents or alternative libraries where necessary.
*   Modify data source and target connections to use Azure Data Lake Storage Gen2 instead of S3.  Use `spark.read.parquet` and `spark.write.parquet` with ADLS Gen2 paths.
*   Use `dbutils.widgets` to handle pipeline parameters passed from Azure Data Factory.
*   Implement error handling and logging using Databricks utilities and standard Python logging.
*   Read JDBC connection details from Azure Key Vault using Databricks secrets.

Example Databricks Notebook Code Snippet:

```python
# Databricks notebook source
dbutils.widgets.text("databaseName", "sample_database", "Database Name")
dbutils.widgets.text("tableName", "sample_table", "Table Name")
dbutils.widgets.text("outputPath", "abfss://<container>@<storageAccount>.dfs.core.windows.net/processed-data/", "Output Path")
dbutils.widgets.text("jdbcConnectionName", "my-jdbc-connection", "JDBC Connection Name")

databaseName = dbutils.widgets.get("databaseName")
tableName = dbutils.widgets.get("tableName")
outputPath = dbutils.widgets.get("outputPath")
jdbcConnectionName = dbutils.widgets.get("jdbcConnectionName")

# Read data from ADLS Gen2 (replace with your actual source)
try:
    df = spark.read.table(f"{databaseName}.{tableName}") # Assuming source is already in Delta Lake.  If not, use spark.read.format("parquet").load("<path>")
    print("Successfully read source data.")
except Exception as e:
    print(f"Error reading source data: {e}")
    raise

# Example Transformation: Drop Columns
columns_to_drop = ['column1', 'column2']
df_transformed = df.drop(*columns_to_drop)

# Write data to ADLS Gen2 in Parquet format
try:
    df_transformed.write.mode("overwrite").parquet(outputPath)
    print(f"Successfully wrote transformed data to {outputPath}")
except Exception as e:
    print(f"Error writing data to ADLS Gen2: {e}")
    raise

#Example of reading JDBC connection details from Key Vault (using Databricks secrets)
# Replace with your actual Key Vault scope and secret name
# jdbcUsername = dbutils.secrets.get(scope="my-key-vault-scope", key="jdbc-username")
# jdbcPassword = dbutils.secrets.get(scope="my-key-vault-scope", key="jdbc-password")
```

## 7. Mapping Table

| AWS Glue Configuration          | Azure Equivalent                                       | Notes                                                                                                                                   |
|---------------------------------|--------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| **Job Overview**                |                                                        |                                                                                                                                         |
| JobName                         | ADF Pipeline Name (`pl_etl_sampleGlueJob_migrate`)    | Follow ADF naming conventions.                                                                                                        |
| JobType                         | Azure Databricks (Spark)                               | Spark transformation handled in Databricks.                                                                                              |
| GlueVersion                     | Databricks Runtime Version                              | Specify the Databricks runtime version in the Databricks cluster configuration.                                                           |
| Description                     | ADF Pipeline Description                               | Document the purpose of the pipeline.                                                                                                   |
| **Script Details**              |                                                        |                                                                                                                                         |
| ScriptLocation                  | Databricks Notebook Path                               | Path to the Databricks notebook in the Databricks workspace.                                                                              |
| ScriptLanguage                  | Python (PySpark)                                       | Ensure Databricks cluster is configured with Python.                                                                                    |
| MainLibraries                   | Python Libraries in Databricks                         | Install required Python libraries in the Databricks cluster using init scripts or the Databricks UI.                                        |
| Transformations                 | PySpark Transformations in Databricks Notebook          | Implement the transformations using PySpark code within the Databricks notebook.                                                          |
| **Data Sources**                |                                                        |                                                                                                                                         |
| SourceType                      | Azure Data Lake Storage Gen2 or Azure Synapse Analytics | Data is read from ADLS Gen2 or an external table in Synapse.                                                                             |
| DatabaseName                    | Parameter in ADF Pipeline and Databricks Notebook      | Passed as a parameter to the Databricks notebook.                                                                                       |
| TableName                       | Parameter in ADF Pipeline and Databricks Notebook      | Passed as a parameter to the Databricks notebook.                                                                                       |
| ConnectionType                  | Azure Linked Service                                   | Use an Azure Linked Service to connect to the data source (ADLS Gen2).                                                                  |
| **Data Targets**                |                                                        |                                                                                                                                         |
| TargetType                      | Azure Data Lake Storage Gen2                           | Data is written to ADLS Gen2.                                                                                                          |
| OutputPath                      | Parameter in ADF Pipeline and Databricks Notebook      | Passed as a parameter to the Databricks notebook.                                                                                       |
| OutputFormat                    | Parquet                                                | Specify the output format in the Databricks notebook (e.g., `df.write.parquet()`).                                                             |
| ConnectionType                  | Azure Linked Service                                   | Use an Azure Linked Service to connect to the data target (ADLS Gen2).                                                                  |
| **Job Parameters and Arguments** |                                                        |                                                                                                                                         |
| RequiredArguments               | ADF Pipeline Parameters                                | Define required arguments as parameters in the ADF pipeline.                                                                              |
| DefaultArguments                | Default Values in ADF Pipeline Parameters and Databricks | Set default values for parameters in the ADF pipeline and within the Databricks notebook using `dbutils.widgets`.                          |
| `--job-language`               | N/A                                                    | Handled by the Databricks environment.                                                                                                    |
| `--job-bookmark-option`        | N/A                                                    | Azure Data Factory and Databricks handle state management differently. Consider using Delta Lake for change data capture.                |
| `--enable-metrics`             | Azure Monitor                                          | Use Azure Monitor to collect and analyze metrics.                                                                                         |
| `--enable-continuous-cloudwatch-log` | Azure Monitor Logs                                 | Use Azure Monitor Logs to collect and analyze logs. Configure logging in the Databricks notebook.                                           |
| `--enable-spark-ui`            | Spark UI in Databricks                                 | Access the Spark UI through the Databricks UI.                                                                                            |
| `--spark-event-logs-path`      | Azure Blob Storage or ADLS Gen2                       | Configure Spark event logs to be stored in Azure Blob Storage or ADLS Gen2.                                                              |
| `--TempDir`                    | ADLS Gen2                                              | Use ADLS Gen2 as the temporary directory for Spark jobs in Databricks. Configure in Spark configuration.                                    |
| **Connections**                 |                                                        |                                                                                                                                         |
| ConnectionsUsed                 | Azure Linked Services                                   | Create Azure Linked Services for each connection required by the job (e.g., JDBC connection). Store credentials in Azure Key Vault.      |
| **Security Configuration**      |                                                        |                                                                                                                                         |
| IAMRole                         | Managed Identity                                       | Use Managed Identities for Azure resources to grant necessary permissions.                                                                  |
| **Resource Allocation and Execution** |                                                        |                                                                                                                                         |
| MaxConcurrentRuns               | ADF Trigger Concurrency                                | Control concurrency through ADF trigger settings.                                                                                          |
| MaxRetries                      | ADF Activity Retry                                     | Configure retry attempts in the ADF activity settings.                                                                                     |
| AllocatedCapacity/MaxCapacity/NumberOfWorkers/WorkerType | Databricks Cluster Configuration | Configure the Databricks cluster with appropriate resources (e.g., worker type, number of workers) to match the allocated capacity.   |
| Timeout                         | ADF Activity Timeout                                     | Set the timeout for the Databricks notebook activity in ADF.                                                                               |
| **Tags**                        | ADF Pipeline Tags                                      | Add tags to the ADF pipeline for organizational purposes.                                                                                 |

## 8. Post-Migration Considerations

*   **Testing:**
    *   **Data Validation:** Implement data validation checks to ensure data integrity after migration. Compare row counts and data samples between the source (AWS S3) and target (ADLS Gen2).
    *   **Functional Testing:** Verify that the migrated ETL process produces the same results as the original Glue job.
    *   **Performance Testing:** Conduct performance testing to identify and address any performance bottlenecks.

*   **Performance Tuning:**
    *   **Databricks Cluster Optimization:** Optimize the Databricks cluster configuration based on the workload requirements. Consider autoscaling to dynamically adjust resources.
    *   **Data Partitioning:** Partition data in ADLS Gen2 and Databricks for improved query performance.
    *   **Caching:** Utilize caching mechanisms in Databricks to improve performance of frequently accessed data.

*   **Cost Optimization:**
    *   **Databricks Cluster Sizing:** Right-size the Databricks cluster to avoid over-provisioning resources.
    *   **ADLS Gen2 Storage Tiering:** Use appropriate storage tiers in ADLS Gen2 based on data access patterns (hot, cool, archive).
    *   **ADF Pipeline Scheduling:** Optimize the pipeline schedule to minimize costs.

*   **Monitoring and Alerting:**
    *   **Azure Monitor:** Configure Azure Monitor to monitor the ADF pipeline and Databricks cluster performance.
    *   **Alerting:** Set up alerts for critical events, such as pipeline failures, performance degradation, and cost overruns.
    *   **Logging:** Implement comprehensive logging in the Databricks notebook to facilitate troubleshooting and monitoring.
