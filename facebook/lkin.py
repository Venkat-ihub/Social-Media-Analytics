from linkedin_api import Linkedin
import pandas as pd

# Authenticate using LinkedIn user account credentials
api = Linkedin('lenskinnn@gmail.com', 'Frost4115')

# GET a profile
profile_data = api.get_profile('ramaswamy-rajesh')

# Create a structured and organized output
def create_profile_summary(data):
    summary = {
        "Name": f"{data.get('firstName', None)} {data.get('lastName', None)}",
        "Headline": data.get('headline', None),
        "Location": data.get('locationName', None),
        "Industry": data.get('industryName', None),
        "Summary": data.get('summary', None),
        "Experience": [],
        "Education": [],
        "Skills": [skill['name'] for skill in data.get('skills', [])] or None
    }

    # Process experience
    for exp in data.get('experience', []):
        experience_entry = {
            "Title": exp.get('title', None),
            "Company": exp.get('companyName', None),
            "Location": exp.get('locationName', None),
            "Start Date": f"{exp.get('timePeriod', {}).get('startDate', {}).get('month', None)}/{exp.get('timePeriod', {}).get('startDate', {}).get('year', None)}",
            "End Date": f"{exp.get('timePeriod', {}).get('endDate', {}).get('month', None)}/{exp.get('timePeriod', {}).get('endDate', {}).get('year', None)}",
            "Description": exp.get('description', None)
        }
        summary['Experience'].append(experience_entry)

    # Process education
    for edu in data.get('education', []):
        education_entry = {
            "Degree": edu.get('degreeName', None),
            "School": edu.get('schoolName', None),
            "Field of Study": edu.get('fieldOfStudy', None),
            "Start Date": f"{edu.get('timePeriod', {}).get('startDate', {}).get('month', None)}/{edu.get('timePeriod', {}).get('startDate', {}).get('year', None)}",
            "End Date": f"{edu.get('timePeriod', {}).get('endDate', {}).get('month', None)}/{edu.get('timePeriod', {}).get('endDate', {}).get('year', None)}"
        }
        summary['Education'].append(education_entry)

    return summary

# Generate the structured summary
profile_summary = create_profile_summary(profile_data)

# Convert to DataFrame for better visualization
experience_df = pd.DataFrame(profile_summary['Experience'])
education_df = pd.DataFrame(profile_summary['Education'])

# Print summary
print("Profile Summary:")
for key, value in profile_summary.items():
    if key not in ["Experience", "Education"]:
        print(f"{key}: {value}")
    else:
        print(f"{key}:")
        print(value)

# Print Experience DataFrame
print("\nExperience:")
print(experience_df.to_string(index=False))

# Print Education DataFrame
print("\nEducation:")
print(education_df.to_string(index=False))

# Save to CSV
profile_summary_df = pd.DataFrame([profile_summary])
profile_summary_df.to_csv('linkedin_profile_summary.csv', index=False)
experience_df.to_csv('linkedin_experience.csv', index=False)
education_df.to_csv('linkedin_education.csv', index=False)

print("\nProfile summary saved to 'linkedin_profile_summary.csv'")
print("Experience data saved to 'linkedin_experience.csv'")
print("Education data saved to 'linkedin_education.csv'")
