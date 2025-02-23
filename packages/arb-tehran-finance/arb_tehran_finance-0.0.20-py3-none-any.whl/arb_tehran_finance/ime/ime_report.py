from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import re
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from typing import Union



###################################################################################################################################
###################################################################################################################################



def future_group(group_name="کلیه گروه‌ها"):
    """
    Fetches trading data for a specific group or all groups from the Iran Mercantile Exchange (IME) website.

    This function extracts data from the trading board of a selected group on the IME website using 
    web scraping. The data is structured into a Pandas DataFrame, which contains information about 
    contracts, their prices, and trading volumes for the selected group.

    Parameters:
    group_name (str): The name of the group for which data should be fetched. Available groups:
                       - 'گروه صندوق طلای لوتوس'
                       - 'گروه صندوق طلای کهربا'
                       - 'گروه شمش طلای خام'
                       - 'گروه زعفران نگین'
                       - 'گروه نقره'
                       - 'کلیه گروه‌ها' (to fetch data for all groups)

    Returns:
    pandas.DataFrame: A DataFrame containing the trading data for the selected group(s). The DataFrame 
                      includes columns such as 'futures ticker', 'yesterday price', 'today price', 
                      'absolute change', 'percent change', 'volume', 'value', and 'open interest'.
    
    Raises:
    Exception: If an error occurs during the web scraping process, an exception is raised with 
               details of the error. For example, if the group is not found or the website structure 
               changes, a meaningful error message will be displayed.
    
    Example:
    df = future_group("گروه صندوق طلای لوتوس")
    This would return a DataFrame containing the trading data for the "گروه صندوق طلای لوتوس".

    df_all = future_group("کلیه گروه‌ها")
    This would return a DataFrame containing trading data for all available groups.

    Notes:
    - This function requires a stable internet connection and an active web browser environment 
      (Selenium with ChromeDriver).
    - The data is extracted by navigating the website and scraping the necessary tables, 
      so the structure of the website should remain consistent for the function to work correctly.
    """
    
    def convert_data(df):
        numeric_columns = ["yesterday price", "today price", "absolute change", "volume", "value", "open interest"]
        percent_column = "percent change"
        
        for col in numeric_columns:
            df[col] = df[col].str.replace(",", "").astype(int, errors='ignore')
        
        df[percent_column] = df[percent_column].str.replace("%", "").astype(float, errors='ignore') / 100
        
        return df

    # Browser setup
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # اختیاری: اجرای بدون رابط گرافیکی
    service = Service(ChromeDriverManager().install())  # نصب خودکار ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # URL of the IME website
    url = "https://cdn2.ime.co.ir/"
    driver.get(url)
    
    # XPath map for each group's trading table
    group_xpath_map = {
        "گروه صندوق طلای لوتوس": "//*[@id='futureView']/div/uib-accordion/div/div/div[1]/div/div[2]/div",
        "گروه صندوق طلای کهربا": "//*[@id='futureView']/div/uib-accordion/div/div/div[2]/div/div[2]/div",
        "گروه شمش طلای خام": "//*[@id='futureView']/div/uib-accordion/div/div/div[3]/div/div[2]/div",
        "گروه زعفران نگین": "//*[@id='futureView']/div/uib-accordion/div/div/div[4]/div/div[2]/div",
        "گروه نقره": "//*[@id='futureView']/div/uib-accordion/div/div/div[6]/div/div[2]/div"
    }
    
    # Column names
    column_names = ['futures ticker', 'yesterday price', 'today price', 'absolute change', 
                    'percent change', 'volume', 'value', 'open interest','']
    
    # If fetching all groups, iterate over each group
    if group_name == "کلیه گروه‌ها":
        all_data = []
        for name, xpath in group_xpath_map.items():
            try:
                table_element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                rows = table_element.find_elements(By.TAG_NAME, "tr")
                table_data = []
                for row in rows:
                    row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
                    if any(row_data):
                        table_data.append(row_data)
                
                if table_data:
                    # Convert data to appropriate types using convert_data function
                    df = pd.DataFrame(table_data, columns=column_names)
                    df = convert_data(df)  # Apply conversion
                    df.insert(0, "group", name)  # Add group name as the first column
                    all_data.append(df)
            except Exception as e:
                print(f"Error fetching data for group {name}: {e}")
        
        driver.quit()
        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame(columns=column_names)
    
    # Fetch data for a single specified group
    try:
        table_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, group_xpath_map[group_name]))
        )
        
        rows = table_element.find_elements(By.TAG_NAME, "tr")
        table_data = []
        for row in rows:
            row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
            if any(row_data):
                table_data.append(row_data)
        
        if table_data:
            # Convert data to appropriate types using convert_data function
            df = pd.DataFrame(table_data, columns=column_names)
            df = convert_data(df)  # Apply conversion
            return df
        else:
            print(f"No data found for group {group_name}.")
            return pd.DataFrame(columns=column_names)
        
    except Exception as e:
        print(f"Error fetching data for group {group_name}: {e}")
        return pd.DataFrame(columns=column_names)
    
    finally:
        driver.quit()
        driver.close()


