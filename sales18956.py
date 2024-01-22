
import tkinter as tk
from tkinter import ttk
from num2words import num2words
import pdfplusmail

def add_price():
    unit_price = int(unitprice_entry.get())
    quantity = int(quantity_entry.get())
    price = unit_price * quantity
    totalprice_entry.delete(0, tk.END)
    totalprice_entry.insert(0, str(price))
    prices.append(price)
    total_price = sum(prices)
    # total_label.config(text=f"Total Bill: {total_price}")
 


# function to handle email submission
def submit_email(purchases,individialPname,individualPrice,repmail):
    root = tk.Tk()
    root.geometry('150x75')
    email_label = tk.Label(root, text="Message")
    email_label.grid(row=12, column=6)
    try:
        pdfplusmail.create_pdf(purchases,individialPname,individualPrice,repmail)
        email_label.config(text="Mail deivered successfully")
    except:
        email_label.config(text="Error Occured !!!!")
    root.mainloop()
    
def submit_phone():
    pass
   
    

    # do something with the email
def UIofBill(purchases,individialPname,individualPrice):
    root = tk.Tk()
    root.geometry('800x600')
    root.title("Total Bill")



    # create a treeview widget to display the table
    treeview = ttk.Treeview(root)
    treeview.grid(row=1, column=0, columnspan=10)

    # define the columns of the table
    treeview['columns'] = ("Serial No.", "Product Name", "Unit Price", "Quantity", "Price")

    # format the columns
    treeview.column("#0", width=0, stretch=tk.NO)
    treeview.column("Serial No.", anchor=tk.CENTER, width=100)
    treeview.column("Product Name", anchor=tk.CENTER, width=100)
    treeview.column("Unit Price", anchor=tk.CENTER, width=100)
    treeview.column("Quantity", anchor=tk.CENTER, width=100)
    treeview.column("Price", anchor=tk.CENTER, width=100)

    # set the column headings
    treeview.heading("Serial No.", text="Serial No.")
    treeview.heading("Product Name", text="Product Name")
    treeview.heading("Unit Price", text="Unit Price")
    treeview.heading("Quantity", text="Quantity")
    treeview.heading("Price", text="Price")

    # create a label and entry box for email
    tk.Label(root, text="Email:", bg='White', fg='blue').grid(row=10, column=6)
    email_var = tk.StringVar()
    email_entry = tk.Entry(root,textvariable=email_var)
    email_entry.grid(row=7, column=6)
   
    submit_button = tk.Button(root, text="Submit", command=lambda: submit_email(purchases,individialPname,individualPrice,email_var.get()))
    submit_button.grid(row=8, column=6)
    
    
    tk.Label(root, text="Phone:", bg='White', fg='blue').grid(row=6, column=6)
    phone_var = tk.StringVar()
    phone_entry = tk.Entry(root,textvariable=phone_var)
    phone_entry.grid(row=3, column=6)
    
    submit_button = tk.Button(root, text="Submit", command=submit_phone)
    submit_button.grid(row=4, column=6)

    # create a label for displaying the total
    total_label = tk.Label(root, text="Total Bill:   0", bg='White', fg='blue')
    total_label.grid(row=3, column=0, columnspan=10, sticky="w")

    # call function to add prices for the list of products
    prices = []
    
    for i in range(0,len(purchases)):
        product_price = individualPrice[i]# QR bata aunxa
        price = product_price * purchases[i][1]
        treeview.insert(parent='', index=i, iid=i, values=(i+1,individialPname[i] ,product_price,purchases[i][1], price))
        prices.append(price)
        total_price = sum(prices)
    total_label.config(text=f"Total Bill: {total_price} ({num2words(int(total_price))} rupees only)")

    # make the table expand to fill the entire width of the window
    for i in range(7):
        root.grid_columnconfigure(i, weight=1)

    root.mainloop()
    return phone_var.get()
