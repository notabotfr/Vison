# Vision: Voice-Controlled Virtual Assistant for Education

Vision is a voice-controlled virtual assistant designed to assist blind students with online education.  It utilizes speech recognition, text-to-speech, the Gemini API, and web automation to provide an accessible learning experience.

## Features

*   **Voice Control:** Interact with the assistant using voice commands.
*   **Text-to-Speech:** Vision speaks responses and reads content aloud.
*   **Gemini API Integration:** Leverages the Gemini API for natural language understanding, question answering, summarization, and explanation of topics.
*   **Web Automation:** Performs actions in a web browser, such as opening URLs, searching the web, reading webpage content, and typing in the browser.
*   **Action Keyword System:** Uses a structured action keyword system for Gemini to trigger specific tasks, enabling a deterministic and reliable workflow.
*   **Conversation History:** Maintains a conversation history for context-aware interactions.

## Prerequisites

*   **Python 3.7+**
*   **Google Gemini API Key:**  You *must* obtain a Gemini API key from [Google AI Studio](https://makersuite.google.com/).  Follow the instructions in the "Securely Store Your API Key" section below.
*   **A working microphone and speakers.**
*   **Internet connection.**

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <your_repository_url>
    cd <your_repository_directory>
    ```

2.  **Install Dependencies:**

    ```bash
    pip install SpeechRecognition pyttsx3 beautifulsoup4 requests google-generativeai python-dotenv
    ```

## Securely Store Your API Key

**Important:** Do *not* hardcode your Gemini API key directly into the `main.py` file! This is a major security risk.  Instead, use environment variables.

1.  **Create a `.env` file:**  In the same directory as your `main.py` file, create a file named `.env`.

2.  **Add your API key to the `.env` file:**

    ```
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY
    ```

    Replace `YOUR_GEMINI_API_KEY` with your actual Gemini API key.

3.  **Add `.env` to `.gitignore`:** Make sure your `.env` file is *not* committed to your Git repository. Add `.env` to your `.gitignore` file.

## Usage

1.  **Set the GEMINI_API_KEY environment variable:** This step is already handled if you followed the above instructions for .env
2.  **Run the script:**

    ```bash
    python main.py
    ```

3.  **Interact with Vision:** Speak to the assistant and provide voice commands. Vision will respond verbally and perform actions in the web browser as instructed.

## Voice Commands and Actions

Vision understands natural language commands. Here are some example commands and the actions they trigger:

*   "Open a browser": Opens the default web browser.
*   "Search the web for python tutorial w3schools": Performs a web search using Google.
*   "Navigate to https://www.w3schools.com/python/": Opens the specified URL in the browser.
*   "Read page content": Reads the text content of the current webpage aloud.
*   "Summarize content": Provides a summary of the current webpage.
*   "Explain python variables": Explains the specified topic based on the current webpage content.
*   "What is python indentation?": Answers the question using the current webpage.
*   "Type w3schools.com in the browser": Types the specified text in the browser's address bar
*   "Exit", "Quit", "Stop": Exits the application.

## Implementation Details

*   **Speech Recognition:**  Uses the `speech_recognition` library to convert voice input to text.
*   **Text-to-Speech:** Uses the `pyttsx3` library to convert text responses to speech.
*   **Gemini API:**  Leverages the Google Gemini API for natural language understanding and generation. The `get_gemini_response_with_actions` function formats the prompt, calls the API, and extracts the response.
*   **Action Execution:** The `execute_action` function parses the Gemini response for `ACTION:` keywords and performs the corresponding actions using the `webbrowser` library.
*   **Web Scraping:** The `extract_website_content` function extracts the text content from a webpage using `requests` and `BeautifulSoup4`.

## Limitations

*   **Dependency on Gemini API:** Requires a valid and active Gemini API key.
*   **Web Automation Reliability:** Web automation relies on the `webbrowser` library, which may have limitations in certain environments.  The script attempts to get current URLs and content but this may be unreliable.
*   **Error Handling:** Error handling is implemented but may need further refinement.
*   **No Current URL Retreival** The script is not reliable in getting current URL

## Future Enhancements

*   **Improve Web Automation:** Implement more robust web automation using libraries like Selenium or Playwright for better reliability and cross-browser compatibility.
*   **Enhance Error Handling:** Add more comprehensive error handling and logging.
*   **Implement a GUI:** Develop a graphical user interface for a more user-friendly experience.
*   **Add More Actions:** Expand the range of available actions to support more complex tasks.
*   **Improve Voice Command Recognition:** Refine the voice command recognition for better accuracy and flexibility.
*   **Implement user authentication**
*   **Integrate the model into mobile devices**
*   **Implement multithreading to prevent program from freezing**
*   **Integrate more web browser functionality (tab management, incognito etc)**

## Contributing
Note that this is incomplete! We would like to hear your suggestions and improvements.
Contributions are welcome! Please feel free to submit pull requests with bug fixes, improvements, or new features.

## License

[MIT License](LICENSE)
