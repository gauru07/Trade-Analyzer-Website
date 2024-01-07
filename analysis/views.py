from django.shortcuts import render,redirect
from django.http import HttpResponse
from io import TextIOWrapper
import csv
import pandas as pd
from .final_analysis import *
from sample_data_generator import *
import openai
import os
openai.organization = os.environ.get("OPENAI_ORG_ID")
openai.api_key = os.environ.get("OPENAI_API_KEY")


def csv_upload(request):
    if request.method == 'POST':


        csv_file = request.FILES.get('csv_file')

        if csv_file is None:
            return HttpResponse("No file uploaded.")

        with TextIOWrapper(csv_file, encoding=request.encoding) as text_file:
            reader = csv.reader(text_file)
            csv_contents = [row for row in reader]


        df = pd.DataFrame(csv_contents[1:], columns=csv_contents[0])
        df['datetime'] = pd.to_datetime(df['datetime'])


        df['price'] = df['price'].astype(float)
        df['quantity'] = df['quantity'].astype(int)
        



        response2=4
        response1="The trader's purchase of INFY stock suggests that he or she believes the stock is undervalued at its current price relative to its earnings and should appreciate in price. Another financial ratio that is useful for analyzing the performance of the trader is the price-to-book (P/B) ratio, which is calculated by dividing the current stock price by its book value. The higher the P/B ratio, the more expensive the stock is relative to its book value. The trader's purchase of INFY suggests that he or she believes the stock is undervalued at its current price relative to its"
        try:
            last_row = df.tail(1).to_string(index=False)
            prompt1 = f"Can you provide an analysis of the trader's(not about how much quantity he bought but about what are different types of financial ratio) performance based on the following data?\n\n{last_row}"
            prompt2 = f"Please rate the trader's performance between 0.0 and 10.0 on the basis of {last_row}:"

            completion1 = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt1,
                max_tokens=200
            )

            response1 = completion1.choices[0].text.strip()

            completion2 = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt2,
                max_tokens=5,  
                temperature=0.0,  
                stop=None
            )

            response2 = completion2.choices[0].text.strip()

            print(response1,response2)
        except Exception as e:
            print(str(e))



        df = calculation(df)

        df.dropna(inplace=True)

        diction = df.iloc[-1].to_dict()
        diction = {key: round(value, 2) for key, value in diction.items() if key != 'datetime' and type(value)!=str}

        print(df)
        context = {
            'datetime': df['datetime'].dt.strftime('%y %m-%d ').tolist(),
            'max_drawdown': df['max_drawdown'].tolist(),
            'win_loss': df['win_loss_ratio'].tolist(),
            'sortino_ratio': df['sortino_ratio'].tolist(),
            'sharpe_ratio': df['sharpe_ratio'].tolist(),
            'cumulative_returns':df['cumulative_returns'].tolist(),
            'standard_deviation':df['standard_deviation'].tolist(),
            'excess_returns':df['excess_returns'].tolist(),
            'information_ratio':df['information_ratio'].tolist(),
            'calmar_ratio':df['calmar_ratio'].tolist(),
            'response1': response1,
            'response2': response2,
            'last_value':diction
        }
        return render(request, 'analysis_final.html', context)

    return render(request, "file_upload.html")

def analysis_data(request):
    generate()

    df=pd.read_csv('./sample_data.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])


    df['price'] = df['price'].astype(float)
    df['quantity'] = df['quantity'].astype(int)
    
    response2=4
    response1="The trader's purchase of INFY stock suggests that he or she believes the stock is undervalued at its current price relative to its earnings and should appreciate in price. Another financial ratio that is useful for analyzing the performance of the trader is the price-to-book (P/B) ratio, which is calculated by dividing the current stock price by its book value. The higher the P/B ratio, the more expensive the stock is relative to its book value. The trader's purchase of INFY suggests that he or she believes the stock is undervalued at its current price relative to its"
    try:
        last_row = df.tail(1).to_string(index=False)
        prompt1 = f"Can you provide an analysis of the trader's(not about how much quantity he bought but about what are different types of financial ratio) performance based on the following data?\n\n{last_row}"
        prompt2 = f"Please rate the trader's performance between 0.0 and 10.0 on the basis of {last_row}:"

        completion1 = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt1,
            max_tokens=200
        )

        response1 = completion1.choices[0].text.strip()

        completion2 = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt2,
            max_tokens=5,  # Limit to a few tokens to force a floating number response
            temperature=0.0,  # Set temperature to 0.0 for deterministic output
            stop=None  # Disable the default stop sequence
        )

        response2 = completion2.choices[0].text.strip()

        print(response1,response2)
    except Exception as e:
        print(str(e))


    df = calculation(df)

    df.dropna(inplace=True)
    diction = df.iloc[-1].to_dict()
    diction = {key: round(value, 2) for key, value in diction.items() if key != 'datetime' and type(value)!=str}

    print(df)
    context = {
        'datetime': df['datetime'].dt.strftime('%m-%d ').tolist(),
        'max_drawdown': df['max_drawdown'].tolist(),
        'win_loss': df['win_loss_ratio'].tolist(),
        'sortino_ratio': df['sortino_ratio'].tolist(),
        'sharpe_ratio': df['sharpe_ratio'].tolist(),
        'cumulative_returns':df['cumulative_returns'].tolist(),
        'standard_deviation':df['standard_deviation'].tolist(),
        'excess_returns':df['excess_returns'].tolist(),
        'information_ratio':df['information_ratio'].tolist(),
        'calmar_ratio':df['calmar_ratio'].tolist(),
        'response1': response1,
        'response2': response2,
        'last_value':diction
    }

    return render(request, 'analysis_final.html', context)