###################################################################################################################################
###################################################################################################################################


def future(group_name='کلیه گروه‌ها', contract_name='کلیه قراردادها'):
    """
    Retrieves futures trading data from the Iran Mercantile Exchange (IME) website.

    This function scrapes the IME trading board for futures contracts and organizes the data into a Pandas DataFrame. 
    The retrieved data includes key financial metrics such as prices, percentage changes, trading volume, and open interest. 
    It supports filtering by specific groups and contracts, ensuring precise data extraction.

    Parameters:
    group_name (str): The name of the trading group to fetch data for. Available groups:
                       - 'گروه صندوق طلای لوتوس'
                       - 'گروه صندوق طلای کهربا'
                       - 'گروه شمش طلای خام'
                       - 'گروه زعفران نگین'
                       - 'گروه نقره'
                       - 'کلیه گروه‌ها' (to fetch data for all groups)
    contract_name (str, optional): The specific contract name within the selected group. 
                                   Defaults to "کلیه قراردادها" (all contracts).
                                   If a specific contract is provided (e.g., "ETCFA04"), only its data will be returned.

    Returns:
    pandas.DataFrame: A DataFrame containing futures trading data with the following columns:
        - 'group name' (str): The trading group name.
        - 'futures ticker' (str): The contract ticker symbol.
        - 'yesterday price' (int): The closing price from the previous trading session.
        - 'today price' (int): The last recorded price of the contract.
        - 'absolute change' (int): The absolute price difference between today and yesterday.
        - 'percent change' (float): The percentage change in price compared to the previous session.
        - 'volume' (int): The total number of contracts traded.
        - 'value' (int): The total monetary value of trades in the contract.
        - 'open interest' (int): The total number of open contracts that remain unsettled.

    Raises:
    Exception: An exception is raised if the scraping process encounters errors such as:
        - The specified group is not found on the IME website.
        - The website structure changes, affecting data extraction.
        - A timeout occurs while waiting for the elements to load.

    Example:
    Suppose you want to retrieve all available futures contracts in the "گروه زعفران نگین" group:
    
        df = future(group_name='گروه زعفران نگین')
        print(df)
    
    To fetch data for a specific contract (e.g., "ETCFA04") in the same group:
    
        df = future(group_name='گروه زعفران نگین', contract_name='ETCFA04')
        print(df)
    
    If you want to fetch all available data across all groups:
    
        df = future()
        print(df)

    """
    
    # Browser setup

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # اختیاری: اجرای بدون رابط گرافیکی
    service = Service(ChromeDriverManager().install())  # نصب خودکار ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # IME website URL
    url = "https://cdn2.ime.co.ir/"
    driver.get(url)
    
    # Xpath dictionary for each group
    group_xpath_map = {
        "گروه صندوق طلای لوتوس": "//*[@id='futureView']/div/uib-accordion/div/div/div[1]/div/div[2]/div",
        "گروه صندوق طلای کهربا": "//*[@id='futureView']/div/uib-accordion/div/div/div[2]/div/div[2]/div",
        "گروه شمش طلای خام": "//*[@id='futureView']/div/uib-accordion/div/div/div[3]/div/div[2]/div",
        "گروه زعفران نگین": "//*[@id='futureView']/div/uib-accordion/div/div/div[4]/div/div[2]/div",
        "گروه نقره": "//*[@id='futureView']/div/uib-accordion/div/div/div[6]/div/div[2]/div"
    }
    
    # Correct column names
    columns = [
        "futures ticker", "yesterday price", "today price", "absolute change",
        "percent change", "volume", "value", "open interest",""
    ]
    
    def convert_data(df):
        numeric_columns = ["yesterday price", "today price", "absolute change", "volume", "value", "open interest"]
        percent_column = "percent change"
        
        for col in numeric_columns:
            df[col] = df[col].str.replace(",", "").astype(int, errors='ignore')
        
        df[percent_column] = df[percent_column].str.replace("%", "").astype(float, errors='ignore') / 100
        
        return df
    
    try:
        # Fetch data for all groups
        if group_name == "کلیه گروه‌ها":
            all_data = []
            for group, xpath in group_xpath_map.items():
                table_element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                rows = table_element.find_elements(By.TAG_NAME, "tr")
                table_data = []
                for row in rows:
                    row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
                    if any(row_data):
                        row_data.insert(0, group)  # Add group name to the start of each row
                        table_data.append(row_data)

                if table_data:
                    table_df = pd.DataFrame(table_data, columns=["group name"] + columns)  # Adding "group name" column at the beginning
                    table_df = convert_data(table_df)
                    all_data.append(table_df)

            if all_data:
                return pd.concat(all_data, ignore_index=True)
            else:
                return pd.DataFrame(columns=["group name"] + columns)
        
        # Fetch data for the specific group
        table_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, group_xpath_map[group_name]))
        )
        
        # Extract data from the table
        rows = table_element.find_elements(By.TAG_NAME, "tr")
        table_data = []
        for row in rows:
            row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
            if any(row_data):
                row_data.insert(0, group_name)  # Add group name to the start of each row
                table_data.append(row_data)
        
        # If there is data
        if table_data:
            table_df = pd.DataFrame(table_data, columns=["group name"] + columns)
            table_df = convert_data(table_df)
            
            # Filter by specific contract
            if contract_name != "کلیه قراردادها":
                table_df = table_df[table_df["futures ticker"] == contract_name]
                if table_df.empty:
                    print(f"No data found for contract {contract_name} in group {group_name}.")
                    return pd.DataFrame(columns=["group name"] + columns)
            
            return table_df
        else:
            print(f"No data found for group {group_name}.")
            return pd.DataFrame(columns=["group name"] + columns)
        
    except Exception as e:
        print(f"Error fetching data for group {group_name}: {e}")
        return pd.DataFrame(columns=["group name"] + columns)
    
    finally:
        # Close the browser
        driver.close()
        driver.quit()


