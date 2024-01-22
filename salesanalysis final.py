#!/usr/bin/env python
# coding: utf-8

# In[7]:



import mysql.connector
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from calendar import month_name
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkcalendar import DateEntry
from datetime import datetime, date
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import mplcursors
import matplotlib

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ourshoppingcenter"
)


def profit_by_date(start_date, end_date):
    # Create the tkinter window
    root = tk.Tk()
    root.title('Profit Graph')

    query = """
        SELECT DATE(s.sold_datetime) as date, SUM((d.sp * s.quantity) - (d.cp * s.quantity)) AS profit
        FROM productsdetail d
        JOIN products_sold s ON d.pid = s.pid
        WHERE s.sold_datetime BETWEEN %s AND %s
        GROUP BY DATE(s.sold_datetime)
    """
    sales_data = pd.read_sql_query(query, cnx, params=[start_date, end_date])
    sns.set(style="darkgrid")
    fig = Figure(figsize=(10, 7), dpi=100)
    ax = fig.add_subplot(111)
    sns.lineplot(data=sales_data, x='date', y='profit', ax=ax)
    ax.set_xlabel('Date')
    ax.set_ylabel('Profit')
    ax.set_title('Profit by Date')
    cursor = mplcursors.cursor(ax, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f"Sales: {sel.target[1]:.2f}"))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()


    root.mainloop()


def sales_by_date(start_date, end_date):
    root = tk.Tk()
    root.title('Sales Graph')
    query = """
        SELECT DATE(s.sold_datetime) as date, SUM(d.sp * s.quantity) AS sales
        FROM productsdetail d
        JOIN products_sold s ON d.pid = s.pid
        WHERE s.sold_datetime BETWEEN %s AND %s
        GROUP BY DATE(s.sold_datetime)
    """
    sales_data = pd.read_sql_query(query, cnx, params=[start_date, end_date])


    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(10,7))
    sns.set(style="darkgrid")
    sns.lineplot(data=sales_data, x='date', y='sales', ax=ax)
    ax.set(xlabel='Date', ylabel='Sales')
    cursor = mplcursors.cursor(ax, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f"Sales: {sel.target[1]:.2f}"))
    # Create a Tkinter canvas for the figure
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    root.mainloop()

def sales_by_month():
    root = tk.Tk()
    root.title('Sales Graph by month')
    query = """
        SELECT MONTH(s.sold_datetime) as month, SUM(d.sp * s.quantity) AS sales
        FROM productsdetail d
        JOIN products_sold s ON d.pid = s.pid
        GROUP BY MONTH(s.sold_datetime)
    """
    sales_data = pd.read_sql_query(query, cnx)

    sales_data['month'] = sales_data['month'].apply(lambda x: month_name[x])
    print("Sales by month")
    print(sales_data)

    sns.set(style="darkgrid")
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.barplot(data=sales_data, x='month', y='sales', ax=ax)
    ax.set_xlabel('Month')
    ax.set_ylabel('Sales')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    # Run the Tkinter event loop
    root.mainloop()

def profit_by_month():
    root = tk.Tk()
    root.title('Profit by Month')
    query = """
        SELECT MONTH(s.sold_datetime) as month, SUM((d.sp * s.quantity) - (d.cp * s.quantity)) AS profit
        FROM productsdetail d
        JOIN products_sold s ON d.pid = s.pid
        GROUP BY MONTH(s.sold_datetime)
    """
    sales_data = pd.read_sql_query(query, cnx)

    # Convert the month numbers to month names
    sales_data['month'] = sales_data['month'].apply(lambda x: month_name[x])

    # Create a bar plot of profit by month using Seaborn
    sns.set(style="darkgrid")
    fig = plt.Figure(figsize=(10, 7), dpi=100)
    ax = fig.add_subplot(111)
    sns.barplot(data=sales_data, x='month', y='profit', ax=ax)
    ax.set_xlabel('Month')
    ax.set_ylabel('Profit')
    ax.set_title('Profit by Month')

    # Create a Tkinter window and canvas for the figure

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    root.mainloop()

def most_sold_product(start_date, end_date):
    root = tk.Tk()
    root.title('Top 10 Most Sold Products')
    query = """
        SELECT pid, SUM(quantity) as total_quantity
        FROM products_sold
        GROUP BY pid
        ORDER BY total_quantity DESC
        LIMIT 10
    """
    top_products = pd.read_sql_query(query, cnx)

    # Create a Seaborn bar plot
    sns.set(style="darkgrid")
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.barplot(data=top_products, x='pid', y='total_quantity', ax=ax)
    ax.set(xlabel='Product ID', ylabel='Total Quantity Sold', title='Top 10 Most Sold Products')

    # Create a Tkinter window and canvas for the plot
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    root.mainloop()


