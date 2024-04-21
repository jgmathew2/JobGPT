import json
import requests
import os

# Load the local JSON file with the criteria
with open('public/uploads/WorkDayForm.json', 'r') as file:
    criteria = json.load(file)

# URL of the JSON file containing listings
url = "https://raw.githubusercontent.com/SimplifyJobs/Summer2024-Internships/dev/.github/scripts/listings.json"

# Fetch the listings JSON from the URL
response = requests.get(url)
jobs = response.json()  # Make sure this results in a list of job postings

# Function to check for partial match in location
def is_partial_match_location(job_locations, criteria_location):
    if not criteria_location:
        return True
    for location in job_locations:
        if any(word in criteria_location.casefold() for word in location.casefold().split(',')):
            return True
    return False

# Function to check for partial match in role
def is_partial_match_role(job_role, criteria_role):
    if not criteria_role:
        return True
    criteria_role_words = criteria_role.casefold().split()
    return any(word in job_role.casefold() for word in criteria_role_words)

# Filter the listings based on the criteria from the local JSON file
filtered_links = []
for job in jobs:
    # Check if the job is active
    if job.get('active', False):
        if job.get('is_visible', False):
            # Check for partial match in location if criteria location is not empty
            if is_partial_match_location(job.get('locations', ''), criteria.get('location', '')):
                # Check for partial match in role if criteria role is not empty
                if is_partial_match_role(job.get('title', ''), criteria.get('role', '')):
                    # Collect the WorkDay links
                    if 'workdayjobs.com' in job.get('url', ''):
                        filtered_links.append((job['url'], job['date_updated']))

sorted_links = sorted(filtered_links)

# Write the sorted links to a file in a specific directory
output_directory = 'public/uploads/'
output_file_path = output_directory + 'filtered_links.txt'

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

with open(output_file_path, 'w') as output_file:
    for link in sorted_links:
        # Properly format the tuple to a string
        output_file.write(f'{link[0]}\n')