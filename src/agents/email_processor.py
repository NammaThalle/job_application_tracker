import os
import json
from typing import Optional
from pydantic import BaseModel, Field, ValidationError
from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import get_gmail_credentials
from langchain.prompts import PromptTemplate
from googleapiclient.discovery import build
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor

from utils.logging import logger
from utils.prompts import email_classifier_prompt
from dotenv import load_dotenv

class EmailData(BaseModel):
    company: str = Field(..., title="Company Name")
    role: str = Field(..., title="Job Role")
    source: Optional[str] = Field("", title="Application Source (LinkedIn, Indeed, etc.)")
    location: Optional[str] = Field("", title="Job Location")
    salary: Optional[str] = Field("", title="Salary Details")
    date_viewed: Optional[str] = Field("", title="Date Application was Viewed (YYYY-MM-DD)")
    date: Optional[str] = Field("", title="Interview Date (YYYY-MM-DD)")
    time: Optional[str] = Field("", title="Interview Time")
    format: Optional[str] = Field("", title="Interview Format (Online/In-person)")
    status: str = Field(..., title="Application Status")

class EmailProcessor:
    def __init__(self):
        self._load_credentials()
        self.api_resource = self._initialize_gmail_api()
        self.toolkit = GmailToolkit(api_resource=self.api_resource)
        self.tools = self.toolkit.get_tools()
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, file_cache=False)
        self.agent = self._initialize_agent()
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=False)

    def _load_credentials(self):
        """Loads API credentials from a .env file."""
        load_dotenv()
        # Verify that the environment variables are set
        google_api_key = os.getenv("GOOGLE_API_KEY")
        langsmith_api_key = os.getenv("LANGSMITH_API_KEY")

        if not google_api_key or not langsmith_api_key:
            raise ValueError("GOOGLE_API_KEY or LANGSMITH_API_KEY not found in .env file")

    def _initialize_gmail_api(self):
        """Initializes the Gmail API service.

        This function retrieves Gmail credentials using the specified token and client secrets files,
        then builds and returns the Gmail API service resource.

        Returns:
            googleapiclient.discovery.Resource: The initialized Gmail API service resource.
        """
        token_file = os.getenv("TOKEN_FILE")
        client_secrets_file = os.getenv("CLIENT_SECRETS_FILE")
        scopes = os.getenv("SCOPES")
        if not token_file or not client_secrets_file: #or not scopes:
            raise ValueError("TOKEN_FILE, CLIENT_SECRETS_FILE, and SCOPES must be set in the .env file")
        # scopes = [scope.strip() for scope in scopes.split(",")]

        credentials = get_gmail_credentials(
            token_file=token_file,
            scopes=scopes,
            client_secrets_file=client_secrets_file,
        )
        service = build('gmail', 'v1', credentials=credentials, cache_discovery=False)
        return service

    def _initialize_agent(self):
        """Initializes the agent for processing emails.

        This function defines the instructions for the agent, which include how to classify emails
        related to job applications into categories such as New Application, Viewed, Interview Scheduled,
        or Rejection. The agent is configured to extract relevant information from each email and
        return the data as a JSON object.

        Returns:
            AgentExecutor: An instance of AgentExecutor configured with the specified tools, LLM, and prompt.
        """
        prompt = PromptTemplate(input_variables=["input", "agent_scratchpad"], template=email_classifier_prompt + "\n {agent_scratchpad} ")
        return create_tool_calling_agent(tools=self.tools, llm=self.llm, prompt=prompt)

    def process_emails(self):
        logger.info("Checking emails for job application updates...")
        try:
            result = self.agent_executor.invoke({})
            raw_output = result.get("output", "")
            raw_output = raw_output[7:] if raw_output.startswith("```json") else raw_output
            raw_output = raw_output[:-3] if raw_output.endswith("```") else raw_output
            parsed_data = json.loads(raw_output.strip())

            validated_results = []
            for item in parsed_data:
                try:
                    validated_data = EmailData(**item)
                    validated_results.append(validated_data.model_dump())
                except ValidationError as e:
                    logger.error("\n❌ Validation Error: %s", str(e))

            logger.info("\n✅ Validated Results: %s", json.dumps(validated_results, indent=4))
        except Exception as e:
            logger.error("\n❌ Error: %s", str(e))

if __name__ == "__main__":
    processor = EmailProcessor()
    processor.process_emails()
