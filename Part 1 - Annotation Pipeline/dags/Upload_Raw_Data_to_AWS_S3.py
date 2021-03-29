def upload_to_aws(local_file, bucket, s3_file):
    import boto3
    from botocore.exceptions import NoCredentialsError
    ACCESS_KEY = 'AKIA5CUSOFRV64J75U7W'
    SECRET_KEY = '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'
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


# uploading all unstructured files to S3
def upload_files(path):
    session = boto3.Session(
        aws_access_key_id='AKIA5CUSOFRV64J75U7W',
        aws_secret_access_key='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',
        region_name='us-east-2'
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket('edgarteam3')

    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                bucket.put_object(Key=full_path[len(path) + 1:], Body=data)


print('Upload to S3 Done!!!!!!!')