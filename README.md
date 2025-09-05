# SyncroPatch Support Bot

A Streamlit web application that provides AI-powered support for SyncroPatch users. The bot can answer technical questions, analyze documents, and access Jira projects.

## Features

- 🤖 AI-powered responses using OpenAI GPT-4
- 📄 Document analysis and file upload support
- 🎯 Jira project access (FSM, FSO, SP-WISHLIST, SCS)
- 💾 Memory management (1-hour session memory)
- 🔄 Real-time chat interface
- 📎 File attachment support

## Live Demo

[Deploy to Streamlit Cloud](https://share.streamlit.io)

## Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Configuration

The app connects to an Azure Function for AI processing. The function URL is configured in the code.

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** Azure Functions
- **AI:** OpenAI GPT-4
- **Storage:** Azure Table Storage
