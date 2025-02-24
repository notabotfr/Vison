import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os  
from dotenv import load_dotenv 

# Load environment variables from .env file
load_dotenv()

# --- Gemini API Setup ---
# Retrieve the API key from the environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# --- Speech and Text Initialization ---
r = sr.Recognizer()
engine = pyttsx3.init()
def speak(text):
    """Speaks the given text using TTS."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listens for user speech and converts it to text."""
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        text = r.recognize_google(audio)
        print(f"User said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand.")
        return ""
    except sr.RequestError as e:
        speak(f"Could not request results from speech recognition service; {e}")
        return ""

def get_gemini_response_with_actions(prompt_text, conversation_history=[]):
    """Gets response from Gemini and looks for ACTION keywords to execute."""

    action_keywords_description = """
    Available Actions (use these keywords in your response if an action is needed):
    - ACTION:OPEN_BROWSER: Opens a web browser.
    - ACTION:SEARCH_WEB: Performs a web search using the given query.  Example: ACTION:SEARCH_WEB:python tutorial w3schools
    - ACTION:NAVIGATE_URL: Navigates the browser to a specific URL. Example: ACTION:NAVIGATE_URL:https://www.w3schools.com/python/
    - ACTION:READ_PAGE_CONTENT: Reads the main text content of the current webpage aloud.
    - ACTION:SUMMARIZE_CONTENT: Summarizes the content of the current webpage.
    - ACTION:EXPLAIN_TOPIC: Explains a given topic based on the current webpage content. Example: ACTION:EXPLAIN_TOPIC:python variables
    - ACTION:ANSWER_QUESTION: Answers a user's question based on the current webpage content. Example: ACTION:ANSWER_QUESTION:what is python indentation?
    - ACTION:TYPE_IN_BROWSER: Types text into the browser's address bar or a search bar. Example: ACTION:TYPE_IN_BROWSER:w3schools.com
    - ACTION:NONE: No specific action is needed, just provide a verbal response.

    When using an ACTION that requires parameters (like URL, search query, topic), include them after the ACTION keyword, separated by a colon.
    If no action is needed, and you just need to respond verbally, use ACTION:NONE.

    Your responses should be natural, helpful, and human-like, as if you are a virtual assistant named Vision helping a blind student.
    """

    full_prompt = f"""You are Vision, a helpful and intelligent virtual assistant designed to assist a blind student with online education.
    You can understand natural language and perform actions on the user's computer to help them learn.

    {action_keywords_description}

    Conversation History:
    --- START HISTORY ---
    {''.join([f'{turn["role"]}: {turn["content"]}\n' for turn in conversation_history])}
    --- END HISTORY ---

    User's Command: {prompt_text}

    Assistant's Response (include ACTION keywords if necessary, followed by your verbal response):
    """

    try:
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=800, # Increased max output tokens for potentially longer action instructions + response
            )
        )
        if response.candidates and response.candidates[0].content.parts:
            gemini_response_text = response.candidates[0].content.parts[0].text
            return gemini_response_text
        else:
            return "ACTION:NONE Sorry, I couldn't generate a response." # Default to no action if response is empty

    except Exception as e:
        print(f"Gemini API error: {e}")
        return f"ACTION:NONE Sorry, I encountered an issue with the virtual assistant: {e}" # Default to no action on error