def most_sold_product(start_date, end_date):
    root = tk.Tk()
    root.title('Top 10 Most Sold Products')
    query = """
        SELECT pid, SUM(quantity) as total_quantity
        FROM products_sold
        GROUP BY pid
        ORDER BY total_quantity DESC
        LIMIT 10
    """
    top_products = pd.read_sql_query(query, cnx)

    # Create a Seaborn bar plot
    sns.set(style="darkgrid")
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.barplot(data=top_products, x='pid', y='total_quantity', ax=ax)
    ax.set(xlabel='Product ID', ylabel='Total Quantity Sold', title='Top 10 Most Sold Products')

    # Create a Tkinter window and canvas for the plot
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    root.mainloop()
def product(pid):
    window = tk.Toplevel()
    window.title('Product Detail')
    if pid == 'all':
        query = """
        select p.pid,p.pname,p.ptype,d.cp,d.sp, d.order_datetime from 
        products p join productsdetail d on p.pid=d.pid
        
        """
        products = pd.read_sql_query(query, cnx)
    else:
        query = """
        select p.pid,p.pname,p.ptype,d.cp,d.sp, d.order_datetime from 
        products p join productsdetail d on p.pid=d.pid
        where p.pid= %s
        """
        products = pd.read_sql_query(query, cnx, params=[pid])
    print(products)  # Make sure the DataFrame contains the expected data
    df = pd.DataFrame(products)
    tree = ttk.Treeview(window, columns=list(df.columns), show='headings')
    for col in df.columns:
        tree.heading(col, text=col)
    for index, row in df.iterrows():
        tree.insert("", tk.END, values=row.tolist())

    # Add the Treeview widget to the Tkinter window
    tree.pack(fill='both', expand=True)

    # Run the Tkinter event loop
    window.mainloop()

def productremain(pid):
    window = tk.Toplevel()
    window.title('Product Quantity Details')

    # Retrieve the product details from the database
    if pid == "all":
        query = """
        SELECT p.pid, p.pname, d.quantity AS total_quantity,
            SUM(s.quantity) AS quantity_sold, (d.quantity - SUM(s.quantity)) AS remaining_quantity
        FROM products p
        JOIN productsdetail d ON d.pid = p.pid
        JOIN products_sold s ON p.pid = s.pid
      
        GROUP BY p.pid, p.pname, d.quantity
        """
        products = pd.read_sql_query(query, cnx)
    else:
        query = """
        SELECT p.pid, p.pname, d.quantity AS total_quantity,
        SUM(s.quantity) AS quantity_sold, (d.quantity - SUM(s.quantity)) AS remaining_quantity
        FROM products p
        JOIN productsdetail d ON d.pid = p.pid
        JOIN products_sold s ON p.pid = s.pid
        WHERE p.pid = %s
        GROUP BY p.pid, p.pname, d.quantity
        """
        products = pd.read_sql_query(query, cnx, params=[pid])


    # Create a Treeview widget to dsplay the product details
    tree = ttk.Treeview(window, columns=list(products.columns), show='headings')
    for col in products.columns:
        tree.heading(col, text=col)
    for index, row in products.iterrows():
        tree.insert("", tk.END, values=row.tolist())

    # Add the Treeview widget to the Tkinter window
    tree.pack(fill='both', expand=True)

    # Run the Tkinter event loop
    window.mainloop()

    # Run the Tkinter event loop
    window.mainloop()


def customer():
    window = tk.Toplevel()
    window.title('Customer Details')
    query = """
            select cust_id,fname,lname,gender,address,email,phone_number from customer
       """
    products = pd.read_sql_query(query, cnx)
    df = pd.DataFrame(products)
    tree = ttk.Treeview(window, columns=list(df.columns), show='headings')
    for col in df.columns:
        tree.heading(col, text=col)
    for index, row in df.iterrows():
        tree.insert("", tk.END, values=row.tolist())

    # Add the Treeview widget to the Tkinter window
    tree.pack(fill='both', expand=True)

    # Run the Tkinter event loop
    window.mainloop()




def timeee():
    root = tk.Tk()
    root.title('Timely Sales Report')
 # Retrieve the sales data from the database table
    query = """
        SELECT HOUR(sold_datetime) AS hour, SUM(quantity) AS total_sales
        FROM products_sold
        GROUP BY HOUR(sold_datetime)
    """

    sales_data = pd.read_sql_query(query, cnx)

    sns.set(style="darkgrid")
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.barplot(data=sales_data, x='hour', y='total_sales', ax=ax)
    ax.set_xlabel('Hour')
    ax.set_ylabel('Quantity')
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Run the Tkinter event loop
    root.mainloop()
    

    # Convert the month numbers to month names


