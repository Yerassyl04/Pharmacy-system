import requests
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import psycopg2 as pg
from io import BytesIO

# database commands
def create_connection():
    conn=pg.connect(host='localhost',database='Pharmacy', port='5432', user='postgres', password='admin')
    return conn

def signin_page():
    user_window.destroy()
    import signin

def search_command():
    medname = mednameEntry.get()
    uses = usesEntry.get()
    manu = manEntry.get()
    conn = create_connection()
    cur = conn.cursor()

    query = "SELECT med_id, medicine_name, uses, price, manufacturer FROM medicine WHERE TRUE"
    parameters = []

    if medname:
        query += " AND medicine_name LIKE %s"
        parameters.append('%' + medname + '%')

    if uses:
        query += " AND uses LIKE %s"
        parameters.append('%' + uses + '%')

    if manu:
        query += " AND manufacturer LIKE %s"
        parameters.append('%' + manu + '%')

    cur.execute(query, parameters)
    rows = cur.fetchall()
    conn.close()

    list1.delete(0, END)
    for row in rows:
        list1.insert(END, row)


def addbasket():
    selected_item = list1.get(list1.curselection())
    if selected_item:
        basketList.insert(END, selected_item)

def removeitem():
    selected_indices = basketList.curselection()
    if selected_indices:
        for index in selected_indices[::-1]:
            basketList.delete(index)
def price():
    total = 0
    for item in basketList.get(0, END):
        price = float(item[3])
        total += price
    return total

def buyitem():
    total_price = price()
    messagebox.showinfo("Info-show", f"Total Price: ${total_price:.2f}\nThank you for your purchase!")
    basketList.delete(0, END)



# other pagesss--------------------
def aboutus():
    aboutus_window = Toplevel() #new windowww
    aboutus_window.title("About Us")

    img = Image.open("aboutus.png")
    photo = ImageTk.PhotoImage(img)
    label = Label(aboutus_window, image=photo)
    label.image = photo
    label.pack()


def contacts():
    aboutus_window = Toplevel() #new windowww
    aboutus_window.title("Contacts")

    img = Image.open("cont.png")
    photo = ImageTk.PhotoImage(img)
    label = Label(aboutus_window, image=photo)
    label.image = photo
    label.pack()


# main configs
user_window=Tk()
user_window.geometry('1900x1000+50+50')
user_window.resizable(1,1)
user_window.wm_title("User Page")

bgImage = ImageTk.PhotoImage(file='userpag.png')

bgLabel=Label(user_window, image=bgImage)
bgLabel.place(x=0, y=0)


def show_image(event):
    index = list1.curselection()
    if index:
        selected_item = list1.get(index)
        med_id = selected_item[0]

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT image_url FROM medicine WHERE med_id=%s", (med_id,))
        image_url = cursor.fetchone()[0] if cursor.rowcount > 0 else None
        conn.close()

        if image_url:
            response = requests.get(image_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((200, 300))
            photo = ImageTk.PhotoImage(img)

            canvas.delete("all")
            canvas.create_image(0, 0, anchor=NW, image=photo)
            canvas.image = photo



# ---------------------------------------------
phar=Label(user_window, text="Welcome to Jainapharm system", font=('Bandal', 40, 'bold'), bg='#c6e8d0', fg='#385b66')
phar.place(x=500, y=20)

closeButton=Button(user_window, text="Log out",font=('Lilita', 20),  width=7, command=signin_page, bg='#e7f5eb')
closeButton.place(x=25, y=300)

aboutButton=Button(user_window, text="About us",font=('Lilita', 20),  width=7, command=aboutus, bg='#e7f5eb')
aboutButton.place(x=25, y=400)

contButton=Button(user_window, text="Contacts",font=('Lilita', 20),  width=7, command=contacts, bg='#e7f5eb')
contButton.place(x=25, y=500)

# Listboxxx ----------------------------------
list1=Listbox(user_window, height=20, width=100) #bg='#c6e8d0'
list1.place(x=1200, y=350)

list1.bind("<<ListboxSelect>>", show_image)

sb1=Scrollbar(user_window)
sb1.place(x=1781, y=350)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

basketList=Listbox(user_window, height=10, width=100) #bg='#c6e8d0'
basketList.place(x=1200, y=750)

canvas = Canvas(user_window, width=230, height=320, bg='white')
canvas.place(x=900, y=350)

img = PhotoImage(file='familmask.png')
save = Canvas(user_window, width=650, height=500)
save.place(x=200, y=200)
save.create_image(325, 250, image=img)

infLabel=Label(user_window, text="Save your family, save the world!", font=('Lalita', 18, 'bold'), bg='#c6e8d0', fg='#385b66')
infLabel.place(x=300, y=710)

mybasketLabel=Label(user_window, text="My Basket", font=('Lalita', 18, 'bold'), bg='#c6e8d0', fg='#385b66')
mybasketLabel.place(x=1450, y=700)

imageLabel=Label(user_window, text="Medicine image", font=('Lalita', 12, 'bold'), bg='#c6e8d0', fg='#385b66')
imageLabel.place(x=955, y=650)

# med functionsssssssssssssssssss
mednameLabel=Label(user_window, text="Medicine name", font=('Lalita', 18, 'bold'), bg='#c6e8d0', fg='#385b66')
mednameLabel.place(x=900, y=200)

mednameEntry=Entry(user_window, width=15, font=('Lalita', 18, 'bold'))
mednameEntry.place(x=1200, y=200)

usesLabel=Label(user_window, text="Uses", font=('Lalita', 18, 'bold'), bg='#c6e8d0', fg='#385b66')
usesLabel.place(x=900, y=250)

usesEntry=Entry(user_window, width=15, font=('Lalita', 18, 'bold'))   #manf
usesEntry.place(x=1200, y=250)

manLabel=Label(user_window, text="Manufacturer", font=('Lalita', 18, 'bold'), bg='#c6e8d0', fg='#385b66')
manLabel.place(x=900, y=300)

manEntry=Entry(user_window, width=15, font=('Lalita', 18, 'bold'))   #manf
manEntry.place(x=1200, y=300)

searchButton=Button(user_window, text="Search item",font=('Lilita', 14), width=12, command=search_command, bg='#e7f5eb')
searchButton.place(x=1450, y=200)

addbasketButton=Button(user_window, text="Add to basket",font=('Lilita', 14), width=12,  command=addbasket,  bg='#e7f5eb')
addbasketButton.place(x=1450, y=250)

removeButton= Button(user_window, text="Remove item", font=('Lilita', 14), width=12, command=removeitem, bg='#e7f5eb')
removeButton.place(x=1000, y=750)

buyButton = Button(user_window, text="Buy Items", font=('Lilita', 14), width=12, command=buyitem, bg='#e7f5eb')
buyButton.place(x=1000, y=800)

user_window.mainloop()