def execute_action(gemini_response_text):
    """Parses Gemini's response for ACTION keywords and executes them."""
    action_lines = [line for line in gemini_response_text.split('\n') if line.startswith('ACTION:')]
    verbal_response = '\n'.join([line for line in gemini_response_text.split('\n') if not line.startswith('ACTION:')]).strip() # Extract verbal part

    if verbal_response:
        speak(verbal_response) # Speak the verbal part of Gemini's response

    for action_line in action_lines:
        parts = action_line.split(':', 1) # Split only once at the first colon
        action_type = parts[1].split(':')[0] if len(parts) > 1 else parts[1] # Further split to get action type, handle if no params
        action_param = parts[1].split(':', 1)[1].strip() if len(parts) > 1 and ':' in parts[1] else None # Extract parameter if present

        print(f"Executing action: {action_type}, Parameter: {action_param}") # Debugging

        if action_type == 'OPEN_BROWSER':
            webbrowser.open('') # Opens default browser - could refine to open a specific one if needed

        elif action_type == 'SEARCH_WEB':
            if action_param:
                search_query = action_param
                webbrowser.open(f'https://www.google.com/search?q={search_query}')
            else:
                speak("Please specify what you want to search for.")

        elif action_type == 'NAVIGATE_URL':
            if action_param:
                url = action_param
                webbrowser.open(url)
            else:
                speak("Please specify the URL you want to navigate to.")

        elif action_type == 'READ_PAGE_CONTENT':
            current_url = webbrowser.get('chrome').open_new_tab('').geturl() # Try to get current URL - might need browser specific solution
            if current_url and current_url.startswith('http'): # Basic URL check
                content = extract_website_content(current_url)
                if content:
                    speak("Reading page content:")
                    speak(content)
                else:
                    speak("Could not extract content from the current page.")
            else:
                speak("I'm not sure which page you want me to read. Please navigate to a webpage first.")


        elif action_type == 'SUMMARIZE_CONTENT':
            current_url = webbrowser.get('chrome').open_new_tab('').geturl() #  Try to get current URL
            if current_url and current_url.startswith('http'):
                content = extract_website_content(current_url)
                if content:
                    summary = summarize_content_with_gemini(content) # You'd need to reimplement or adjust summarization function
                    speak("Summarizing page content:")
                    speak(summary)
                else:
                    speak("Could not summarize content from the current page.")
            else:
                speak("Please navigate to a webpage first so I can summarize it.")

        elif action_type == 'EXPLAIN_TOPIC':
            if action_param:
                topic_name = action_param
                current_url = webbrowser.get('chrome').open_new_tab('').geturl() # Try to get current URL
                if current_url and current_url.startswith('http'):
                    content = extract_website_content(current_url)
                    if content:
                        explanation = explain_topic_with_gemini(topic_name, content) # You'd need to reimplement or adjust explanation function
                        speak(f"Explaining {topic_name}:")
                        speak(explanation)
                    else:
                        speak("Could not get website content to explain the topic.")
                else:
                    speak("Please navigate to a webpage with relevant content first.")
            else:
                speak("Please specify the topic you want me to explain.")

        elif action_type == 'ANSWER_QUESTION':
            if action_param:
                question = action_param
                current_url = webbrowser.get('chrome').open_new_tab('').geturl() # Try to get current URL
                if current_url and current_url.startswith('http'):
                    content = extract_website_content(current_url)
                    if content:
                        answer = answer_question_with_gemini(question, "", content) # You'd need to reimplement or adjust answer function
                        speak("Answering your question:")
                        speak(answer)
                    else:
                        speak("Could not get website content to answer your question.")
                else:
                    speak("Please navigate to a webpage with relevant content first.")
            else:
                speak("Please specify the question you want me to answer.")

        elif action_type == 'TYPE_IN_BROWSER':
            if action_param:
                text_to_type = action_param
                
                webbrowser.open(f'https://www.google.com/search?q={text_to_type}') # Example: Open search with typed text
                speak(f"Opening a browser tab with: {text_to_type}")

            else:
                speak("Please specify what you want me to type in the browser.")

        elif action_type == 'NONE':
            pass 

def extract_website_content(url):
    """Extracts text content from a website URL using BeautifulSoup."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        text_content = ' '.join(soup.stripped_strings)
        return text_content[:5000] 
    except requests.exceptions.RequestException as e:
        print(f"Website access error: {e}")
        return None

def summarize_content_with_gemini(content): 
    prompt = f"Summarize the following text:\n{content}\nSummary:"
    return get_gemini_response_with_actions(prompt) 

def explain_topic_with_gemini(topic_name, content): 
    prompt = f"Explain the topic '{topic_name}' based on this text:\n{content}\nExplanation:"
    return get_gemini_response_with_actions(prompt) 

def answer_question_with_gemini(question, topic_name, content): 
    prompt = f"Answer the question '{question}' about '{topic_name}' using this text:\n{content}\nAnswer:"
    return get_gemini_response_with_actions(prompt)


if __name__ == "__main__":
    speak("Vision virtual assistant is ready. How can I help you?")
    conversation_history = []

    while True:
        user_command = listen()
        if not user_command:
            continue

        conversation_history.append({'role': 'user', 'content': user_command})

        if "exit" in user_command or "quit" in user_command or "stop" in user_command:
            speak("Goodbye! Have a great learning session.")
            break

        gemini_response = get_gemini_response_with_actions(user_command, conversation_history)
        print(f"Gemini Response: {gemini_response}") 

        execute_action(gemini_response)

        
        if len(conversation_history) > 5:
            conversation_history = conversation_history[-5:]