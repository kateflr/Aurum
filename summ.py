from tkinter import *
from tkinter import ttk
import tkinter as tk
import random
from tkinter import Button, PhotoImage
import tkinter.messagebox
import datetime
import time
import os
import sys
import tempfile,os
import sqlite3


#---Επιχείρηση
def openSuppliers():
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Backend!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def suppliersData():
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        sql = """CREATE TABLE IF NOT EXISTS
        suppliers(
        name TEXT,
        price FLOAT
        )"""
        c.execute(sql)
        conn.commit()
        conn.close()

    def addSupplier (name,price):
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("INSERT INTO  suppliers VALUES (?,?)",(name,price))
        conn.commit()
        conn.close()

    def viewSupplier():
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("SELECT * FROM suppliers")
        rows = c.fetchall()
        conn.close()
        return rows

    def deleteSupplier(name):
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("""DELETE FROM  suppliers
        WHERE name = :name """,
            {
                'name':name
            }
        )
        conn.commit()
        conn.close()


    def updateSupplier(name,price):
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("""UPDATE  suppliers SET
        name = :name,
        price = :price
        WHERE name = :name """,
            {
                'name':name,
                'price':price
            }
        )
        conn.commit()
        conn.close()



    suppliersData()
    class Suppliers:
        def __init__(self):
            self.root =  Toplevel()
            blank_space = " "
            self.root.title(200 * blank_space + "A U R U M ")
            self.root.geometry("1350x580+200+200")


            name = StringVar()
            price = StringVar()
            #========================================FUNCTIONS==================================
            #def iExit():
            #    iExit = tkinter.messagebox.askyesno("Σύστημα","Θέλετε σίγουρα να αποχωρήσετε;")
            #    if iExit > 0:
            #        root.destroy()
            #        return

            def iReset():
                self.txtName.delete(0,END)
                self.txtPrice.delete(0,END)

            def iAddData():
                iCheck()
                if name.get()=="":
                    tkinter.messagebox.showwarning("Σύστημα","Δεν έχετε προσθέσει όνομα στον προμηθευτή σας!")
                else:
                    addSupplier(name.get(),price.get())                
                    iDisplay()
    
            def iDisplay():
                result = viewSupplier()
                if len(result)!=0:
                    self.productlist.delete(*self.productlist.get_children())
                    for row in result:
                        self.productlist.insert('',END,values=row)

            def iDelete():    
                iDeleteMessage = tkinter.messagebox.askyesno("Σύστημα","Θέλετε σίγουτα να κάνετε Διαγραφή;")
                if iDeleteMessage>0:
                    deleteSupplier(name.get())
                    tkinter.messagebox.showinfo("Σύστημα","Επιτυχής Διαγραφή")
                    iDisplay()
                    
            def iSupplier(e):
                iReset()
                selected = self.productlist.focus()
                values = self.productlist.item(selected,'values')
                self.txtName.insert(0,values[0])
                self.txtPrice.insert(0,values[1])

            def iUpdate():
                iCheck()
                if  name.get()=="":
                    tkinter.messagebox.showwarning("Σύστημα","Δεν έχετε επιλέξει Προμηθευτή")
                else:                
                    updateSupplier(name.get(),price.get())                
                    iDisplay()

            def iCheck():
                if price.get().isalpha():
                    tkinter.messagebox.showwarning("Σύστημα","Λάθος στις Οφειλές, εισάγεται αριθμό!!")
            
            #========================================Frames==================================
            MainFrame = Frame(self.root , bd=10, width = 1350, height=700, relief=RIDGE, bg="cadet blue")
            MainFrame.grid()

            TopFrame1 = Frame(MainFrame, bd=5, width = 1340, height=50, relief=RIDGE)
            TopFrame1.grid(row=2,column=0,pady=8)

            TitleFrame = Frame(MainFrame, bd=7, width = 1340, height=100, relief=RIDGE)
            TitleFrame.grid(row=0,column=0)

            TopFrame3 = Frame(MainFrame, bd=5, width = 1340, height=500, relief=RIDGE)
            TopFrame3.grid(row=1,column=0)

            LeftFrame = Frame(TopFrame3, bd=5, width = 1340, height=400, padx=2 , bg="cadet blue", relief=RIDGE)
            LeftFrame.pack(side=LEFT)

            LeftFrame1 = Frame(LeftFrame, bd=5, width = 600, height=180, padx=2,pady=4 , relief=RIDGE)
            LeftFrame1.pack(side=TOP,padx=0,pady=4)

            # RightFrame = Frame(TopFrame3, bd=5, width = 310, height=400, padx=2 ,pady=2, bg="cadet blue", relief=RIDGE)
            # RightFrame.pack(side=RIGHT)

            RightFrame1 = Frame(TopFrame3, bd=5, width=320 , height=400, padx=2, pady=2,relief=RIDGE)
            RightFrame1.pack(side=RIGHT)

            RightFrame1a = Frame(RightFrame1, bd=5, width=310, height=200, padx=2,pady=2,relief=RIDGE)
            RightFrame1a.pack(side=TOP)


            #========================================Title==================================
            self.lblTitle = Label(TitleFrame, font=('arial',56,'bold'),text="Οφειλές προς Προμηθευτές...",bd=7 )
            self.lblTitle.grid(row=0,column=0,padx=132)
            #========================================Widget==================================

            self.lblName = Label(LeftFrame1, font=('arial',12,'bold'),text="Όνομα Προμηθευτή",bd=7,anchor=W,justify=LEFT )
            self.lblName.grid(row=0,column=0, sticky=W , padx=5)
            self.txtName = Entry(LeftFrame1, font=('arial',10,'bold'),bd=5,width=40,justify=LEFT, textvariable=name )
            self.txtName.grid(row=0,column=1)

            self.lblPrice = Label(LeftFrame1, font=('arial',12,'bold'),text="Χρέος υπόλοιπο προς Προμηθευτή",bd=7,anchor=W,justify=LEFT )
            self.lblPrice.grid(row=1,column=0, sticky=W , padx=5)
            self.txtPrice = Entry(LeftFrame1, font=('arial',10,'bold'),bd=5,width=40,justify=LEFT, textvariable=price )
            self.txtPrice.grid(row=1,column=1)

            #========================================TreeView==================================
            scroll_x = Scrollbar(RightFrame1a, orient=HORIZONTAL)
            scroll_y = Scrollbar(RightFrame1a, orient=VERTICAL)

            self.productlist = ttk.Treeview(RightFrame1a,height=12,columns=("name","price"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

            scroll_x.pack(side=BOTTOM,fill=X)
            scroll_y.pack(side=RIGHT,fill=Y)

            self.productlist.heading("#0", text="")
            self.productlist.heading("name",text="Όνομα Προμηθευτή")
            self.productlist.heading("price",text="Χρέος προς Προμηθευτή")

            self.productlist['show'] = 'headings'

            self.productlist.column("#0", width=0)
            self.productlist.column("name",width=200)
            self.productlist.column("price",width=200)

            self.productlist.pack(fill=BOTH,expand=1)

            self.productlist.bind("<ButtonRelease-1>",iSupplier)
            iDisplay()
            #========================================Buttons==================================
            self.btnAddNew = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Προσθήκη",padx=24, width=12, height=2, command=iAddData).grid(row=0,column=0, padx=1)

            self.btnDisplay = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Καθαρισμός",padx=24, width=12, height=2, command=iReset).grid(row=0,column=1, padx=1)

            self.btnReset = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Αλλαγή",padx=24, width=12, height=2, command=iUpdate).grid(row=0,column=2, padx=1)
            
            self.btnDelete = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Διαγραφή",padx=24, width=12, height=2, command=iDelete).grid(row=0,column=3, padx=1)

            self.btnExit = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Έξοδος",padx=24, width=12, height=2, command=self.root.destroy).grid(row=0,column=4, padx=1)
    
    Suppliers()

def openProfits():
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Backend!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def profitData():
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        sql = """CREATE TABLE IF NOT EXISTS
        profit(
        name TEXT,
        price FLOAT
        )"""
        c.execute(sql)
        conn.commit()
        conn.close()

    def addProfit (name,price):
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("INSERT INTO  profit VALUES (?,?)",(name,price))
        conn.commit()
        conn.close()

    def viewProfits():
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("SELECT * FROM profit")
        rows = c.fetchall()
        conn.close()
        return rows

    def deleteProfit(name):
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("""DELETE FROM  profit
        WHERE name = :name """,
            {
                'name':name
            }
        )
        conn.commit()
        conn.close()


    def updateProfit(name,price):
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("""UPDATE  profit SET
        name = :name,
        price = :price
        WHERE name = :name """,
            {
                'name':name,
                'price':price
            }
        )
        conn.commit()
        conn.close()



    profitData()


    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Frontend!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    class Profit:
        
        def __init__(self):
            self.root = Toplevel()
            blank_space = " "
            self.root.title(200 * blank_space + "A U R U M ")
            self.root.geometry("1350x580+200+200")


            name = StringVar()
            price = StringVar()
            #========================================FUNCTIONS==================================
            def iExit():
                iExit = tkinter.messagebox.askyesno("Σύστημα","Θέλετε σίγουρα να αποχωρήσετε;")
                if iExit > 0:
                    root.destroy()
                    return

            def iReset():
                self.txtName.delete(0,END)
                self.txtPrice.delete(0,END)

            def iAddData():
                iCheck()
                if name.get()=="":
                    tkinter.messagebox.showwarning("Σύστημα","Δεν έχετε προσθέσει τον αριθμό απόδειξης...")
                else:
                    addProfit(name.get(),price.get())                
                    iDisplay()
    
            def iDisplay():
                result = viewProfits()
                if len(result)!=0:
                    self.productlist.delete(*self.productlist.get_children())
                    for row in result:
                        self.productlist.insert('',END,values=row)

            def iDelete():    
                iDeleteMessage = tkinter.messagebox.askyesno("Σύστημα","Θέλετε σίγουτα να κάνετε Διαγραφή;")
                if iDeleteMessage>0:
                    deleteProfit(name.get())
                    tkinter.messagebox.showinfo("Σύστημα","Επιτυχής Διαγραφή")
                    iDisplay()
                    
            def iProfit(e):
                iReset()
                selected = self.productlist.focus()
                values = self.productlist.item(selected,'values')
                self.txtName.insert(0,values[0])
                self.txtPrice.insert(0,values[1])

            def iUpdate():
                iCheck()
                if  name.get()=="":
                    tkinter.messagebox.showwarning("Σύστημα","Δεν έχετε επιλέξει Προμηθευτή")
                else:                
                    updateProfit(name.get(),price.get())                
                    iDisplay()

            def iCheck():
                if price.get().isalpha():
                    tkinter.messagebox.showwarning("Σύστημα","Λάθος στις Οφειλές, εισάγεται αριθμό!!")
            
            #========================================Frames==================================
            MainFrame = Frame(self.root , bd=10, width = 1350, height=700, relief=RIDGE, bg="cadet blue")
            MainFrame.grid()

            TopFrame1 = Frame(MainFrame, bd=5, width = 1340, height=50, relief=RIDGE)
            TopFrame1.grid(row=2,column=0,pady=8)

            TitleFrame = Frame(MainFrame, bd=7, width = 1340, height=100, relief=RIDGE)
            TitleFrame.grid(row=0,column=0)

            TopFrame3 = Frame(MainFrame, bd=5, width = 1340, height=500, relief=RIDGE)
            TopFrame3.grid(row=1,column=0)

            LeftFrame = Frame(TopFrame3, bd=5, width = 1340, height=400, padx=2 , bg="cadet blue", relief=RIDGE)
            LeftFrame.pack(side=LEFT)

            LeftFrame1 = Frame(LeftFrame, bd=5, width = 600, height=180, padx=2,pady=4 , relief=RIDGE)
            LeftFrame1.pack(side=TOP,padx=0,pady=4)

            RightFrame1 = Frame(TopFrame3, bd=5, width=320 , height=400, padx=2, pady=2,relief=RIDGE)
            RightFrame1.pack(side=RIGHT)

            RightFrame1a = Frame(RightFrame1, bd=5, width=310, height=200, padx=2,pady=2,relief=RIDGE)
            RightFrame1a.pack(side=TOP)

            #========================================Title==================================
            self.lblTitle = Label(TitleFrame, font=('arial',56,'bold'),text="Κέρδη επιχείρησης...",bd=7 )
            self.lblTitle.grid(row=0,column=0,padx=132)
            #========================================Widget==================================

            self.lblName = Label(LeftFrame1, font=('arial',12,'bold'),text="Μοναδικός Κωδικός Απόδειξης",bd=7,anchor=W,justify=LEFT )
            self.lblName.grid(row=0,column=0, sticky=W , padx=5)
            self.txtName = Entry(LeftFrame1, font=('arial',10,'bold'),bd=5,width=40,justify=LEFT, textvariable=name )
            self.txtName.grid(row=0,column=1)

            self.lblPrice = Label(LeftFrame1, font=('arial',12,'bold'),text="Ποσό €",bd=7,anchor=W,justify=LEFT )
            self.lblPrice.grid(row=1,column=0, sticky=W , padx=5)
            self.txtPrice = Entry(LeftFrame1, font=('arial',10,'bold'),bd=5,width=40,justify=LEFT, textvariable=price )
            self.txtPrice.grid(row=1,column=1)

            #========================================TreeView==================================
            scroll_x = Scrollbar(RightFrame1a, orient=HORIZONTAL)
            scroll_y = Scrollbar(RightFrame1a, orient=VERTICAL)

            self.productlist = ttk.Treeview(RightFrame1a,height=12,columns=("name","price"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

            scroll_x.pack(side=BOTTOM,fill=X)
            scroll_y.pack(side=RIGHT,fill=Y)

            self.productlist.heading("#0", text="")
            self.productlist.heading("name",text="Μοναδικός Κωδικός Απόδειξης")
            self.productlist.heading("price",text="Ποσό €")

            self.productlist['show'] = 'headings'

            self.productlist.column("#0", width=0)
            self.productlist.column("name",width=200)
            self.productlist.column("price",width=200)

            self.productlist.pack(fill=BOTH,expand=1)

            self.productlist.bind("<ButtonRelease-1>",iProfit)
            iDisplay()
            #========================================Buttons==================================
            self.btnAddNew = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Προσθήκη",padx=24, width=12, height=2, command=iAddData).grid(row=0,column=0, padx=1)

            self.btnDisplay = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Καθαρισμός",padx=24, width=12, height=2, command=iReset).grid(row=0,column=1, padx=1)

            self.btnReset = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Αλλαγή",padx=24, width=12, height=2, command=iUpdate).grid(row=0,column=2, padx=1)
            
            self.btnDelete = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Διαγραφή",padx=24, width=12, height=2, command=iDelete).grid(row=0,column=3, padx=1)

            self.btnExit = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Έξοδος",padx=24, width=12, height=2, command=self.root.destroy).grid(row=0,column=4, padx=1)
    Profit()

def openProducts():
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Backend!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    class Products(Frame):
            def __init__(self):
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Frontend!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
                self.root = Toplevel()
                blank_space = " "
                self.root.title(200 * blank_space + "A U R U M ")
                self.root.geometry("1350x600+200+200")

                barcode = StringVar()
                name = StringVar()
                buy_price = StringVar()
                profit = StringVar()
                #sell_price = DoubleVar()
                quantity = StringVar()
                #========================================FUNCTIONS==================================
                def productData():
                    conn = sqlite3.connect("aurum.db")
                    c = conn.cursor()
                    sql = """CREATE TABLE IF NOT EXISTS
                    products(
                    barcode TEXT,
                    name TEXT,
                    buy_price FLOAT,
                    profit FLOAT,
                    sell_price FLOAT,
                    quantity INTEGER
                    )"""
                    c.execute(sql)
                    conn.commit()
                    conn.close()

                def addProduct (barcode, name, buy_price, profit, sell_price,quantity):
                    conn = sqlite3.connect("aurum.db")
                    c = conn.cursor()
                    c.execute("INSERT INTO  products VALUES (?,?,?,?,?,?)",(barcode,name,buy_price,profit,sell_price,quantity))
                    conn.commit()
                    conn.close()

                def viewData():
                    conn = sqlite3.connect("aurum.db")
                    c = conn.cursor()
                    c.execute("SELECT * FROM products")
                    rows = c.fetchall()
                    conn.close()
                    return rows

                def deleteData(barcode):
                    conn = sqlite3.connect("aurum.db")
                    c = conn.cursor()
                    c.execute("""DELETE FROM  products
                    WHERE barcode = :barcode """,
                        {
                            'barcode':barcode
                        }
                    )
                    conn.commit()
                    conn.close()

                def updateData(barcode, name, buy_price, profit, sell_price,quantity):
                    conn = sqlite3.connect("aurum.db")
                    c = conn.cursor()
                    c.execute("""UPDATE  products SET
                    barcode = :barcode, 
                    name = :name,
                    buy_price = :buy_price,
                    profit = :profit,
                    sell_price = :sell_price,
                    quantity = :quantity
                    WHERE barcode = :barcode """,
                        {
                            'barcode':barcode,
                            'name':name,
                            'buy_price':buy_price,
                            'profit':profit,
                            'sell_price':sell_price,
                            'quantity':quantity
                        }
                    )
                    conn.commit()
                    conn.close()
                productData()
                def iExit():
                    iExit = tkinter.messagebox.askyesno("Σύστημα","Θέλετε σίγουρα να αποχωρήσετε;")
                    if iExit > 0:
                        root.destroy()
                        return

                def iReset():
                    self.txtBarcode.delete(0,END)
                    self.txtName.delete(0,END)
                    self.txtBuyPrice.delete(0,END)
                    self.txtProfit.delete(0,END)
                    self.txtQuantity.delete(0,END)

            
                def iAddData():
                    iCheck()
                    if barcode.get()=="" or  name.get()=="":
                        tkinter.messagebox.showwarning("Ειδοποίηση Συστήματος","Έχετε κενό το Barcode ή το Όνομα")
                    else:
                        
                        sell_price = float(buy_price.get())+float(buy_price.get())*float(profit.get())
                        addProduct(
                            barcode.get(), 
                            name.get(),
                            buy_price.get(),
                            profit.get(), 
                            sell_price,
                            quantity.get()
                            )                
                        iDisplay()
        
                def iDisplay():
                    result = viewData()
                    if len(result)!=0:
                        self.productlist.delete(*self.productlist.get_children())
                        for row in result:
                            self.productlist.insert('',END,values=row)

                def iDelete():    
                    iDeleteMessage = tkinter.messagebox.askyesno("Σύστημα","Θέλετε σίγουτα να κάνετε Διαγραφή;")
                    if iDeleteMessage>0:
                        deleteData(
                            barcode.get()
                            )
                        tkinter.messagebox.showinfo("Σύστημα","Επιτυχής Διαγραφή")
                        iDisplay()
                        
                def iProduct(e):
                    iReset()
                    selected = self.productlist.focus()
                    values = self.productlist.item(selected,'values')
                    self.txtBarcode.insert(0,values[0])
                    self.txtName.insert(0,values[1])
                    self.txtBuyPrice.insert(0,values[2])
                    self.txtProfit.insert(0,values[3])
                    self.txtQuantity.insert(0,values[5])

                def iUpdate():
                    iCheck()
                    if barcode.get()=="" or name.get()=="":
                        tkinter.messagebox.showwarning("Σύστημα","Δεν έχετε επιλέξει Barcode")
                    else:                
                        sell_price = float(buy_price.get())+float(buy_price.get())*float(profit.get())
                        updateData(
                            barcode.get(), 
                            name.get(),
                            buy_price.get(),
                            profit.get(), 
                            sell_price,
                            quantity.get()
                            )                
                        iDisplay()

                def iCheck():
                    if buy_price.get().isalpha():
                        tkinter.messagebox.showwarning("Σύστημα","Λάθος στην Τιμή Αγοράς, εισάγεται αριθμό!!")
                    if profit.get().isalpha():
                        tkinter.messagebox.showwarning("Σύστημα","Λάθος στο Ποσοστό Κέρδους, εισάγεται αριθμό!!")
                    if quantity.get().isalpha():
                        tkinter.messagebox.showwarning("Σύστημα","Λάθος στην Ποσότητα , εισάγεται αριθμό!!")
                
                #========================================Frames==================================
                MainFrame = Frame(self.root , bd=10, width = 1350, height=700, relief=RIDGE, bg="cadet blue")
                MainFrame.grid()

                TopFrame1 = Frame(MainFrame, bd=5, width = 1340, height=50, relief=RIDGE)
                TopFrame1.grid(row=2,column=0,pady=8)

                TitleFrame = Frame(MainFrame, bd=7, width = 1340, height=100, relief=RIDGE)
                TitleFrame.grid(row=0,column=0)

                TopFrame3 = Frame(MainFrame, bd=5, width = 1340, height=500, relief=RIDGE)
                TopFrame3.grid(row=1,column=0)

                LeftFrame = Frame(TopFrame3, bd=5, width = 1340, height=400, padx=2 , bg="cadet blue", relief=RIDGE)
                LeftFrame.pack(side=LEFT)

                LeftFrame1 = Frame(LeftFrame, bd=5, width = 600, height=180, padx=2,pady=4 , relief=RIDGE)
                LeftFrame1.pack(side=TOP,padx=0,pady=4)

                # RightFrame = Frame(TopFrame3, bd=5, width = 310, height=400, padx=2 ,pady=2, bg="cadet blue", relief=RIDGE)
                # RightFrame.pack(side=RIGHT)

                RightFrame1 = Frame(TopFrame3, bd=5, width=320 , height=400, padx=2, pady=2,relief=RIDGE)
                RightFrame1.pack(side=RIGHT)

                RightFrame1a = Frame(RightFrame1, bd=5, width=310, height=200, padx=2,pady=2,relief=RIDGE)
                RightFrame1a.pack(side=TOP)


                #========================================Title==================================
                self.lblTitle = Label(TitleFrame, font=('arial',56,'bold'),text="Η Αποθήκη μου...",bd=7 )
                self.lblTitle.grid(row=0,column=0,padx=132)
                #========================================Widget==================================
                self.lblBarcode = Label(LeftFrame1, font=('arial',12,'bold'),text="Barcode",bd=7,anchor=W,justify=LEFT )
                self.lblBarcode.grid(row=0,column=0, sticky=W , padx=5)
                self.txtBarcode = Entry(LeftFrame1, font=('arial',10,'bold'),bd=5,width=40,justify=LEFT, textvariable=barcode )
                self.txtBarcode.grid(row=0,column=1)

                self.lblName = Label(LeftFrame1, font=('arial',12,'bold'),text="Περιγραφή",bd=7,anchor=W,justify=LEFT )
                self.lblName.grid(row=1,column=0, sticky=W , padx=5)
                self.txtName = Entry(LeftFrame1, font=('arial',10,'bold'),bd=5,width=40,justify=LEFT, textvariable=name )
                self.txtName.grid(row=1,column=1)

                self.lblBuyPrice = Label(LeftFrame1, font=('arial',12,'bold'),text="Τιμή Αγοράς",bd=7,anchor=W,justify=LEFT )
                self.lblBuyPrice.grid(row=2,column=0, sticky=W , padx=5)
                self.txtBuyPrice = Entry(LeftFrame1, font=('arial',10,'bold'),bd=5,width=40,justify=LEFT, textvariable=buy_price )
                self.txtBuyPrice.grid(row=2,column=1)

                self.lblProfit = Label(LeftFrame1, font=('arial',12,'bold'),text="Ποσοστό Κέρδους",bd=7,anchor=W,justify=LEFT )
                self.lblProfit.grid(row=3,column=0, sticky=W , padx=5)
                self.txtProfit = Entry(LeftFrame1, font=('arial',10,'bold'),bd=5,width=40,justify=LEFT, textvariable=profit )
                self.txtProfit.grid(row=3,column=1)

                self.lblQuantity = Label(LeftFrame1, font=('arial',12,'bold'),text="Ποσότητα",bd=7,anchor=W,justify=LEFT )
                self.lblQuantity.grid(row=4,column=0, sticky=W , padx=5)
                self.txtQuantity = Entry(LeftFrame1, font=('arial',10,'bold'),bd=5,width=40,justify=LEFT, textvariable=quantity)
                self.txtQuantity.grid(row=4,column=1)
                #========================================TreeView==================================
                scroll_x = Scrollbar(RightFrame1a, orient=HORIZONTAL)
                scroll_y = Scrollbar(RightFrame1a, orient=VERTICAL)

                self.productlist = ttk.Treeview(RightFrame1a,height=12,columns=("Barcode","name","buy_price","profit","sell_price","quantity"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

                scroll_x.pack(side=BOTTOM,fill=X)
                scroll_y.pack(side=RIGHT,fill=Y)

                self.productlist.heading("#0", text="")
                self.productlist.heading("Barcode",text="Barcode")
                self.productlist.heading("name",text="Περιγραφή")
                self.productlist.heading("buy_price",text="Τιμή Αγοράς")
                self.productlist.heading("profit",text="Ποσοστό Κέρδους")
                self.productlist.heading("sell_price",text="Τιμή Πώλησης")
                self.productlist.heading("quantity",text="Ποσότητα")

                self.productlist['show'] = 'headings'

                self.productlist.column("#0", width=0)
                self.productlist.column("Barcode",width=100)
                self.productlist.column("name",width=200)
                self.productlist.column("buy_price",width=80)
                self.productlist.column("profit",width=110)
                self.productlist.column("sell_price",width=100)
                self.productlist.column("quantity",width=80)

                self.productlist.pack(fill=BOTH,expand=1)

                self.productlist.bind("<ButtonRelease-1>",iProduct)
                iDisplay()
                #========================================Buttons==================================
                self.btnAddNew = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Προσθήκη",padx=24, width=12, height=2, command=iAddData).grid(row=0,column=0, padx=1)

                self.btnDisplay = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Καθαρισμός",padx=24, width=12, height=2, command=iReset).grid(row=0,column=1, padx=1)

                self.btnReset = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Αλλαγή",padx=24, width=12, height=2, command=iUpdate).grid(row=0,column=2, padx=1)
                
                self.btnDelete = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Διαγραφή",padx=24, width=12, height=2, command=iDelete).grid(row=0,column=3, padx=1)

                self.btnExit = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Έξοδος",padx=24, width=12, height=2, command=self.root.destroy).grid(row=0,column=4, padx=1)
    Products()

def openExpenses():
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Backend!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def expensesData():
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        sql = """CREATE TABLE IF NOT EXISTS
        expenses(
        name TEXT,
        price FLOAT
        )"""
        c.execute(sql)
        conn.commit()
        conn.close()
    def addExpenses (name,price):
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("INSERT INTO  expenses VALUES (?,?)",(name,price))
        conn.commit()
        conn.close()
    def viewExpenses():
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("SELECT * FROM expenses")
        rows = c.fetchall()
        conn.close()
        return rows
    def deleteExpenses(name):
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("""DELETE FROM  expenses
        WHERE name = :name """,
            {
                'name':name
            }
        )
        conn.commit()
        conn.close()
    def updateExpenses(name,price):
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("""UPDATE  expenses SET
        name = :name,
        price = :price
        WHERE name = :name """,
            {
                'name':name,
                'price':price
            }
        )
        conn.commit()
        conn.close()
    expensesData()
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Frontend!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    class Expenses:
    
        def __init__(self):
            self.root = Toplevel()
            blank_space = " "
            self.root.title(200 * blank_space + "A U R U M ")
            self.root.geometry("1350x580+200+200")
            name = StringVar()
            price = StringVar()
            #========================================FUNCTIONS==================================
            def iExit():
                iExit = tkinter.messagebox.askyesno("Σύστημα","Θέλετε σίγουρα να αποχωρήσετε;")
                if iExit > 0:
                    root.destroy()
                    return
            def iReset():
                self.txtName.delete(0,END)
                self.txtPrice.delete(0,END)
            def iAddData():
                iCheck()
                if name.get()=="":
                    tkinter.messagebox.showwarning("Σύστημα","Δεν έχετε προσθέσει κάποια περιγραφή στα έξοδα σας")
                else:
                    addExpenses(name.get(),price.get())                
                    iDisplay()

            def iDisplay():
                result = viewExpenses()
                if len(result)!=0:
                    self.productlist.delete(*self.productlist.get_children())
                    for row in result:
                        self.productlist.insert('',END,values=row)

            def iDelete():    
                iDeleteMessage = tkinter.messagebox.askyesno("Σύστημα","Θέλετε σίγουτα να κάνετε Διαγραφή;")
                if iDeleteMessage>0:
                    deleteExpenses(name.get())
                    tkinter.messagebox.showinfo("Σύστημα","Επιτυχής Διαγραφή")
                    iDisplay()
                    
            def iExpenses(e):
                iReset()
                selected = self.productlist.focus()
                values = self.productlist.item(selected,'values')
                self.txtName.insert(0,values[0])
                self.txtPrice.insert(0,values[1])

            def iUpdate():
                iCheck()
                if  name.get()=="":
                    tkinter.messagebox.showwarning("Σύστημα","Δεν έχετε επιλέξει Πειργραφή")
                else:                
                    updateExpenses(name.get(),price.get())                
                    iDisplay()

            def iCheck():
                if price.get().isalpha():
                    tkinter.messagebox.showwarning("Σύστημα","Λάθος στο Ποσό, εισάγεται αριθμό!!")
            
            #========================================Frames==================================
            MainFrame = Frame(self.root , bd=10, width = 1350, height=700, relief=RIDGE, bg="cadet blue")
            MainFrame.grid()

            TopFrame1 = Frame(MainFrame, bd=5, width = 1340, height=50, relief=RIDGE)
            TopFrame1.grid(row=2,column=0,pady=8)

            TitleFrame = Frame(MainFrame, bd=7, width = 1340, height=100, relief=RIDGE)
            TitleFrame.grid(row=0,column=0)

            TopFrame3 = Frame(MainFrame, bd=5, width = 1340, height=500, relief=RIDGE)
            TopFrame3.grid(row=1,column=0)

            LeftFrame = Frame(TopFrame3, bd=5, width = 1340, height=400, padx=2 , bg="cadet blue", relief=RIDGE)
            LeftFrame.pack(side=LEFT)

            LeftFrame1 = Frame(LeftFrame, bd=5, width = 600, height=180, padx=2,pady=4 , relief=RIDGE)
            LeftFrame1.pack(side=TOP,padx=0,pady=4)

            RightFrame1 = Frame(TopFrame3, bd=5, width=320 , height=400, padx=2, pady=2,relief=RIDGE)
            RightFrame1.pack(side=RIGHT)

            RightFrame1a = Frame(RightFrame1, bd=5, width=310, height=200, padx=2,pady=2,relief=RIDGE)
            RightFrame1a.pack(side=TOP)

            #========================================Title==================================
            self.lblTitle = Label(TitleFrame, font=('arial',56,'bold'),text="Έξοδα επιχείρησης...",bd=7 )
            self.lblTitle.grid(row=0,column=0,padx=132)
            #========================================Widget==================================

            self.lblName = Label(LeftFrame1, font=('arial',12,'bold'),text="Περιγραφή",bd=7,anchor=W,justify=LEFT )
            self.lblName.grid(row=0,column=0, sticky=W , padx=5)
            self.txtName = Entry(LeftFrame1, font=('arial',10,'bold'),bd=5,width=40,justify=LEFT, textvariable=name )
            self.txtName.grid(row=0,column=1)

            self.lblPrice = Label(LeftFrame1, font=('arial',12,'bold'),text="Ποσό €",bd=7,anchor=W,justify=LEFT )
            self.lblPrice.grid(row=1,column=0, sticky=W , padx=5)
            self.txtPrice = Entry(LeftFrame1, font=('arial',10,'bold'),bd=5,width=40,justify=LEFT, textvariable=price )
            self.txtPrice.grid(row=1,column=1)

            #========================================TreeView==================================
            scroll_x = Scrollbar(RightFrame1a, orient=HORIZONTAL)
            scroll_y = Scrollbar(RightFrame1a, orient=VERTICAL)

            self.productlist = ttk.Treeview(RightFrame1a,height=12,columns=("name","price"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

            scroll_x.pack(side=BOTTOM,fill=X)
            scroll_y.pack(side=RIGHT,fill=Y)

            self.productlist.heading("#0", text="")
            self.productlist.heading("name",text="Πειγραφη")
            self.productlist.heading("price",text="Ποσό €")

            self.productlist['show'] = 'headings'

            self.productlist.column("#0", width=0)
            self.productlist.column("name",width=200)
            self.productlist.column("price",width=200)

            self.productlist.pack(fill=BOTH,expand=1)

            self.productlist.bind("<ButtonRelease-1>",iExpenses)
            iDisplay()
            #========================================Buttons==================================
            self.btnAddNew = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Προσθήκη",padx=24, width=12, height=2, command=iAddData).grid(row=0,column=0, padx=1)

            self.btnDisplay = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Καθαρισμός",padx=24, width=12, height=2, command=iReset).grid(row=0,column=1, padx=1)

            self.btnReset = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Αλλαγή",padx=24, width=12, height=2, command=iUpdate).grid(row=0,column=2, padx=1)
            
            self.btnDelete = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Διαγραφή",padx=24, width=12, height=2, command=iDelete).grid(row=0,column=3, padx=1)

            self.btnExit = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Έξοδος",padx=24, width=12, height=2, command=self.root.destroy).grid(row=0,column=4, padx=1)
    Expenses()

def openFullView():
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Backend!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def viewSumExpenses():
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("SELECT SUM(price) FROM expenses")
        rows = c.fetchall()
        conn.close()
        return rows
    def viewSumProfits():
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("SELECT SUM(price) FROM profit")
        rows = c.fetchall()
        conn.close()
        return rows

    def viewSumSuppliers():
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("SELECT SUM(price) FROM suppliers")
        rows = c.fetchall()
        conn.close()
        return rows

    def viewSumProductBuy():
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("SELECT SUM(buy_price) FROM products")
        rows = c.fetchall()
        conn.close()
        return rows

    def viewSumProductSell():
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("SELECT SUM(sell_price) FROM products")
        rows = c.fetchall()
        conn.close()
        return rows
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Frontend!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    class FullViewEp:
        
        def __init__(self):
            self.root = Toplevel()
            blank_space = " "
            self.root.title(200 * blank_space + "A U R U M ")
            self.root.geometry("1350x580+200+200")


            name = StringVar()
            price = StringVar()
            
            #========================================FUNCTIONS==================================

            #========================================Frames==================================
            MainFrame = Frame(self.root , bd=10, width = 1350, height=700, relief=RIDGE, bg="cadet blue")
            MainFrame.grid()

            TopFrame1 = Frame(MainFrame, bd=5, width = 1340, height=50, relief=RIDGE)
            TopFrame1.grid(row=2,column=0,pady=8)

            TitleFrame = Frame(MainFrame, bd=7, width = 1340, height=100, relief=RIDGE)
            TitleFrame.grid(row=0,column=0)

            TopFrame3 = Frame(MainFrame, bd=5, width = 1340, height=500, relief=RIDGE)
            TopFrame3.grid(row=1,column=0)
            RightFrame1 = Frame(TopFrame3, bd=5, width=320 , height=400, padx=2, pady=2,relief=RIDGE)
            RightFrame1.pack(side=RIGHT)

            RightFrame1a = Frame(RightFrame1, bd=5, width=1310, height=100, padx=2,pady=2,relief=RIDGE)
            RightFrame1a.pack(side=TOP)

            #========================================Title==================================
            self.lblTitle = Label(TitleFrame, font=('arial',56,'bold'),text="Συνολική Εικόνα Επιχείρησης...",bd=7 )
            self.lblTitle.grid(row=0,column=0,padx=132)
            #========================================TreeView==================================
            scroll_x = Scrollbar(RightFrame1a, orient=HORIZONTAL)
            scroll_y = Scrollbar(RightFrame1a, orient=VERTICAL)

            self.productlist = ttk.Treeview(RightFrame1a,height=9,columns=("name","price"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

            scroll_x.pack(side=BOTTOM,fill=X)
            scroll_y.pack(side=RIGHT,fill=Y)

            self.productlist.heading("#0", text="")
            self.productlist.heading("name",text="Κατηγορία")
            self.productlist.heading("price",text="Ποσό €")

            self.productlist['show'] = 'headings'

            self.productlist.column("#0", width=0)
            self.productlist.column("name",width=500)
            self.productlist.column("price",width=500)

            self.productlist.pack(fill=BOTH,expand=1)

            self.productlist.insert(parent='',index=END,iid=0,values=("Σύνολο Εξόδων Επιχείρησης",viewSumExpenses()))
            self.productlist.configure()
            self.productlist.insert(parent='',index=END,iid=1,values=("Σύνολο Εσόδων Επιχείρησης",viewSumProfits()))
            self.productlist.insert(parent='',index=END,iid=2,values=("Σύνολικό Κόστος Αποθήκης",viewSumProductBuy()))
            self.productlist.insert(parent='',index=END,iid=3,values=("Σύνολική Αξία Αποθήκης",viewSumProductSell()))
            self.productlist.insert(parent='',index=END,iid=4,values=("Συνολικά Χρέη σε Προμηθευτές",viewSumSuppliers()))
            self.productlist.insert(parent='',index=END,iid=5,values=("-------------------------------------","------------------------------"))
            self.btnExit = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Έξοδος",padx=24, width=12, height=2, command=self.root.destroy).grid(row=0,column=4, padx=1)
    FullViewEp()
#---Τέλος Επιχείρησης

#---Σπίτι
def openMonthExpenses():
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Backend!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def monthlyexpensesData():
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        sql = """CREATE TABLE IF NOT EXISTS
        monthlyexpenses(
        name TEXT,
        price FLOAT
        )"""
        c.execute(sql)
        conn.commit()
        conn.close()

    def addmonthlyExpenses (name,price):
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("INSERT INTO  monthlyexpenses VALUES (?,?)",(name,price))
        conn.commit()
        conn.close()

    def viewmonthlyExpenses():
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("SELECT * FROM monthlyexpenses")
        rows = c.fetchall()
        conn.close()
        return rows

    def deletemonthlyExpenses(name):
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("""DELETE FROM  monthlyexpenses
        WHERE name = :name """,
            {
                'name':name
            }
        )
        conn.commit()
        conn.close()


    def updatemonthlyExpenses(name,price):
        conn = sqlite3.connect("aurum.db")
        c = conn.cursor()
        c.execute("""UPDATE  monthlyexpenses SET
        name = :name,
        price = :price
        WHERE name = :name """,
            {
                'name':name,
                'price':price
            }
        )
        conn.commit()
        conn.close()

    monthlyexpensesData()
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Frontend!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    class MonthlyExpenses:
        
        def __init__(self):
            self.root = Toplevel()
            blank_space = " "
            self.root.title(200 * blank_space + "A U R U M ")
            self.root.geometry("1350x580+200+200")


            name = StringVar()
            price = StringVar()
            #========================================FUNCTIONS==================================
            def iExit():
                iExit = tkinter.messagebox.askyesno("Σύστημα","Θέλετε σίγουρα να αποχωρήσετε;")
                if iExit > 0:
                    root.destroy()
                    return

            def iReset():
                self.txtName.delete(0,END)
                self.txtPrice.delete(0,END)

            def iAddData():
                iCheck()
                if name.get()=="":
                    tkinter.messagebox.showwarning("Σύστημα","Δεν έχετε προσθέσει κάποια περιγραφή στα έξοδα σας")
                else:
                    addmonthlyExpenses(name.get(),price.get())                
                    iDisplay()
    
            def iDisplay():
                result = viewmonthlyExpenses()
                if len(result)!=0:
                    self.productlist.delete(*self.productlist.get_children())
                    for row in result:
                        self.productlist.insert('',END,values=row)

            def iDelete():    
                iDeleteMessage = tkinter.messagebox.askyesno("Σύστημα","Θέλετε σίγουτα να κάνετε Διαγραφή;")
                if iDeleteMessage>0:
                    deletemonthlyExpenses(name.get())
                    tkinter.messagebox.showinfo("Σύστημα","Επιτυχής Διαγραφή")
                    iDisplay()
                    
            def iExpenses(e):
                iReset()
                selected = self.productlist.focus()
                values = self.productlist.item(selected,'values')
                self.txtName.insert(0,values[0])
                self.txtPrice.insert(0,values[1])

            def iUpdate():
                iCheck()
                if  name.get()=="":
                    tkinter.messagebox.showwarning("Σύστημα","Δεν έχετε επιλέξει Πειργραφή")
                else:                
                    updatemonthlyExpenses(name.get(),price.get())                
                    iDisplay()

            def iCheck():
                if price.get().isalpha():
                    tkinter.messagebox.showwarning("Σύστημα","Λάθος στο Ποσό, εισάγεται αριθμό!!")
            
            #========================================Frames==================================
            MainFrame = Frame(self.root , bd=10, width = 1350, height=700, relief=RIDGE, bg="cadet blue")
            MainFrame.grid()

            TopFrame1 = Frame(MainFrame, bd=5, width = 1340, height=50, relief=RIDGE)
            TopFrame1.grid(row=2,column=0,pady=8)

            TitleFrame = Frame(MainFrame, bd=7, width = 1340, height=100, relief=RIDGE)
            TitleFrame.grid(row=0,column=0)

            TopFrame3 = Frame(MainFrame, bd=5, width = 1340, height=500, relief=RIDGE)
            TopFrame3.grid(row=1,column=0)

            LeftFrame = Frame(TopFrame3, bd=5, width = 1340, height=400, padx=2 , bg="cadet blue", relief=RIDGE)
            LeftFrame.pack(side=LEFT)

            LeftFrame1 = Frame(LeftFrame, bd=5, width = 600, height=180, padx=2,pady=4 , relief=RIDGE)
            LeftFrame1.pack(side=TOP,padx=0,pady=4)

            RightFrame1 = Frame(TopFrame3, bd=5, width=320 , height=400, padx=2, pady=2,relief=RIDGE)
            RightFrame1.pack(side=RIGHT)

            RightFrame1a = Frame(RightFrame1, bd=5, width=310, height=200, padx=2,pady=2,relief=RIDGE)
            RightFrame1a.pack(side=TOP)

            #========================================Title==================================
            self.lblTitle = Label(TitleFrame, font=('arial',56,'bold'),text="Μηνιαία Έξοδα Σπιτιού...",bd=7 )
            self.lblTitle.grid(row=0,column=0,padx=132)
            #========================================Widget==================================

            self.lblName = Label(LeftFrame1, font=('arial',12,'bold'),text="Περιγραφή",bd=7,anchor=W,justify=LEFT )
            self.lblName.grid(row=0,column=0, sticky=W , padx=5)
            self.txtName = Entry(LeftFrame1, font=('arial',10,'bold'),bd=5,width=40,justify=LEFT, textvariable=name )
            self.txtName.grid(row=0,column=1)

            self.lblPrice = Label(LeftFrame1, font=('arial',12,'bold'),text="Ποσό €",bd=7,anchor=W,justify=LEFT )
            self.lblPrice.grid(row=1,column=0, sticky=W , padx=5)
            self.txtPrice = Entry(LeftFrame1, font=('arial',10,'bold'),bd=5,width=40,justify=LEFT, textvariable=price )
            self.txtPrice.grid(row=1,column=1)

            #========================================TreeView==================================
            scroll_x = Scrollbar(RightFrame1a, orient=HORIZONTAL)
            scroll_y = Scrollbar(RightFrame1a, orient=VERTICAL)

            self.productlist = ttk.Treeview(RightFrame1a,height=12,columns=("name","price"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

            scroll_x.pack(side=BOTTOM,fill=X)
            scroll_y.pack(side=RIGHT,fill=Y)

            self.productlist.heading("#0", text="")
            self.productlist.heading("name",text="Πειγραφη")
            self.productlist.heading("price",text="Ποσό €")

            self.productlist['show'] = 'headings'

            self.productlist.column("#0", width=0)
            self.productlist.column("name",width=200)
            self.productlist.column("price",width=200)

            self.productlist.pack(fill=BOTH,expand=1)

            self.productlist.bind("<ButtonRelease-1>",iExpenses)
            iDisplay()
            #========================================Buttons==================================
            self.btnAddNew = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Προσθήκη",padx=24, width=12, height=2, command=iAddData).grid(row=0,column=0, padx=1)

            self.btnDisplay = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Καθαρισμός",padx=24, width=12, height=2, command=iReset).grid(row=0,column=1, padx=1)

            self.btnReset = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Αλλαγή",padx=24, width=12, height=2, command=iUpdate).grid(row=0,column=2, padx=1)
            
            self.btnDelete = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Διαγραφή",padx=24, width=12, height=2, command=iDelete).grid(row=0,column=3, padx=1)

            self.btnExit = Button(TopFrame1, pady=1,bd=4,font=('arial',20,'bold'),text="Έξοδος",padx=24, width=12, height=2, command=self.root.destroy).grid(row=0,column=4, padx=1)
    MonthlyExpenses()

def openDailyExpenses():
    print("")

def openSalary():
    print("")

def openHouseView():
    print("")
   
#---Τέλος Σπιτιού

color = {"nero": "#252726" , 
        "orange": "#FF8700" , 
        "darkorange": "#FE6101",
        "kyan": "#00FFFF",
        "Glacial Blue Ice": "#3B9C9C",
        "green": "#728C00",
        "light green": "#99C68E",
        "Vanilla" : "#F3E5AB",
        "white": "#ffffff"
        }


root = Tk()
root.title("Aurum")
root.config(bg="gray17")
root.geometry("1100x900+400+30")

#setting switch state
#btnState = False
#loading Navbar icon image
#navIcon = PhotoImage(file='C:\\Users\\paulo\\Desktop\\Python Projects\\Training\\menu.png')
#closeIcon = PhotoImage(file='C:\\Users\\paulo\\Desktop\\Python Projects\\Training\\close.png')
#brandLabel = Label(root,
#    text="A u r u m",
#    font="System 30",
#    bg="gray17",
#    fg="green")
#brandLabel.place(x=450, y=00)

companyIcon = PhotoImage(file='C:\\Users\\paulo\Desktop\\Python Projects\Training\\company.png')
homeIcon = PhotoImage(file='C:\\Users\\paulo\Desktop\\Python Projects\Training\\home.png')
brandIcon = PhotoImage(file='C:\\Users\\paulo\Desktop\\Python Projects\Training\\aurum.png')

class HoverButton1(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground

class HoverButton2(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground


LabelBrand = Label(root ,image=brandIcon, pady=1,bd=0,padx=0,width=300,height=380).place(x=430,y=20)


Label1 = Label(root, bg=color["light green"],bd=0 ,text="Οικία", padx=0 ,pady=1,height=4, width=60, font=('arial',13,'bold')).place(x=200,y=430)
LabelIcon1 = Label(root, bg=color["light green"] ,image=homeIcon, pady=1,bd=0,padx=0,width=200,height=78).place(x=750,y=430)
btn11 = HoverButton1(root, pady=1,activebackground=color["Glacial Blue Ice"],bg=color["green"],bd=4,font=('arial',13,'bold'),text="Καθημερινά Έξοδα",padx=24, width=12, height=2, command=openDailyExpenses).place(x=50,y=530)
btn12 = HoverButton1(root, pady=1,activebackground=color["Glacial Blue Ice"],bg=color["green"],bd=4,font=('arial',13,'bold'),text="Μηνιαίες Δαπάνες",padx=24, width=12, height=2, command=openMonthExpenses).place(x=330,y=530)
btn13 = HoverButton1(root, pady=1,activebackground=color["Glacial Blue Ice"],bg=color["green"],bd=4,font=('arial',13,'bold'),text="Συνολικά Χρήματα",padx=24, width=12, height=2, command=openSalary).place(x=610,y=530)
btn14 = HoverButton1(root, pady=1,activebackground=color["Glacial Blue Ice"],bg=color["green"],bd=4,font=('arial',13,'bold'),text="Γενική Εικόνα",padx=24, width=12, height=2, command=openHouseView).place(x=890,y=530)

Label2 = Label(root, bg=color["Vanilla"],bd=0 ,text="Επιχείρηση", padx=0 ,pady=1,height=4, width=60, font=('arial',13,'bold')).place(x=200,y=610)
LabelIcon2 = Label(root, bg=color["Vanilla"] ,image=companyIcon, pady=1,bd=0,padx=0,width=200,height=78).place(x=750,y=610)
btn21 = HoverButton2(root, pady=1,activebackground='green',bg=color["orange"],bd=4,font=('arial',13,'bold'),text="Προϊόντα",padx=24, width=12, height=2, command=openProducts).place(x=50,y=730)
btn22 = HoverButton2(root, pady=1,activebackground='green',bg=color["orange"],bd=4,font=('arial',13,'bold'),text="Προμηθευτές",padx=24, width=12, height=2, command=openSuppliers).place(x=260,y=730)
btn23 = HoverButton2(root, pady=1,activebackground='green',bg=color["orange"],bd=4,font=('arial',13,'bold'),text="Έσοδα",padx=24, width=12, height=2, command=openProfits).place(x=470,y=730)
btn24 = HoverButton2(root, pady=1,activebackground='green',bg=color["orange"],bd=4,font=('arial',13,'bold'),text="Έξοδα",padx=24, width=12, height=2, command=openExpenses).place(x=680,y=730)
btn25 = HoverButton2(root, pady=1,activebackground='green',bg=color["orange"],bd=4,font=('arial',13,'bold'),text="Γενική Εικόνα",padx=24, width=12, height=2, command=openFullView).place(x=890,y=730)

mainloop()