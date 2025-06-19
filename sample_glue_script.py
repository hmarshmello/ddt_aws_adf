import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Get job arguments
args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'DATABASE_NAME',
    'TABLE_NAME',
    'OUTPUT_PATH'
])

# Initialize Spark and Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read data from Glue Data Catalog
datasource = glueContext.create_dynamic_frame.from_catalog(
    database=args['DATABASE_NAME'],
    table_name=args['TABLE_NAME'],
    transformation_ctx="datasource"
)

# Apply a transformation (example: drop a column)
transformed_datasource = datasource.drop_fields(['some_column_to_drop'])

# Write data to S3 in Parquet format
glueContext.write_dynamic_frame.from_options(
    frame=transformed_datasource,
    connection_type="s3",
    connection_options={"path": args['OUTPUT_PATH']},
    format="parquet",
    transformation_ctx="datasink"
)

job.commit()
