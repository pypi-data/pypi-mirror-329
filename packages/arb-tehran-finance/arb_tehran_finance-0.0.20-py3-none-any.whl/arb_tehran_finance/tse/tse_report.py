# imports:
import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()

import aiohttp
import asyncio
from unsync import unsync
import tracemalloc

import datetime
import jdatetime
import calendar
import time
import re

from persiantools import characters
from IPython.display import clear_output

from fake_useragent import UserAgent



################################################################################################################################################################################

ua = UserAgent()
headers = {'User-Agent': ua.random}

################################################################################################################################################################################
################################################################################################################################################################################

def list_stock():
    url = requests.get('http://old.tsetmc.com/tsev2/data/MarketWatchPlus.aspx')
    main_text = url.text

    csvs = main_text.split('@')
    main_csv = csvs[2]
    csv = main_csv.split(';')

    list_stocks=[]
    for i in range(0,len(csv)):
        list=csv[i].split(",")[2]
        list_stocks.append(list)
    
    df_stock=pd.DataFrame(list_stocks,columns=['stock'])

    return df_stock

################################################################################################################################################################################
################################################################################################################################################################################


def marketwatch():
    """
    Function Description:
    marketwatch() retrieves market data from the old TSETMC MarketWatch page. 
    The function fetches real-time market data, processes it, and returns a DataFrame 
    with key market indicators for various symbols, such as opening price, closing price, 
    volume, and more.

    Parameters:
    None

    Returns:
    - A DataFrame containing market data with columns like 'webid', 'symbol', 'name', 
      'open', 'close', 'volume', 'yesterday', etc.
    - If the request fails or the data format is not as expected, the function returns None 
      and prints an error message.

    Example Usage:
    To retrieve market data from the old TSETMC MarketWatch page, use the following:
    marketwatch()
    
    This will return a DataFrame with the market data of various symbols, including 
    prices, volumes, and other related details.

    Notes:
    - The function performs an HTTP request to fetch data and processes the CSV-formatted 
      response into a structured DataFrame.
    - Numerical values such as 'open', 'close', 'volume', and 'value' are converted to integers 
      for consistency in data processing.
    - If the data format changes or the structure is unexpected, the function will handle it 
      gracefully and return None.
    - The function uses a timeout of 10 seconds to prevent excessive delays during data fetching.
    """
    
    url = 'http://old.tsetmc.com/tsev2/data/MarketWatchPlus.aspx'
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check if the request was successful (status code 200)
        
        if response.status_code != 200:
            print(f"Error: Received unexpected status code {response.status_code}")
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    
    main_text = response.text
    csvs = main_text.split('@')
    if len(csvs) < 3:
        print("Unexpected data format: Missing expected sections.")
        return None
    
    main_csv = csvs[2]
    csv = main_csv.split(';')
    rows = [row.split(',') for row in csv if row]
    
    # Dynamically set columns based on row length
    num_columns = len(rows[0]) if rows else 0
    if num_columns == 23:
        columns = ['webid', 'nameid', 'symbol', 'name', 'column_4', 'open', 'final', 'close', 'number', 'volume', 'value',
                   'low', 'high', 'yesterday', 'eps', 'base_volume', 'max_range', 'min_range', 'shares', 'column_19',
                   'column_20', 'column_21', 'column_22']
    elif num_columns == 25:
        columns = ['webid', 'nameid', 'symbol', 'name', 'column_4', 'open', 'final', 'close', 'number', 'volume', 'value',
                   'low', 'high', 'yesterday', 'eps', 'base_volume', 'max_range', 'min_range', 'shares', 'column_19',
                   'column_20', 'column_21', 'column_22', 'extra_column_1', 'extra_column_2']
    else:
        print(f"Unexpected number of columns: {num_columns}")
        return None

    # Create DataFrame
    df = pd.DataFrame(rows, columns=columns)
    
    # Step 1: Remove columns that are not needed
    columns_to_remove = ['max_range', 'min_range', 'shares', 'column_22']
    df = df.drop(columns=[col for col in columns_to_remove if col in df.columns])
    
    # Step 2: Rename columns as per your request
    df.rename(columns={
        'column_19': 'max_range',
        'column_20': 'min_range',
        'column_21': 'shares'
    }, inplace=True)
    
    # Convert numerical columns to integers using 'apply'
    numeric_columns = ['open', 'final', 'close', 'number', 'volume', 'value', 'low', 'high', 'yesterday', 'eps', 'base_volume', 'max_range', 'min_range', 'shares']
    
    for col in numeric_columns:
        df[col] = df[col].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
    
    # Set 'symbol' column as index
    df.set_index('symbol', inplace=True)
    
    return df


################################################################################################################################################################################
################################################################################################################################################################################


def future_for_underlying(base_symbol):
    """
    Function Description:
    future_for_underlying() retrieves futures contract symbols related to a given underlying asset.
    If the provided symbol is a base asset (e.g., 'اهرم'), the function maps it to its corresponding 
    futures contract prefix (e.g., 'جهرم'). The function then filters market data to return only the 
    related futures contracts.

    Parameters:
    - base_symbol (str): The name of the underlying asset or the prefix of the futures contracts.

    Returns:
    - A DataFrame containing only the futures contracts related to the given underlying asset.
    - If no related futures contracts are found, the function returns an empty DataFrame.

    Example Usage:
    To retrieve all futures contracts related to 'اهرم':
    future_for_underlying('اهرم')
    
    This will return a DataFrame with futures contracts that start with 'جهرم', such as:
    'جهرم0312', 'جهرم0403', etc.

    Notes:
    - The function automatically calls marketwatch() to fetch real-time market data.
    - The mapping between underlying assets and futures contract prefixes is predefined in a dictionary.
    - The function uses a regex pattern to filter contracts that follow the expected naming convention.
    """
    # فراخوانی marketwatch() از داخل tse_report


    # Retrieve market data
    df = marketwatch()

    # Mapping dictionary for underlying assets to futures contract prefixes
    future_prefixes = {
        "اهرم": "جهرم",
        "شتاب": "جتاب",
        "فولاد": "جفلا",
        "شستا": "جستا",
        "خودرو": "جخود",
        "خساپا": "جسپا"
    }

    # Determine the prefix: either mapped from base_symbol or used as-is
    prefix = future_prefixes.get(base_symbol, base_symbol)

    # Define the regex pattern (prefix followed by four digits)
    pattern = rf'^{prefix}\d{{4}}$'
    
    # Filter symbols matching the pattern
    filtered_df = df[df.index.str.match(pattern)]
    
    return filtered_df


################################################################################################################################################################################
################################################################################################################################################################################


def get_gold_funds():
    """
    Retrieves a filtered list of gold commodity funds from the market data.

    This function calls marketwatch() to obtain real-time market data and then filters 
    the results to include only commodity funds related to gold. Additionally, any fund 
    whose symbol (index) ends with the digit '2' will be excluded.

    Parameters:
    None

    Returns:
    - A DataFrame containing filtered gold commodity funds with relevant market data.
    - If no matching funds are found or data retrieval fails, an empty DataFrame is returned.

    Example Usage:
    gold_funds = get_gold_funds()
    print(gold_funds)

    Notes:
    - The function relies on the marketwatch() function from `arb_tehran_finance.tse.tse_report`.
    - Ensures that only gold-related funds are included while filtering out those whose symbol ends with '2'.
    """

    # Fetch market data
    df = marketwatch()
    
    if df is None or df.empty:
        return pd.DataFrame()  # Return empty DataFrame if no data is available

    # Step 1: Filter by name containing "طلا"
    gold_funds = df[df['name'].str.contains("طلا", na=False)]

    # Step 2: Exclude rows where symbol (index) ends with "2"
    gold_funds = gold_funds[~gold_funds.index.str.endswith("2")]

    return gold_funds




################################################################################################################################################################################
################################################################################################################################################################################





def stocks_fees(asset: str, role: str = "") -> dict or float:
    """
    Returns the cash transaction fees (buy/sell) for a given asset, specifically for gold commodity funds.
    
    Parameters:
        asset (str): The name of the asset for which the fees are requested.
        role (str, optional): The role of the user, either "خریدار" or "فروشنده".
                             If not provided or invalid, both fees will be returned as a dictionary.
    
    Returns:
        - If role is specified as "خریدار" or "فروشنده", a float representing the fee is returned.
        - Otherwise, a dictionary containing both buyer and seller fees is returned.
    
    Example Usage:
        fees = stocks_fees("مثال نماد صندوق طلا")
        print(fees)
        # Output: {'خریدار': 0.00125, 'فروشنده': 0.00125} if the symbol is a gold fund
        
        buyer_fee = stocks_fees("مثال نماد صندوق طلا", "خریدار")
        print(buyer_fee)
        # Output: 0.00125
        
        seller_fee = stocks_fees("مثال نماد صندوق طلا", "فروشنده")
        print(seller_fee)
        # Output: 0.00125
        
    Notes:
        - This function checks if the asset is among the gold funds listed by get_gold_funds().
        - It also handles Arabic characters, converting ك to ک and ي to ی.
        - If the asset is not a gold fund, None values are returned for both buyer and seller fees.
    """
    # Convert Arabic characters to Persian
    asset = asset.replace("ک", "ك").replace("ی", "ي")

    # Get list of gold funds
    gold_funds_df = get_gold_funds()
    gold_fund_symbols = gold_funds_df.index.tolist()  # List of gold fund symbols

    # Check if asset is a gold fund
    if asset in gold_fund_symbols:
        fees = {"خریدار": 0.00125, "فروشنده": 0.00125}
        # Check role and return the corresponding fee
        if role == "خریدار":
            return fees["خریدار"]
        elif role == "فروشنده":
            return fees["فروشنده"]
        else:
            return fees
    else:
        return {"خریدار": None, "فروشنده": None}




################################################################################################################################################################################
################################################################################################################################################################################



def check_date(date, key_word):
    '''
    Function Description:
    check_date() is used to validate and convert a given date to a specific format. 
    It checks if the provided date follows the proper "YYYY-MM-DD" format and converts 
    it into the standard format. If the date is in the correct format, it is converted 
    into a Jalali date format; otherwise, an error message is displayed.

    Parameters:
    date (str): The date to be validated and formatted. Expected format is "YYYY-MM-DD".
    key_word (str): A keyword used in error messages to indicate which date type 
                    (e.g., "start", "end") is invalid.

    Returns:
    - If the date is valid, it returns the date in the format "YYYY-MM-DD" (in the Jalali calendar if applicable).
    - If the date is invalid, it prints an error message indicating that the date is not in the correct format.

    Example Usage:
    To check and format the start date, use the function like this:
    check_date("1400-09-15", "start")
    
    Notes:
    - The function handles both the validation of the date format and the conversion 
      to the Jalali calendar when necessary.
    - If the date format is incorrect, the function displays an error message indicating the issue.
    '''
    try:
        if(len(date.split('-')[0])==4):
            date = jdatetime.date(year=int(date.split('-')[0]), month=int(date.split('-')[1]), day=int(date.split('-')[2]))
            date = f'{date.year:04}-{date.month:02}-{date.day:02}'
            return date
        else:
            print(f'Please enter valid {key_word} date in YYYY-MM-DD format')
    except:
        if(len(date)==10):
            print(f'Please enter valid {key_word} date')
            return
        else:
            print(f'Please enter valid {key_word} date in YYYY-MM-DD format')
            
################################################################################################################################################################################
################################################################################################################################################################################
def share_id_new(stock:str = 'خودرو'):
    '''
    Function Description:
    share_id_new() is used to retrieve detailed information about a stock or instrument 
    from the Tehran Stock Exchange (TSETMC)(new site). The function searches for a stock based on 
    its ticker or name, cleans the data, and returns key information such as the ticker, 
    name, market type, and other related details.

    Parameters:
    stock (str, default='خودرو'): The stock's ticker symbol or full name to search for.

    Returns:
    - A DataFrame containing the stock's Name, webid, NameSplit, SymbolSplit, and Market.
    - If the input is invalid, it returns False and prints an error message.

    Example Usage:
    To retrieve the stock information for "خودرو", use the following:
    share_id_new('خودرو')
    
    This will search for the stock "خودرو" and return the relevant data including the 
    market and symbol information.

    Notes:
    - The function first checks if the input is a valid ticker or name, and handles some 
      special cases (e.g., "آ س پ" is automatically converted to "آ.س.پ").
    - The market type is mapped to Persian names such as "بورس" or "فرابورس". If the 
      market type is unknown, it returns 'نامعلوم'.
    - If no valid results are found, it prints an error message and returns False.
    '''

    # basic search function: searches for and cleans the search results
    def srch_req(srch_key):
        srch_page = requests.get(f'http://cdn.tsetmc.com/api/Instrument/GetInstrumentSearch/{srch_key}', headers=headers)
        srch_res = pd.DataFrame(srch_page.json()['instrumentSearch'])
        srch_res = srch_res[['lVal18AFC','lVal30','insCode','lastDate','cgrValCot']]
        srch_res.columns = ['Ticker','Name','webid','active','Market']
        srch_res['Name'] = srch_res['Name'].apply(lambda x : characters.ar_to_fa(' '.join([i.strip() for i in x.split('\u200c')]).strip()))
        srch_res['Ticker'] = srch_res['Ticker'].apply(lambda x : characters.ar_to_fa(''.join(x.split('\u200c')).strip()))
        srch_res['NameSplit'] = srch_res['Name'].apply(lambda x : ''.join(x.split()).strip())
        srch_res['SymbolSplit'] = srch_res['Ticker'].apply(lambda x : ''.join(x.split()).strip())
        srch_res['active'] = pd.to_numeric(srch_res['active'])
        srch_res = srch_res.sort_values('Ticker')
        srch_res = pd.DataFrame(srch_res[['Name','webid','NameSplit','SymbolSplit','Market']].values, columns=['Name','webid',
                                'NameSplit','SymbolSplit','Market'], index=pd.MultiIndex.from_frame(srch_res[['Ticker','active']]))
        return srch_res
    
    # checking function inputs
    if type(stock) != str:
        print('Please Enetr a Valid Ticker or Name!')
        return False
    
    # special case that can not be found using Ticker: convert Ticker to full Name!
    if(stock=='آ س پ'):
        stock = 'آ.س.پ'
        
    # generating search keys
    stock = characters.ar_to_fa(''.join(stock.split('\u200c')).strip())
    first_name = stock.split()[0]
    stock = ''.join(stock.split())
    
    # start searching using keys, cleaning data, checking search results and handling special cases (Ticker or full Name)
    data = srch_req(first_name)
    df_symbol = data[data['SymbolSplit'] == stock]
    df_name = data[data['NameSplit'] == stock]
    
    # matching search results with search key, cleaning the data and adding market data  
    if len(df_symbol) > 0 :
        df_symbol = df_symbol.sort_index(level=1,ascending=False).drop(['NameSplit','SymbolSplit'], axis=1)
        df_symbol['Market'] = df_symbol['Market'].apply(lambda x: re.sub('[0-9]', '', x))
        df_symbol['Market'] = df_symbol['Market'].map({'N':'بورس', 'Z':'فرابورس', 'D':'فرابورس', 'A':'پایه زرد', 'P':'پایه زرد', 'C':'پایه نارنجی', 'L':'پایه قرمز',
                                                       'W':'کوچک و متوسط فرابورس', 'V':'کوچک و متوسط فرابورس',})
        df_symbol['Market'] = df_symbol['Market'].fillna('نامعلوم')
        return df_symbol
    elif len(df_name) > 0 :
        symbol = df_name.index[0][0]
        data = srch_req(symbol)
        symbol = characters.ar_to_fa(''.join(symbol.split('\u200c')).strip())
        df_symbol = data[data.index.get_level_values('Ticker') == symbol]
        if len(df_symbol) > 0 :
            df_symbol = df_symbol.sort_index(level=1, ascending=False).drop(['NameSplit','SymbolSplit'], axis=1)
            df_symbol['Market'] = df_symbol['Market'].apply(lambda x: re.sub('[0-9]', '', x))
            df_symbol['Market'] = df_symbol['Market'].map({'N':'بورس', 'Z':'فرابورس', 'D':'فرابورس', 'A':'پایه زرد', 'P':'پایه زرد', 'C':'پایه نارنجی', 'L':'پایه قرمز',
                                                           'W':'کوچک و متوسط فرابورس', 'V':'کوچک و متوسط فرابورس',})
            df_symbol['Market'] = df_symbol['Market'].fillna('نامعلوم')
            return df_symbol
    
    # invalid entry
    print('Please Enetr a Valid Ticker or Name!')
    
    return False


def share_id_old(stock:str = 'خودرو'):
    '''
    Function Description:
    share_id_new() is used to retrieve detailed information about a stock or instrument 
    from the Tehran Stock Exchange (TSETMC)(old site). The function searches for a stock based on 
    its ticker or name, cleans the data, and returns key information such as the ticker, 
    name, market type, and other related details.

    Parameters:
    stock (str, default='خودرو'): The stock's ticker symbol or full name to search for.

    Returns:
    - A DataFrame containing the stock's Name, webid, NameSplit, SymbolSplit, and Market.
    - If the input is invalid, it returns False and prints an error message.

    Example Usage:
    To retrieve the stock information for "خودرو", use the following:
    share_id_new('خودرو')
    
    This will search for the stock "خودرو" and return the relevant data including the 
    market and symbol information.

    Notes:
    - The function first checks if the input is a valid ticker or name, and handles some 
      special cases (e.g., "آ س پ" is automatically converted to "آ.س.پ").
    - The market type is mapped to Persian names such as "بورس" or "فرابورس". If the 
      market type is unknown, it returns 'نامعلوم'.
    - If no valid results are found, it prints an error message and returns False.
    '''

    # search TSE function ------------------------------------------------------------------------------------------------------------
    def request(Name):
        page = requests.get(f'http://old.tsetmc.com/tsev2/data/search.aspx?skey={Name}', headers=headers)
        data = []
        for i in page.text.split(';') :
            try :
                i = i.split(',')
                data.append([i[0],i[1],i[2],i[7],i[-1]])
            except :
                pass
        data = pd.DataFrame(data, columns=['Ticker','Name','webid','active','Market'])
        data['Name'] = data['Name'].apply(lambda x : characters.ar_to_fa(' '.join([i.strip() for i in x.split('\u200c')]).strip()))
        data['Ticker'] = data['Ticker'].apply(lambda x : characters.ar_to_fa(''.join(x.split('\u200c')).strip()))
        data['Name-Split'] = data['Name'].apply(lambda x : ''.join(x.split()).strip())
        data['Symbol-Split'] = data['Ticker'].apply(lambda x : ''.join(x.split()).strip())
        data['active'] = pd.to_numeric(data['active'])
        data = data.sort_values('Ticker')
        data = pd.DataFrame(data[['Name','webid','Name-Split','Symbol-Split','Market']].values, columns=['Name','webid',
                            'Name-Split','Symbol-Split','Market'], index=pd.MultiIndex.from_frame(data[['Ticker','active']]))
        return data
    #---------------------------------------------------------------------------------------------------------------------------------
    if type(stock) != str:
        print('Please Enetr a Valid Ticker or Name!')
        return False
    if(stock=='آ س پ'):
        stock = 'آ.س.پ'
    # cleaning input search key
    stock = characters.ar_to_fa(''.join(stock.split('\u200c')).strip())
    first_name = stock.split()[0]
    if(stock=='فن آوا'):
        first_name = stock
    stock = ''.join(stock.split())
    # search TSE and process:
    data = request(first_name)
    df_symbol = data[data['Symbol-Split'] == stock]
    df_name = data[data['Name-Split'] == stock]
    if len(df_symbol) > 0 :
        df_symbol = df_symbol.sort_index(level=1,ascending=False).drop(['Name-Split','Symbol-Split'], axis=1)
        df_symbol['Market'] = df_symbol['Market'].apply(lambda x: re.sub('[0-9]', '', x))
        df_symbol['Market'] = df_symbol['Market'].map({'N':'بورس', 'Z':'فرابورس', 'D':'فرابورس', 'A':'پایه زرد', 'P':'پایه زرد', 'C':'پایه نارنجی', 'L':'پایه قرمز',
                                                       'W':'کوچک و متوسط فرابورس', 'V':'کوچک و متوسط فرابورس',})
        df_symbol['Market'] = df_symbol['Market'].fillna('نامعلوم')
        return df_symbol
    elif len(df_name) > 0 :
        symbol = df_name.index[0][0]
        data = request(symbol)
        symbol = characters.ar_to_fa(''.join(symbol.split('\u200c')).strip())
        df_symbol = data[data.index.get_level_values('Ticker') == symbol]
        if len(df_symbol) > 0 :
            df_symbol = df_symbol.sort_index(level=1,ascending=False).drop(['Name-Split','Symbol-Split'], axis=1)
            df_symbol['Market'] = df_symbol['Market'].apply(lambda x: re.sub('[0-9]', '', x))
            df_symbol['Market'] = df_symbol['Market'].map({'N':'بورس', 'Z':'فرابورس', 'D':'فرابورس', 'A':'پایه زرد', 'P':'پایه زرد', 'C':'پایه نارنجی', 'L':'پایه قرمز',
                                                           'W':'کوچک و متوسط فرابورس', 'V':'کوچک و متوسط فرابورس',})
            df_symbol['Market'] = df_symbol['Market'].fillna('نامعلوم')
            return df_symbol
    print('Please Enetr a Valid Ticker or Name!')
    return False
################################################################################################################################################################################
################################################################################################################################################################################

