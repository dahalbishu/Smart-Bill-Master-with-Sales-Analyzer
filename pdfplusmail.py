#!/usr/bin/env python
# coding: utf-8

# In[38]:


import tkinter as tk
import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fpdf import FPDF
import tempfile
from tkinter import ttk
from num2words import num2words
from datetime import datetime, date



def create_pdf(purchases,individialPname,individualPrice,repmail):
    
    today = date.today()
    current_date = today.strftime("%Y-%m-%d")

    # create a PDF object
    pdf = FPDF()
    
    # add a page to the PDF
    pdf.add_page()
    
    # set the font for the title
    pdf.set_font("Arial", "B", 16)
   
    
    # write the title
    pdf.cell(0, 10, "Our Shopping Center", 0, 1, "C")
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Thapathali-3,ktm, 01-4456568", 0, 1, "C")
    pdf.ln()
    pdf.cell(0, 10, "Date:- {}".format(current_date), 0, 1, "R")
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Total Bill", 0, 1, "C")
    pdf.ln()
    
   
    
    # set the font for the table
   
    # add the table headers
    pdf.set_fill_color(192, 192, 192)  # set fill color to grey
    pdf.cell(20, 10, "Serial No.", 1, 0, 'C', 1)
    pdf.cell(50, 10, "Product Name", 1, 0, 'C', 1)
    pdf.cell(30, 10, "Unit Price", 1, 0, 'C', 1)
    pdf.cell(20, 10, "Quantity", 1, 0, 'C', 1)
    pdf.cell(30, 10, "Price", 1, 1, 'C', 1)
    

  
    total_price_list = []
    invtotalprice = 0
    for i in range(0,len(purchases)):
        pdf.cell(20, 10, str(i+1), 1, 0, "C", False)
        pdf.cell(50, 10, individialPname[i], 1, 0, "C", False)
        pdf.cell(30, 10, str(individualPrice[i]), 1, 0, "C", False)
        pdf.cell(20, 10, str(purchases[i][1]), 1, 0, "C", False)
        invtotalprice = float(individualPrice[i])*int(purchases[i][1])
        pdf.cell(30, 10, str(invtotalprice), 1, 0, "C", False)
        total_price_list.append(invtotalprice)
        pdf.ln()

    

    
    # add the total label
    pdf.ln()
    pdf.ln()
    total_price = sum(total_price_list)
    total_price_words = num2words(total_price)
    pdf.cell(0,5, f"Total Amount:- Rs.{total_price} /-", 0, 1)
    pdf.cell(0,5, f"In words:- {total_price_words} rupees only", 0, 1)
    pdf.ln()
    pdf.cell(0, 10, "*** Thank You ***", 0, 1, "C")
    
    
    

    sender = 'surampok@gmail.com'
    recipient =  repmail

    passwd = "uexwvtmw"


    msg = MIMEMultipart()
    msg['Subject'] = 'Our Shopping Center Bill'
    msg['From'] = sender
    msg['To'] = recipient

    # attach PDF file
    with tempfile.NamedTemporaryFile(delete=False) as fp:
        pdf.output(fp.name)
        with open(fp.name, 'rb') as f:
            pdf_data = f.read()
        pdf_attachment = MIMEApplication(pdf_data, _subtype='pdf')
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename='bill.pdf')
        msg.attach(pdf_attachment)

    # add text message
    text = MIMEText("Dear Customer,\nPlease find attached the bill for your recent purchases at our store.\nThank you for your continued patronage!")


    msg.attach(text)


    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(sender, passwd)
    smtp.sendmail(sender, recipient, msg.as_string())
    smtp.quit()






# In[ ]:




