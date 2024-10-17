import os
import boto3
import re


def check_credentials(fucntion):
    """Check env variables for credentials"""

    def wrapper(*args, **kwargs):
        aws_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.getenv('AWS_ACCESS_KEY')

        if not aws_key_id:
            print('AWS_ACCESS_KEY_ID not set')
            exit(1)
        if not aws_secret_key:
            print('AWS_SECRET_ACCESS_KEY not set')
            exit(1)

        session = boto3.Session(
            aws_access_key_id=aws_key_id,
            aws_secret_access_key=aws_secret_key
        )

        return fucntion(*args, **kwargs, _session=session)

    return wrapper


@check_credentials
def list_all_in_bucket(
        bucket_name: str = "developer-task",
        directory: str = " TIE-sa",
        _session: boto3.Session = None
):
    """List all files in bucket under directory"""
    s3 = _session.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=directory)
    return [obj.key for obj in response]


@check_credentials
def find_in_bucket(
        bucket_name: str = "developer-task",
        directory: str = "TIE-sa",
        pattern: str = ".*",
        _session: boto3.Session = None
):
    """Find file in bucket under directory"""
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=directory)
    files = response['Contents']
    for file in files:
        if re.search(pattern, file['Key']):
            return file['Key']
    return None


@check_credentials
def upload_file_to_bucket(
        file_path: str,
        bucket_name: str = "developer-task",
        directory: str = "TIE-sa",
        _session: boto3.Session = None
):
    """Upload file to bucket under directory"""
    s3 = _session.resource('s3')
    s3.meta.client.upload_file(
        file_path,
        bucket_name,
        f"{directory}/{os.path.basename(file_path)}"
    )
    return f"File {file_path} uploaded"


@check_credentials
def delete_matching_files(
        bucket_name: str = "developer-task",
        directory: str = "TIE-sa",
        pattern: str = ".*",
        _session: boto3.Session = None
):
    """Delete files in bucket under directory that match pattern"""
    s3 = _session.resource('s3')
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=directory):
        if re.search(pattern, obj.key):
            obj.delete()
    return f"Files matching {pattern} deleted"


if __name__ == '__main__':
    print(list_all_in_bucket())
