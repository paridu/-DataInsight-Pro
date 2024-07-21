from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variable
API_KEY = os.getenv('GOOGLE_API_KEY')
if not API_KEY:
    st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
else:
    # Configure the API key
    genai.configure(api_key=API_KEY)
