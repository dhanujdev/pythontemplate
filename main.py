import subprocess
import sys
import os
import site

def main():
    """
    Run the YouTube Transcript Summarizer application.
    """
    print("Starting YouTube Transcript Summarizer...")
    
    # Check if required packages are installed
    try:
        import streamlit
        import youtube_transcript_api
        import dotenv
        import requests
    except ImportError as e:
        print(f"Missing required package: {e.name}")
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Check if .env file exists and has the API key
    if not os.path.exists(".env"):
        api_key = input("Enter your OpenRouter API key: ")
        with open(".env", "w") as f:
            f.write(f"OPENROUTER_API_KEY={api_key}")
    
    # Run the Streamlit app
    print("Running Streamlit app...")
    
    # Try different methods to run Streamlit
    try:
        # Method 1: Use streamlit module directly
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except Exception as e1:
        print(f"Error running streamlit module: {e1}")
        try:
            # Method 2: Try to find streamlit executable
            user_site = site.USER_SITE
            if user_site:
                user_base = os.path.dirname(os.path.dirname(os.path.dirname(user_site)))
                streamlit_path = os.path.join(user_base, "bin", "streamlit")
                
                if os.path.exists(streamlit_path):
                    subprocess.run([streamlit_path, "run", "app.py"])
                else:
                    raise FileNotFoundError(f"Streamlit executable not found at {streamlit_path}")
            else:
                raise ValueError("User site-packages not found")
        except Exception as e2:
            print(f"Error finding streamlit executable: {e2}")
            print("Please run 'streamlit run app.py' manually")

if __name__ == "__main__":
    main()