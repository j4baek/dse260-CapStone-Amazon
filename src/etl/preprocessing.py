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
## @type: DataSource
## @args: [database = "reviews", table_name = "metadata", transformation_ctx = "datasource0"]
## @return: datasource0
## @inputs: []
datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "reviews", table_name = "metadata", transformation_ctx = "datasource0")
## @type: ApplyMapping
## @args: [mapping = [("category", "array", "category", "array"), ("brand", "string", "brand", "string"), ("rank", "string", "rank", "string"), ("date", "string", "date", "string"), ("asin", "string", "asin", "string"), ("also_view", "array", "also_view", "array"), ("price", "string", "price", "string"), ("also_buy", "array", "also_buy", "array"), ("main_cat", "string", "main_cat", "string"), ("similar_item", "array", "similar_item", "array")], transformation_ctx = "applymapping1"]
## @return: applymapping1
## @inputs: [frame = datasource0]
applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("category", "array", "category", "array"), ("brand", "string", "brand", "string"), ("rank", "string", "rank", "string"), ("date", "string", "date", "string"), ("asin", "string", "asin", "string"), ("also_view", "array", "also_view", "array"), ("price", "string", "price", "string"), ("also_buy", "array", "also_buy", "array"), ("main_cat", "string", "main_cat", "string"), ("similar_item", "array", "similar_item", "array")], transformation_ctx = "applymapping1")
## @type: ResolveChoice
## @args: [choice = "make_struct", transformation_ctx = "resolvechoice2"]
## @return: resolvechoice2
## @inputs: [frame = applymapping1]
resolvechoice2 = ResolveChoice.apply(frame = applymapping1, choice = "make_struct", transformation_ctx = "resolvechoice2")
## @type: SplitFields
## @args: [paths = ["<paths>"], transformation_ctx = "<transformation_ctx>"]
## @return: <output>
## @inputs: [frame = <frame>]

## @type: Map
## @args: [f = <function>, transformation_ctx = "<transformation_ctx>"]
## @return: <output>
## @inputs: [frame = <frame>]

## @type: DropNullFields
## @args: [transformation_ctx = "dropnullfields3"]
## @return: dropnullfields3
## @inputs: [frame = resolvechoice2]
dropnullfields3 = DropNullFields.apply(frame = resolvechoice2, transformation_ctx = "dropnullfields3")

# def partitionCategory(dynamicRecord):
#     dynamicRecord['cid'] = dynamicRecord['category'][0]
#     dynamicRecord['scid'] = dynamicRecord['category'][1]
#     dynamicRecord['scid2'] = dynamicRecord['category'][2]
#     return dynamicRecord
	
products_dataframe = dropnullfields3.toDF()

category0 = udf(lambda x: x[0], StringType())
category1 = udf(lambda x: x[1], StringType())
category2 = udf(lambda x: x[2], StringType())
products_dataframe = products_dataframe.withColumn(
        "category0", category0(
            products_dataframe["category"])).withColumn(
                "category1", category1(
                    products_dataframe["category"])).withColumn(
                        "category2", category2(
                            products_dataframe["category"]))
products_dyf = products_dataframe.fromDF(products_dataframe, glueContext, "nested")

# mapCategory4 = Map.apply(frame = dropnullfields3, f = partitionCategory, transformation_ctx = "mapCategory4")


## @type: DataSink
## @args: [connection_type = "s3", connection_options = {"path": "s3://platform-data-lake-landing-zone-dev/amazon/stand"}, format = "parquet", transformation_ctx = "datasink4"]
## @return: datasink4
## @inputs: [frame = dropnullfields3]
datasink4 = glueContext.write_dynamic_frame.from_options(frame = products_dyf, connection_type = "s3", connection_options = {"path": "s3://platform-data-lake-landing-zone-dev/amazon/stand", "partitionKeys": ["category0", "category1", "category2"]}, format = "parquet", transformation_ctx = "datasink4")
job.commit()

