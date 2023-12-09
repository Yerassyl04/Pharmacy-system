from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import psycopg2 as pg

#conn=pg.connect(host='localhost',database='Pharmacy', port='5432', user='postgres', password='admin')
            #mycursor=conn.cursor()

def create_connection():
    conn=pg.connect(host='localhost',database='Pharmacy', port='5432', user='postgres', password='admin')
    return conn
# database table medicine columns -------- medicine_name, uses, price, manufacturer,

# listbox of medicine       -----
def view_command():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT medicine_name, uses, price, manufacturer FROM medicine")
    rows = cur.fetchall()
    conn.close()
    list1.delete(0, END)
    for row in rows:
        list1.insert(END, row)

def search_command():
    medname = e1.get()
    uses = e3.get()
    price = e2.get()
    manu = e4.get()
    conn = create_connection()
    cur = conn.cursor()

    query = "SELECT medicine_name, uses, price, manufacturer FROM medicine WHERE TRUE"
    parameters = []

    if medname:
        query += " AND medicine_name LIKE %s"
        parameters.append('%' + medname + '%')

    if uses:
        query += " AND uses LIKE %s"
        parameters.append('%' + uses + '%')

    if price:
        query += " AND price = %s"
        parameters.append(price)

    if manu:
        query += " AND manufacturer LIKE %s"
        parameters.append('%' + manu + '%')

    cur.execute(query, parameters)
    rows = cur.fetchall()
    conn.close()

    list1.delete(0, END)
    for row in rows:
        list1.insert(END, row)

def add_command():
    data = (e1.get(), e2.get(), e3.get(), e4.get())
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO medicine VALUES (%s, %s, %s, %s)", data)
    conn.commit()
    conn.close()

def update_command():
    data = (e2.get(), e3.get(), e4.get(), e1.get())
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE medicine SET price=%s, uses=%s, manufacturer=%s WHERE medicine_name LIKE %s", data)
    conn.commit()
    conn.close()

def delete_command():
    med_id = e1.get()
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM medicine WHERE medicine_name LIKE %s", (med_id,))
    conn.commit()
    conn.close()

#listbox of user ------------

def viewuser_command():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT email, username, password FROM userdata")
    rows = cur.fetchall()
    conn.close()
    list2.delete(0, END)
    for row in rows:
        list2.insert(END, row)


def searchuser_command():
    search_term = usernameEntry.get()
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT email, username, password FROM userdata WHERE username=%s", (search_term,))
    rows = cur.fetchall()
    conn.close()
    list2.delete(0, END)
    for row in rows:
        list2.insert(END, row)


def deleteuser_command():
    user_id = usernameEntry.get()
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM userdata WHERE username LIKE %s", (user_id,))
    conn.commit()
    conn.close()

# page fronendddddddddddd

admin_window=Tk()
admin_window.geometry('1900x1000+50+50')
admin_window.resizable(1,1)
admin_window.wm_title("Admin Page")

bgImage = ImageTk.PhotoImage(file='userpag.png')

bgLabel=Label(admin_window, image=bgImage)
bgLabel.place(x=0, y=0)


def signin_page():
    admin_window.destroy()
    import signin

phar=Label(admin_window, text="Medicine management", font=('Lalita', 40, 'bold'), bg='#c6e8d0', fg='#46af6b')
phar.place(x=1100, y=100)


l1=Label(admin_window, text="Medicine name", font=('Lalita', 16, 'bold'), bg='#c6e8d0', fg='#46af6b')
l1.place(x=1000, y=200)

l2=Label(admin_window, text="Price", font=('Lalita', 16, 'bold'), bg='#c6e8d0', fg='#46af6b')
l2.place(x=1400, y=200)

l3=Label(admin_window, text="Uses", font=('Lalita', 16, 'bold'), bg='#c6e8d0', fg='#46af6b')
l3.place(x=1000, y=250)

l4=Label(admin_window, text="Manufacturer", font=('Lalita', 16, 'bold'), bg='#c6e8d0', fg='#46af6b')
l4.place(x=1400, y=250)

#----------------------------

e1=Entry(admin_window, width=15, font=('Lalita', 16, 'bold'))
e1.place(x=1200, y=200)

e2=Entry(admin_window,  width=15, font=('Lalita', 16, 'bold'))  #price
e2.place(x=1600, y=200)

e3=Entry(admin_window,  width=15, font=('Lalita', 16, 'bold'))
e3.place(x=1200, y=250)

e4=Entry(admin_window, width=15, font=('Lalita', 16, 'bold'))   #manf
e4.place(x=1600, y=250)


list1=Listbox(admin_window, height=30, width=128)
list1.place(x=1000, y=300)

sb1=Scrollbar(admin_window)
sb1.place(x=1767, y=300)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)


sb2=Scrollbar(admin_window)
sb2.place(x=1000, y=700)

list1.configure(xscrollcommand=sb2.set)
sb2.configure(command=list1.xview)

#functionsss -------------------------------------------------

viewButton=Button(admin_window, text="View all",font=('Lilita', 14), width =12, command=view_command, bg='#e7f5eb')
viewButton.place(x=850, y=300)

searchButton=Button(admin_window, text="Search Entry",font=('Lilita', 14), width=12, command=search_command, bg='#e7f5eb')
searchButton.place(x=850, y=350)

addButton=Button(admin_window, text="Add Entry",font=('Lilita', 14), width=12, command=add_command, bg='#e7f5eb')
addButton.place(x=850, y=400)

updateButton=Button(admin_window, text="Update",font=('Lilita', 14), width=12, command=update_command, bg='#e7f5eb')
updateButton.place(x=850, y=450)

deleteButton=Button(admin_window, text="Delete",font=('Lilita', 14), width=12, command=delete_command, bg='#e7f5eb')
deleteButton.place(x=850, y=500)

closeButton=Button(admin_window, text="Log out",font=('Lilita', 14),  width=7, command=signin_page, bg='#46af6b')
closeButton.place(x=25, y=25)

# user labelssss-------------------------------
use=Label(admin_window, text="User management", font=('Lalita', 40, 'bold'), bg='#c6e8d0', fg='#46af6b')
use.place(x=200, y=100)

username=Label(admin_window, text="Enter user name", font=('Lalita', 16, 'bold'), bg='#c6e8d0', fg='#46af6b')
username.place(x=100, y=200)

usernameEntry=Entry(admin_window, width=20, font=('Lalita', 16, 'bold'))
usernameEntry.place(x=300, y=200)

viewuserButton=Button(admin_window, text="View all",font=('Lilita', 14), width =14, command=viewuser_command, bg='#e7f5eb')
viewuserButton.place(x=100, y=300)

searchuserButton=Button(admin_window, text="Search username",font=('Lilita', 14), width=14, command=searchuser_command, bg='#e7f5eb')
searchuserButton.place(x=100, y=350)

deleteuserButton=Button(admin_window, text="Delete user",font=('Lilita', 14), width=14, command=deleteuser_command, bg='#e7f5eb')
deleteuserButton.place(x=100, y=400)



list2=Listbox(admin_window, height=17, width=70)
list2.place(x=290, y=300)

sb11=Scrollbar(admin_window)
sb11.place(x=700, y=300)

list2.configure(yscrollcommand=sb11.set)
sb11.configure(command=list2.yview)

sb22=Scrollbar(admin_window)
sb22.place(x=290, y=520)

list2.configure(xscrollcommand=sb22.set)
sb22.configure(command=list2.xview)



admin_window.mainloop()


