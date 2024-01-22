import pdfplusmail

def databasework(purchases,conn,cursor,getPhoneNum,individialPname,individualPrice):
    # Fetch the latest bill number
    cursor.execute("SELECT MAX(bill_num) FROM products_sold")
    last_bill_num = cursor.fetchall()

    # Generate a unique bill number
    if last_bill_num[0][0] != []:
        bill_num = last_bill_num[0][0] + 1
    else:
        bill_num = 1

    # email access of registered cutomer
    if getPhoneNum != "nOne":
        query = "SELECT cust_id,email FROM customer WHERE phone_number = {}".format(getPhoneNum)
        cursor.execute(query)
        resofcust = cursor.fetchall()

        if resofcust == []:
            outputemail = "nOne"
            outputid = "nOne"
        else:
            outputid = resofcust[0][0]
            outputemail = resofcust[0][1]
            #send mail to registerd customer
            try:
                pdfplusmail.create_pdf(purchases, individialPname, individualPrice, outputemail)
            except:
                print("Unable to send mail")
    else:
        outputid = "nOne"
    # decreasing quantity in productsdetail

    for pid, quantity in purchases:
      
        # Insert the purchases into the product_sold table
        if outputid == 'nOne':
            sql = "INSERT INTO products_sold (bill_num, pid, quantity, sold_datetime) VALUES (%s, %s, %s, NOW())"
            val = (bill_num, pid, quantity)
        
        else:
            sql = "INSERT INTO products_sold (bill_num, pid, quantity,cust_id, sold_datetime) VALUES (%s, %s, %s, %s, NOW())"
            val = (bill_num, pid, quantity, outputid)
        
        cursor.execute(sql, val)

    conn.commit()

    # Close the connection
    conn.close()

