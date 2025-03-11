from pocketflow import Node, Flow
from utils.call_llm import call_llm
from utils.youtube_transcript import get_transcript

class FetchTranscriptNode(Node):
    def prep(self, shared):
        # Get the YouTube URL from shared
        return shared.get("youtube_url", "")
    
    def exec(self, youtube_url):
        # Fetch the transcript
        return get_transcript(youtube_url)
    
    def post(self, shared, prep_res, exec_res):
        # Store the transcript result in shared
        shared["transcript_result"] = exec_res
        
        # Determine next action based on success
        if exec_res["success"]:
            shared["transcript"] = exec_res["transcript"]
            shared["video_id"] = exec_res["video_id"]
            return "success"
        else:
            shared["error"] = exec_res["error"]
            return "error"

class SummarizeTranscriptNode(Node):
    def prep(self, shared):
        # Get the transcript from shared
        return shared.get("transcript", "")
    
    def exec(self, transcript):
        # Create a system prompt for summarization
        system_prompt = """You are an expert at summarizing content. 
        Create a comprehensive summary of the following YouTube video transcript. 
        Include the main topics, key points, and important details.
        Structure your summary with clear sections and bullet points where appropriate."""
        
        # Call LLM to summarize the transcript
        return call_llm(transcript, system_prompt)
    
    def post(self, shared, prep_res, exec_res):
        # Store the summary in shared
        shared["summary"] = exec_res
        return "default"

class AnswerQuestionNode(Node):
    def prep(self, shared):
        # Get the transcript and question from shared
        transcript = shared.get("transcript", "")
        question = shared.get("question", "")
        return transcript, question
    
    def exec(self, inputs):
        transcript, question = inputs
        
        # Create a system prompt for answering questions
        system_prompt = """You are an expert at analyzing content and answering questions.
        Based on the provided YouTube video transcript, answer the user's question thoroughly and accurately.
        If the answer cannot be determined from the transcript, clearly state that."""
        
        # Construct the prompt
        prompt = f"""Question: {question}
        
        Transcript:
        {transcript}"""
        
        # Call LLM to answer the question
        return call_llm(prompt, system_prompt)
    
    def post(self, shared, prep_res, exec_res):
        # Store the answer in shared
        shared["answer"] = exec_res
        return "default"

# Create nodes
fetch_transcript_node = FetchTranscriptNode()
summarize_node = SummarizeTranscriptNode()
answer_node = AnswerQuestionNode()

# Connect nodes
fetch_transcript_node - "success" >> summarize_node
fetch_transcript_node - "error" >> None  # End flow on error

# Create flows
transcript_flow = Flow(start=fetch_transcript_node)
qa_flow = Flow(start=answer_node)