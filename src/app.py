# src/app.py
import time
import os
from datetime import datetime
from utils.logging import logger
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import List, Dict, Optional
from dotenv import load_dotenv  # Import load_dotenv

from agents.email_processor import EmailProcessor

email_processor = EmailProcessor()
email_processor.process_emails()

