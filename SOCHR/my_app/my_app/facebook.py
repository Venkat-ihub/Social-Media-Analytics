import requests
import json
import sys

# Facebook page ID and access token
def facebook(job_description, image_path=None):
    facebook_page_id = ""
    facebook_access_token = ""  # Replace with secure token

    def upload_media(page_id, image_file, job_description, access_token):
        url = f"https://graph.facebook.com/v12.0/{page_id}/photos"
        params = {
            "access_token": access_token,
            "message": job_description
        }
        files = {
            "source": image_file  # expects file data in bytes
        }
        
        response = requests.post(url, params=params, files=files)
        if response.status_code == 200:
            print("Media uploaded successfully.")
            return response.json().get("id")
        else:
            print("Failed to upload media.")
            return None

    def post_to_facebook(page_id, access_token, job_description, media_id=None):
        url = f"https://graph.facebook.com/v12.0/{page_id}/feed"
        params = {
            "message": job_description,
            "access_token": access_token
        }
        
        if media_id:
            params["attached_media"] = json.dumps([{"media_fbid": media_id}])
        
        response = requests.post(url, data=params)
