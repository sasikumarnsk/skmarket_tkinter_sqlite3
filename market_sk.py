import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk
import re
from tkinter import ttk
from PIL import Image, ImageTk


try:
    conn=sqlite3.connect("maindata.db")
    cur=conn.cursor()
    cur.execute("create table main_data(datas)")
    

    try:
        
        def create():
            market_name=market_name_entry.get()
            admin_name=admin_name_entry.get()
            admin_id=admin_id_entry.get()
            password=admin_password_entry.get()
            repassword=admin_confirm_password_entry.get()
            password_hint=passwordhint_entry.get()
            if market_name !="" and admin_name !="" and admin_id!="" and password!="" and repassword!="" and password_hint!="":
                if password==repassword and len(password)>5:
                    
                    conn=sqlite3.connect(market_name+".db")
                    cur=conn.cursor()
                    cur.execute("create table admin_details(market_name,name,id,password,hint)")
                    cur.execute("insert into admin_details(market_name,name,id,password,hint)values(?,?,?,?,?)",(market_name,admin_name,admin_id,password,password_hint))
                    cur.execute("create table product_details(name,id,price,quantity)")
                    cur.execute("create table register_data(name,user_id,mbl_num,mailid,password,re_password,qestion,answer)")
                    cur.execute("create table admin_accept_data(name,user_id,mbl_num,mailid,password,re_password,qestion,answer)")
                    cur.execute("create table sales_data(product_name,id,price)")
                    conn.commit()
                    conn=sqlite3.connect("maindata.db")
                    cur=conn.cursor()
                    cur.execute("insert into main_data(datas)values(?)",(market_name,))
                    conn.commit()
                    app.destroy()
                else:
                    m=messagebox.askquestion("REGISTER ADMIN","CONFIRM PASSWORD IS RONG ")
                    
            else:
                m=messagebox.askquestion("REGISTER ADMIN","CHEK YOUR ENTRES")

            
          
        app=tk.Tk()
        app.geometry("700x500")
        app.resizable(width=False,height=False)
        app.title("CREATE MARKET ELEMENT")
        market_name_label=tk.Label(app,text="MARKET NAME",font=("italic",14,"bold"),)
        market_name_label.place(x=50,y=50)
       
        admin_name_label=tk.Label(app,text="ADMIN NAME",font=("italic",14,"bold"))
        admin_name_label.place(x=50,y=100)
        admin_id_label=tk.Label(app,text="ADMIN ID",font=("italic",14,"bold"))
        admin_id_label.place(x=50,y=150)
        admin_password_label=tk.Label(app,text="PASSWORD",font=("italic",14,"bold"))
        admin_password_label.place(x=50,y=200)
        admin_confirm_password_label=tk.Label(app,text="CONFIRM PASSWORD",font=("italic",13,"bold"))
        admin_confirm_password_label.place(x=50,y=250)
        admin_password_hint_label=tk.Label(app,text="PASSWORD HINT",font=("italic",14,"bold"))
        admin_password_hint_label.place(x=50,y=300)
        
        market_name_entry=tk.Entry(app)
        market_name_entry.place(x=250,y=53,width=170,height=24)
        admin_name_entry=tk.Entry(app)
        admin_name_entry.place(x=250,y=103,width=170,height=24)
        admin_id_entry=tk.Entry(app)
        admin_id_entry.place(x=250,y=153,width=170,height=24)
        admin_password_entry=tk.Entry(app)
        admin_password_entry.place(x=250,y=203,width=170,height=24)
        admin_confirm_password_entry=tk.Entry(app)
        admin_confirm_password_entry.place(x=250,y=253,width=170,height=24)
        passwordhint_entry=tk.Entry(app)
        passwordhint_entry.place(x=250,y=303,width=170,height=24)

        create_button=tk.Button(app,text="CREATE",font=("italic",12,"bold"),bg="green",command=create)
        create_button.place(x=280,y=370)
        app.mainloop()
    except:
        pass
except:
    pass
conn=sqlite3.connect("maindata.db")
cur=conn.cursor()
cur.execute("select * from main_data")
data_base=cur.fetchone()
#print(data_base)
conn=sqlite3.connect(data_base[0]+".db")
cur=conn.cursor()


