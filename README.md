# Job Application Tracker

This project automates the process of tracking job applications by parsing emails from a Gmail account, extracting relevant information, analyzing email threads for application status, and storing the data.

## Features

*   **Email Parsing:** Extracts company name, application date, job position, and other relevant details from application-related emails.
*   **Status Analysis:** Analyzes email content to determine the application status (Applied, Viewed, Interview Scheduled, Rejected).
*   **Agentic AI:** Uses the Gemini API and agentic logic to extract and analyze data.
*   **Gmail API integration:** Uses the Gmail API to access and process emails.

## Prerequisites

*   Python 3.x
*   Google Cloud Project with Gmail API enabled
*   Gemini API key
*   `langchain`
*   `langchain-google-genai`
*   `langchain-google-community`
*   `google-api-python-client`
*   `google-auth`
*   `python-dotenv`
*   Internet Connection

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd job_application_tracker
    ```

2.  **Install the required Python libraries:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Google Cloud Credentials:**

    *   Follow the Google Cloud documentation to create a project and enable the Gmail API.
    *   Download the `client_secret.json` file and place it in the `src/secrets/` directory.

4.  **Set up Gemini API Key:**

    *   Obtain a Gemini API key from the Google AI Studio.
    *   Set the API key as an environment variable in `.env` file.

    ```properties
    GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
    ```

5.  **Configure the `.env` file:**

    *   Create a `.env` file in the root directory.
    *   Add the necessary environment variables, such as:

    ```properties
    GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
    LANGSMITH_API_KEY=YOUR_LANGSMITH_API_KEY
    CLIENT_SECRETS_FILE=src/secrets/client_secret.json
    TOKEN_FILE=src/secrets/token.json
    SCOPES=["https://www.googleapis.com/auth/gmail.readonly"]
    ```

## Usage

1.  **Run the application:**

    ```bash
    python app.py
    ```

2.  **Using Docker:**

    *   Build the Docker image:

        ```bash
        docker build -t job_application_tracker .
        ```

    *   Run the Docker container:

        ```bash
        docker run -it --rm -v $(pwd)/src/:/app job_application_tracker
        ```

## File Structure

```
job_application_tracker/
├── src/
│   ├── agents/
│   │   └── email_processor.py
│   ├── secrets/
│   │   └── client_secret.json
│   │   └── token.json
│   ├── utils/
│   │   ├── logging.py
│   │   └── prompts.py
│   ├── app.py
├── .env
├── Dockerfile
├── requirements.txt
├── README.md
├── .gitignore
├── build.sh
└── run.sh
```