def productalldetails():
    window = tk.Toplevel()
    window.title('All products in stock')
    query = """
          SELECT p.pid,p.pname,p.ptype,d.cp,d.sp,d.quantity,d.order_datetime from products p 
          join productsdetail d on p.pid=d.pid
          order by pid asc
       """
    products = pd.read_sql_query(query, cnx)
    df = pd.DataFrame(products)
    tree = ttk.Treeview(window, columns=list(df.columns), show='headings')
    for col in df.columns:
        tree.heading(col, text=col)
    for index, row in df.iterrows():
        tree.insert("", tk.END, values=row.tolist())

    # Add the Treeview widget to the Tkinter window
    tree.pack(fill='both', expand=True)

    # Run the Tkinter event loop
    window.mainloop()

def deletecustomer(cid):
    query="update products_sold set cust_id = Null where cust_id=%s"
    val = (cid,)
    cursor = cnx.cursor()
    cursor.execute(query, val)
    
    query="delete from customer where cust_id=%s"
    val = (cid,)
    cursor = cnx.cursor()
    cursor.execute(query, val)
    cnx.commit()


def productbygender():
    window = tk.Toplevel()
    window.title('Product Sales by Gender')
    query = """
    SELECT ps.pid, c.gender, 
           COUNT(*) as total_sales, 
           COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY ps.pid) * 100 as sales_percentage
    FROM products_sold ps 
    INNER JOIN customer c ON ps.cust_id = c.cust_id
    GROUP BY ps.pid, c.gender
    ORDER BY ps.pid, c.gender;
       """
    products = pd.read_sql_query(query, cnx)
    df = pd.DataFrame(products)
    tree = ttk.Treeview(window, columns=list(df.columns), show='headings')
    for col in df.columns:
        tree.heading(col, text=col)
    for index, row in df.iterrows():
        tree.insert("", tk.END, values=row.tolist())

    # Add the Treeview widget to the Tkinter window
    tree.pack(fill='both', expand=True)

    # Run the Tkinter event loop
    window.mainloop()

    
def productbyage():
    window = tk.Toplevel()
    window.title('Product Sales by Gender')
    query = """
    SELECT 
        ps.pid,
        CASE 
            WHEN YEAR(CURDATE()) - YEAR(c.dob) BETWEEN 0 AND 10 THEN '0-10'
            WHEN YEAR(CURDATE()) - YEAR(c.dob) BETWEEN 11 AND 20 THEN '11-20'
            WHEN YEAR(CURDATE()) - YEAR(c.dob) BETWEEN 21 AND 30 THEN '21-30'
            WHEN YEAR(CURDATE()) - YEAR(c.dob) BETWEEN 31 AND 40 THEN '31-40'
            WHEN YEAR(CURDATE()) - YEAR(c.dob) BETWEEN 41 AND 50 THEN '41-50'
            WHEN YEAR(CURDATE()) - YEAR(c.dob) BETWEEN 51 AND 60 THEN '51-60'
            WHEN YEAR(CURDATE()) - YEAR(c.dob) BETWEEN 61 AND 70 THEN '61-70'
            ELSE '70+'
        END AS age_group,
        COUNT(DISTINCT ps.cust_id) AS customers,
        SUM(ps.quantity) AS quantity_sold,
        (SUM(ps.quantity) / (SELECT SUM(quantity) FROM products_sold WHERE pid = ps.pid)) * 100 AS percentage_sold
    FROM 
        products_sold ps
        JOIN customer c ON ps.cust_id = c.cust_id
    GROUP BY 
        ps.pid, age_group;
       """
    products = pd.read_sql_query(query, cnx)
    df = pd.DataFrame(products)
    tree = ttk.Treeview(window, columns=list(df.columns), show='headings')
    for col in df.columns:
        tree.heading(col, text=col)
    for index, row in df.iterrows():
        tree.insert("", tk.END, values=row.tolist())

    # Add the Treeview widget to the Tkinter window
    tree.pack(fill='both', expand=True)

    # Run the Tkinter event loop
    window.mainloop()



def handle_most_sold_product():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    most_sold_product(start_date, end_date)



def handle_sales_by_date():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    sales_by_date(start_date, end_date)


def handle_profit_by_date():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    profit_by_date(start_date, end_date)


def handle_sales_by_month():
    sales_by_month()


def handle_profit_by_month():
    profit_by_month()

def handle_customer():
    customer()