class billpage():

    no_of_product=0
    def __init__(self,root):
      
        def listbox_update(data):
            self.listbox.delete(0, 'end')
            data = sorted(data, key=str.lower)
            for item in data:
                self.listbox.insert('end', item)

        def on_keyrelease(event=0):
            Component = event.widget.get()
            query = str(
                "SELECT " + "_rowid_" + ",* FROM " + "main" + "." + "product_details" + " WHERE " + "name" +
                " LIKE '%" + Component + "%' ESCAPE '\\' ORDER BY " + "_rowid_" + " ASC LIMIT 0, 49999;")
      
            cur.execute(query)
            sk = cur.fetchall()
            search_list = []
            j = 0
            for i in sk:
                search_list.append(sk[j][1])
                j += 1
            listbox_update(search_list)

        def on_select(event):
            try:
                en_text.set(event.widget.get(event.widget.curselection()))
            except:
                pass
        def finish_bill():
            self.product_list_box.insert("","end",values=("_","_","_","_","TOTAL=",sum(total_price)))
        def add(event=None):
            try:
                self.quantity_entry_warning_label.destroy()
            except:
                pass
            
            try:    
                product=self.entry.get()
                quantity=self.combo_box.get()
                if(quantity==""):
                    #print(event)

                    self.quantity_entry_warning_label=tk.Label(root,bg="red",font=("italic",15,"bold"),text="ENTER QUANITITY")
                    self.quantity_entry_warning_label.place(x=690,y=300)
                    
                cur.execute("select * from product_details where name=?",(product,))
                product_detail=cur.fetchone()
            except:
                pass

            try:
                quantity=int(quantity)
                price=int(product_detail[2])
                total=quantity*price
                total_price.append(total)
                self.no_of_product+=1
                self.product_list_box.insert("","end",values=(self.no_of_product,product_detail[0],product_detail[1],product_detail[2],quantity,str(total)))
                cur.execute("insert into sales_data(product_name,id,quantity)values(?,?,?)",(product_detail[0],product_detail[1],product_detail[2]))
                conn.commit()
  
            except:
                pass
        root.title("BILL PAGE")
        total_price=[]

        self.product_label=tk.Label(root,bg="yellow",font=("italic",18,"bold"),text="PRODUCT:")
        self.product_label.place(x=100,y=70)
        self.quantity_combo_label=tk.Label(root,bg="yellow",font=("italic",8,"bold"),text="QUANTITY:")
        self.quantity_combo_label.place(x=360,y=78)
        self.combo_box=ttk.Combobox(root)
        self.combo_box['values']=[1,2,3,4,5,6,7,8,9]
        self.combo_box.current(0)
        
        self.combo_box.place(x=360,y=100,width=60,height=26)
        test_list = ()
        en_text = tk.StringVar()
        self.entry = tk.Entry(root, textvariable=en_text)
        self.entry.place(x=100,y=100,height=30,width=260)
        self.entry.bind('<KeyRelease>',on_keyrelease)
        self.listbox = tk.Listbox(root)
        self.listbox.place(x=100,y=135,width=260,height=180)
        self.listbox.bind('<<ListboxSelect>>',on_select)
        listbox_update(test_list)
        
        self.product_details_list_box_label=tk.Label(root,bg="yellow",font=("italic",12,"bold"),text="PRODUCT DETAILS:")
        self.product_details_list_box_label.place(x=500,y=70)

        self.product_list_box=ttk.Treeview(root,show="headings")
        #colum=("NO","PRODUCT NAME","PRODUCT ID","PRICE","QUANITITY","TOTAL")
        self.product_list_box["columns"]=("1","2","3","4","5","6")
        self.product_list_box.column("1",width=40)
        self.product_list_box.column("2",width=100)
        self.product_list_box.column("3",width=60)
        self.product_list_box.column("4",width=40)
        self.product_list_box.column("5",width=40)
        self.product_list_box.column("6",width=40)

        self.product_list_box.heading("1",text="NO")
        self.product_list_box.heading("2",text="PRODUCT NAME")
        self.product_list_box.heading("3",text="PRODUCT ID")
        self.product_list_box.heading("4",text="PRICE")
        self.product_list_box.heading("5",text="QUANTITY")
        self.product_list_box.heading("6",text="TOTAL")


        self.product_list_box.place(x=500,y=120,width=650,height=450)
        
        self.add_button=tk.Button(root,text="add",command=add)
        root.bind("<Key-+>",add)
        self.add_button.place(x=400,y=300)
        self.finish_button=tk.Button(root,bg="orange",font=("italic",10,"bold"),text="FINISH",command=finish_bill)
        self.finish_button.place(x=400,y=400)
        self.log_out_button=tk.Button(root,bg="red",width=8,height=2,font=("italic",7,"bold"),text="LOG OUT",command=self.logout)
        self.log_out_button.place(x=0,y=0)
    def logout(self):
        try:
            self.quantity_entry_warning_label.destroy()
        except:
            pass

        self.log_out_button.destroy()
        self.product_label.destroy()
        self.quantity_combo_label.destroy()
        self.combo_box.destroy()
        self.entry.destroy()
        self.listbox.destroy()
        self.product_details_list_box_label.destroy()
        self.product_list_box.destroy()
        self.add_button.destroy()
        self.finish_button.destroy()
   
        mainpage(root)

            


