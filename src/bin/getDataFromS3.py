import boto
import sys, os
from boto.s3.key import Key
from boto.exception import S3ResponseError

DOWNLOAD_LOCATION_PATH = "{cwd}/{DN}".format(cwd=os.path.abspath(os.getcwd()),DN=os.getenv("LOCAL_DATA_DIR"))

BUCKET_NAME = os.getenv("BUCKET_NAME")
AWS_ACCESS_KEY_ID= os.getenv("AWS_ACCESS_KEY") # set your AWS_KEY_ID  on your environment path
AWS_ACCESS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY") # set your AWS_ACCESS_KEY  on your environment path

conn  = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_ACCESS_SECRET_KEY)
bucket = conn.get_bucket(BUCKET_NAME)

bucket_list = bucket.list()

for l in bucket_list:
    key_string = str(l.key)
    s3_path = DOWNLOAD_LOCATION_PATH + key_string
    try:
        l.get_contents_to_filename(s3_path)
    except (OSError,S3ResponseError) as e:
        pass
        if not os.path.exists(s3_path):
            try:
                os.makedirs(s3_path)
            except OSError as exc:
                import errno
                if exc.errno != errno.EEXIST:
                    raise
    break

