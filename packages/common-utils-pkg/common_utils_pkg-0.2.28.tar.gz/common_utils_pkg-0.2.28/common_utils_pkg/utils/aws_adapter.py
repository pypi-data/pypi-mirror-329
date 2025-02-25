from .logger import Logger

import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError


class AWSAdapter:
    def __init__(self, logger: Logger, region):
        self.logger = logger.create_prefix("AWSAdapter")
        self.region = region

    def upload_file_to_s3(self, bucket_name, file_path, file_key):
        try:
            self.logger.info(
                f"Uploading file {file_path} to Bucket (region: {self.region}): {bucket_name} -> {file_key}"
            )
            s3_resource = boto3.resource("s3", region_name=self.region)
            config = TransferConfig(
                multipart_threshold=1024 * 25,
                max_concurrency=10,
                multipart_chunksize=1024 * 25,
                use_threads=True,
            )
            s3_resource.Bucket(bucket_name).upload_file(file_path, file_key, Config=config)
            self.logger.info(f"File {file_path} uploaded")
        except ClientError as e:
            self.logger.error(
                f"Error uploading file {file_path} to Bucket: {bucket_name} -> {file_key}: {e.response['Error']['Message']}",
                notify=True,
            )

    def get_parameter(self, name, with_decryption=False):
        try:
            self.logger.info(f"Fetching parameter {name} from aws SSM")
            ssm_client = boto3.client("ssm", region_name=self.region)
            parameter = ssm_client.get_parameter(Name=name, WithDecryption=with_decryption)
            return parameter["Parameter"]["Value"]
        except Exception as e:
            self.logger.error(f"Error fetching parameter from AWS SSM: {e}", notify=True)


def get_parameter(region, name, with_decryption=False):
    ssm_client = boto3.client("ssm", region_name=region)
    parameter = ssm_client.get_parameter(Name=name, WithDecryption=with_decryption)
    return parameter["Parameter"]["Value"]
