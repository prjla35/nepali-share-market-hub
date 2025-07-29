import pandas as pd
from nepse import Nepse

def get_market_data():
    try:
        api = Nepse()
        api.setTLSVerification(False)
        
        status = api.getMarketStatus()
        gainers = api.getTopGainers()
        losers = api.getTopLosers()
        turnover = api.getTopTenTurnoverScrips()
        indices = api.getNepseSubIndices()

        # getNepseIndex returns a list with several indices
        nepse_index_list = api.getNepseIndex()
        nepse_index = next((item for item in nepse_index_list if item['index'] == 'NEPSE Index'), None)
     
        if nepse_index:
            indices_df = pd.DataFrame([nepse_index] + indices)
        else:
            indices_df = pd.DataFrame(indices)

        return {
            "status": status.get('status', 'Unknown'),
            "gainers": pd.DataFrame(gainers),
            "losers": pd.DataFrame(losers),
            "turnover": pd.DataFrame(turnover),
            "indices": indices_df
        }
    except Exception as e:
        print(f"An error occurred while fetching market data: {e}")
        return {"error": str(e)}

def get_all_companies():
    try:
        api = Nepse()
        api.setTLSVerification(False)
        company_list = api.getCompanyList()
        return pd.DataFrame(company_list)
    except Exception as e:
        print(f"An error occurred fetching company list: {e}")
        return {"error": str(e)}

def get_company_details(symbol):
    try:
        api = Nepse()
        api.setTLSVerification(False)
        details = api.getCompanyDetails(symbol)
        return details
    except Exception as e:
        print(f"An error occurred fetching details for {symbol}: {e}")
        return {"error": str(e)}
