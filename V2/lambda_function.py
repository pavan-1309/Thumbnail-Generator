import boto3
from PIL import Image
import io
import os
import urllib.parse

s3 = boto3.client('s3')

def resize_image(image_data, size=(800, 800)):
    with Image.open(io.BytesIO(image_data)) as img:
        img.thumbnail(size)
        output = io.BytesIO()
        img.save(output, format=img.format)
        output.seek(0)
        return output

def lambda_handler(event, context):
    print("Event received:", event)

    # Parse bucket and key
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    raw_key = event['Records'][0]['s3']['object']['key']
    source_key = urllib.parse.unquote_plus(raw_key)

    print("Decoded key:", source_key)

    # Check prefix
    if not source_key.startswith("source/"):
        return {
            'statusCode': 400,
            'body': f"Object key '{source_key}' not in 'source/' folder. Ignored."
        }

    # Extract filename only
    filename = source_key.split('/')[-1]
    destination_key = f"thumbnails/{filename}"

    # Get the original image from S3
    response = s3.get_object(Bucket=source_bucket, Key=source_key)
    image_data = response['Body'].read()

    # Resize image
    resized_image = resize_image(image_data, size=(800, 800))

    # Upload resized image to S3
    s3.put_object(
        Bucket=source_bucket,
        Key=destination_key,
        Body=resized_image,
        ContentType=response['ContentType']
    )

    return {
        'statusCode': 200,
        'body': f"Thumbnail created at {source_bucket}/{destination_key}"
    }
