import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
import base64
from datetime import datetime
import os

class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Setup custom styles for the PDF"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#667eea')
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#333333')
        ))
        
        self.styles.add(ParagraphStyle(
            name='MetricValue',
            parent=self.styles['Normal'],
            fontSize=14,
            spaceAfter=6,
            textColor=colors.HexColor('#667eea'),
            alignment=TA_CENTER
        ))

    def create_chart_image(self, data, title, chart_type='line', color='#667eea'):
        """Create a chart and return as base64 image"""
        plt.style.use('seaborn-v0_8')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if chart_type == 'line':
            ax.plot(data, color=color, linewidth=2)
            ax.fill_between(range(len(data)), data, alpha=0.3, color=color)
        elif chart_type == 'bar':
            ax.bar(range(len(data)), data, color=color, alpha=0.7)
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('#f8f9fa')
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64

    def create_metrics_table(self, metrics):
        """Create a table of key metrics"""
        data = [
            ['Metric', 'Value', 'Description'],
            ['Performance Score', f"{metrics.get('score', 'N/A')}", 'AI-powered trader rating'],
            ['Maximum Drawdown', f"{metrics.get('max_drawdown', 'N/A')}", 'Largest peak-to-trough decline'],
            ['Win/Loss Ratio', f"{metrics.get('win_loss_ratio', 'N/A')}", 'Ratio of winning to losing trades'],
            ['Sharpe Ratio', f"{metrics.get('sharpe_ratio', 'N/A')}", 'Risk-adjusted return measure'],
            ['Sortino Ratio', f"{metrics.get('sortino_ratio', 'N/A')}", 'Downside risk-adjusted return'],
            ['Cumulative Returns', f"{metrics.get('cumulative_returns', 'N/A')}%", 'Total portfolio return'],
            ['Calmar Ratio', f"{metrics.get('calmar_ratio', 'N/A')}", 'Return vs maximum drawdown']
        ]
        
        table = Table(data, colWidths=[2*inch, 1.5*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
        ]))
        
        return table

    def generate_report(self, analysis_data, output_path='portfolio_analysis_report.pdf'):
        """Generate a comprehensive PDF report"""
        doc = SimpleDocTemplate(output_path, pagesize=A4,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title
        story.append(Paragraph("Portfolio Analysis Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 12))
        
        # Date
        current_date = datetime.now().strftime("%B %d, %Y")
        story.append(Paragraph(f"Generated on: {current_date}", self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        story.append(Paragraph(
            f"This report provides a comprehensive analysis of your trading portfolio performance. "
            f"Your AI-powered performance score is {analysis_data.get('score', 'N/A')}, indicating "
            f"{'excellent' if float(analysis_data.get('score', 0)) > 7 else 'good' if float(analysis_data.get('score', 0)) > 5 else 'moderate'} trading performance.",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 20))
        
        # Key Metrics Table
        story.append(Paragraph("Key Performance Metrics", self.styles['SectionHeader']))
        metrics_table = self.create_metrics_table(analysis_data.get('last_value', {}))
        story.append(metrics_table)
        story.append(Spacer(1, 20))
        
        # Charts Section
        story.append(Paragraph("Performance Charts", self.styles['SectionHeader']))
        
        # Create charts
        charts_data = analysis_data.get('charts', {})
        for chart_name, chart_data in charts_data.items():
            if chart_data and len(chart_data) > 0:
                chart_title = chart_name.replace('_', ' ').title()
                image_base64 = self.create_chart_image(chart_data, chart_title)
                
                # Save temporary image
                temp_image_path = f"temp_{chart_name}.png"
                with open(temp_image_path, 'wb') as f:
                    f.write(base64.b64decode(image_base64))
                
                # Add to PDF
                img = Image(temp_image_path, width=6*inch, height=3.6*inch)
                story.append(img)
                story.append(Spacer(1, 12))
                
                # Clean up temp file
                os.remove(temp_image_path)
        
        # AI Analysis
        if analysis_data.get('ai_analysis'):
            story.append(Paragraph("AI-Powered Analysis", self.styles['SectionHeader']))
            story.append(Paragraph(analysis_data['ai_analysis'], self.styles['Normal']))
            story.append(Spacer(1, 20))
        
        # Recommendations
        story.append(Paragraph("Recommendations", self.styles['SectionHeader']))
        recommendations = self.generate_recommendations(analysis_data.get('last_value', {}))
        for rec in recommendations:
            story.append(Paragraph(f"• {rec}", self.styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Footer
        story.append(Paragraph("Generated by TradeAnalyzer Pro", 
                              ParagraphStyle('Footer', parent=self.styles['Normal'], 
                                           fontSize=8, alignment=TA_CENTER, 
                                           textColor=colors.grey)))
        
        # Build PDF
        doc.build(story)
        return output_path

    def generate_recommendations(self, metrics):
        """Generate trading recommendations based on metrics"""
        recommendations = []
        
        if metrics.get('sharpe_ratio', 0) < 1:
            recommendations.append("Consider improving risk-adjusted returns by reducing portfolio volatility")
        
        if metrics.get('max_drawdown', 0) < -0.2:
            recommendations.append("High maximum drawdown detected - consider implementing stop-loss strategies")
        
        if metrics.get('win_loss_ratio', 0) < 1:
            recommendations.append("Win/loss ratio below 1 - focus on improving trade selection criteria")
        
        if metrics.get('sortino_ratio', 0) > 2:
            recommendations.append("Excellent downside risk management - maintain current strategy")
        
        if not recommendations:
            recommendations.append("Portfolio shows balanced performance - continue current approach")
        
        return recommendations

# Usage example
def create_pdf_report(analysis_data, output_path='portfolio_report.pdf'):
    """Convenience function to create PDF report"""
    generator = PDFReportGenerator()
    return generator.generate_report(analysis_data, output_path)
