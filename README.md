
AI-Powered Nepal Stock Analysis Hub

A comprehensive, user-friendly web application built with Streamlit and Python to provide analysis, real-time data, and AI-powered insights for the Nepali stock market (NEPSE).

This tool is designed for both beginners and experienced investors, consolidating scattered information into a single, interactive dashboard.

✨ Key Features

📈 Live Market Overview: A real-time snapshot of the NEPSE market, including:

AI-generated daily market briefings.

Live market status (Open/Closed).

Key indices and their performance.

Tabs for Top Gainers, Losers, and Top by Turnover.

📰 Deep-Scrape IPO Center:

Automatically scrapes the latest IPO news from financial portals.

Performs a "deep scrape" to fetch the full text of each news article.

Provides in-depth, AI-powered analysis of each IPO, intelligently identifying key details.


🔍 Detailed Stock Analysis:

Search for any company listed on NEPSE.

Fetches detailed company information and financial data via an API.

Presents a structured, AI-generated analysis of the company's fundamentals and price performance.

🤖 Context-Aware AI Chat Assistant ("NEPSE Sahayogi"):

A powerful chatbot that understands the user's current context (e.g., if you are viewing an IPO or a specific stock).

Answers specific questions based on the scraped article text or live stock data.

Functions as a general guide for the app and the Nepali share market.

Includes a rate limit (2 messages/minute) to manage API usage.

🌐 Bilingual Support:

Switch between English and Nepali (नेपाली) languages for a localized experience.

🛠️ Technology Stack

Framework: Streamlit

Language: Python 3.11+

Web Scraping: requests, BeautifulSoup4

Large Language Model (LLM): groq (for AI analysis and chat)

NEPSE Data: nepse-unofficial-api for live market data

Data Handling: pandas

Translation: deep-translator

🚀 Setup and Installation

Follow these steps to get the application running on your local machine.

1. Clone the Repository
git clone https://github.com/your-username/nepali-share-market-hub.git
cd your-repository-name

2. Install Dependencies

It is highly recommended to use a virtual environment.

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install all required packages
pip install -r requirements.txt
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
3. Configure API Keys

The application requires an API key for the Groq LLM service.

⚠️ Important Security Note: The provided llm_client.py hardcodes the API key. This is a major security risk and is not recommended for production or public repositories. The correct way is to use environment variables.

Recommended Setup:

Create a file named .env in the project's root directory.

Add your API key to this file:

GROQ_API_KEY="gsk_YourSecretGroqApiKeyGoesHere"
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END

Modify llm_client.py to securely load the key:

# llm_client.py (Recommended Change)
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv() # Loads variables from .env file

# Securely get the API key
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in .env file. Please set it.")

groq_client = Groq(api_key=groq_api_key)

# ... rest
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END

You will also need to run pip install python-dotenv.

🏃‍♂️ How to Run the Application

Once the dependencies are installed and the API key is configured, run the following command from your terminal:

streamlit run app.py
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Your web browser will automatically open with the application running.

📂 File Structure
.
├── app.py                  # Main Streamlit application, handles UI and page routing
├── scraper.py              # Scrapes IPO news and full article content from ShareSansar
├── market_data.py          # Fetches live market data from the NEPSE Unofficial API
├── analysis.py             # Contains all prompts and functions for LLM-based analysis
├── llm_client.py           # Configures and handles the connection to the Groq API
├── requirements.txt        # Lists all Python dependencies for the project
└── README.md               # You are here!
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END
📜 Disclaimer

This application is for educational and informational purposes only. The data is sourced from unofficial APIs and public websites, and its accuracy is not guaranteed. The AI-generated analyses are based on this data and should not be considered financial advice. Always do your own research (DYOR) before making any investment decisions.

🙏 Acknowledgments

Groq for providing the high-speed LLM inference API.

ShareSansar for being a valuable public source of financial news and IPO data.

The developers of the Nepse Unofficial API.

The Streamlit team for creating an amazing framework for building data apps.