def group_id(group_name : str = "خودرو"):
    '''
    Function Description:
    group_id() is used to retrieve the web ID of a specific sector or group from the Tehran Stock Exchange (TSETMC). 
    The function searches for the sector using a predefined lookup table and returns the corresponding Web-ID. 
    If the sector name is not found, it performs a Google search to extract the Web-ID associated with the group.

    Parameters:
    group_name (str, default="خودرو"): The name of the sector or group to search for. 

    Returns:
    - The Web-ID corresponding to the sector group.
    - If the sector is not found, it prints an error message and returns nothing.

    Example Usage:
    To retrieve the Web-ID for the "خودرو" sector, use the following:
    group_id("خودرو")

    This will search for the "خودرو" sector and return its Web-ID. 

    Notes:
    - The function first tries to find the Web-ID using a predefined lookup table of sectors and their corresponding Web-IDs.
    - If the sector name is not found, the function will attempt to retrieve the Web-ID through a Google search.
    - If an invalid sector name is provided, the function will print an error message and stop.

    '''

    sector_list = ['زراعت','ذغال سنگ','کانی فلزی','سایر معادن','منسوجات','محصولات چرمی','محصولات چوبی','محصولات کاغذی','انتشار و چاپ','فرآورده های نفتی','لاستیک',\
                   'فلزات اساسی','محصولات فلزی','ماشین آلات','دستگاه های برقی','وسایل ارتباطی','خودرو','قند و شکر','چند رشته ای','تامین آب، برق و گاز','غذایی',\
                   'دارویی','شیمیایی','خرده فروشی','کاشی و سرامیک','سیمان','کانی غیر فلزی','سرمایه گذاری','بانک','سایر مالی','حمل و نقل',\
                   'رادیویی','مالی','اداره بازارهای مالی','انبوه سازی','رایانه','اطلاعات و ارتباطات','فنی مهندسی','استخراج نفت','بیمه و بازنشستگی']
    sector_web_id = [34408080767216529,19219679288446732,13235969998952202,62691002126902464,59288237226302898,69306841376553334,58440550086834602,30106839080444358,25766336681098389,\
     12331083953323969,36469751685735891,32453344048876642,1123534346391630,11451389074113298,33878047680249697,24733701189547084,20213770409093165,21948907150049163,40355846462826897,\
     54843635503648458,15508900928481581,3615666621538524,33626672012415176,65986638607018835,57616105980228781,70077233737515808,14651627750314021,34295935482222451,72002976013856737,\
     25163959460949732,24187097921483699,41867092385281437,61247168213690670,61985386521682984,4654922806626448,8900726085939949,18780171241610744,47233872677452574,65675836323214668,\
     59105676994811497]
    df_index_lookup = pd.DataFrame({'Sector':sector_list,'Web-ID':sector_web_id}).set_index('Sector')

    """index_list_url = 'http://tsetmc.com/Loader.aspx?Partree=151315&Flow=1'
    index_list_page = requests.get(index_list_url)
    soup = BeautifulSoup(index_list_page.content, 'html.parser')
    list_of_index = (soup.find_all('tbody')[0]).find_all('a')
    index_title = []
    index_webid = []
    for i in range(len(list_of_index)):
        index_title.append(list_of_index[i].text)
        index_webid.append(list_of_index[i].get('href').split('=')[-1])
    df_index_lookup = pd.DataFrame({'Sector':index_title,'Web-ID':index_webid}) 
    # Filter the lookup table to keep just industries
    df_index_lookup = df_index_lookup.iloc[:44]
    df_index_lookup.drop([16,18,19,26], axis=0, inplace=True)
    df_index_lookup['Sector'] = df_index_lookup['Sector'].apply(lambda x: (''.join([i for i in x if not i.isdigit()]).replace('-','')))
    df_index_lookup['Sector'] = df_index_lookup['Sector'].apply(lambda x: (((str(x).replace('ي','ی')).replace('ك','ک')).replace(' ص','')).strip())
    df_index_lookup = df_index_lookup.set_index('Sector')
    df_index_lookup['Web-ID'] = df_index_lookup['Web-ID'].apply(lambda x: int(x))"""
    # try search keyy with available look-up table and find web-id:
    try:
        sector_web_id = df_index_lookup.loc[group_name]['Web-ID']
    except:
        group_name = characters.fa_to_ar(group_name)
        page = requests.get(f'https://www.google.com/search?q={group_name} tsetmc اطلاعات شاخص', headers=headers)
        code = page.text.split('http://www.tsetmc.com/Loader.aspx%3FParTree%3D15131J%26i%3D')[1]
        code = code.split('&')[0]
        # check google acquired code with reference table
        if(len(df_index_lookup[df_index_lookup['Web-ID'] == int(code)]) == 1):
            sector_web_id = int(code)
        else:
            print('Invalid sector Name! Please try again with correct sector Name!')
            return
    return sector_web_id   

