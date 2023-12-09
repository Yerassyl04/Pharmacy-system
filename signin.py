# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# COLORSSS   #c6e8d0 color if bg  #46af6b color of fg
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import psycopg2 as pg

bgPic = None
#funct part
def forget_pass():
    global bgPic
    def change_password():
        if email_entry.get()=='' or password_entry.get()=='' or confirmpass_entry.get()=='':
            messagebox.showerror('Error', 'All Fields Are Required', parent=windows)
        elif password_entry.get()!=confirmpass_entry.get():
            messagebox.showerror('Error', 'Passwords arent matching', parent=windows)
        else:
            conn = pg.connect(host='localhost', database='Pharmacy', port='5432', user='postgres', password='admin')
            mycursor = conn.cursor()

            query = 'select * from userdata where email=%s'
            mycursor.execute(query, (email_entry.get(),))
            row = mycursor.fetchone()
            if row==None:
                messagebox.showerror('Error', 'User with this email doesnt exist', parent=windows)
            else:
                query='update userdata set password=%s where email=%s'
                mycursor.execute(query, (password_entry.get(), email_entry.get()))
                conn.commit()
                conn.close()
                messagebox.showinfo('Succes', 'Password is reset', parent=windows)
                windows.destroy()


    windows = Toplevel()
    windows.title('Change Password')

    bgPic= ImageTk.PhotoImage(file='login.png')
    bg2Label = Label(windows, image=bgPic)
    bg2Label.grid()

    heading_label = Label(windows, text='RESET PASSWORD', font=('Lalita', 40, 'bold'),
                                                                 bg='#c6e8d0', fg='#46af6b')
    heading_label.place(x=1180, y=100)

    emailLabel = Label(windows, text='Email', font=('Lilita', 18), bd=0, bg='#c6e8d0', fg='black')
    emailLabel.place(x=1200, y=180)

    email_entry = Entry(windows, width=25, font=('Lilita', 18), bd=0, bg='#e7f5eb', fg='black')
    email_entry.place(x=1200, y=220)

    Frame(windows, width=350, height=3, bg='green').place(x=1200, y=260)

    passwordLabel = Label(windows, text='New Password', font=('Lilita', 18), bd=0, bg='#c6e8d0', fg='black')
    passwordLabel.place(x=1200, y=280)

    password_entry = Entry(windows, width=25, font=('Lilita', 18), bd=0, bg='#e7f5eb', fg='black')
    password_entry.place(x=1200, y=340)

    Frame(windows, width=350, height=3, bg='green').place(x=1200, y=380)

    confirmpassLabel = Label(windows, text='Confirm Password', font=('Lilita', 18), bd=0, bg='#c6e8d0', fg='black')
    confirmpassLabel.place(x=1200, y=420)

    confirmpass_entry=Entry(windows, width=25, font=('Lilita', 18), bd=0, bg='#e7f5eb', fg='black')
    confirmpass_entry.place(x=1200, y=460)

    Frame(windows, width=350, height=3, bg='green').place(x=1200, y=500)

    submitButton = Button(windows, text='Submit',font=('Lilita', 20),
                        bg='#c6e8d0', fg='black', cursor='hand2', bd=0, width=15, command=change_password)
    submitButton.place(x=1260, y=540)


def login_user():
    if usernameEntry.get() == 'admin' and passwordEntry.get() == 'admin':
        admin_page()
    else:
        if usernameEntry.get()=='' or passwordEntry.get()=='':
             messagebox.showerror('Error', 'All fields are required to fill')

        else:
         try:
             conn = pg.connect(host='localhost', database='Pharmacy', port='5432', user='postgres', password='admin')
             mycursor=conn.cursor()
             pass
         except:
             messagebox.showerror('Error', 'Connection is not established')
             return

         mycursor = conn.cursor()
         query='Select * from userdata where username=%s and password=%s'
         mycursor.execute(query, (usernameEntry.get(), passwordEntry.get()))
         row=mycursor.fetchone()
         if row == None:
            messagebox.showerror('Error', 'Invalid username or password')
         else:
            user_page()

def user_page():
    login_window.destroy()
    import Userpage

def admin_page():
    login_window.destroy()
    import admin

def signup_page():
    login_window.destroy()
    import signup

def user_enter(event):
    if usernameEntry.get()=='Username':
        usernameEntry.delete(0, END)

def password_enter(event):
    if passwordEntry.get()=='Password':
        passwordEntry.delete(0, END)


#main part
login_window = Tk()
login_window.geometry('1900x1000+50+50')
login_window.resizable(1,1)
login_window.title('Login page')

bgImage = ImageTk.PhotoImage(file='login.png')

bgLabel=Label(login_window, image=bgImage)
bgLabel.place(x=0, y=0)


heading=Label(login_window, text='USER LOGIN', font=('Lilita',40, 'bold'), bg='#c6e8d0', fg='#46af6b')
heading.place(x=1180,y=200)

usernameEntry = Entry(login_window, width=25, font=('Lilita', 18), bd=0, bg='#c6e8d0', fg='black')
usernameEntry.place(x=1200, y=320)
usernameEntry.insert(0, 'Username')

usernameEntry.bind('<FocusIn>', user_enter)

frame1 =Frame(login_window, width=300, height=3, bg='green')
frame1.place(x=1200, y=360)

passwordEntry = Entry(login_window, width=25, font=('Lilita', 18), bd=0 ,bg='#c6e8d0', fg='black')
passwordEntry.place(x=1200, y=400)
passwordEntry.insert(0, 'Password')

passwordEntry.bind('<FocusIn>', password_enter)


frame2 =Frame(login_window, width=300, height=3, bg='green')
frame2.place(x=1200, y=440)

forgetButton =Button(login_window,text='Forget password?', bd=0, bg='#c6e8d0',
                     activebackground='#88D8C0', cursor='hand2', font=('Lilita', 14, 'underline'), command=forget_pass)
forgetButton.place(x=1340, y=460)

loginButton= Button(login_window, text='Login', font=('Open Sans', 20, 'bold'),
                    bg='#e7f5eb', fg='black', cursor='hand2', bd=0, width=15, command=login_user)
loginButton.place(x=1220 , y=530)

newaccountButton=Button(login_window, text='Create an account',font=('Lilita', 14, 'underline'),
                    bg='#c6e8d0', fg='black', cursor='hand2', bd=0, width=20, command=signup_page)
newaccountButton.place(x=1300, y=610)


login_window.mainloop()

