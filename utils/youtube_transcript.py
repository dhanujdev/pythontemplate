from youtube_transcript_api import YouTubeTranscriptApi
import re

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
        
        # Combine all text parts
        full_transcript = ' '.join([entry['text'] for entry in transcript_data])
        
        return {
            'success': True,
            'transcript': full_transcript,
            'video_id': video_id
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == "__main__":
    # Test the function
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    result = get_transcript(url)
    if result['success']:
        print(f"Transcript length: {len(result['transcript'])} characters")
        print(f"First 100 characters: {result['transcript'][:100]}...")
    else:
        print(f"Error: {result['error']}") 