class adminpage:
    add_win_count=True
    delete_win_count=True
    change_product_price_win_count=True
    user_login_accept_win_count=True
    show_today_sales_win_count=True
    def __init__(self,root):


      
        root.title("ADMIN PAGE")
        self.logout_button = tk.Button(root,bg="gray",width=8,height=2,font=("italic",7,"bold"),text="LOG OUT", command=self.logout)
        self.logout_button.place(x=0,y=0)
        self.daily_sales_button=tk.Button(root,width=15,height=4,bg="white",font=("italic",20,"bold"),text="DAILY SALES",command=self.show_today_sales)
        self.daily_sales_button.place(x=120,y=100)
        self.add_product_button=tk.Button(root,width=15,height=4,bg="white",font=("italic",20,"bold"),text="ADD PRODUCT",command=self.add_product)
        self.add_product_button.place(x=450,y=100)
        self.change_price_button=tk.Button(root,width=15,height=4,bg="white",font=("italic",20,"bold"),text="CHANGE PRODUCT\nPRICE",command=self.change_product_price)
        self.change_price_button.place(x=120,y=300)
        self.delete_product_button=tk.Button(root,width=15,height=4,bg="white",font=("italic",20,"bold"),text="DELETE PRODUCT",command=self.delete_product)
        self.delete_product_button.place(x=450,y=300)
        self.register_accept_button=tk.Button(root,width=15,height=4,bg="white",font=("italic",20,"bold"),text="ACCEPT USER\n LOGIN",command=self.accept_users)
        self.register_accept_button.place(x=800,y=100)
                
    def show_today_sales(self):
        def close_today_sales():
            self.show_today_sales_count=True
            show_today_sales_win.destroy()
        if (self.add_win_count is True and self.delete_win_count is True and self.change_product_price_win_count is True and self.user_login_accept_win_count is True and self.show_today_sales_win_count is True):
            self.show_today_sales_count=False
            show_today_sales_win=tk.Toplevel()
            show_today_sales_win.geometry("350x500")
            show_today_sales_win.resizable(width=False,height=False)
            show_today_sales_win.title("SHOW TODAY SALES")
            label=tk.Label(show_today_sales_win,text="TODAY TOTAL SALES\nRATRE IS",font=("italic",20,"bold"))
            label.place(x=25,y=20)
            cur.execute("select * from sales_data where price")
            sales=cur.fetchone()
            print(sales)
            show_today_sales_win.protocol("WM_DELETE_WINDOW",close_today_sales)
        

                
       
    def add_product(self):
        def close_add_win():
            add_product_win.destroy()
            self.add_win_count=True

        if (self.show_today_sales_win_count is True and self.add_win_count is True and self.delete_win_count is True and self.change_product_price_win_count is True and self.user_login_accept_win_count is True):
            self.add_win_count=False
            add_product_win=tk.Toplevel()
            add_product_win.resizable(width=False,height=False)
            add_product_win.title("ADD PRODUCT")
            add_product_win.geometry("350x500")

            def add_product_data():
               
                name=name_entry.get()
                product_id=id_entry.get()
                price=price_entry.get()
                quantity=quantity_entry.get()
                try:
                    quantity_rong_label.destroy()
                except:
                    pass
                try:
                    price_rong_label.destroy()
                except:
                    pass
                    
            
                if(price.isdigit()):
                    price=int(price)
                    if(quantity.isdigit()):
                        quantity=int(quantity)
                        cur.execute("insert into product_details(name,id,price,quantity)values(?,?,?,?)",
                                (name,product_id,price,quantity))
                        conn.commit()
                        name_entry.delete(0,"end")
                        id_entry.delete(0,"end")
                        price_entry.delete(0,"end")
                        quantity_entry.delete(0,"end")
                        add_complete_label=tk.Label(add_product_win,bg="green",font=("italic",13,"bold"),text="ADD SUCCESFULL")
                        add_complete_label.place(x=10,y=400)

                                
                        
                    else:
                        quantity_rong_label=tk.Label(add_product_win,bg="red",font=("italic",13,"bold"),text="INVALID QUANTITY")
                        quantity_rong_label.place(x=10,y=400)
                            
                           
                else:
                    price_rong_label=tk.Label(add_product_win,bg="red",font=("italic",13,"bold"),text="   INVALID PRICE   ")
                    price_rong_label.place(x=10,y=400)
              
                        
            name_label=tk.Label(add_product_win,text="PRODUCT NAME",font=("italic",15,"bold"))
            name_label.place(x=50,y=40)
            name_entry=tk.Entry(add_product_win)
            name_entry.place(x=50,y=80,width=200,height=30)
            id_label=tk.Label(add_product_win,text="ID",font=("italic",15,"bold"))
            id_label.place(x=50,y=120)
            id_entry=tk.Entry(add_product_win)
            id_entry.place(x=50,y=160,width=200,height=30)
            price_label=tk.Label(add_product_win,text="PRICE",font=("italic",15,"bold"))
            price_label.place(x=50,y=200)
            price_entry=tk.Entry(add_product_win)
            price_entry.place(x=50,y=240,width=200,height=30)
            quantity_label=tk.Label(add_product_win,text="QUANTITY",font=("italic",15,"bold"))
            quantity_label.place(x=50,y=280)
            quantity_entry=tk.Entry(add_product_win)
            quantity_entry.place(x=50,y=320,width=200,height=30)
            add_button=tk.Button(add_product_win,bg="green",font=("italic",15,"bold"),text="ADD",command=add_product_data)
            add_button.place(x=250,y=400)
            add_product_win.protocol("WM_DELETE_WINDOW",close_add_win)
    def delete_product(self):
        def close_delete_win():
            delete_product_win.destroy()
            self.delete_win_count=True
        if (self.show_today_sales_win_count is True and self.add_win_count is True and self.delete_win_count is True and self.change_product_price_win_count is True and self.user_login_accept_win_count is True):
            self.delete_win_count=False
            delete_product_win=tk.Toplevel()
            delete_product_win.resizable(width=False,height=False)
            delete_product_win.title("DELETE PRODUCT")
            delete_product_win.geometry("350x400")

            def delete_product_data():
                    
                name=name_entry.get()
                product_id=id_entry.get()
                cur.execute("select name from product_details where name=?",(name,))
                product=cur.fetchone()
                if product!=None:
                    cur.execute("delete from product_details where name=(?)",(name,))
                    conn.commit()
                    name_entry.delete(0,"end")
                    id_entry.delete(0,"end")
                    
                else:
                    m=messagebox.askquestion("DELETE PRODUCTS","ITEM NOT FOUND")
                     
           

                    
            name_label=tk.Label(delete_product_win,text="PRODUCT NAME",bg="white",font=("italic",15,"bold"))
            name_label.place(x=50,y=50)
            name_entry=tk.Entry(delete_product_win)
            name_entry.place(x=50,y=100,width=200,height=30)

            id_label=tk.Label(delete_product_win,text="ID",bg="white",font=("italic",15,"bold"))
            id_label.place(x=50,y=150)
            id_entry=tk.Entry(delete_product_win)
            id_entry.place(x=50,y=200,width=200,height=30)
            delete_button=tk.Button(delete_product_win,bg="green",font=("italic",15,"bold"),text="DELETE",command=delete_product_data)
            delete_button.place(x=180,y=300)
            delete_product_win.protocol("WM_DELETE_WINDOW",close_delete_win)
            
    def change_product_price(self):
        def close_change_product_price_win():
            change_price_win.destroy()
            self.change_product_price_win_count=True

                
        if (self.show_today_sales_win_count is True and self.add_win_count is True and self.delete_win_count is True and self.change_product_price_win_count is True and self.user_login_accept_win_count is True):
            self.change_product_price_win_count=False
            change_price_win=tk.Toplevel()
            change_price_win.title("DELETE PRODUCT")
            change_price_win.resizable(width=False,height=False)
            change_price_win.geometry("350x400")
                

                    
            def change_price():
                name=name_entry.get()
                product_id=id_entry.get()
                price=price_entry.get()
                if (price.isdigit()):
                    price=int(price)
                    cur.execute("update product_details set price=? where name=?",(price,name))
                    conn.commit()
                    name_entry.delete(0,"end")
                    id_entry.delete(0,"end")
       
            name_label=tk.Label(change_price_win,text="PRODUCT NAME",bg="white",font=("italic",15,"bold"))
            name_label.place(x=50,y=50)
            name_entry=tk.Entry(change_price_win)
            name_entry.place(x=50,y=100,width=200,height=30)
            id_label=tk.Label(change_price_win,text="ID",bg="white",font=("italic",15,"bold"))
            id_label.place(x=50,y=150)
            id_entry=tk.Entry(change_price_win)
            id_entry.place(x=50,y=200,width=200,height=30)
            price_label=tk.Label(change_price_win,text="PRICE",bg="white",font=("italic",15,"bold"))
            price_label.place(x=50,y=250)
            price_entry=tk.Entry(change_price_win)
            price_entry.place(x=50,y=300,width=200,height=30)
            change_button=tk.Button(change_price_win,bg="green",font=("italic",15,"bold"),text="CHANGE",command=change_price)
            change_button.place(x=150,y=350)
            change_price_win.protocol("WM_DELETE_WINDOW",close_change_product_price_win)
    
    def accept_users(self):

        def close_admin_accept_win():
            admin_accept_win.destroy()
            self.user_login_accept_win_count=True
            
        def chek_and_pass_data():
            cur.execute("select * from admin_accept_data")
            accept_data=cur.fetchall()
            count=len(accept_data)
            if count!=0:
                accept_admin(accept_data[0])
            else:
                info_label=tk.Label(admin_accept_win,text="NO USERS REQVEST",font=("italic",18,"bold"))
                info_label.place(x=50,y=150)
                
      
        def accept_admin(data):
            def accept_and_store_database():
                cur.execute("insert into register_data (name,user_id,mbl_num,mailid,password,re_password,qestion,answer)values(?,?,?,?,?,?,?,?)",
                    (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]))
                conn.commit()
 
                cur.execute("delete from admin_accept_data where user_id=(?)",(data[1],))
                conn.commit()
                data_show_label0.destroy()
                data_show_label1.destroy()
                data_show_label2.destroy()
                data_show_label3.destroy()
                accept_button.destroy()
                chek_and_pass_data()
              
            data_show_label0=tk.Label(admin_accept_win,text=("NAME:",data[0]),font=("italic",15,"bold"))
            data_show_label1=tk.Label(admin_accept_win,text=("USERID:",data[1]),font=("italic",15,"bold"))
            data_show_label2=tk.Label(admin_accept_win,text=("MBLNUM:",data[2]),font=("italic",15,"bold"))
            data_show_label3=tk.Label(admin_accept_win,text=("MAILID:",data[3]),font=("italic",15,"bold"))
            data_show_label0.place(x=50,y=10)
            data_show_label1.place(x=50,y=60)
            data_show_label2.place(x=50,y=110)
            data_show_label3.place(x=50,y=160)
            accept_button=tk.Button(admin_accept_win,bg="green",text="ACCEPT",font=("italic",15,"bold"),command=accept_and_store_database)
            accept_button.place(x=120,y=200)


        if(self.show_today_sales_win_count is True and self.add_win_count is True and self.delete_win_count is True and self.change_product_price_win_count is True and self.user_login_accept_win_count is True):
            self.user_login_accept_win_count=False
            admin_accept_win=tk.Toplevel()
            admin_accept_win.resizable(width=False,height=False)
            admin_accept_win.geometry("400x450")
            admin_accept_win.title("USER LOGIN ACCEPT")
      
            
            chek_and_pass_data()
            admin_accept_win.protocol("WM_DELETE_WINDOW",close_admin_accept_win)
        
                    

                
    def logout(self):
        if(self.show_today_sales_win_count is True and self.add_win_count is True and self.delete_win_count is True and self.change_product_price_win_count is True and self.user_login_accept_win_count is True):
            
            self.daily_sales_button.destroy()
            self.add_product_button.destroy()
            self.change_price_button.destroy()
            self.delete_product_button.destroy()
            self.logout_button.destroy()
            self.register_accept_button.destroy()
            mainpage(root)
        else:
            m=messagebox.askokcancel("INFO","CLOSE ALL TABS AND LOGOUT IS SAVE")
