# Gemini Travel Assistant

## Description
Gemini Travel Assistant is a Streamlit application that provides users with current weather information and top tourist attractions for a specified city. It uses the Gemini AI model and integrates multiple APIs to deliver accurate and helpful travel information.

## Features
- Get current weather details for any city.
- Retrieve top tourist attractions using search tools.
- Interactive and easy-to-use Streamlit interface.
- Utilizes Langchain agents and tools for AI-powered responses.

## Installation
1. Clone the repository or download the project files.
2. Navigate to the `Day 5/Travel_assistant` directory.
3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables
The application requires the following environment variables to be set (e.g., in a `.env` file):
- `WEATHER_API_KEY` - API key for the weather service.
- `GOOGLE_API_KEY` - API key for Google services.
- `TAVILY_API_KEY` - API key for Tavily search service.

## Usage
Run the Streamlit app:
```bash
streamlit run app.py
```
- Enter the name of a city in the input box.
- Click the "Find Info" button.
- View the AI-generated weather and tourist attraction information.

## Dependencies
- langchain
- langchain-google-genai
- requests
- python-dotenv
- duckduckgo-search

## License
This project is licensed under the MIT License.