###################################################################################################################################
###################################################################################################################################



def futures_fees(asset: str = "", role: str = "", fee: str = "") -> Union[dict, float]:
    """
    Retrieves and formats futures contract fees from the Iran Mercantile Exchange website.

    Parameters:
    - asset (str): The name of the underlying asset (e.g., 'طلا'). If empty, shows all assets.
    - role (str): The role of the participant ('خریدار' or 'فروشنده'). If empty, shows both roles.
    - fee (str): Type of fee ('معاملات', 'تسویه و تحویل', or ""). If empty, includes both.

    Returns:
    - dict or float:
      * If specific asset, role, and fee type are provided, returns only the fee as a float.
      * Otherwise, returns a dictionary containing both fee types ('معاملات' and 'تسویه و تحویل') with corresponding values for each asset.
    """
    from arb_tehran_finance.tse.tse_report import get_gold_funds

    # Check if asset matches gold fund symbols
    gold_funds_df = get_gold_funds()
    if asset in gold_funds_df.index:
        asset = "صندوق های طلا"  # Treat the asset as "صندوق های طلا"
    
    url = "https://www.ime.co.ir/FuturesFee.html"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: Failed to retrieve the page, status code {response.status_code}")
        return None
    
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all('table')
    if len(tables) < 2:
        print("Error: Not enough tables found.")
        return None

    fees_data = {"معاملات": {}, "تسویه و تحویل": {}}
    SETTLEMENT_FEE = 0.0014

    # Extract data from "معاملات" table
    rows = tables[0].find_all('tr')[1:]
    for i in range(0, len(rows), 2):
        if i + 1 >= len(rows):
            continue

        buyer_row = rows[i].find_all('td')
        seller_row = rows[i + 1].find_all('td')

        if len(buyer_row) < 6 or len(seller_row) < 5:
            continue

        asset_name = buyer_row[0].text.strip()
        if not asset_name:
            continue

        buyer_fee = float(buyer_row[5].text.strip().replace(',', '').replace('/', '.'))
        seller_fee = float(seller_row[4].text.strip().replace(',', '').replace('/', '.'))

        fees_data["معاملات"].setdefault(asset_name, {})["خریدار"] = buyer_fee
        fees_data["معاملات"].setdefault(asset_name, {})["فروشنده"] = seller_fee
        
        # Add settlement fee for each asset
        fees_data["تسویه و تحویل"].setdefault(asset_name, {"خریدار": SETTLEMENT_FEE, "فروشنده": SETTLEMENT_FEE})

    # Filter by fee type
    if fee in ["معاملات", "تسویه و تحویل"]:
        fees_data = {fee: fees_data[fee]}

    # Filter by asset and role
    if asset:
        filtered_fees = {
            "معاملات": fees_data.get("معاملات", {}).get(asset, {}),
            "تسویه و تحویل": fees_data.get("تسویه و تحویل", {}).get(asset, {})
        }

        if role:
            if role in filtered_fees["معاملات"]:
                return filtered_fees["معاملات"][role]
            elif role in filtered_fees["تسویه و تحویل"]:
                return filtered_fees["تسویه و تحویل"][role]
            else:
                return None  # If no data exists for the specified role
        
        return filtered_fees  # If only asset is provided, return dictionary

    return fees_data  # If no filters are applied, return all data



