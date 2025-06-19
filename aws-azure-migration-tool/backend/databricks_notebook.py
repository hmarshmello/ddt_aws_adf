```python
 # Databricks notebook source
 # Databricks notebook code
 from pyspark.sql import SparkSession
 from pyspark.sql.functions import *

 # COMMAND ----------

 # Get the parameters passed from ADF
 dbutils.widgets.text("DATABASE_NAME", "sample_database", "DATABASE_NAME")
 DATABASE_NAME = dbutils.widgets.get("DATABASE_NAME")

 dbutils.widgets.text("TABLE_NAME", "sample_table", "TABLE_NAME")
 TABLE_NAME = dbutils.widgets.get("TABLE_NAME")

 dbutils.widgets.text("OUTPUT_PATH", "abfs://my-container@my-storageaccount.dfs.core.windows.net/processed-data/", "OUTPUT_PATH")
 OUTPUT_PATH = dbutils.widgets.get("OUTPUT_PATH")

 dbutils.widgets.text("JOB_NAME", "sample-glue-etl-job", "JOB_NAME")
 JOB_NAME = dbutils.widgets.get("JOB_NAME")

 # COMMAND ----------

 # Initialize Spark session
 spark = SparkSession.builder.appName(JOB_NAME).getOrCreate()

 # COMMAND ----------

 # Configure logging
 import logging
 logging.basicConfig(level=logging.INFO)
 logger = logging.getLogger(__name__)

 logger.info(f"Job started: {JOB_NAME}")
 logger.info(f"DATABASE_NAME: {DATABASE_NAME}, TABLE_NAME: {TABLE_NAME}, OUTPUT_PATH: {OUTPUT_PATH}")

 # COMMAND ----------

 # Function to read data from source (example using JDBC)
 def read_data_from_jdbc(database_name, table_name):
     """
     Reads data from a JDBC source using Spark.
     Replace with your actual JDBC connection details.
     """
     try:
         logger.info(f"Reading data from JDBC table: {database_name}.{table_name}")

         # Replace with your JDBC connection properties
         jdbc_url = "jdbc:your_jdbc_url"  # Example: "jdbc:sqlserver://your_server.database.windows.net:1433;database=your_database"
         jdbc_user = "your_user"
         jdbc_password = "your_password"
         jdbc_table = table_name

         df = spark.read.format("jdbc") \
             .option("url", jdbc_url) \
             .option("dbtable", jdbc_table) \
             .option("user", jdbc_user) \
             .option("password", jdbc_password) \
             .load()

         logger.info(f"Successfully read {df.count()} rows from JDBC table.")
         return df

     except Exception as e:
         logger.error(f"Error reading data from JDBC: {e}")
         raise

 # COMMAND ----------

 # Function to read data from source (example using ADLS Gen2)
 def read_data_from_adls(file_path, file_format="parquet"):
     """
     Reads data from Azure Data Lake Storage Gen2.
     """
     try:
         logger.info(f"Reading data from ADLS Gen2: {file_path}")
         df = spark.read.format(file_format).load(file_path)
         logger.info(f"Successfully read {df.count()} rows from ADLS Gen2.")
         return df
     except Exception as e:
         logger.error(f"Error reading data from ADLS Gen2: {e}")
         raise

 # COMMAND ----------

 # Function to perform data transformations
 def transform_data(df):
     """
     Performs data transformations.
     """
     try:
         logger.info("Performing data transformations.")

         # Example transformation: Drop a column
         if "some_column_to_drop" in df.columns:
             df = df.drop("some_column_to_drop")
             logger.info("Dropped column 'some_column_to_drop'.")
         else:
             logger.warning("Column 'some_column_to_drop' does not exist. Skipping.")

         # Add more transformations as needed
         df = df.withColumn("processed_time", current_timestamp())
         logger.info("Added 'processed_time' column.")

         return df

     except Exception as e:
         logger.error(f"Error during data transformation: {e}")
         raise

 # COMMAND ----------

 # Function to write data to the destination (Azure Blob Storage)
 def write_data_to_blob_storage(df, output_path, format="parquet"):
     """
     Writes data to Azure Blob Storage in Parquet format.
     """
     try:
         logger.info(f"Writing data to Azure Blob Storage: {output_path}")
         df.write.mode("overwrite").format(format).save(output_path)
         logger.info(f"Successfully wrote data to Azure Blob Storage.")

     except Exception as e:
         logger.error(f"Error writing data to Azure Blob Storage: {e}")
         raise

 # COMMAND ----------

 # Main ETL process
 def main():
     """
     Main ETL process.
     """
     try:
         # 1. Read data from source
         # Choose one of the read functions based on your source
         # df = read_data_from_jdbc(DATABASE_NAME, TABLE_NAME)
         data_path = "abfs://your-container@your-storageaccount.dfs.core.windows.net/input-data/sample.parquet"
         df = read_data_from_adls(data_path)
         # 2. Transform data
         transformed_df = transform_data(df)

         # 3. Write data to destination
         write_data_to_blob_storage(transformed_df, OUTPUT_PATH)

         logger.info("Job completed successfully.")

     except Exception as e:
         logger.error(f"Job failed: {e}")
         raise

 # COMMAND ----------

 # Run the main ETL process
 if __name__ == "__main__":
     main()
 ```