import streamlit as st
import subprocess
import os

# Function to generate a job description
def generate_job_description(job_title, experience_text, skill_set, job_type, shift, workplace_type, education_level, selected_specification):
    if experience_text == "Fresher":
        job_description = (
            f"Job Title: {job_title}\n\n"
            f"Experience Required: {experience_text}\n\n"
            f"Required Skills: {', '.join(skill_set)}\n\n"
            f"Job Type: {job_type}\n\n"
            f"Shift: {shift}\n\n"
            f"Workplace Type: {workplace_type}\n\n"
            f"Education Level: {education_level}\n\n"
            f"Field of Study: {selected_specification}\n\n\n"
            f"Role Description:\n"
            f"This is a full-time on-site role for a {job_title} at our company. The role involves day-to-day tasks "
            f"related to software development, {', '.join(skill_set)}, integration, databases, and web services. "
            f"We are looking for an enthusiastic and motivated candidate who is eager to kickstart their career "
            f"in the field. The ideal candidate should have foundational knowledge in the required skills and a "
            f"willingness to learn and grow. This role is suitable for a fresher, with training and mentorship provided. "
            f"The position is based on a {shift} shift and is {workplace_type}.\n\n\n"
            f"Qualifications:\n"
            f"- Foundational knowledge in {', '.join(skill_set)}\n"
            f"- Strong problem-solving and analytical skills\n"
            f"- Ability to work effectively in a team environment\n"
            f"- Bachelor’s degree in {selected_specification} or related field\n"
            f"- Experience in a start-up or tech environment is a plus\n"
        )
    else:
        job_description = (
            f"Job Title: {job_title}\n\n"
            f"Experience Required: {experience_text}\n\n"
            f"Required Skills: {', '.join(skill_set)}\n\n"
            f"Job Type: {job_type}\n\n"
            f"Shift: {shift}\n\n"
            f"Workplace Type: {workplace_type}\n\n"
            f"Education Level: {education_level}\n\n"
            f"Field of Study: {selected_specification}\n\n\n"
            f"Role Description:\n"
            f"This is a full-time on-site role for a {job_title} at our company. The role involves day-to-day tasks "
            f"related to software development, {', '.join(skill_set)}, integration, databases, and web services. "
            f"We are seeking an experienced candidate with {experience_text} in the industry, who can demonstrate "
            f"a strong skill set in {', '.join(skill_set)} and is capable of managing complex tasks and contributing to "
            f"team goals. This position requires a seasoned professional with a proven track record, suited for {shift} "
            f"and {workplace_type} work.\n\n\n"
            f"Qualifications:\n"
            f"- Expertise in {', '.join(skill_set)}\n"
            f"- Strong problem-solving and analytical skills\n"
            f"- Ability to work effectively in a team environment\n"
            f"- Bachelor’s degree in {selected_specification} or related field\n"
            f"- Experience in a start-up or tech environment is a plus\n"
        )
    return job_description

# Streamlit UI
st.title("IT Job Recruitment Form")

# Input fields for job details
job_titles = ["Software Engineer", "Data Scientist", "DevOps Engineer", "Systems Analyst", "Database Administrator", "Web Developer"]
job_title = st.selectbox("Job Title", job_titles, key="job_title")
experience_options = ["Fresher"] + list(range(1, 16))
experience_years = st.selectbox("Years of Experience", experience_options, key="experience_years")
experience_text = "Fresher" if experience_years == "Fresher" else f"{experience_years} year(s)"
skills = ["Python", "Java", "JavaScript", "SQL", "HTML", "CSS", "C++", "C#", "Ruby", "PHP", "Cloud Computing", "Machine Learning", "Data Analysis", "DevOps"]
skill_set = st.multiselect("Required Skill Set", skills, key="skill_set")
job_type = st.selectbox("Job Type", ["Full-time", "Part-time", "Internship"], key="job_type")
shift = st.selectbox("Shift", ["Morning Shift", "Night Shift"], key="shift")
workplace_type = st.selectbox("Workplace Type", ["On-site", "Remote"], key="workplace_type")
education_level = st.selectbox("Education Level", ["Select", "Bachelor's Degree", "Master's Degree", "PhD", "Other"], key="education_level")

selected_specification = ""
if education_level != "Select":
    specifications = ["Computer Science Engineering (CSE)", "Information Technology (IT)", "Software Engineering", "Data Science"]
    selected_specification = st.selectbox("Select Field of Study", specifications, key="specification")

# Image upload and saving
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
        
        st.image(image_path)  # Display the uploaded image
        return image_path

uploaded_image_path = upload_image()  # Save the image and get the path

# Generate job description
if st.button("Generate Job Description"):
    job_description = generate_job_description(job_title, experience_text, skill_set, job_type, shift, workplace_type, education_level, selected_specification)
    st.session_state['job_description'] = job_description
    st.write("Job Description generated successfully.")
    st.write(job_description)

    if uploaded_image_path:
        st.image(uploaded_image_path, caption="Uploaded Image", use_column_width=True)

# Function to post to a single platform
def post_to_platform(script_name):
    if 'job_description' not in st.session_state:
        st.error("Please generate a job description first!")
    else:
        job_description = st.session_state['job_description']
        try:
            result = subprocess.run(["python", script_name, job_description, uploaded_image_path], capture_output=True, text=True)
            if result.returncode == 0:
                st.write(f"Posted to {script_name.split('.')[0].capitalize()} successfully!")
            else:
                st.error(f"Failed to post to {script_name.split('.')[0].capitalize()}: {result.stderr}")
        except Exception as e:
            st.error(f"Error running {script_name}: {e}")

# Buttons for posting to each platform individually and all at once
if st.button("Post to LinkedIn"):
    post_to_platform("linkedin.py")

if st.button("Post to Instagram"):
    post_to_platform("instagram.py")

if st.button("Post to Facebook"):
    post_to_platform("facebook.py")

if st.button("Post in All Media"):
    platforms = ["linkedin.py", "facebook.py", "instagram.py"]
    for platform in platforms:
        post_to_platform(platform)
