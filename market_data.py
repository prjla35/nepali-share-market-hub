import pandas as pd
from nepse import Nepse

def get_market_data():
    """
    Fetches a wide range of live market data for the main dashboard.
    """
    try:
        api = Nepse()
        api.setTLSVerification(False)
        
        status = api.getMarketStatus()
        gainers = api.getTopGainers()
        losers = api.getTopLosers()
        turnover = api.getTopTenTurnoverScrips()
        indices = api.getNepseSubIndices()

        gainers_df = pd.DataFrame(gainers)
        losers_df = pd.DataFrame(losers)
        turnover_df = pd.DataFrame(turnover)
        indices_df = pd.DataFrame(indices)

        return {
            "status": status.get('status', 'Unknown'),
            "gainers": gainers_df,
            "losers": losers_df,
            "turnover": turnover_df,
            "indices": indices_df
        }

    except Exception as e:
        print(f"An error occurred while fetching market data: {e}")
        return {"error": str(e)}

def get_all_companies():
    """
    Fetches the list of all companies for the search functionality.
    """
    try:
        api = Nepse()
        api.setTLSVerification(False)
        company_list = api.getCompanyList()
        return pd.DataFrame(company_list)
    except Exception as e:
        print(f"An error occurred fetching company list: {e}")
        return {"error": str(e)}

def get_company_details(symbol):
    """
    Fetches detailed data for a single company symbol.
    """
    try:
        api = Nepse()
        api.setTLSVerification(False)
        details = api.getCompanyDetails(symbol)
        return details
    except Exception as e:
        print(f"An error occurred fetching details for {symbol}: {e}")
        return {"error": str(e)}
