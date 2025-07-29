# app.py
import streamlit as st
import pandas as pd
import json
# --- NEW, BETTER TRANSLATOR LIBRARY ---
from deep_translator import GoogleTranslator

# Import your custom modules
from scraper import scrape_upcoming_ipos
from market_data import get_market_data, get_all_companies, get_company_details
from analysis import get_in_depth_ipo_analysis, get_market_summary_from_data, get_beginner_analysis, analyze_scrip_details

# --- Page Configuration ---
st.set_page_config(
    page_title="Nepal Stock Market Hub",
    layout="wide"
)

# --- Caching Functions ---
@st.cache_data(ttl=600)
def cached_scrape_ipos(): return scrape_upcoming_ipos()
@st.cache_data(ttl=300)
def cached_get_market_data(): return get_market_data()
@st.cache_data(ttl=3600)
def cached_get_all_companies(): return get_all_companies()
@st.cache_data(ttl=300)
def cached_get_company_details(symbol): return get_company_details(symbol)

# --- CORRECTED TRANSLATION FUNCTION using deep-translator ---
@st.cache_data
def translate_text(text, dest_lang='en'):
    """Translates text to the destination language and caches the result."""
    if not text or dest_lang == 'en':
        return text
    try:
        # The syntax for deep-translator is slightly different but simpler
        return GoogleTranslator(source='auto', target=dest_lang).translate(text)
    except Exception as e:
        print(f"Translation Error: {e}")
        return text # If translation fails, return original text

# --- Sidebar Navigation ---
with st.sidebar:
    st.header("Navigation")
    st.selectbox("भाषा / Language", ["English", "नेपाली"], key='language')
    lang_code = 'ne' if st.session_state.language == 'नेपाली' else 'en'
    page_options = ["Market Overview", "IPO Center", "Stock Analysis"]
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
        "This application uses AI and unofficial APIs for data analysis. "
        "All information is for educational purposes only. Always conduct your own research before investing.", lang_code))

# --- UI Helper Function ---
def display_styled_dataframe(df):
    column_rename_map = {
        'symbol': translate_text('Symbol', lang_code), 'ltp': translate_text('LTP', lang_code), 
        'pointChange': translate_text('Change', lang_code), 'percentageChange': translate_text('% Change', lang_code),
        'turnover': translate_text('Turnover', lang_code), 'lastTradedPrice': translate_text('LTP', lang_code), 
        'title': translate_text('IPO Announcement', lang_code), 'date': translate_text('Date', lang_code), 
        'link': translate_text('Source', lang_code)
    }
    df_display = df.rename(columns=lambda x: column_rename_map.get(x, x))
    column_config = {
        translate_text("Source", lang_code): st.column_config.LinkColumn(display_text=translate_text("Read Article", lang_code))
    }
    st.dataframe(df_display, use_container_width=True, hide_index=True, column_config=column_config)

# ==============================================================================
# The rest of the app logic remains the same.
# No changes are needed below this line.
# ==============================================================================

if page == "Market Overview":
    st.title(translate_text("Market Overview", lang_code))
    st.text(translate_text("A real-time snapshot of the Nepal Stock Exchange.", lang_code))
    market_data = cached_get_market_data()
    if market_data.get("error"):
        st.error(translate_text(f"Failed to fetch market data: {market_data['error']}", lang_code))
    else:
        with st.container(border=True):
            st.subheader(translate_text("Today's AI Market Briefing", lang_code))
            with st.spinner(translate_text("Our AI analyst is studying the market...", lang_code)):
                market_summary = get_market_summary_from_data(market_data['gainers'], market_data['losers'], market_data['turnover'])
                st.markdown(translate_text(market_summary, lang_code), unsafe_allow_html=True)
        st.markdown("---")
        st.subheader(translate_text("Key Market Indicators", lang_code))
        cols = st.columns(4)
        with cols[0]:
            market_status_str = market_data.get('status', 'Unknown') 
            if "open" in market_status_str.lower():
                st.success(translate_text("Market is OPEN", lang_code))
            else:
                st.error(translate_text("Market is CLOSED", lang_code))
        indices_df = market_data.get('indices')
        index_names = [
            "NEPSE Index",
            "Microfinance Index",
            "Life Insurance",
            "Mutual Fund",
            "Investment Index",
            "Banking SubIndex",
            "Hotels And Tourism Index",
            "Others Index",
            "HydroPower Index",
            "Development Bank Index",
            "Manufacturing And Processing",
            "Non Life Insurance",
            "Finance Index",
            "Trading Index"
        ]
        for row_start in range(0, len(index_names), 4):
            cols = st.columns(4)
            for i, index_name in enumerate(index_names[row_start:row_start+4]):
                with cols[i]:
                    if indices_df is not None and not indices_df.empty:
                        row = indices_df[indices_df['index'] == index_name]
                        if not row.empty:
                            index_row = row.iloc[0]
                            st.metric(
                                label=translate_text(index_row['index'], lang_code),
                                value=f"{index_row['currentValue']:.2f}",
                                delta=f"{index_row['change']:.2f} ({index_row['perChange']:.2f}%)"
                            )
                        else:
                            st.metric(label=translate_text(index_name, lang_code), value="N/A")

        st.subheader(translate_text("Market Data", lang_code))
        tabs = [translate_text(t, lang_code) for t in ["Top Gainers", "Top Losers", "Top by Turnover", "All Indices"]]
        tab1, tab2, tab3, tab4 = st.tabs(tabs)
        with tab1: display_styled_dataframe(market_data['gainers'])
        with tab2: display_styled_dataframe(market_data['losers'])
        with tab3: display_styled_dataframe(market_data['turnover'])
        with tab4: st.dataframe(market_data['indices'], use_container_width=True, hide_index=True)

