# analysis.py
from llm_client import generate_response
import pandas as pd

# --- IPO Analysis Functions (existing) ---

def get_ipo_summary(ipo_title):
    prompt = f"Provide a brief, one-paragraph summary for the following IPO announcement in Nepal: \"{ipo_title}\". Explain what the company does and the purpose of the IPO."
    return generate_response(prompt)

def get_beginner_analysis(ipo_title):
    prompt = f"As a financial expert advising a beginner, analyze the upcoming IPO: \"{ipo_title}\". Explain in simple terms what investors should consider, including potential risks and rewards."
    return generate_response(prompt)

# --- NEW: Market Data Analysis Functions ---

def get_market_summary_from_data(gainers_df, losers_df, turnover_df):
    """
    Analyzes market data DataFrames to produce a daily market briefing.
    """
    prompt = f"""
    You are a stock market analyst for the Nepali stock market (NEPSE).
    Based on the following data, provide a "Daily Market Insight" summary.

    Top 5 Gainers today:
    {gainers_df.head().to_string()}

    Top 5 Losers today:
    {losers_df.head().to_string()}

    Top 5 Companies by Turnover:
    {turnover_df.head().to_string()}

    Your analysis should be in markdown and cover these points:
    1.  **Overall Market Sentiment:** Briefly describe the general mood of the market today based on the data.
    2.  **Sector Spotlight:** Are there any noticeable trends in specific sectors (e.g., Hydropower, Finance)? Mention any sectors that appear frequently in the lists.
    3.  **Notable Movers:** Point out any particularly interesting companies from the lists and briefly explain why they might be notable (e.g., a blue-chip company in the gainers list, or a high-turnover stock).
    4.  **Conclude with a brief takeaway for investors.**
    """
    return generate_response(prompt)


def analyze_scrip_details(scrip_data):
    """
    Analyzes the detailed JSON data for a single company and provides insights.
    """
    prompt = f"""
    You are a financial analyst. A user has requested details for a company listed on the Nepal Stock Exchange.
    Analyze the following raw JSON data and present a clear, easy-to-understand report in markdown format.

    Raw Company Data:
    ```json
    {scrip_data}
    ```

    Your report should be structured as follows:

    ### 🏢 Company Overview
    - **Company Name:** (Extract from security.companyId.companyName)
    - **Symbol:** (Extract from security.symbol)
    - **Sector:** (Extract from security.companyId.sectorMaster.sectorDescription)

    ### 📈 Price & Performance
    - **Last Traded Price (LTP):** (Extract from securityDailyTradeDto.lastTradedPrice)
    - **Day's High/Low:** (Extract from highPrice and lowPrice)
    - **52-Week High/Low:** (Extract from fiftyTwoWeekHigh and fiftyTwoWeekLow)
    - **Market Capitalization:** (Extract from marketCapitalization)

    ### 📊 Fundamental Snapshot
    - **Listed Shares:** (Extract from stockListedShares)
    - **Paid-Up Capital:** (Extract from paidUpCapital)
    - **Share Structure:** Briefly describe the public vs. promoter share percentage.

    ### 💡 AI Interpretation for Beginners
    Based on all the data, provide a simple, one-paragraph interpretation. Explain what this information means. For example, is the stock trading closer to its yearly high or low? Is the market capitalization large or small for the Nepali market?
    """
    return generate_response(prompt)

def get_in_depth_ipo_analysis(ipo_title, ipo_content):
    """
    Analyzes the full content of an IPO article to provide deep insights.
    """
    prompt = f"""
    You are an expert financial analyst for the Nepal stock market (NEPSE).
    Thoroughly analyze the following IPO announcement based on its title and the full article content.

    **Title:** {ipo_title}

    **Full Article Content:**
    ---
    {ipo_content}
    ---
if it is about upcoming ipo provide INSIGHT the following and if it is not about upcoming ipo generate a summary news of the article and donot generate INSIGHT.
   ISNIGHT: Based on the provided text, generate a report in markdown format with the following structure:

    ### 1. Key IPO Details
    - **Issue Size:** (Total number of shares, value in Rs.)
    - **Opening/Closing Dates:**
    - **Type of Shares:** (e.g., Ordinary, To Locals, To Foreign Employed)
    - **Issue Manager:**
    - **Credit Rating:** (If mentioned, state the rating and what it means, e.g., "CARE-NP BB+ indicates moderate risk")

    ### 2. Company & Sector Analysis
    - **Company Business:** What does the company do? What is its main line of business?
    - **Purpose of IPO:** Why is the company raising this money? (e.g., project development, loan repayment)
    - **Sector Outlook:** Briefly comment on the outlook for this company's sector (e.g., Hydropower, Finance) in Nepal.

    ### 3. AI Speculation & Educational Insights
    **IMPORTANT DISCLAIMER: The following is AI-generated speculation based on public data and is for educational purposes only. It is NOT financial advice. Always do your own research (DYOR).**

    - **Application Strategy:** Based on NEPSE's allotment rules where most IPOs are oversubscribed, what is the typical application strategy for retail investors? (Hint: Mention the standard 10-unit application).
    - **Potential Demand:** Comment on the likely demand for this IPO. (e.g., "Given the small issue size for the general public, demand is expected to be extremely high.")
    - **Opening Range Estimate:** Based on the company's latest Net Worth Per Share (if mentioned in the article), what is the legally permissible opening price range for the first day of trading? (Explain that it's typically 1x to 3x the Net Worth Per Share). If the net worth is not mentioned, state that this cannot be estimated from the text.
    """
    return generate_response(prompt)
