# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# def calculate_cumulative_returns(df):
#     df['returns'] = df['price'].pct_change()
#     df['cumulative_returns'] = (1 + df['returns']).cumprod()
#     return df

# def calculate_max_drawdown(df):
#     df['cumulative_returns'] = df['cumulative_returns'].ffill()
#     df['daily_drawdown'] = df['cumulative_returns'] / df['cumulative_returns'].cummax() - 1
#     df['max_drawdown'] = df['daily_drawdown'].cummin()
#     return df

# def calculate_win_loss_ratio(df):
#     df['gain'] = df['returns'].apply(lambda x: x if x > 0 else 0)
#     df['loss'] = df['returns'].apply(lambda x: -x if x < 0 else 0)
#     df['win_loss_ratio'] = df['gain'].cumsum() / abs(df['loss'].cumsum())
#     return df

# def calculation(df):

#     # Convert the 'datetime' column to datetime type for further calculations
#     df['datetime'] = pd.to_datetime(df['datetime'])

#     # Calculate cumulative returns
#     df = calculate_cumulative_returns(df)

#     # Calculate max drawdown
#     df = calculate_max_drawdown(df)

#     # Calculate win/loss ratio
#     df = calculate_win_loss_ratio(df)

#     # Calculate overall Cumulative Returns
#     overall_cumulative_returns = (1 + df['returns']).prod() - 1

#     # Calculate overall Max Drawdown
#     overall_max_drawdown = df['max_drawdown'].min()

#     # Calculate overall Win/Loss Ratio
#     overall_win_loss_ratio = df['gain'].sum() / abs(df['loss'].sum())

#     print("Overall Cumulative Returns:")
#     print(overall_cumulative_returns)

#     print("\nOverall Max Drawdown:")
#     print(overall_max_drawdown)

#     print("\nOverall Win/Loss Ratio:")
#     print(overall_win_loss_ratio)

#     return df

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_cumulative_returns(df):
    df['returns'] = df['price'].pct_change()
    df['cumulative_returns'] = (1 + df['returns']).cumprod()
    return df

def calculate_max_drawdown(df):
    df['cumulative_returns'] = df['cumulative_returns'].ffill()
    df['daily_drawdown'] = df['cumulative_returns'] / df['cumulative_returns'].cummax() - 1
    df['max_drawdown'] = df['daily_drawdown'].cummin()
    return df

def calculate_win_loss_ratio(df):
    df['gain'] = df['returns'].apply(lambda x: x if x > 0 else 0)
    df['loss'] = df['returns'].apply(lambda x: -x if x < 0 else 0)
    df['win_loss_ratio'] = df['gain'].cumsum() / abs(df['loss'].cumsum())
    return df



def calculate_additional_metrics(df, market_returns, risk_free_rate=0.0):
    # Calculate Sharpe Ratio
    df['sharpe_ratio'] = (df['returns'] - risk_free_rate) / df['returns'].std()

    # Calculate Sortino Ratio
    df['downside_returns'] = df['returns'].apply(lambda x: x if x < 0 else 0)
    downside_volatility = df['downside_returns'].std()
    df['sortino_ratio'] = (df['returns'] - risk_free_rate) / downside_volatility

    # Calculate Standard Deviation
    df['standard_deviation'] = df['returns'].std()

    # Calculate Information Ratio
    df['excess_returns'] = df['returns'] - market_returns
    df['information_ratio'] = df['excess_returns'].mean() / df['excess_returns'].std()




    # Calculate Calmar Ratio
    df['daily_drawdown'] = df['cumulative_returns'] / df['cumulative_returns'].cummax() - 1
    df['max_drawdown'] = df['daily_drawdown'].cummin()
    df['calmar_ratio'] = df['returns'].mean() / abs(df['max_drawdown'].min())

    return df

def calculation(df, market_returns=0.05, risk_free_rate=0.0):
    # Convert the 'datetime' column to datetime type for further calculations
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Calculate cumulative returns
    df = calculate_cumulative_returns(df)

    # Calculate max drawdown
    df = calculate_max_drawdown(df)

    # Calculate win/loss ratio
    df = calculate_win_loss_ratio(df)

    # Calculate alpha and beta
    # df = calculate_alpha_beta(df, market_returns)

    # Calculate additional metrics
    df = calculate_additional_metrics(df, market_returns, risk_free_rate)

    return df


if(__name__=="__main__"):
    df=pd.read_csv("sample_data.csv")

    df = calculation(df)


    print(df)
