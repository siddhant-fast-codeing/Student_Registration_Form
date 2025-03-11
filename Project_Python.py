import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
from datetime import date


conn = mysql.connector.connect(host='localhost', user='root', password='', database='student_db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    reg_no INT PRIMARY KEY,
    first_name VARCHAR(50),
    middle_name VARCHAR(50),
    last_name VARCHAR(50),
    course VARCHAR(100),
    certificate_name VARCHAR(100),
    dob DATE,
    gender VARCHAR(10),
    address TEXT,
    pincode VARCHAR(10),
    contact VARCHAR(15),
    email VARCHAR(100),
    aadhar VARCHAR(12),
    form_date DATE
)
''')
conn.commit()


def get_next_reg_no():
    cursor.execute("SELECT MAX(reg_no) FROM students")
    max_reg_no = cursor.fetchone()[0]
    return (max_reg_no + 1) if max_reg_no else 101 


root = tk.Tk()
root.title("Student Registration Form")
root.geometry("800x850")
root.configure(bg="#f0f0f0")


title_label = tk.Label(root, text="Student Registration Form", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=10)

frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
frame.pack(pady=10)


reg_no_var = tk.StringVar(value=str(get_next_reg_no()))
fname_var = tk.StringVar()
mname_var = tk.StringVar()
lname_var = tk.StringVar()
course_var = tk.StringVar()
cert_name_var = tk.StringVar()
dob_var = tk.StringVar()
gender_var = tk.StringVar()
address_var = tk.StringVar()
pincode_var = tk.StringVar()
contact_var = tk.StringVar()
email_var = tk.StringVar()
aadhar_var = tk.StringVar()
form_date_var = tk.StringVar(value=str(date.today()))

fields = ["Registration No", "First Name", "Middle Name", "Last Name", "Course", "Name on Certificate", 
          "Date of Birth", "Gender", "Address", "Pincode", "Contact Number", "Email", "Aadhar Number", "Date of Form Filling"]

variables = [reg_no_var, fname_var, mname_var, lname_var, course_var, cert_name_var, dob_var,
             gender_var, address_var, pincode_var, contact_var, email_var, aadhar_var, form_date_var]

entries = {}


courses = ["B.Tech", "MCA", "MBA", "BBA", "BCA"]

for i, field in enumerate(fields):
    tk.Label(frame, text=field + ":", font=("Arial", 12), bg="#ffffff").grid(row=i, column=0, sticky="w", pady=5)
    if field == "Course":
        entry = ttk.Combobox(frame, textvariable=variables[i], values=courses, font=("Arial", 12), width=28, state="readonly")
    elif field == "Date of Birth":
        entry = DateEntry(frame, textvariable=variables[i], font=("Arial", 12), width=28, date_pattern='yyyy-mm-dd')
    elif field == "Gender":
        entry = tk.Frame(frame, bg="#ffffff")
        tk.Radiobutton(entry, text="Male", variable=gender_var, value="Male", font=("Arial", 12), bg="#ffffff").pack(side="left", padx=5)
        tk.Radiobutton(entry, text="Female", variable=gender_var, value="Female", font=("Arial", 12), bg="#ffffff").pack(side="left", padx=5)
    else:
        entry = tk.Entry(frame, textvariable=variables[i], font=("Arial", 12), width=30)
        if field == "Date of Form Filling":
            entry.config(state='readonly', bg="#eaeaea")
    entry.grid(row=i, column=1, pady=5)
    entries[field] = entry


def add_student():
    try:
        cursor.execute('''INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                    (reg_no_var.get(), fname_var.get(), mname_var.get(), lname_var.get(), course_var.get(),
                     cert_name_var.get(), dob_var.get(), gender_var.get(), address_var.get(), pincode_var.get(),
                     contact_var.get(), email_var.get(), aadhar_var.get(), form_date_var.get()))
        conn.commit()
        messagebox.showinfo("Success", "Student Registered Successfully")
        reg_no_var.set(str(get_next_reg_no()))  
    except Exception as e:
        messagebox.showerror("Error", f"Could not add student: {e}")

def update_student():
    cursor.execute('''UPDATE students SET first_name=%s, middle_name=%s, last_name=%s, course=%s, 
                      certificate_name=%s, dob=%s, gender=%s, address=%s, pincode=%s, contact=%s, 
                      email=%s, aadhar=%s, form_date=%s WHERE reg_no=%s''', 
                   (fname_var.get(), mname_var.get(), lname_var.get(), course_var.get(), cert_name_var.get(), 
                    dob_var.get(), gender_var.get(), address_var.get(), pincode_var.get(), contact_var.get(), 
                    email_var.get(), aadhar_var.get(), form_date_var.get(), reg_no_var.get()))
    conn.commit()
    messagebox.showinfo("Success", "Student Record Updated")

def delete_student():
    cursor.execute("DELETE FROM students WHERE reg_no=%s", (reg_no_var.get(),))
    conn.commit()
    messagebox.showinfo("Success", "Student Record Deleted")
    clear_fields()
    reg_no_var.set(str(get_next_reg_no())) 

def display_student():
    cursor.execute("SELECT * FROM students WHERE reg_no=%s", (reg_no_var.get(),))
    record = cursor.fetchone()
    if record:
        for i, var in enumerate(variables[1:]):
            var.set(record[i + 1])
    else:
        messagebox.showwarning("Not Found", "No student found with this registration number")
        clear_fields()

def clear_fields():
    for var in variables[1:]:
        var.set("")
    form_date_var.set(str(date.today())) 
    
import subprocess

def backup_database():
    mysql_bin_path = "C:\\xampp\\mysql\\bin\\mysqldump.exe"
    db_name = "oes2"
    db_user = "root"
    db_pass = ""
    backup_path = "D:\Python Project Database Back & Restore\\student_db.sql"
    
    command = [
        mysql_bin_path,
        f"--user={db_user}",
        f"--password={db_pass}",
        db_name,
        f"--result-file={backup_path}"
    ]
    
    try:
        process = subprocess.run(command, capture_output=True, text=True)
        if process.returncode == 0:
            messagebox.showinfo("Success", "Database Backup Successfully")
        else:
            messagebox.showerror("Error", f"Database Backup Failed: {process.stderr}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def restore_database():
    mysql_bin_path = "C:\\xampp\\mysql\\bin\\mysql.exe"
    db_name = "oes2"
    db_user = "root"
    db_pass = ""
    backup_path = "D:\\Python Project Database Back & Restore\\student_db.sql"
    
    command = [
        mysql_bin_path,
        f"--user={db_user}",
        f"--password={db_pass}",
        db_name,
        "-e",
        f"source {backup_path}"
    ]
    
    try:
        process = subprocess.run(command, capture_output=True, text=True)
        if process.returncode == 0:
            messagebox.showinfo("Success", "Database Restore Successfully")
        else:
            messagebox.showerror("Error", f"Database Restore Failed: {process.stderr}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=0)


tk.Button(button_frame, text="Add", command=add_student, font=("Arial", 12), bg="#4CAF50", fg="white", width=10).grid(row=0, column=0, padx=5, pady=5)
tk.Button(button_frame, text="Update", command=update_student, font=("Arial", 12), bg="#2196F3", fg="white", width=10).grid(row=0, column=1, padx=5, pady=5)
tk.Button(button_frame, text="Delete", command=delete_student, font=("Arial", 12), bg="#f44336", fg="white", width=10).grid(row=0, column=2, padx=5, pady=5)
tk.Button(button_frame, text="Display", command=display_student, font=("Arial", 12), bg="#FF9800", fg="white", width=10).grid(row=0, column=3, padx=5)
tk.Button(button_frame, text="Backup", command=backup_database, font=("Arial", 12), bg="#f44336", fg="white", width=10).grid(row=0, column=4, padx=5, pady=5)
tk.Button(button_frame, text="Restore", command=restore_database, font=("Arial", 12), bg="#FF9800", fg="white", width=10).grid(row=0, column=5, padx=5)

root.mainloop()