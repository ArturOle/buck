import os
import boto3


def check_credentials(fucntion):
    """Check env variables for credentials"""

    def wrapper(*args, **kwargs):
        if not os.getenv('AWS_ACCESS_KEY_ID'):
            print('AWS_ACCESS_KEY_ID not set')
            exit(1)
        if not os.getenv('AWS_ACCESS_KEY'):
            print('AWS_ACCESS_KEY not set')
            exit(1)

        return fucntion(*args, **kwargs)

    return wrapper


@check_credentials
def list_all_in_bucket(
        bucket_name: str = "developer-task",
        directory: str = "TIE-sa"
):
    """List all files in bucket under directory"""
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=directory)
    return response['Contents']




if __name__ == '__main__':
    print(list_all_in_bucket())
