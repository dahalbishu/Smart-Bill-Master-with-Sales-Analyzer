import cv2
import RPi.GPIO as GPIO
import time
from pyzbar.pyzbar import decode
import os
import numpy as np
from datetime import datetime, date
import mysql.connector
import smtplib
from num2words import num2words
from tkinter import *
import tkinter as tk
from tkinter import ttk

#self made
import database856365
import sales18956

conn = mysql.connector.connect(
    host="192.168.1.67",
    user="app",
    password="app",
    database="ourshoppingcenter"
)

cursor = conn.cursor()

#pin ------------- description
ses = 37 #for Touch sensor-------------------
in1= 3#for moter driver of moter
in2 = 5#for moter driver of moter
in3 = 11 # for moter driver for led light
in4 = 13#for moter driver for led light
buzz =  15 # pin for buzzer

GPIO.setmode(GPIO.BOARD)
#set required pin as input or output
GPIO.setup(ses,GPIO.IN)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(buzz,GPIO.OUT)
#function for checking expiry date
def checkdate(datei):
   
    expiration_date = datei
    
    # Current date
    today = date.today()
   
    current_date = today.strftime("%Y-%m-%d")
 
    if current_date > expiration_date:
        print("The product has expired.")
        return True
    else:
        print("The product has not expired.") 
        return False
#function to control movement of motor
def motercontrol(control):
    if control == 1:
        
        GPIO.output(in1,True)
        GPIO.output(in2,False)
    else:
        GPIO.output(in1,False)
        GPIO.output(in2,False)       
    
GPIO.output(in1,False)
GPIO.output(in2,False)
machine = 'on'
cap=cv2.VideoCapture(0)
product_list = []
price_list = []

solve____ = 0
while True:
    # if ir button is on
    #machine = getirvalue(machine)
    
    if(machine == 'on'):
        
        solve____ = 1
        motercontrol(1)#start moter
        #start qr scanning and do its work
        
        success,img=cap.read()
        if not success:
            break
        #for loop for decoding detected qr
        for code in decode(img):
            try:
                decoded_data=code.data.decode(("utf-8"))
                id,SP,Expiry=decoded_data.split("\n")
                index,productid = id.split(":")
                inde, price= SP.split(":")
                ind, datei = Expiry.split(":")
                checkexpire = checkdate(datei)
            except:
                continue
            if checkexpire == True:
                motercontrol(0)
                success,img=cap.read()
                #for alert system of expiry date
                for i in range (0,1):
                    GPIO.output(in3,True)
                    GPIO.output(in4,False)
                    GPIO.output(buzz,True)
                    time.sleep(0.5)
                    GPIO.output(in3,False)
                    GPIO.output(in4,False)
                    GPIO.output(buzz,False)
                    time.sleep(.5)
                motercontrol(1)
                continue                        
                
            if productid not in product_list:
                product_list.append(productid)
                price_list.append(float(price))
            
            rect_pts=code.rect
            if decoded_data:
                pts=np.array([code.polygon],np.int32)
                cv2.polylines(img,[pts],True,(255,0,0),3)
                cv2.putText(img,str(decoded_data),(rect_pts[0],rect_pts[1]),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),2)

        cv2.imshow("image",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            machine = 'off'
            cap.release()
            cv2.destroyAllWindows()            

    elif(machine == 'off'):
        motercontrol(0)#off motor
        #if(solve____ == 1 or True):
        givemail = ''
        purchasesOne = []
        purchases=[]
        for priceOne in product_list:
            purchasesOne.append(priceOne[:4])

        purchases = [(digit, purchasesOne.count(digit)) for digit in set(purchasesOne)]

        individualPrice = []
        for purone in purchases:
            pidtocalc = purone[0]
            onePricetotal = []
            for i, purchasesOneindv in enumerate(purchasesOne):
                if pidtocalc == purchasesOneindv:
                    onePricetotal.append(price_list[i])
            individualPrice.append(sum(onePricetotal) / len(onePricetotal))

        #get individual pname
        try:
            #create command
            cmdmerge = " "
            for datapid in purchases:
                cmdmerge = cmdmerge + "pid = '" + datapid[0] + "' or "

            cmdmerge = cmdmerge[:-3]
            #fetch pname

            cmd = "select pid,pname from products where {}".format(cmdmerge)
            
            cursor.execute(cmd)
            indvpname = cursor.fetchall()
            #store pname in list
            individialPname = []
            for purone in purchases:

                for indvpnameOne in indvpname:

                    if purone[0] == indvpnameOne[0]:
                        individialPname.append(indvpnameOne[1])

        except:
            break
        #section for UI
        getPhoneNum = ''
        getPhoneNum = sales18956.UIofBill(purchases, individialPname, individualPrice)
        if not getPhoneNum.isdigit():
            getPhoneNum = "nOne"

        #section for database
        try:

            #call database
            database856365.databasework(purchases, conn, cursor,getPhoneNum,individialPname,individualPrice)

        except:
            print("cannot put in database")

        solve____ = 0    
        product_list = []
        price_list = []
        break
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break 

GPIO.output(in1,False)
GPIO.output(in2,False)
GPIO.output(in3,False)
GPIO.output(in4,False)           
        
       
