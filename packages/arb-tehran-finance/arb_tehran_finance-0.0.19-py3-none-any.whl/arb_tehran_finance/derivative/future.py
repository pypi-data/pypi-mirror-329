import numpy as np
underlying_price = 3_200_000 
futures_price = 4_500_000
contract_size = 10
risk_free_rate = 0.25    #annual risk free rate of return
day_until_maturity = 273    #The number of days left until the maturity
dividend = 0 # In Iran, the divudend should always be considered as zero because the divudend paid is considered in future price calculations
initial_margin = 7_600_000  #based on Irans traded futures #(وجه تضمین)
underlying_buy_fee = 0.0024
futures_short_fee = 0.0006
futures_settlement_delivery_fees = 0.005  #by delivering the underlying
warehousing_taxes = 89_271

def future_value (underlying_price , dividend , risk_free_rate , day_until_maturity):
    dividend_yield = np.log(1+(dividend/underlying_price))  #Calculation of continuous compounding rate for dividend
    future_value = underlying_price * np.exp((risk_free_rate-dividend_yield) *(day_until_maturity/365)) #future_value = underlying_price * ((1+((risk_free_rate-dividend_yield)/365))**day_until_maturity)
    return future_value

'''
future_value = future_value(underlying_price , dividend , risk_free_rate , day_until_maturity)
print(f"Future Value : {future_value :,.0f}")
'''


def future_arbitrage (underlying_price , futures_price , contract_size , dividend , risk_free_rate
                       , day_until_maturity , initial_margin , underlying_buy_fee , futures_short_fee
                         , futures_settlement_delivery_fees , warehousing_taxes):
    arbitrage_profit = contract_size * (futures_price - underlying_price)
    additional_costs = (contract_size * underlying_price * underlying_buy_fee) \
                    + (contract_size * futures_price * futures_short_fee) \
                    + (contract_size * futures_price * futures_settlement_delivery_fees) \
                    + warehousing_taxes
    opportunity_cost = ((contract_size * underlying_price) + initial_margin + additional_costs) * ((risk_free_rate / 365) * day_until_maturity)
    maturity_arbitrage_profit = arbitrage_profit / ((contract_size * underlying_price) + initial_margin + additional_costs + opportunity_cost)
    annually_arbitrage_profit = (maturity_arbitrage_profit / day_until_maturity) * 365
    return arbitrage_profit , additional_costs , opportunity_cost , maturity_arbitrage_profit , annually_arbitrage_profit

'''
arbitrage_profit, additional_costs, opportunity_cost, maturity_arbitrage_profit , annually_arbitrage_profit = future_arbitrage(
    underlying_price, futures_price, contract_size, dividend, risk_free_rate,
    day_until_maturity, initial_margin, underlying_buy_fee, futures_short_fee,
    futures_settlement_delivery_fees, warehousing_taxes)

print(f"arbitrage profit : {arbitrage_profit :,.0f} \nadditional costs : {additional_costs :,.0f} \nopportunity cost : {opportunity_cost :,.0f} \nmaturity arbitrage profit : {maturity_arbitrage_profit :,.2f}  \nannually arbitrage profit : {annually_arbitrage_profit :,.2f}")
'''