################################################################################################################################################################################
################################################################################################################################################################################
def stock_values(stock:str = 'خودرو', start_date:str = '1403-11-01', end_date:str = '1403-11-01', ignore_date:bool = False, adjust_price:bool = False, show_weekday:bool = False, double_date:bool = False):
    '''
    Function Description:
    stock_values() is used to retrieve historical stock trading data for a given stock from the Tehran Stock Exchange (TSETMC) based on user input. 
    The function allows customization of the output, such as adjusting prices, showing weekdays, and displaying the data in different formats. 
    It returns information like Open, High, Low, Close, Final, Volume, Value, No, Ticker, Name, and Market for the specified time range.

    Parameters:
    stock (str, default="خودرو"): The stock or sector name to fetch data for.
    start_date (str, default="1403-11-01"): The start date for the data in Jalali (Persian) format (YYYY-MM-DD).
    end_date (str, default="1403-11-01"): The end date for the data in Jalali (Persian) format (YYYY-MM-DD).
    ignore_date (bool, default=False): Whether to ignore the date range and get all available data.
    adjust_price (bool, default=False): Whether to adjust the price data based on the Y-Final value for normalization.
    show_weekday (bool, default=False): Whether to include the weekday information in the output.
    double_date (bool, default=False): Whether to include both Gregorian and Jalali dates in the output.

    Returns:
    A DataFrame with columns: Open, High, Low, Close, Final, Volume, Value, No, Ticker, Name, Market.
    The DataFrame is indexed by the Jalali date (J-Date).

    Example Usage:
    To get stock data for "خودرو" (Iran Khodro) between "1403-11-01" and "1403-11-01", use:
    stock_values("خودرو", start_date="1403-11-01", end_date="1403-11-01")

    This will return the stock data for "خودرو" on the specified date.

    Notes:
    - The function fetches the stock data from the TSETMC API, processes the data, and returns it in a structured format.
    - The function performs data cleaning and adjusts prices based on user preference.
    - If the `adjust_price` parameter is True, the prices will be adjusted using the Y-Final value for normalization.
    - The function provides an option to include weekdays and display both Gregorian and Jalali dates.

    '''

    # basic request and data cleaning function for historical price data of a Ticker for a given market 
    def get_price_data(ticker_id, Ticker, Name, market):
        r = requests.get(f'http://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceDailyList/{ticker_id}/0', headers=headers)
        df_history = pd.DataFrame(r.json()['closingPriceDaily'])
        columns=['Date','High','Low','Final','Close','Open','Y-Final','Value','Volume','No']
        df_history = df_history[['dEven','priceMax','priceMin','pClosing','pDrCotVal','priceFirst','priceYesterday','qTotCap','qTotTran5J','zTotTran']]
        df_history.columns = ['Date','High','Low','Final','Close','Open','Y-Final','Value','Volume','No']
        df_history['Date'] = df_history['Date'].apply(lambda x: str(x))
        df_history['Date'] = df_history['Date'].apply(lambda x: f'{x[:4]}-{x[4:6]}-{x[-2:]}')
        df_history['Date']=pd.to_datetime(df_history['Date'])
        df_history = df_history[df_history['No']!=0]
        df_history['Ticker'] = Ticker
        df_history['Name'] = Name
        df_history['Market'] = market
        df_history = df_history.set_index('Date')
        return df_history
    
    # check to see if the entry start and end dates are valid or not
    if(not ignore_date):
        start_date = check_date(start_date,key_word="'START'")
        if(start_date==None):
            return
        end_date = check_date(end_date,key_word="'END'")
        if(end_date==None):
            return
        start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
        end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
        if(start>end):
            print('Start date must be a day before end date!')
            return
    
    # search for WebIDs
    ticker_no_df = share_id_new(stock)
    if(type(ticker_no_df)==bool):
        return
    
    # create an empty dataframe:
    df_history = pd.DataFrame({},columns=['Date','High','Low','Final','Close','Open','Y-Final','Value','Volume','No','Ticker','Name','Market']).set_index('Date')
    
    # loop to get data from different pages of a Ticker:
    for index, row in (ticker_no_df.reset_index()).iterrows():
        try:
            df_temp = get_price_data(ticker_id = row['webid'],Ticker = row['Ticker'],Name = row['Name'],market = row['Market'])
            df_history = pd.concat([df_history,df_temp])
        except:
            pass
        
    # sort based on dated index:
    df_history = df_history.sort_index(ascending=True)
    df_history = df_history.reset_index()
    
    # add weekdays and j-date columns:
    df_history['Weekday']=df_history['Date'].dt.weekday
    df_history['Weekday'] = df_history['Weekday'].apply(lambda x: calendar.day_name[x])
    df_history['J-Date']=df_history['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
    df_history = df_history.set_index('J-Date')
    
    # rearrange columns and convert some columns to numeric
    df_history=df_history[['Date','Weekday','Y-Final','Open','High','Low','Close','Final','Volume','Value','No','Ticker','Name','Market']]
    cols = ['Y-Final','Open','High','Low','Close','Final','Volume','No','Value']
    df_history[cols] = df_history[cols].apply(pd.to_numeric, axis=1)
    

    # find stock moves between markets and adjust for nominal price in the new market, if necessary
    df_history['Final(+1)'] = df_history['Final'].shift(+1)          
    df_history['Market(+1)'] = df_history['Market'].shift(+1)        
    df_history['temp'] = df_history.apply(lambda x: x['Y-Final'] if((x['Y-Final']!=0)and(x['Y-Final']!=1000)) 
                                          else (x['Y-Final'] if((x['Market(+1)']==x['Market'])or(pd.isnull(x['Final(+1)']))) 
                                          else x['Final(+1)']),axis = 1)
    df_history['Y-Final'] = df_history['temp']
    df_history.drop(columns=['Final(+1)','temp','Market(+1)'],inplace=True)
    
    # convert numbers to int because we do not have less than Rial, just for clean outputs!
    for col in cols:
        df_history[col] = df_history[col].apply(lambda x: int(x))

    # Adjust price data, if requested:
    if(adjust_price):
        df_history['COEF'] = (df_history['Y-Final'].shift(-1)/df_history['Final']).fillna(1.0)
        df_history['ADJ-COEF']=df_history.iloc[::-1]['COEF'].cumprod().iloc[::-1]
        df_history['Adj Open'] = (df_history['Open']*df_history['ADJ-COEF']).apply(lambda x: int(x))
        df_history['Adj High'] = (df_history['High']*df_history['ADJ-COEF']).apply(lambda x: int(x))
        df_history['Adj Low'] = (df_history['Low']*df_history['ADJ-COEF']).apply(lambda x: int(x))
        df_history['Adj Close'] = (df_history['Close']*df_history['ADJ-COEF']).apply(lambda x: int(x))
        df_history['Adj Final'] = (df_history['Final']*df_history['ADJ-COEF']).apply(lambda x: int(x))
        df_history.drop(columns=['COEF','ADJ-COEF'],inplace=True)
    
    # drop weekdays if not requested
    if(not show_weekday):
        df_history.drop(columns=['Weekday'],inplace=True)
    
    # drop Gregorian date if not requested
    if(not double_date):
        df_history.drop(columns=['Date'],inplace=True)
    
    # drop yesterday's final price!
    df_history.drop(columns=['Y-Final'],inplace=True)
    
    # slice requested time window, if requested:
    if(not ignore_date):
        df_history = df_history[start_date:end_date]
        
    return df_history


def stock_value(stock:str = 'خودرو', start_date:str = '1403-11-01', end_date:str ='1403-11-03', ignore_date:bool = False, adjust_price:bool = False, show_weekday:bool = False, double_date:bool = False):
    ''' 
    Function Description:
    stock_value() retrieves and processes historical stock price data from the Tehran Stock Exchange (TSETMC). 
    The function allows the user to filter data by date range, adjust prices for stock splits, and display detailed market information.
    
    Parameters:
    stock (str, default='خودرو'): The stock's ticker or name to search for.
    start_date (str, default='1403-11-01'): The start date of the data range in the format 'YYYY-MM-DD' (Jalali date).
    end_date (str, default='1403-11-03'): The end date of the data range in the format 'YYYY-MM-DD' (Jalali date).
    ignore_date (bool, default=False): If True, the date range check is ignored.
    adjust_price (bool, default=False): If True, adjusts the stock prices based on stock splits.
    show_weekday (bool, default=False): If True, includes the weekday names in the data.
    double_date (bool, default=False): If True, includes both the Gregorian and Jalali dates.

    Returns:
    - A DataFrame containing stock price data including Open, High, Low, Close, Final, Volume, Value, etc.
    - The data is indexed by Jalali date and can be filtered by the given date range.
    
    Example Usage:
    To retrieve stock prices for "خودرو" from 1403-11-01 to 1403-11-03:
    stock_value('خودرو', '1403-11-01', '1403-11-03')
    
    Notes:
    - If the `adjust_price` flag is True, the stock prices will be adjusted for stock splits using historical price data.
    - The function retrieves data for the stock from multiple pages and processes it into a consolidated DataFrame.
    - If no data is found for the given stock, an empty DataFrame is returned.
    '''

    # a function to get price data from a given page ----------------------------------------------------------------------------------
    def get_price_data(ticker_id,Ticker,Name, data_part):
        r = requests.get(f'http://old.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i={ticker_id}&Top=999999&A=0', headers=headers)
        df_history=pd.DataFrame(r.text.split(';'))
        columns=['Date','High','Low','Final','Close','Open','Y-Final','Value','Volume','No']
        #split data into defined columns
        df_history[columns] = df_history[0].str.split("@",expand=True)
        # drop old column 0
        df_history.drop(columns=[0],inplace=True)
        df_history.dropna(inplace=True)
        df_history['Date']=pd.to_datetime(df_history['Date'])
        df_history['Ticker'] = Ticker
        df_history['Name'] = Name
        df_history['Market'] = data_part
        df_history = df_history.set_index('Date')
        return df_history
    # ----------------------------------------------------------------------------------------------------------------------------------
    # check date validity
    if(not ignore_date):
        start_date = check_date(start_date,key_word="'START'")
        if(start_date==None):
            return
        end_date = check_date(end_date,key_word="'END'")
        if(end_date==None):
            return
        start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
        end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
        if(start>end):
            print('Start date must be a day before end date!')
            return
    #---------------------------------------------------------------------------------------------------------------------------------------
    # find web-ids 
    ticker_no_df = share_id_old(stock)
    if(type(ticker_no_df)==bool):
        return
    # create an empty dataframe:
    df_history = pd.DataFrame({},columns=['Date','High','Low','Final','Close','Open','Y-Final','Value','Volume','No','Ticker','Name','Market']).set_index('Date')
    # loop to get data from different pages of a Ticker:
    for index, row in (ticker_no_df.reset_index()).iterrows():
        try:
            df_temp = get_price_data(ticker_id = row['webid'],Ticker = row['Ticker'],Name = row['Name'],data_part = row['Market'])
            df_history = pd.concat([df_history,df_temp])
        except:
            pass
    # sort index and reverse the order for more processes:
    df_history = df_history.sort_index(ascending=True)
    df_history = df_history.reset_index()
    # determining week days:
    df_history['Weekday']=df_history['Date'].dt.weekday
    df_history['Weekday'] = df_history['Weekday'].apply(lambda x: calendar.day_name[x])
    df_history['J-Date']=df_history['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
    df_history = df_history.set_index('J-Date')
    # rearrange columns:
    df_history=df_history[['Date','Weekday','Y-Final','Open','High','Low','Close','Final','Volume','Value','No','Ticker','Name','Market']]
    cols = ['Y-Final','Open','High','Low','Close','Final','Volume','No','Value']
    df_history[cols] = df_history[cols].apply(pd.to_numeric, axis=1)
    #----------------------------------------------------------------------------------------------------------------------
    # Y-Final for new part of data could be 0 or 1000, we need to replace them with yesterday's final price:
    df_history['Final(+1)'] = df_history['Final'].shift(+1)          # final prices shifted forward by one day
    df_history['Market(+1)'] = df_history['Market'].shift(+1)        # market shifted forward by one day
    df_history['temp'] = df_history.apply(lambda x: x['Y-Final'] if((x['Y-Final']!=0)and(x['Y-Final']!=1000)) 
                                          else (x['Y-Final'] if((x['Market(+1)']==x['Market'])or(pd.isnull(x['Final(+1)']))) 
                                          else x['Final(+1)']),axis = 1)
    df_history['Y-Final'] = df_history['temp']
    df_history.drop(columns=['Final(+1)','temp','Market(+1)'],inplace=True)
    #-----------------------------------------------------------------------------------------------------------------------
    for col in cols:
        df_history[col] = df_history[col].apply(lambda x: int(x)) # convert to int because we do not have less than Rial
    #--------------------------------------------------------------------------------------------------------------------
    # Adjust price data:
    if(adjust_price):
        df_history['COEF'] = (df_history['Y-Final'].shift(-1)/df_history['Final']).fillna(1.0)
        df_history['ADJ-COEF']=df_history.iloc[::-1]['COEF'].cumprod().iloc[::-1]
        df_history['Adj Open'] = (df_history['Open']*df_history['ADJ-COEF']).apply(lambda x: int(x))
        df_history['Adj High'] = (df_history['High']*df_history['ADJ-COEF']).apply(lambda x: int(x))
        df_history['Adj Low'] = (df_history['Low']*df_history['ADJ-COEF']).apply(lambda x: int(x))
        df_history['Adj Close'] = (df_history['Close']*df_history['ADJ-COEF']).apply(lambda x: int(x))
        df_history['Adj Final'] = (df_history['Final']*df_history['ADJ-COEF']).apply(lambda x: int(x))
        df_history.drop(columns=['COEF','ADJ-COEF'],inplace=True)
    if(not show_weekday):
        df_history.drop(columns=['Weekday'],inplace=True)
    if(not double_date):
        df_history.drop(columns=['Date'],inplace=True)
    df_history.drop(columns=['Y-Final'],inplace=True)
    # slice requested time window:
    if(not ignore_date):
        df_history = df_history[start_date:end_date]
    return df_history


################################################################################################################################################################################
################################################################################################################################################################################
def ri_informations(stock:str = 'خودرو', start_date:str = '1403-11-01', end_date:str = '1403-11-01', ignore_date:bool = False, show_weekday:bool = False, double_date:bool = False):
    ''' 
    Function Description:
    ri_informations() retrieves and processes historical retail vs institutional trading data for a given stock on the Tehran Stock Exchange (TSETMC). 
    The function enables users to filter the data by date range, display weekly information, and include or exclude certain columns like weekdays and Gregorian dates.
    
    Parameters:
    stock (str, default='خودرو'): The stock's ticker or name to search for.
    start_date (str, default='1403-11-01'): The start date of the data range in the format 'YYYY-MM-DD' (Jalali date).
    end_date (str, default='1403-11-01'): The end date of the data range in the format 'YYYY-MM-DD' (Jalali date).
    ignore_date (bool, default=False): If True, the date range check is ignored.
    show_weekday (bool, default=False): If True, includes the weekday names in the data.
    double_date (bool, default=False): If True, includes both the Gregorian and Jalali dates.

    Returns:
    - A DataFrame containing retail-institutional trading data including volume and value for both retail and institutional buyers and sellers.
    - The data is indexed by Jalali date and can be filtered by the given date range.
    
    Example Usage:
    To retrieve retail-institutional data for "خودرو" from 1403-11-01 to 1403-11-01:
    ri_informations('خودرو', '1403-11-01', '1403-11-01')
    
    Notes:
    - The data includes several trading metrics like the number of shares bought or sold by retail and institutional traders, the volume of trades, and the value of the trades.
    - If the `show_weekday` flag is True, the weekday names will be included in the data.
    - If `double_date` is True, both Gregorian and Jalali dates will be included.
    - If no data is found for the given stock, an empty DataFrame is returned.
    '''
    
    # basic request and data cleaning function for historical retail-institutional data of a Ticker for a given market:
    def get_ri_data(ticker_id, Ticker, Name, market):
        r = requests.get(f'http://cdn.tsetmc.com/api/ClientType/GetClientTypeHistory/{ticker_id}',headers=headers)
        df_RI_tab = pd.DataFrame(r.json()['clientType'])
        cols = ['Date','webid','Vol_Buy_R','Vol_Buy_I','Val_Buy_R','Val_Buy_I','No_Buy_I','Vol_Sell_R','No_Buy_R','Vol_Sell_I','Val_Sell_R','Val_Sell_I','No_Sell_I','No_Sell_R']
        df_RI_tab.columns = cols
        df_RI_tab = df_RI_tab[['Date','No_Buy_R','No_Buy_I','No_Sell_R','No_Sell_I','Vol_Buy_R','Vol_Buy_I','Vol_Sell_R','Vol_Sell_I','Val_Buy_R','Val_Buy_I','Val_Sell_R','Val_Sell_I']]
        df_RI_tab['Date'] = df_RI_tab['Date'].apply(lambda x: str(x))
        cols = ['No_Buy_R','No_Buy_I','No_Sell_R','No_Sell_I','Vol_Buy_R','Vol_Buy_I','Vol_Sell_R','Vol_Sell_I','Val_Buy_R','Val_Buy_I','Val_Sell_R','Val_Sell_I']
        df_RI_tab[cols] = df_RI_tab[cols].astype('int64')
        df_RI_tab['Date']=pd.to_datetime(df_RI_tab['Date'])
        df_RI_tab['Ticker'] = Ticker
        df_RI_tab['Name'] = Name
        df_RI_tab['Market'] = market
        df_RI_tab = df_RI_tab.set_index('Date')
        return df_RI_tab
    
    # check to see if the entry start and end dates are valid or not:
    if(not ignore_date):
        start_date = check_date(start_date,key_word="'START'")
        if(start_date==None):
            return
        end_date = check_date(end_date,key_word="'END'")
        if(end_date==None):
            return
        start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
        end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
        if(start>end):
            print('Start date must be a day before end date!')
            return

    # search for WebIDs:
    ticker_no_df = share_id_new(stock)
    if(type(ticker_no_df)==bool):
        return
    
    # create an empty dataframe:   
    df_RI_tab = pd.DataFrame({},columns=['Date','No_Buy_R','No_Buy_I','No_Sell_R','No_Sell_I','Vol_Buy_R','Vol_Buy_I','Vol_Sell_R',
                                         'Vol_Sell_I','Val_Buy_R','Val_Buy_I','Val_Sell_R','Val_Sell_I','Ticker','Name','Market']).set_index('Date')
   
    # loop to get data from different pages of a Ticker:
    for index, row in (ticker_no_df.reset_index()).iterrows():
        try:
            df_temp = get_ri_data(ticker_id = row['webid'], Ticker = row['Ticker'], Name = row['Name'], market = row['Market'])
            df_RI_tab = pd.concat([df_RI_tab,df_temp])
        except:
            pass
        
    # sort date index 
    df_RI_tab = df_RI_tab.sort_index(ascending=True)
    df_RI_tab = df_RI_tab.reset_index()
    
    # add weekdays and Jalali date:
    df_RI_tab['Weekday']=df_RI_tab['Date'].dt.weekday
    df_RI_tab['Weekday'] = df_RI_tab['Weekday'].apply(lambda x: calendar.day_name[x])
    df_RI_tab['J-Date']=df_RI_tab['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
    df_RI_tab.set_index(df_RI_tab['J-Date'],inplace = True)
    df_RI_tab = df_RI_tab.set_index('J-Date')
    
    # rearrange columns and convert some columns to numeric:
    df_RI_tab=df_RI_tab[['Date','Weekday','No_Buy_R','No_Buy_I','No_Sell_R','No_Sell_I','Vol_Buy_R','Vol_Buy_I','Vol_Sell_R','Vol_Sell_I',
                         'Val_Buy_R','Val_Buy_I','Val_Sell_R','Val_Sell_I','Ticker','Name','Market']]
    cols = ['No_Buy_R','No_Buy_I','No_Sell_R','No_Sell_I','Vol_Buy_R','Vol_Buy_I','Vol_Sell_R','Vol_Sell_I','Val_Buy_R','Val_Buy_I','Val_Sell_R','Val_Sell_I']
    df_RI_tab[cols] = df_RI_tab[cols].apply(pd.to_numeric, axis=1)
    
    # drop weekdays if not requested:
    if(not show_weekday):
        df_RI_tab.drop(columns=['Weekday'],inplace=True)
        
    # drop Gregorian date if not requested:
    if(not double_date):
        df_RI_tab.drop(columns=['Date'],inplace=True)
        
    # # slice requested time window, if requested:
    if(not ignore_date):
        df_RI_tab = df_RI_tab[start_date:end_date]
        
    return df_RI_tab


'''def ri_information(stock:str = 'خودرو', start_date:str = '1403-11-01', end_date:str ='1403-11-03', ignore_date:bool = False, show_weekday:bool = False, double_date:bool = False, alt:bool = False):
    
    # a function to get ri data from a given page ----------------------------------------------------------------------------------
    def get_ri_data(ticker_id, Ticker, Name, data_part):
        if(alt):
            r = requests.get(f'http://cdn.tsetmc.com/api/ClientType/GetClientTypeHistory/{ticker_id}', headers=headers)
            df_RI_tab = pd.DataFrame(r.json()['clientType'])
            cols = ['Date', 'webid', 'Vol_Buy_R', 'Vol_Buy_I', 'Val_Buy_R', 'Val_Buy_I', 'No_Buy_I', 'Vol_Sell_R', 'No_Buy_R', 'Vol_Sell_I', 'Val_Sell_R', 'Val_Sell_I', 'No_Sell_I', 'No_Sell_R']
            df_RI_tab.columns = cols
            df_RI_tab = df_RI_tab[['Date', 'No_Buy_R', 'No_Buy_I', 'No_Sell_R', 'No_Sell_I', 'Vol_Buy_R', 'Vol_Buy_I', 'Vol_Sell_R', 'Vol_Sell_I', 'Val_Buy_R', 'Val_Buy_I', 'Val_Sell_R', 'Val_Sell_I']]
            df_RI_tab['Date'] = df_RI_tab['Date'].apply(lambda x: str(x))
            cols = ['No_Buy_R', 'No_Buy_I', 'No_Sell_R', 'No_Sell_I', 'Vol_Buy_R', 'Vol_Buy_I', 'Vol_Sell_R', 'Vol_Sell_I', 'Val_Buy_R', 'Val_Buy_I', 'Val_Sell_R', 'Val_Sell_I']
            df_RI_tab[cols] = df_RI_tab[cols].astype('int64')
        else:
            r = requests.get(f'http://www.tsetmc.com/tsev2/data/clienttype.aspx?i={ticker_id}', headers=headers)
            df_RI_tab = pd.DataFrame(r.text.split(';'))
            columns = ['Date', 'No_Buy_R', 'No_Buy_I', 'No_Sell_R', 'No_Sell_I', 'Vol_Buy_R', 'Vol_Buy_I', 'Vol_Sell_R', 'Vol_Sell_I', 'Val_Buy_R', 'Val_Buy_I', 'Val_Sell_R', 'Val_Sell_I']
            df_RI_tab[columns] = df_RI_tab[0].str.split(",", expand=True)
            df_RI_tab.drop(columns=[0], inplace=True)

        # تبدیل تاریخ به datetime و چاپ نوع داده و چند مقدار از تاریخ‌ها برای بررسی
        df_RI_tab['Date'] = pd.to_datetime(df_RI_tab['Date'], errors='coerce', format='%Y-%m-%d')  # افزودن فرمت تاریخ به تابع
        print("Converted Dates:")
        print(df_RI_tab['Date'].head())  # چاپ چند مقدار از تاریخ‌ها برای بررسی
        print(f"Data type of 'Date' column: {df_RI_tab['Date'].dtype}")  # چاپ نوع داده

        # حذف ردیف‌هایی که تاریخ آنها به درستی تبدیل نشده است
        df_RI_tab = df_RI_tab.dropna(subset=['Date'])

        # بررسی اینکه آیا همه تاریخ‌ها به datetime تبدیل شده‌اند
        if df_RI_tab['Date'].dtype != 'datetime64[ns]':
            print("Error: Date column is not of datetime type!")
            return None  # یا هر روش دیگری برای مدیریت خطا

        # اضافه کردن ستون‌های مورد نظر
        df_RI_tab['Ticker'] = Ticker
        df_RI_tab['Name'] = Name
        df_RI_tab['Market'] = data_part
        df_RI_tab = df_RI_tab.set_index('Date')
        
        # اگر show_weekday برابر True باشد، روز هفته را اضافه می‌کنیم
        if show_weekday:
            df_RI_tab['Weekday'] = df_RI_tab.index.weekday  # استفاده از index برای استخراج روز هفته
            df_RI_tab['Weekday_Name'] = df_RI_tab.index.day_name()  # استخراج نام روز هفته (مثل دوشنبه، سه‌شنبه و...)
        
        return df_RI_tab




    # check date validity --------------------------------------------------------------------------------------------------------------
    if(not ignore_date):
        start_date = check_date(start_date,key_word="'START'")
        if(start_date==None):
            return
        end_date = check_date(end_date,key_word="'END'")
        if(end_date==None):
            return
        start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
        end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
        if(start>end):
            print('Start date must be a day before end date!')
            return
    #---------------------------------------------------------------------------------------------------------------------------------------
    # find web-ids 
    ticker_no_df = share_id_old(stock)
    if(type(ticker_no_df)==bool):
        return
    # create an empty dataframe:   
    df_RI_tab = pd.DataFrame({},columns=['Date','No_Buy_R','No_Buy_I','No_Sell_R','No_Sell_I','Vol_Buy_R','Vol_Buy_I','Vol_Sell_R',
                                         'Vol_Sell_I','Val_Buy_R','Val_Buy_I','Val_Sell_R','Val_Sell_I','Ticker','Name','Market']).set_index('Date')
    # loop to get data from different pages of a Ticker:
    for index, row in (ticker_no_df.reset_index()).iterrows():
        try:
            df_temp = get_ri_data(ticker_id = row['webid'],Ticker = row['Ticker'],Name = row['Name'],data_part = row['Market'])
            df_RI_tab = pd.concat([df_RI_tab,df_temp])
        except:
            pass
    # sort index and reverse the order for more processes:
    df_RI_tab = df_RI_tab.sort_index(ascending=True)
    df_RI_tab = df_RI_tab.reset_index()
    # determining week days:
    df_RI_tab['Weekday']=df_RI_tab['Date'].dt.weekday
    df_RI_tab['Weekday'] = df_RI_tab['Weekday'].apply(lambda x: calendar.day_name[x])
    df_RI_tab['J-Date']=df_RI_tab['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
    df_RI_tab.set_index(df_RI_tab['J-Date'],inplace = True)
    df_RI_tab = df_RI_tab.set_index('J-Date')
    # rearrange columns:
    df_RI_tab=df_RI_tab[['Date','Weekday','No_Buy_R','No_Buy_I','No_Sell_R','No_Sell_I','Vol_Buy_R','Vol_Buy_I','Vol_Sell_R','Vol_Sell_I',
                         'Val_Buy_R','Val_Buy_I','Val_Sell_R','Val_Sell_I','Ticker','Name','Market']]
    cols = ['No_Buy_R','No_Buy_I','No_Sell_R','No_Sell_I','Vol_Buy_R','Vol_Buy_I','Vol_Sell_R','Vol_Sell_I','Val_Buy_R','Val_Buy_I','Val_Sell_R','Val_Sell_I']
    df_RI_tab[cols] = df_RI_tab[cols].apply(pd.to_numeric, axis=1)
    if(not show_weekday):
        df_RI_tab.drop(columns=['Weekday'],inplace=True)
    if(not double_date):
        df_RI_tab.drop(columns=['Date'],inplace=True)
    # slice requested time window:
    if(not ignore_date):
        df_RI_tab = df_RI_tab[start_date:end_date]
    return df_RI_tab'''

################################################################################################################################################################################
################################################################################################################################################################################

def index_tedpix(start_date:str = '1403-11-01', end_date:str ='1403-11-03', ignore_date:bool = False, just_adj_close:bool = False, show_weekday:bool = False, double_date:bool = False):
    """
    Function Description:
    index_tedpix() retrieves the Tehran Stock Exchange (TEDPIX) index data for a specified date range.
    The function outputs trading metrics including Open, High, Low, Close, Adjusted Close, and Volume.
    It allows users to choose whether to display the weekday names and whether to keep the date column in the output.

    Parameters:
    start_date (str, default = '1403-11-01'): The start date of the data range in the format 'YYYY-MM-DD' (Jalali date).
    end_date (str, default = '1403-11-03'): The end date of the data range in the format 'YYYY-MM-DD' (Jalali date).
    ignore_date (bool, default = False): If True, the date range check is ignored.
    just_adj_close (bool, default = False): If True, only the Adjusted Close data is returned.
    show_weekday (bool, default = False): If True, includes the weekday names in the data.
    double_date (bool, default = False): If True, includes both the Gregorian and Jalali dates in the output.

    Returns:
    A DataFrame containing the TEDPIX index data including:
        - Open: The opening value of the index.
        - High: The highest value of the index.
        - Low: The lowest value of the index.
        - Close: The closing value of the index.
        - Adj Close: The adjusted closing value of the index.
        - Volume: The trading volume for the index.
        - Weekday (optional): The weekday name corresponding to the date (if `show_weekday` is True).
        - Date (optional): The original date (if `double_date` is False).

    Example Usage:
    To retrieve TEDPIX index data between '1403-11-01' and '1403-11-03':
    df = index_tedpix(start_date='1403-11-01', end_date='1403-11-03')

    To retrieve TEDPIX index data without weekday names:
    df_no_weekday = index_tedpix(start_date='1403-11-01', end_date='1403-11-03', show_weekday=False)

    To retrieve only Adjusted Close data:
    df_adj_close = index_tedpix(start_date='1403-11-01', end_date='1403-11-03', just_adj_close=True)

    Notes:
    - The function checks if the provided start and end dates are valid in the Jalali calendar and ensures the start date is before the end date.
    - If no data is found for the given date range, an empty DataFrame will be returned.
    """
    # check date validity --------------------------------------------------------------------------------------------------------------
    if(not ignore_date):
        start_date = check_date(start_date,key_word="'START'")
        if(start_date==None):
            return
        end_date = check_date(end_date,key_word="'END'")
        if(end_date==None):
            return
        start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
        end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
        if(start>end):
            print('Start date must be a day before end date!')
            return
    #---------------------------------------------------------------------------------------------------------------------------------------
    sector_web_id = 32097828799138957
    # get only close chart data for sector index:
    r_cl = requests.get(f'http://cdn.tsetmc.com/api/Index/GetIndexB2History/{sector_web_id}', headers=headers)
    df_sector_cl = pd.DataFrame(r_cl.json()['indexB2'])[['dEven','xNivInuClMresIbs']]
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: str(x))
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: x[:4]+'-'+x[4:6]+'-'+x[-2:])
    df_sector_cl['dEven'] = pd.to_datetime(df_sector_cl['dEven'])
    df_sector_cl.rename(columns={"dEven": "Date", "xNivInuClMresIbs":"Adj Close"}, inplace=True)
    df_sector_cl['J-Date']=df_sector_cl['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
    df_sector_cl['Weekday']=df_sector_cl['Date'].dt.weekday
    df_sector_cl['Weekday'] = df_sector_cl['Weekday'].apply(lambda x: calendar.day_name[x])
    df_sector_cl = df_sector_cl.set_index('J-Date')
    df_sector_cl = df_sector_cl[['Date','Weekday','Adj Close']]
    df_sector_cl['Adj Close'] = pd.to_numeric(df_sector_cl['Adj Close'])
    if(not just_adj_close):
        r = requests.get(f'http://old.tsetmc.com/tsev2/chart/data/IndexFinancial.aspx?i={sector_web_id}&t=ph', headers=headers)
        df_sector = pd.DataFrame(r.text.split(';'))
        columns=['Date','High','Low','Open','Close','Volume','D']
        # split data into defined columns
        df_sector[columns] = df_sector[0].str.split(",",expand=True)
        df_sector.drop(columns=[0,'D'],inplace=True)
        df_sector['Date']=pd.to_datetime(df_sector['Date'])
        df_sector['J-Date']=df_sector['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
        df_sector = df_sector.set_index('J-Date')
        df_sector.drop(columns=['Date'],inplace=True)
        # now concat:
        df_sector_cl = pd.concat([df_sector,df_sector_cl],axis=1).dropna()
        df_sector_cl = df_sector_cl[['Date','Weekday','Open','High','Low','Close','Adj Close','Volume']]
        cols = ['Open','High','Low','Close','Adj Close','Volume']
        df_sector_cl[cols] = df_sector_cl[cols].apply(pd.to_numeric, axis=1)
        df_sector_cl['Volume'] = df_sector_cl['Volume'].astype('int64')
    if(not show_weekday):
        df_sector_cl.drop(columns=['Weekday'],inplace=True)
    if(not double_date):
        df_sector_cl.drop(columns=['Date'],inplace=True)
    # slice requested time window:
    if(not ignore_date):
        df_sector_cl = df_sector_cl[start_date:end_date]    
    return df_sector_cl

################################################################################################################################################################################
################################################################################################################################################################################

def index_tedpix_ew(start_date:str = '1403-11-01', end_date:str = '1403-11-03', ignore_date:bool = False, just_adj_close:bool = True, show_weekday:bool = False, double_date:bool = False):
    """
    Function Description:
    index_tedpix_ew() retrieves the Tehran Stock Exchange (TEDPIX Equal Weight) index data for a specified date range.
    The function outputs trading metrics including Open, High, Low, Close, Adjusted Close, and Volume.
    It allows users to choose whether to display the weekday names and whether to keep the date column in the output.

    Parameters:
    start_date (str, default = '1403-11-01'): The start date of the data range in the format 'YYYY-MM-DD' (Jalali date).
    end_date (str, default = '1403-11-03'): The end date of the data range in the format 'YYYY-MM-DD' (Jalali date).
    ignore_date (bool, default = False): If True, the date range check is ignored.
    just_adj_close (bool, default = False): If True, only the Adjusted Close data is returned.
    show_weekday (bool, default = False): If True, includes the weekday names in the data.
    double_date (bool, default = False): If True, includes both the Gregorian and Jalali dates in the output.

    Returns:
    A DataFrame containing the TEDPIX Equal Weight index data including:
        - Open: The opening value of the index.
        - High: The highest value of the index.
        - Low: The lowest value of the index.
        - Close: The closing value of the index.
        - Adj Close: The adjusted closing value of the index.
        - Volume: The trading volume for the index.
        - Weekday (optional): The weekday name corresponding to the date (if `show_weekday` is True).
        - Date (optional): The original date (if `double_date` is False).

    Example Usage:
    To retrieve TEDPIX Equal Weight index data between '1403-11-01' and '1403-11-03':
    df = index_tedpix_ew(start_date='1403-11-01', end_date='1403-11-03')

    To retrieve TEDPIX Equal Weight index data without weekday names:
    df_no_weekday = index_tedpix_ew(start_date='1403-11-01', end_date='1403-11-03', show_weekday=False)

    To retrieve only Adjusted Close data:
    df_adj_close = index_tedpix_ew(start_date='1403-11-01', end_date='1403-11-03', just_adj_close=True)

    Notes:
    - The function checks if the provided start and end dates are valid in the Jalali calendar and ensures the start date is before the end date.
    - If no data is found for the given date range, an empty DataFrame will be returned.
    """
    # check date validity --------------------------------------------------------------------------------------------------------------
    if(not ignore_date):
        start_date = check_date(start_date,key_word="'START'")
        if(start_date==None):
            return
        end_date = check_date(end_date,key_word="'END'")
        if(end_date==None):
            return
        start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
        end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
        if(start>end):
            print('Start date must be a day before end date!')
            return
    #---------------------------------------------------------------------------------------------------------------------------------------
    sector_web_id = 67130298613737946
    # get only close chart data for sector index:
    r_cl = requests.get(f'http://cdn.tsetmc.com/api/Index/GetIndexB2History/{sector_web_id}', headers=headers)
    df_sector_cl = pd.DataFrame(r_cl.json()['indexB2'])[['dEven','xNivInuClMresIbs']]
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: str(x))
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: x[:4]+'-'+x[4:6]+'-'+x[-2:])
    df_sector_cl['dEven'] = pd.to_datetime(df_sector_cl['dEven'])
    df_sector_cl.rename(columns={"dEven": "Date", "xNivInuClMresIbs":"Adj Close"}, inplace=True)
    df_sector_cl['J-Date']=df_sector_cl['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
    df_sector_cl['Weekday']=df_sector_cl['Date'].dt.weekday
    df_sector_cl['Weekday'] = df_sector_cl['Weekday'].apply(lambda x: calendar.day_name[x])
    df_sector_cl = df_sector_cl.set_index('J-Date')
    df_sector_cl = df_sector_cl[['Date','Weekday','Adj Close']]
    df_sector_cl['Adj Close'] = pd.to_numeric(df_sector_cl['Adj Close'])
    if(not just_adj_close):
        r = requests.get(f'http://old.tsetmc.com/tsev2/chart/data/IndexFinancial.aspx?i={sector_web_id}&t=ph', headers=headers)
        df_sector = pd.DataFrame(r.text.split(';'))
        columns=['Date','High','Low','Open','Close','Volume','D']
        # split data into defined columns
        df_sector[columns] = df_sector[0].str.split(",",expand=True)
        df_sector.drop(columns=[0,'D'],inplace=True)
        df_sector['Date']=pd.to_datetime(df_sector['Date'])
        df_sector['J-Date']=df_sector['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
        df_sector = df_sector.set_index('J-Date')
        df_sector.drop(columns=['Date'],inplace=True)
        # now concat:
        df_sector_cl = pd.concat([df_sector,df_sector_cl],axis=1).dropna()
        df_sector_cl = df_sector_cl[['Date','Weekday','Open','High','Low','Close','Adj Close','Volume']]
        cols = ['Open','High','Low','Close','Adj Close','Volume']
        df_sector_cl[cols] = df_sector_cl[cols].apply(pd.to_numeric, axis=1)
        df_sector_cl['Volume'] = df_sector_cl['Volume'].astype('int64')
    if(not show_weekday):
        df_sector_cl.drop(columns=['Weekday'],inplace=True)
    if(not double_date):
        df_sector_cl.drop(columns=['Date'],inplace=True)
    # slice requested time window:
    if(not ignore_date):
        df_sector_cl = df_sector_cl[start_date:end_date]    
    return df_sector_cl

################################################################################################################################################################################
################################################################################################################################################################################

def micro_transactions(ticker_id, Jalali_date):
    """
    Instead of using this function, use the alternative "micro_transaction" function to calculate micro transactions.
    """
    #convert to desired Cristian data format
    year, month, day = Jalali_date.split('-')
    date = jdatetime.date(int(year), int(month), int(day)).togregorian()
    date = f'{date.year:04}{date.month:02}{date.day:02}'
    # request and process
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page = requests.get(f'http://cdn.tsetmc.com/api/Trade/GetTradeHistory/{ticker_id}/{date}/false', headers=headers)
    df_intraday = (pd.DataFrame(page.json()['tradeHistory'])).iloc[:,2:6]
    df_intraday = df_intraday.sort_values(by='nTran')
    df_intraday.drop(columns=['nTran'],inplace=True)
    df_intraday.columns = ['Time','Volume','Price']
    df_intraday['Time'] = df_intraday['Time'].astype('str').apply(lambda x: '0'+x[0]+':'+x[1:3]+':'+x[3:]  if len(x)==5 else x[:2]+':'+x[2:4]+':'+x[4:])
    df_intraday['J-Date'] = Jalali_date
    df_intraday = df_intraday.set_index(['J-Date','Time'])
    return df_intraday

################################################################################################################################################################################
################################################################################################################################################################################

def micro_transaction(stock:str = 'خودرو', start_date:str = '1403-11-01', end_date:str ='1403-11-03', jalali_date:bool = True, combined_datatime:bool = False, show_progress:bool = True):
    """
    Function Description:
    micro_transaction() retrieves micro transaction data for a specific stock ticker over a specified date range.
    The output includes trading information such as the trading volume and price for each transaction during that period.

    Parameters:
    stock (str, default = 'وخارزم'): The stock ticker (e.g., 'وخارزم') for which micro transaction data is requested.
    start_date (str, default = '1400-09-15'): The start date of the data range in the format 'YYYY-MM-DD' (Jalali date).
    end_date (str, default = '1400-12-29'): The end date of the data range in the format 'YYYY-MM-DD' (Jalali date).
    jalali_date (bool, default = True): If True, the data will be returned with Jalali dates.
    combined_datatime (bool, default = False): If True, the date and time will be combined into a single datetime column.
    show_progress (bool, default = True): If True, the progress of data retrieval is displayed during the process.

    Returns:
    A DataFrame containing the following columns:
        - Volume: The trading volume of the stock during the micro transaction.
        - Price: The price of the stock during the micro transaction.
        - J-Date: The Jalali date of the transaction.
        - Time: The time of the transaction.

    Example Usage:
    To retrieve micro transaction data for 'وخارزم' stock between '1400-09-15' and '1400-12-29':
    df = micro_transaction(stock='وخارزم', start_date='1400-09-15', end_date='1400-12-29')

    To retrieve the data with combined Jalali date and time:
    df_combined = micro_transaction(stock='وخارزم', start_date='1400-09-15', end_date='1400-12-29', combined_datatime=True)

    Notes:
    - The function retrieves the data by fetching intraday trading information for each day within the given date range.
    - If any data is unavailable for certain dates, the function will output a warning with a list of failed dates.
    - The returned DataFrame's index is based on the combination of Jalali date and time or just the Jalali date and time separately, depending on the input parameters.
    """
    # a function to get price data from a given page ----------------------------------------------------------------------------------
    failed_jdates = []
    def get_price_data_forintraday(ticker_id):
        r = requests.get(f'http://old.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i={ticker_id}&Top=999999&A=0', headers=headers)
        df_history=pd.DataFrame(r.text.split(';'))
        columns=['Date','High','Low','Final','Close','Open','Y-Final','Value','Volume','No']
        #split data into defined columns
        df_history[columns] = df_history[0].str.split("@",expand=True)
        # drop old column 0
        df_history.drop(columns=[0],inplace=True)
        df_history.dropna(inplace=True)
        df_history['Date']=pd.to_datetime(df_history['Date'])
        df_history['webid'] = ticker_id
        df_history = df_history.set_index('Date')
        return df_history
    # check date validity --------------------------------------------------------------------------------------------------------------
    start_date = check_date(start_date,key_word="'START'")
    if(start_date==None):
        return
    end_date = check_date(end_date,key_word="'END'")
    if(end_date==None):
        return
    start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
    end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
    if(start>end):
        print('Start date must be a day before end date!')
        return
    #-----------------------------------------------------------------------------------------------------------------------------------
    # find web-ids 
    ticker_no_df = share_id_old(stock)
    if(type(ticker_no_df)==bool):
        return
    # create an empty dataframe:
    df_history = pd.DataFrame({},columns=['Date','High','Low','Final','Close','Open','Y-Final','Value','Volume','No','webid']).set_index('Date')
    # loop to get data from different pages of a Ticker:
    for index, row in (ticker_no_df.reset_index()).iterrows():
        try:
            df_temp = get_price_data_forintraday(ticker_id = row['webid'])
            df_history = pd.concat([df_history,df_temp])
        except:
            pass
    # sort index and reverse the order for more processes:
    df_history = df_history.sort_index(ascending=True)
    df_history = df_history.reset_index()
    df_history['J-Date']=df_history['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
    df_history = df_history.set_index('J-Date')
    df_history = df_history[start_date:end_date]
    j_date_list = df_history.index.to_list()
    ticker_no_list = df_history['webid'].to_list()
    # now we have valid Jalali date list, let's loop over and concat:
    no_days = len(j_date_list)
    if(no_days==0):
        print('There is no trading day between start and end date for this stock!')
        return
    else:
        df_intraday = pd.DataFrame(columns=['J-Date','Time','Volume','Price']).set_index(['J-Date','Time'])
        day_counter = 1
        for Jalali_date in j_date_list:
            try:
                df_intraday = pd.concat([df_intraday,micro_transactions(ticker_no_list[day_counter-1], Jalali_date)], axis=0)
            except:
                failed_jdates.append(Jalali_date)
            if(show_progress):
                clear_output(wait=True)
                print('Progress : ', f'{round((day_counter)/no_days*100,1)} %')
            day_counter+=1
    # other settings -------------------------------------------------------------------------------------------------------------
    if(jalali_date):
        if(combined_datatime):
            df_intraday = df_intraday.reset_index()
            # add date to data frame:
            df_intraday['Date'] = df_intraday['J-Date'].apply(lambda x: jdatetime.date(int(x[:4]),int(x[5:7]),int(x[8:])).togregorian())
            df_intraday['DateTime'] = pd.to_datetime(df_intraday['Date'].astype(str) +' '+ df_intraday['Time'].astype(str))
            print('Combining Jalali date and time takes a few more seconds!')
            df_intraday['J-DateTime'] = df_intraday['DateTime'].apply(lambda x: str(jdatetime.datetime.fromgregorian(datetime=x)))
            df_intraday.drop(columns=['DateTime','Date','J-Date','Time'],inplace=True)
            df_intraday = df_intraday.set_index(['J-DateTime'])
    else:
        if(combined_datatime):
            df_intraday = df_intraday.reset_index()
            df_intraday['Date'] = df_intraday['J-Date'].apply(lambda x: jdatetime.date(int(x[:4]),int(x[5:7]),int(x[8:])).togregorian())
            df_intraday['DateTime'] = pd.to_datetime(df_intraday['Date'].astype(str) +' '+ df_intraday['Time'].astype(str))
            df_intraday.drop(columns=['Date','J-Date','Time'],inplace=True)
            df_intraday = df_intraday.set_index(['DateTime'])
        else:
            df_intraday = df_intraday.reset_index()
            df_intraday['Date'] = df_intraday['J-Date'].apply(lambda x: jdatetime.date(int(x[:4]),int(x[5:7]),int(x[8:])).togregorian())
            df_intraday.drop(columns=['J-Date'],inplace=True)
            df_intraday = df_intraday.set_index(['Date','Time'])
    df_intraday[['Volume','Price']] = df_intraday[['Volume','Price']].astype('int64')
    # warning for failed dates:
    if(len(failed_jdates)!=0):
        print('WARNING: The following days data is not available on TSE website, even if those are trading days!')
        print(failed_jdates)
    return df_intraday
    
################################################################################################################################################################################
################################################################################################################################################################################

def usd_rial(start_date = '1403-11-01', end_date='1403-11-03', ignore_date = False, show_weekday = False, double_date = False):
    """
    Function Description:
    usd_rial() retrieves the historical exchange rate data between the US Dollar (USD) and Iranian Rial (IRR) 
    for a specified date range. The output includes information about the opening, closing, highest, 
    and lowest values of the USD/Rial exchange rate for each day within the range.

    Parameters:
    start_date (str, default = '1403-11-01'): The start date of the data range in the format 'YYYY-MM-DD' (Jalali date).
    end_date (str, default = '1403-11-03'): The end date of the data range in the format 'YYYY-MM-DD' (Jalali date).
    ignore_date (bool, default = False): If False, the function checks the validity of the dates provided.
    show_weekday (bool, default = False): If True, includes the weekday name for each date in the output.
    double_date (bool, default = False): If True, includes the Gregorian date alongside the Jalali date in the output.

    Returns:
    A DataFrame containing the following columns:
    - Open: The opening exchange rate of USD to Rial for the day.
    - High: The highest exchange rate of USD to Rial for the day.
    - Low: The lowest exchange rate of USD to Rial for the day.
    - Close: The closing exchange rate of USD to Rial for the day.
    - J-Date: The Jalali date of the transaction.
    - Weekday (optional): The weekday name of the transaction.

    Example Usage:
    To retrieve USD/Rial exchange rate data between '1403-11-01' and '1403-11-03':
    df = usd_rial(start_date='1403-11-01', end_date='1403-11-03')

    To retrieve the data with the weekday name and double date (Gregorian and Jalali):
    df_with_weekday = usd_rial(start_date='1403-11-01', end_date='1403-11-03', show_weekday=True, double_date=True)

    Notes:
    - The function retrieves data from the platform.tgju.org API, which provides USD to Rial exchange rates.
    - If the data is not up-to-date or unavailable, the function will fetch alternative data from a backup source.
    - The function checks the validity of the start and end dates and ensures the start date is earlier than the end date.
    """

    # check date validity --------------------------------------------------------------------------------------------------------------
    if(not ignore_date):
        start_date = check_date(start_date,key_word="'START'")
        if(start_date==None):
            return
        end_date = check_date(end_date,key_word="'END'")
        if(end_date==None):
            return
        start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
        end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
        if(start>end):
            print('Start date must be a day before end date!')
            return
    #---------------------------------------------------------------------------------------------------------------------------------------
    r = requests.get('https://platform.tgju.org/fa/tvdata/history?symbol=PRICE_DOLLAR_RL&resolution=1D', headers=headers)
    df_data = r.json()
    try:
        df_data = pd.DataFrame({'Date':df_data['t'],'Open':df_data['o'],'High':df_data['h'],'Low':df_data['l'],'Close':df_data['c'],})
        df_data['Date'] = df_data['Date'].apply(lambda x: datetime.datetime.fromtimestamp(x))
        df_data = df_data.set_index('Date')
        df_data.index = df_data.index.to_period("D")
        df_data.index=df_data.index.to_series().astype(str)
        df_data = df_data.reset_index()
        df_data['Date'] = pd.to_datetime(df_data['Date'])
        df_data['Weekday']=df_data['Date'].dt.weekday
        df_data['Weekday'] = df_data['Weekday'].apply(lambda x: calendar.day_name[x])
        df_data['J-Date']=df_data['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
        df_data = df_data.set_index('J-Date')
        df_data=df_data[['Date','Weekday','Open','High','Low','Close']]
        if(not show_weekday):
            df_data.drop(columns=['Weekday'],inplace=True)
        if(not double_date):
            df_data.drop(columns=['Date'],inplace=True)
        if(not ignore_date):
            df_data = df_data[start_date:end_date]
    except:
        print('WARNING: USD/RIAL data is not up-to-date! Check the following links to find out what is going on!')
        print('https://www.tgju.org/profile/price_dollar_rl/technical')
        print('https://www.tgju.org/profile/price_dollar_rl/history')
        url = 'https://api.accessban.com/v1/market/indicator/summary-table-data/price_dollar_rl' # get existing history
        r = requests.get(url, headers=headers)
        df_data = pd.DataFrame(r.json()['data'])
        df_data.columns = ['Open','Low','High','Close','4','3','Date','7']
        df_data = df_data[['Date','Open','High','Low','Close']]
        df_data['Date'] = pd.to_datetime(df_data['Date'])
        df_data['Weekday']=df_data['Date'].dt.weekday
        df_data['Weekday'] = df_data['Weekday'].apply(lambda x: calendar.day_name[x])
        df_data['J-Date']=df_data['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
        df_data = df_data.set_index('J-Date')
        df_data=df_data[['Date','Weekday','Open','High','Low','Close']]
        cols = ['Open','High','Low','Close']
        df_data['Open'] = df_data['Open'].apply(lambda x: x.replace(',',''))
        df_data['High'] = df_data['High'].apply(lambda x: x.replace(',',''))
        df_data['Low'] = df_data['Low'].apply(lambda x: x.replace(',',''))
        df_data['Close'] = df_data['Close'].apply(lambda x: x.replace(',',''))
        df_data[cols] = df_data[cols].apply(pd.to_numeric).astype('int64')
        df_data = df_data[df_data['Open']!=0]
        df_data = df_data.iloc[::-1]
        if(not show_weekday):
            df_data.drop(columns=['Weekday'],inplace=True)
        if(not double_date):
            df_data.drop(columns=['Date'],inplace=True)
        if(not ignore_date):
            df_data = df_data[start_date: end_date]
    return df_data

################################################################################################################################################################################
################################################################################################################################################################################

def queue_one_day(ticker_id, Jalali_date):
    """
    Function Description:
    queue_one_day() retrieves the buy and sell queues' values for a specific stock ticker at a given date 
    on the Tehran Stock Exchange (TSETMC). The function fetches the static threshold values (upper and lower 
    band prices) and the limit order book (LOB) data. It then calculates the buy queue (BQ) and sell queue (SQ) 
    values before the market close (12:30:00) and computes per capita values for both the buy and sell queues.

    Parameters:
    ticker_id (str): The stock ticker ID for the desired stock on TSETMC.
    Jalali_date (str): The date of interest in the Jalali (Persian) calendar format 'YYYY-MM-DD'.

    Returns:
    A DataFrame containing the following columns:
    - Day_UL: The upper price threshold for the day.
    - Day_LL: The lower price threshold for the day.
    - Time: The timestamp of the last order before the market close.
    - BQ_Value: The total buy queue value.
    - SQ_Value: The total sell queue value.
    - BQPC: The per capita buy queue value.
    - SQPC: The per capita sell queue value.
    - J-Date: The Jalali date of the transaction.

    Example Usage:
    To retrieve the buy and sell queue values for a stock with ticker 65883838195688438 on the date '1403-11-01':
    df = queue_one_day(ticker_id=65883838195688438, Jalali_date='1403-11-01')

    Notes:
    - The function retrieves data from TSETMC's API endpoints for static threshold values and limit order book (LOB) data.
    - The calculations for the buy and sell queues are done before 12:30:00 (market close time).
    """

    #convert to desired Cristian data format
    year, month, day = Jalali_date.split('-')
    date = jdatetime.date(int(year), int(month), int(day)).togregorian()
    date = f'{date.year:04}{date.month:02}{date.day:02}'
    # get day upper and lower band prices:
    page = requests.get(f'http://cdn.tsetmc.com/api/MarketData/GetStaticThreshold/{ticker_id}/{date}', headers=headers)
    df_ub_lb = pd.DataFrame(page.json()['staticThreshold'])
    day_ub = df_ub_lb.iloc[-1]['psGelStaMax']    # day upper band price
    day_lb = df_ub_lb.iloc[-1]['psGelStaMin']    # day lower band price
    # get LOB data:
    page = requests.get(f'http://cdn.tsetmc.com/api/BestLimits/{ticker_id}/{date}', headers=headers)
    data = pd.DataFrame(page.json()['bestLimitsHistory'])
    # find last orders before 12:30:00 (market close)
    time = 123000
    bq, sq, bq_percap, sq_percap = 0.0, 0.0, 0.0, 0.0
    while(time>122900):
        end_lob = data[data['hEven'] == time]
        end_lob = end_lob.sort_values(by='number', ascending=True).iloc[:1,5:-1]
        end_lob.columns = ['Vol_Buy','No_Buy','Price_Buy','Price_Sell','No_Sell','Vol_Sell']
        end_lob = end_lob[['No_Sell','Vol_Sell','Price_Sell','Price_Buy','No_Buy','Vol_Buy']]
        if(len(end_lob)==0): #go one second back and try again
            time-=1
            if(int(str(time)[-2:])>59):
                a = int(str(time)[:-2]+'59')
        else:
            # check buy and sell queue and do calculations
            if(end_lob.iloc[0]['Price_Sell'] == day_lb):
                sq = day_lb * end_lob.iloc[0]['Vol_Sell']
                sq_percap = sq/end_lob.iloc[0]['No_Sell']
            if(end_lob.iloc[0]['Price_Buy'] == day_ub):
                bq = day_ub * end_lob.iloc[0]['Vol_Buy']
                bq_percap = bq/end_lob.iloc[0]['No_Buy']
            break
    df_sq_bq = pd.DataFrame({'J-Date':[Jalali_date],'Day_UL':[int(day_lb)],'Day_LL':[int(day_ub)], 'Time':[str(time)[:2]+':'+str(time)[2:4]+':'+str(time)[-2:]],\
                             'BQ_Value':[int(bq)],'SQ_Value':[int(sq)],'BQPC':[int(round(bq_percap,0))], 'SQPC':[int(round(sq_percap,0))]})
    df_sq_bq = df_sq_bq.set_index('J-Date')
    return df_sq_bq

################################################################################################################################################################################
################################################################################################################################################################################

def queues(stock = 'خودرو', start_date = '1403-11-01', end_date='1403-11-03', show_per_capita = True, show_weekday = False, double_date = False, show_progress = True):
    """
    Function Description:
    queues() retrieves the buy and sell queue values for a specified stock in Tehran Stock Exchange (TSETMC)
    over a range of trading days between a start and end date. It calculates the buy queue (BQ) and sell queue (SQ) 
    values before market close for each day within the provided date range. This function also retrieves the 
    upper and lower band prices for the stock on each trading day and the total stock value for the day.

    Parameters:
    stock (str): The stock ticker name for the desired stock.
    start_date (str): The start date in Jalali (Persian) calendar format 'YYYY-MM-DD'.
    end_date (str): The end date in Jalali (Persian) calendar format 'YYYY-MM-DD'.
    show_per_capita (bool): A flag to control whether to show per capita values for buy and sell queues.
    show_weekday (bool): A flag to control whether to include weekday information in the output.
    double_date (bool): A flag to control whether to show the full date (Gregorian) in the output.
    show_progress (bool): A flag to display progress during data retrieval and processing.

    Returns:
    A DataFrame containing the following columns:
    - Day_UL: The upper price threshold for the day.
    - Day_LL: The lower price threshold for the day.
    - Value: The total value of the stock for the day.
    - Time: The timestamp of the last order before the market close.
    - BQ_Value: The total buy queue value.
    - SQ_Value: The total sell queue value.
    - BQPC: The per capita buy queue value.
    - SQPC: The per capita sell queue value.
    - Weekday: The weekday of the trading day.
    - J-Date: The Jalali date of the transaction.

    Example Usage:
    To retrieve buy and sell queue values for the stock 'خودرو' between '1403-11-01' and '1403-11-03':
    df = queues(stock='خودرو', start_date='1403-11-01', end_date='1403-11-03')

    Notes:
    - The function retrieves stock data from TSETMC's API and processes multiple ticker web-ids for the stock.
    - The function calculates the buy and sell queues before 12:30:00 (market close time) and retrieves the trading value for each day.
    - Any failed dates, where data could not be retrieved, will be printed as warnings.
    """

    # a function to get price data from a given page ----------------------------------------------------------------------------------
    def get_price_data_forintraday(ticker_id):
        r = requests.get(f'http://old.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i={ticker_id}&Top=999999&A=0', headers=headers)
        df_history=pd.DataFrame(r.text.split(';'))
        columns=['Date','High','Low','Final','Close','Open','Y-Final','Value','Volume','No']
        #split data into defined columns
        df_history[columns] = df_history[0].str.split("@",expand=True)
        # drop old column 0
        df_history.drop(columns=[0],inplace=True)
        df_history.dropna(inplace=True)
        df_history['Date']=pd.to_datetime(df_history['Date'])
        df_history['webid'] = ticker_id
        df_history = df_history.set_index('Date')
        return df_history
    # check date validity --------------------------------------------------------------------------------------------------------------
    failed_jdates = []
    start_date = check_date(start_date,key_word="'START'")
    if(start_date==None):
        return
    end_date = check_date(end_date,key_word="'END'")
    if(end_date==None):
        return
    start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
    end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
    if(start>end):
        print('Start date must be a day before end date!')
        return
    #-----------------------------------------------------------------------------------------------------------------------------------
    # find web-ids 
    ticker_no_df = share_id_old(stock)
    if(type(ticker_no_df)==bool):
        return
    # create an empty dataframe:
    df_history = pd.DataFrame({},columns=['Date','High','Low','Final','Close','Open','Y-Final','Value','Volume','No','webid']).set_index('Date')
    # loop to get data from different pages of a Ticker:
    for index, row in (ticker_no_df.reset_index()).iterrows():
        try:
            df_temp = get_price_data_forintraday(ticker_id = row['webid'])
            df_history = pd.concat([df_history,df_temp])
        except:
            pass
    # sort index and reverse the order for more processes:
    df_history = df_history.sort_index(ascending=True)
    df_history = df_history.reset_index()
    df_history['J-Date']=df_history['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
    df_history['Weekday']=df_history['Date'].dt.weekday
    df_history['Weekday'] = df_history['Weekday'].apply(lambda x: calendar.day_name[x])
    df_history = df_history.set_index('J-Date')
    df_history = df_history[start_date:end_date]
    j_date_list = df_history.index.to_list()
    ticker_no_list = df_history['webid'].to_list()
    # now we have valid Jalali date list, let's loop over and concat:
    no_days = len(j_date_list)
    if(no_days==0):
        print('There is no trading day between start and end date for this stock!')
        return
    else:
        df_bq_sq_val = pd.DataFrame(columns=['J-Date','Day_UL','Day_LL','Time','BQ_Value','SQ_Value','BQPC','SQPC']).set_index(['J-Date'])
        day_counter = 1
        for Jalali_date in j_date_list:
            try:
                df_bq_sq_val = pd.concat([df_bq_sq_val,queue_one_day(ticker_no_list[day_counter-1], Jalali_date)], axis=0)
            except:
                failed_jdates.append(Jalali_date)
            if(show_progress):
                clear_output(wait=True)
                print('Progress : ', f'{round((day_counter)/no_days*100,1)} %')
            day_counter+=1
    df_bq_sq_val = pd.concat([df_bq_sq_val, df_history[['Value','Date','Weekday']]], axis=1, join="inner") 
    cols = ['Day_UL','Day_LL','Value','BQ_Value','SQ_Value','BQPC','SQPC']
    df_bq_sq_val[cols] = df_bq_sq_val[cols].apply(pd.to_numeric).astype('int64')
    # re-arrange columns order:
    df_bq_sq_val = df_bq_sq_val[['Date','Weekday','Day_UL','Day_LL','Value','Time','BQ_Value','SQ_Value','BQPC','SQPC']]
    if(not show_per_capita):
        df_bq_sq_val.drop(columns=['BQPC','SQPC'],inplace=True)
    if(not show_weekday):
        df_bq_sq_val.drop(columns=['Weekday'],inplace=True)
    if(not double_date):
        df_bq_sq_val.drop(columns=['Date'],inplace=True)
    # warning for failed dates:
    if(len(failed_jdates)!=0):
        print('WARNING: The following days data is not available on TSE website, even if those are trading days!')
        print(failed_jdates)
    return df_bq_sq_val

################################################################################################################################################################################
################################################################################################################################################################################

def supply_demand_one_day(ticker_id, Jalali_date):
    """
    Function Description:
    supply_demand_one_day() retrieves the supply and demand data for a specific stock ticker 
    on a given trading day from the Tehran Stock Exchange (TSETMC). The function collects 
    real-time order book data including buy and sell prices, volumes, and other relevant 
    information about the stock's trading activity.

    Parameters:
    ticker_id (str): The stock's unique identifier (ticker) on the Tehran Stock Exchange (TSETMC).
    Jalali_date (str): The date of interest in the Jalali calendar format ('YYYY-MM-DD').

    Returns:
    A DataFrame containing the following columns:
    - J-Date: The Jalali date of the transaction.
    - Time: The exact time of the order book data.
    - Depth: The depth of the order.
    - Sell_No: The number of sell orders.
    - Sell_Vol: The volume of sell orders.
    - Sell_Price: The price at which the sell orders were placed.
    - Buy_Price: The price at which the buy orders were placed.
    - Buy_Vol: The volume of buy orders.
    - Buy_No: The number of buy orders.
    - Day_LL: The lower price band for the day.
    - Day_UL: The upper price band for the day.
    - Date: The Gregorian date of the transaction.

    Example Usage:
    To retrieve the supply and demand data for a stock with ticker 65883838195688438 on '1403-11-03':
    df = supply_demand_one_day(ticker_id=65883838195688438, Jalali_date='1403-11-03')

    Notes:
    - The function retrieves data from TSETMC APIs to fetch static threshold data (upper and lower price bands)
      and order book data (buy and sell orders).
    - The data is filtered to only include transactions between 8:45 AM and 12:30 PM.
    - The returned DataFrame is indexed by the Jalali date, time, and order depth.
    """

    #convert to desired Cristian data format
    year, month, day = Jalali_date.split('-')
    date = jdatetime.date(int(year), int(month), int(day)).togregorian()
    date = f'{date.year:04}{date.month:02}{date.day:02}'
    # get day upper and lower band prices:
    page = requests.get(f'http://cdn.tsetmc.com/api/MarketData/GetStaticThreshold/{ticker_id}/{date}', headers=headers)
    df_ub_lb = pd.DataFrame(page.json()['staticThreshold'])
    day_ub = df_ub_lb.iloc[-1]['psGelStaMax']    # day upper band price
    day_lb = df_ub_lb.iloc[-1]['psGelStaMin']    # day lower band price
    # get LOB data:
    page = requests.get(f'http://cdn.tsetmc.com/api/BestLimits/{ticker_id}/{date}',headers=headers)
    data = pd.DataFrame(page.json()['bestLimitsHistory'])
    data.drop(columns=['idn','dEven','refID','insCode'],inplace=True)
    data = data.sort_values(['hEven','number'], ascending = (True, True))
    data = data[(data['hEven']>=84500) & (data['hEven']<123000)]  # filter out 8:30 to 12:35
    data.columns = ['Time','Depth','Buy_Vol','Buy_No','Buy_Price','Sell_Price','Sell_No','Sell_Vol']
    data['J-Date'] = Jalali_date
    data['Date'] = date
    data['Date'] = pd.to_datetime(data['Date'])
    # re-arrange columns:
    data['Time'] = data['Time'].astype('str').apply(lambda x :datetime.time(hour=int(x[0]),minute=int(x[1:3]),second=int(x[3:])) if len(x)==5\
                                                    else datetime.time(hour=int(x[:2]),minute=int(x[2:4]),second=int(x[4:])))
    data['Day_UL'] = day_ub
    data['Day_LL'] = day_lb
    data = data[['J-Date','Time','Depth','Sell_No','Sell_Vol','Sell_Price','Buy_Price','Buy_Vol','Buy_No','Day_LL','Day_UL','Date']]
    data = data.set_index(['J-Date','Time','Depth'])
    return data

################################################################################################################################################################################
################################################################################################################################################################################

def supply_demand(stock = 'خودرو', start_date = '1403-11-01', end_date= '1403-11-03', jalali_date = True, combined_datatime = False, show_progress = True):
    """
    Function Description:
    supply_demand() retrieves the supply and demand data for the order book of a specific stock
    during the trading days between the provided start and end dates. If you only need data for a specific
    day, set the start and end dates to the same value.

    Parameters:
    stock (str): The stock's ticker symbol (e.g., 'کرمان').
    start_date (str): The start date for data retrieval in Jalali format ('YYYY-MM-DD').
    end_date (str): The end date for data retrieval in Jalali format ('YYYY-MM-DD').
    jalali_date (bool): If True, the output will be in Jalali date format. Defaults to True.
    combined_datatime (bool): If True, combines the date and time into a single column in the output. Defaults to False.
    show_progress (bool): If True, displays progress of data retrieval. Defaults to True.

    Returns:
    pd.DataFrame: A DataFrame containing the following columns:
        - J-Date: The Jalali date of the transaction.
        - Time: The exact time of the order book data.
        - Depth: The depth of the order.
        - Sell_No: The number of sell orders.
        - Sell_Vol: The volume of sell orders.
        - Sell_Price: The price at which the sell orders were placed.
        - Buy_Price: The price at which the buy orders were placed.
        - Buy_Vol: The volume of buy orders.
        - Buy_No: The number of buy orders.
        - Day_LL: The lower price band for the day.
        - Day_UL: The upper price band for the day.

    Example Usage:
    To retrieve the supply and demand data for the stock 'کرمان' between '1400-08-01' and '1400-08-05':
    df = supply_demand(stock='کرمان', start_date='1400-08-01', end_date='1400-08-05')

    Notes:
    - The function retrieves data from TSETMC APIs for each trading day within the specified range.
    - The data includes price, volume, and order details for each stock's buy and sell orders.
    - The function handles both Jalali and Gregorian dates, with the option to combine date and time into a single column.
    - The DataFrame is indexed by the Jalali date, time, and depth of the order.
    """

# a function to get price data from a given page ----------------------------------------------------------------------------------
    def get_price_data_forintraday(ticker_id):
        r = requests.get(f'http://old.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i={ticker_id}&Top=999999&A=0', headers=headers)
        df_history=pd.DataFrame(r.text.split(';'))
        columns=['Date','High','Low','Final','Close','Open','Y-Final','Value','Volume','No']
        #split data into defined columns
        df_history[columns] = df_history[0].str.split("@",expand=True)
        # drop old column 0
        df_history.drop(columns=[0],inplace=True)
        df_history.dropna(inplace=True)
        df_history['Date']=pd.to_datetime(df_history['Date'])
        df_history['webid'] = ticker_id
        df_history = df_history.set_index('Date')
        return df_history
    # check date validity --------------------------------------------------------------------------------------------------------------
    failed_jdates = []
    start_date = check_date(start_date,key_word="'START'")
    if(start_date==None):
        return
    end_date = check_date(end_date,key_word="'END'")
    if(end_date==None):
        return
    start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
    end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
    if(start>end):
        print('Start date must be a day before end date!')
        return
    #-----------------------------------------------------------------------------------------------------------------------------------
    # find web-ids 
    ticker_no_df = share_id_old(stock)
    if(type(ticker_no_df)==bool):
        return
    # create an empty dataframe:
    df_history = pd.DataFrame({},columns=['Date','High','Low','Final','Close','Open','Y-Final','Value','Volume','No','webid']).set_index('Date')
    # loop to get data from different pages of a Ticker:
    for index, row in (ticker_no_df.reset_index()).iterrows():
        try:
            df_temp = get_price_data_forintraday(ticker_id = row['webid'])
            df_history = pd.concat([df_history,df_temp])
        except:
            pass
    # sort index and reverse the order for more processes:
    df_history = df_history.sort_index(ascending=True)
    df_history = df_history.reset_index()
    df_history['J-Date']=df_history['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
    df_history = df_history.set_index('J-Date')
    df_history = df_history[start_date:end_date]
    j_date_list = df_history.index.to_list()
    ticker_no_list = df_history['webid'].to_list()
    # now we have valid Jalali date list, let's loop over and concat:
    no_days = len(j_date_list)
    if(no_days==0):
        print('There is no trading day between start and end date for this stock!')
        return 
    else:
        df_lob = pd.DataFrame(columns=['J-Date','Time','Depth','Sell_No','Sell_Vol','Sell_Price','Buy_Price','Buy_Vol','Buy_No',\
                                       'Day_LL','Day_UL','Date']).set_index(['J-Date','Time','Depth'])
        day_counter = 1
        for Jalali_date in j_date_list:
            try:
                df_lob = pd.concat([df_lob,supply_demand_one_day(ticker_no_list[day_counter-1], Jalali_date)], axis=0)
            except:
                failed_jdates.append(Jalali_date)
            if(show_progress):
                clear_output(wait=True)
                print('Progress : ', f'{round((day_counter)/no_days*100,1)} %')
            day_counter+=1
    if(jalali_date):
        if(combined_datatime):
            df_lob = df_lob.reset_index()
            df_lob['DateTime'] = pd.to_datetime(df_lob['Date'].astype(str) +' '+ df_lob['Time'].astype(str))
            print('Combining Jalali date and time takes a few more seconds!')
            df_lob['J-DateTime'] = df_lob['DateTime'].apply(lambda x: str(jdatetime.datetime.fromgregorian(datetime=x)))
            df_lob.drop(columns=['DateTime','Date','J-Date','Time'],inplace=True)
            df_lob = df_lob.set_index(['J-DateTime','Depth'])
        else:
            df_lob.drop(columns=['Date'],inplace=True)
    else:
        if(combined_datatime):
            df_lob = df_lob.reset_index()
            df_lob['DateTime'] = pd.to_datetime(df_lob['Date'].astype(str) +' '+ df_lob['Time'].astype(str))
            df_lob.drop(columns=['Date','J-Date','Time'],inplace=True)
            df_lob = df_lob.set_index(['DateTime','Depth'])
        else:
            df_lob = df_lob.reset_index()
            df_lob.drop(columns=['J-Date'],inplace=True)
            df_lob = df_lob.set_index(['Date','Time','Depth'])
    if(len(failed_jdates)!=0):
        print('WARNING: The following days data is not available on TSE website, even if those are trading days!')
        print(failed_jdates)
    return df_lob

################################################################################################################################################################################
################################################################################################################################################################################

def index_group(sector = 'خودرو', start_date='1403-11-01', end_date='1403-11-03', ignore_date = False, just_adj_close = False, show_weekday = False, double_date = False):
    """
    Function Description:
    index_group() retrieves the historical index data for a specific sector group during the trading days
    between the given start and end dates. It supports retrieving the full index history for the sector
    without regard to the start and end dates, displaying the day of the week, showing only the adjusted close
    values, and using either Jalali or Gregorian dates.

    Parameters:
    sector (str): The name of the sector group (e.g., 'خودرو').
    start_date (str): The start date for data retrieval in Jalali format ('YYYY-MM-DD').
    end_date (str): The end date for data retrieval in Jalali format ('YYYY-MM-DD').
    ignore_date (bool): If True, ignores the start and end date and retrieves all available data. Defaults to False.
    just_adj_close (bool): If True, only retrieves the adjusted close values. Defaults to False.
    show_weekday (bool): If True, displays the weekday for each date. Defaults to False.
    double_date (bool): If True, includes both Jalali and Gregorian dates in the output. Defaults to False.

    Returns:
    pd.DataFrame: A DataFrame containing the following columns:
        - Date: The date of the index value (either Jalali or Gregorian, based on the `double_date` parameter).
        - Weekday: The weekday name (if `show_weekday` is True).
        - Open: The opening value of the index.
        - High: The highest value of the index.
        - Low: The lowest value of the index.
        - Close: The closing value of the index.
        - Adj Close: The adjusted closing value of the index.
        - Volume: The volume of the transactions.

    Example Usage:
    To retrieve the index data for the 'خودرو' sector between '1403-11-01' and '1403-11-03':
    df = index_group(sector='خودرو', start_date='1403-11-01', end_date='1403-11-03')

    Notes:
    - The function retrieves data from TSETMC APIs for each trading day within the specified date range.
    - The data includes prices, volume, and other financial indicators for the sector group index.
    - The returned DataFrame is indexed by the Jalali date and contains columns for various financial data.
    - The function handles both Jalali and Gregorian dates, with the option to show weekday names and combine both date formats.
    """

    # check date validity --------------------------------------------------------------------------------------------------------------
    if(not ignore_date):
        start_date = check_date(start_date,key_word="'START'")
        if(start_date==None):
            return
        end_date = check_date(end_date,key_word="'END'")
        if(end_date==None):
            return
        start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
        end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
        if(start>end):
            print('Start date must be a day before end date!')
            return
    # get sector web-id ---------------------------------------------------------------------------------------------------------------------
    try:
        sector_web_id = group_id(group_name = sector)
    except:
        print('Please Enter a Valid Name for Sector Index!')
        return
    if(sector_web_id == None):
        return
    r_cl = requests.get(f'http://cdn.tsetmc.com/api/Index/GetIndexB2History/{sector_web_id}', headers=headers)
    df_sector_cl = pd.DataFrame(r_cl.json()['indexB2'])[['dEven','xNivInuClMresIbs']]
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: str(x))
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: x[:4]+'-'+x[4:6]+'-'+x[-2:])
    df_sector_cl['dEven'] = pd.to_datetime(df_sector_cl['dEven'])
    df_sector_cl.rename(columns={"dEven": "Date", "xNivInuClMresIbs":"Adj Close"}, inplace=True)
    df_sector_cl['J-Date']=df_sector_cl['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
    df_sector_cl['Weekday']=df_sector_cl['Date'].dt.weekday
    df_sector_cl['Weekday'] = df_sector_cl['Weekday'].apply(lambda x: calendar.day_name[x])
    df_sector_cl = df_sector_cl.set_index('J-Date')
    df_sector_cl = df_sector_cl[['Date','Weekday','Adj Close']]
    df_sector_cl['Adj Close'] = pd.to_numeric(df_sector_cl['Adj Close'])
    if(not just_adj_close):
        r = requests.get(f'http://old.tsetmc.com/tsev2/chart/data/IndexFinancial.aspx?i={sector_web_id}&t=ph', headers=headers)
        df_sector = pd.DataFrame(r.text.split(';'))
        columns=['Date','High','Low','Open','Close','Volume','D']
        # split data into defined columns
        df_sector[columns] = df_sector[0].str.split(",",expand=True)
        df_sector.drop(columns=[0,'D'],inplace=True)
        df_sector['Date']=pd.to_datetime(df_sector['Date'])
        df_sector['J-Date']=df_sector['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
        df_sector = df_sector.set_index('J-Date')
        df_sector.drop(columns=['Date'],inplace=True)
        # now concat:
        df_sector_cl = pd.concat([df_sector,df_sector_cl],axis=1).dropna()
        df_sector_cl = df_sector_cl[['Date','Weekday','Open','High','Low','Close','Adj Close','Volume']]
        cols = ['Open','High','Low','Close','Adj Close','Volume']
        df_sector_cl[cols] = df_sector_cl[cols].apply(pd.to_numeric, axis=1)
        df_sector_cl['Volume'] = df_sector_cl['Volume'].astype('int64')
    if(not show_weekday):
        df_sector_cl.drop(columns=['Weekday'],inplace=True)
    if(not double_date):
        df_sector_cl.drop(columns=['Date'],inplace=True)
    # slice requested time window:
    if(not ignore_date):
        df_sector_cl = df_sector_cl[start_date:end_date]    
    return df_sector_cl


################################################################################################################################################################################
################################################################################################################################################################################

def index_tepix(start_date='1403-11-01', end_date='1403-11-03', ignore_date = False, just_adj_close = False, show_weekday = False, double_date = False):
    """
    Function Description:
    index_tepix() retrieves the historical price index (TEPIX) data for the given trading days
    between the specified start and end dates. It supports retrieving the full price index history
    without considering the start and end dates, displaying the day of the week, showing only the adjusted close
    values, and using either Jalali or Gregorian dates.

    Parameters:
    start_date (str): The start date for data retrieval in Jalali format ('YYYY-MM-DD').
    end_date (str): The end date for data retrieval in Jalali format ('YYYY-MM-DD').
    ignore_date (bool): If True, ignores the start and end date and retrieves all available data. Defaults to False.
    just_adj_close (bool): If True, only retrieves the adjusted close values. Defaults to False.
    show_weekday (bool): If True, displays the weekday for each date. Defaults to False.
    double_date (bool): If True, includes both Jalali and Gregorian dates in the output. Defaults to False.

    Returns:
    pd.DataFrame: A DataFrame containing the following columns:
        - Date: The date of the index value (either Jalali or Gregorian, based on the `double_date` parameter).
        - Weekday: The weekday name (if `show_weekday` is True).
        - Open: The opening value of the index.
        - High: The highest value of the index.
        - Low: The lowest value of the index.
        - Close: The closing value of the index.
        - Adj Close: The adjusted closing value of the index.
        - Volume: The volume of the transactions.

    Example Usage:
    To retrieve the price index data (TEPIX) between '1403-11-01' and '1403-11-03':
    df = index_tepix(start_date='1403-11-01', end_date='1403-11-03')

    Notes:
    - The function retrieves data from TSETMC APIs for each trading day within the specified date range.
    - The data includes prices, volume, and other financial indicators for the price index.
    - The returned DataFrame is indexed by the Jalali date and contains columns for various financial data.
    - The function handles both Jalali and Gregorian dates, with the option to show weekday names and combine both date formats.
    """

    # check date validity --------------------------------------------------------------------------------------------------------------
    if(not ignore_date):
        start_date = check_date(start_date,key_word="'START'")
        if(start_date==None):
            return
        end_date = check_date(end_date,key_word="'END'")
        if(end_date==None):
            return
        start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
        end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
        if(start>end):
            print('Start date must be a day before end date!')
            return
    # get sector web-id ---------------------------------------------------------------------------------------------------------------------
    sector_web_id = 5798407779416661
    r_cl = requests.get(f'http://cdn.tsetmc.com/api/Index/GetIndexB2History/{sector_web_id}', headers=headers)
    df_sector_cl = pd.DataFrame(r_cl.json()['indexB2'])[['dEven','xNivInuClMresIbs']]
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: str(x))
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: x[:4]+'-'+x[4:6]+'-'+x[-2:])
    df_sector_cl['dEven'] = pd.to_datetime(df_sector_cl['dEven'])
    df_sector_cl.rename(columns={"dEven": "Date", "xNivInuClMresIbs":"Adj Close"}, inplace=True)
    df_sector_cl['J-Date']=df_sector_cl['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
    df_sector_cl['Weekday']=df_sector_cl['Date'].dt.weekday
    df_sector_cl['Weekday'] = df_sector_cl['Weekday'].apply(lambda x: calendar.day_name[x])
    df_sector_cl = df_sector_cl.set_index('J-Date')
    df_sector_cl = df_sector_cl[['Date','Weekday','Adj Close']]
    df_sector_cl['Adj Close'] = pd.to_numeric(df_sector_cl['Adj Close'])
    if(not just_adj_close):
        r = requests.get(f'http://old.tsetmc.com/tsev2/chart/data/IndexFinancial.aspx?i={sector_web_id}&t=ph', headers=headers)
        df_sector = pd.DataFrame(r.text.split(';'))
        columns=['Date','High','Low','Open','Close','Volume','D']
        # split data into defined columns
        df_sector[columns] = df_sector[0].str.split(",",expand=True)
        df_sector.drop(columns=[0,'D'],inplace=True)
        df_sector['Date']=pd.to_datetime(df_sector['Date'])
        df_sector['J-Date']=df_sector['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
        df_sector = df_sector.set_index('J-Date')
        df_sector.drop(columns=['Date'],inplace=True)
        # now concat:
        df_sector_cl = pd.concat([df_sector,df_sector_cl],axis=1).dropna()
        df_sector_cl = df_sector_cl[['Date','Weekday','Open','High','Low','Close','Adj Close','Volume']]
        cols = ['Open','High','Low','Close','Adj Close','Volume']
        df_sector_cl[cols] = df_sector_cl[cols].apply(pd.to_numeric, axis=1)
        df_sector_cl['Volume'] = df_sector_cl['Volume'].astype('int64')
    if(not show_weekday):
        df_sector_cl.drop(columns=['Weekday'],inplace=True)
    if(not double_date):
        df_sector_cl.drop(columns=['Date'],inplace=True)
    # slice requested time window:
    if(not ignore_date):
        df_sector_cl = df_sector_cl[start_date:end_date]    
    return df_sector_cl

################################################################################################################################################################################
################################################################################################################################################################################

def index_tepix_ew(start_date='1403-11-01', end_date='1403-11-03', ignore_date = False, just_adj_close = False, show_weekday = False, double_date = False):
    """
    Function Description:
    index_tepix_ew() retrieves the historical Equal-Weighted Price Index (EWPI) data for the given trading days between the specified start and end dates.
    It supports retrieving the full price index history, displaying weekdays, and showing only the adjusted close values. 
    Additionally, it can display both Jalali and Gregorian dates.

    Parameters:
    start_date (str): The start date for data retrieval in Jalali format ('YYYY-MM-DD').
    end_date (str): The end date for data retrieval in Jalali format ('YYYY-MM-DD').
    ignore_date (bool): If True, ignores the start and end date and retrieves all available data. Defaults to False.
    just_adj_close (bool): If True, only retrieves the adjusted close values. Defaults to False.
    show_weekday (bool): If True, displays the weekday for each date. Defaults to False.
    double_date (bool): If True, includes both Jalali and Gregorian dates in the output. Defaults to False.

    Returns:
    pd.DataFrame: A DataFrame containing the following columns:
        - Date: The date of the index value (either Jalali or Gregorian, based on the `double_date` parameter).
        - Weekday: The weekday name (if `show_weekday` is True).
        - Open: The opening value of the index.
        - High: The highest value of the index.
        - Low: The lowest value of the index.
        - Close: The closing value of the index.
        - Adj Close: The adjusted closing value of the index.
        - Volume: The volume of the transactions.

    Example Usage:
    To retrieve the Equal-Weighted Price Index (EWPI) data between '1395-01-01' and '1400-12-29':
    df = index_tepix_ew(start_date='1395-01-01', end_date='1400-12-29')

    Notes:
    - The function retrieves data from TSETMC APIs for each trading day within the specified date range.
    - The data includes prices, volume, and other financial indicators for the Equal-Weighted Price Index.
    - The returned DataFrame is indexed by the Jalali date and contains columns for various financial data.
    - The function handles both Jalali and Gregorian dates, with the option to show weekday names and combine both date formats.
    """

    # check date validity --------------------------------------------------------------------------------------------------------------
    if(not ignore_date):
        start_date = check_date(start_date,key_word="'START'")
        if(start_date==None):
            return
        end_date = check_date(end_date,key_word="'END'")
        if(end_date==None):
            return
        start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
        end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
        if(start>end):
            print('Start date must be a day before end date!')
            return
    # get sector web-id ---------------------------------------------------------------------------------------------------------------------
    sector_web_id = 8384385859414435
    # get only close chart data for sector index:
    r_cl = requests.get(f'http://tsetmc.com/tsev2/chart/data/Index.aspx?i={sector_web_id}&t=value', headers=headers)
    df_sector_cl = pd.DataFrame(r_cl.text.split(';'))
    columns=['J-Date','Adj Close']
    df_sector_cl[columns] = df_sector_cl[0].str.split(",",expand=True)
    df_sector_cl.drop(columns=[0],inplace=True)
    df_sector_cl['J-Date'] = df_sector_cl['J-Date'].apply(lambda x: str(jdatetime.date(int(x.split('/')[0]),int(x.split('/')[1]),int(x.split('/')[2]))))
    df_sector_cl['Date'] = df_sector_cl['J-Date'].apply(lambda x: jdatetime.date(int(x[:4]),int(x[5:7]),int(x[8:])).togregorian())  
    df_sector_cl['Date'] = pd.to_datetime(df_sector_cl['Date'])
    df_sector_cl['Weekday']=df_sector_cl['Date'].dt.weekday
    df_sector_cl['Weekday'] = df_sector_cl['Weekday'].apply(lambda x: calendar.day_name[x])
    df_sector_cl = df_sector_cl.set_index('J-Date')
    df_sector_cl = df_sector_cl[['Date','Weekday','Adj Close']]
    df_sector_cl['Adj Close'] = pd.to_numeric(df_sector_cl['Adj Close'])
    if(not just_adj_close):
        r = requests.get(f'http://www.tsetmc.com/tsev2/chart/data/IndexFinancial.aspx?i={sector_web_id}&t=ph', headers=headers)
        df_sector = pd.DataFrame(r.text.split(';'))
        columns=['Date','High','Low','Open','Close','Volume','D']
        # split data into defined columns
        df_sector[columns] = df_sector[0].str.split(",",expand=True)
        df_sector.drop(columns=[0,'D'],inplace=True)
        df_sector['Date']=pd.to_datetime(df_sector['Date'])
        df_sector['J-Date']=df_sector['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
        df_sector = df_sector.set_index('J-Date')
        df_sector.drop(columns=['Date'],inplace=True)
        # now concat:
        df_sector_cl = pd.concat([df_sector,df_sector_cl],axis=1).dropna()
        df_sector_cl = df_sector_cl[['Date','Weekday','Open','High','Low','Close','Adj Close','Volume']]
        cols = ['Open','High','Low','Close','Adj Close','Volume']
        df_sector_cl[cols] = df_sector_cl[cols].apply(pd.to_numeric, axis=1)
        df_sector_cl['Volume'] = df_sector_cl['Volume'].astype('int64')
    if(not show_weekday):
        df_sector_cl.drop(columns=['Weekday'],inplace=True)
    if(not double_date):
        df_sector_cl.drop(columns=['Date'],inplace=True)
    # slice requested time window:
    if(not ignore_date):
        df_sector_cl = df_sector_cl[start_date:end_date]    
    return df_sector_cl

################################################################################################################################################################################
################################################################################################################################################################################

def index_tefix(start_date='1403-11-01', end_date='1403-11-03', ignore_date = False, just_adj_close = False, show_weekday = False, double_date = False):
    """
    Function Description:
    index_tefix() retrieves the historical Free-Float Index (FFI) data for the specified trading days between the start and end dates.
    It supports retrieving all available data, displaying weekdays, and showing only the adjusted close values. 
    Additionally, it can provide both Jalali and Gregorian dates.

    Parameters:
    start_date (str): The start date for data retrieval in Jalali format ('YYYY-MM-DD').
    end_date (str): The end date for data retrieval in Jalali format ('YYYY-MM-DD').
    ignore_date (bool): If True, ignores the start and end date and retrieves all available data. Defaults to False.
    just_adj_close (bool): If True, only retrieves the adjusted close values. Defaults to False.
    show_weekday (bool): If True, displays the weekday for each date. Defaults to False.
    double_date (bool): If True, includes both Jalali and Gregorian dates in the output. Defaults to False.

    Returns:
    pd.DataFrame: A DataFrame containing the following columns:
        - Date: The date of the index value (either Jalali or Gregorian, based on the `double_date` parameter).
        - Weekday: The weekday name (if `show_weekday` is True).
        - Open: The opening value of the index.
        - High: The highest value of the index.
        - Low: The lowest value of the index.
        - Close: The closing value of the index.
        - Adj Close: The adjusted closing value of the index.
        - Volume: The volume of the transactions.

    Example Usage:
    To retrieve the Free-Float Index (FFI) data between '1395-01-01' and '1400-12-29':
    df = index_tefix(start_date='1395-01-01', end_date='1400-12-29')

    Notes:
    - The function retrieves data from TSETMC APIs for each trading day within the specified date range.
    - The data includes prices, volume, and other financial indicators for the Free-Float Index.
    - The returned DataFrame is indexed by the Jalali date and contains columns for various financial data.
    - The function handles both Jalali and Gregorian dates, with the option to show weekday names and combine both date formats.
    """

    # check date validity --------------------------------------------------------------------------------------------------------------
    if(not ignore_date):
        start_date = check_date(start_date,key_word="'START'")
        if(start_date==None):
            return
        end_date = check_date(end_date,key_word="'END'")
        if(end_date==None):
            return
        start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
        end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
        if(start>end):
            print('Start date must be a day before end date!')
            return
    # get sector web-id ---------------------------------------------------------------------------------------------------------------------
    sector_web_id = 49579049405614711
    r_cl = requests.get(f'http://cdn.tsetmc.com/api/Index/GetIndexB2History/{sector_web_id}', headers=headers)
    df_sector_cl = pd.DataFrame(r_cl.json()['indexB2'])[['dEven','xNivInuClMresIbs']]
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: str(x))
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: x[:4]+'-'+x[4:6]+'-'+x[-2:])
    df_sector_cl['dEven'] = pd.to_datetime(df_sector_cl['dEven'])
    df_sector_cl.rename(columns={"dEven": "Date", "xNivInuClMresIbs":"Adj Close"}, inplace=True)
    df_sector_cl['J-Date']=df_sector_cl['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
    df_sector_cl['Weekday']=df_sector_cl['Date'].dt.weekday
    df_sector_cl['Weekday'] = df_sector_cl['Weekday'].apply(lambda x: calendar.day_name[x])
    df_sector_cl = df_sector_cl.set_index('J-Date')
    df_sector_cl = df_sector_cl[['Date','Weekday','Adj Close']]
    df_sector_cl['Adj Close'] = pd.to_numeric(df_sector_cl['Adj Close'])
    if(not just_adj_close):
        r = requests.get(f'http://old.tsetmc.com/tsev2/chart/data/IndexFinancial.aspx?i={sector_web_id}&t=ph', headers=headers)
        df_sector = pd.DataFrame(r.text.split(';'))
        columns=['Date','High','Low','Open','Close','Volume','D']
        # split data into defined columns
        df_sector[columns] = df_sector[0].str.split(",",expand=True)
        df_sector.drop(columns=[0,'D'],inplace=True)
        df_sector['Date']=pd.to_datetime(df_sector['Date'])
        df_sector['J-Date']=df_sector['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
        df_sector = df_sector.set_index('J-Date')
        df_sector.drop(columns=['Date'],inplace=True)
        # now concat:
        df_sector_cl = pd.concat([df_sector,df_sector_cl],axis=1).dropna()
        df_sector_cl = df_sector_cl[['Date','Weekday','Open','High','Low','Close','Adj Close','Volume']]
        cols = ['Open','High','Low','Close','Adj Close','Volume']
        df_sector_cl[cols] = df_sector_cl[cols].apply(pd.to_numeric, axis=1)
        df_sector_cl['Volume'] = df_sector_cl['Volume'].astype('int64')
    if(not show_weekday):
        df_sector_cl.drop(columns=['Weekday'],inplace=True)
    if(not double_date):
        df_sector_cl.drop(columns=['Date'],inplace=True)
    # slice requested time window:
    if(not ignore_date):
        df_sector_cl = df_sector_cl[start_date:end_date]    
    return df_sector_cl

################################################################################################################################################################################
################################################################################################################################################################################

def index_market_one(start_date='1403-11-01', end_date='1403-11-03', ignore_date = False, just_adj_close = False, show_weekday = False, double_date = False):
    """
    Function Description:
    index_market_one() retrieves the historical First Market Index data for the specified trading days between the start and end dates.
    It supports retrieving all available data, displaying weekdays, and showing only the adjusted close values.
    Additionally, it can provide both Jalali and Gregorian dates.

    Parameters:
    start_date (str): The start date for data retrieval in Jalali format ('YYYY-MM-DD').
    end_date (str): The end date for data retrieval in Jalali format ('YYYY-MM-DD').
    ignore_date (bool): If True, ignores the start and end date and retrieves all available data. Defaults to False.
    just_adj_close (bool): If True, only retrieves the adjusted close values. Defaults to False.
    show_weekday (bool): If True, displays the weekday for each date. Defaults to False.
    double_date (bool): If True, includes both Jalali and Gregorian dates in the output. Defaults to False.

    Returns:
    pd.DataFrame: A DataFrame containing the following columns:
        - Date: The date of the index value (either Jalali or Gregorian, based on the `double_date` parameter).
        - Weekday: The weekday name (if `show_weekday` is True).
        - Open: The opening value of the index.
        - High: The highest value of the index.
        - Low: The lowest value of the index.
        - Close: The closing value of the index.
        - Adj Close: The adjusted closing value of the index.
        - Volume: The volume of the transactions.

    Example Usage:
    To retrieve the First Market Index data between '1395-01-01' and '1400-12-29':
    df = index_market_one(start_date='1395-01-01', end_date='1400-12-29')

    Notes:
    - The function retrieves data from TSETMC APIs for each trading day within the specified date range.
    - The data includes prices, volume, and other financial indicators for the First Market Index.
    - The returned DataFrame is indexed by the Jalali date and contains columns for various financial data.
    - The function handles both Jalali and Gregorian dates, with the option to show weekday names and combine both date formats.
    """

    # check date validity --------------------------------------------------------------------------------------------------------------
    if(not ignore_date):
        start_date = check_date(start_date,key_word="'START'")
        if(start_date==None):
            return
        end_date = check_date(end_date,key_word="'END'")
        if(end_date==None):
            return
        start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
        end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
        if(start>end):
            print('Start date must be a day before end date!')
            return
    # get sector web-id ---------------------------------------------------------------------------------------------------------------------
    sector_web_id = 62752761908615603
    r_cl = requests.get(f'http://cdn.tsetmc.com/api/Index/GetIndexB2History/{sector_web_id}', headers=headers)
    df_sector_cl = pd.DataFrame(r_cl.json()['indexB2'])[['dEven','xNivInuClMresIbs']]
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: str(x))
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: x[:4]+'-'+x[4:6]+'-'+x[-2:])
    df_sector_cl['dEven'] = pd.to_datetime(df_sector_cl['dEven'])
    df_sector_cl.rename(columns={"dEven": "Date", "xNivInuClMresIbs":"Adj Close"}, inplace=True)
    df_sector_cl['J-Date']=df_sector_cl['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
    df_sector_cl['Weekday']=df_sector_cl['Date'].dt.weekday
    df_sector_cl['Weekday'] = df_sector_cl['Weekday'].apply(lambda x: calendar.day_name[x])
    df_sector_cl = df_sector_cl.set_index('J-Date')
    df_sector_cl = df_sector_cl[['Date','Weekday','Adj Close']]
    df_sector_cl['Adj Close'] = pd.to_numeric(df_sector_cl['Adj Close'])
    if(not just_adj_close):
        r = requests.get(f'http://old.tsetmc.com/tsev2/chart/data/IndexFinancial.aspx?i={sector_web_id}&t=ph', headers=headers)
        df_sector = pd.DataFrame(r.text.split(';'))
        columns=['Date','High','Low','Open','Close','Volume','D']
        # split data into defined columns
        df_sector[columns] = df_sector[0].str.split(",",expand=True)
        df_sector.drop(columns=[0,'D'],inplace=True)
        df_sector['Date']=pd.to_datetime(df_sector['Date'])
        df_sector['J-Date']=df_sector['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
        df_sector = df_sector.set_index('J-Date')
        df_sector.drop(columns=['Date'],inplace=True)
        # now concat:
        df_sector_cl = pd.concat([df_sector,df_sector_cl],axis=1).dropna()
        df_sector_cl = df_sector_cl[['Date','Weekday','Open','High','Low','Close','Adj Close','Volume']]
        cols = ['Open','High','Low','Close','Adj Close','Volume']
        df_sector_cl[cols] = df_sector_cl[cols].apply(pd.to_numeric, axis=1)
        df_sector_cl['Volume'] = df_sector_cl['Volume'].astype('int64')
    if(not show_weekday):
        df_sector_cl.drop(columns=['Weekday'],inplace=True)
    if(not double_date):
        df_sector_cl.drop(columns=['Date'],inplace=True)
    # slice requested time window:
    if(not ignore_date):
        df_sector_cl = df_sector_cl[start_date:end_date]    
    return df_sector_cl

################################################################################################################################################################################
################################################################################################################################################################################

def index_market_two(start_date='1403-11-01', end_date='1403-11-03', ignore_date = False, just_adj_close = False, show_weekday = False, double_date = False):
    """
    Function Description:
    index_market_two() retrieves the historical Second Market Index data for the specified trading days between the start and end dates.
    It supports retrieving all available data, displaying weekdays, and showing only the adjusted close values.
    Additionally, it can provide both Jalali and Gregorian dates.

    Parameters:
    start_date (str): The start date for data retrieval in Jalali format ('YYYY-MM-DD').
    end_date (str): The end date for data retrieval in Jalali format ('YYYY-MM-DD').
    ignore_date (bool): If True, ignores the start and end date and retrieves all available data. Defaults to False.
    just_adj_close (bool): If True, only retrieves the adjusted close values. Defaults to False.
    show_weekday (bool): If True, displays the weekday for each date. Defaults to False.
    double_date (bool): If True, includes both Jalali and Gregorian dates in the output. Defaults to False.

    Returns:
    pd.DataFrame: A DataFrame containing the following columns:
        - Date: The date of the index value (either Jalali or Gregorian, based on the `double_date` parameter).
        - Weekday: The weekday name (if `show_weekday` is True).
        - Open: The opening value of the index.
        - High: The highest value of the index.
        - Low: The lowest value of the index.
        - Close: The closing value of the index.
        - Adj Close: The adjusted closing value of the index.
        - Volume: The volume of the transactions.

    Example Usage:
    To retrieve the Second Market Index data between '1403-11-01' and '1403-11-03':
    df = index_market_two(start_date='1403-11-01', end_date='1403-11-03')

    Notes:
    - The function retrieves data from TSETMC APIs for each trading day within the specified date range.
    - The data includes prices, volume, and other financial indicators for the Second Market Index.
    - The returned DataFrame is indexed by the Jalali date and contains columns for various financial data.
    - The function handles both Jalali and Gregorian dates, with the option to show weekday names and combine both date formats.
    """
    
    # check date validity --------------------------------------------------------------------------------------------------------------
    if(not ignore_date):
        start_date = check_date(start_date,key_word="'START'")
        if(start_date==None):
            return
        end_date = check_date(end_date,key_word="'END'")
        if(end_date==None):
            return
        start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
        end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
        if(start>end):
            print('Start date must be a day before end date!')
            return
    # get sector web-id ---------------------------------------------------------------------------------------------------------------------
    sector_web_id = 71704845530629737
    # get only close chart data for sector index:
    r_cl = requests.get(f'http://cdn.tsetmc.com/api/Index/GetIndexB2History/{sector_web_id}', headers=headers)
    df_sector_cl = pd.DataFrame(r_cl.json()['indexB2'])[['dEven','xNivInuClMresIbs']]
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: str(x))
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: x[:4]+'-'+x[4:6]+'-'+x[-2:])
    df_sector_cl['dEven'] = pd.to_datetime(df_sector_cl['dEven'])
    df_sector_cl.rename(columns={"dEven": "Date", "xNivInuClMresIbs":"Adj Close"}, inplace=True)
    df_sector_cl['J-Date']=df_sector_cl['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
    df_sector_cl['Weekday']=df_sector_cl['Date'].dt.weekday
    df_sector_cl['Weekday'] = df_sector_cl['Weekday'].apply(lambda x: calendar.day_name[x])
    df_sector_cl = df_sector_cl.set_index('J-Date')
    df_sector_cl = df_sector_cl[['Date','Weekday','Adj Close']]
    df_sector_cl['Adj Close'] = pd.to_numeric(df_sector_cl['Adj Close'])
    if(not just_adj_close):
        r = requests.get(f'http://old.tsetmc.com/tsev2/chart/data/IndexFinancial.aspx?i={sector_web_id}&t=ph', headers=headers)
        df_sector = pd.DataFrame(r.text.split(';'))
        columns=['Date','High','Low','Open','Close','Volume','D']
        # split data into defined columns
        df_sector[columns] = df_sector[0].str.split(",",expand=True)
        df_sector.drop(columns=[0,'D'],inplace=True)
        df_sector['Date']=pd.to_datetime(df_sector['Date'])
        df_sector['J-Date']=df_sector['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
        df_sector = df_sector.set_index('J-Date')
        df_sector.drop(columns=['Date'],inplace=True)
        # now concat:
        df_sector_cl = pd.concat([df_sector,df_sector_cl],axis=1).dropna()
        df_sector_cl = df_sector_cl[['Date','Weekday','Open','High','Low','Close','Adj Close','Volume']]
        cols = ['Open','High','Low','Close','Adj Close','Volume']
        df_sector_cl[cols] = df_sector_cl[cols].apply(pd.to_numeric, axis=1)
        df_sector_cl['Volume'] = df_sector_cl['Volume'].astype('int64')
    if(not show_weekday):
        df_sector_cl.drop(columns=['Weekday'],inplace=True)
    if(not double_date):
        df_sector_cl.drop(columns=['Date'],inplace=True)
    # slice requested time window:
    if(not ignore_date):
        df_sector_cl = df_sector_cl[start_date:end_date]    
    return df_sector_cl

################################################################################################################################################################################
################################################################################################################################################################################

def index_industry(start_date='1403-11-01', end_date='1403-11-03', ignore_date = False, just_adj_close = False, show_weekday = False, double_date = False):
    """
    Function Description:
    index_industry() retrieves the historical Industry Index data for the specified trading days between the start and end dates.
    It supports retrieving all available data, displaying weekdays, and showing only the adjusted close values.
    Additionally, it can provide both Jalali and Gregorian dates.

    Parameters:
    start_date (str): The start date for data retrieval in Jalali format ('YYYY-MM-DD').
    end_date (str): The end date for data retrieval in Jalali format ('YYYY-MM-DD').
    ignore_date (bool): If True, ignores the start and end date and retrieves all available data. Defaults to False.
    just_adj_close (bool): If True, only retrieves the adjusted close values. Defaults to False.
    show_weekday (bool): If True, displays the weekday for each date. Defaults to False.
    double_date (bool): If True, includes both Jalali and Gregorian dates in the output. Defaults to False.

    Returns:
    pd.DataFrame: A DataFrame containing the following columns:
        - Date: The date of the index value (either Jalali or Gregorian, based on the `double_date` parameter).
        - Weekday: The weekday name (if `show_weekday` is True).
        - Open: The opening value of the index.
        - High: The highest value of the index.
        - Low: The lowest value of the index.
        - Close: The closing value of the index.
        - Adj Close: The adjusted closing value of the index.
        - Volume: The volume of the transactions.

    Example Usage:
    To retrieve the Industry Index data between '1395-01-01' and '1400-12-29':
    df = index_industry(start_date='1395-01-01', end_date='1400-12-29')

    Notes:
    - The function retrieves data from TSETMC APIs for each trading day within the specified date range.
    - The data includes prices, volume, and other financial indicators for the Industry Index.
    - The returned DataFrame is indexed by the Jalali date and contains columns for various financial data.
    - The function handles both Jalali and Gregorian dates, with the option to show weekday names and combine both date formats.
    """

    # check date validity --------------------------------------------------------------------------------------------------------------
    if(not ignore_date):
        start_date = check_date(start_date,key_word="'START'")
        if(start_date==None):
            return
        end_date = check_date(end_date,key_word="'END'")
        if(end_date==None):
            return
        start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
        end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
        if(start>end):
            print('Start date must be a day before end date!')
            return
    # get sector web-id ---------------------------------------------------------------------------------------------------------------------
    sector_web_id = 43754960038275285
    # get only close chart data for sector index:
    r_cl = requests.get(f'http://cdn.tsetmc.com/api/Index/GetIndexB2History/{sector_web_id}', headers=headers)
    df_sector_cl = pd.DataFrame(r_cl.json()['indexB2'])[['dEven','xNivInuClMresIbs']]
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: str(x))
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: x[:4]+'-'+x[4:6]+'-'+x[-2:])
    df_sector_cl['dEven'] = pd.to_datetime(df_sector_cl['dEven'])
    df_sector_cl.rename(columns={"dEven": "Date", "xNivInuClMresIbs":"Adj Close"}, inplace=True)
    df_sector_cl['J-Date']=df_sector_cl['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
    df_sector_cl['Weekday']=df_sector_cl['Date'].dt.weekday
    df_sector_cl['Weekday'] = df_sector_cl['Weekday'].apply(lambda x: calendar.day_name[x])
    df_sector_cl = df_sector_cl.set_index('J-Date')
    df_sector_cl = df_sector_cl[['Date','Weekday','Adj Close']]
    df_sector_cl['Adj Close'] = pd.to_numeric(df_sector_cl['Adj Close'])
    if(not just_adj_close):
        r = requests.get(f'http://old.tsetmc.com/tsev2/chart/data/IndexFinancial.aspx?i={sector_web_id}&t=ph', headers=headers)
        df_sector = pd.DataFrame(r.text.split(';'))
        columns=['Date','High','Low','Open','Close','Volume','D']
        # split data into defined columns
        df_sector[columns] = df_sector[0].str.split(",",expand=True)
        df_sector.drop(columns=[0,'D'],inplace=True)
        df_sector['Date']=pd.to_datetime(df_sector['Date'])
        df_sector['J-Date']=df_sector['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
        df_sector = df_sector.set_index('J-Date')
        df_sector.drop(columns=['Date'],inplace=True)
        # now concat:
        df_sector_cl = pd.concat([df_sector,df_sector_cl],axis=1).dropna()
        df_sector_cl = df_sector_cl[['Date','Weekday','Open','High','Low','Close','Adj Close','Volume']]
        cols = ['Open','High','Low','Close','Adj Close','Volume']
        df_sector_cl[cols] = df_sector_cl[cols].apply(pd.to_numeric, axis=1)
        df_sector_cl['Volume'] = df_sector_cl['Volume'].astype('int64')
    if(not show_weekday):
        df_sector_cl.drop(columns=['Weekday'],inplace=True)
    if(not double_date):
        df_sector_cl.drop(columns=['Date'],inplace=True)
    # slice requested time window:
    if(not ignore_date):
        df_sector_cl = df_sector_cl[start_date:end_date]    
    return df_sector_cl

################################################################################################################################################################################
################################################################################################################################################################################

def index_thirty_big(start_date='1403-11-01', end_date='1403-11-03', ignore_date = False, just_adj_close = False, show_weekday = False, double_date = False):
    """
    Function Description:
    index_thirty_big() retrieves the historical data for the 30 Large-Cap Index (شاخص 30 شرکت بزرگ بورس تهران) for the specified trading days between the start and end dates.
    The function allows retrieving all available data, displaying weekdays, and showing only the adjusted close values.
    It also supports both Jalali and Gregorian dates.

    Parameters:
    start_date (str): The start date for data retrieval in Jalali format ('YYYY-MM-DD').
    end_date (str): The end date for data retrieval in Jalali format ('YYYY-MM-DD').
    ignore_date (bool): If True, ignores the start and end date and retrieves all available data. Defaults to False.
    just_adj_close (bool): If True, only retrieves the adjusted close values. Defaults to False.
    show_weekday (bool): If True, displays the weekday for each date. Defaults to False.
    double_date (bool): If True, includes both Jalali and Gregorian dates in the output. Defaults to False.

    Returns:
    pd.DataFrame: A DataFrame containing the following columns:
        - Date: The date of the index value (either Jalali or Gregorian, based on the `double_date` parameter).
        - Weekday: The weekday name (if `show_weekday` is True).
        - Open: The opening value of the index.
        - High: The highest value of the index.
        - Low: The lowest value of the index.
        - Close: The closing value of the index.
        - Adj Close: The adjusted closing value of the index.
        - Volume: The volume of the transactions.

    Example Usage:
    To retrieve the 30 Large-Cap Index data between '1395-01-01' and '1400-12-29':
    df = index_thirty_big(start_date='1395-01-01', end_date='1400-12-29')

    Notes:
    - The function retrieves data from TSETMC APIs for each trading day within the specified date range.
    - The data includes prices, volume, and other financial indicators for the 30 Large-Cap Index.
    - The returned DataFrame is indexed by the Jalali date and contains columns for various financial data.
    - The function handles both Jalali and Gregorian dates, with the option to show weekday names and combine both date formats.
    """

    # check date validity --------------------------------------------------------------------------------------------------------------
    if(not ignore_date):
        start_date = check_date(start_date,key_word="'START'")
        if(start_date==None):
            return
        end_date = check_date(end_date,key_word="'END'")
        if(end_date==None):
            return
        start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
        end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
        if(start>end):
            print('Start date must be a day before end date!')
            return
    # get sector web-id ---------------------------------------------------------------------------------------------------------------------
    sector_web_id = 10523825119011581
    # get only close chart data for sector index:
    r_cl = requests.get(f'http://cdn.tsetmc.com/api/Index/GetIndexB2History/{sector_web_id}', headers=headers)
    df_sector_cl = pd.DataFrame(r_cl.json()['indexB2'])[['dEven','xNivInuClMresIbs']]
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: str(x))
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: x[:4]+'-'+x[4:6]+'-'+x[-2:])
    df_sector_cl['dEven'] = pd.to_datetime(df_sector_cl['dEven'])
    df_sector_cl.rename(columns={"dEven": "Date", "xNivInuClMresIbs":"Adj Close"}, inplace=True)
    df_sector_cl['J-Date']=df_sector_cl['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
    df_sector_cl['Weekday']=df_sector_cl['Date'].dt.weekday
    df_sector_cl['Weekday'] = df_sector_cl['Weekday'].apply(lambda x: calendar.day_name[x])
    df_sector_cl = df_sector_cl.set_index('J-Date')
    df_sector_cl = df_sector_cl[['Date','Weekday','Adj Close']]
    df_sector_cl['Adj Close'] = pd.to_numeric(df_sector_cl['Adj Close'])
    if(not just_adj_close):
        r = requests.get(f'http://old.tsetmc.com/tsev2/chart/data/IndexFinancial.aspx?i={sector_web_id}&t=ph', headers=headers)
        df_sector = pd.DataFrame(r.text.split(';'))
        columns=['Date','High','Low','Open','Close','Volume','D']
        # split data into defined columns
        df_sector[columns] = df_sector[0].str.split(",",expand=True)
        df_sector.drop(columns=[0,'D'],inplace=True)
        df_sector['Date']=pd.to_datetime(df_sector['Date'])
        df_sector['J-Date']=df_sector['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
        df_sector = df_sector.set_index('J-Date')
        df_sector.drop(columns=['Date'],inplace=True)
        # now concat:
        df_sector_cl = pd.concat([df_sector,df_sector_cl],axis=1).dropna()
        df_sector_cl = df_sector_cl[['Date','Weekday','Open','High','Low','Close','Adj Close','Volume']]
        cols = ['Open','High','Low','Close','Adj Close','Volume']
        df_sector_cl[cols] = df_sector_cl[cols].apply(pd.to_numeric, axis=1)
        df_sector_cl['Volume'] = df_sector_cl['Volume'].astype('int64')
    if(not show_weekday):
        df_sector_cl.drop(columns=['Weekday'],inplace=True)
    if(not double_date):
        df_sector_cl.drop(columns=['Date'],inplace=True)
    # slice requested time window:
    if(not ignore_date):
        df_sector_cl = df_sector_cl[start_date:end_date]    
    return df_sector_cl

################################################################################################################################################################################
################################################################################################################################################################################

def index_fifty_big(start_date='1403-11-01', end_date='1403-11-03', ignore_date = False, just_adj_close = False, show_weekday = False, double_date = False):
    """
    Function Description:
    index_fifty_big() retrieves the historical data for the 50 Most Active Stocks Index (شاخص 50 شرکت فعال بورس) for the specified trading days between the start and end dates.
    The function allows retrieving all available data, displaying weekdays, and showing only the adjusted close values.
    It also supports both Jalali and Gregorian dates.

    Parameters:
    start_date (str): The start date for data retrieval in Jalali format ('YYYY-MM-DD').
    end_date (str): The end date for data retrieval in Jalali format ('YYYY-MM-DD').
    ignore_date (bool): If True, ignores the start and end date and retrieves all available data. Defaults to False.
    just_adj_close (bool): If True, only retrieves the adjusted close values. Defaults to False.
    show_weekday (bool): If True, displays the weekday for each date. Defaults to False.
    double_date (bool): If True, includes both Jalali and Gregorian dates in the output. Defaults to False.

    Returns:
    pd.DataFrame: A DataFrame containing the following columns:
        - Date: The date of the index value (either Jalali or Gregorian, based on the `double_date` parameter).
        - Weekday: The weekday name (if `show_weekday` is True).
        - Open: The opening value of the index.
        - High: The highest value of the index.
        - Low: The lowest value of the index.
        - Close: The closing value of the index.
        - Adj Close: The adjusted closing value of the index.
        - Volume: The volume of the transactions.

    Example Usage:
    To retrieve the 50 Most Active Stocks Index data between '1403-11-01' and '1403-11-03':
    df = index_fifty_big(start_date='1403-11-01', end_date='1403-11-03')

    Notes:
    - The function retrieves data from TSETMC APIs for each trading day within the specified date range.
    - The data includes prices, volume, and other financial indicators for the 50 Most Active Stocks Index.
    - The returned DataFrame is indexed by the Jalali date and contains columns for various financial data.
    - The function handles both Jalali and Gregorian dates, with the option to show weekday names and combine both date formats.
    """

    # check date validity --------------------------------------------------------------------------------------------------------------
    if(not ignore_date):
        start_date = check_date(start_date,key_word="'START'")
        if(start_date==None):
            return
        end_date = check_date(end_date,key_word="'END'")
        if(end_date==None):
            return
        start = jdatetime.date(year=int(start_date.split('-')[0]), month=int(start_date.split('-')[1]), day=int(start_date.split('-')[2]))
        end = jdatetime.date(year=int(end_date.split('-')[0]), month=int(end_date.split('-')[1]), day=int(end_date.split('-')[2]))
        if(start>end):
            print('Start date must be a day before end date!')
            return
    # get sector web-id ---------------------------------------------------------------------------------------------------------------------
    sector_web_id = 46342955726788357
    # get only close chart data for sector index:
    r_cl = requests.get(f'http://cdn.tsetmc.com/api/Index/GetIndexB2History/{sector_web_id}', headers=headers)
    df_sector_cl = pd.DataFrame(r_cl.json()['indexB2'])[['dEven','xNivInuClMresIbs']]
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: str(x))
    df_sector_cl['dEven'] = df_sector_cl['dEven'].apply(lambda x: x[:4]+'-'+x[4:6]+'-'+x[-2:])
    df_sector_cl['dEven'] = pd.to_datetime(df_sector_cl['dEven'])
    df_sector_cl.rename(columns={"dEven": "Date", "xNivInuClMresIbs":"Adj Close"}, inplace=True)
    df_sector_cl['J-Date']=df_sector_cl['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
    df_sector_cl['Weekday']=df_sector_cl['Date'].dt.weekday
    df_sector_cl['Weekday'] = df_sector_cl['Weekday'].apply(lambda x: calendar.day_name[x])
    df_sector_cl = df_sector_cl.set_index('J-Date')
    df_sector_cl = df_sector_cl[['Date','Weekday','Adj Close']]
    df_sector_cl['Adj Close'] = pd.to_numeric(df_sector_cl['Adj Close'])
    if(not just_adj_close):
        r = requests.get(f'http://old.tsetmc.com/tsev2/chart/data/IndexFinancial.aspx?i={sector_web_id}&t=ph', headers=headers)
        df_sector = pd.DataFrame(r.text.split(';'))
        columns=['Date','High','Low','Open','Close','Volume','D']
        # split data into defined columns
        df_sector[columns] = df_sector[0].str.split(",",expand=True)
        df_sector.drop(columns=[0,'D'],inplace=True)
        df_sector['Date']=pd.to_datetime(df_sector['Date'])
        df_sector['J-Date']=df_sector['Date'].apply(lambda x: str(jdatetime.date.fromgregorian(date=x.date())))
        df_sector = df_sector.set_index('J-Date')
        df_sector.drop(columns=['Date'],inplace=True)
        # now concat:
        df_sector_cl = pd.concat([df_sector,df_sector_cl],axis=1).dropna()
        df_sector_cl = df_sector_cl[['Date','Weekday','Open','High','Low','Close','Adj Close','Volume']]
        cols = ['Open','High','Low','Close','Adj Close','Volume']
        df_sector_cl[cols] = df_sector_cl[cols].apply(pd.to_numeric, axis=1)
        df_sector_cl['Volume'] = df_sector_cl['Volume'].astype('int64')
    if(not show_weekday):
        df_sector_cl.drop(columns=['Weekday'],inplace=True)
    if(not double_date):
        df_sector_cl.drop(columns=['Date'],inplace=True)
    # slice requested time window:
    if(not ignore_date):
        df_sector_cl = df_sector_cl[start_date:end_date]    
    return df_sector_cl

################################################################################################################################################################################
################################################################################################################################################################################
def marketwatch_file(save_excel = True, save_path = 'C:/Users/Asus/OneDrive/Documents/GitHub'):
    """
    Function Description:
    marketwatch_file() retrieves and processes real-time market data, including retail and institutional transactions,
    stock prices, order book depth, and more, from the Tehran Stock Exchange. It aggregates this data, calculates additional metrics 
    such as trade types and market capitalization, and optionally saves the result as Excel files.

    Parameters:
    save_excel (bool): If True, the function saves the processed data as Excel files. Default is True.
    save_path (str): The directory path where the Excel files will be saved. Default is 'C:/Users/Asus/OneDrive/Documents/GitHub'.

    Returns:
    pd.DataFrame: 
        - final_df: A DataFrame containing comprehensive market data including prices, volumes, trade types, etc.
        - final_OB_df: A DataFrame containing order book data, including buy and sell volumes and prices.

    Example Usage:
    To retrieve the market watch data and save it as Excel files:
    final_df, final_OB_df = marketwatch_file(save_excel=True, save_path='C:/Your/Path')

    Notes:
    - The function retrieves data from multiple TSETMC APIs for real-time stock prices, volumes, retail and institutional transactions, 
      order book data, etc.
    - It calculates several new columns such as percentage changes in stock prices and market cap, and organizes the data in a 
      well-structured format.
    - The function also assigns trade types (e.g., 'tablo', 'block', etc.) based on ticker information.
    - If `save_excel` is set to True, the function saves the final DataFrames to Excel files in the specified path.
    - If the `save_path` directory doesn't exist, an error will be raised. 
    """

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # GET MARKET RETAIL AND INSTITUTIONAL DATA
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    r = requests.get('http://old.tsetmc.com/tsev2/data/ClientTypeAll.aspx', headers=headers)
    Mkt_RI_df = pd.DataFrame(r.text.split(';'))
    Mkt_RI_df = Mkt_RI_df[0].str.split(",",expand=True)
    # assign names to columns:
    Mkt_RI_df.columns = ['webid','No_Buy_R','No_Buy_I','Vol_Buy_R','Vol_Buy_I','No_Sell_R','No_Sell_I','Vol_Sell_R','Vol_Sell_I']
    # convert columns to numeric type:
    cols = ['No_Buy_R','No_Buy_I','Vol_Buy_R','Vol_Buy_I','No_Sell_R','No_Sell_I','Vol_Sell_R','Vol_Sell_I']
    Mkt_RI_df[cols] = Mkt_RI_df[cols].apply(pd.to_numeric, axis=1)
    Mkt_RI_df['webid'] = Mkt_RI_df['webid'].apply(lambda x: x.strip())
    Mkt_RI_df = Mkt_RI_df.set_index('webid')
    # re-arrange the order of columns:
    Mkt_RI_df = Mkt_RI_df[['No_Buy_R','No_Buy_I','No_Sell_R','No_Sell_I','Vol_Buy_R','Vol_Buy_I','Vol_Sell_R','Vol_Sell_I']]
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # GET MARKET WATCH PRICE AND OB DATA
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    r = requests.get('http://old.tsetmc.com/tsev2/data/MarketWatchPlus.aspx', headers=headers)
    main_text = r.text
    Mkt_df = pd.DataFrame((main_text.split('@')[2]).split(';'))
    Mkt_df = Mkt_df[0].str.split(",",expand=True)
    Mkt_df = Mkt_df.iloc[:,:23]
    Mkt_df.columns = ['webid','Ticker-Code','Ticker','Name','Time','Open','Final','Close','No','Volume','Value',
                      'Low','High','Y-Final','EPS','Base-Vol','Unknown1','Unknown2','Sector','Day_UL','Day_LL','Share-No','Mkt-ID']
    # re-arrange columns and drop some columns:
    Mkt_df = Mkt_df[['webid','Ticker','Name','Time','Open','Final','Close','No','Volume','Value',
                      'Low','High','Y-Final','EPS','Base-Vol','Sector','Day_UL','Day_LL','Share-No','Mkt-ID']]
    # Just keep: 300 Bourse, 303 Fara-Bourse, 305 Sandoogh, 309 Payeh, 400 H-Bourse, 403 H-FaraBourse, 404 H-Payeh
    Mkt_ID_list = ['300','303','305','309','400','403','404']
    Mkt_df = Mkt_df[Mkt_df['Mkt-ID'].isin(Mkt_ID_list)]
    Mkt_df['Market'] = Mkt_df['Mkt-ID'].map({'300':'بورس','303':'فرابورس','305':'صندوق قابل معامله','309':'پایه','400':'حق تقدم بورس','403':'حق تقدم فرابورس','404':'حق تقدم پایه'})
    Mkt_df.drop(columns=['Mkt-ID'],inplace=True)   # we do not need Mkt-ID column anymore
    # assign sector names:
    r = requests.get('https://cdn.tsetmc.com/api/StaticData/GetStaticData', headers=headers)
    sec_df = pd.DataFrame(r.json()['staticData'])
    sec_df['code'] = (sec_df['code'].astype(str).apply(lambda x: '0' + x if len(x) == 1 else x))
    sec_df['Name'] = (sec_df['Name'].apply(lambda x: re.sub(r'\u200c', '', x)).str.strip().apply(characters.ar_to_fa))
    sec_df = sec_df[sec_df['type'] == 'IndustrialGroup'][['code', 'Name']]
    Mkt_df['Sector'] = Mkt_df['Sector'].map(dict(sec_df[['code', 'Name']].values))
    # r = requests.get('http://old.tsetmc.com/Loader.aspx?ParTree=111C1213', headers=headers)
    # sectro_lookup = (pd.read_html(r.text)[0]).iloc[1:,:]
    # # convert from Arabic to Farsi and remove half-space
    # sectro_lookup[1] = sectro_lookup[1].apply(lambda x: (str(x).replace('ي','ی')).replace('ك','ک'))
    # sectro_lookup[1] = sectro_lookup[1].apply(lambda x: x.replace('\u200c',' '))
    # sectro_lookup[1] = sectro_lookup[1].apply(lambda x: x.strip())
    # Mkt_df['Sector'] = Mkt_df['Sector'].map(dict(sectro_lookup[[0, 1]].values))
    # modify format of columns:
    cols = ['Open','Final','Close','No','Volume','Value','Low','High','Y-Final','EPS','Base-Vol','Day_UL','Day_LL','Share-No']
    Mkt_df[cols] = Mkt_df[cols].apply(pd.to_numeric, axis=1)
    Mkt_df['Time'] = Mkt_df['Time'].apply(lambda x: x[:-4]+':'+x[-4:-2]+':'+x[-2:])
    Mkt_df['Ticker'] = Mkt_df['Ticker'].apply(lambda x: (str(x).replace('ي','ی')).replace('ك','ک'))
    Mkt_df['Name'] = Mkt_df['Name'].apply(lambda x: (str(x).replace('ي','ی')).replace('ك','ک'))
    Mkt_df['Name'] = Mkt_df['Name'].apply(lambda x: x.replace('\u200c',' '))
    #calculate some new columns
    Mkt_df['Close(%)'] = round((Mkt_df['Close']-Mkt_df['Y-Final'])/Mkt_df['Y-Final']*100,2)
    Mkt_df['Final(%)'] = round((Mkt_df['Final']-Mkt_df['Y-Final'])/Mkt_df['Y-Final']*100,2)
    Mkt_df['Market Cap'] = round(Mkt_df['Share-No']*Mkt_df['Final'],2)
    # set index
    Mkt_df['webid'] = Mkt_df['webid'].apply(lambda x: x.strip())
    Mkt_df = Mkt_df.set_index('webid')
    #------------------------------------------------------------------------------------------------------------------------------------------
    # reading OB (order book) and cleaning the data
    OB_df = pd.DataFrame((main_text.split('@')[3]).split(';'))
    OB_df = OB_df[0].str.split(",",expand=True)
    OB_df.columns = ['webid','OB-Depth','Sell-No','Buy-No','Buy-Price','Sell-Price','Buy-Vol','Sell-Vol']
    OB_df = OB_df[['webid','OB-Depth','Sell-No','Sell-Vol','Sell-Price','Buy-Price','Buy-Vol','Buy-No']]
    # extract top row of order book = OB1
    OB1_df = (OB_df[OB_df['OB-Depth']=='1']).copy()         # just keep top row of OB
    OB1_df.drop(columns=['OB-Depth'],inplace=True)          # we do not need this column anymore
    # set webid as index for future joining operations:
    OB1_df['webid'] = OB1_df['webid'].apply(lambda x: x.strip())
    OB1_df = OB1_df.set_index('webid')
    # convert columns to numeric format:
    cols = ['Sell-No','Sell-Vol','Sell-Price','Buy-Price','Buy-Vol','Buy-No']
    OB1_df[cols] = OB1_df[cols].apply(pd.to_numeric, axis=1)
    # join OB1_df to Mkt_df
    Mkt_df = Mkt_df.join(OB1_df)
    # calculate buy/sell queue value
    bq_value = Mkt_df.apply(lambda x: int(x['Buy-Vol']*x['Buy-Price']) if(x['Buy-Price']==x['Day_UL']) else 0 ,axis = 1)
    sq_value = Mkt_df.apply(lambda x: int(x['Sell-Vol']*x['Sell-Price']) if(x['Sell-Price']==x['Day_LL']) else 0 ,axis = 1)
    Mkt_df = pd.concat([Mkt_df,pd.DataFrame(bq_value,columns=['BQ-Value']),pd.DataFrame(sq_value,columns=['SQ-Value'])],axis=1)
    # calculate buy/sell queue average per-capita:
    bq_pc_avg = Mkt_df.apply(lambda x: int(round(x['BQ-Value']/x['Buy-No'],0)) if((x['BQ-Value']!=0) and (x['Buy-No']!=0)) else 0 ,axis = 1)
    sq_pc_avg = Mkt_df.apply(lambda x: int(round(x['SQ-Value']/x['Sell-No'],0)) if((x['SQ-Value']!=0) and (x['Sell-No']!=0)) else 0 ,axis = 1)
    Mkt_df = pd.concat([Mkt_df,pd.DataFrame(bq_pc_avg,columns=['BQPC']),pd.DataFrame(sq_pc_avg,columns=['SQPC'])],axis=1)
    # just keep tickers with Value grater than zero! = traded stocks:
    #Mkt_df = Mkt_df[Mkt_df['Value']!=0]
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # JOIN DATA
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    final_df = Mkt_df.join(Mkt_RI_df)
    # add trade types:
    final_df['Trade Type'] = pd.DataFrame(final_df['Ticker'].apply(lambda x: 'تابلو' if((not x[-1].isdigit())or(x in ['انرژی1','انرژی2','انرژی3'])) 
                                                                   else ('بلوکی' if(x[-1]=='2') else ('عمده' if(x[-1]=='4') else ('جبرانی' if(x[-1]=='3') else 'تابلو')))))
    # add update Jalali date and time:
    jdatetime_download = jdatetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    final_df['Download'] = jdatetime_download
    # just keep necessary columns and re-arrange theor order:
    final_df = final_df[['Ticker','Trade Type','Time','Open','High','Low','Close','Final','Close(%)','Final(%)',
                         'Day_UL', 'Day_LL','Value','BQ-Value', 'SQ-Value', 'BQPC', 'SQPC',
                         'Volume','Vol_Buy_R', 'Vol_Buy_I', 'Vol_Sell_R', 'Vol_Sell_I','No','No_Buy_R', 'No_Buy_I', 'No_Sell_R', 'No_Sell_I',
                         'Name','Market','Sector','Share-No','Base-Vol','Market Cap','EPS','Download']]
    final_df = final_df.set_index('Ticker')
    # convert columns to int64 data type:
    """cols = ['Open','High','Low','Close','Final','Day_UL', 'Day_LL','Value', 'BQ-Value', 'SQ-Value', 'BQPC', 'SQPC',
            'Volume','Vol_Buy_R', 'Vol_Buy_I', 'Vol_Sell_R', 'Vol_Sell_I','No','No_Buy_R', 'No_Buy_I', 'No_Sell_R', 'No_Sell_I',
            'Share-No','Base-Vol','Market Cap']
    final_df[cols] = final_df[cols].astype('int64')"""
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # PROCESS ORDER BOOK DATA IF REQUESTED
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    final_OB_df = ((Mkt_df[['Ticker','Day_LL','Day_UL']]).join(OB_df.set_index('webid')))
    # convert columns to numeric int64
    cols = ['Day_LL','Day_UL','OB-Depth','Sell-No','Sell-Vol','Sell-Price','Buy-Price','Buy-Vol','Buy-No']
    final_OB_df[cols] = final_OB_df[cols].astype('int64')
    # sort using tickers and order book depth:
    final_OB_df = final_OB_df.sort_values(['Ticker','OB-Depth'], ascending = (True, True))
    final_OB_df = final_OB_df.set_index(['Ticker','Day_LL','Day_UL','OB-Depth'])
    # add Jalali date and time:
    final_OB_df['Download'] =jdatetime_download
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # SAVE OPTIONS AND RETURNS
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if(save_excel):
        try:
            if(save_path[-1] != '/'):
                save_path = save_path+'/'
            mkt_watch_file_name = 'MarketWatch '+jdatetime.datetime.today().strftime("%Y-%m-%d %H-%M-%S")
            OB_file_name = 'OrderBook '+jdatetime.datetime.today().strftime("%Y-%m-%d %H-%M-%S")
            final_OB_df.to_excel(save_path+OB_file_name+'.xlsx')
            final_df.to_excel(save_path+mkt_watch_file_name+'.xlsx')
        except:
            print('Save path does not exist, you can handle saving this data by returned dataframe as Excel using ".to_excel()", if you will!')  
    return final_df, final_OB_df
################################################################################################################################################################################
################################################################################################################################################################################
def save_list(df_data, bourse, farabourse, payeh, detailed_list, save_excel, save_csv, save_path = 'C:/Users/Asus/OneDrive/Documents/GitHub'):
    # find today's j-date ti use in Name of the file
    today_j_date = jdatetime.datetime.now().strftime("%Y-%m-%d")
    # select Name:
    if(bourse):
        if(farabourse):
            if(payeh):
                if(detailed_list):
                    Name = today_j_date+' detailed_stocklist_bfp'
                else:
                    Name = today_j_date+' stocklist_bfp'
            else:
                if(detailed_list):
                    Name = today_j_date+' detailed_stocklist_bf'
                else:
                    Name = today_j_date+' stocklist_bf'
        else:
            if(payeh):
                if(detailed_list):
                    Name = today_j_date+' detailed_stocklist_bp'
                else:
                    Name = today_j_date+' stocklist_bp'
            else:
                if(detailed_list):
                    Name = today_j_date+' detailed_stocklist_b'
                else:
                    Name = today_j_date+' stocklist_b'
    else:
        if(farabourse):
            if(payeh):
                if(detailed_list):
                    Name = today_j_date+' detailed_stocklist_fp'
                else:
                    Name = today_j_date+' stocklist_fp'
            else:
                if(detailed_list):
                    Name = today_j_date+' detailed_stocklist_f'
                else:
                    Name = today_j_date+' stocklist_f'
        else:
            if(payeh):
                if(detailed_list):
                    Name = today_j_date+' detailed_stocklist_p'
                else:
                    Name = today_j_date+' stocklist_p'
            else:
                Name = None
    #------------------------------------------------
    # modify save path if necessary:
    if(save_path[-1] != '/'):
        save_path = save_path+'/'
    # save Excel file:
    if(save_excel):
        try:
            df_data.to_excel(save_path+Name+'.xlsx')
            print('File saved in the specificed directory as: ',Name+'.xlsx')
        except:
            print('Save path does not exist, you can handle saving this data by returned dataframe as Excel using ".to_excel()", if you will!')  
    # save Excel file:
    if(save_csv):
        try:
            df_data.to_csv(save_path+Name+'.csv')
            print('File saved in the specificed directory as: ',Name+'.csv')
        except:
            print('Save path does not exist, you can handle saving this data by returned dataframe as CSV using ".to_csv()", if you will!') 
    return


def stocklist(bourse = True, farabourse = True, payeh = True, detailed_list = True, show_progress = True, save_excel = True, save_csv = True, save_path = 'C:/Users/Asus/OneDrive/Documents/GitHub'):
    """
    Function Description:
    stocklist() retrieves and compiles stock lists from the Tehran Stock Exchange, Fara-Bourse, and Payeh markets, 
    and optionally gathers detailed stock data. The function can save the data to Excel or CSV files and allows for 
    customization of the markets and data details to include.

    Parameters:
    bourse (bool): If True, retrieves the stock list from the Tehran Stock Exchange. Default is True.
    farabourse (bool): If True, retrieves the stock list from the Fara-Bourse. Default is True.
    payeh (bool): If True, retrieves the stock list from the Payeh market. Default is True.
    detailed_list (bool): If True, retrieves detailed data for stocks. Default is True.
    show_progress (bool): If True, shows progress during the data retrieval process. Default is True.
    save_excel (bool): If True, saves the stock list as an Excel file. Default is True.
    save_csv (bool): If True, saves the stock list as a CSV file. Default is True.
    save_path (str): The directory path to save the Excel or CSV files. Default is 'C:/Users/Asus/OneDrive/Documents/GitHub'.

    Returns:
    pd.DataFrame: 
        - look_up: A DataFrame containing basic stock information including tickers, names, markets, and web IDs.
        - df_final: A DataFrame containing detailed stock information, if `detailed_list` is True.

    Example Usage:
    To retrieve the stock list and save it as both Excel and CSV files:
    stocklist(bourse=True, farabourse=True, payeh=True, detailed_list=True, save_excel=True, save_csv=True, save_path='C:/Your/Path')

    Notes:
    - The function retrieves stock information from multiple sources, including the Tehran Stock Exchange (TSE), 
      Fara-Bourse, and Payeh markets.
    - It handles the retrieval of basic stock data as well as more detailed stock data, including sectors, sub-sectors, and other attributes.
    - The function supports saving the retrieved data to both Excel and CSV formats.
    - If `show_progress` is set to True, progress updates will be shown during the execution.
    - Data retrieval from external websites can take time, especially when gathering detailed stock data, so the execution 
      time may vary based on the number of stocks processed.
    """
    
    if(not bourse and not farabourse and not payeh):
        print('Choose at least one market!')
        return
    start_time = time.time()
    http = urllib3.PoolManager()
    look_up = pd.DataFrame({'Ticker':[],'Name':[],'webid':[],'Market':[]})
    # --------------------------------------------------------------------------------------------------
    if(bourse):
        if(show_progress):
            clear_output(wait=True)
            print('Gathering Bourse market stock list ...')
        r = http.request('GET', "http://old.tsetmc.com/Loader.aspx?ParTree=15131J&i=32097828799138957") 
        soup = BeautifulSoup(r.data.decode('utf-8'), 'html.parser')
        table = soup.findAll("table", {"class": "table1"})
        stock_list = table[0].find_all('a')
        Ticker = []
        web_id = []
        Name = []
        for stock in stock_list:
            Ticker.append(stock.text)
            Name.append(stock.attrs["title"])
            web_id.append(stock.attrs["href"].split("&i=")[1])
        bourse_lookup = pd.DataFrame({'Ticker':Ticker, 'Name':Name,'webid':web_id}) 
        bourse_lookup['Market'] = 'بورس'
        look_up = pd.concat([look_up,bourse_lookup],axis=0)
    # --------------------------------------------------------------------------------------------------
    if(farabourse):
        if(show_progress):
            clear_output(wait=True)
            print('Gathering Fara-Bourse market stock list ...')
        r = http.request('GET', 'http://old.tsetmc.com/Loader.aspx?ParTree=15131J&i=43685683301327984') 
        soup = BeautifulSoup(r.data.decode('utf-8'), 'html.parser')
        table = soup.findAll("table", {"class": "table1"})
        stock_list = table[0].find_all('a')
        Ticker = []
        web_id = []
        Name = []
        for stock in stock_list:
            Ticker.append(stock.text)
            Name.append(stock.attrs["title"])
            web_id.append(stock.attrs["href"].split("&i=")[1])
        farabourse_lookup = pd.DataFrame({'Ticker':Ticker, 'Name':Name,'webid':web_id}) 
        farabourse_lookup['Market'] = 'فرابورس'
        look_up = pd.concat([look_up,farabourse_lookup],axis=0)
    # --------------------------------------------------------------------------------------------------
    if(payeh):
        if(show_progress):
            clear_output(wait=True)
            print('Gathering Payeh market stock list ...')
        url = "https://www.ifb.ir/StockQoute.aspx"
        header = {"__EVENTTARGET": "exportbtn"}
        response = requests.post(url, header, verify=False)
        table = pd.read_html(response.content.decode('utf-8'))[0]
        payeh_lookup = table.iloc[2:,:3]
        payeh_lookup.columns = ['Ticker','Name','Market']
        payeh_lookup = payeh_lookup[payeh_lookup['Market'].isin(['تابلو پایه زرد','تابلو پایه نارنجی','تابلو پایه قرمز'])] 
        payeh_lookup['Market'] = payeh_lookup['Market'].apply(lambda x: (x.replace('تابلو','')).strip())
        # drop other than normal trades:
        payeh_lookup = payeh_lookup[payeh_lookup['Ticker'].apply(lambda x: x[-1].isdigit())==False]
        # drop hagh-taghaddom!
        payeh_lookup = payeh_lookup[payeh_lookup['Ticker'].apply(lambda x: x.strip()[-1]!='ح')]
        look_up = pd.concat([look_up,payeh_lookup],axis=0)
    # ---------------------------------------------------------------------------------------------------
    if(not detailed_list):
        # convert tickers and names to farsi characters 
        look_up['Ticker'] = look_up['Ticker'].apply(lambda x: (str(x).replace('ي','ی')).replace('ك','ک'))
        look_up['Name'] = look_up['Name'].apply(lambda x: (str(x).replace('ي','ی')).replace('ك','ک'))
        look_up['Name'] = look_up['Name'].apply(lambda x: x.replace('\u200c',' '))
        look_up = look_up.set_index('Ticker')
        look_up.drop(columns=['webid'],inplace=True)
        if(show_progress):
            clear_output(wait=True) 
        # save file if necessary
        if(save_excel|save_csv):
            save_list(df_data=look_up, bourse=bourse, farabourse=bourse, payeh=payeh, detailed_list=detailed_list,save_excel=save_excel, save_csv=save_csv, save_path=save_path)
        return look_up
    else:
        if(show_progress):
            clear_output(wait=True)
            print('Searching Payeh market stocks web-pages ...')
        # rearrange columns
        look_up['Ticker'] = look_up['Ticker'].apply(lambda x: (str(x).replace('ي','ی')).replace('ك','ک'))
        look_up['Ticker'] = look_up['Ticker'].apply(lambda x: x.replace('\u200c',' '))
        look_up['Name'] = look_up['Name'].apply(lambda x: (str(x).replace('ي','ی')).replace('ك','ک'))
        look_up['Name'] = look_up['Name'].apply(lambda x: x.replace('\u200c',' '))
        look_up = look_up.set_index('Ticker')
        look_up = look_up[['Name','Market','webid']]
        if(payeh):
            # some minor changes in payeh_lookup
            payeh_lookup['Ticker'] = payeh_lookup['Ticker'].apply(lambda x: characters.ar_to_fa(x))
            payeh_lookup = payeh_lookup.set_index('Ticker')
            # look for payeh market web-ids from market watch
            r = requests.get('http://old.tsetmc.com/tsev2/data/MarketWatchPlus.aspx', headers=headers)
            mkt_watch = pd.DataFrame((r.text.split('@')[2]).split(';'))
            mkt_watch = mkt_watch[0].str.split(",",expand=True)
            mkt_watch = mkt_watch[[0,2]]
            mkt_watch.columns = ['webid','Ticker']
            mkt_watch['Ticker'] = mkt_watch['Ticker'].apply(lambda x: characters.ar_to_fa(x))
            mkt_watch = mkt_watch.set_index('Ticker')
            # join based on payeh_lookup
            payeh_lookup = payeh_lookup.join(mkt_watch)
            with_web_id = (payeh_lookup[payeh_lookup['webid'].notnull()]).copy()
            no_web_id = (payeh_lookup[payeh_lookup['webid'].isnull()]).copy()
            no_web_id.drop(columns=['webid'],inplace=True)
            # search from google for no web-id stocks:
            web_id = []
            no_stocks = len(no_web_id)
            counter = 1
            for index, row in no_web_id.iterrows():
                if(show_progress):
                    clear_output(wait=True)
                    print('Searching Payeh market stocks web-pages: ', f'{round((counter)/no_stocks*100,1)} %')
                # search with Ticker, if you find nothing, then search with Name
                code_df = share_id_old(index)
                code_df = code_df.reset_index()
                try:
                    web_id.append(code_df[code_df['active']==1].iloc[0]['webid'])
                    counter+=1
                except:
                    web_id.append(code_df[code_df['active']==0].iloc[0]['webid'])
                    counter+=1
                    pass
            # add new codes to dataframe
            no_web_id['webid'] = web_id 
            # build payeh dataframe with web-ids again:
            payeh_lookup = pd.concat([with_web_id,no_web_id])
            # add to bourse and fara-bourse:
            look_up = pd.concat([look_up[look_up['webid'].notnull()],payeh_lookup])
            look_up['Name'] = look_up['Name'].apply(lambda x: characters.ar_to_fa(x))
        # read stocks IDs from TSE webpages:
        def get_data_optimaize(codes):
            tracemalloc.start()
            @unsync
            async def get_data_parallel(codes):
                counter = 1
                async with aiohttp.ClientSession() as session:
                    tasks = []
                    for code in codes:
                        task = asyncio.ensure_future(get_session(session, code))
                        tasks.append(task)
                    view_counts = await asyncio.gather(*tasks)
                    for i in view_counts :
                        if (counter==1):
                            df_final = i.copy()
                        else:
                            df_final = pd.concat([df_final,i])
                        counter+=1
                return df_final
            async def get_session(session, code):
                url = f'http://old.tsetmc.com/Loader.aspx?Partree=15131M&i={code}'
                async with session.get(url, headers=headers) as response:
                    try:
                        data_text = await response.text()
                        soup = BeautifulSoup(data_text, 'html.parser')
                        table = soup.findAll("table", {"class": "table1"})
                        df_id = pd.read_html(str(table[0]))[0]
                        # rotate data frame:
                        df_id = df_id.T
                        df_id.columns = df_id.iloc[0]
                        df_id = df_id[1:]
                        df_current_stock = look_up[look_up['webid'] == code]
                        df_id['Ticker'] = df_current_stock.index[0]
                        df_id['Market'] = df_current_stock['Market'][0]
                        df_id['webid'] = df_current_stock['webid'][0]
                        return df_id
                    except:
                        failed_tickers_code.append(code)
                        return pd.DataFrame()
                return 
            return get_data_parallel(codes).result()
        
        no_stocks = len(look_up)
        if(show_progress):
            clear_output(wait=True)
            print(f'Gathering detailed data for {no_stocks} stocks ...')
            
        # gathering detailed data:
        continue_loop = True
        df_final = pd.DataFrame()
        web_id_list = look_up['webid'].to_list()
        failed_tickers_code = []
        while(continue_loop):
            df_temp = get_data_optimaize(codes = web_id_list)
            if(len(failed_tickers_code)>0):  # failed tickers
                web_id_list = failed_tickers_code
                failed_tickers_code = []
                df_final = pd.concat([df_final, df_temp])
            else:
                df_final = pd.concat([df_final, df_temp])
                continue_loop = False
                
        df_final.columns=['Ticker(12)','Ticker(5)','Name(EN)','Ticker(4)','Name','Comment','Ticker(30)','Company Code(12)',
                          'Panel','Panel Code', 'Sector Code','Sector','Sub-Sector Code','Sub-Sector','Ticker','Market','webid']
        df_final['Comment'] = df_final['Comment'].apply(lambda x: x.split('-')[1] if(len(x.split('-'))>1) else '-')
        df_final = df_final[['Ticker','Name','Market','Panel','Sector','Sub-Sector','Comment','Name(EN)',\
                             'Company Code(12)','Ticker(4)','Ticker(5)','Ticker(12)','Sector Code','Sub-Sector Code','Panel Code','webid']]
        # change arabic letter to farsi letters nad drop half-spaces:
        df_final['Ticker']=df_final['Ticker'].apply(lambda x: (str(x).replace('ي','ی')).replace('ك','ک'))
        df_final['Name']=df_final['Name'].apply(lambda x: (str(x).replace('ي','ی')).replace('ك','ک'))
        df_final['Panel']=df_final['Panel'].apply(lambda x: (str(x).replace('ي','ی')).replace('ك','ک'))
        df_final['Sector']=df_final['Sector'].apply(lambda x: (str(x).replace('ي','ی')).replace('ك','ک'))
        df_final['Sub-Sector']=df_final['Sub-Sector'].apply(lambda x: (str(x).replace('ي','ی')).replace('ك','ک'))
        df_final['Ticker']=df_final['Ticker'].apply(lambda x: (x.replace('\u200c',' ')).strip())
        df_final['Name'] = df_final['Name'].apply(lambda x: (x.replace('\u200c',' ')).strip())
        df_final['Panel'] = df_final['Panel'].apply(lambda x: (x.replace('\u200c',' ')).strip())
        df_final['Sector'] = df_final['Sector'].apply(lambda x: (x.replace('\u200c',' ')).strip())
        df_final['Sub-Sector'] = df_final['Sub-Sector'].apply(lambda x: (x.replace('\u200c',' ')).strip())

        df_final = df_final.set_index('Ticker')
        df_final.drop(columns=['webid'],inplace=True)
        end_time = time.time()
        if(show_progress):
            clear_output(wait=True)
            print('Progress : 100 % , Done in ' + str(int(round(end_time - start_time,0)))+' seconds!')
        #print(str(int(round(end_time - start_time,0)))+' seconds took to gather detailed data')
        #-------------------------------------------------------------------------------------------------------------------------------------
        # save file if necessary
        if(save_excel|save_csv):
            save_list(df_data=df_final, bourse=bourse, farabourse=bourse, payeh=payeh, detailed_list=detailed_list,save_excel=save_excel, save_csv=save_csv, save_path=save_path)
        return df_final