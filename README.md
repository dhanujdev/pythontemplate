# YouTube Transcript Summarizer

A web application that fetches transcripts from YouTube videos, summarizes them, and allows users to ask follow-up questions about the content.

## Features

- Extract transcripts from YouTube videos using the YouTube Transcript API
- Summarize video content using the DeepSeek R1 Zero model via OpenRouter API
- Ask follow-up questions about the video content
- Simple and intuitive user interface built with Streamlit

## Requirements

- Python 3.7+
- OpenRouter API key (for DeepSeek R1 Zero model)
- Internet connection to access YouTube and OpenRouter API

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd youtube-transcript-summarizer
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

## Usage

1. Run the application:
   ```
   python main.py
   ```
   
   Alternatively, you can run the Streamlit app directly:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to `http://localhost:8501`

3. Enter a YouTube URL in the input field and click "Process Video"

4. View the summary and ask follow-up questions about the video content

## Project Structure

- `app.py`: Streamlit web application
- `flow.py`: PocketFlow nodes and flows for transcript processing
- `main.py`: Entry point for the application
- `utils/`: Utility functions
  - `call_llm.py`: OpenRouter API integration
  - `youtube_transcript.py`: YouTube transcript extraction

## License

MIT

## Acknowledgements

- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)
- [Streamlit](https://streamlit.io/)
- [OpenRouter](https://openrouter.ai/)
- [PocketFlow](https://github.com/the-pocket/PocketFlow)
