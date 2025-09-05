import pandas as pd
import xlsxwriter
from datetime import datetime
import os
from typing import Dict, List, Any

class ExcelReportGenerator:
    """Generate comprehensive Excel reports with multiple sheets and formatting"""
    
    def __init__(self):
        self.workbook = None
        self.worksheet = None
        
    def create_excel_report(self, analysis_data: Dict, output_path: str = 'portfolio_analysis.xlsx') -> str:
        """Create a comprehensive Excel report with multiple sheets"""
        
        # Create workbook with xlsxwriter for advanced formatting
        self.workbook = xlsxwriter.Workbook(output_path)
        
        # Define formats
        self.setup_formats()
        
        # Create different sheets
        self.create_summary_sheet(analysis_data)
        self.create_metrics_sheet(analysis_data)
        self.create_charts_data_sheet(analysis_data)
        self.create_detailed_analysis_sheet(analysis_data)
        self.create_recommendations_sheet(analysis_data)
        
        # Close workbook
        self.workbook.close()
        return output_path
    
    def setup_formats(self):
        """Setup Excel formatting styles"""
        self.formats = {
            'title': self.workbook.add_format({
                'bold': True,
                'font_size': 16,
                'font_color': '#667eea',
                'align': 'center',
                'valign': 'vcenter'
            }),
            'header': self.workbook.add_format({
                'bold': True,
                'font_size': 12,
                'bg_color': '#667eea',
                'font_color': 'white',
                'align': 'center',
                'valign': 'vcenter',
                'border': 1
            }),
            'metric_value': self.workbook.add_format({
                'font_size': 14,
                'font_color': '#667eea',
                'bold': True,
                'align': 'center',
                'num_format': '0.00'
            }),
            'metric_label': self.workbook.add_format({
                'font_size': 11,
                'align': 'left',
                'valign': 'vcenter'
            }),
            'data_cell': self.workbook.add_format({
                'font_size': 10,
                'align': 'center',
                'valign': 'vcenter',
                'border': 1
            }),
            'positive': self.workbook.add_format({
                'font_color': '#28a745',
                'bold': True
            }),
            'negative': self.workbook.add_format({
                'font_color': '#dc3545',
                'bold': True
            }),
            'neutral': self.workbook.add_format({
                'font_color': '#6c757d'
            })
        }
    
    def create_summary_sheet(self, analysis_data: Dict):
        """Create the executive summary sheet"""
        worksheet = self.workbook.add_worksheet('Executive Summary')
        
        # Title
        worksheet.merge_range('A1:F1', 'Portfolio Analysis Report', self.formats['title'])
        worksheet.write('A2', f'Generated on: {datetime.now().strftime("%B %d, %Y at %H:%M")}', self.formats['neutral'])
        
        # Performance Score
        worksheet.write('A4', 'Performance Score:', self.formats['metric_label'])
        score = analysis_data.get('response2', 'N/A')
        worksheet.write('B4', score, self.formats['metric_value'])
        
        # Key Metrics Summary
        worksheet.write('A6', 'Key Performance Metrics', self.formats['header'])
        
        metrics = analysis_data.get('last_value', {})
        row = 7
        
        metric_descriptions = {
            'max_drawdown': 'Maximum Drawdown',
            'win_loss_ratio': 'Win/Loss Ratio',
            'sharpe_ratio': 'Sharpe Ratio',
            'sortino_ratio': 'Sortino Ratio',
            'cumulative_returns': 'Cumulative Returns (%)',
            'calmar_ratio': 'Calmar Ratio'
        }
        
        for key, description in metric_descriptions.items():
            value = metrics.get(key, 'N/A')
            worksheet.write(f'A{row}', description, self.formats['metric_label'])
            worksheet.write(f'B{row}', value, self.formats['data_cell'])
            row += 1
        
        # AI Analysis
        worksheet.write('A15', 'AI Analysis', self.formats['header'])
        ai_analysis = analysis_data.get('response1', 'No analysis available')
        worksheet.merge_range('A16:F20', ai_analysis, self.formats['data_cell'])
        
        # Set column widths
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:F', 12)
    
    def create_metrics_sheet(self, analysis_data: Dict):
        """Create detailed metrics sheet"""
        worksheet = self.workbook.add_worksheet('Detailed Metrics')
        
        # Title
        worksheet.merge_range('A1:E1', 'Detailed Performance Metrics', self.formats['title'])
        
        # Headers
        headers = ['Metric', 'Value', 'Description', 'Benchmark', 'Status']
        for col, header in enumerate(headers):
            worksheet.write(2, col, header, self.formats['header'])
        
        # Metrics data
        metrics = analysis_data.get('last_value', {})
        row = 3
        
        metric_data = [
            ('Maximum Drawdown', metrics.get('max_drawdown', 'N/A'), 
             'Largest peak-to-trough decline', '< -10%', 'Good' if metrics.get('max_drawdown', 0) > -0.1 else 'Needs Improvement'),
            ('Win/Loss Ratio', metrics.get('win_loss_ratio', 'N/A'), 
             'Ratio of winning to losing trades', '> 1.0', 'Good' if metrics.get('win_loss_ratio', 0) > 1 else 'Needs Improvement'),
            ('Sharpe Ratio', metrics.get('sharpe_ratio', 'N/A'), 
             'Risk-adjusted return measure', '> 1.0', 'Good' if metrics.get('sharpe_ratio', 0) > 1 else 'Needs Improvement'),
            ('Sortino Ratio', metrics.get('sortino_ratio', 'N/A'), 
             'Downside risk-adjusted return', '> 1.0', 'Good' if metrics.get('sortino_ratio', 0) > 1 else 'Needs Improvement'),
            ('Cumulative Returns', f"{metrics.get('cumulative_returns', 'N/A')}%", 
             'Total portfolio return', '> 10%', 'Good' if metrics.get('cumulative_returns', 0) > 10 else 'Needs Improvement'),
            ('Calmar Ratio', metrics.get('calmar_ratio', 'N/A'), 
             'Return vs maximum drawdown', '> 1.0', 'Good' if metrics.get('calmar_ratio', 0) > 1 else 'Needs Improvement')
        ]
        
        for metric_name, value, description, benchmark, status in metric_data:
            worksheet.write(row, 0, metric_name, self.formats['metric_label'])
            worksheet.write(row, 1, value, self.formats['data_cell'])
            worksheet.write(row, 2, description, self.formats['data_cell'])
            worksheet.write(row, 3, benchmark, self.formats['data_cell'])
            
            # Color code status
            if 'Good' in status:
                worksheet.write(row, 4, status, self.formats['positive'])
            else:
                worksheet.write(row, 4, status, self.formats['negative'])
            
            row += 1
        
        # Set column widths
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 35)
        worksheet.set_column('D:D', 15)
        worksheet.set_column('E:E', 20)
    
    def create_charts_data_sheet(self, analysis_data: Dict):
        """Create sheet with chart data for further analysis"""
        worksheet = self.workbook.add_worksheet('Chart Data')
        
        # Title
        worksheet.merge_range('A1:H1', 'Time Series Data for Charts', self.formats['title'])
        
        # Headers
        headers = ['Date', 'Max Drawdown', 'Win/Loss Ratio', 'Sortino Ratio', 
                  'Cumulative Returns', 'Sharpe Ratio', 'Calmar Ratio']
        
        for col, header in enumerate(headers):
            worksheet.write(2, col, header, self.formats['header'])
        
        # Data
        datetime_list = analysis_data.get('datetime', [])
        max_drawdown = analysis_data.get('max_drawdown', [])
        win_loss = analysis_data.get('win_loss', [])
        sortino_ratio = analysis_data.get('sortino_ratio', [])
        cumulative_returns = analysis_data.get('cumulative_returns', [])
        sharpe_ratio = analysis_data.get('sharpe_ratio', [])
        calmar_ratio = analysis_data.get('calmar_ratio', [])
        
        row = 3
        for i in range(len(datetime_list)):
            worksheet.write(row, 0, datetime_list[i], self.formats['data_cell'])
            worksheet.write(row, 1, max_drawdown[i] if i < len(max_drawdown) else '', self.formats['data_cell'])
            worksheet.write(row, 2, win_loss[i] if i < len(win_loss) else '', self.formats['data_cell'])
            worksheet.write(row, 3, sortino_ratio[i] if i < len(sortino_ratio) else '', self.formats['data_cell'])
            worksheet.write(row, 4, cumulative_returns[i] if i < len(cumulative_returns) else '', self.formats['data_cell'])
            worksheet.write(row, 5, sharpe_ratio[i] if i < len(sharpe_ratio) else '', self.formats['data_cell'])
            worksheet.write(row, 6, calmar_ratio[i] if i < len(calmar_ratio) else '', self.formats['data_cell'])
            row += 1
        
        # Set column widths
        for col in range(7):
            worksheet.set_column(col, col, 15)
    
    def create_detailed_analysis_sheet(self, analysis_data: Dict):
        """Create detailed analysis sheet"""
        worksheet = self.workbook.add_worksheet('Detailed Analysis')
        
        # Title
        worksheet.merge_range('A1:D1', 'Detailed Financial Analysis', self.formats['title'])
        
        # Risk Analysis
        worksheet.write('A3', 'Risk Analysis', self.formats['header'])
        worksheet.write('A4', 'Maximum Drawdown:', self.formats['metric_label'])
        worksheet.write('B4', analysis_data.get('last_value', {}).get('max_drawdown', 'N/A'), self.formats['metric_value'])
        
        worksheet.write('A5', 'Volatility (Std Dev):', self.formats['metric_label'])
        worksheet.write('B5', analysis_data.get('last_value', {}).get('standard_deviation', 'N/A'), self.formats['metric_value'])
        
        # Return Analysis
        worksheet.write('A7', 'Return Analysis', self.formats['header'])
        worksheet.write('A8', 'Cumulative Returns:', self.formats['metric_label'])
        worksheet.write('B8', f"{analysis_data.get('last_value', {}).get('cumulative_returns', 'N/A')}%", self.formats['metric_value'])
        
        worksheet.write('A9', 'Excess Returns:', self.formats['metric_label'])
        worksheet.write('B9', analysis_data.get('last_value', {}).get('excess_returns', 'N/A'), self.formats['metric_value'])
        
        # Risk-Adjusted Returns
        worksheet.write('A11', 'Risk-Adjusted Returns', self.formats['header'])
        worksheet.write('A12', 'Sharpe Ratio:', self.formats['metric_label'])
        worksheet.write('B12', analysis_data.get('last_value', {}).get('sharpe_ratio', 'N/A'), self.formats['metric_value'])
        
        worksheet.write('A13', 'Sortino Ratio:', self.formats['metric_label'])
        worksheet.write('B13', analysis_data.get('last_value', {}).get('sortino_ratio', 'N/A'), self.formats['metric_value'])
        
        worksheet.write('A14', 'Calmar Ratio:', self.formats['metric_label'])
        worksheet.write('B14', analysis_data.get('last_value', {}).get('calmar_ratio', 'N/A'), self.formats['metric_value'])
        
        # Information Ratio
        worksheet.write('A16', 'Information Ratio:', self.formats['metric_label'])
        worksheet.write('B16', analysis_data.get('last_value', {}).get('information_ratio', 'N/A'), self.formats['metric_value'])
        
        # Set column widths
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 15)
    
    def create_recommendations_sheet(self, analysis_data: Dict):
        """Create recommendations sheet"""
        worksheet = self.workbook.add_worksheet('Recommendations')
        
        # Title
        worksheet.merge_range('A1:C1', 'Trading Recommendations', self.formats['title'])
        
        # Generate recommendations based on metrics
        recommendations = self.generate_recommendations(analysis_data.get('last_value', {}))
        
        worksheet.write('A3', 'Recommendation', self.formats['header'])
        worksheet.write('B3', 'Priority', self.formats['header'])
        worksheet.write('C3', 'Description', self.formats['header'])
        
        row = 4
        for rec in recommendations:
            worksheet.write(row, 0, rec['recommendation'], self.formats['metric_label'])
            worksheet.write(row, 1, rec['priority'], self.formats['data_cell'])
            worksheet.write(row, 2, rec['description'], self.formats['data_cell'])
            row += 1
        
        # Set column widths
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 50)
    
    def generate_recommendations(self, metrics: Dict) -> List[Dict]:
        """Generate trading recommendations based on metrics"""
        recommendations = []
        
        sharpe_ratio = metrics.get('sharpe_ratio', 0)
        max_drawdown = metrics.get('max_drawdown', 0)
        win_loss_ratio = metrics.get('win_loss_ratio', 0)
        sortino_ratio = metrics.get('sortino_ratio', 0)
        
        if sharpe_ratio < 1:
            recommendations.append({
                'recommendation': 'Improve Risk-Adjusted Returns',
                'priority': 'High',
                'description': 'Sharpe ratio below 1.0 indicates poor risk-adjusted returns. Consider reducing portfolio volatility or improving returns.'
            })
        
        if max_drawdown < -0.2:
            recommendations.append({
                'recommendation': 'Implement Risk Management',
                'priority': 'High',
                'description': 'High maximum drawdown detected. Implement stop-loss strategies and position sizing rules.'
            })
        
        if win_loss_ratio < 1:
            recommendations.append({
                'recommendation': 'Improve Trade Selection',
                'priority': 'Medium',
                'description': 'Win/loss ratio below 1.0 indicates more losing trades than winning ones. Focus on improving trade selection criteria.'
            })
        
        if sortino_ratio > 2:
            recommendations.append({
                'recommendation': 'Maintain Current Strategy',
                'priority': 'Low',
                'description': 'Excellent downside risk management. Continue with current approach while monitoring performance.'
            })
        
        if not recommendations:
            recommendations.append({
                'recommendation': 'Continue Current Approach',
                'priority': 'Low',
                'description': 'Portfolio shows balanced performance across key metrics. Continue current strategy with regular monitoring.'
            })
        
        return recommendations

# Convenience function
def create_excel_report(analysis_data: Dict, output_path: str = 'portfolio_analysis.xlsx') -> str:
    """Create Excel report from analysis data"""
    generator = ExcelReportGenerator()
    return generator.create_excel_report(analysis_data, output_path)
