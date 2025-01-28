import streamlit as st
import pymongo
import subprocess
import os
import json
from bson import ObjectId

# MongoDB Connection Setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["HRAPP"]
collection = db["hrsoc"]

# Function to retrieve job description from MongoDB
def get_job_description_from_db(job_id):
    try:
        # Convert job_id to ObjectId
        job_description_data = collection.find_one({"_id": ObjectId(job_id)})
        if job_description_data:
            # Convert MongoDB object to dictionary and fetch the needed fields
            job_description = {
                "job_title": job_description_data.get("job_title", ""),
                "experience_required": job_description_data.get("experience_required", ""),
                "required_skills": job_description_data.get("required_skills", []),
                "job_type": job_description_data.get("job_type", ""),
                "shift": job_description_data.get("shift", ""),
                "workplace_type": job_description_data.get("workplace_type", ""),
                "education_level": job_description_data.get("education_level", ""),
                "field_of_study": job_description_data.get("field_of_study", ""),
                "role_description": job_description_data.get("role_description", ""),
                "qualifications": job_description_data.get("qualifications", {})
            }
            return json.dumps(job_description, indent=4)  # Convert to JSON for easy readability
        else:
            return "Job description not found in the database."
    except Exception as e:
        return f"Error fetching job description: {e}"

# Function to format job description as a neat paragraph
def format_job_description(json_data):
    try:
        job_data = json.loads(json_data)
        
        # Basic information
        description = f"Job Title: {job_data['job_title']}\n\n"
        description += f"Experience Required: {job_data['experience_required']}\n\n"
        
        # Required Skills
        description += f"Required Skills: {', '.join(job_data['required_skills'])}\n\n"
        
        # Job Type, Shift, Workplace Type, etc.
        description += f"Job Type: {job_data['job_type']}\n\n"
        description += f"Shift: {job_data['shift']}\n\n"
        description += f"Workplace Type: {job_data['workplace_type']}\n\n"
        
        # Education Level and Field of Study
        description += f"Education Level: {job_data['education_level']}\n\n"
        description += f"Field of Study: {job_data['field_of_study']}\n\n"
        
        # Role Description
        description += f"Role Description: {job_data['role_description']}\n\n"
        
        # Qualifications
        description += "Qualifications:\n"
        
        if "foundational_knowledge" in job_data['qualifications']:
            description += f"- Foundational knowledge in {', '.join(job_data['qualifications']['foundational_knowledge'])}\n"
        if "skills" in job_data['qualifications']:
            description += f"- {', '.join(job_data['qualifications']['skills'])}\n"
        if "education" in job_data['qualifications']:
            description += f"- {job_data['qualifications']['education']['degree']} in {job_data['qualifications']['education']['field']}\n"
        if "experience" in job_data['qualifications']:
            description += f"- {job_data['qualifications']['experience']}\n"
        
        return description.strip()
    except Exception as e:
        return f"Error formatting job description: {e}"

# Function to delete the uploaded image after posting
def delete_uploaded_image(image_path):
    try:
        if os.path.exists(image_path):
            os.remove(image_path)
            st.success("Uploaded image has been deleted.")
        else:
            st.warning("Image not found.")
    except Exception as e:
        st.error(f"Error deleting image: {e}")

# Function to post to a single platform
def post_to_platform(script_name, job_description):
    try:
        result = subprocess.run(["python", script_name, job_description, uploaded_image_path], capture_output=True, text=True)
        if result.returncode == 0:
            st.write(f"Posted to {script_name.split('.')[0].capitalize()} successfully!")
        else:
            st.error(f"Failed to post to {script_name.split('.')[0].capitalize()}: {result.stderr}")
    except Exception as e:
        st.error(f"Error running {script_name}: {e}")

# Streamlit UI
st.title("IT Job Recruitment Posting")

# Image upload
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def upload_image():
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        # Save the image locally
        image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.image(image_path, caption="Uploaded Image", use_column_width=True)
        return image_path

uploaded_image_path = upload_image()  # Save the image and get the path

# Fetch job description
job_id = st.text_input("Enter Job ID")
if st.button("Fetch Job Description"):
    job_description = get_job_description_from_db(job_id)
    if "not found" not in job_description:
        st.session_state['job_description'] = job_description
        st.write("Job Description fetched successfully.")
        st.json(json.loads(job_description))  # Display as JSON for readability
        st.write("Formatted Job Description:")
        st.write(format_job_description(job_description))  # Display the formatted description
    else:
        st.error(job_description)

# Buttons for posting to each platform individually and all at once
if st.button("Post to LinkedIn") and 'job_description' in st.session_state:
    post_to_platform("linkedin.py", st.session_state['job_description'])

if st.button("Post to Instagram") and 'job_description' in st.session_state:
    post_to_platform("instagram.py", st.session_state['job_description'])

if st.button("Post to Facebook") and 'job_description' in st.session_state:
    post_to_platform("facebook.py", st.session_state['job_description'])

if st.button("Post in All Media") and 'job_description' in st.session_state:
    platforms = ["linkedin.py", "facebook.py", "instagram.py"]
    for platform in platforms:
        post_to_platform(platform, st.session_state['job_description'])
    # Delete the uploaded image after posting
    if uploaded_image_path:
        delete_uploaded_image(uploaded_image_path)
