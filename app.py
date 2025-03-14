import streamlit as st
from flow import transcript_flow, qa_flow
import re

# Set page configuration
st.set_page_config(
    page_title="YouTube Transcript Summarizer",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF0000;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
    }
    .error-message {
        color: #dc3545;
        font-weight: bold;
    }
    .warning-message {
        color: #ffc107;
        font-weight: bold;
    }
    .info-box {
        background-color: #e7f3fe;
        border-left: 6px solid #2196F3;
        padding: 1rem;
        margin: 1rem 0;
    }
    .summary-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    .question-container {
        background-color: #e9ecef;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>YouTube Transcript Summarizer</h1>", unsafe_allow_html=True)
st.markdown("Enter a YouTube URL to get a summary of the video's transcript and ask follow-up questions.")

# Information box about potential limitations
with st.expander("⚠️ Important Information - Please Read"):
    st.markdown("""
    ### Potential Limitations
    
    This application uses the YouTube Transcript API to fetch video transcripts. Due to YouTube's policies:
    
    1. **Some videos may not have transcripts available**
    2. **YouTube may block requests from cloud servers** (like the one hosting this app)
    
    If you encounter errors:
    
    - Try a different YouTube video
    - Run this application locally on your computer
    - Some educational videos and official channels are more likely to have accessible transcripts
    
    ### Example Videos That Usually Work
    
    - TED Talks: [https://www.youtube.com/watch?v=8jPQjjsBbIc](https://www.youtube.com/watch?v=8jPQjjsBbIc)
    - Khan Academy: [https://www.youtube.com/watch?v=NKmGVE85GUU](https://www.youtube.com/watch?v=NKmGVE85GUU)
    - MIT OpenCourseWare: [https://www.youtube.com/watch?v=HtSuA80QTyo](https://www.youtube.com/watch?v=HtSuA80QTyo)
    """)

# Initialize session state
if 'transcript' not in st.session_state:
    st.session_state.transcript = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'video_id' not in st.session_state:
    st.session_state.video_id = None
if 'error' not in st.session_state:
    st.session_state.error = None
if 'answer' not in st.session_state:
    st.session_state.answer = None

# YouTube URL input
youtube_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

# Process button
if st.button("Process Video"):
    if youtube_url:
        # Show loading spinner
        with st.spinner("Fetching and processing transcript..."):
            # Create shared data
            shared = {"youtube_url": youtube_url}
            
            # Run the transcript flow
            transcript_flow.run(shared)
            
            # Check if successful
            if "error" in shared:
                st.session_state.error = shared["error"]
                st.session_state.transcript = None
                st.session_state.summary = None
                st.session_state.video_id = None
            else:
                st.session_state.transcript = shared["transcript"]
                st.session_state.summary = shared["summary"]
                st.session_state.video_id = shared["video_id"]
                st.session_state.error = None
    else:
        st.session_state.error = "Please enter a YouTube URL"

# Display error if any
if st.session_state.error:
    st.markdown(f"<p class='error-message'>Error:</p>", unsafe_allow_html=True)
    st.markdown(st.session_state.error)
    
    # If it's likely an IP blocking issue, show additional guidance
    if "YouTube is blocking" in st.session_state.error or "IP" in st.session_state.error:
        st.markdown("""
        ### Try these example videos that may work better:
        
        - TED Talk: [https://www.youtube.com/watch?v=8jPQjjsBbIc](https://www.youtube.com/watch?v=8jPQjjsBbIc)
        - Khan Academy: [https://www.youtube.com/watch?v=NKmGVE85GUU](https://www.youtube.com/watch?v=NKmGVE85GUU)
        - MIT OpenCourseWare: [https://www.youtube.com/watch?v=HtSuA80QTyo](https://www.youtube.com/watch?v=HtSuA80QTyo)
        """)

# Display results if transcript is available
if st.session_state.transcript:
    # Display embedded video
    if st.session_state.video_id:
        st.markdown("<h2 class='sub-header'>Video</h2>", unsafe_allow_html=True)
        st.video(f"https://www.youtube.com/watch?v={st.session_state.video_id}")
    
    # Display summary
    st.markdown("<h2 class='sub-header'>Summary</h2>", unsafe_allow_html=True)
    st.markdown("<div class='summary-container'>", unsafe_allow_html=True)
    st.markdown(st.session_state.summary)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Follow-up questions
    st.markdown("<h2 class='sub-header'>Ask Follow-up Questions</h2>", unsafe_allow_html=True)
    question = st.text_input("Your question about the video", placeholder="What is the main point of the video?")
    
    if st.button("Ask Question"):
        if question:
            with st.spinner("Generating answer..."):
                # Create shared data
                shared = {
                    "transcript": st.session_state.transcript,
                    "question": question
                }
                
                # Run the QA flow
                qa_flow.run(shared)
                
                # Store the answer
                st.session_state.answer = shared["answer"]
        else:
            st.warning("Please enter a question")
    
    # Display answer if available
    if st.session_state.answer:
        st.markdown("<div class='question-container'>", unsafe_allow_html=True)
        st.markdown(f"**Q: {question}**")
        st.markdown(f"**A:** {st.session_state.answer}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Option to view full transcript
    with st.expander("View Full Transcript"):
        st.text(st.session_state.transcript)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and OpenRouter API")

if __name__ == "__main__":
    # This is already handled by Streamlit
    pass 