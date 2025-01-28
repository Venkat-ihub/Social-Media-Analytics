




import sys

# my_app/linkedin.py
import requests
import json

def linkedin(job_post):
    linkedin_access_token = "xxxx"  # Replace with secure token
    person_urn = "xxxx"  # Replace with LinkedIn person URN

    def get_upload_url():
        url = "https://api.linkedin.com/v2/assets?action=registerUpload"
        headers = {
            "Authorization": f"Bearer {linkedin_access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "registerUploadRequest": {
                "owner": person_urn,
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "serviceRelationships": [{"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}]
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        print(f"LinkedIn upload URL request status: {response.status_code}, response: {response.text}")

        if response.status_code == 200:
            upload_data = response.json()
            return upload_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"], upload_data["value"]["asset"]
        else:
            return None, None

    def upload_image(upload_url, image_file):
        headers = {"Authorization": f"Bearer {linkedin_access_token}", "Content-Type": "image/jpeg"}
        response = requests.put(upload_url, headers=headers, data=image_file)
        print(f"LinkedIn image upload status: {response.status_code}, response: {response.text}")
        return response.status_code == 201

    def post_to_linkedin(job_description, asset_urn=None):
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {linkedin_access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        payload = {
            "author": person_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": job_description},
                    "shareMediaCategory": "IMAGE" if asset_urn else "NONE",
                    "media": [{"status": "READY", "media": asset_urn}] if asset_urn else []
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }
        response = requests.post(url, headers=headers, json=payload)
        print(f"LinkedIn post status: {response.status_code}, response: {response.text}")

        return response.status_code == 201

    if job_post.image:
        upload_url, asset_urn = get_upload_url()
        if upload_url and upload_image(upload_url, job_post.image.file):
            return post_to_linkedin(job_post.description, asset_urn)
    return post_to_linkedin(job_post.description)