###################################################################################################################################
###################################################################################################################################



def get_underlying_price(symbol_underlying: str) -> float:

    from arb_tehran_finance.tse.tse_report import marketwatch

    # Fetch market data
    df = marketwatch()
    
    if df is None or symbol_underlying not in df.index:
        raise ValueError(f"Symbol {symbol_underlying} not found in market data.")
    return df.loc[symbol_underlying, "close"]



###################################################################################################################################
###################################################################################################################################



def future_contract(contract_names: list) -> pd.DataFrame:
    """
    Extracts trading data for a list of futures contracts from the Iran Mercantile Exchange website.

    This function navigates the Iran Mercantile Exchange (IME) website, clicks on the "آتی" (Futures) tab,
    and searches for each contract in the provided list. For each contract, it scrapes trading data including
    contract details such as Initial Margin, Maturity, and Contract Size, and compiles this data into a DataFrame.

    Parameters:
    contract_names (list): A list of strings representing the names of the futures contracts to extract data for.

    Returns:
    pd.DataFrame: A DataFrame containing the extracted data for all contracts. The DataFrame includes the following columns:
        - "Contract Name": The name of the futures contract.
        - "Margin": The margin for the contract.
        - "Initial Margin": The initial margin requirement for the contract.
        - "Contract Size": The size of the contract.
        - "Maturity": The maturity date of the contract.
        - "Settlement Price": The settlement price of the contract.
        - "First": The first trade price of the contract.
        - "High": The highest trade price of the contract.
        - "Low": The lowest trade price of the contract.
        - "Last": The last trade price of the contract.

    Example:
    contract_names = ["Contract1", "Contract2", "Contract3"]
    df = future_contract(contract_names)
    print(df)
    """
    # تنظیمات مرورگر Chrome برای بهینه‌سازی سرعت بارگذاری
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # اجرای بدون رابط گرافیکی
    chrome_options.add_argument("--disable-gpu")  # غیرفعال کردن GPU برای بهبود عملکرد
    chrome_options.add_argument("--no-sandbox")  # غیرفعال کردن sandbox برای سرعت بیشتر
    chrome_options.add_argument("--disable-dev-shm-usage")  # کاهش استفاده از حافظه
    chrome_options.add_argument("--disable-software-rasterizer")  # غیرفعال کردن رندر نرم‌افزاری
    chrome_options.add_argument("--disable-images")  # غیرفعال کردن بارگذاری تصاویر
    chrome_options.add_argument("--window-size=1920x1080")  # تنظیم اندازه پنجره برای جلوگیری از کاهش سرعت به دلیل تغییر اندازه صفحه
    chrome_options.add_argument("--disable-extensions")  # غیرفعال کردن اکستنشن‌ها
    chrome_options.add_argument("--incognito")  # استفاده از حالت ناشناس برای جلوگیری از بارگذاری تبلیغات
    chrome_options.add_argument("--disable-plugins")  # غیرفعال کردن پلاگین‌ها
    chrome_options.add_argument("--disable-translate")  # غیرفعال کردن قابلیت ترجمه

    # نصب و راه‌اندازی ChromeDriver
    service = Service(ChromeDriverManager().install())  # نصب خودکار ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    wait = WebDriverWait(driver, 20)

    try:
        # باز کردن صفحه بورس کالا
        url = "https://cdn2.ime.co.ir/"
        driver.get(url)

        # پیدا کردن لینک "آتی" و کلیک روی آن
        future_tab = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "آتی")))
        future_tab.click()
        time.sleep(5)  # صبر برای لود شدن جدول قراردادها

        # لیست برای ذخیره اطلاعات همه قراردادها
        all_contracts_data = []

        # شمارنده برای تشخیص قرارداد اول
        first_contract = True

        # حلقه برای جستجو و استخراج اطلاعات برای هر قرارداد
        for contract_name in contract_names:
            # اسکرول به بالا برای اطمینان از نمایش باکس جستجو
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)

            # پیدا کردن باکس جستجو
            search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 
                "#futureView > div > div > div.card > div.card-body > div:nth-child(1) > div:nth-child(1) > input")))

            actions = ActionChains(driver)
            actions.move_to_element(search_box).click().perform()
            time.sleep(2)
            search_box.clear()
            time.sleep(2)
            search_box.send_keys(contract_name)
            time.sleep(5)  # تاخیر برای به‌روزرسانی لیست

            # جستجوی نام قرارداد در جدول
            contract_rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
            target_row = None

            for row in contract_rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if cells and contract_name in row.text:
                    target_row = row
                    break

            if not target_row:
                print(f"❌ قرارداد '{contract_name}' یافت نشد!")
                continue  # میریم سراغ قرارداد بعدی

            # فقط در قرارداد اول کلیک روی نام قرارداد انجام می‌شود
            if first_contract:
                target_row.click()
                time.sleep(10)  # صبر برای نمایش جزئیات قرارداد
                first_contract = False  # تغییر وضعیت برای قراردادهای بعدی

            # اسکرول کردن برای لود شدن همه داده‌ها
            for _ in range(3):
                actions.send_keys(Keys.PAGE_DOWN).perform()
                time.sleep(5)

            # استخراج داده‌های جدول معاملات
            table_rows = driver.find_elements(By.CSS_SELECTOR, "#future tbody.content tr")
            data = []
            for row in table_rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                row_data = [col.text.strip() for col in cols]
                if row_data:
                    data.append(row_data)

            if not data:  # Check if no data was found
                print(f"❌ داده‌ای برای قرارداد '{contract_name}' پیدا نشد!")
                continue

            # خودکار شناسایی تعداد ستون‌ها
            num_columns = len(data[0]) if data else 0
            columns = [
                "Contract Code", "Bid Volume", "Bid Price", "Ask Price", "Ask Volume",
                "First Trade", "High Trade", "Low Trade", "Last Trade", "Percent Change"
            ][:num_columns]

            # تبدیل داده‌ها به DataFrame
            df = pd.DataFrame(data, columns=columns)

            # استخراج اطلاعات خاص
            contract_name = df.loc[0, "Contract Code"] if len(df) > 0 else None
            margin = df.loc[2, "Contract Code"] if len(df) > 2 else None
            initial_margin = df.loc[3, "Contract Code"] if len(df) > 3 else None
            contract_size = df.loc[5, "Contract Code"] if len(df) > 5 else None  # تغییر به ردیف 6
            maturity = df.loc[4, "Contract Code"] if len(df) > 4 else None
            settlement_price = df.loc[5, "Bid Volume"] if len(df) > 5 else None  # تغییر به ردیف 6
            first_trade = df.loc[0, "First Trade"] if len(df) > 0 else None
            high_trade = df.loc[0, "High Trade"] if len(df) > 0 else None
            low_trade = df.loc[0, "Low Trade"] if len(df) > 0 else None
            last_trade = df.loc[0, "Last Trade"] if len(df) > 0 else None

            # ساخت یک DataFrame از اطلاعات خاص
            result = {
                "Contract Name": contract_name,
                "Margin": margin,
                "Initial Margin": initial_margin,
                "Contract Size": contract_size,
                "Maturity": maturity,
                "Settlement Price": settlement_price,
                "First": first_trade,
                "High": high_trade,
                "Low": low_trade,
                "Last": last_trade
            }

            # اضافه کردن اطلاعات به لیست
            all_contracts_data.append(result)

            # پاک کردن باکس جستجو و ادامه برای قرارداد بعدی
            search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 
                "#futureView > div > div > div.card > div.card-body > div:nth-child(1) > div:nth-child(1) > input")))

            actions.move_to_element(search_box).click().perform()
            time.sleep(2)
            search_box.clear()
            time.sleep(2)

        # برگرداندن تمام اطلاعات به صورت یک DataFrame
        if all_contracts_data:
            df_all = pd.DataFrame(all_contracts_data)
            df_all.set_index('Contract Name', inplace=True)
            return df_all
        else:
            print("❌ هیچ داده‌ای برای قراردادها یافت نشد!")
            return pd.DataFrame()  # Return an empty DataFrame if no data was collected

    finally:
        driver.quit()






