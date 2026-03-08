import os
from dotenv import load_dotenv

# Load environment variables with explicit path
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

from sentence_transformers import SentenceTransformer
from newsapi import NewsApiClient
from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import chromadb