elif page == "IPO Center":
    st.title(translate_text("IPO Center", lang_code))
    st.text(translate_text("Latest Initial Public Offering announcements and AI-powered analysis.", lang_code))
    with st.container(border=True):
        st.subheader(translate_text("Recently Announced IPOs", lang_code))
        with st.spinner(translate_text("Scraping for the latest IPO announcements...", lang_code)):
            ipo_data = cached_scrape_ipos()
        if isinstance(ipo_data, str):
            st.error(translate_text(f"Failed to scrape IPO data: {ipo_data}", lang_code))
        else:
            display_df = ipo_data[['title', 'date', 'link']]
            display_styled_dataframe(display_df)
            st.markdown("---")
            if not ipo_data.empty:
                selected_title = st.selectbox(translate_text("Select an IPO for In-Depth AI Analysis:", lang_code), options=ipo_data['title'].tolist())
                if selected_title:
                    st.subheader(f"{translate_text('In-Depth Analysis for', lang_code)}: {selected_title}")
                    with st.spinner(translate_text("AI is reading the full article and generating insights...", lang_code)):
                        selected_row = ipo_data[ipo_data['title'] == selected_title].iloc[0]
                        article_content = selected_row['content']
                        ipo_analysis = get_in_depth_ipo_analysis(selected_title, article_content)
                        st.markdown(translate_text(ipo_analysis, lang_code), unsafe_allow_html=True)
                        with st.expander(translate_text("View Raw Article Text Scraped by AI", lang_code)):
                            st.text(article_content)

elif page == "Stock Analysis":
    st.title(translate_text("Stock Analysis", lang_code))
    st.text(translate_text("Search for any company listed on NEPSE to get a detailed AI-powered analysis.", lang_code))
    company_df = cached_get_all_companies()
    if isinstance(company_df, dict) and company_df.get("error"):
        st.error(translate_text(f"Could not load company list: {company_df['error']}", lang_code))
    else:
        company_symbols = company_df['symbol'].tolist()
        selected_symbol = st.selectbox(
            translate_text("Type or select a company symbol:", lang_code),
            options=company_symbols,
            index=None,
            placeholder=translate_text("Search for a symbol like 'NABIL', 'HDL'...", lang_code)
        )
        if selected_symbol:
            st.subheader(f"{translate_text('Analysis for', lang_code)} {selected_symbol}")
            with st.container(border=True):
                with st.spinner(translate_text(f"Fetching and analyzing data for {selected_symbol}...", lang_code)):
                    details = cached_get_company_details(selected_symbol)
                    if isinstance(details, dict) and details.get("error"):
                        st.error(translate_text(f"Could not fetch details for {selected_symbol}: {details['error']}", lang_code))
                    else:
                        details_str = json.dumps(details, indent=2)
                        ai_analysis = analyze_scrip_details(details_str)
                        st.markdown(translate_text(ai_analysis, lang_code), unsafe_allow_html=True)
                        with st.expander(translate_text("View Raw API Data", lang_code)):
                            st.json(details)

