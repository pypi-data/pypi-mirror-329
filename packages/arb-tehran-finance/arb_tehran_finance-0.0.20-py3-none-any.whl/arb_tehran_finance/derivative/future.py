import numpy as np
import pandas as pd



######################################################################################################################################
######################################################################################################################################


def future_value_manual (underlying_price , dividend , risk_free_rate , day_until_maturity):
    """
    Calculates the future value of an underlying asset using the cost-of-carry model, 
    accounting for dividend yield and the risk-free interest rate.

    Parameters:
        underlying_price (float): The current market price of the underlying asset.
        dividend (float): The expected dividend amount for the underlying asset.
        risk_free_rate (float): The annualized risk-free interest rate (in decimal form).
        day_until_maturity (int): The number of days remaining until contract maturity.

    Process:
        1. Computes the continuous compounding rate for dividend yield using the formula:
        dividend_yield = ln(1 + (dividend / underlying_price)).
        2. Applies the cost-of-carry model to determine the theoretical future price:
        future_value = underlying_price * exp((risk_free_rate - dividend_yield) * (day_until_maturity / 365)).
        3. Returns the calculated future value, reflecting the asset's expected price at maturity.

    Example Usage:
        Suppose a stock is currently priced at 1,000, with an expected dividend of 20, 
        a risk-free rate of 15% (0.15), and 90 days until maturity:
        
            future_value_manual(underlying_price=1000, dividend=20, risk_free_rate=0.15, day_until_maturity=90)

    Notes:
        - The function assumes continuous compounding for dividends and interest rates.
        - If the dividend is zero, the future value will be based solely on the risk-free rate.
        - This method is useful for pricing futures and forward contracts under normal market conditions.
"""

    dividend_yield = np.log(1+(dividend/underlying_price))  #Calculation of continuous compounding rate for dividend
    future_value = underlying_price * np.exp((risk_free_rate-dividend_yield) *(day_until_maturity/365)) #future_value = underlying_price * ((1+((risk_free_rate-dividend_yield)/365))**day_until_maturity)
    return future_value

######################################################################################################################################
######################################################################################################################################


def future_arbitrage_manual(
    underlying_price: float, futures_price: float, contract_size: int, dividend: float, 
    risk_free_rate: float, day_until_maturity: int, initial_margin: float, 
    underlying_buy_fee: float, futures_short_fee: float, 
    futures_settlement_delivery_fees: float, warehousing_taxes: float) -> dict:
    """
    Calculates the arbitrage profit from trading futures contracts by considering transaction costs 
    and the time value of money.

    Parameters:
    - underlying_price (float): Current price of the underlying asset.
    - futures_price (float): Price of the futures contract.
    - contract_size (int): Number of units in one futures contract.
    - dividend (float): Expected dividend payout (not used in current calculation).
    - risk_free_rate (float): Annual risk-free interest rate (as a decimal).
    - day_until_maturity (int): Number of days until the futures contract expires.
    - initial_margin (float): Margin required to enter the futures contract.
    - underlying_buy_fee (float): Fee for purchasing the underlying asset.
    - futures_short_fee (float): Fee for shorting the futures contract.
    - futures_settlement_delivery_fees (float): Fees for settling and delivering the futures contract.
    - warehousing_taxes (float): Taxes associated with storing the underlying asset.

    Returns:
    - dict: A dictionary containing the following arbitrage profit calculations:
      - "arbitrage profit": Profit from arbitrage before costs.
      - "additional costs": Total transaction costs and fees.
      - "opportunity cost": Cost of capital over the contract period.
      - "maturity arbitrage profit": Profitability of arbitrage at contract maturity.
      - "annual arbitrage profit": Annualized arbitrage profit for comparison.

    Example:
    arbitrage = future_arbitrage(
        underlying_price=1000, futures_price=1050, contract_size=100, dividend=0,
        risk_free_rate=0.05, day_until_maturity=180, initial_margin=5000,
        underlying_buy_fee=10, futures_short_fee=15, futures_settlement_delivery_fees=20,
        warehousing_taxes=30)
    print(arbitrage)

    Notes:
    - A positive arbitrage profit suggests a profitable trading opportunity.
    - If `day_until_maturity` is too short, opportunity cost will be lower.
    - Ensure all costs are included to get an accurate arbitrage calculation.
    """

    if contract_size <= 0 or day_until_maturity <= 0:
        raise ValueError("Contract size and days until maturity must be greater than zero.")

    # Arbitrage Profit Calculation
    arbitrage_profit = contract_size * (futures_price - underlying_price)

    # Additional Costs
    additional_costs = (
        (contract_size * underlying_price * underlying_buy_fee) +
        (contract_size * futures_price * futures_short_fee) +
        (contract_size * futures_price * futures_settlement_delivery_fees) +
        warehousing_taxes)

    # Opportunity Cost
    invested_capital = (contract_size * underlying_price) + initial_margin + additional_costs
    opportunity_cost = invested_capital * ((risk_free_rate / 365) * day_until_maturity)

    # Maturity & Annualized Arbitrage Profit
    maturity_arbitrage_profit = arbitrage_profit / (invested_capital + opportunity_cost)
    annual_arbitrage_profit = (maturity_arbitrage_profit / day_until_maturity) * 365

    # Return as a structured dictionary
    return {
        "arbitrage profit": arbitrage_profit,
        "additional costs": additional_costs,
        "opportunity cost": opportunity_cost,
        "maturity arbitrage profit": maturity_arbitrage_profit,
        "annual arbitrage profit": annual_arbitrage_profit
    }


