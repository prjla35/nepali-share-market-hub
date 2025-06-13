# app.py
import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
from deep_translator import GoogleTranslator

# project modules
from scraper import scrape_upcoming_ipos
from market_data import get_market_data, get_all_companies, get_company_details
from analysis import (
    get_in_depth_ipo_analysis, 
    get_market_summary_from_data, 
    analyze_scrip_details,
    get_chat_response
)

# Streamlit config
st.set_page_config(
    page_title="Nepal Stock Market Hub",
    layout="wide"
)

# Session state stuff (for chat history, rate limit, etc.)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_query_time" not in st.session_state:
    st.session_state.last_query_time = None
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
if "current_context" not in st.session_state:
    st.session_state.current_context = None

# Cache functions (so we don't overload APIs every time)
@st.cache_data(ttl=600)
def cached_scrape_ipos(): return scrape_upcoming_ipos()

@st.cache_data(ttl=300)
def cached_get_market_data(): return get_market_data()

@st.cache_data(ttl=3600)
def cached_get_all_companies(): return get_all_companies()

@st.cache_data(ttl=300)
def cached_get_company_details(symbol): return get_company_details(symbol)

# Translation helper (simple but works fine)
@st.cache_data
def translate_text(text, dest_lang='en'):
    if not text or not isinstance(text, str) or dest_lang == 'en':
        return text
    try:
        return GoogleTranslator(source='auto', target=dest_lang).translate(text)
    except Exception as e:
        print(f"Translation Error: {e}")
        return text

# Sidebar UI
with st.sidebar:
    st.header(translate_text("Navigation", "ne" if st.session_state.get('language') == 'नेपाली' else 'en'))
    st.selectbox(translate_text("भाषा / Language", "ne" if st.session_state.get('language') == 'नेपाली' else 'en'), ["English", "नेपाली"], key='language')
    lang_code = 'ne' if st.session_state.language == 'नेपाली' else 'en'
    
    page_options = ["Market Overview", "IPO Center", "Stock Analysis", "AI Chat Assistant"]
    translated_page_options = [translate_text(page, lang_code) for page in page_options]
    
    selected_translated_page = st.radio(
        translate_text("Choose a section", lang_code),
        translated_page_options,
        label_visibility="collapsed"
    )
    page = page_options[translated_page_options.index(selected_translated_page)]
    
    st.markdown("---")
    st.write(translate_text("Having issues or want the latest data?", lang_code))
    if st.button(translate_text("Clear Cache & Refresh Data", lang_code)):
        st.cache_data.clear()
        st.rerun()
    st.markdown("---")
    st.info(translate_text(
        "This app uses AI + unofficial APIs. Info here is educational only, do your own research before investing.", lang_code))

# reusable function for displaying dataframes
def display_styled_dataframe(df):
    if df.empty: return
    column_rename_map = {
        'symbol': translate_text('Symbol', lang_code), 'ltp': translate_text('LTP', lang_code), 
        'pointChange': translate_text('Change', lang_code), 'percentageChange': translate_text('% Change', lang_code),
        'turnover': translate_text('Turnover', lang_code), 'lastTradedPrice': translate_text('LTP', lang_code), 
        'title': translate_text('IPO Announcement', lang_code), 'date': translate_text('Date', lang_code), 
        'link': translate_text('Source', lang_code)
    }
    df_display = df.copy().rename(columns=lambda x: column_rename_map.get(x, x))
    st.dataframe(df_display, use_container_width=True, hide_index=True)

# Main app pages:

if page == "Market Overview":
    st.session_state.current_context = None
    st.title(translate_text("Market Overview", lang_code))
    st.text(translate_text("Real-time NEPSE snapshot", lang_code))
    
    market_data = cached_get_market_data()
    
    if isinstance(market_data, dict) and "error" in market_data:
        st.error(translate_text(f"Failed to fetch market data: {market_data['error']}", lang_code))
    else:
        with st.container(border=True):
            st.subheader(translate_text("Today's AI Market Briefing", lang_code))
            with st.spinner(translate_text("AI analyzing the market...", lang_code)):
                market_summary = get_market_summary_from_data(market_data['gainers'], market_data['losers'], market_data['turnover'])
                st.markdown(translate_text(market_summary, lang_code))
        
        st.markdown("---")
        st.subheader(translate_text("Key Market Indicators", lang_code))
        cols = st.columns(4)
        with cols[0]:
            market_status_str = market_data.get('status', 'Unknown') 
            if "open" in market_status_str.lower():
                st.success(translate_text("Market is OPEN", lang_code))
            else:
                st.error(translate_text("Market is CLOSED", lang_code))
        with cols[1]:
            indices_df = market_data.get('indices', pd.DataFrame())
            if not indices_df.empty:
                main_index = indices_df.loc[indices_df['currentValue'].idxmax()]
                st.metric(label=main_index['index'], value=f"{main_index['currentValue']:.2f}", delta=f"{main_index['change']:.2f} ({main_index['perChange']:.2f}%)")

        st.subheader(translate_text("Market Data", lang_code))
        tabs = [translate_text(t, lang_code) for t in ["Top Gainers", "Top Losers", "Top by Turnover", "All Indices"]]
        tab1, tab2, tab3, tab4 = st.tabs(tabs)
        with tab1: display_styled_dataframe(market_data.get('gainers', pd.DataFrame()))
        with tab2: display_styled_dataframe(market_data.get('losers', pd.DataFrame()))
        with tab3: display_styled_dataframe(market_data.get('turnover', pd.DataFrame()))
        with tab4: st.dataframe(market_data.get('indices', pd.DataFrame()), use_container_width=True, hide_index=True)

