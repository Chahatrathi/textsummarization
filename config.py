import torch

# Reddit API Credentials
REDDIT_CLIENT_ID = '_PHpbAqog8BdDunWi6pdUg'
REDDIT_CLIENT_SECRET = '14MHOWJEn8VfoLO73eRbHQSA6FOxtQ'
REDDIT_USER_AGENT = 'summarizer:v1.0 (by u/DifferentLynx2538)'

# Model Configuration
MODEL_PATH = "facebook/bart-large-cnn"  # Pretrained BART model
# MODEL_PATH = './saved_model_20241206-135116' 
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# Data Settings
MAX_INPUT_LENGTH = 1024
MAX_SUMMARY_LENGTH = 256
TOP_POST_LIMIT = 100
COMMENT_UPVOTE_THRESHOLD = 5
