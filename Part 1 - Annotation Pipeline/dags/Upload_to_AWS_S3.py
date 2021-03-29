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


print('All the files Uploaded to AWS S3')