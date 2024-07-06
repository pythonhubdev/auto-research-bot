# AutoResearchBot

A multi-agent system that automates research and generates concise reports on given topics using Langchain and
Streamlit, with data stored in SQLite.

## Features

- **Automated Research**: Gathers information on a given topic using various APIs.
- **Summarization**: Generates concise summaries using a language model.
- **Interactive Interface**: User-friendly Streamlit interface to input topics and view/edit summaries.
- **Database Integration**: Stores edited summaries in an SQLite database.

## Requirements

- Python 3.10+
- Docker (for containerized setup)

## Setup

### Local Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/AutoResearchBot.git
   cd AutoResearchBot
   ```

2. **Create a Virtual Environment:**
   ```bash
   poetry install
   poetry shell
   ```
3. **Set Up Environment Variables:**
   Create a `.env` file in the root directory and add the following:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   ```
4. Run the Application:
   ```bash
   streamlit run app.py
   ```

## Docker Setup

1. Build the Docker Image:
    ```bash
    docker build -t autoresearchbot .
    ```

2. Run the Docker Container:
    ```bash
    docker run -d -p 8501:8501 --env OPENAI_API_KEY=your_openai_api_key autoresearchbot
    ```

## Usage

1. **Input a Topic:** Enter a topic in the input field on the Streamlit interface.

2. **Generate Report:** Click the "Generate Report" button to fetch data and generate a summary.

3. **Edit and Save Summary:** Edit the summary if needed and click the "Save Summary" button to store it in the
   database.