class forgot_password:
    def __init__(self,root):
        def forgot_use_old_password():
            name=self.name_entry.get()
            user_id=self.id_number_entry.get()
            cur.execute("select * from register_data where user_id=?",(user_id,))
            user_detail=cur.fetchone()
            if user_detail is None:
                m=messagebox.askokcancel("FORGOT PASSWORD","ID IS RONG ")
                
            else:
                if name==user_detail[0]:
                    old_password=self.old_password_entry.get()
                    if old_password==user_detail[4]:
                        password=self.password_entry.get()
                        repassword=self.re_password_entry.get()
                        if password==repassword and password!="" and len(password)>5:
                            cur.execute("update register_data set password=? where user_id=?",(password,user_id))
                            cur.execute("update register_data set re_password=? where user_id=?",(password,user_id))
                            conn.commit()
                            m=messagebox.askokcancel("FOGOT PASSWORD","SUCCES FORGOT YOUR PASSWORD")
                            if m=="True":
                                self.back_useold_pass()
                            if m=="False":
                                self.back_useold_pass()
                        else:
                            m=messagebox.askokcancel("FOGOT PASSWORD","REMEBER PASSWORD IS RONG")
                    else:
                        m=messagebox.askokcancel("FOGOT PASSWORD","OLD PASSWORD IS RONG")

                        
                else:
                    m=messagebox.askokcancel("FOGOT PASSWORD","USER NAME IS RONG")
                

                            
                        


                    

        self.name_label=tk.Label(root,text="USER NAME",font=("italic",20,"bold"))
        self.id_number_label=tk.Label(root,text="USER ID",font=("italic",20,"bold"))
        self.old_password_label=tk.Label(root,text="OLD PASSWORD",font=("italic",20,"bold"))

        self.password_label=tk.Label(root,text="PASSWORD",font=("italic",20,"bold"))
        self.re_password_label=tk.Label(root,text="CONFIRM PASSWORD",font=("italic",19,"bold"))

        self.name_entry=tk.Entry(root)
        self.id_number_entry=tk.Entry(root)
        self.old_password_entry=tk.Entry(root)
        self.password_entry=tk.Entry(root)
        self.re_password_entry=tk.Entry(root)

        self.name_label.place(x=350,y=100)
        self.name_entry.place(x=650,y=100,width=250,height=30)

        self.id_number_label.place(x=350,y=150)
        self.id_number_entry.place(x=650,y=150,width=250,height=30)
        self.old_password_label.place(x=350,y=200)
        self.old_password_entry.place(x=650,y=200,width=250,height=30)
        self.password_label.place(x=350,y=250)
        self.password_entry.place(x=650,y=250,width=250,height=30)

        self.re_password_label.place(x=350,y=300)
        self.re_password_entry.place(x=650,y=300,width=250,height=30)
        self.oldpass_forgot_button=tk.Button(root,bg="gray",width=10,height=2,font=("italic",10,"bold"),text="FORGOT",command=forgot_use_old_password)
        self.oldpass_forgot_button.place(x=580,y=370)
        self.back_button=tk.Button(root,bg="gray",width=8,height=2,font=("italic",7,"bold"),text="BACK",command=self.back_useold_pass)
        self.back_button.place(x=0,y=0)
        self.forgot_another_way_button=tk.Button(root,bg="yellow",width=20,height=2,font=("italic",10,"bold"),text="FORGOT another way",command=self.goto_another_way_pass)
        self.forgot_another_way_button.place(x=850,y=500)            
        


    def goto_another_way_pass(self):
        self.name_label.destroy()
        self.id_number_label.destroy()
        self.old_password_label.destroy()
        self.password_label.destroy()
        self.re_password_label.destroy()
        self.name_entry.destroy()
        self.id_number_entry.destroy()
        self.old_password_entry.destroy()
        self.password_entry.destroy()
        self.re_password_entry.destroy()
        self.oldpass_forgot_button.destroy()
        self.back_button.destroy()
        self.forgot_another_way_button.destroy()
        
        def forgot_another_way():
            
            def forgot_entrys():
                def forgot_password_finally():
                    def change_to_database():
                        password=self.password_entry.get()
                        repassword=self.re_password_entry.get()
                        if password==repassword:
                            cur.execute("update register_data set password=? where user_id=?",(password,user_id))
                            cur.execute("update register_data set re_password=? where user_id=?",(password,user_id))
                            conn.commit()
                            m=messagebox.askquestion("FOGOT PASSWORD","SUCCES FORGOT YOUR PASSWORD")
                            if m=="yes":
                                self.back()
                            
                        else:
                            m=messagebox.askokcancel("FOGOT PASSWORD","REMEBER PASSWORD IS RONG")
                            
                    answer=self.answer_entry.get()
                    if answer==user_detail[7]:
                        self.forgot_button.destroy()
                        self.password_label=tk.Label(root,text="PASSWORD",font=("italic",20,"bold"))
                        self.re_password_label=tk.Label(root,text="CONFIRM PASSWORD",font=("italic",19,"bold"))
                        self.password_entry=tk.Entry(root)
                        self.re_password_entry=tk.Entry(root)
                        
                        self.password_label.place(x=350,y=350)
                        self.password_entry.place(x=650,y=350,width=250,height=30)

                        self.re_password_label.place(x=350,y=400)
                        self.re_password_entry.place(x=650,y=400,width=250,height=30)
                        self.confirm_forgot=tk.Button(root,bg="red",width=10,height=2,font=("italic",10,"bold"),text="FORGOT",command=change_to_database)
                        self.confirm_forgot.place(x=500,y=450)
                   
                name=self.name_entry.get()
                user_id=self.id_number_entry.get()
                mailid=self.emailid_entry.get()
                cur.execute("select * from register_data where user_id=?",(user_id,))
                user_detail=cur.fetchone()
                if user_detail is None:
                    m=messagebox.askokcancel("FORGOT PASSWORD","ID IS RONG ")
                    
                else:
                    if name==user_detail[0] and mailid==user_detail[3]:
                        self.forgot_date_check_button.destroy()    
                        self.qestion_label=tk.Label(root,text=user_detail[6],font=("italic",20,"bold"))
                        self.qestion_label.place(x=350,y=250)
                        self.answer_entry=tk.Entry(root)
                        self.answer_entry.place(x=350,y=300,width=350,height=30)
                        self.forgot_button=tk.Button(root,bg="green",width=10,height=2,font=("italic",10,"bold"),text="FORGOT",command=forgot_password_finally)
                        self.forgot_button.place(x=500,y=350)
                        
                            
                    else:
                        m=messagebox.askokcancel("FORGOT PASSWORD","CHECK NAME AND MAILID")

            root.title("FORGOT PASSWORD")
            self.name_label=tk.Label(root,text="USER NAME",font=("italic",20,"bold"))
            self.id_number_label=tk.Label(root,text="USER ID",font=("italic",20,"bold"))
            self.emailid_label=tk.Label(root,text="EMAIL ID",font=("italic",20,"bold"))

            self.name_entry=tk.Entry(root)
            self.id_number_entry=tk.Entry(root)
            self.emailid_entry=tk.Entry(root)
                    
            self.name_label.place(x=350,y=100)
            self.name_entry.place(x=650,y=100,width=250,height=30)

            self.id_number_label.place(x=350,y=150)
            self.id_number_entry.place(x=650,y=150,width=250,height=30)

            self.emailid_label.place(x=350,y=200)
            self.emailid_entry.place(x=650,y=200,width=250,height=30)
            self.forgot_data_check_button=tk.Button(root,bg="grey",width=10,height=2,font=("italic",10,"bold"),text="CONFIRM",command=forgot_entrys)
            self.forgot_data_check_button.place(x=550,y=300)
            self.back_button=tk.Button(root,bg="gray",width=8,height=2,font=("italic",7,"bold"),text="BACK",command=self.back)
            self.back_button.place(x=0,y=0)

        forgot_another_way()
        
    def back_useold_pass(self):
        self.name_label.destroy()
        self.id_number_label.destroy()
        self.old_password_label.destroy()
        self.password_label.destroy()
        self.re_password_label.destroy()
        self.name_entry.destroy()
        self.id_number_entry.destroy()
        self.old_password_entry.destroy()
        self.password_entry.destroy()
        self.re_password_entry.destroy()
        self.oldpass_forgot_button.destroy()
        self.back_button.destroy()
        self.forgot_another_way_button.destroy()
        registerpage(root)

     
        
    def back(self):
        self.name_label.destroy()
        self.id_number_label.destroy()
        self.emailid_label.destroy()
        self.name_entry.destroy()
        self.id_number_entry.destroy()
        self.emailid_entry.destroy()
        self.forgot_data_check_button.destroy()
        self.back_button.destroy()
        try:
            self.qestion_label.destroy()
            self.answer_entry.destroy()
            self.forgot_button.destroy()
        except:
            pass
        try:
            self.password_label.destroy()
            self.re_password_label.destroy()
            self.password_entry.destroy()
            self.re_password_entry.destroy()
            self.confirm_forgot.destroy()
        except:
            pass
        registerpage(root)

        
            
        
         
        
        
