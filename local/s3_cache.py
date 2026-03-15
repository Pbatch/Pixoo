import json
import os

import boto3


class S3Cache:
    def __init__(self):
        self.s3 = boto3.client("s3")
        self.bucket_name = os.environ["BUCKET_NAME"]

    def get(self, key):
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        except self.s3.exceptions.NoSuchKey:
            return {}, None

        last_updated = response["LastModified"].timestamp()
        results = json.loads(response["Body"].read().decode("utf-8"))
        return results, last_updated

    def save(self, results, key):
        self.s3.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=json.dumps(results),
            ContentType="application/json",
        )
