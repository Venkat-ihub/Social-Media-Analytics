import os
import requests
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def instagram(job_post):
    # Securely fetch sensitive data from environment variables
    access_token = "xxxx"  # Instagram access token
    instagram_account_id = "xxxx"  # Instagram Business account ID
    aws_access_key = "xxxx"  # AWS Access Key
    aws_secret_key = "xxxx"  # AWS Secret Key
    aws_bucket_name = "xxxx"  # S3 Bucket Name
    aws_region = "AWS_REGION", "us-east-1"  # Default AWS Region

    # Initialize S3 client
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Error initializing S3 client: {e}")
        return False

    def upload_image_to_s3(file):
        """Uploads an image to AWS S3 and returns its public URL."""
        object_key = f"instagram_images/{os.path.basename(file.name)}"
        try:
            s3_client.upload_fileobj(file, aws_bucket_name, object_key, ExtraArgs={'ACL': 'public-read'})
            url = f"https://{aws_bucket_name}.s3.{aws_region}.amazonaws.com/{object_key}"
            print(f"S3 upload success: {url}")
            return url
        except Exception as e:
            print(f"S3 upload error: {e}")
            return None

    def post_to_instagram(image_url, caption):
        """Handles media creation and publishing on Instagram."""
        create_media_url = f"https://graph.facebook.com/v17.0/{instagram_account_id}/media"
        payload = {
            "image_url": image_url,
            "caption": caption,
            "access_token": access_token
        }
        response = requests.post(create_media_url, data=payload)
        print(f"Instagram media creation status: {response.status_code}, response: {response.text}")

        if response.status_code == 200:
            media_id = response.json().get("id")
            publish_url = f"https://graph.facebook.com/v17.0/{instagram_account_id}/media_publish"
            publish_payload = {"creation_id": media_id, "access_token": access_token}
            publish_response = requests.post(publish_url, data=publish_payload)
            print(f"Instagram publish status: {publish_response.status_code}, response: {publish_response.text}")
            return publish_response.status_code == 200
        else:
            return False

    # Main process: upload image and post to Instagram
    if job_post.image:
        try:
            image_url = upload_image_to_s3(job_post.image.file)
            if image_url:
                return post_to_instagram(image_url, job_post.description)
            else:
                print("Image upload failed.")
                return False
        except Exception as e:
            print(f"Error during image upload or posting: {e}")
            return False
    else:
        print("No image provided for the job post.")
        return False