class registerpage():
    def __init__(self,root):

        def register_data():
            
            name=self.name_entry.get()
            user_id=self.id_number_entry.get()
            mbl_num=self.mbl_number_entry.get()
            mailid=self.emailid_entry.get()
            password=self.password_entry.get()
            re_password=self.re_password_entry.get()
            qestion=self.set_qestion_entry.get()
            answer=self.set_answer_entry.get()
            chek_all_correct=0
            c=0
            mbl_num_str=0
            if(mbl_num.isdigit()):
                mbl_num_str=0
            else:
                mbl_num_str=1
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            def check_mailid(email):
                if(re.search(regex,email)):
                    return "no"
                      
                else:  
                    return "yes"
            mail_is_rong=check_mailid(mailid)
          
                    
            if(name=="" or len(name)<3):
                m=messagebox.askokcancel("REGISTER","USERNAME IS INVALID")
                self.name_entry.delete(0,"end")
                chek_all_correct=1
            elif(user_id=="" or len(user_id)<6):
                m=messagebox.askokcancel("REGISTER","USERID IS INVALID")
                self.id_number_entry.delete(0,"end")
                chek_all_correct=1
            elif(mbl_num=="" or mbl_num_str==1):
                m=messagebox.askokcancel("REGISTER","MOBILENUMBER IS INVALID")
                self.mbl_number_entry.delete(0,"end")
                chek_all_correct=1
            
            elif(mailid=="" or mail_is_rong=="yes"):
                m=messagebox.askokcancel("REGISTER","MAILID IS INVALID")
                self.password_entry.delete(0,"end")
                chek_all_correct=1                

            elif(password=="" or len(password)<6):
                m=messagebox.askokcancel("REGISTER","PASSWORD IS INVALID")
                self.password_entry.delete(0,"end")
                chek_all_correct=1
            elif(re_password=="" or re_password!=password):
                m=messagebox.askokcancel("REGISTER","CONFIRM PASSWORD IS INVALID")
                self.re_password_entry.delete(0,"end")
                chek_all_correct=1
            elif(qestion=="" or len(qestion)<10):
                m=messagebox.askokcancel("REGISTER","CHANGE QESTION")
                self.set_qestion_entry.delete(0,"end")
                chek_all_correct=1
            elif(answer=="" or len(answer)<4):
                m=messagebox.askokcancel("REGISTER","TRY ANOTHER QESTION OR ANSWER")
                self.set_answer_entry.delete(0,"end")
                chek_all_correct=1
            if(chek_all_correct==0):
                
                m=messagebox.askokcancel("REGISTER","SUCCES WAIT FOR ADMIN ACCEPT")

                cur.execute("insert into admin_accept_data(name,user_id,mbl_num,mailid,password,re_password,qestion,answer)values(?,?,?,?,?,?,?,?)",
                    (name,user_id,mbl_num,mailid,password,re_password,qestion,answer))
                conn.commit()
                self.name_entry.delete(0,"end")
                self.id_number_entry.delete(0,"end")
                self.mbl_number_entry.delete(0,"end")
                self.emailid_entry.delete(0,"end")
                self.password_entry.delete(0,"end")
                self.re_password_entry.delete(0,"end")
                self.set_qestion_entry.delete(0,"end")
                self.set_answer_entry.delete(0,"end")

        root.title("REGISTERPAGE")
        
        self.name_label=tk.Label(root,text="USER NAME",font=("italic",20,"bold"))
        self.id_number_label=tk.Label(root,text="USER ID",font=("italic",20,"bold"))
        self.mbl_number_label=tk.Label(root,text="MOBILE NUMBER",font=("italic",20,"bold"))
        self.emailid_label=tk.Label(root,text="EMAIL ID",font=("italic",20,"bold"))
        self.password_label=tk.Label(root,text="PASSWORD",font=("italic",20,"bold"))
        self.re_password_label=tk.Label(root,text="CONFIRM PASSWORD",font=("italic",19,"bold"))
        self.set_qestion_label=tk.Label(root,text="SET QESTION",font=("italic",20,"bold"))
        self.set_answer_label=tk.Label(root,text="ANSWER",font=("italic",20,"bold"))


        self.name_entry=tk.Entry(root)
        self.id_number_entry=tk.Entry(root)
        self.mbl_number_entry=tk.Entry(root)
        self.emailid_entry=tk.Entry(root)
        self.password_entry=tk.Entry(root)
        self.re_password_entry=tk.Entry(root)
        self.set_qestion_entry=tk.Entry(root)
        self.set_answer_entry=tk.Entry(root)
            
        self.name_label.place(x=350,y=100)
        self.name_entry.place(x=650,y=100,width=250,height=30)

        self.id_number_label.place(x=350,y=150)
        self.id_number_entry.place(x=650,y=150,width=250,height=30)

        self.mbl_number_label.place(x=350,y=200)
        self.mbl_number_entry.place(x=650,y=200,width=250,height=30)

        self.emailid_label.place(x=350,y=250)
        self.emailid_entry.place(x=650,y=250,width=250,height=30)

        self.password_label.place(x=350,y=300)
        self.password_entry.place(x=650,y=300,width=250,height=30)

        self.re_password_label.place(x=350,y=350)
        self.re_password_entry.place(x=650,y=350,width=250,height=30)

        self.set_qestion_label.place(x=350,y=400)
        self.set_qestion_entry.place(x=650,y=400,width=250,height=30)
                
                
        self.set_answer_label.place(x=350,y=450)
        self.set_answer_entry.place(x=650,y=450,width=250,height=30)
                
              

        self.register_button=tk.Button(root,bg="grey",width=10,height=2,font=("italic",10,"bold"),text="CONFIRM",command=register_data)
        self.register_button.place(x=700,y=550)
        self.back_button=tk.Button(root,bg="grey",width=8,height=2,font=("italic",7,"bold"),text="BACK",command=self.back)
        self.back_button.place(x=0,y=0)
        self.forgot_password_button=tk.Button(root,bg="red",width=15,height=3,font=("italic",8,"bold"),text="FORGOT PASSWORD",command=self.forgot)
        self.forgot_password_button.place(x=950,y=550)
    def forgot(self):
        self.name_label.destroy()
        self.id_number_label.destroy()
        self.mbl_number_label.destroy()
        self.emailid_label.destroy()
        self.password_label.destroy()
        self.re_password_label.destroy()
        self.name_entry.destroy()
        self.id_number_entry.destroy()
        self.mbl_number_entry.destroy()
        self.emailid_entry.destroy()
        self.password_entry.destroy()
        self.re_password_entry.destroy()
        self.register_button.destroy()
        self.back_button.destroy()
        self.forgot_password_button.destroy()
        self.set_qestion_label.destroy()
        self.set_answer_label.destroy()
        self.set_qestion_entry.destroy()
        self.set_answer_entry.destroy()
        self.forgot_password_button.destroy()
        forgot_password(root)
         
    def back(self):
        self.name_label.destroy()
        self.id_number_label.destroy()
        self.mbl_number_label.destroy()
        self.emailid_label.destroy()
        self.password_label.destroy()
        self.re_password_label.destroy()
        self.name_entry.destroy()
        self.id_number_entry.destroy()
        self.mbl_number_entry.destroy()
        self.emailid_entry.destroy()
        self.password_entry.destroy()
        self.re_password_entry.destroy()
        self.register_button.destroy()
        self.back_button.destroy()
        self.forgot_password_button.destroy()
        self.set_qestion_label.destroy()
        self.set_answer_label.destroy()
        self.set_qestion_entry.destroy()
        self.set_answer_entry.destroy()
        self.forgot_password_button.destroy()
        mainpage(root)

       
    
