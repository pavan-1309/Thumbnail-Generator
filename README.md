# Image-Resize
using AWS lambda images are converted into tumbnails and stored in S3 bucket
For V1
Create two buckets one is source and thr other will be for destination
create a lambda function
create a new role with the following policy 
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:PutLogEvents",
                "logs:CreateLogGroup",
                "logs:CreateLogStream"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": "arn:aws:s3:::Source-bucket-name/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::Destination-Bucket-name/*"
        }
    ]
}

Add the role to your lambda
Upload the zip file
under layers add
Pillow  library arn from this git repo https://github.com/keithrozario/Klayers?tab=readme-ov-file

Test by uploading a sample jpeg image 
and add triggers 

For V2
