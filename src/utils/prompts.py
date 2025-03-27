email_classifier_prompt = '''
You are an AI assistant.

Fetch the first 3 emails containing 'your application was' in the subject or body. For each email retrieved, classify it into one of the following categories and return the data as a **single JSON object per email**:  

1️⃣ **New Application:** The email confirms that an application was sent or received.  
    **Extract:**  
    - `"source"`: Source of application (e.g., LinkedIn, Indeed)  
    - `"company"`: Name of the company  
    - `"role"`: Job role applied for  
    - `"location"`: Job location  
    - `"salary"`: Salary details (if available)  
    - `"status"`: `"Applied"`  

2️⃣ **Viewed:** The email confirms that a recruiter has viewed the application.  
    **Extract:**  
    - `"source"`: Source of application (e.g., LinkedIn, Indeed)  
    - `"company"`: Name of the company  
    - `"role"`: Job role applied for  
    - `"date_viewed"`: Date the application was viewed  
    - `"status"`: `"Viewed"`  

3️⃣ **Interview Scheduled:** The email contains information about a scheduled interview.  
    **Extract:**  
    - `"company"`: Name of the company  
    - `"role"`: Job role for which the interview is scheduled  
    - `"date"`: Interview date  
    - `"time"`: Interview time  
    - `"format"`: Interview format (Online/In-person)  
    - `"status"`: `"Interview Scheduled"`  

4️⃣ **Rejection:** The email indicates that the application was rejected.  
    **Extract:**  
    - `"company"`: Name of the company  
    - `"role"`: Job role applied for  
    - `"status"`: `"Rejected"`  

📌 **Return each email's classification as a List of JSON object. If a field has no relevant data, leave it as an empty string `""`.**  

📌 **Example Output:**  
{{
    "company": "Google",
    "role": "Machine Learning Engineer",
    "source": "LinkedIn",
    "location": "Remote",
    "salary": "",
    "date_viewed": "2025-03-27",
    "date": "2025-04-05",
    "time": "10:00 AM",
    "format": "Online",
    "status": "Interview Scheduled"
}}
'''
