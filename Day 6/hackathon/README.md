# LinkedIn Connection Relevance Checker

## Description
This project is a Streamlit application that helps users verify if their LinkedIn connections are related to tech domains such as AI, software, or EdTech. It uses the Gemini AI model via Langchain to analyze job titles and determine relevance.

## Features
- Upload a CSV file of scraped LinkedIn connections.
- AI-powered verification of connection relevance to tech domains.
- Displays verification results along with original connection data.
- User-friendly Streamlit interface.

## Installation
1. Clone the repository or download the project files.
2. Navigate to the `Day 6/hackathon` directory.
3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install the required dependencies:
   ```bash
   pip install pandas streamlit langchain_google_genai python-dotenv
   ```

## Usage
Run the Streamlit app:
```bash
streamlit run app.py
```
- Upload a CSV file containing your LinkedIn connections with columns: Name, Title, Messages, Endorsements, Events.
- The app will analyze and display which connections are relevant to the tech domain.

## Environment Variables
The application uses a `.env` file to load environment variables for API keys required by the Gemini AI model and other services. Make sure to create a `.env` file with the necessary keys.

## License
This project is licensed under the MIT License.
