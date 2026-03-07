# InfoTrace - Project Configuration

# Project Info
PROJECT_NAME = "InfoTrace"
VERSION = "0.1.0"

# Platforms
SUPPORTED_PLATFORMS = ["twitter", "facebook", "instagram"]

# Data Paths
RAW_DATA_PATH = "data/raw/"
PROCESSED_DATA_PATH = "data/processed/"
MODELS_PATH = "models/"

# Model Config
MODEL_NAME = "roberta-base"
NUM_LABELS = 3  # Factual, Misleading, Uncertain
MAX_TOKEN_LENGTH = 512
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
EPOCHS = 3

# Labels
LABEL_MAP = {
    0: "Factual",
    1: "Misleading", 
    2: "Uncertain"
}

# API Keys (fill these in after getting API access)
TWITTER_API_KEY = ""
TWITTER_API_SECRET = ""
TWITTER_BEARER_TOKEN = ""
FACEBOOK_ACCESS_TOKEN = ""