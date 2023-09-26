#import yfinance
import yfinance as yf
import pandas as pd

#import yfinance CSV data
import csv

# Open the CSV file
with open('constituents_csv.csv', 'r') as csv_file:
    # Create a CSV reader
    csv_reader = csv.reader(csv_file)

    # Convert CSV to a list of dictionaries
    csv_data = [row for row in csv_reader]

# Close the CSV file
csv_file.close()

# Prompt the user to enter a stock symbol
stock_symbol = input("Enter a stock symbol: ")

try:
    # Use yf.Ticker to fetch data for the entered stock symbol
    ticker = yf.Ticker(stock_symbol)

    # Access and print information about the stock (e.g., stock name, price, etc.)
    stock_name = ticker.info["shortName"]
    stock_price = ticker.history(period="1d")["Close"].iloc[0]

    print(f"Stock Name: {stock_name}")
    print(f"Current Price: ${stock_price:.2f}")
except ValueError:
    print("Invalid stock symbol or unable to fetch data.")
except Exception as e:
    print(f"An error occurred: {str(e)}")

msft = yf.Ticker("MSFT")

#Altman Z-Score Calculation to Assess Financial Health of a Stock
balance_sheet = ticker.balance_sheet
income_statement = ticker.income_stmt

#Pulling Current Asset Data from yfinance Balance Sheet Dataframe
ca = balance_sheet.loc[['Current Assets']]
current_assets = ca.iloc[0,0]

#Pulling Total Asset Data from yfinance Balance Sheet Dataframe
ta = balance_sheet.loc[["Total Assets"]]
total_assets = ta.iloc[0,0]

#Pulling Current Liabilities Data
cl = balance_sheet.loc[["Current Liabilities"]]
current_liabilities = cl.iloc[0,0]

working_capital = current_assets - current_liabilities

#Retained Earnings which is Capital Reinvested into the Company
re = balance_sheet.loc[["Retained Earnings"]]
retained_earnings = re.iloc[0,0]

#EBIT = Earnings before Interest and Taxes
earnings_before_interest_taxes = income_statement.loc[["EBIT"]]
ebit = earnings_before_interest_taxes.iloc[0,0]

market_cap = ticker.info["marketCap"]

#Total Liabilities of Stock
tl = balance_sheet.loc[['Total Liabilities Net Minority Interest']]
total_liabilities = tl.iloc[0,0]

#Total Revenue (aka Sales)
tr = income_statement.loc[["Total Revenue"]]
total_revenue = tr.iloc[0,0]

#Interest Expense
ie = income_statement.loc[['Interest Expense']]
interest_expense = ie.iloc[0,0]

total_debt = ticker.info['totalDebt']

total_equity = ticker.info["bookValue"] * ticker.info["impliedSharesOutstanding"]

a1 = working_capital / total_assets
b1 = retained_earnings / total_assets
c1 = ebit / total_assets
d1 = market_cap / total_liabilities
e1 = total_revenue / total_assets

z_score = (a1 * 1.2) + (b1 * 1.4) + (c1 * 3.3) + (d1 * 0.6) + (e1 * 1)

ncav = (current_assets - total_liabilities) / ticker.info["impliedSharesOutstanding"]

print(f"The net current asset value for {stock_name} is ${ncav:.2f}")

if z_score > 3:
  print(f"The Altman Z-Score for {stock_name} is {z_score:.2f}. This means {stock_name} is financially healthy and low risk for experiencing financial trouble.")

elif 1.8 <= z_score <= 3:
  print(f"The Altman Z-Score for {stock_name} is {z_score:.2f}. This means that {stock_name} is at moderate risk for experiencing financial trouble.")

elif 0 <= z_score < 1.8:
  print(f"The Altman Z-Score for {stock_name} is {z_score:.2f}. This means that {stock_name} is at high risk for experiencing financial trouble.")

elif z_score < 0:
  print(f"The Altman Z-Score for {stock_name} is {z_score:.2f}. This means that {stock_name} is at very high risk for experiencing financial trouble and chances for bankruptcy are high.")

# Get the percentage input from the user
fcf_growth_rate_input = input("Enter a percentage which is the projected free cash flow growth rate over the next 5 years (e.g., 5%: ): ")

# Remove the '%' symbol and convert the input to a float
try:
    fcf_growth_rate = float(fcf_growth_rate_input.rstrip('%')) / 100
except ValueError:
    print("Invalid input. Please enter a valid percentage.")
    exit()