###################################################################################################################################
###################################################################################################################################



def futures_contract_for_gold_funds():
    """
    Matches gold ETFs with related futures contracts based on the last word in the 'name' column.

    Returns:
    dict: A dictionary where keys are gold ETF names and values are lists of matching futures contracts.
    """

    from arb_tehran_finance.tse.tse_report import get_gold_funds

    # Retrieve data
    gold_funds_df = get_gold_funds()
    futures_df = future()

    # Normalize Arabic and Persian characters
    def normalize_text(text):
        return text.replace("ي", "ی").replace("ك", "ک").strip()

    # Apply normalization to 'group name' in futures_df
    futures_df["group name"] = futures_df["group name"].apply(normalize_text)

    # Initialize a dictionary
    gold_fund_to_futures = {}

    # Match each gold ETF with related futures contracts
    for fund_symbol, row in gold_funds_df.iterrows():
        fund_name = normalize_text(str(row["name"]))  # Normalize and extract name
        last_word = fund_name.split()[-1]  # Get the last word

        # Use regex for exact word matching
        pattern = rf"\b{re.escape(last_word)}\b"

        matched_futures = futures_df[futures_df["group name"].str.contains(pattern, na=False, regex=True)]["futures ticker"].tolist()
        gold_fund_to_futures[fund_symbol] = matched_futures  # Store results

    return gold_fund_to_futures
