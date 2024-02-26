import boto3
import os
import zipfile
from io import BytesIO

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Starting compressing...")
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print(bucket_name)
        print("     ")
        print(key)

        obj = s3.get_object(Bucket=bucket_name, Key=key)
        file_content = obj['Body'].read()
        
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(key, file_content)
        zip_buffer.seek(0)
        
        s3.put_object(Bucket=bucket_name, Key=f"{key}.zip", Body=zip_buffer)
        
        s3.delete_object(Bucket=bucket_name, Key=key)

    return {
        'statusCode': 200,
        'body': 'Object compressed and uploaded successfully'
    }