#Normalized Projected Dividend Yield (aka Capitalization Rate)
fcf_yield = ticker.info["freeCashflow"] / ticker.info["marketCap"]
#Current Free Cash Flow for Stock (y0 = Year 0)
y0_fcf = ticker.info["freeCashflow"]
#Weighted Average Cost of Capital (WACC)
book_value_of_equity = ticker.info["bookValue"] * ticker.info["impliedSharesOutstanding"]
total_debt = ticker.info["totalDebt"]
debt_and_equity = book_value_of_equity + total_debt

#% of Company financed by debt
percentage_debt = total_debt / debt_and_equity
#% of Company financed by equity
percentage_equity = book_value_of_equity / debt_and_equity

#Risk free rate which roughly equates to current long-term US Treasury Yields
risk_free_rate = .05
beta = ticker.info["beta"]
#Expected long-term stock market return rate
mkt_rate_of_return = .08
#Cost of debt which roughly equals current US Corporate Bond Yields
cost_of_debt = .05
#Cost of equity which is based on the Capital Asset Pricing Model
cost_of_equity = risk_free_rate + (beta * (mkt_rate_of_return - risk_free_rate))
#Current Corporate Tax Rate
corporate_tax_rate = .21

#Weighted Average Cost of Capital formula (WACC)
wacc = (percentage_equity * cost_of_equity) + (percentage_debt * cost_of_debt *(1-corporate_tax_rate))

discount_rate = wacc

#Year 1 Discounted Cash Flow Formula
y1_fcf = y0_fcf * (1+(fcf_growth_rate))
y1_discount_factor = 1 / (1+(discount_rate)) ** 1
y1_dcf = y1_fcf * y1_discount_factor
#Year 2 Discounted Cash Flow Formula
y2_fcf = y1_fcf * (1+(fcf_growth_rate))
y2_discount_factor = 1 / (1+(discount_rate)) ** 2
y2_dcf = y2_fcf * y2_discount_factor
#Year 3 Discounted Cash Flow Formula
y3_fcf = y2_fcf * (1+(fcf_growth_rate))
y3_discount_factor = 1 / (1+(discount_rate)) ** 3
y3_dcf = y3_fcf * y3_discount_factor
#Year 4 Discounted Cash Flow Formula
y4_fcf = y3_fcf * (1+(fcf_growth_rate))
y4_discount_factor = 1 / (1+(discount_rate)) ** 4
y4_dcf = y4_fcf * y4_discount_factor
#Year 5 Discounted Cash Flow Formula
y5_fcf = y4_fcf * (1+(fcf_growth_rate))
y5_discount_factor = 1 / (1+(discount_rate)) ** 5
y5_dcf = y5_fcf * y5_discount_factor

total_dcfs = (y1_dcf, y2_dcf, y3_dcf, y4_dcf, y5_dcf)

sum_dcfs = sum(total_dcfs)
pv_terminal_value = y5_dcf / fcf_yield

enterprise_value = pv_terminal_value + sum_dcfs
total_debt = ticker.info["totalDebt"]
total_cash = ticker.info["totalCash"]

equity_value = enterprise_value + total_debt - total_cash

shares_outstanding = ticker.info["impliedSharesOutstanding"]

equity_value_per_share = equity_value / shares_outstanding

print(f"{stock_name} has a free cash flow yield of {fcf_yield:.2%}, weighted average cost of capital of {wacc:.2%} and debt to equity ratio of {percentage_debt / percentage_equity:.2}")

print(f"You projected {stock_name} would grow free cash flows over the next 5 years by {fcf_growth_rate:.2%}. Based on this information, the intrinsic value of {stock_name} based on the 5 year discounted cash flow model is " +     "${:.2f}".format(round(float(equity_value_per_share), 2)))

stock_discount_percentage = 1 - (stock_price / equity_value_per_share)
stock_premium_percentage = (stock_price / equity_value_per_share) - 1

if stock_price < equity_value_per_share:
  print(f"Based on the current share price of {stock_name} of ${stock_price:.2f}, this implies that {stock_name} stock is undervalued and there is currently a {stock_discount_percentage:.2%} discount to the DCF fair market value of ${equity_value_per_share:.2f}")
elif stock_price > equity_value_per_share:
  print(f"Based on the current share price of {stock_name} of ${stock_price:.2f}, this implies that {stock_name} stock is overvalued and there is currently a {stock_premium_percentage:.2%} premium to the DCF fair market value of ${equity_value_per_share:.2f}")
elif stock_price == equity_value_per_share:
  print(f"Based on the current share price of {stock_name} of ${stock_price:.2f}, this implies that {stock_name} stock is fairly valued and the DCF fair market value matches the current stock price.")
