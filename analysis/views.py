from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from io import TextIOWrapper
import csv
import pandas as pd
from .final_analysis import *
from sample_data_generator import *
import openai
import os
from .pdf_generator import create_pdf_report
from .excel_export import create_excel_report
from .email_service import EmailReportService
import json

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

def export_pdf(request):
    """Export analysis results as PDF"""
    if request.method == 'POST':
        try:
            # Get analysis data from session or request
            analysis_data = json.loads(request.body)
            
            # Generate PDF report
            pdf_path = create_pdf_report(analysis_data)
            
            # Return PDF file
            with open(pdf_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="portfolio_analysis_report.pdf"'
                
                # Clean up temporary file
                os.remove(pdf_path)
                return response
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def export_excel(request):
    """Export analysis results as Excel"""
    if request.method == 'POST':
        try:
            # Get analysis data from session or request
            analysis_data = json.loads(request.body)
            
            # Generate Excel report
            excel_path = create_excel_report(analysis_data)
            
            # Return Excel file
            with open(excel_path, 'rb') as excel_file:
                response = HttpResponse(excel_file.read(), 
                                      content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="portfolio_analysis.xlsx"'
                
                # Clean up temporary file
                os.remove(excel_path)
                return response
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def send_email_report(request):
    """Send analysis report via email"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            analysis_data = data.get('analysis_data')
            report_type = data.get('report_type', 'pdf')
            
            if not email or not analysis_data:
                return JsonResponse({'error': 'Email and analysis data required'}, status=400)
            
            # Send email report
            email_service = EmailReportService()
            success = email_service.send_analysis_report(email, analysis_data, report_type)
            
            if success:
                return JsonResponse({'message': 'Report sent successfully!'})
            else:
                return JsonResponse({'error': 'Failed to send email'}, status=500)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

