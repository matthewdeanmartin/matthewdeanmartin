# My test resume as translated into python by ChatGPT.
# until write unit tests for this, it isn't done.

resume = {
    "name": "Matthew Martin",
    "position": "Tech Lead",
    "company": "Artemis Consulting",
    "location": "Herndon, VA",
    "email": "matthewdeanmartin@gmail.com",
    "experience": [
        {
            "position": "Tech Lead",
            "company": "Artemis Consulting",
            "start_date": "September 2019",
            "end_date": "current"
        },
        {
            "position": "Systems Architech",
            "company": "ASRD",
            "start_date": "March 2015",
            "end_date": "September 2019"
        },
        {
            "position": "Senior Software Developer",
            "company": "BWC Global/Burson Marsteller",
            "start_date": "July 2016",
            "end_date": "March 2019"
        },
        {
            "position": "Senior Software Engineer I",
            "company": "Fors Marsh Group",
            "start_date": "July 2014",
            "end_date": "July 2016"
        },
        {
            "position": "JavaScript and C# Software Developer III",
            "company": "CACI",
            "start_date": "August 2012",
            "end_date": "July 2014"
        },
        {
            "position": "Senior Consultant",
            "company": "Procentrix",
            "start_date": "May 2008",
            "end_date": "August 2012"
        }
    ],
    "education": [
        {
            "degree": "Masters in Economics",
            "university": "University of Akron",
            "start_year": 1996,
            "end_year": 1998
        },
        {
            "degree": "Bachelors of Science in Business Administration",
            "university": "The University of Akron",
            "start_year": 1994,
            "end_year": 1996
        }
    ]
}

def get_experience(resume):
    """Returns a list of dictionaries containing information about the candidate's work experience"""
    return resume["experience"]

def get_education(resume):
    """Returns a list of dictionaries containing information about the candidate's education"""
    return resume["education"]

def get_most_recent_experience(resume):
    """Returns the most recent job in the candidate's work experience"""
    return resume["experience"][0]

def get_relevant_experience(resume, keyword):
    """Returns a list of dictionaries containing information about the candidate's work experience that includes the specified keyword"""
    relevant_experience = []
    for job in resume["experience"]:
        if keyword in job["position"]:
            relevant_experience.append(job)
    return relevant_experience

def get_duration_of_experience(resume):
    """Returns the total amount of time the candidate has spent in the workforce, in years"""
    total_duration = 0
    for job in resume["experience"]:
        start_year = int(job["start_date"].split(" ")[1])
        end_year = int(job["end_date"].split(" ")[1]) if job["end_date"] != "current" else datetime.datetime.now().year
        duration = end_year - start_year
        total_duration += duration
    return total_duration
