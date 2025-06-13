# AI-Powered Nepal Stock Analysis Hub

A comprehensive, user-friendly web application built with Streamlit and Python to provide analysis, real-time data, and AI-powered insights for the Nepali stock market (NEPSE).

This tool is designed for both beginners and experienced investors, consolidating scattered information into a single, interactive dashboard.

---

## ✨ Key Features

### 📈 Live Market Overview
- AI-generated daily market briefings.
- Live market status (Open/Closed).
- Key indices and their performance.
- Tabs for Top Gainers, Losers, and Top by Turnover.

###  Deep-Scrape IPO Center
- Automatically scrapes the latest IPO news from financial portals.
- Performs a "deep scrape" to fetch the full text of each news article.
- Provides in-depth, AI-powered analysis of each IPO, intelligently identifying key details.

### 🔍 Detailed Stock Analysis
- Search for any company listed on NEPSE.
- Fetches detailed company information and financial data via an API.
- Presents a structured, AI-generated analysis of the company's fundamentals and price performance.

###  Context-Aware AI Chat Assistant ("NEPSE Sahayogi")
- A powerful chatbot that understands the user's current context (e.g., IPOs or specific stocks).
- Answers specific questions based on the scraped article text or live stock data.
- Functions as a general guide for the app and the Nepali share market.
- Includes a rate limit (2 messages/minute) to manage API usage.

###  Bilingual Support
- Switch between English and Nepali (नेपाली) languages for a localized experience.

---

## 🛠️ Technology Stack

- **Framework:** Streamlit
- **Language:** Python 3.11+
- **Web Scraping:** requests, BeautifulSoup4
- **Large Language Model (LLM):** Groq (for AI analysis and chat)
- **NEPSE Data:** nepse-unofficial-api for live market data
- **Data Handling:** pandas
- **Translation:** deep-translator

---

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/nepali-share-market-hub.git
cd nepali-share-market-hub
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Configure API keys
```bash
GROQ_API_KEY="API KEY"
```
### 4. Running the program
```bash
streamlit run app.py
```
## File Structure
```bash
.
├── app.py           # Main Streamlit application, handles UI and page routing
├── scraper.py       # Scrapes IPO news and full article content from ShareSansar
├── market_data.py   # Fetches live market data from the NEPSE Unofficial API
├── analysis.py      # Contains all prompts and functions for LLM-based analysis
├── llm_client.py    # Configures and handles the connection to the Groq API
├── requirements.txt # Lists all Python dependencies for the project
```

## Acknowledgments

#### ShareSansar for being a valuable public source of financial news and IPO data.

#### The developers of the Nepse Unofficial API.


## Note: Most of the code was written by AI (gemini) and There are many errors in the program. Donot take this project seriously as it was just a hobby project which was created in less than 4 hours. 

