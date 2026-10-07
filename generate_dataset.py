import os
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

os.makedirs('dataset/documents', exist_ok=True)

# 1. Production Report (with conflict)
def create_production_report():
    c = canvas.Canvas("dataset/documents/production_report.pdf", pagesize=letter)
    
    # Page 1: Text
    c.drawString(100, 750, "Production Report - 2025")
    c.drawString(100, 730, "This document outlines the quarterly production data.")
    c.drawString(100, 710, "Our main objective is maximizing production efficiency.")
    c.drawString(100, 690, "Reasons for changes: reduced machine downtime, improved scheduling,")
    c.drawString(100, 670, "automation, and better resource allocation.")
    c.showPage()
    
    # Page 2: Table
    c.drawString(100, 750, "Production Table")
    c.drawString(100, 730, "Quarter | Units | Efficiency")
    c.drawString(100, 710, "Q1      | 10,000| 72%")
    c.drawString(100, 690, "Q2      | 12,000| 78%")
    c.drawString(100, 670, "Q3      | 13,500| 81%")
    c.drawString(100, 650, "Q4      | 15,000| 86%") # Table says 86%
    c.showPage()
    
    # Page 3: Chart (conflict: Q4 is 84%)
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    efficiencies = [72, 78, 81, 84] # Chart says 84%
    plt.figure(figsize=(5,3))
    plt.bar(quarters, efficiencies, color='blue')
    plt.title('Production Efficiency by Quarter')
    plt.ylabel('Efficiency (%)')
    plt.savefig('dataset/documents/eff_chart.png')
    plt.close()
    
    c.drawString(100, 750, "Production Efficiency Chart")
    c.drawImage("dataset/documents/eff_chart.png", 100, 400, width=400, height=300)
    c.showPage()
    
    c.save()

# 2. Financial Report
def create_financial_report():
    c = canvas.Canvas("dataset/documents/financial_report.pdf", pagesize=letter)
    c.drawString(100, 750, "Financial Report - 2025")
    c.drawString(100, 730, "Quarter | Revenue")
    c.drawString(100, 710, "Q1      | $10M")
    c.drawString(100, 690, "Q2      | $12M")
    c.drawString(100, 670, "Q3      | $15M")
    c.drawString(100, 650, "Q4      | $20M")
    c.showPage()
    c.save()

create_production_report()
create_financial_report()