######################################################################################################################################
######################################################################################################################################


def future_arbitrage(symbol_underlying: str, dividend: float, risk_free_rate: float):
    """
    Calculates arbitrage opportunities in the futures market based on the underlying asset price,  
    contract details, and relevant transaction costs.  

    ### Parameters:  
    - **symbol_underlying (str)**: The ticker symbol of the underlying asset.  
    - **dividend (float)**: The annualized dividend yield of the underlying asset (in percentage).  
    - **risk_free_rate (float)**: The annualized risk-free interest rate (in percentage).  

    ### Process:  
    1. Retrieves futures contracts associated with the underlying asset.  
    2. Fetches or prompts user input for missing contract details, including:  
        - Futures contract prices  
        - Contract size  
        - Time to maturity (days)  
        - Initial margin requirements  
    3. Computes transaction fees for trading the underlying asset and futures contracts.  
    4. Applies cost-of-carry and arbitrage pricing principles to:  
        - Calculate the fair theoretical futures price based on the underlying asset price, interest rate, dividend, and storage costs.  
        - Compare the fair price with actual market prices to determine mispricing.  
        - Identify risk-free arbitrage opportunities by evaluating whether the futures price is overvalued or undervalued relative to the spot price.  

    ### Example Usage:  
    Suppose we want to analyze arbitrage opportunities for a gold ETF with a given dividend yield  
    and a 20% risk-free rate:  
    ```python
    future_arbitrage(symbol_underlying='طلا', dividend=0, risk_free_rate=0.20)
    ```

    ### Output:
    - A DataFrame summarizing arbitrage opportunities with the following columns:
        * `day until maturity`: Number of days remaining until the futures contract expires.
        * `arbitrage profit`: Estimated profit from arbitrage per contract.
        * `additional costs`: Extra costs such as transaction fees and margin requirements.
        * `opportunity cost`: The cost of capital tied up in the arbitrage trade.
        * `maturity arbitrage profit`: Expected profit at contract maturity, accounting for costs.
        * `annual arbitrage profit`: Profit expressed as an annualized return based on maturity.

    This output helps traders assess the feasibility and profitability of arbitrage trades.

    ### Notes:
        -The function interacts with Tehran Stock Exchange (TSETMC) and Iran Mercantile Exchange (IME) data sources.
        -User input may be required if data retrieval encounters issues.
        -The function assumes that contract names and structures are stable.
    """

    from arb_tehran_finance.tse.tse_report import stocks_fees
    from arb_tehran_finance.ime.ime_report import futures_contract_for_gold_funds, get_underlying_price, future_contract, futures_fees
    from arb_tehran_finance.sundry.utility_functions import remaining_days

    
    # Variable 1


    def get_user_input_list(prompt: str):
        """
        دریافت لیستی از مقادیر از کاربر با جداسازی توسط کاما.
        """
        while True:
            user_input = input(prompt).strip()
            
            if not user_input:
                print("❌ مقدار نمی‌تواند خالی باشد. لطفاً مقدار صحیح وارد کنید.")
                continue
            
            return [item.strip() for item in user_input.split(",")]

    # دریافت لیست قراردادهای آتی
    future_contracts_data = futures_contract_for_gold_funds()

    if not isinstance(future_contracts_data, dict):  # بررسی نوع داده بازگشتی
        print("⚠️ داده‌های قراردادهای آتی معتبر نیستند. لطفاً به‌صورت دستی وارد کنید.")
        future_contracts_data = {}

    future_contracts = future_contracts_data.get(symbol_underlying, [])

    if not isinstance(future_contracts, list) or not future_contracts:
        print(f"⚠️ هیچ قراردادی برای {symbol_underlying} پیدا نشد. لطفاً به‌صورت دستی وارد کنید.")
        future_contracts = get_user_input_list(f"🔹 لطفاً لیست قراردادهای آتی برای {symbol_underlying} را وارد کنید (با کاما جدا کنید): ")

    print(f"✅ قراردادهای آتی برای {symbol_underlying}: {future_contracts}")


    future_contract = future_contract(contract_names = future_contracts )

    
    # Variable 2


    def get_user_input_float(prompt: str):
        """
        دریافت مقدار عددی از کاربر و اطمینان از معتبر بودن آن.
        """
        while True:
            user_input = input(prompt).strip()
            
            try:
                value = float(user_input)
                if value <= 0:
                    print("❌ مقدار باید یک عدد مثبت باشد. لطفاً مقدار صحیح وارد کنید.")
                    continue
                return value
            except ValueError:
                print("❌ مقدار وارد شده عددی نیست. لطفاً مقدار صحیح وارد کنید.")

    # دریافت قیمت دارایی پایه
    underlying_price = get_underlying_price(symbol_underlying=symbol_underlying)

    # بررسی اعتبار مقدار دریافت شده
    if underlying_price is None or isinstance(underlying_price, (str, list, dict)) or \
    (isinstance(underlying_price, (int, float, np.number)) and (np.isnan(underlying_price) or underlying_price <= 0)):
        print(f"⚠️ قیمت دارایی پایه برای {symbol_underlying} معتبر نیست. لطفاً به‌صورت دستی وارد کنید.")
        underlying_price = get_user_input_float(f"🔹 لطفاً قیمت دارایی پایه برای {symbol_underlying} را وارد کنید: ")

    print(f"✅ قیمت دارایی پایه ({symbol_underlying}): {underlying_price}")


    # Variable 3


    def get_user_input_int(prompt: str):
        """
        دریافت مقدار عددی از کاربر و اطمینان از معتبر بودن آن.
        """
        while True:
            user_input = input(prompt).strip().replace(",", "")  # حذف کاما برای اعداد فارسی
            if user_input.isdigit():
                return int(user_input)
            print("❌ مقدار وارد شده معتبر نیست. لطفاً فقط عدد صحیح وارد کنید.")

    # بررسی قیمت قراردادهای آتی
    futures_price = {}

    for contract in future_contracts:
        try:
            price_value = future_contract.loc[contract, "Last"]

            if pd.notna(price_value) and isinstance(price_value, (int, float, str)):
                cleaned_price = int(str(price_value).replace(",", ""))
                futures_price[contract] = cleaned_price
            else:
                raise ValueError("Invalid price value")  # اگر مقدار معتبر نباشد، به ورودی دستی می‌رود.

        except (KeyError, ValueError, TypeError):
            print(f"⚠️ قیمت قرارداد {contract} معتبر نیست. لطفاً به‌صورت دستی وارد کنید.")
            futures_price[contract] = get_user_input_int(f"🔹 لطفاً قیمت قرارداد {contract} را وارد کنید: ")

    print(f"✅ قیمت قراردادهای آتی: {futures_price}")


    # Variable 4



    def get_user_input_int(prompt: str):
        """
        دریافت مقدار عددی از کاربر و اطمینان از معتبر بودن آن.
        """
        while True:
            user_input = input(prompt).strip().replace(",", "")  # حذف کاما برای پشتیبانی از قالب فارسی
            if user_input.isdigit():
                return int(user_input)
            print("❌ مقدار وارد شده معتبر نیست. لطفاً فقط عدد صحیح وارد کنید.")

    # بررسی مقدار "Contract Size" برای هر قرارداد
    contract_size = {}

    for contract in future_contracts:
        try:
            size_value = future_contract.loc[contract, "Contract Size"]

            if pd.notna(size_value) and isinstance(size_value, (int, float, str)):
                cleaned_size = int(str(size_value).split()[0].replace(",", ""))
                contract_size[contract] = cleaned_size
            else:
                raise ValueError("Invalid contract size")  # مقدار نامعتبر → دریافت ورودی از کاربر

        except (KeyError, ValueError, TypeError):
            print(f"⚠️ مقدار 'Contract Size' برای قرارداد {contract} نامعتبر است. لطفاً مقدار را به‌صورت دستی وارد کنید.")
            contract_size[contract] = get_user_input_int(f"🔹 لطفاً مقدار قرارداد {contract} را وارد کنید: ")

    print(f"✅ مقدار سایز قراردادها: {contract_size}")


    # Variable 5


    day_until_maturity = {}

    for contract in future_contracts:
        maturity_value = future_contract.loc[contract, "Maturity"]

        if pd.notna(maturity_value) and isinstance(maturity_value, str) and maturity_value.strip():  
            # اگر مقدار تاریخ سررسید خالی نباشد، محاسبه خودکار انجام شود
            try:
                day_until_maturity[contract] = remaining_days(maturity_value)
            except Exception as e:
                print(f"Error processing maturity date for {contract}: {e}")
                while True:
                    user_input = input(f"Enter maturity date for {contract} (e.g., 'سه شنبه ۲۴ تیر ۱۴۰۴'): ").strip()
                    if user_input:
                        try:
                            day_until_maturity[contract] = remaining_days(user_input)
                            break
                        except Exception as e:
                            print(f"Invalid date format. Error: {e}")
                    else:
                        print("Maturity date cannot be empty.")
        else:
            # اگر مقدار موجود نباشد، از کاربر تاریخ سررسید دریافت شود
            while True:
                user_input = input(f"Enter maturity date for {contract} (e.g., 'سه شنبه ۲۴ تیر ۱۴۰۴'): ").strip()
                if user_input:
                    try:
                        day_until_maturity[contract] = remaining_days(user_input)
                        break
                    except Exception as e:
                        print(f"Invalid date format. Error: {e}")
                else:
                    print("Maturity date cannot be empty.")

    # پرینت نام و مقدار متغیر
    print(f"✅ مقدار روز مانده تا سررسید قراردادها: {day_until_maturity}")



    # Variable 6


    def get_user_input_int(prompt: str):
        """
        دریافت مقدار عددی از کاربر و اطمینان از معتبر بودن آن.
        """
        while True:
            user_input = input(prompt).strip().replace(",", "")  # حذف کاما برای پشتیبانی از قالب فارسی
            if user_input.isdigit():
                return int(user_input)
            print("❌ مقدار وارد شده معتبر نیست. لطفاً فقط عدد صحیح وارد کنید.")

    # بررسی مقدار "Initial Margin" برای هر قرارداد
    initial_margin = {}

    for contract in future_contracts:
        try:
            margin_value = future_contract.loc[contract, "Initial Margin"]

            if pd.notna(margin_value) and isinstance(margin_value, (int, float, str)):
                cleaned_margin = int(str(margin_value).replace(",", ""))  # حذف کاما و تبدیل به عدد
                initial_margin[contract] = cleaned_margin
            else:
                raise ValueError("Invalid margin value")  # مقدار نامعتبر → دریافت ورودی از کاربر

        except (KeyError, ValueError, TypeError):
            print(f"⚠️ مقدار 'Initial Margin' برای قرارداد {contract} نامعتبر است. لطفاً مقدار را به‌صورت دستی وارد کنید.")
            initial_margin[contract] = get_user_input_int(f"🔹 لطفاً مقدار اولیه مارجین برای قرارداد {contract} را وارد کنید: ")

    print(f"✅ مقدار وجه تضمین اولیه قراردادها: {initial_margin}")


    # Variable 7


    # تابع کمکی برای دریافت مقدار عددی از کاربر
    def get_user_input_float(prompt: str):
        """دریافت مقدار عددی از کاربر و اطمینان از معتبر بودن آن."""
        while True:
            user_input = input(prompt).strip().replace(",", "")  # حذف کاما برای اعداد فارسی
            try:
                return float(user_input)
            except ValueError:
                print("❌ مقدار وارد شده معتبر نیست. لطفاً فقط عدد وارد کنید.")

    # مقداردهی `underlying_buy_fee` و مدیریت خطاها
    try:
        underlying_buy_fee = stocks_fees(asset=symbol_underlying, role="خریدار")

        if underlying_buy_fee is None or not isinstance(underlying_buy_fee, (int, float)):
            raise ValueError("Invalid underlying buy fee")  # مقدار نامعتبر → دریافت ورودی از کاربر

    except (KeyError, ValueError, TypeError):
        print(f"⚠️ مقدار 'کارمزد خرید دارایی پایه' برای {symbol_underlying} نامعتبر است. لطفاً مقدار را به‌صورت دستی وارد کنید.")
        underlying_buy_fee = get_user_input_float(f"🔹 لطفاً کارمزد خرید برای {symbol_underlying} را وارد کنید: ")

    print(f"✅ مقدار 'کارمزد خرید دارایی پایه': {underlying_buy_fee}")


    # Variable 8


    # تابع کمکی برای دریافت مقدار عددی از کاربر
    def get_user_input_float(prompt: str):
        """دریافت مقدار عددی از کاربر و اطمینان از معتبر بودن آن."""
        while True:
            user_input = input(prompt).strip().replace(",", "")  # حذف کاما برای اعداد فارسی
            try:
                return float(user_input)
            except ValueError:
                print("❌ مقدار وارد شده معتبر نیست. لطفاً فقط عدد وارد کنید.")

    # مقداردهی `futures_short_fee` و مدیریت خطاها
    try:
        futures_short_fee = futures_fees(asset=symbol_underlying, role="فروشنده", fee="معاملات")

        if futures_short_fee is None or not isinstance(futures_short_fee, (int, float)):
            raise ValueError("Invalid futures short fee")  # مقدار نامعتبر → دریافت ورودی از کاربر

    except (KeyError, ValueError, TypeError):
        print(f"⚠️ مقدار 'کارمزد فروش قرارداد آتی' برای {symbol_underlying} نامعتبر است. لطفاً مقدار را به‌صورت دستی وارد کنید.")
        futures_short_fee = get_user_input_float(f"🔹 لطفاً کارمزد فروش برای {symbol_underlying} را وارد کنید: ")

    print(f"✅ مقدار 'کارمزد فروش قرارداد آتی': {futures_short_fee}")


    # Variable 9

    # تابع کمکی برای دریافت مقدار عددی از کاربر
    def get_user_input_float(prompt: str):
        """دریافت مقدار عددی از کاربر و اطمینان از معتبر بودن آن."""
        while True:
            user_input = input(prompt).strip().replace(",", "")  # حذف کاما برای اعداد فارسی
            try:
                return float(user_input)
            except ValueError:
                print("❌ مقدار وارد شده معتبر نیست. لطفاً فقط عدد وارد کنید.")

    # مقداردهی `futures_settlement_delivery_fees` و مدیریت خطاها
    try:
        futures_settlement_delivery_fees = futures_fees(asset=symbol_underlying, role="فروشنده", fee="تسویه و تحویل")

        if futures_settlement_delivery_fees is None or not isinstance(futures_settlement_delivery_fees, (int, float)):
            raise ValueError("Invalid futures settlement/delivery fees")  # مقدار نامعتبر → دریافت ورودی از کاربر

    except (KeyError, ValueError, TypeError):
        print(f"⚠️ مقدار 'کارمزد تسویه و تحویل قرارداد آتی' برای {symbol_underlying} نامعتبر است. لطفاً مقدار را به‌صورت دستی وارد کنید.")
        futures_settlement_delivery_fees = get_user_input_float(f"🔹 لطفاً کارمزد تسویه و تحویل برای {symbol_underlying} را وارد کنید: ")

    print(f"✅ مقدار 'کارمزد تسویه و تحویل قرارداد آتی': {futures_settlement_delivery_fees}")

    # Variable 10

    warehousing_taxes = 0

    print(f"✅ مقدار 'کارمزد انبارداری و مالیات قرارداد آتی': {warehousing_taxes}")


    results = []

    for contract in future_contracts:
        # Get the values for each contract
        futures_price_contract = futures_price[contract]
        contract_size_contract = contract_size[contract]
        day_until_maturity_contract = day_until_maturity[contract]
        initial_margin_contract = initial_margin[contract]
        
        if contract_size_contract <= 0 or day_until_maturity_contract <= 0:
            raise ValueError("Contract size and days until maturity must be greater than zero.")

        # Arbitrage Profit Calculation
        arbitrage_profit = contract_size_contract * (futures_price_contract - underlying_price)

        # Additional Costs
        additional_costs = (
            (contract_size_contract * underlying_price * underlying_buy_fee) +
            (contract_size_contract * futures_price_contract * futures_short_fee) +
            (contract_size_contract * futures_price_contract * futures_settlement_delivery_fees) +
            warehousing_taxes
        )

        # Opportunity Cost
        invested_capital = (contract_size_contract * underlying_price) + initial_margin_contract + additional_costs
        opportunity_cost = invested_capital * ((risk_free_rate / 365) * day_until_maturity_contract)

        # Maturity & Annualized Arbitrage Profit
        maturity_arbitrage_profit = arbitrage_profit / (invested_capital + opportunity_cost)
        annual_arbitrage_profit = (maturity_arbitrage_profit / day_until_maturity_contract) * 365

        # Future Value Calculation
        future_value = underlying_price * np.exp((risk_free_rate - np.log(1 + (dividend / underlying_price))) * (day_until_maturity_contract / 365))

        # Store the results for this contract
        results.append({
            "day until maturity": day_until_maturity_contract,
            "arbitrage profit": arbitrage_profit,
            "additional costs": additional_costs,
            "opportunity cost": opportunity_cost,
            "maturity arbitrage profit": round(maturity_arbitrage_profit, 2),
            "annual arbitrage profit": round(annual_arbitrage_profit, 2),
            "future value": round(future_value, 2)
        })

    # Convert the results into a DataFrame
    df_results = pd.DataFrame(results, index=future_contracts)

    return df_results

