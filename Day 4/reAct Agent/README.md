# ReAct Agent

## Project Description
ReAct Agent is a Streamlit web application that leverages the ReAct (Reasoning and Acting) pattern to perform structured web research. Given a research topic, the agent generates in-depth research questions using the Gemini API, searches for relevant answers on the web using the Tavily search client, and compiles the findings into a well-structured markdown report.

## Features
- Generate 5-6 in-depth research questions about any given topic.
- Perform advanced web searches to find relevant answers for each question.
- Summarize and compile search results into a comprehensive markdown report.
- Interactive web interface built with Streamlit for easy use.
- Downloadable research report for offline reading and sharing.

## Installation

1. Clone the repository or download the project files.

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables for API keys. Create a `.env` file in the project root with the following content:
```
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```
Replace `your_gemini_api_key_here` and `your_tavily_api_key_here` with your actual API keys.

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. In the web interface, enter a research topic in the input box.

3. Click the "Generate Report" button to start the research process.

4. View the generated research questions and web-sourced answers.

5. Download the final research report as a markdown file.

## Main Components

- `agent.py`: Contains the `ReActAgent` class that generates research questions using the Gemini API and fetches answers using the Tavily search client.
- `app.py`: Streamlit application that provides the user interface for inputting topics, displaying questions and answers, and generating the report.
- `report_generator.py`: Generates a structured markdown report from the research questions and answers.

## Environment Variables

- `GEMINI_API_KEY`: API key for accessing the Gemini generative model.
- `TAVILY_API_KEY`: API key for accessing the Tavily search service.

Make sure these are set in your environment or in a `.env` file for the app to function correctly.

## License

This project is provided as-is without any warranty. Use it responsibly and ensure compliance with the terms of service of the APIs used.
