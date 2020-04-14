import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# catalog: database and table names
db_name = "reviews"
tbl_metadata = "metadata"
# db_name = "amazon"
# tbl_metadata = "amazon_metadata"
# tbl_5core = "amazon_5core"

# s3 output directories
amazon_products = 's3://platform-data-lake-landing-zone-dev/amazon/products'
amazon_reviews = 's3://platform-data-lake-landing-zone-dev/amazon/reviews'

## @type: DataSource
## @args: [database = "reviews", table_name = "metadata", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = db_name, table_name = tbl_metadata, transformation_ctx = "datasource0")

## @type: ApplyMapping
## @args: [mapping = [("category", "array", "category", "array"), ("brand", "string", "brand", "string"), ("rank", "string", "rank", "string"), ("date", "string", "date", "string"), ("asin", "string", "asin", "string"), ("also_view", "array", "also_view", "array"), ("price", "string", "price", "string"), ("also_buy", "array", "also_buy", "array"), ("main_cat", "string", "main_cat", "string"), ("similar_item", "array", "similar_item", "array")], transformation_ctx = "applymapping1"]
## @return: applymapping1
## @inputs: [frame = datasource0]
applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [
    ("asin", "string", "asin", "string"), 
    ("brand", "string", "brand", "string"), 
    ("rank", "string", "rank", "string"), 
    ("date", "string", "date", "string"), 
    ("price", "string", "price", "string"), 
    ("main_cat", "string", "main_cat", "string"), ## maybe gone
    ("also_buy", "array", "also_buy", "array"), 
    ("also_view", "array", "also_view", "array"), 
    ("similar_item", "array", "similar_item", "array"), ## maybe gone
    ("category", "array", "category", "array")
], transformation_ctx = "applymapping1")

## @type: ResolveChoice
## @args: [choice = "make_struct", transformation_ctx = "resolvechoice2"]
## @return: resolvechoice2
## @inputs: [frame = applymapping1]
resolvechoice2 = ResolveChoice.apply(frame = applymapping1, choice = "make_struct", transformation_ctx = "resolvechoice2")

## @type: DropNullFields
## @args: [transformation_ctx = "dropnullfields3"]
## @return: dropnullfields3
## @inputs: [frame = resolvechoice2]
dropnullfields3 = DropNullFields.apply(frame = resolvechoice2, transformation_ctx = "dropnullfields3")

products_dataframe = dropnullfields3.toDF()

category0 = udf(lambda x: x[0], StringType())
category1 = udf(lambda x: x[1], StringType())
category2 = udf(lambda x: x[2], StringType())
products_dataframe_part = products_dataframe.withColumn(
        "category0", category0(
            products_dataframe["category"])).withColumn(
                "category1", category1(
                    products_dataframe["category"])).withColumn(
                        "category2", category2(
                            products_dataframe["category"]))

products_dataframe_part.write.parquet(amazon_products, partitionBy=["category0", "category1", "category2"])
job.commit()

