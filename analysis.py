# analysis.py
from llm_client import generate_response
import pandas as pd

def get_in_depth_ipo_analysis(ipo_title, ipo_content):
    """
    Analyzes the full content of an IPO article.
    It intelligently decides whether to provide a detailed "INSIGHT" report (for upcoming IPOs)
    or a general summary (for other news).
    """
    prompt = f"""
    You are an expert financial analyst for the Nepal stock market (NEPSE).
    Your task is to analyze the following news article.

    **Title:** {ipo_title}

    **Full Article Content:**
    ---
    {ipo_content}
    ---

    **Instructions:**
    1.  First, carefully read the title and content to determine if this article is announcing a **new, upcoming IPO for the general public**.
    2.  **If it IS an upcoming IPO announcement**, you MUST generate the detailed "INSIGHT" report using the exact format below.
    3.  **If it is NOT an upcoming IPO** (e.g., it's news about right shares, an auction, a past IPO result, etc.), then simply write a concise, one-paragraph summary of the news and **DO NOT** generate the "INSIGHT" report.

    ---
    **"INSIGHT" Report Format (Only use for upcoming IPOs):**

    ### 1. Key IPO Details
    - **Issue Size:** (Find the total number of shares and value in Rs.)
    - **Opening/Closing Dates:** (Find the dates mentioned.)
    - **Type of Shares:** (e.g., Ordinary, To Locals, To Foreign Employed.)
    - **Issue Manager:** (Find the name of the capital/issue manager.)
    - **Credit Rating:** (If mentioned, state the rating and what it means, e.g., "CARE-NP BB+ indicates moderate risk of default.")

    ### 2. Company & Sector Analysis
    - **Company Business:** What does the company do? What is its main line of business?
    - **Purpose of IPO:** Why is the company raising this money? (e.g., project development, loan repayment.)
    - **Sector Outlook:** Briefly comment on the outlook for this company's sector (e.g., Hydropower, Finance) in Nepal.

    ### 3. AI Speculation & Educational Insights
    **IMPORTANT DISCLAIMER: The following is AI-generated speculation based on public data and is for educational purposes only. It is NOT financial advice. Always do your own research (DYOR).**

    - **Application Strategy:** Based on NEPSE's allotment rules where most IPOs are heavily oversubscribed, what is the standard application strategy for retail investors? (Hint: Mention the standard 10-unit application).
    - **Potential Demand:** Based on the article, comment on the likely demand for this IPO.
    - **Opening Range Estimate:** Based on the company's latest Net Worth Per Share (if mentioned in the article), what is the legally permissible opening price range for its first day of trading? (Explain that it's typically 1x to 3x the Net Worth Per Share). If the net worth is not mentioned, state that this cannot be estimated from the provided text.
    ---
    """
    return generate_response(prompt)


def analyze_scrip_details(scrip_data):
    """
    Analyzes the detailed JSON data for a single company and provides a structured report.
    """
    prompt = f"""
    You are a financial analyst. Analyze the following raw JSON data for a company listed on NEPSE
    and present a clear, easy-to-understand report in markdown format.

    Raw Company Data:
    ```json
    {scrip_data}
    ```

    Your report should be structured as follows:

    ### 🏢 Company Overview
    - **Company Name & Symbol:**
    - **Sector:**

    ### 📈 Price & Performance
    - **Last Traded Price (LTP):**
    - **Day's High/Low:**
    - **52-Week High/Low:**
    - **Market Capitalization:**

    ### 📊 Fundamental Snapshot
    - **Listed Shares:**
    - **Paid-Up Capital:**

    ### 💡 AI Interpretation for Beginners
    Based on all the data, provide a simple, one-paragraph interpretation. Explain what this information means. For example, is the stock trading closer to its yearly high or low? Is the market capitalization large or small for the Nepali market?
    """
    return generate_response(prompt)


def get_market_summary_from_data(gainers_df, losers_df, turnover_df):
    """
    Analyzes market data DataFrames to produce a daily market briefing.
    """
    prompt = f"""
    You are a stock market analyst for NEPSE. Based on the following data, provide a "Daily Market Insight" summary in markdown.

    Top 5 Gainers:
    {gainers_df.head().to_string()}

    Top 5 Losers:
    {losers_df.head().to_string()}

    Top 5 by Turnover:
    {turnover_df.head().to_string()}

    Your analysis should cover:
    1.  **Overall Market Sentiment:** The general mood of the market today.
    2.  **Sector Spotlight:** Any noticeable trends in specific sectors.
    3.  **Notable Movers:** Interesting companies from the lists.
    4.  **A brief takeaway for investors.**
    """
    return generate_response(prompt)


#=======

def get_chat_response(query, context=None):
    """
    Generates a context-aware response for the chatbot. This new version is significantly more intelligent.
    """
    # This is the new, more sophisticated "brain" for the chatbot.
    system_prompt = """
    You are 'NEPSE Sahayogi', a helpful AI assistant embedded in a stock market analysis app.
    Your primary goal is to assist users by answering their questions about the Nepali share market.

    You have three modes of operation:

    1.  **No Context (General Queries):**
        - If you are not given any specific data, answer the user's question using your general knowledge of the Nepali market, investing, and finance.
        - Example Question: "What is a DEMAT account?"
        - Example Answer: "A DEMAT account is an electronic account that holds shares and securities..."

    2.  **IPO Context (Article Data):**
        - If you are given context of `type: 'IPO'` with article data, you MUST prioritize information found in that data to answer the user's question.
        - You can ask the user to check the 'IPO Center' page for more details.
        - Example Question: "Who is the issue manager for this IPO?"
        - Example Answer: "Based on the article provided, the issue manager is [Name from Article]..."

    3.  **Stock Context (JSON Data):**
        - If you are given context of `type: 'Stock'` with JSON data, you MUST prioritize information from that JSON to answer.
        - You can ask the user to check the 'Stock Analysis' page for the full report.
        - Example Question: "What is the 52-week high for this stock?"
        - Example Answer: "According to the data, the 52-week high for this stock is [Value from JSON]..."

    **General Rules:**
    - Be polite, encouraging, and clear, especially with beginners.
    - **Never give direct financial advice** (e.g., "buy this stock"). Instead, provide information and explain concepts.
    - You can guide users on how to use the app. For example, if they ask about top gainers, tell them to check the "Market Overview" page.
    """
    
    if context and isinstance(context, dict) and 'data' in context:
        context_type = context.get('type', 'Unknown')
        context_name = context.get('title') or context.get('symbol', 'N/A')
        
        full_prompt = f"""{system_prompt}

        ---
        **CURRENT CONTEXT FOR THIS QUERY:**
        - **Type:** {context_type}
        - **Name:** {context_name}
        - **Data:** 
        ```
        {context['data']}
        ```
        ---

        A user is asking the following question. Use the rules and context data above to formulate your answer.
        
        **User's Question:** {query}
        """
    else:
        # Fallback to general knowledge if no context is provided
        full_prompt = f"{system_prompt}\n\n**A user is asking a general question. Use your 'No Context' mode to answer.**\n\n**User's Question:** {query}"
        
    return generate_response(full_prompt)

