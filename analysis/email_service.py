from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import os
import tempfile
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class EmailReportService:
    """Service for sending analysis reports via email"""
    
    def __init__(self):
        self.from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@tradeanalyzer.com')
    
    def send_analysis_report(self, 
                           recipient_email: str, 
                           analysis_data: Dict, 
                           report_type: str = 'pdf',
                           subject: str = None) -> bool:
        """
        Send analysis report via email
        
        Args:
            recipient_email: Email address to send report to
            analysis_data: Analysis data dictionary
            report_type: Type of report ('pdf' or 'excel')
            subject: Custom email subject
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Generate report file
            if report_type.lower() == 'pdf':
                from .pdf_generator import create_pdf_report
                report_path = create_pdf_report(analysis_data)
                attachment_name = 'portfolio_analysis_report.pdf'
            elif report_type.lower() == 'excel':
                from .excel_export import create_excel_report
                report_path = create_excel_report(analysis_data)
                attachment_name = 'portfolio_analysis.xlsx'
            else:
                raise ValueError(f"Unsupported report type: {report_type}")
            
            # Create email subject
            if not subject:
                subject = f"Portfolio Analysis Report - {analysis_data.get('response2', 'N/A')} Score"
            
            # Create email body
            html_content = self.create_email_html(analysis_data)
            text_content = self.create_email_text(analysis_data)
            
            # Create email message
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=self.from_email,
                to=[recipient_email]
            )
            
            # Attach HTML version
            email.attach_alternative(html_content, "text/html")
            
            # Attach report file
            with open(report_path, 'rb') as f:
                email.attach(attachment_name, f.read(), 
                           'application/pdf' if report_type == 'pdf' else 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            
            # Send email
            email.send()
            
            # Clean up temporary file
            if os.path.exists(report_path):
                os.remove(report_path)
            
            logger.info(f"Analysis report sent successfully to {recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send analysis report to {recipient_email}: {str(e)}")
            return False
    
    def create_email_html(self, analysis_data: Dict) -> str:
        """Create HTML email content"""
        score = analysis_data.get('response2', 'N/A')
        metrics = analysis_data.get('last_value', {})
        ai_analysis = analysis_data.get('response1', 'No analysis available')
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f8f9fa;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .score-circle {{
                    width: 80px;
                    height: 80px;
                    border-radius: 50%;
                    background: white;
                    color: #667eea;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 24px;
                    font-weight: bold;
                    margin: 0 auto 20px;
                }}
                .metrics-grid {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                    margin: 20px 0;
                }}
                .metric-card {{
                    background: white;
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .metric-value {{
                    font-size: 18px;
                    font-weight: bold;
                    color: #667eea;
                }}
                .metric-label {{
                    font-size: 12px;
                    color: #666;
                    margin-top: 5px;
                }}
                .ai-analysis {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                    border-left: 4px solid #667eea;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Portfolio Analysis Report</h1>
                <div class="score-circle">{score}</div>
                <p>Your AI-Powered Performance Score</p>
            </div>
            
            <div class="content">
                <h2>Key Performance Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{metrics.get('max_drawdown', 'N/A')}</div>
                        <div class="metric-label">Maximum Drawdown</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{metrics.get('win_loss_ratio', 'N/A')}</div>
                        <div class="metric-label">Win/Loss Ratio</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{metrics.get('sharpe_ratio', 'N/A')}</div>
                        <div class="metric-label">Sharpe Ratio</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{metrics.get('cumulative_returns', 'N/A')}%</div>
                        <div class="metric-label">Cumulative Returns</div>
                    </div>
                </div>
                
                <div class="ai-analysis">
                    <h3>🤖 AI Analysis</h3>
                    <p>{ai_analysis}</p>
                </div>
                
                <p><strong>📎 Attached:</strong> Complete analysis report with detailed charts and recommendations.</p>
            </div>
            
            <div class="footer">
                <p>Generated by TradeAnalyzer Pro</p>
                <p>This report was automatically generated based on your trading data analysis.</p>
            </div>
        </body>
        </html>
        """
        return html_content
    
    def create_email_text(self, analysis_data: Dict) -> str:
        """Create plain text email content"""
        score = analysis_data.get('response2', 'N/A')
        metrics = analysis_data.get('last_value', {})
        ai_analysis = analysis_data.get('response1', 'No analysis available')
        
        text_content = f"""
Portfolio Analysis Report

Your AI-Powered Performance Score: {score}

Key Performance Metrics:
- Maximum Drawdown: {metrics.get('max_drawdown', 'N/A')}
- Win/Loss Ratio: {metrics.get('win_loss_ratio', 'N/A')}
- Sharpe Ratio: {metrics.get('sharpe_ratio', 'N/A')}
- Sortino Ratio: {metrics.get('sortino_ratio', 'N/A')}
- Cumulative Returns: {metrics.get('cumulative_returns', 'N/A')}%
- Calmar Ratio: {metrics.get('calmar_ratio', 'N/A')}

AI Analysis:
{ai_analysis}

A detailed report with charts and recommendations is attached to this email.

Generated by TradeAnalyzer Pro
        """
        return text_content
    
    def send_bulk_reports(self, 
                         recipient_emails: List[str], 
                         analysis_data: Dict, 
                         report_type: str = 'pdf') -> Dict[str, bool]:
        """
        Send reports to multiple recipients
        
        Args:
            recipient_emails: List of email addresses
            analysis_data: Analysis data dictionary
            report_type: Type of report ('pdf' or 'excel')
            
        Returns:
            Dict mapping email addresses to success status
        """
        results = {}
        
        for email in recipient_emails:
            try:
                success = self.send_analysis_report(email, analysis_data, report_type)
                results[email] = success
            except Exception as e:
                logger.error(f"Failed to send report to {email}: {str(e)}")
                results[email] = False
        
        return results
    
    def send_scheduled_report(self, 
                            recipient_email: str, 
                            analysis_data: Dict,
                            schedule_type: str = 'weekly') -> bool:
        """
        Send scheduled reports (for future implementation with Celery)
        
        Args:
            recipient_email: Email address
            analysis_data: Analysis data
            schedule_type: 'daily', 'weekly', 'monthly'
            
        Returns:
            bool: Success status
        """
        subject = f"Scheduled {schedule_type.title()} Portfolio Analysis Report"
        return self.send_analysis_report(recipient_email, analysis_data, 'pdf', subject)

# Convenience functions
def send_pdf_report(email: str, analysis_data: Dict) -> bool:
    """Send PDF report via email"""
    service = EmailReportService()
    return service.send_analysis_report(email, analysis_data, 'pdf')

def send_excel_report(email: str, analysis_data: Dict) -> bool:
    """Send Excel report via email"""
    service = EmailReportService()
    return service.send_analysis_report(email, analysis_data, 'excel')

def send_both_reports(email: str, analysis_data: Dict) -> Dict[str, bool]:
    """Send both PDF and Excel reports"""
    service = EmailReportService()
    results = {}
    
    results['pdf'] = service.send_analysis_report(email, analysis_data, 'pdf')
    results['excel'] = service.send_analysis_report(email, analysis_data, 'excel')
    
    return results
