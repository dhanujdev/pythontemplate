from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re
import random
import requests
import json
import streamlit as st

def extract_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    
    Args:
        url (str): YouTube URL
        
    Returns:
        str: YouTube video ID
    """
    # Regular expressions to match different YouTube URL formats
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/|youtube\.com\/watch\?.*&v=)([^&\n?#]+)',
        r'youtube\.com\/shorts\/([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def get_transcript_alternative(video_id):
    """
    Alternative method to get transcript using a third-party API.
    
    Args:
        video_id (str): YouTube video ID
        
    Returns:
        dict: Dictionary with 'success' (bool), 'transcript' (str) or 'error' (str)
    """
    try:
        # Try using a third-party API that provides YouTube transcripts
        response = requests.get(f"https://youtubetranscript.com/?server_vid={video_id}")
        
        if response.status_code == 200:
            try:
                # Parse the response
                data = response.text
                # Extract the transcript data from the response
                transcript_start = data.find('{"transcriptData')
                if transcript_start != -1:
                    transcript_end = data.find('</script>', transcript_start)
                    transcript_json = data[transcript_start:transcript_end].strip()
                    transcript_data = json.loads(transcript_json)
                    
                    if 'transcriptData' in transcript_data and transcript_data['transcriptData']:
                        # Combine all text parts
                        full_transcript = ' '.join([item.get('text', '') for item in transcript_data['transcriptData']])
                        
                        return {
                            'success': True,
                            'transcript': full_transcript,
                            'video_id': video_id
                        }
            except Exception as e:
                pass  # Continue to the next method if this fails
    
    except Exception as e:
        pass  # Continue to the next method if this fails
    
    # If we get here, the alternative method failed
    return {
        'success': False,
        'error': 'Could not retrieve transcript using alternative method'
    }

def get_transcript(url, languages=['en']):
    """
    Get the transcript of a YouTube video.
    
    Args:
        url (str): YouTube URL
        languages (list): List of language codes to try, in order of preference
        
    Returns:
        dict: Dictionary with 'success' (bool), 'transcript' (str) or 'error' (str)
    """
    video_id = extract_video_id(url)
    
    if not video_id:
        return {
            'success': False,
            'error': 'Could not extract video ID from URL'
        }
    
    # First try the official YouTube Transcript API
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to get transcript in preferred languages
        transcript = None
        for lang in languages:
            try:
                transcript = transcript_list.find_transcript([lang])
                break
            except:
                continue
        
        # If no preferred language found, get the first available
        if not transcript:
            transcript = transcript_list.find_transcript([])
        
        # Get the transcript data
        transcript_data = transcript.fetch()
        
        # Format the transcript
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript_data)
        
        return {
            'success': True,
            'transcript': formatted_transcript,
            'video_id': video_id
        }
    
    except Exception as e:
        # If the official API fails, try the alternative method
        st.warning(f"YouTube Transcript API failed: {str(e)}. Trying alternative method...")
        
        result = get_transcript_alternative(video_id)
        
        # If the alternative method also fails, show a helpful error message
        if not result['success']:
            error_message = str(e)
            
            # Check if it's an IP block issue
            if "YouTube is blocking" in error_message or "IP" in error_message:
                error_message = """
                YouTube is blocking requests from the server's IP address. 
                
                This is a common issue with cloud-hosted applications. Here are some options:
                
                1. Try a different YouTube video - some videos may work while others are blocked
                2. Run the application locally on your computer instead of using the cloud version
                3. Use a VPN or proxy service when accessing this application
                
                We've attempted to use an alternative method to fetch the transcript, but it also failed.
                """
            
            return {
                'success': False,
                'error': error_message
            }
        
        return result

if __name__ == "__main__":
    # Test the function
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    result = get_transcript(url)
    if result['success']:
        print(f"Transcript length: {len(result['transcript'])} characters")
        print(f"First 100 characters: {result['transcript'][:100]}...")
    else:
        print(f"Error: {result['error']}") 