elif page == "IPO Center":
    st.title(translate_text("IPO Center", lang_code))
    st.text(translate_text("Latest IPOs + AI-powered analysis", lang_code))
    
    with st.spinner(translate_text("Scraping latest IPO announcements...", lang_code)):
        ipo_data = cached_scrape_ipos()
    
    if isinstance(ipo_data, str):
        st.error(translate_text(f"Failed to scrape IPO data: {ipo_data}", lang_code))
    else:
        display_styled_dataframe(ipo_data[['title', 'date']])
        st.markdown("---")
        if not ipo_data.empty:
            selected_title = st.selectbox(translate_text("Select an IPO for In-Depth AI Analysis:", lang_code), options=ipo_data['title'].tolist())
            if selected_title:
                selected_row = ipo_data[ipo_data['title'] == selected_title].iloc[0]
                st.session_state.current_context = {'type': 'IPO', 'title': selected_title, 'data': selected_row['content']}
                
                st.subheader(f"{translate_text('In-Depth Analysis for', lang_code)}: {selected_title}")
                with st.spinner(translate_text("AI reading full article and generating insights...", lang_code)):
                    ipo_analysis = get_in_depth_ipo_analysis(selected_title, selected_row['content'])
                    st.markdown(translate_text(ipo_analysis, lang_code))
                    with st.expander(translate_text("View Raw Article Text Scraped by AI", lang_code)):
                        st.text(selected_row['content'])

elif page == "Stock Analysis":
    st.title(translate_text("Stock Analysis", lang_code))
    st.text(translate_text("Search any company listed on NEPSE", lang_code))
    
    company_df = cached_get_all_companies()
    if isinstance(company_df, dict) and "error" in company_df:
        st.error(translate_text(f"Could not load company list: {company_df['error']}", lang_code))
    else:
        company_symbols = company_df['symbol'].tolist()
        selected_symbol = st.selectbox(
            translate_text("Type or select a company symbol:", lang_code),
            options=company_symbols, index=None, placeholder=translate_text("Search like 'NABIL', 'HDL'...", lang_code)
        )
        if selected_symbol:
            st.subheader(f"{translate_text('Analysis for', lang_code)} {selected_symbol}")
            with st.spinner(translate_text(f"Fetching + analyzing data for {selected_symbol}...", lang_code)):
                details = cached_get_company_details(selected_symbol)
                if isinstance(details, dict) and "error" in details:
                    st.error(translate_text(f"Could not fetch details: {details['error']}", lang_code))
                else:
                    details_str = json.dumps(details, indent=2)
                    st.session_state.current_context = {'type': 'Stock', 'symbol': selected_symbol, 'data': details_str}
                    
                    ai_analysis = analyze_scrip_details(details_str)
                    st.markdown(translate_text(ai_analysis, lang_code))
                    with st.expander(translate_text("View Raw API Data", lang_code)):
                        st.json(details)

elif page == "AI Chat Assistant":
    st.title(f"💬 {translate_text('AI Chat Assistant (NEPSE Sahayogi)', lang_code)}")
    
    if st.session_state.current_context:
        context_type = st.session_state.current_context.get('type', 'N/A')
        context_name = st.session_state.current_context.get('title') or st.session_state.current_context.get('symbol')
        st.info(f"**{translate_text('Context Loaded', lang_code)}:** {context_type} - {context_name}\n\n{translate_text('AI will use full data for this item.', lang_code)}")
    else:
        st.info(translate_text("No context loaded. Ask general questions or go to IPO/Stock section to load one.", lang_code))

    st.warning(f"**{translate_text('Rate Limit', lang_code)}:** {translate_text('2 messages per minute', lang_code)}")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]): st.markdown(message["content"])

    if prompt := st.chat_input(translate_text("Ask a question...", lang_code)):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        current_time, allow_query = datetime.now(), False
        if st.session_state.last_query_time is None or (current_time - st.session_state.last_query_time) > timedelta(minutes=1):
            st.session_state.query_count, st.session_state.last_query_time, allow_query = 1, current_time, True
        elif st.session_state.query_count < 2:
            st.session_state.query_count += 1; allow_query = True
        
        if allow_query:
            with st.chat_message("assistant"):
                with st.spinner(translate_text("AI analyzing...", lang_code)):
                    response = get_chat_response(prompt, context=st.session_state.current_context)
                    translated_response = translate_text(response, lang_code)
                    st.markdown(translated_response)
                    st.session_state.messages.append({"role": "assistant", "content": translated_response})
        else:
            error_message = translate_text("Rate limit exceeded. Wait a bit.", lang_code)
            with st.chat_message("assistant"): st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
