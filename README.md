# Financial Analyzer

> Note- So, I just discovered this that, I have hosted the website on render.com, so I think the server, gets slow when not used, so I would request you , wait for 30 sec-45 sec, if the website is not responding, then it will show you the results, Thanks 😅  

The Financial Analyzer is a tool designed to analyze trade history data. It takes a document containing trade history with specific columns and provides various insights and metrics related to the trades. This documentation provides an in-depth explanation of the project, its functionalities, and the underlying code.



https://github.com/sudhanshu8833/Financial_Analyzer/assets/84956779/b930471c-abc9-46b4-a2b4-b1a425b6c90d



## 1. Introduction
The Financial Analyzer is a Python-based tool that aims to help traders and investors analyze their trade history and gain valuable insights. It takes a document in CSV format as input, which should contain the following columns: Datetime, Stock, OrderType, Price, and Exchange. The analyzer performs calculations and generates metrics such as Compound Annual Growth Rate (CAGR), Return on Investment (ROI), Win/Loss Ratio, and Maximum Drawdown. It also provides visualizations of cumulative returns, daily returns, continuous returns, and ROI over time.



![Alt text](https://github.com/sudhanshu8833/Financial_Analyzer/blob/main/dashboard_pics/final_analysis.png)



## 2. Features
The Financial Analyzer offers the following features:
- Analyze trade history data and generate financial metrics
- Gives insights and rating using ChatGpt
- Calculate Compound Annual Growth Rate (CAGR)
- Calculate Sharpe ratio
- Calculate Win/Loss Ratio
- Calculate Maximum Drawdown
- Calculate calmar's ratio
- Calculate sortino's Ratio
> We also plotted all the ratio's with respect to time, in a continous fashion




## 3. Installation
To use the Financial Analyzer, follow these steps:
1. Clone the project repository: `git clone https://github.com/sudhanshu8833/Financial_Analyzer.git`
2. Install the required dependencies. See the Dependencies section for details. `pip3 install -r requirements.txt`
3. Open any terminal and change the working directory to the folder where the project is present.
4. Now run the command `python3 manage.py runserver`



## 4. Usage
1. Prepare the trade history data. To input using CSV files, make sure the columns are in the exact order as mentioned:
2. You can download the trade history data from broker directly, and make sure to change the names of column to below
> (datetime,stock,ordertype,price,quantity,Exchange)
3. Follow the on-screen instructions to input the name of your trade history file.
4. The analyzer will process the data, calculate metrics, and display the results along with the generated plots and ChatGpt insights.
5. Now suppose you do not possess data, and just wants to test how the website is working, You can do it by clicking `Upload Random data`

![Alt text](https://github.com/sudhanshu8833/Financial_Analyzer/blob/main/dashboard_pics/input_data.png)

## 5. Input Options:
1. Manual Input: Allow users to manually enter their trade history data into the web application.
2. File Formats: Extend the analyzer to support other file formats such as Excel spreadsheets, JSON files, or database integration to import trade data.
3. API Integration: Provide an option to connect to brokerage APIs or financial data providers to fetch trade history directly `future`



## 6. Code Explanation
The Financial Analyzer code is structured into several sections:
- Importing necessary libraries: The required libraries, including pandas, numpy, and matplotlib, are imported at the beginning of the code.
- Function Definitions: Functions for calculating CAGR, ROI, Win/Loss Ratio, Maximum Drawdown, and analyzing the financial statement are defined.
- Load and Prepare Data: The script prompts the user to input the name of the trade history file, loads the data using pandas, and performs sorting and data manipulation.
- Financial Statement Analysis: The data is analyzed using the defined functions, and the results are printed to the console.
- Plots: Various plots, including cumulative returns, daily returns, continuous returns, and ROI over time, are generated using matplotlib.



## 7. Dependencies
The Financial Analyzer code relies on the following dependencies:
(More exhaustive and complete list of requirements is mentioned in `requirements.txt`)

> To install it `pip3 install -r requirements.txt`

### mostly used API
- `pandas`: Used for data manipulation and analysis.
- `numpy`: Used for mathematical calculations and array operations.
- `matplotlib`: Used for data visualization and plotting.
- `openai` we used Open AI to access the profile of a trader.




## 8. Conclusion
The Financial Analyzer provides a valuable tool for traders and investors to analyze their trade history data. By calculating metrics such as CAGR, ROI, Win/Loss Ratio, and Maximum Drawdown, users can gain insights into their trading performance. The generated plots further aid in visualizing the cumulative returns, daily returns, continuous returns, and ROI over time. With this tool, traders can make informed decisions and improve their trading