class mainpage(object):
    def __init__(self,root):
        def bill_page_go(event=None):
            def destroy_mainpage_itms_go_bill_page():
                self.user_namelabel.destroy()
                self.password_label.destroy()
                self.userid_entry.destroy()
                self.password_entry.destroy()
                self.login_button.destroy()
                self.register_button.destroy()
                self.admin_button.destroy()
                self.label.destroy()

                billpage(root)
            try:   
                user_id=self.userid_entry.get()
                password=self.password_entry.get()
                cur.execute("select user_id from register_data where user_id=?",(user_id,))
                user_id=cur.fetchone()
                if user_id!=None:
                    cur.execute("select password from register_data where password=?",(password,))
                    password=cur.fetchone()
                    if password!=None:
                        destroy_mainpage_itms_go_bill_page()
                    else:
                        m=messagebox.askretrycancel("LOGIN","USER PASSWORD IS RONG")
                        if(m==True):
                           
                            self.password_entry.delete(0,"end")
                else:
                    m=messagebox.askretrycancel("LOGIN","USER ID IS RONG")
                    if(m==True):
                        self.userid_entry.delete(0,"end")
                        self.password_entry.delete(0,"end")
            except:
                pass
                
            
            
        def register_page_go():
            self.user_namelabel.destroy()
            self.password_label.destroy()
            self.userid_entry.destroy()
            self.password_entry.destroy()
            self.login_button.destroy()
            self.register_button.destroy()
            self.admin_button.destroy()
            self.label.destroy()
            registerpage(root)

        def chek_admin_login():
            def destroy_mainpage_itms_go_admin_page():
                self.user_namelabel.destroy()
                self.password_label.destroy()
                self.userid_entry.destroy()
                self.password_entry.destroy()
                self.login_button.destroy()
                self.register_button.destroy()
                self.admin_button.destroy()
                self.label.destroy()

                
                adminpage(root)

            
            user_id=self.userid_entry.get()
            password=self.password_entry.get()
            cur.execute("select id from admin_details where id=?",(user_id,))
            user_id=cur.fetchone()
            if user_id!=None:
                cur.execute("select password from admin_details where password=?",(password,))
                password=cur.fetchone()
                if password!=None:
                    destroy_mainpage_itms_go_admin_page()
                else:
                    m=messagebox.askretrycancel("ADMIN","LOGIN PASSWORD IS RONG")
                    if(m==True):
                        self.password_entry.delete(0,"end")
            else:
                m=messagebox.askretrycancel("ADMIN","RONG ID TRY AGAIN")
                if(m==True):
                    self.userid_entry.delete(0,"end")
                    self.password_entry.delete(0,"end")
           
                    
        cur.execute("select market_name from admin_details")
        market_name=cur.fetchone()
        #print(market_name)
        root.title(market_name[0])
        def resize_image(event):
            new_width = event.width
            new_height = event.height
            image = copy_of_image.resize((new_width, new_height))
            photo = ImageTk.PhotoImage(image)
            self.label.config(image = photo)
            self.label.image = photo
        image =Image.open("login3.png")
        copy_of_image = image.copy()
        photo = ImageTk.PhotoImage(image)
        self.label = ttk.Label(root, image = photo)
        self.label.bind('<Configure>',resize_image)
        self.label.pack(fill=tk.BOTH, expand = tk.YES)
        self.user_namelabel=tk.Label(root,text="USER ID",font=("italic",17,"bold"))
        self.password_label=tk.Label(root,text="PASSWORD",font=("italic",17,"bold"))
        self.user_namelabel.place(x=480,y=260)
        self.password_label.place(x=480,y=340)
        self.userid_entry=tk.Entry(root,font=("italic",12,"bold"))
        self.password_entry=tk.Entry(root,show="*",font=(20))

        self.userid_entry.place(x=640,y=260,width=300,height=40)
        self.password_entry.place(x=640,y=340,width=300,height=40)
        
        root.bind("<Return>",bill_page_go)
        self.login_button=tk.Button(root,bg="green",width=25,height=2,font=("italic",12,"bold"),text="LOGIN",command=bill_page_go)
        self.login_button.place(x=640,y=440)
        self.register_button=tk.Button(root,bg="grey",width=20,height=2,font=("italic",12,"bold"),text="REGISTER",command=register_page_go)
        self.register_button.place(x=230,y=480)
        self.admin_button=tk.Button(root,bg="grey",width=25,height=2,font=("italic",12,"bold"),text="ADMIN",command=chek_admin_login)
        self.admin_button.place(x=640,y=520)

                
  
        

    
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    app = mainpage(root)
    root.mainloop()
