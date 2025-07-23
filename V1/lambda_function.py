import boto3
from PIL import Image
import io
import os

s3 = boto3.client('s3')

def resize_image(image_data, size=(800, 800)):
    with Image.open(io.BytesIO(image_data)) as img:
        img.thumbnail(size)
        output = io.BytesIO()
        img.save(output, format=img.format)
        output.seek(0)
        return output

def lambda_handler(event, context):
    # Parse S3 event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']
    
    destination_bucket = os.environ.get('DEST_BUCKET', source_bucket)
    destination_key = f"resized/{source_key}"
    
    # Download the image
    response = s3.get_object(Bucket=source_bucket, Key=source_key)
    image_data = response['Body'].read()
    
    # Resize
    resized_image = resize_image(image_data, size=(800, 800))
    
    # Upload
    s3.put_object(
        Bucket=destination_bucket,
        Key=destination_key,
        Body=resized_image,
        ContentType=response['ContentType']
    )
    
    return {
        'statusCode': 200,
        'body': f"Image resized and saved to {destination_bucket}/{destination_key}"
    }