def handle_productdetail():
    pid = product_entry.get()
    product(pid)
    # Create the tkinter window and widgets
def handle_productremain():
    pid = product_entry.get()
    productremain(pid)

def handle_time():
    timeee()

def handle_productbygender():
    productbygender()
def handle_productbyage():
    productbyage()
    
def handle_productall():
    productalldetails()

def handle_custdel():
    cid= customer_entry.get()
    deletecustomer(cid)


root = tk.Tk()
root.geometry("1200x500")
root.title("Sales Analytics Dashboard")
title_label = tk.Label(root, text="OUR SHOPPING CENTER ", font=("Arial Bold", 24), fg="blue")
title_label.grid(row=0, column=0, columnspan=7, pady=20)

today = date.today()
current_date = today.strftime("%Y-%m-%d")


start_date_label = tk.Label(root, text="Start Date (YYYY-MM-DD): ")
start_date_label.grid(row=1, column=0)
start_date_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
start_date_entry.grid(row=1, column=1)
end_date_label = tk.Label(root, text="End Date (YYYY-MM-DD): ")
end_date_label.grid(row=2, column=0)
end_date_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
end_date_entry.grid(row=2, column=1)

product_label = tk.Label(root, text=" PRODUCT SECTION Product ID (P00X) :")
product_label.grid(row=3, column=0)
product_entry = tk.Entry(root)
product_entry.grid(row=3, column=1)
customer_label = tk.Label(root, text="CUSTOMER SECTION(Customer ID:CUSTX")
customer_label.grid(row=5, column=0)
customer_entry = tk.Entry(root)
customer_entry.grid(row=5, column=1)






time_label = tk.Label(root, text="TIMELY ANALYSIS :")
time_label.grid(row=7, column=0)

# Set default text for entries
start_date_entry.set_date('2023-01-01')
end_date_entry.set_date(current_date)


sales_by_date_button = tk.Button(root, text="Show Sales by Date",font=("Arial", 13),fg="blue" ,command=handle_sales_by_date)
sales_by_date_button.grid(row=1, column=2,sticky=tk.NSEW)

profit_by_date_button = tk.Button(root, text="Show Profit by Date", font=("Arial", 13),fg="blue",command=handle_profit_by_date)
profit_by_date_button.grid(row=1, column=3,sticky=tk.NSEW)

sales_by_month_button = tk.Button(root, text="Show Sales by Month", font=("Arial", 13),fg="blue",command=handle_sales_by_month)
sales_by_month_button.grid(row=1, column=4,sticky=tk.NSEW)

profit_by_month_button = tk.Button(root, text="Show Profit by Month", font=("Arial", 13),fg="blue",command=handle_profit_by_month)
profit_by_month_button.grid(row=1, column=5,sticky=tk.NSEW)

most_sold_product_button = tk.Button(root, text="show most sold product", font=("Arial", 13),fg="blue",command=handle_most_sold_product)
most_sold_product_button.grid(row=2, column=2,sticky=tk.NSEW)


product_button = tk.Button(root, text="show product detail", font=("Arial", 13),fg="blue",command=handle_productdetail)
product_button.grid(row=3, column=2,sticky=tk.NSEW)


productremain_button = tk.Button(root, text="show product quantity", font=("Arial", 13),fg="blue",command=handle_productremain)
productremain_button.grid(row=3, column=3,sticky=tk.NSEW)

productall_button = tk.Button(root, text="show all products in stock ", font=("Arial", 13),fg="blue",command=handle_productall)
productall_button.grid(row=3, column=4,sticky=tk.NSEW)


customer_button = tk.Button(root, text=" All Customers detail ", font=("Arial", 13),fg="blue",command=handle_customer)
customer_button.grid(row=5, column=2,sticky=tk.NSEW)

custdel_button = tk.Button(root, text=" Delete Customer ", font=("Arial", 13),fg="blue",command=handle_custdel)
custdel_button.grid(row=5, column=3,sticky=tk.NSEW)


time_button = tk.Button(root, text="Timely graph", font=("Arial", 13),fg="blue",command=handle_time)
time_button.grid(row=7, column=2,sticky=tk.NSEW)

productbygender_button = tk.Button(root, text="Show Sales product by gender", font=("Arial", 13),fg="blue",command=handle_productbygender)
productbygender_button.grid(row=8, column=2,sticky=tk.NSEW)

productbyage_button = tk.Button(root, text="Show Sales product by age group", font=("Arial", 13),fg="blue",command=handle_productbyage)
productbyage_button.grid(row=8, column=3,sticky=tk.NSEW)




root.mainloop()





# In[ ]:





# In[ ]:




